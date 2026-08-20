#!/usr/bin/env python3
"""
Layer 1: Deterministic Verification
Implements Algorithm 3 of Chapter 7.

Two things are checked.

  A. Hash verification.  Each record is canonicalised and its SHA-256 digest
     recomputed, then compared against the digest anchored on-chain.  Where no
     anchor file is supplied the script computes and writes the digests, which
     establishes the baseline against which later runs are checked.

  B. Lifecycle integrity.  Four conditions are evaluated over the reconstructed
     event sequence for each credit serial:

       V1  double retirement        the same serial retired more than once
       V2  post-retirement transfer a cancellation dated after a retirement
       V3  quantity breach          retired or cancelled beyond the quantity issued
       V4  disordered timestamps    an event dated before the issuance it follows

Usage
-----
    python layer1_verification.py --data DIR
    python layer1_verification.py --data DIR --anchors anchors.json
    python layer1_verification.py --data DIR --inject          # fault injection

The --inject flag writes four deliberate violations into an in-memory copy of
the corpus, one of each type, and reports whether each is detected.  The corpus
on disk is never modified.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ISSUE = "ACR Issuances"
RETIRE = "ACR Retirements"
CANCEL = "ACR Cancellations"


def find(data_dir, stem):
    """Locate a workbook whose name matches, with a space or an underscore."""
    d = Path(data_dir)
    for name in (stem, stem.replace(" ", "_")):
        for ext in (".xlsx", ".xls"):
            p = d / (name + ext)
            if p.exists():
                return p
    # fall back to a case-insensitive, separator-insensitive search
    want = stem.lower().replace(" ", "").replace("_", "")
    for p in d.glob("*.xls*"):
        if p.stem.lower().replace(" ", "").replace("_", "") == want:
            return p
    raise FileNotFoundError(
        f"could not find a workbook for '{stem}' in {d.resolve()}. "
        f"Files present: {[q.name for q in d.glob('*.xls*')]}")


# ---------------------------------------------------------------------------
# Loading and normalisation
# ---------------------------------------------------------------------------
def _num(series):
    """Coerce a column to numeric, treating unparseable values as zero."""
    return pd.to_numeric(series, errors="coerce").fillna(0)


def load_corpus(data_dir):
    """Read the three event files and normalise them to a common schema."""
    d = Path(data_dir)

    iss = pd.read_excel(find(d, ISSUE))
    iss = pd.DataFrame({
        "project": iss["Project ID"].astype(str).str.strip(),
        "vintage": iss["Vintage"].astype(str).str.strip(),
        "serial": None,
        "quantity": _num(iss["Total Credits Issued"]),
        "date": pd.to_datetime(iss["Date Issued"], errors="coerce"),
        "event": "issuance",
    })

    ret = pd.read_excel(find(d, RETIRE))
    ret = pd.DataFrame({
        "project": ret["Project ID"].astype(str).str.strip(),
        "vintage": ret["Vintage"].astype(str).str.strip(),
        "serial": ret["Offset Credit Serial Numbers"].astype(str).str.strip(),
        "quantity": _num(ret["Quantity of Offset Credits"]),
        "date": pd.to_datetime(ret["Status Effective"], errors="coerce"),
        "event": "retirement",
    })

    can = pd.read_excel(find(d, CANCEL))
    can = pd.DataFrame({
        "project": can["Project ID"].astype(str).str.strip(),
        "vintage": can["Vintage"].astype(str).str.strip(),
        "serial": can["Credit Serial Numbers"].astype(str).str.strip(),
        "quantity": _num(can["Quantity of Credits"]),
        "date": pd.to_datetime(can["Status Effective"], errors="coerce"),
        "event": "cancellation",
    })

    events = pd.concat([iss, ret, can], ignore_index=True)
    events = events[events["project"].notna() & (events["project"] != "nan")]
    return events.reset_index(drop=True)


# ---------------------------------------------------------------------------
# A. Hash verification
# ---------------------------------------------------------------------------
def canonical(row):
    """Canonical string form of a record, so digests are reproducible."""
    date = "" if pd.isna(row["date"]) else row["date"].strftime("%Y-%m-%d")
    return "|".join([
        str(row["project"]), str(row["vintage"]), str(row["serial"]),
        f"{float(row['quantity']):.4f}", date, str(row["event"]),
    ])


def digests(events):
    return {i: hashlib.sha256(canonical(r).encode()).hexdigest()
            for i, r in events.iterrows()}


def verify_hashes(events, anchor_path):
    """Compare recomputed digests against the anchored set."""
    current = digests(events)
    if anchor_path is None or not Path(anchor_path).exists():
        return None, current, "no anchor file: digests computed as baseline"

    anchors = {int(k): v for k, v in json.load(open(anchor_path)).items()}
    checked = matched = 0
    mismatches = []
    for i, h in current.items():
        if i in anchors:
            checked += 1
            if anchors[i] == h:
                matched += 1
            else:
                mismatches.append(i)
    rate = (matched / checked * 100) if checked else 0.0
    return rate, current, f"{matched}/{checked} records matched"


# ---------------------------------------------------------------------------
# B. Lifecycle integrity checks
# ---------------------------------------------------------------------------
def check_v1_double_retirement(events):
    """A serial appearing in more than one retirement event."""
    r = events[(events["event"] == "retirement") & events["serial"].notna()]
    counts = r.groupby("serial").size()
    return sorted(counts[counts > 1].index.tolist())


def check_v2_post_retirement_transfer(events):
    """A cancellation dated after a retirement of the same serial."""
    r = events[(events["event"] == "retirement") & events["date"].notna()]
    c = events[(events["event"] == "cancellation") & events["date"].notna()]
    first_ret = r.groupby("serial")["date"].min()
    hits = []
    for _, row in c.iterrows():
        s = row["serial"]
        if s in first_ret.index and row["date"] > first_ret[s]:
            hits.append((s, first_ret[s].date(), row["date"].date()))
    return hits


def check_v3_quantity_breach(events):
    """Retired plus cancelled exceeding issued, per project and vintage."""
    key = ["project", "vintage"]
    issued = events[events["event"] == "issuance"].groupby(key)["quantity"].sum()
    spent = (events[events["event"].isin(["retirement", "cancellation"])]
             .groupby(key)["quantity"].sum())
    hits = []
    for k, out in spent.items():
        inn = issued.get(k, 0)
        if inn > 0 and out > inn:
            hits.append((k[0], k[1], float(inn), float(out)))
    return hits


def check_v4_disordered_timestamps(events):
    """A retirement or cancellation dated before its project's issuance."""
    key = ["project", "vintage"]
    first_iss = (events[(events["event"] == "issuance") & events["date"].notna()]
                 .groupby(key)["date"].min())
    later = events[events["event"].isin(["retirement", "cancellation"])
                   & events["date"].notna()]
    hits = []
    for _, row in later.iterrows():
        k = (row["project"], row["vintage"])
        if k in first_iss.index and row["date"] < first_iss[k]:
            hits.append((row["project"], row["vintage"],
                         first_iss[k].date(), row["date"].date(), row["event"]))
    return hits


