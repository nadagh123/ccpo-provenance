# Carbon Credit Provenance Ontology (CCPO)

A domain ontology for the provenance of carbon credits, extending the W3C PROV-O
standard with the classes, properties and lifecycle constraints that PROV-O
leaves undefined for carbon markets.

Developed as part of doctoral research at the University of Technology Sydney.

## Contents

| Path | What it is |
|---|---|
| `ontology/ccpo.owl` | The ontology in RDF/XML, as loaded in Protégé. Authoritative. |
| `ontology/ccpo.ttl` | The same ontology in Turtle, for readability and diffs. |
| `docs/vocabulary.md` | Class, property and individual tables, generated from the ontology. |
| `sparql/competency_questions.sparql` | SPARQL queries operationalising the competency questions. |

Both ontology files contain the schema **and** the instantiated individuals used
in the traceability demonstrations. They are two serialisations of one artefact,
not two artefacts.

## Scope

- 26 classes, 25 object properties, 29 data properties, 46 individuals
- Aligned to PROV-O: domain classes specialise `prov:Entity`, `prov:Activity`
  and `prov:Agent`
- Instantiated with two real registered projects drawn from the Berkeley
  Voluntary Registry Offsets Database: VCS1225 (Kenya Agricultural Carbon
  Project) and VCS1176 (a rejected issuance)

## Integrity constraints

Three OWL 2 restriction axioms declare what a well-formed provenance record must
contain:

| Axiom | Meaning |
|---|---|
| `CarbonCredit ⊑ prov:wasGeneratedBy some IssuanceActivity` | Every credit must originate in an issuance |
| `IssuanceActivity ⊑ hasEvidence some MRVEvidence` | Every issuance must be evidenced |
| `CarbonCredit ⊑ isCreditOf exactly 1 Project` | A credit belongs to exactly one project |

**How these are checked.** OWL 2 operates under the open world assumption, so a
reasoner encountering a credit with no issuance link infers that one must exist
rather than reporting a violation. The first two axioms therefore *declare* the
requirement; the corresponding SPARQL queries *enforce* it, evaluating a closed
world over the asserted graph using negation as failure.

The cardinality axiom is the exception and is genuinely reasoner-detectable:
asserting a credit as belonging to two projects known to be distinct contradicts
the restriction directly. This was verified in Protégé — HermiT reports the
ontology inconsistent when such an assertion is added, and consistent when it is
removed.

A fourth constraint, that a transfer must not follow a retirement of the same
credit, is documented but not formally axiomatised: temporal ordering over
timestamps is not expressible in OWL 2 DL without SWRL or SPARQL. It is declared
here and enforced at the verification layer of the wider framework. The
individuals `Retirement_VCS1225_Energy` and `InvalidTransfer_VCS1225_Airline`
carry the timestamps from which the violation follows.

## Reasoner status

Checked with HermiT: the ontology is consistent and no class is unsatisfiable.

## Naming conventions

Identifiers use camel case (`cc:IssuanceActivity`, `cc:isCreditOf`). WebProtégé
renders `rdfs:label`, which is written in spaced lower case for readability, so
the interface may display `cc: issuance activity` where the identifier is
`cc:IssuanceActivity`.

Classes and properties are in the `http://example.org/cc#` namespace;
individuals are in `http://www.semanticweb.org/owl/owlapi/turtle#`.

## Loading the ontology

**Protégé** — File → Open → `ontology/ccpo.owl`, then Reasoner → HermiT → Start
reasoner.

**Python**

```python
from rdflib import Graph
g = Graph()
g.parse("ontology/ccpo.ttl", format="turtle")
```

## Licence

CC BY 4.0. See `LICENSE`.
