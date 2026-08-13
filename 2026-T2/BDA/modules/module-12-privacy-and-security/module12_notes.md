# Module 12 — Big Data Privacy and Security

## TL;DR
- **Privacy ≠ security**: security controls unauthorised access; privacy governs what may be collected, how it's used, and who can access it - privacy incorporates security but adds governance on top.
- Securing Big Data is a **four-way balancing act** (access, availability, performance, liability) with no clean solution - tightening one loosens another (Ohlhorst).
- **Data classification** and the **at-rest/in-motion** split (Chapple) are the two practical levers for routing the right control to the right data.
- **GDPR** sets a risk-based legal floor for lawful processing within its scope: an Article 6 lawful basis, subject rights, breach notification "without undue delay," and tiered Article 83 fines.
- 🔴 Module 12 is conceptual/ethical closing content, not a required A3 component - but its framing is a legitimate cross-reference if A3 discusses responsible data use.

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Ohlhorst (2013) — Ch.7 Security, Compliance, Auditing and Protection | **✅** |
| **2** | Watch & summarise Chapple (2018) — Data Security (Section 4 clips) | **✅** |
| 3 | Watch & summarise Torrens University (2020) — Big Data and Analytics Interview | 🔥 WIP — needs manual watch (no transcript URL, embedded Kaltura player) |
| **4** | Read & summarise GDPR (gdpr-info.eu) | **✅** |
| 5 | Activity 1: Analyse the Facebook Data Privacy Scandal | 🕐 |
| 6 | Activity 2: Review All Things Big Data and Analytics (closing discussion) | 🕐 |

---

## Key Highlights

### 1. Ohlhorst, F. (2013). Big data analytics: Turning big data into big money — Ch.7.

**Citation:** Ohlhorst, F. (2013). Big data analytics: Turning big data into big money. Hoboken, NJ: John Wiley. Chapter 7: Security, compliance, auditing and protection (pp. 63-77).

**Purpose:** Pragmatic, non-academic walkthrough of what actually breaks when you try to secure a Big Data store - access, availability, performance and liability trade-offs - and a set of concrete controls (data classification, encryption, key management, IP protection) rather than abstract security theory.

---

#### 1. The four security caveats
Ohlhorst frames Big Data security as a **balancing act**, not a solvable problem - every gain on one caveat costs you on another.

| Caveat | What it means | Practical tension |
|---|---|---|
| **Access** | You can only fully secure data by cutting off access - not viable | Need controlled, not eliminated, access |
| **Availability** | Where data lives and how it's distributed | More control = more protection, but less flexibility |
| **Performance** | Encryption/security layers add processing overhead | Big Data's volume/velocity makes this cost compound fast |
| **Liability** | Sensitivity, legal requirements, privacy, IP tied to the data itself | Keeping data = keeping risk |

#### 2. The keep-or-delete dilemma
- Simplest security move: **destroy data you no longer need** - it's a standing risk for as long as it's kept.
- But Big Data's value is often in what looks disposable: **activity/access logs** are simultaneously (a) a security risk if exposed, and (b) the exact data needed to analyse system scale/efficiency (a legitimate Big Data analytics use case). Ohlhorst calls this a genuine catch-22 with "no easy answer" - archive-and-retrieve (keep it, but disconnect it from live systems) is his suggested middle path.

#### 3. Data classification as the security enabler
- Not all data needs the same protection. A simple classification scheme (financial / HR / sales / inventory / communications) is enough to route the right controls to the right data - internal email ≠ financial reports ≠ customer data.
- Classification responsibility should be **shared across technical, security and business teams**, not owned solely by IT.
- More granular classification → smaller, easier-to-monitor silos → cheaper, more targeted encryption and monitoring.

#### 4. Why Big Data breaks conventional backup
- Big Data is often **unique and non-reproducible** (sensor/traffic/surveillance streams) - lose it once, lose it forever, so backup failure is higher-stakes than in traditional IT.
- Its uniqueness also defeats **deduplication**, a standard backup time-saver, inflating backup capacity/bandwidth needs.
- Workload shape is the worst case for backup appliances: **billions of small files + a handful of massive database files** simultaneously - this dual profile is the real engineering challenge, not raw volume alone.

