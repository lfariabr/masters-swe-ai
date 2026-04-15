# Module 10 — Security Threats while in cloud - Mitigation and Identification

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | **Read & summarise University Australia (2022) — Cloud Security short course** | **✅** |
| **2** | **Watch & summarise Media Design School (2022) — Cloud Computing Fundamentals (video transcript)** | **✅** |
| **3** | **Read & summarise Mello (2022/2024) — 7 top cloud security threats, CSO Online** | **✅** |
| **4** | **Read & summarise Ablett (2022) — 7 ways I'd hack you on AWS** | **✅** |
| **5** | **Read & summarise Estrin (2022) — Cloud Security Handbook, Chapter 8** | **✅** |
| 6 | Activity 1: Components of Cloud Data Security — Discussion Forum | 🕐 |
| 7 | Activity 2: Major Cloud Security Threats — Discussion Forum | 🕐 |

---

## Key Highlights

---

### 1. University Australia (2022). Cloud Security [Short course].

**Citation:** University Australia. (2022). Cloud security [Short course]. Torrens University Blackboard.

**Purpose:** A foundational short course covering cloud security concerns and best practices. Establishes the vocabulary and threat surface that all other Module 10 resources build on.

---

#### 1. Why Cloud Security Matters
- **Cloud = remote servers** → security concerns that don't exist with local infrastructure
- Key concerns: **data breaches**, **insecure APIs**, **data loss**, **cloud service abuse**, **malware injection**
- As cloud adoption grows, security literacy becomes non-negotiable for practitioners

#### 2. Course Objectives (the "know-how" ladder)
| Level | Objective |
|-------|-----------|
| Awareness | Recognise cloud characteristics and definitions |
| Understanding | Grasp service and deployment model security implications |
| Analysis | Distinguish vulnerabilities and common security concerns |
| Application | Apply best practices and security techniques |

#### 3. Key Topics Covered
- **Security Concerns in Cloud Computing** — threat landscape overview
- **Cloud Security Techniques and Best Practices** — controls and countermeasures
- **Shared Responsibility Model** — who owns what between provider and customer

#### Key Takeaways for CCF501
1. The **Shared Responsibility Model** is the conceptual backbone for all cloud security decisions — every threat in this module maps back to "whose job is it to fix this?"
2. The short course frames the threats broadly; Resources 2–5 drill into specifics (attack types, frameworks, real attack vectors)
3. Connects directly to Activity 1 (data security controls) and Activity 2 (selecting and discussing major threats)

---

### 2. Media Design School (2022). Cloud Computing Fundamentals [Video transcript].

**Citation:** Media Design School. (2022). Cloud computing fundamentals [Video]. Kaltura Media.

**Purpose:** A revision video (with transcript) covering key cloud computing concepts, then focusing on security threats and mitigation strategies in cloud environments.

---

#### 1. Security Threats Covered

| Threat | Description |
|--------|-------------|
| **Email spam** | Compromised accounts used to bombard customers |
| **DDoS attacks** | Repeated requests overwhelm network/compute/bandwidth |
| **API-based attacks** | Hackers inject bugs or take over systems via API hooks |
| **Phishing campaigns** | Social engineering to steal credentials |
| **Data leaks** | Expose IP, invite regulatory penalties (e.g., GDPR) |

#### 2. Multi-Tenancy Risk
- **Multi-tenancy** offers cost savings but increases attack surface
- Risks include: deliberate/unintentional **tenant interference**, **snooping via bandwidth monitoring**, **identity-agnostic access policies**

#### 3. API Attack Anatomy
- APIs = keys to underlying cloud services
- **Injection** of malicious code through untested API hooks
- **Unauthorised data extraction** via unexpected access patterns
- **Inadequate authentication** on API endpoints → intrusion and privacy breaches

#### 4. Mitigation Strategies

| Threat | Mitigation |
|--------|-----------|
| General | Multi-layer threat detection; role-based + multi-step auth |
| APIs | Comprehensive testing; API gateways + IAM; automated monitoring |
| DDoS | Transport-layer IP blocks; blacklisting tools; cloud-native DDoS protection |
| New VMs | Automatically apply group security policies on provisioning |

#### 5. Shared Responsibility in Practice
- Compliance is a *starting point*, not the whole answer
- Due diligence before signing up to a provider is essential
- Both budget and premium providers face the same threat categories

#### Key Takeaways for CCF501
1. Connects the deployment model choice (from earlier modules) to security posture — the model you pick determines your threat surface
2. Multi-tenancy is a core cloud feature with real security trade-offs; useful for Assessment 2 cloud provider comparisons
3. DDoS and API attacks are the two most "cloud-native" threats — legacy on-prem defences don't fully translate