def run_checks(events):
    return {
        "V1 double retirement": check_v1_double_retirement(events),
        "V2 post-retirement transfer": check_v2_post_retirement_transfer(events),
        "V3 quantity breach": check_v3_quantity_breach(events),
        "V4 disordered timestamps": check_v4_disordered_timestamps(events),
    }


# ---------------------------------------------------------------------------
# Fault injection
# ---------------------------------------------------------------------------
def inject(events):
    """Return a copy of the corpus carrying one violation of each type."""
    e = events.copy()
    notes = {}

    # V1: duplicate an existing retirement row
    r = e[(e["event"] == "retirement") & e["serial"].notna()].iloc[0]
    e = pd.concat([e, pd.DataFrame([r])], ignore_index=True)
    notes["V1"] = f"duplicated retirement of serial {r['serial'][:34]}"

    # V2: a cancellation of that serial, dated after its retirement
    row = r.copy()
    row["event"] = "cancellation"
    row["date"] = r["date"] + pd.Timedelta(days=60)
    e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)
    notes["V2"] = f"cancellation 60 days after retirement of {r['serial'][:34]}"

    # V3: a retirement far exceeding the quantity issued
    iss = e[e["event"] == "issuance"].iloc[0]
    row = r.copy()
    row["project"], row["vintage"] = iss["project"], iss["vintage"]
    row["quantity"] = float(iss["quantity"]) * 3 + 1000
    row["serial"] = "INJECTED-V3"
    row["date"] = iss["date"] + pd.Timedelta(days=1)
    e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)
    notes["V3"] = f"retirement of {row['quantity']:.0f} against {iss['quantity']:.0f} issued"

    # V4: a retirement dated before the issuance it follows
    row = r.copy()
    row["project"], row["vintage"] = iss["project"], iss["vintage"]
    row["serial"] = "INJECTED-V4"
    row["quantity"] = 1.0
    row["date"] = iss["date"] - pd.Timedelta(days=400)
    e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)
    notes["V4"] = "retirement dated 400 days before issuance"

    return e, notes


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="directory holding the ACR files")
    ap.add_argument("--anchors", default=None, help="anchor digest file (JSON)")
    ap.add_argument("--write-anchors", default=None, help="write digests here")
    ap.add_argument("--inject", action="store_true", help="run fault injection")
    a = ap.parse_args()

    events = load_corpus(a.data)
    print(f"Corpus loaded: {len(events)} events "
          f"({(events['event'] == 'issuance').sum()} issuances, "
          f"{(events['event'] == 'retirement').sum()} retirements, "
          f"{(events['event'] == 'cancellation').sum()} cancellations)\n")

    rate, current, msg = verify_hashes(events, a.anchors)
    print("A. HASH VERIFICATION")
    print(f"   {msg}")
    if rate is not None:
        print(f"   pass rate: {rate:.2f}%")
    if a.write_anchors:
        json.dump({str(k): v for k, v in current.items()},
                  open(a.write_anchors, "w"), indent=0)
        print(f"   digests written to {a.write_anchors}")

    print("\nB. LIFECYCLE INTEGRITY, UNMODIFIED CORPUS")
    base = run_checks(events)
    for name, hits in base.items():
        print(f"   {name:32s} {len(hits):6d} flagged")

    if a.inject:
        print("\nC. FAULT INJECTION")
        faulty, notes = inject(events)
        after = run_checks(faulty)
        print(f"   {'check':32s} {'before':>8s} {'after':>8s}   detected")
        for k, name in (("V1", "V1 double retirement"),
                        ("V2", "V2 post-retirement transfer"),
                        ("V3", "V3 quantity breach"),
                        ("V4", "V4 disordered timestamps")):
            b, f = len(base[name]), len(after[name])
            print(f"   {name:32s} {b:8d} {f:8d}   {'YES' if f > b else 'NO'}")
        print("\n   injected:")
        for k, v in notes.items():
            print(f"      {k}: {v}")


if __name__ == "__main__":
    sys.exit(main())
