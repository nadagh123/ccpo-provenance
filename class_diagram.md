# CCPO Class Diagram

This document describes the class hierarchy and relationships of the Carbon Credit Provenance Ontology (CCPO) as implemented in WebProtégé (CCPO_CCPT project).

## Class Hierarchy

```
owl:Thing
│
├── prov:Entity
│   ├── cc:CarbonCredit             ← primary traceable entity
│   ├── cc:Project                  ← originating offset project
│   ├── cc:MRVEvidence              ← measurement & verification artefacts
│   │   ├── cc:VerificationStatement
│   │   └── cc:MonitoringReport
│   ├── cc:OnChainAnchor            ← cryptographic hash commitment
│   └── cc:Methodology              ← calculation methodology
│
├── prov:Activity
│   ├── cc:IssuanceActivity         ← credit creation event (must have MRVEvidence)
│   ├── cc:ValidationActivity       ← third-party review
│   ├── cc:TransferActivity         ← ownership change
│   ├── cc:RetirementActivity       ← terminal event (blocks further transfer)
│   └── cc:RevocationActivity       ← invalidation
│
└── prov:Agent
    ├── cc:Registry                 ← Verra, Gold Standard, UNFCCC CDM, CER
    ├── cc:Issuer
    ├── cc:Verifier
    ├── cc:ProjectDeveloper
    ├── cc:Buyer
    └── cc:Auditor
```

## Provenance Relationship Map

```
[cc:Project]
    │
    │ cc:hasCredit (forward)
    ▼
[cc:CarbonCredit] ←── prov:wasGeneratedBy ──── [cc:IssuanceActivity]
    │                                                │
    │ cc:wasIssuedBy                                 │ cc:hasEvidence
    ▼                                                ▼
[cc:Registry]                               [cc:MRVEvidence]
                                                     │
                                                     │ cc:hasOnChainAnchor
                                                     ▼
                                            [cc:OnChainAnchor]
                                             (contentHash on Ethereum)
```

## OWL 2 Integrity Constraints

| Constraint | Class | Restriction | Purpose |
|---|---|---|---|
| Valid issuance | `cc:CarbonCredit` | `prov:wasGeneratedBy some cc:IssuanceActivity` | Detects credits without valid issuance (Integrity Check A) |
| Evidence required | `cc:IssuanceActivity` | `cc:hasEvidence some cc:MRVEvidence` | Detects issuances without MRV evidence |
| One project per credit | `cc:CarbonCredit` | `cc:isCreditOf exactly 1 cc:Project` | Ensures unique project linkage |

## Credit Status Lifecycle

```
[Issued] → [Transferred] → [Retired]
         ↘              ↗
           [Revoked] ←──── (at any stage)
```

**Integrity Check B:** If `TransferActivity.timestamp > RetirementActivity.timestamp` on the same credit → OWL 2 reasoner raises inconsistency (transfer-after-retirement violation).