---

### 3. Mello, J. P., Jr. (2022/2024). 7 top cloud security threats. CSO Australia.

**Citation:** Mello, J. P., Jr. (2022, July 4; updated 2024, Jul 31). 7 top cloud security threats. CSO Australia. https://www.csoonline.com/article/3043030/top-cloud-security-threats.html

**Purpose:** A practitioner-level overview of the seven most probable cloud security threats enterprises face, with expert-attributed mitigation guidance. Required reading for identifying threats and mitigation strategies.

---

#### 1. The Seven Threats at a Glance

| # | Threat | Core Risk |
|---|--------|-----------|
| 1 | **Human errors** | Misconfigurations, clicked phishing links — hardest to eliminate |
| 2 | **Cloud-assisted malware** | Cloud storage (Drive, Dropbox) weaponised for malware delivery |
| 3 | **Data theft** | Leading threat; affects hybrid cloud and AI systems; ~1/3 of incidents |
| 4 | **Credentials theft** | Primary initial vector; legitimate credentials = invisible attacker |
| 5 | **Poor access management** | Distributed cloud permissions → overly broad developer grants |
| 6 | **DoS/DDoS attacks** | Resource exhaustion; disrupt critical ops without data breach |
| 7 | **Data exfiltration** | Silent, long-tail damage: IP theft, competitive erosion, legal action |

#### 2. Human Errors (Threat #1) — Deep Dive
- Multi-cloud complexity magnifies human error risk (different rules per cloud)
- **Fix:** Regular training cycles — teach users what unusual looks like
- Complex environments require humans to follow consistent protocols across all devices/accounts

#### 3. Credentials Theft (Threat #4) — Deep Dive
- **Insidious** because authorised-vs-unauthorised access looks identical
- Attacker can cause major damage in minutes after infiltration
- **Fix (layered approach):**
  1. Strong MFA — first line
  2. Dark web monitoring + social engineering training — second line

#### 4. Data Exfiltration (Threat #7) — Deep Dive
- **Definition:** Electronic transmission of data to an unauthorised external location
- Entry points: vulnerability exploitation, misconfigurations, compromised credentials
- **Long-term consequences:** stolen IP → competitive disadvantage; regulatory/legal exposure; operational downtime

#### 5. Mitigation Approaches by Threat

| Threat | Primary Mitigation |
|--------|-------------------|
| Human errors | Regular security training, established protocols |
| Cloud-assisted malware | Endpoint logging (Sysmon, PowerShell logs), user alerting |
| Data theft | Strategic, integrated approach: access controls + threat intelligence |
| Credentials theft | MFA + dark web monitoring + social engineering awareness |
| Poor access management | Strict network access policy + abstraction layer for non-security teams |
| DoS/DDoS | Basic cyber hygiene: IDS, network monitoring, cloud-native DDoS filters |
| Data exfiltration | Data classification, access controls, monitoring |

#### Key Takeaways for CCF501
1. These seven threats directly map to Activity 2 — pick three and discuss mitigation; Threats 3, 4, and 7 are the strongest choices for a 250-word response
2. **Human error + credentials theft** account for the majority of actual breaches — technical controls alone are insufficient; process and training matter
3. DDoS is the only threat that doesn't necessarily cause data loss — important nuance for distinguishing availability vs. confidentiality impacts

---

### 4. Ablett, J. (2022). Secure Cloud Computing: 7 Ways I'd Hack You on AWS. Adelia Risk.

**Citation:** Ablett, J. (2022, April 4). Secure cloud computing: 7 ways I'd hack you on AWS. Adelia Risk. https://adeliarisk.com/secure-cloud-computing-7-ways-id-hack-aws/

**Purpose:** Practitioner-written attack simulation for AWS environments, explaining seven real attack vectors and their corresponding defences. Concepts transfer to any cloud provider.

---

#### 1. The Seven Attack Vectors

