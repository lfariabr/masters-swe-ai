# BDA · Module 12 - One-Pager

> **Privacy vs security · classify then control · data states · GDPR + Australian APPs · governance failures**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **Big Data security protects data from unauthorised access; privacy decides what may be collected, why it may be used, who may access it, and when it must go. Classify the data first, then apply controls by sensitivity, state, purpose, and legal risk across the whole lifecycle.**

## 🖤 Zone 1 - Privacy ≠ security

| Concept | Core question | Typical mechanisms |
|---|---|---|
| **Security** | How do we prevent unauthorised access, modification, loss, or disclosure? | Encryption · ACL/RBAC · TLS · monitoring · backup · key management |
| **Privacy** | Are we allowed to collect/use/share/retain this personal data for this purpose? | Lawful basis/consent · minimisation · purpose limitation · transparency · retention · individual rights |

- **Security is necessary but not sufficient for privacy:** perfectly encrypted data can still be collected or used unlawfully.
- Big Data spreads risk across the lifecycle: source → ingest → store → process/model → share → archive/delete. Distributed stores do not escape legal or governance duties.
- The Vs amplify the problem: **volume** increases breach impact; **velocity** compresses response time; **variety** makes classification/control inconsistent; **valence/linkage** raises re-identification risk.

## 🔴 Zone 2 - Ohlhorst's four-way balancing act

| Caveat | What you want | What pushes back |
|---|---|---|
| **Access** | Only authorised processes/users reach data | Analytics needs controlled access; zero access destroys utility |
| **Availability** | Data is reachable when needed | Distribution/replication widens the attack surface |
| **Performance** | Fast ingest, queries, models | Encryption, inspection, and auditing add overhead |
| **Liability** | Minimise legal, privacy, and IP exposure | Retaining/linking more sensitive data retains more risk |

> **No perfect setting exists:** tightening one dimension can weaken another. State the trade-off and justify the chosen control. (Ohlhorst 2013, Ch. 7)

## 🖤 Zone 3 - Classify → control → retain/delete

1. **Inventory + classify** by sensitivity/purpose: public · internal · confidential · restricted; or domain groups such as financial/HR/customer/comms.
2. **Assign an owner + permitted process:** entitlement follows the business process and purpose, not merely someone's job title or server login.
3. **Apply proportionate controls:** more sensitive data gets tighter access, encryption, monitoring, segmentation, and audit.
4. **Set retention:** destroy/de-identify when no longer needed and legally permitted; archive offline only when a valid purpose remains.

- 🔵 **Keep/delete catch-22:** access logs create privacy/security exposure but may be essential for audit, capacity, and anomaly analysis. Solve with purpose, retention, restricted archive, and retrieval rules - not “keep everything forever.”
- 🔵 **Big Data backup problem:** unique streams may be impossible to recreate; billions of tiny files plus a few huge stores strain conventional backup and deduplication.
- 🔵 **Keys separate from ciphertext:** encryption with the key beside the data is a weak control. Harden configuration/access files too.
- 🔵 **IP is data too:** inventory, label, prioritise, train staff, use DLP/monitoring, and investigate patterns across incidents.

## 🔵 Zone 4 - Match controls to the data state

| State | Meaning | Main attack surface | Control examples |
|---|---|---|---|
| **At rest** | Stored on disk, cloud, USB, backup | Physical/logical storage access | File/disk/database encryption · ACL/RBAC · secure backup |
| **In motion** | Moving between systems/networks | Interception/eavesdropping | TLS · authenticated endpoints · secure APIs/VPNs |

- Chapple's clip covers these **two** states; it is a useful model, not an exhaustive security architecture.
- **Three-part control stack:** policy says what is allowed → encryption protects confidentiality → access control determines who/process can view, change, or delete.
- Big Data/NoSQL changes where and how controls are enforced; performance architecture is not permission to weaken them. (Chapple 2018)

## 🔴 Zone 5 - GDPR: the legal spine (within scope)

