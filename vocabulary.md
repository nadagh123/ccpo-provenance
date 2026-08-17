# CCPO vocabulary

Generated from `ontology/ccpo.ttl`. This file is derived from the ontology, not written by hand, so it cannot drift out of step with it.

**Classes** 26 · **Object properties** 25 · **Data properties** 29 · **Individuals** 46

## Classes

| Class | Label | Subclass of | Comment |
|---|---|---|---|
| `cc:AssuranceLevel` | Assurance level | — | Strength of assurance associated with a provenance event or evidence item. |
| `cc:CarbonCredit` | cc:carbon credit | Entity |  |
| `cc:Country` | cc:Country | Entity |  |
| `cc:CreditOwner` | Credit owner | Agent | Agent that legally owns carbon credits and can initiate transfers or retirements. |
| `cc:EventRole` | Lifecycle role | — | Classification of provenance activities as creation, transformation, or termination events. |
| `cc:EvidenceType` | Evidence type | — | Kind of document or artefact that supports a provenance event, such as a monitoring report or verification statement. |
| `cc:IssuanceActivity` | cc:issuance activity | Activity |  |
| `cc:MRVEvidence` | MRV evidence | Entity | Monitoring, reporting and verification artefacts supporting an issuance. |
| `cc:Market` | Market type | — | Regulatory or voluntary context in which credits are issued or traded. |
| `cc:Mechanism` | Mitigation mechanism | — | Classification of whether a credit is avoidance-based or removal-based. |
| `cc:Methodology` | cc:Methodology / protocol | Entity |  |
| `cc:Project` | cc:Project | Entity |  |
| `cc:ProjectCategory` | Project category | — | High-level category grouping projects by mitigation approach (e.g. ARR, land management). |
| `cc:ProjectDeveloper` | cc:Project developer | Agent |  |
| `cc:ProjectOperator` | cc:Project operator | Agent |  |
| `cc:ProjectOwner` | cc:Project owner | Agent |  |
| `cc:ProjectStatus` | cc:Project status | Entity |  |
| `cc:ProjectType` | cc:Project type / sector | Entity |  |
| `cc:Region` | cc:Region | Entity |  |
| `cc:Registry` | cc:Registry | Agent |  |
| `cc:RegistryOperator` | cc:registry operator | Registry, Agent |  |
| `cc:RetirementActivity` | Retirement activity | Activity | Activity that retires or cancels a batch of carbon credits. |
| `cc:State` | cc:State / Province | Entity |  |
| `cc:TransferActivity` | cc:transfer activity | Activity |  |
| `cc:Validator` | cc:validator | Agent |  |
| `cc:Verifier` | cc:Verifier | Agent |  |

## Object properties

| Property | Domain | Range | Label |
|---|---|---|---|
| `cc:generatedCredit` | IssuanceActivity | CarbonCredit | cc:generated credit |
| `cc:hasAssuranceLevel` | Activity | AssuranceLevel | has assurance level |
| `cc:hasCountry` | Project | Country | cc:has country |
| `cc:hasCredit` | Project | CarbonCredit | cc:has credit |
| `cc:hasCreditOwner` | CarbonCredit | CreditOwner | has credit owner |
| `cc:hasDeveloper` | Project | ProjectDeveloper | cc:has developer |
| `cc:hasEventRole` | Activity | EventRole | has lifecycle role |
| `cc:hasEvidence` | Activity, IssuanceActivity | EvidenceType, MRVEvidence | has evidence |
| `cc:hasMarket` | CarbonCredit | Market | has market type |
| `cc:hasMechanism` | CarbonCredit | Mechanism | has mechanism |
| `cc:hasOperator` | Project | ProjectOperator | cc:has operator |
| `cc:hasOwner` | Project | ProjectOwner | cc:has owner |
| `cc:hasProject` | CarbonCredit | Project | cc:has project |
| `cc:hasProjectCategory` | Project | ProjectCategory, ProjectType | cc:has project category |
| `cc:hasProjectStatus` | Project | ProjectStatus | cc:has project status |
| `cc:hasRegion` | Project | Region | cc:has region |
| `cc:hasRegistry` | Project | Registry | cc:has registry |
| `cc:hasState` | Project | State | cc:has state / province |
| `cc:hasVerifier` | Project | Verifier | cc:has verifier |
| `cc:involvesCredit` | TransferActivity | CarbonCredit | cc:involves credit |
| `cc:isCreditOf` | CarbonCredit | Project | cc:is credit of |
| `cc:isProjectOf` | Project | CarbonCredit | cc:is project of |
| `cc:usesMethodology` | Project | Methodology | cc:uses methodology |
| `cc:wasIssuedBy` | IssuanceActivity | RegistryOperator | cc:was issued by |
| `cc:wasVerifiedBy` | IssuanceActivity | Validator | cc:was verified by |

## Data properties

