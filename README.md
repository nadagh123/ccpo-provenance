# Carbon Credit Provenance Ontology (CCPO)

**Author:** Dr. Nada Alghanmi  
**Supervisor:** Dr. Farookh Hussain  
**Institution:** School of Computer Science and Engineering, University of Technology Sydney (UTS)  
**Year:** 2026  
**Namespace:** `https://w3id.org/ccpo#`  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

The **Carbon Credit Provenance Ontology (CCPO)** is a formal, machine-interpretable semantic model for end-to-end carbon credit provenance. It extends the [W3C PROV-O standard](https://www.w3.org/TR/prov-o/) with domain-specific classes, properties, and relationships for the full carbon credit lifecycle: **issuance → verification → transfer → retirement**.

The CCPO was developed as part of a doctoral thesis addressing five persistent challenges in carbon credit markets:
- No shared semantic vocabulary across heterogeneous registries (Verra, Gold Standard, UNFCCC CDM, CER)
- No machine-traversable backward/forward provenance tracing
- No automated integrity checking (double counting, transfer-after-retirement)
- No formal linkage between MRV evidence and issued credits
- Fragmented lifecycle records preventing auditor verification

The CCPO resolves these gaps by providing a single, machine-interpretable model in which every lifecycle entity, event, and actor is formally typed and linked.

---

## Repository Structure

```
ccpo-provenance/
├── ontology/
│   └── ccpo.ttl                      ← Main OWL 2 ontology (Turtle format)
│
├── individuals/
│   └── ccpo_individuals_vcs1225.ttl  ← Instantiated individuals (traceability scenario)
│
├── taxonomy/
│   └── ccpt_taxonomy.ttl             ← Carbon Credit Provenance Taxonomy (CCPT)
│
├── sparql/
│   └── competency_questions.sparql   ← 10 SPARQL queries for ontology validation
│
├── docs/
│   ├── class_diagram.md              ← CCPO class hierarchy description
│   └── provenance_design.md          ← Design methodology notes
│
└── README.md
```

---

## CCPO Core Classes

| Class | PROV-O Alignment | Description |
|---|---|---|
| `cc:CarbonCredit` | `prov:Entity` | Primary traceable entity — a tradeable certificate of verified emissions reduction |
| `cc:Project` | `prov:Entity` | The offset project generating the credits |
| `cc:MRVEvidence` | `prov:Entity` | Measurement, Reporting, Verification artefacts (satellite imagery, sensor logs) |
| `cc:VerificationStatement` | `cc:MRVEvidence` | Third-party verification confirmation |
| `cc:MonitoringReport` | `cc:MRVEvidence` | Periodic project monitoring data |
| `cc:OnChainAnchor` | `prov:Entity` | Cryptographic hash committed on-chain for tamper detection |
| `cc:IssuanceActivity` | `prov:Activity` | Registry event creating a credit after verification |
| `cc:ValidationActivity` | `prov:Activity` | Independent third-party review of emissions claims |
| `cc:TransferActivity` | `prov:Activity` | Ownership change between market participants |
| `cc:RetirementActivity` | `prov:Activity` | Terminal event extinguishing a credit against an emissions claim |
| `cc:RevocationActivity` | `prov:Activity` | Invalidation due to fraud or MRV failure |
| `cc:Registry` | `prov:Agent` | Issuing authority (Verra, Gold Standard, UNFCCC CDM) |
| `cc:Verifier` | `prov:Agent` | Accredited independent third-party auditor |
| `cc:ProjectDeveloper` | `prov:Agent` | Entity implementing the offset project |
| `cc:Buyer` | `prov:Agent` | Entity purchasing or retiring credits |

---

## Key Object Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `cc:isCreditOf` | `cc:CarbonCredit` | `cc:Project` | Links credit to its originating project |
| `cc:wasIssuedBy` | `cc:CarbonCredit` | `cc:Registry` | Links credit to its issuing registry |
| `cc:wasValidatedBy` | `cc:CarbonCredit` | `cc:Verifier` | Links credit to its third-party verifier |
| `cc:wasTransferredTo` | `cc:CarbonCredit` | `prov:Agent` | Records receiving agent in a transfer |
| `cc:wasRetiredBy` | `cc:CarbonCredit` | `cc:Buyer` | Links retired credit to retiring agent |
| `cc:generatedCredit` | `cc:IssuanceActivity` | `cc:CarbonCredit` | Links issuance event to generated credit |
| `cc:hasEvidence` | `cc:IssuanceActivity` | `cc:MRVEvidence` | Links issuance to supporting evidence |
| `cc:hasOnChainAnchor` | `cc:MRVEvidence` | `cc:OnChainAnchor` | Links off-chain evidence to on-chain hash |
| `cc:hasMethodology` | `cc:Project` | `cc:Methodology` | Specifies the calculation methodology |

---

## Traceability Capabilities

### Backward Trace
Starting from any `cc:CarbonCredit`, traverse the full provenance chain back to the originating `cc:Project` and all linked `cc:MRVEvidence`:

```
CarbonCredit → [cc:isCreditOf] → Project
             → [prov:wasGeneratedBy] → IssuanceActivity
             → [cc:wasIssuedBy] → Registry
             → [cc:hasEvidence] → VerificationStatement + MonitoringReport
             → [cc:hasOnChainAnchor] → OnChainAnchor
```

### Forward Trace
Starting from any `cc:Project`, retrieve all credits it generated, their issuance events, and current status:

```
Project → [cc:hasCredit] → CarbonCredit
        → [prov:wasGeneratedBy inverse] → IssuanceActivity
        → [cc:creditStatus] → {issued | transferred | retired | revoked}
```

### Integrity Checks (OWL 2 Reasoner)

**Integrity Check A — Invalid Issuance Detection:**  
Any `cc:CarbonCredit` that lacks a `prov:wasGeneratedBy` link to a valid `cc:IssuanceActivity` is automatically flagged as a provenance violation. This detects fraudulently created credits before they enter the trading system.

**Integrity Check B — Transfer After Retirement:**  
If a `cc:TransferActivity` timestamp is later than a `cc:RetirementActivity` timestamp on the same credit, the OWL 2 reasoner raises an inconsistency — preventing double retirement at the semantic layer.

---

## How to Load the Ontology

### Protégé (Desktop)
1. Open **Protégé 5.x** ([protege.stanford.edu](https://protege.stanford.edu/))
2. `File → Open` → select `ontology/ccpo.ttl`
3. To also load individuals: `File → Load imports` → select `individuals/ccpo_individuals_vcs1225.ttl`
4. Run the **HermiT** or **Pellet** reasoner to trigger integrity checks

### WebProtégé
1. Log in at [webprotege.stanford.edu](https://webprotege.stanford.edu)
2. Create a new project → Upload `ccpo.ttl`
3. Upload `ccpo_individuals_vcs1225.ttl` as a second ontology document

### Apache Jena Fuseki (SPARQL endpoint)
```bash
# Download Apache Jena
# https://jena.apache.org/download/

# Load the ontology and individuals
fuseki-server --file=ontology/ccpo.ttl \
              --file=individuals/ccpo_individuals_vcs1225.ttl \
              /ccpo

# Then run competency questions:
# sparql/competency_questions.sparql
```

### Python (rdflib)
```python
from rdflib import Graph, Namespace

g = Graph()
g.parse("ontology/ccpo.ttl", format="turtle")
g.parse("individuals/ccpo_individuals_vcs1225.ttl", format="turtle")

CC = Namespace("https://w3id.org/ccpo#")

# Query: all carbon credits and their projects
q = """
PREFIX cc: <https://w3id.org/ccpo#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?credit ?project WHERE {
    ?credit a cc:CarbonCredit ;
            cc:isCreditOf ?project .
}
"""
for row in g.query(q):
    print(row)
```

---

## SPARQL Competency Questions

Ten SPARQL queries in `sparql/competency_questions.sparql` validate the ontology:

| Query | Purpose |
|---|---|
| CQ1 | Backward trace — credit to project to MRV evidence |
| CQ2 | Forward trace — project to all credits and statuses |
| CQ3 | Integrity Check A — credits without valid issuance |
| CQ4 | Integrity Check B — transfer after retirement detection |
| CQ5 | Double counting — credits with multiple issuance activities |
| CQ6 | MRV completeness — issuances missing verification statements |
| CQ7 | Full lifecycle summary per project |
| CQ8 | Cross-registry verification listing |
| CQ9 | Credits filtered by methodology type (e.g. REDD+) |
| CQ10 | On-chain anchor verification for all MRV evidence |

---

## Taxonomy (CCPT)

The companion **Carbon Credit Provenance Taxonomy** (`taxonomy/ccpt_taxonomy.ttl`) classifies credits across three dimensions:

1. **Compliance Type** — Compliance (CER, EUA, ACCU) vs Voluntary (VER, CORSIA)
2. **Project Methodology** — REDD+, CDM, Soil Carbon, A/R, Renewable Energy, Methane Capture
3. **Metadata Attribute Weight** — Integrity-critical (on-chain candidates) vs Supporting (off-chain candidates)

---

## Related Publications

1. **Alghanmi, N. A., et al.** (2025). Data-driven approach for selection of on-chain vs off-chain carbon credits data storage methods. *Knowledge-Based Systems, 310*. Elsevier. https://doi.org/10.1016/j.knosys.2024.1

2. **Alghanmi, N. A., et al.** (2024). Social carbon credits: A new approach to assessing the impact of social development projects against the SDGs. *IEEE ICEBE 2024* (pp. 191–199). https://doi.org/10.1109/ICEBE62490.2024.00037

3. **Alghanmi, N. A., et al.** (2023). Carbon credits storage: A comparative multifactor analysis of on-chain vs off-chain approaches. *IEEE ICEBE 2023*. https://doi.org/10.1109/icebe59045.2023.00031

4. **Alghanmi, N. A., et al.** (2026). RAG-Assisted on-chain provenance and conversational visualization for carbon credits. *AINA 2026* (Accepted).

---

## Citation

If you use the CCPO in your work, please cite:

```bibtex
@phdthesis{alghanmi2026ccpo,
  author    = {Nada Alghanmi},
  title     = {A Provenance-Centric Architecture for Carbon Credit Systems:
               Ontology Design, Storage Decisions, and Intelligent Forensic Tracing},
  school    = {University of Technology Sydney},
  year      = {2026},
  supervisor = {Farookh Hussain}
}
```

---

## Contact

Dr. Nada Alghanmi — University of Technology Sydney  
Sponsor: University of Jeddah / Saudi Cultural Mission (SCAM) in Australia
