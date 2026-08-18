# Module 12 Follow-up Quiz - Answer Key

Use this after completing `module12_follow-up-quiz.md` closed book. Equivalent answers earn credit when they preserve the same privacy, security, legal, and governance distinctions.

## 1. Privacy versus security (8 points)

- **Security** protects data and systems against unauthorised access, alteration, misuse, disclosure, loss, or unavailability.
- **Privacy** governs whether personal data may be collected, used, shared, retained, and linked for a defined purpose, including applicable individual rights and expectations.

A company could encrypt a detailed location history, restrict it to authorised staff, and still violate privacy by collecting or using it beyond the stated purpose. Security is necessary for privacy but does not make an unjustified use legitimate.

## 2. Lifecycle control map (12 points)

| Stage | Example risk | Example control |
|---|---|---|
| Collection | Excess or unjustified personal data | Defined purpose, valid authority/consent, minimisation |
| Ingestion | Interception, tampering, or wrong endpoint | TLS, endpoint authentication, integrity validation |
| Storage | Theft, excessive privilege, or unavailable service | Encryption, least privilege, protected tested backups |
| Processing/analysis | Curiosity access, accidental changes, bias, or exposed notebook | Sandboxing, role/process access, logging, bias/privacy review |
| Reporting/sharing | Small groups or detailed outputs reveal people | Aggregation, suppression, de-identification, disclosure review |
| Retention/deletion | Data remains after its valid purpose ends | Retention schedule, defensible archive, secure deletion/de-identification |

Controls must follow the data. Protecting only the central store leaves collection, transit, processing, output, backup, and disposal exposed.

## 3. Data states (10 points)

| Item | State | Relevant control |
|---|---|---|
| Encrypted SQL backup | At rest | Storage encryption, restricted key access, restore testing |
| SIS-to-portal API request | In motion | TLS, authenticated endpoints, integrity validation |
| Student rows in Jupyter | In use | Least privilege, isolated compute, logging, no public notebook |
| Dashboard result in memory | In use | Output control, row-level access, session protection, logging |

Encryption at rest does not protect data while it travels, after an authorised process decrypts it, from over-broad privileges, or from unsafe outputs. Keys and access configuration must also be protected separately.

## 4. Prevent, detect, respond (10 points)

- **Prevent:** least privilege plus an export limit or step-up approval for restricted bulk extraction.
- **Detect:** audit logs for record/export access and anomaly monitoring for unusual time, volume, device, or IP address.
- **Respond:** disable or isolate the account/session, preserve evidence, contain any downstream disclosure, follow the notification workflow, rotate credentials if needed, and recover/verify affected services.

Evidence includes user/service identity, timestamps, source device/IP, authentication events, query/export parameters, record count, destination, authorisation state, configuration/policy version, alerts, and response actions. A sensitive action that cannot be traced cannot be governed effectively.

## 5. Re-identification (12 points)

The fields are **quasi-identifiers**. Their combination may be unique, especially for a rare condition or small school/postcode, and external public information can narrow the record to one person even though direct identifiers were removed.

Three defensible changes are:

1. generalise exact age to a wider age band and postcode/school to a larger region;
2. suppress or combine rare-condition and small-cell results below a disclosure threshold;
3. publish only necessary aggregates or proportions after testing combinations against external-data linkage risk.

De-identification reduces risk but cannot guarantee anonymity.

## 6. Classify, control, retain (12 points)

| Data | Classification | Proportionate decision |
|---|---|---|
| Public school calendar | Public | Public read access; version and retain under ordinary publishing/records policy |
| Staff operational memo | Internal | Authenticated staff access; delete/archive when superseded under records policy |
| Parent contact and fee records | Confidential | Limit to authorised administration/finance processes; encrypt and retain only for the applicable operational/legal period |
| Student medical and behavioural notes | Restricted | Need-to-know access for authorised wellbeing/safeguarding roles, strong logging and disclosure controls, legally governed retention and secure disposal |

Entitlement follows purpose and process, not merely a broad job title or server login.

## 7. GDPR and Australian APPs (10 points)

1. GDPR applies to processing within Article 3 scope, including an EU establishment or relevant offering/monitoring of people in the EU. Australian location alone neither triggers nor avoids it.
2. Consent is one of six Article 6 lawful bases, alongside contract, legal obligation, vital interests, public task, and legitimate interests. The correct basis depends on the processing.
3. APP 11.2 requires reasonable steps to destroy or de-identify personal information no longer needed, subject to record/retention exceptions. Australia has no general Privacy Act right equivalent to GDPR erasure, and GDPR erasure itself has conditions and exceptions rather than being unconditional.

## 8. Ownership and auditability (10 points)

| Responsibility | Accountable role |
|---|---|
| Approve purpose, access, and retention | Data owner/business owner |
| Implement secure pipeline/storage | Data engineer/platform owner |
| Request and use only necessary data | Data scientist/analyst |
| Monitor and respond to incidents | Security team |
| Interpret obligations and independently review use | Legal/compliance/privacy team |
| Use and share outputs appropriately | Business/report owner |

Evidence may include approved purpose/access requests, a data inventory and owner register, access-review records, immutable logs, audit findings, retention/deletion decisions, incident exercises, privacy reviews, and output approvals.

## 9. Cambridge Analytica (8 points)

The failure involved platform-permitted but over-broad collection, weak third-party oversight, permissive defaults, inadequate purpose limitation, and failure to verify downstream retention/use. A conventional intrusion is not required for a privacy breach.

Root-cause controls include purpose-scoped API permissions, privacy-protective defaults, third-party due diligence and monitoring, clear user disclosure, retention/deletion verification, and periodic access audits.

## 10. Assessment 3 live clarification (8 points)

- Weekly or cumulative values can both be defensible if countries are compared consistently and the interpretation matches the representation; cumulative values were suggested for regression but not mandated.
- Do not substitute geographic adjacency for graph analytics. Define relationships using weekly infection patterns; geography may select or contextualise countries.
- Present to a mixed technical/stakeholder audience: explain method concisely and foreground results, insights, decisions, limitations, and restrained recommendations within 10 slides / 10 minutes.
- Submit the notebook/code with all cells already executed and outputs, tables, and plots visible so the marker does not need to rerun it.