#### 5. Compliance: healthcare as the worked example
- Regulatory scope follows the personal data being processed and the jurisdiction involved, not the database engine - a Hadoop/Cassandra/MongoDB store is not exempt from compliance law just because it isn't relational. Ohlhorst's own concern was historical: non-relational stores were, at the time of writing, less mature at *enforcing* compliance controls, not that the law didn't reach them. The practical implication is that privacy/security controls have to follow the data across every distributed store it touches.
- **HIPAA-driven** electronic health records are Ohlhorst's case study for how compliance and Big Data collide: massive sensitive data volumes, real-time access, inter-enterprise exchange, and stores (Hadoop, Cassandra, MongoDB) that historically shipped with **little to no built-in data-level security**.
- Four goals distilled from the healthcare industry's response:
  1. **Control access by process, not job function** - OS-level access ≠ entitlement to the data on that server.
  2. **Secure data at rest** - encrypt regardless of whether it's on disk, on-prem, or in the cloud.
  3. **Separate the cryptographic keys from the data they protect** - a key stored next to its data is not a control, it's a formality.
  4. **Harden the whole application/config stack**, not just the data itself - encrypting data means nothing if the access-control config file is unprotected.
- ⚠️ Regulatory ambiguity flagged directly in the text: if one database mixes credit-card and health data, whether **PCI-DSS and HIPAA apply to the whole store or just the relevant fields** is "highly dependent on your interpretation" - not a solved question even for the source's own worked example.

#### 6. Intellectual property (IP) protection
- Big Data consolidates diverse content (photos → patent filings) into one store, making it easy for IP to get swept up and exposed by design, since analytics is explicitly built to surface "nuggets" of information.
- Eight practical rules given: understand & inventory what needs protecting, prioritise by risk/cost-benefit, label confidential data, physically lock down storage, train employees (the "weakest link"), use DLP tooling, take a holistic view (isolated incidents often hide one repeat offender), and think like an attacker ("counterintelligence mind-set").

#### Key Takeaways for BDA601
1. **The classification-then-control pattern maps directly onto Synergetic**: student PII (medical/behavioural notes), financial data (fee accounts), and general comms records already sit in different sensitivity tiers in practice - Ohlhorst's four healthcare-derived goals (process-based access, encryption at rest, separated key management, hardened application stack) are the same controls a school SIS admin reasons about, just without the "Big Data" label.
2. The **access-vs-availability-vs-performance-vs-liability** framing is a good lens for A3's write-up if it touches on data governance/evaluation criteria - it forces you to name the trade-off explicitly instead of just asserting "the data is secure."
3. Complements Module 10's Synergetic "Mandatory Data" flag example (support/confidence analogy) - both are instances of the same idea: not all fields carry equal risk, so treat them differently rather than uniformly.

---

### 2. Chapple, M. (2018). Data Security [Video transcript, Section 4].

**Citation:** Chapple, M. (2018, 18 May). Data security [Video file]. Retrieved from https://www.linkedin.com/learning/sscp-cert-prep-2-security-operations-and-administration/understanding-data-security

**Purpose:** A short, practitioner-level primer distinguishing the two *states* this clip covers - and therefore the two different attack surfaces - security controls have to address. (Not exhaustive: NIST also names "data in use" as a third state; this resource only covers the two below.)

---

#### 1. Data at rest vs. data in motion
| State | Definition | Attack vector | Primary control |
|---|---|---|---|
| **At rest** | Stored for later use - hard drive, USB, cloud, backup tape | Theft via physical or logical access to the storage media | File/disk encryption, access control lists |
| **In motion** | Actively moving between systems/network | Eavesdropping over public networks (e.g. entering a card number, sending an email) | Transport-layer security (TLS) |

#### 2. The three-part control stack
1. **Policy** - clear rules on appropriate data use and the controls required for sensitive information.
2. **Encryption** - matched to the state: file encryption for data at rest, transport-layer security for data in transit. "Different types of encryption are appropriate for different environments" - one scheme doesn't cover both states.
3. **Access control** - file-system ACLs to govern who may view, modify, or delete data on a device.

#### 3. Big Data adds a new wrinkle
- Chapple explicitly flags that Big Data initiatives introduce **unique security concerns** beyond conventional data security, because Big Data typically forgoes relational databases in favour of **NoSQL key-value stores** for performance reasons - and that architectural shift changes how "appropriate access to sensitive information" even gets defined and enforced.