- **Scope, Art. 3:** EU establishment, or offering goods/services to or monitoring the behaviour of people **in the EU**. An Australian location alone neither triggers nor avoids GDPR.
- **Lawfulness, Art. 6:** at least one basis - **consent · contract · legal obligation · vital interests · public task · legitimate interests**. Consent is one basis, not the universal answer.
- **Rights, Ch. III:** access · rectification · erasure · restriction · portability · objection - each has conditions/exceptions; none is a magic unconditional delete button.
- **By design/default, Art. 25:** minimise and protect data in the architecture, not after deployment.
- **Security, Art. 32:** risk-based technical/organisational measures; encryption is an explicit example. Access control is a practical way to support confidentiality, not wording literally listed as a standalone measure.
- **Breach, Arts 33-34:** authority notified without undue delay and, where feasible, ≤72h unless unlikely to risk rights/freedoms; affected people notified without undue delay when **high risk** is likely.
- **DPIA/records, Arts 35/30:** high-risk processing may require a DPIA; controllers/processors may need processing records (exceptions can apply).
- **Highest fine tier, Art. 83:** up to **€20m or 4% of worldwide annual turnover, whichever is higher**.

### 🔵 Australian comparison - do not claim GDPR applies by default

- **APP 11.1:** reasonable steps against misuse, interference, loss, unauthorised access/modification/disclosure.
- **APP 11.2:** reasonable steps to destroy or de-identify data no longer needed, unless a Commonwealth-record or legal/court-retention exception applies.
- **APPs 12-13:** access and correction rights. Australia has no general Privacy Act equivalents to GDPR erasure, portability, or objection rights. (OAIC)

## 🔴 Zone 6 - Facebook/Cambridge Analytica: governance, not just “a hack”

- Kogan's app used access that Facebook's platform permitted at the time; the core failure was **over-broad collection, weak third-party oversight, permissive defaults, and poor purpose control**.
- Better response: audit first → disclose clearly → restrict API scopes by purpose → verify deletion/retention → monitor third parties → design privacy defaults before the incident.
- **Lesson:** “No system was infiltrated” does not mean “no privacy failure occurred.” Security language cannot excuse governance failure.

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Model Evaluation** · source code + presentation (7-10 min) · **40%** · due **19/08/2026** · SLOs **c), d), e)**.
> Module 12 is conceptual/ethical closing content, **not a required A3 pipeline step**. Use it only as a concise responsible-use limitation: lawful purpose, minimisation, access, retention, re-identification, or model/data governance.

## 🔴 If you only memorise 5 things

1. **Privacy ≠ security:** security controls access; privacy governs lawful collection, purpose, sharing, retention, and rights.
2. **Classify first, then control** - one security level for every dataset is wasteful and unsafe.
3. Ohlhorst's four tensions: **access · availability · performance · liability**; every design is a justified trade-off.
4. Match encryption/control to state: **at rest** vs **in motion**; protect keys/configuration separately.
5. GDPR is conditional: check **scope → lawful basis → rights/obligations → risk-based controls**. Australian APPs are related but not equivalent.

---

### Margin prompts (answer in blue while you write - anchor to your day job)

1. In Synergetic/SEQTA/Schoolbox, which fields are restricted (medical/behavioural), confidential (fees/contact), or internal (general comms) - and which process genuinely needs each tier?
2. When SIS data flows to portals and reports, where is it at rest vs in motion, where do keys live, and how would you prove access was purpose-limited?

### This-week to-dos (still incomplete in your notes)

- [ ] Resource 3: watch Torrens University's embedded *Big Data and Analytics Interview* (manual watch; no transcript saved).
- [ ] Activity 1: Facebook Data Privacy Scandal - explain the governance failure and propose audit/disclosure + purpose-based API controls.
- [ ] Activity 2: closing discussion - most important topic, most interesting topic, weakest area, and how to improve it.

### Source anchors

- Ohlhorst (2013), *Big Data Analytics*, Ch. 7; Chapple (2018), *Data Security* transcript.
- GDPR: Articles 3, 6, 25, 30, 32, 33-35, 83; official text at https://eur-lex.europa.eu/eli/reg/2016/679/oj
- OAIC, Australian Privacy Principles 11-13: https://www.oaic.gov.au/privacy/australian-privacy-principles/read-the-australian-privacy-principles