| # | Attack | How It Works | Fix |
|---|--------|-------------|-----|
| 1 | **Little Phish** (credential phishing) | Fake AWS login page steals credentials | Enable **2FA** on all accounts |
| 2 | **Big Phish** (spear phishing) | Targeted attack on admins using social engineering | Never use root for daily tasks; isolate root to billing only |
| 3 | **Password reuse** | Credentials from breached sites tried on AWS | Unique password per account + password manager |
| 4 | **Access key theft** | AWS access keys (strings, no password) give full server control | Encrypted storage, never email keys, rotate regularly, CloudWatch billing alerts |
| 5 | **GitHub exposure** | Dev accidentally commits access keys to public repo | Never embed keys in code; bots constantly scan GitHub |
| 6 | **Web app attacks** (OWASP Top 10) | SQLi, XSS, and other app-layer attacks | IP whitelisting, Security Groups, AWS WAF, Amazon VPC |
| 7 | **Advanced Persistent Threat (APT)** | Deep malware infection impossible to clean in place | Robust backup strategy; restore to new servers; preserve infected ones as evidence |

#### 2. The Root Account Principle
- **Root** = all-powerful AWS account; should only exist for initial setup + billing
- Create separate IAM accounts with minimal necessary permissions (least privilege)
- Change root password to something complex; enable 2FA on root

#### 3. Access Key Hygiene — Critical Rules
1. Store only on encrypted machines
2. **Never** send via email
3. **Never** generate a key for the root account
4. Set expiration dates; rotate periodically
5. Remove unused keys immediately

#### 4. Defence-in-Depth Stack for AWS

```
Layer 1: IAM (least privilege, separate accounts, no root for ops)
Layer 2: MFA / 2FA (all accounts, especially root)
Layer 3: Unique credentials + password manager
Layer 4: Key management (rotation, no code embedding, no GitHub exposure)
Layer 5: Network controls (Security Groups, WAF, VPC, IP whitelisting)
Layer 6: Monitoring (CloudWatch, billing alerts)
Layer 7: Backups (EBS, S3, Glacier — restore to clean servers if APT)
```

#### 5. The GitHub Bots Problem
- Automated bots continuously scan GitHub for exposed AWS access keys
- Real incident: developer published keys → attackers spun up 140 new servers for litecoin mining
- **Fix:** Use temporary access keys; enforce code review policy to catch embedded keys

#### Key Takeaways for CCF501
1. Most AWS-specific concepts (Security Groups, CloudWatch, IAM, access keys) generalise to Azure and GCP with equivalent services — useful for provider comparison in Assessment 2
2. **Root account management** is the #1 practical risk many organisations miss — connects to poor access management in Resource 3
3. The "nuke from orbit" APT response (backup + restore rather than clean-in-place) is the industry standard — illustrates why backup strategy is a security control, not just a DR tool

---

### 5. Estrin, E. (2022). Cloud Security Handbook: Chapter 8 — Understanding Common Security Threats to Cloud Services. Packt.

**Citation:** Estrin, E. (2022). Cloud security handbook: Find out how to effectively secure cloud environments using AWS, Azure, and GCP. Packt. https://learning-oreilly-com.torrens.idm.oclc.org/library/view/cloud-security-handbook/9781800569195/

**Purpose:** Academic-grade chapter covering the MITRE ATT&CK framework and four major cloud threat categories with detection/mitigation guidance across AWS, Azure, and GCP.

---

#### 1. The MITRE ATT&CK Framework

**Definition:** A knowledge base of hacking techniques organised as a kill chain of attack stages.

| Stage | Description |
|-------|-------------|
| Initial access | Gaining entry to the environment |
| Execution | Running malicious code |
| Persistence | Maintaining access across sessions |
| Privilege escalation | Gaining higher-level permissions |
| Defense evasion | Avoiding detection |
| Credential access | Stealing credentials |
| Discovery | Mapping the environment |
| Lateral movement | Moving through systems |
| Collection | Gathering target data |
| Exfiltration | Sending data outside |
| Impact | Disrupting/destroying systems |

- MITRE provides separate **Cloud**, **IaaS**, and **SaaS** matrices
- Mapping your controls to the MITRE framework reveals gaps in your defence

#### 2. Data Breaches — Detection & Mitigation

**Key insight:** Under the shared responsibility model, the cloud customer always owns application-layer security. SaaS providers vary wildly in maturity — always evaluate before signing.

| Data Type | Sensitivity |
|-----------|------------|
| Public data | Low — safe to expose |
| Intellectual property / trade secrets | Critical — competitive damage if exposed |
| PII | Regulated — GDPR, HIPAA exposure |

**Breach consequences:** confidentiality loss → reputational damage → regulatory fines → ransomware availability impact

**Best practices:**
- Network ACLs + security groups (access control)
- Encryption in transit and at rest
- Audit trails (CloudTrail / Azure Monitor / GCP Logging)
- Threat management (GuardDuty / Defender / Security Command Center)
- Disaster recovery plan with tested backups