#### Key Takeaways for BDA601
1. Chapple's at-rest/in-motion split is the simplest possible mental model to bolt onto Ohlhorst's Ch.7 - Ohlhorst explains *why* Big Data security is hard, Chapple gives the two-bucket vocabulary to describe *what* is actually being protected in any given control.
2. Directly relevant to Synergetic/SEQTA/Schoolbox in practice: data at rest = the SQL Server database and its backups; data in motion = SIS-to-portal sync traffic (Synergetic ↔ SEQTA/Schoolbox) and any reporting exports leaving the network - a genuine at-rest/in-motion pair worth naming if this ever comes up in a security-flavoured write-up.
3. Reinforces (does not extend) Ohlhorst's "secure data at rest, protect keys separately" goal from a different, more operational angle.

---

### 3. General Data Protection Regulation (GDPR).

**Citation:** Gdpr-info.eu. (n.d.). General Data Protection Regulation (GDPR). Retrieved from https://gdpr-info.eu/

**Purpose:** The GDPR is the EU's binding legal framework for personal data protection and privacy (effective 25 May 2018) - the closest thing Module 12 has to a worked answer for "what does *lawful, accountable* Big Data privacy actually require, in law."

---

#### 1. Scope: it reaches beyond the EU
- Applies to all EU member states, **and** to non-EU organisations that process the data of, or offer goods/services/monitor the behaviour of, data subjects **in the Union** (Article 3, extraterritorial scope) - precisely "in the Union," not "EU resident," so it also covers visitors and temporary users physically present there. Relevant to any Australian business whose processing meets that test, not just EU-based firms.

#### 2. Lawful basis for processing (Article 6)
- Organisations must have at least one of Article 6's six lawful bases before processing personal data at all: **consent, contract, legal obligation, vital interests, public task, or legitimate interests.** Processing without one of these grounds is unlawful by default, not just risky.

#### 3. Data subject rights (Chapter 3)
| Right | What it gives the individual |
|---|---|
| **Right of Access** | See what data an organisation holds about them |
| **Right to Rectification** | Correct inaccurate data |
| **Right to Erasure** ("right to be forgotten", Art. 17) | Have their data deleted |
| **Right to Data Portability** | Receive their data in a transferable format |
| **Right to Object** | Oppose processing in specified circumstances |

#### 4. Organisational obligations
- **Data protection by design and default** (Article 25) - privacy has to be architected in, not bolted on.
- **Breach notification** to the supervisory authority "without undue delay" and, where feasible, **within 72 hours** (Article 33) - conditional on the breach being likely to result in a risk to individuals, not a universal deadline for every incident.
- **Data Protection Impact Assessments** required for high-risk processing (Article 35).
- **Records of processing activities** must be maintained (Article 30).
- **Risk-based technical and organisational measures** required under Article 32 - encryption and access control are named examples, not a fixed universal checklist.
- Penalties (Article 83) are **tiered by infringement severity**; the higher tier reaches up to **€20 million or 4% of global annual turnover, whichever is higher**.

#### Key Takeaways for BDA601
1. For organisations within its scope, GDPR's Article 32 makes *some* form of technical and organisational security risk-based mandatory - Ohlhorst's controls (encryption, access control, breach response) are legitimate examples of what that can look like, not the literal text of the law.
2. 🔴 **Direct A3 relevance if the report/video touches evaluation criteria or ethics**: the "without undue delay" breach-notification standard and the "by design and default" principle are concrete, citable standards for what "good" data handling looks like - useful if A3 asks you to reflect on responsible use of the JHU COVID dataset or model outputs.
3. School-domain anchor: Synergetic/SEQTA/Schoolbox hold minors' data, governed in Australia by the Privacy Act 1988 and the Australian Privacy Principles (APPs), **not** GDPR. The two aren't equivalent - APPs give access and correction rights, and APP 11.2 requires destruction or de-identification of information once it's no longer needed, but Australia has **no general right to erasure, portability, or objection** the way GDPR does. Useful as a comparative reference model, not as a claim that the same rights apply here.

---

## Where this module fits

**Feeds Assessment 3?** Indirectly. A3's four required components (regression → K-Means → Graph Analytics → visualisation, per the brief and Week 11 lecture) do not include a privacy/security or compliance step - Module 12 is the subject's closing **conceptual/ethical** module, not a technical A3 requirement. If A3's video/report includes any reflection on responsible use of the dataset or model limitations, Ohlhorst's caveat framing (access/availability/performance/liability) and GDPR's "by design and default" principle are legitimate, citable cross-references - but nothing in Module 12 changes the required pipeline.