| Property | Range | Label |
|---|---|---|
| `cc:bufferCreditsReleasedToProject` | integer | cc:buffer credits released to project |
| `cc:creditId` | string | credit ID |
| `cc:dateAddedToDatabase` | dateTime | cc:date project added to database |
| `cc:estimatedAnnualEmissionReductions` | integer | cc:estimated annual emission reductions |
| `cc:eventTimestamp` | dateTime | event timestamp |
| `cc:firstVintageYear` | integer | cc:first year of project (vintage) |
| `cc:hasActivityType` | string | cc:activity type |
| `cc:hasBerkeleyNotes` | string | cc:notes from Berkeley Carbon Trading Project |
| `cc:hasCreditID` | string | cc:credit ID |
| `cc:hasMethodologyCode` | string | cc:methodology / protocol code |
| `cc:hasMethodologyVersion` | string | cc:methodology version |
| `cc:hasProjectDescription` | string | cc:project description |
| `cc:hasProjectID` | string | cc:project ID |
| `cc:hasProjectName` | string | cc:project name |
| `cc:hasProjectSiteLocation` | string | cc:project site location |
| `cc:hasProjectWebsite` | anyURI | cc:project website |
| `cc:hasReductionOrRemoval` | string | cc:reduction or removal |
| `cc:hasRegistryNotes` | string | cc:notes from registry |
| `cc:hasRegistryProjectType` | string | cc:project type from registry |
| `cc:hasScope` | string | cc:scope (e.g. Agriculture) |
| `cc:hasVoluntaryRegistryName` | string | cc:voluntary registry name (text) |
| `cc:hasVoluntaryStatus` | string | cc:voluntary status |
| `cc:reversalsCoveredByBuffer` | integer | cc:reversals covered by buffer |
| `cc:reversalsNotCoveredByBuffer` | integer | cc:reversals NOT covered by buffer |
| `cc:totalBufferPoolDeposits` | integer | cc:total buffer pool deposits |
| `cc:totalCreditsIssued` | integer | cc:total credits issued |
| `cc:totalCreditsRemaining` | integer | cc:total credits remaining |
| `cc:totalCreditsRetired` | integer | cc:total credits retired |
| `cc:vintageYear` | integer | cc:vintage year |

## Restriction axioms

- `cc:IssuanceActivity` &sqsubseteq; `hasEvidence` **some** `MRVEvidence`
- `cc:CarbonCredit` &sqsubseteq; `wasGeneratedBy` **some** `IssuanceActivity`
- `cc:CarbonCredit` &sqsubseteq; `isCreditOf` **exactly** `1 Project`

## Individuals

| Individual | Type | Label |
|---|---|---|
| `AfforestationReforestation` | ProjectCategory | Afforestation and reforestation (ARR) |
| `Avoidance` | Mechanism | Avoidance |
| `ComplianceMarket` | Market | Compliance |
| `ContractDocument` | EvidenceType | Contract document |
| `CreationEvent` | EventRole | Creation event |
| `EnergyIndustrial` | ProjectCategory | Energy and industrial |
| `HighAssurance` | AssuranceLevel | High assurance |
| `HouseholdCommunity` | ProjectCategory | Household and community |
| `LandManagement` | ProjectCategory | Land management |
| `LaurelbrookFarm` | ProjectDeveloper | Laurelbrook Farm |
| `LowAssurance` | AssuranceLevel | Low assurance |
| `MediumAssurance` | AssuranceLevel | Medium assurance |
| `MonitoringReport` | EvidenceType | Monitoring report |
| `NorthAmerica` | Region | North America |
| `OnChainAnchor` | EvidenceType | On-chain anchor |
| `RegistryLog` | EvidenceType | Registry log |
| `Removal` | Mechanism | Removal |
| `TerminationEvent` | EventRole | Termination event |
| `TransformationEvent` | EventRole | Transformation event |
| `UnitedStates` | Country | United States |
| `VCS` | Registry | Verra VCS registry |
| `VCS1089_LaurelbrookProject` | Project |  |
| `ValidationStatement` | EvidenceType | Validation statement |
| `VerificationStatement` | EvidenceType | Verification statement |
| `VoluntaryMarket` | Market | Voluntary |
| `WasteHandlingAndDisposal` | ProjectType | Waste handling and disposal |
| `India` | Country | India |
| `InvalidTransfer_VCS1225_Airline` | TransferActivity | Invalid transfer of VCS1225 credits to an airline, after retirement |
| `Kenya` | Country | Kenya |
| `LateToVerify` | ProjectStatus | Late to verify |
| `RejectedByAdministrator` | ProjectStatus | Rejected by Administrator |
| `Retirement_VCS1225_Energy` | RetirementActivity | Retirement of VCS1225 credits against an energy-sector claim |
| `SouthernAsia` | Region | Southern Asia |
| `SubSaharanAfrica` | Region | Sub-Saharan Africa |
| `credit_VCS1176_all` | CarbonCredit | Carbon credits for project VCS1176 (none issued) |
| `credit_VCS1225_all` | CarbonCredit | Carbon credits for project VCS1225 (all vintages) |
| `dev_EmergentVenturesIndia` | ProjectDeveloper | Emergent Ventures India Private Limited |
| `dev_ViAgroforestry` | ProjectDeveloper | Vi Agroforestry Programme |
| `evidence_VCS1225_monitoring` | MRVEvidence | Monitoring report for VCS1225 |
| `evidence_VCS1225_verification` | MRVEvidence | Verification statement for VCS1225 |
| `issuance_VCS1176_attempt` | IssuanceActivity | Attempted issuance for VCS1176 (rejected) |
| `issuance_VCS1225_initial` | IssuanceActivity | Initial issuance for VCS1225 |
| `proj_VCS1176` | Project | System of Root Intensification (SRI) programme: Reduction of Methane emissions and water consumption in rice fields of India |
| `proj_VCS1225` | Project | Kenya Agricultural Carbon Project |
| `reg_VCS` | Registry | Verra VCS registry (issuing instance) |
| `val_None` | Validator | No validator (project rejected) |