#### 3. Misconfigurations — Detection & Mitigation

**Root causes:**
- Lack of knowledge in operating cloud services
- Human error
- Default settings left unsecured
- Fast, unmanaged changes in complex environments

**Common misconfigs:**

| Misconfiguration | Example |
|-----------------|---------|
| Overly broad IAM | Default permissions to sensitive resources |
| Public object storage | S3 bucket open to the internet |
| Public snapshots/VM images | Anyone can download your disk images |
| Public databases | DB accessible without VPN |
| SSH/RDP exposed | Servers reachable on port 22/3389 from 0.0.0.0/0 |
| Unpatched servers | Known CVEs unaddressed |

**Fix:** CSPM tools (AWS Security Hub, Azure Defender, GCP Security Command Center) + infrastructure-as-code for standardised deployments + employee training

#### 4. Insufficient IAM & Key Management

**Core principle violated:** Principle of least privilege

**Common failures:**
- Excessive permissions granted
- Weak password policies
- No MFA enforced
- Keys embedded in code
- No key rotation
- No audit trails → zero visibility

**Best practices summary:**
- Full identity lifecycle management (provisioning → deprovisioning)
- Central identity repository with federation
- Block legacy auth protocols (NTLM, clear-text LDAP)
- Enforce MFA across all accounts
- Use SIEM for anomalous behaviour detection
- Rotate and centrally manage encryption keys + secrets

#### 5. Account Hijacking — Detection & Mitigation

**Definition:** Unauthorised person uses a compromised account (human or service account) to act on behalf of it.

**Consequences beyond data theft:**
- Ransomware infection
- **Denial of wallet** — attacker spins up expensive resources (e.g., Bitcoin mining) on your bill
- Website defacement

**Common vectors:**
1. Phishing against admin accounts
2. Access keys stored in public S3 bucket
3. Weak admin passwords → permission escalation

**Mitigation stack:**
- Strong passwords + MFA (non-negotiable)
- Principle of least privilege + segregation of duties
- Employee awareness training for phishing detection
- SIEM for anomalous login patterns
- Business continuity planning for post-compromise recovery

#### 6. Cloud Security Services Comparison

| Concern | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Network access | VPC, Security Groups, Network Firewall | NSGs, Azure Firewall | VPC Firewall Rules |
| IAM | AWS IAM, Directory Service | Azure AD, Azure AD DS | Google Cloud IAM |
| Encryption | KMS, Secrets Manager | Key Vault | Cloud KMS, Secret Manager |
| Threat detection | GuardDuty, Inspector | Defender for Cloud, Sentinel | Security Command Center |
| Audit | CloudTrail, CloudWatch | Azure Monitor, Log Analytics | Cloud Logging |
| Misconfiguration | Config, Security Hub, Trusted Advisor | Defender for Cloud, Advisor | Security Command Center |
| Configuration enforcement | Control Tower, CloudFormation | Azure Policy, Resource Manager | Resource Manager, Deployment Manager |

#### Key Takeaways for CCF501
1. **MITRE ATT&CK** is the industry standard for mapping attacks — knowing the kill chain lets you design defence at each stage rather than reacting post-breach
2. **Misconfigurations** are the most preventable threat — CSPM tools and IaC close most of the gap without relying on humans to get defaults right
3. The **cross-provider comparison table** above is directly useful for Assessment 2 (provider comparisons) and any exam question about cloud-native security tools
4. **Account hijacking → Denial of Wallet** is a cloud-specific risk with no on-premises equivalent — worth highlighting in Activity 2

---

## Activity Reference Notes

### Activity 1: Components of Cloud Data Security
*Source: Thompson, G. (2020). CCSK Certificate of Cloud Security Knowledge. Chapter 11.*

Key areas to address in the Discussion Forum response:
- **Three main components of cloud data security controls** (from the reading): likely encryption, access control, and data classification/monitoring
- **Tools for monitoring cloud data transfers:** audit logs, VPC flow logs, SIEM systems
- **Cloud data access controls:** IAM policies, role-based access control (RBAC), network-level controls

### Activity 2: Major Cloud Security Threats
*Source: Check Point. (2021). Main cloud security issues and threats in 2021.*

Suggested three threats for discussion (strongest for 250-word response):
1. **Data breaches** — most widespread, regulatory implications, cross-provider relevance
2. **Account hijacking** — practical severity, includes Denial of Wallet (cloud-unique)
3. **Misconfigurations** — most preventable, human error root cause, CSPM solution

Each should include: what the threat is → how it manifests → mitigation strategy
