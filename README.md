# Carbon Credit Provenance Ontology (CCPO)

**Author:** Dr. Nada Alghanmi  
**Supervisor:** Dr. Farookh Hussain  
**Institution:** School of Computer Science and Engineering, University of Technology Sydney (UTS)  
**Year:** 2026  
**Namespace:** `http://example.org/cc#`  
**License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

The **Carbon Credit Provenance Ontology (CCPO)** is a formal, machine-interpretable semantic model for end-to-end carbon credit provenance. It extends the [W3C PROV-O standard](https://www.w3.org/TR/prov-o/) with domain-specific classes, properties, and relationships for the full carbon credit lifecycle: **issuance → verification → transfer → retirement**.

The CCPO was developed as part of a doctoral thesis addressing five persistent challenges in carbon credit markets:

- No shared semantic vocabulary across heterogeneous registries (Verra, Gold Standard, UNFCCC CDM, CER)
- No machine-traversable backward and forward provenance tracing
- No automated integrity checking for double counting and transfer-after-retirement
- No formal linkage between MRV evidence and issued credits
- Fragmented lifecycle records preventing auditor verification

The CCPO resolves these gaps by providing a single, machine-interpretable model in which every lifecycle entity, event, and actor is formally typed and linked.

---

## Repository Structure

```
ccpo-provenance/
├── ontology/
│   └── ccpo.ttl                       ← Main OWL 2 ontology (Turtle format)
├── individuals/
│   └── ccpo_individuals_vcs1225.ttl   ← Instantiated individuals (traceability scenario)
├── taxonomy/
│   └── ccpt_taxonomy.ttl              ← Carbon Credit Provenance Taxonomy (CCPT)
├── sparql/
│   ├── competency_questions.sparql    ← SPARQL queries for ontology validation
│   └── run_queries.py                 ← Python script to run all queries automatically
├── docs/
│   ├── images/                        ← SPARQL query result screenshots
│   ├── class_diagram.md               ← CCPO class hierarchy
│   └── how_to_run_sparql.md           ← Step-by-step SPARQL guide
└── README.md
```

---

## CCPO Core Classes

The ontology contains **31 classes** confirmed by SPARQL query in Protégé Desktop:

| Class | PROV-O Alignment | Description |
|---|---|---|
| `cc:CarbonCredit` | `prov:Entity` | Primary traceable entity — a tradeable certificate of verified emissions reduction |
| `cc:Project` | `prov:Entity` | The offset project generating the credits |
| `cc:EvidenceType` | `prov:Entity` | MRV artefacts including verification statements and monitoring reports |
| `cc:IssuanceActivity` | `prov:Activity` | Registry event creating a credit after verification |
| `cc:RetirementActivity` | `prov:Activity` | Terminal event extinguishing a credit against an emissions claim |
| `cc:CreditOwner` | `prov:Agent` | Entity purchasing or retiring credits |
| `cc:Registry` | `prov:Agent` | Issuing authority such as Verra VCS, Gold Standard, UNFCCC CDM |
| `cc:Verifier` | `prov:Agent` | Accredited independent third-party auditor |
| `cc:ProjectDeveloper` | `prov:Agent` | Entity implementing the offset project |
| `cc:Methodology` | `prov:Entity` | Calculation methodology such as REDD+, CDM, Soil Carbon |
| `cc:Market` | `prov:Entity` | Market type — Compliance or Voluntary |
| `cc:AssuranceLevel` | `prov:Entity` | Verification assurance level — High, Medium, or Low |

---

## Key Object Properties

The ontology contains **29 object properties** confirmed by SPARQL query:

| Property | Description |
|---|---|
| `cc:isCreditOf` | Links a CarbonCredit to its originating Project |
| `cc:generatedCredit` | Links an IssuanceActivity to the CarbonCredit it generated |
| `cc:wasIssuedBy` | Links a CarbonCredit to its issuing Registry |
| `cc:hasVerifier` | Links a credit or project to its Verifier |
| `cc:hasEvidence` | Links an issuance to its MRV evidence artefacts |
| `cc:hasRegistry` | Links a Project to its Registry |
| `cc:hasDeveloper` | Links a Project to its Developer |
| `cc:usesMethodology` | Links a Project to its calculation Methodology |
| `cc:hasMarket` | Links a credit to its Market type |
| `cc:hasAssuranceLevel` | Links a credit to its AssuranceLevel |
| `prov:generated` | PROV-O — activity generated an entity |
| `prov:used` | PROV-O — activity used an entity |
| `prov:wasAssociatedWith` | PROV-O — activity was associated with an agent |

---

## Individuals Instantiated in the Ontology

The ontology includes **36 named individuals** confirmed by SPARQL query, covering two real traceability scenarios.

### Valid scenario — Kenya Agricultural Carbon Project (VCS1225)

| Individual | Class | Label |
|---|---|---|
| `proj_VCS1225` | `cc:Project` | Kenya Agricultural Carbon Project |
| `credit_VCS1225_all` | `cc:CarbonCredit` | Carbon credits for project VCS1225 (all vintages) |
| `issuance_VCS1225_initial` | `cc:IssuanceActivity` | Initial issuance for VCS1225 |
| `reg_VCS` | `cc:Registry` | Verra VCS registry |
| `dev_EmergentVenturesIndia` | `cc:ProjectDeveloper` | Emergent Ventures India Private Limited |

### Integrity violation scenario — VCS1176 (rejected issuance)

| Individual | Class | Label |
|---|---|---|
| `proj_VCS1176` | `cc:Project` | System of Root Intensification (SRI) programme |
| `credit_VCS1176_all` | `cc:CarbonCredit` | Carbon credits for project VCS1176 (none issued) |
| `issuance_VCS1176_attempt` | `cc:IssuanceActivity` | Attempted issuance for VCS1176 (rejected) |
| `val_None` | individual | No validator — project rejected |

---

## SPARQL Query Results — Validated Evidence

All queries were executed in **Protégé Desktop** using the **Snap SPARQL** plugin. Screenshots are saved in `docs/images/`.

### Query 1 — All carbon credit individuals

```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cc:   <http://example.org/cc#>

SELECT ?individual ?label
WHERE {
  ?individual rdf:type cc:CarbonCredit .
  ?individual rdfs:label ?label .
}
```

**Result:** 2 carbon credit individuals — VCS1225 and VCS1176  
![Credits list](docs/images/CQ_credits_list.png)

---

### Query 2 — Forward trace (Chapter 5, Section 5.6.3)

Starting from a project, retrieve all credits it generated and their issuance events.

```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cc:   <http://example.org/cc#>

SELECT ?projectLabel ?creditLabel ?issuanceLabel
WHERE {
  ?project  rdf:type cc:Project .
  ?project  rdfs:label ?projectLabel .
  ?credit   cc:isCreditOf ?project .
  ?credit   rdfs:label ?creditLabel .
  ?issuance cc:generatedCredit ?credit .
  ?issuance rdfs:label ?issuanceLabel .
}
ORDER BY ?projectLabel
```

**Result:** Kenya Agricultural Carbon Project → Carbon credits for project VCS1225 (all vintages) → Initial issuance for VCS1225  
![Forward trace](docs/images/CQ_forward_trace.png)

---

### Query 3 — Integrity Check A: Rejected issuance detection (Chapter 5, Section 5.6.4)

This query proves the ontology automatically distinguishes valid from invalid issuances. The rejected VCS1176 issuance has no generated credit — the ontology detects this as a provenance violation.

```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cc:   <http://example.org/cc#>

SELECT ?issuanceLabel ?creditLabel
WHERE {
  ?issuance rdf:type cc:IssuanceActivity .
  ?issuance rdfs:label ?issuanceLabel .
  OPTIONAL {
    ?issuance cc:generatedCredit ?credit .
    ?credit rdfs:label ?creditLabel
  }
}
ORDER BY ?issuanceLabel
```

**Result:**
- `Attempted issuance for VCS1176 (rejected)` → credit column **empty** — violation detected
- `Initial issuance for VCS1225` → `Carbon credits for project VCS1225 (all vintages)` — valid

![Integrity Check A](docs/images/CQ_integrity_check_A.png)

---

### Query 4 — All projects (Chapter 5, Section 5.3)

```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cc:   <http://example.org/cc#>

SELECT ?project ?label
WHERE {
  ?project rdf:type cc:Project .
  ?project rdfs:label ?label .
}
ORDER BY ?label
```

**Result:** 2 projects — Kenya Agricultural Carbon Project + System of Root Intensification (SRI) programme  
![Projects list](docs/images/CQ_projects_list.png)

---

### Query 5 — GreenCanopy full audit (Chapter 5, Section 5.6)

This single query returns the complete provenance chain — replacing the 3-week manual audit described in the thesis (Chapter 1, Section 1.7, Failure 4).

```sparql
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cc:   <http://example.org/cc#>

SELECT ?projectLabel ?creditLabel ?issuanceLabel ?developerLabel
WHERE {
  ?project  rdf:type cc:Project .
  ?project  rdfs:label ?projectLabel .
  ?credit   cc:isCreditOf ?project .
  ?credit   rdfs:label ?creditLabel .
  ?issuance cc:generatedCredit ?credit .
  ?issuance rdfs:label ?issuanceLabel .
  OPTIONAL {
    ?project cc:hasDeveloper ?developer .
    ?developer rdfs:label ?developerLabel
  }
}
```

**Result:** Kenya Agricultural Carbon Project → Carbon credits for project VCS1225 → Initial issuance for VCS1225  
![GreenCanopy audit](docs/images/CQ_greencanopy_audit.png)

---

## How to Load and Query the Ontology

### Protégé Desktop (recommended)
1. Download free from [protege.stanford.edu](https://protege.stanford.edu)
2. `File → Open` → select `ontology/ccpo.ttl`
3. `Window → Tabs → SPARQL Query` to enable the SPARQL tab
4. Install **Snap SPARQL Query** plugin via `File → Check for plugins`
5. Paste any query from `sparql/competency_questions.sparql` and click **Execute**
6. See `docs/how_to_run_sparql.md` for a complete step-by-step guide

### Python — no tools needed except one command
```bash
pip install rdflib
python sparql/run_queries.py
```

### WebProtégé
1. Log in at [webprotege.stanford.edu](https://webprotege.stanford.edu)
2. Open your CCPO project
3. Use the **DL Query** tab for class-based exploration

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

```bibtex
@phdthesis{alghanmi2026ccpo,
  author     = {Nada Alghanmi},
  title      = {A Provenance-Centric Architecture for Carbon Credit Systems:
                Ontology Design, Storage Decisions, and Intelligent Forensic Tracing},
  school     = {University of Technology Sydney},
  year       = {2026},
  supervisor = {Farookh Hussain}
}
```

---

## Contact

Dr. Nada Alghanmi — University of Technology Sydney  
Sponsor: University of Jeddah / Saudi Cultural Mission (SCAM) in Australia
