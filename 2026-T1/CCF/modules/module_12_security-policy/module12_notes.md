# Module 12 — Implementation of Security Policy

## TL;DR

- **Cloud security policy** spans DDoS protection, application-layer firewalls, SIEM platforms, and formalised risk management frameworks — every provider has its own toolset.
- **AWS Shield** (Standard + Advanced) defends infrastructure-layer attacks (L3/L4) automatically; **AWS WAF** handles HTTP/S threats (L7) via web ACLs and rule groups.
- **Microsoft Sentinel** is a cloud-native SIEM/SOAR that uses ML to cut alert fatigue; MSSPs like Quorum wrap it into affordable managed-security products for SMBs.
- **NIST's RMF** (SP 800-37) provides a vendor-neutral 6-step cycle — Categorise → Select → Implement → Assess → Authorise → Monitor — applicable to cloud providers *and* consumers.
- Security posture is not just technology: governance, compliance (PCI-DSS, HIPAA, GDPR), and continuous monitoring are equally critical.

---

## Task List

| # | Task | Status |
|---|------|--------|
| **1** | **Read & summarise Amazon Web Services (2022) — OutSystems / AWS Shield Advanced case study** | ✅ |
| 2 | Watch & summarise Carpenter, T. (2020) — AWS WAF LinkedIn Learning video | 🔥 WIP — needs manual watch |
| 3 | Watch & summarise Lachance, D. (2020) — Azure Cloud Firewall LinkedIn Learning video | 🔥 WIP — needs manual watch |
| **4** | **Read & summarise Microsoft (2021) — Quorum / Microsoft Sentinel case study** | ✅ |
| **5** | **Read & summarise RSI Security (2022) — NIST cloud security policy recommendations** | ✅ |
| 6 | Watch & summarise Kaushal, S. (2022) — Azure Firewall Policies LinkedIn Learning video | 🔥 WIP — needs manual watch |
| 7 | Activity 1: Established vs Newbie — cloud provider security offerings post | 🕐 |
| 8 | Activity 2: AWS WAF components, protected resources, ACL vs rule groups | 🕐 |
| 9 | Activity 3: AWS Shield Advanced — OSI layers, detection & mitigation | 🕐 |

---

## Key Highlights

---

### 1. Amazon Web Services (2022). Cost and time savings achieved, security posture strengthened using AWS Shield Advanced with OutSystems.

**Citation:** Amazon Web Services. (2022). Cost and time savings achieved, security posture strengthened using AWS Shield Advanced with OutSystems. https://aws.amazon.com/solutions/case-studies/outsystems-case-study/

**Purpose:** Demonstrates how OutSystems — a low-code platform — deployed AWS Shield Advanced to achieve a scalable, managed DDoS defence for their cloud web applications on AWS. *(Note: the original case study URL redirects; the highlights below synthesise the resource overview with supplementary AWS technical material.)*

---

#### 1. Opportunity — The Problem OutSystems Faced

- **OutSystems** provides a low-code platform so companies can build, launch, and manage cross-channel business apps.
- As a platform hosting apps *for* other businesses, any downtime or degradation from DDoS attacks translates directly to **customer SLA breaches** and **reputational loss**.
- They needed a security solution that could scale with their AWS footprint without requiring a dedicated in-house DDoS team.

#### 2. Solution — AWS Shield Advanced

| Feature | Description |
|---|---|
| **Shield Standard** | Always-on, no-cost; protects all public IPs on AWS against common L3/L4 attacks |
| **Shield Advanced** | Subscription tier with enhanced detection thresholds, faster mitigation, and SRT access |
| **SRT (Shield Response Team)** | AWS experts who provide live assistance during active DDoS events |
| **Proactive engagement** | SRT reaches out to the customer when attack criteria are met on protected resources |
| **WAF integration** | Shield Advanced coordinates with AWS WAF to inspect and block application-layer (L7) floods |

- Protected resource types: CloudFront distributions, Route 53 hosted zones, Global Accelerator, Application/Classic Load Balancers, EC2 Elastic IPs.
- Mitigation is **packet-level**: blocked traffic never reaches the application, enabling defence at terabit-per-second scales.

#### 3. How DDoS Attacks Work (Context)

**Infrastructure-layer attacks (L3/L4):**
- Packet-level floods using **amplification** (e.g., DNS reflection: 64-byte request → 3,400-byte response, ×50 amplification).
- Distributed: 1,000 compromised systems × 10,000 packets/s = multi-gigabyte-per-second floods.

**Application-layer attacks (L7):**
- HTTP floods targeting specific pages (e.g., login page).
- **Cache-busting attacks**: vary query strings to bypass CDN caches and hammer the origin server.
- Can reach hundreds of millions of requests per second.

#### 4. Outcome

- Strengthened security posture without additional in-house security headcount.
- Cost savings from consolidated subscription (one fee covers all accounts in an AWS Organization).
- Time savings from automated detection and mitigation — no manual intervention required for standard events.

#### Key Takeaways for CCF501

1. **Shield Advanced + WAF is the AWS answer to end-to-end DDoS defence** — Standard covers infrastructure layers automatically; Advanced + WAF adds application-layer intelligence.
2. For Activity 3, the OSI layers protected are L3 (network volumetric), L4 (protocol attacks), and L7 (application floods).
3. The OutSystems case illustrates how a platform-as-a-service provider must protect not just itself but its *customers' applications* — security policy must account for upstream/downstream stakeholders.

---

### 4. Microsoft (2021). Quorum bases its Cyber One solution on Microsoft Sentinel, easing and lifting security for customers like CountPlus.

**Citation:** Microsoft. (2021). Quorum bases its Cyber One solution on Microsoft Sentinel, easing and lifting security for customers like CountPlus. https://customers.microsoft.com/en-us/story/1435310687711059601-countplus-professional-services-security

**Purpose:** Case study showing how Australian MSSP Quorum Systems built a managed-security product (Cyber One) on Microsoft Sentinel to deliver enterprise-grade security to small and mid-size businesses — with CountPlus (an accounting network) as the reference customer.

---

#### 1. The Business Problem

- SMBs like **CountPlus** (a network of 16 accounting firms) cannot afford a dedicated in-house security team but face the same threat landscape as enterprises.
- Manual ticket-based security monitoring created delays; CountPlus's IT manager was time-constrained.
- Quorum set out to build a product that: avoids duplicating existing portals, reduces insight complexity, and can be priced affordably.

#### 2. What Cyber One Is

**Cyber One** is a managed security incident and event management (SIEM) portal built on top of the Microsoft security stack:

| Component | Role in Cyber One |
|---|---|
| **Microsoft Sentinel** | Core SIEM/SOAR — ingests, correlates, and surfaces alerts with ML |
| **Microsoft Defender for Cloud** | Cloud workload protection; feeds signals into Sentinel |
| **Defender for Office 365 / Endpoint / Identity** | Endpoint and identity telemetry |
| **Microsoft Entra ID** (Azure AD) | Identity data source |
| **Microsoft Secure Score** | Quantifies customer security posture; guides hardening priorities |
| **Azure dashboards** | Self-service insight layer for CountPlus IT manager |

- Cyber One is described as "a wrapper" — it surfaces the right data from multiple Microsoft portals in one place without requiring customers to hold a Microsoft 365 E5 licence outright.

#### 3. Key Capabilities Unlocked

- **ML-driven false positive reduction**: Sentinel's ML performs heavy lifting before alerts reach Quorum analysts; very few false positives reach the operations team.
- **Automated ticket creation**: All high-severity alerts auto-generate tickets in Quorum's ITSM board, enforcing SLA compliance and enabling ownership transfer.
- **Push notifications for on-call**: Replaces expensive 24/7 human monitoring — on-call engineers get push alerts and respond immediately.
- **Real-time customer visibility**: CountPlus IT staff can view Quorum's progress live — transparent, self-serve dashboards.
- **Extended Detection and Response (XDR)**: One Microsoft interoperability enables XDR across the entire Microsoft 365 E5 estate — everything is connected, on, and tuned.

#### 4. Outcome for CountPlus

| Metric | Result |
|---|---|
| **Time to go live** | < 6 weeks |
| **Microsoft Secure Score** | Jumped to 79% post-deployment |
| **Cost vs. alternatives** | 4× less expensive than comparable solutions |
| **Monitoring quality** | More comprehensive; incidents identified earlier |

#### 5. Strategic Observations

- **MISA membership** (Microsoft Intelligent Security Association) gives Quorum access to Microsoft engineering and peer intelligence — a competitive moat.
- Quorum argues that **"One Microsoft" interoperability** beats "best of breed" multi-vendor strategies for MSSP economics and XDR capability.
- **Secure Score is contextual**: a score of 70–80% may be appropriate for an SMB; what matters is that it is *attainable, understandable, and safe* for the specific organisation.

#### Key Takeaways for CCF501

1. Microsoft Sentinel is the Azure-native equivalent of AWS Security Hub + WAF threat intelligence — cloud providers converge on ML-powered, centralised security operations.
2. This case study is a direct comparison point for Activity 1: a cloud-native accounting firm (CountPlus, post-digital era) uses cloud-native security tools; a pre-digital firm would likely have legacy on-prem SIEM integration challenges.
3. MSSPs like Quorum demonstrate how cloud security policy is *operationalised* in practice — not just configured once but continuously monitored, scored, and improved.

---

### 5. RSI Security (2022). Understanding cloud security policy: NIST's recommendations.

**Citation:** RSI Security. (2022, May 3). Understanding cloud security policy: NIST's recommendations. RSI Security. https://blog.rsisecurity.com/understanding-cloud-security-policy-nists-recommendations/

**Purpose:** Explains how NIST's "Managing Risk in the Cloud" framework (drawn from SP 800-37) helps organisations — both cloud providers and consumers — develop a structured, risk-based cloud security policy.

---

#### 1. Why NIST for Cloud Security?

- NIST provides a **vendor-neutral**, standards-based framework applicable to any cloud deployment model (public, private, hybrid, community) and any service model (IaaS, PaaS, SaaS).
- Cloud security threats impact: critical digital assets (databases, app-hosting systems), individuals (customers, employees), and operations (mission objectives, organisational reputation).
- Organisations that follow NIST stay "steps ahead of cybercriminals looking to exploit gaps."

#### 2. Three Levels of Risk Management

| Level | Scope |
|---|---|
| **Organisation-level** | Governance policies, risk appetite, board-level decisions |
| **Mission/business process-level** | Departmental risk across specific workflows |
| **Information system-level** | Technical controls per system or application |

Effective cloud security policy coordinates all three levels simultaneously.

#### 3. The NIST Risk Management Framework (RMF) — 6 Steps

The RMF (NIST SP 800-37) structures cloud security into a continuous lifecycle:

| Step | Name | Key Actions |
|---|---|---|
| **1** | **Categorise** | Classify information based on operational, security, and privacy requirements; system impact analysis |
| **2** | **Select** | Choose baseline security controls; assess risk in current operating environment; document the security plan |
| **3** | **Implement** | Deploy security controls; document operating environment and configuration |
| **4** | **Assess** | Evaluate whether controls are properly implemented and achieving desired outcomes |
| **5** | **Authorise** | Formally accept operating risk; authorise system to operate |
| **6** | **Monitor** | Continuously assess control effectiveness; document environmental changes; report posture changes |

- The RMF integrates with the **System Development Life Cycle (SDLC)** — security is designed in from initiation, not patched in later.
- Steps 1–2 = **Risk Assessment** | Steps 3–5 = **Risk Treatment** | Step 6 = **Risk Control**

#### 4. NIST Recommendations for Cloud Providers

| Area | Requirement |
|---|---|
| **Regulatory compliance** | PCI-DSS (payments), HIPAA (healthcare), GDPR (EU data subjects) |
| **Optimised security** | Centralised cloud architecture enables specialised, consistent security controls across all tenants |
| **Shared responsibility** | Providers manage infrastructure security; consumers manage their configurations and data |

#### 5. NIST Recommendations for Cloud Consumers (9-Step Process)

For organisations *adopting* cloud services, NIST recommends:

1. Define which services/applications the cloud solution will support.
2. Determine functional capabilities required.
3. Identify privacy and security requirements per NIST security category.
4. Select the most appropriate cloud architecture (deployment model × service model).
5. Designate actors responsible for each cloud environment (providers, brokers).
6. Understand the security posture of the cloud provider — baseline controls, compliance, compensating controls.
7. Assign and document organisation-specific security parameters.
8. Establish internal enhancements beyond provider baseline.
9. List specifications for controls that don't yet meet baseline requirements.

#### 6. SDLC Integration

The SDLC phases align to RMF to ensure security is continuous:

| SDLC Phase | Security Concern |
|---|---|
| Initiation | Define security and privacy requirements |
| Analysis | Assess feasibility of controls; identify risks |
| Design | Architect security controls into the system |
| Implementation | Configure and deploy controls |
| Maintenance | Periodic configuration management; continuous monitoring |
| Disposal | Secure decommissioning of end-of-life components |

#### Key Takeaways for CCF501

1. **The RMF is provider-agnostic** — it applies equally to AWS Shield/WAF environments (Resources 1–2) and Azure Sentinel/Firewall environments (Resources 3–4, 6).
2. For Activity 1 (established vs. newbie organisations): a pre-digital firm inherits legacy compliance obligations and on-prem integrations; a post-digital firm can adopt native cloud security from day one — their RMF starting points are very different.
3. The Monitor step (Step 6) maps directly to tools like Microsoft Sentinel and AWS Shield event dashboards — technology operationalises the framework.
4. Cloud consumers must negotiate security requirements in **service agreements** — the RMF's consumer 9-step process is the academic backing for due-diligence checklists in procurement.

---

## Activity 2 Prep — AWS WAF (from Developer Guide)

*Source: A2-WAF.pdf — AWS WAF, AWS Firewall Manager, AWS Shield Advanced Developer Guide*

**Q1: What are the main components of AWS WAF?**

- **Web ACL (Access Control List)**: An ordered list of rules applied to incoming HTTP/S requests. The first matching rule determines the action taken; subsequent rules are not evaluated.
- **Rules**: Evaluate request attributes (URI, headers, query strings, body, source IP, geolocation, request size) using string matches, regex patterns, or size conditions. Rules can combine AND/OR/NOT logic.
- **Rule Groups**: Reusable sets of rules that can be shared across multiple web ACLs.
- **Amazon Managed Rules (AMRs)**: Pre-built rule sets maintained by AWS covering general threats, OS-specific threats, application-specific threats (e.g., WordPress), bot/fraud detection, and Amazon threat intelligence (e.g., known DDoS source IPs).

**Q2: Resources protected by AWS WAF**

- Amazon CloudFront distributions
- Amazon API Gateway REST APIs
- Application Load Balancers
- AWS AppSync GraphQL APIs
- Amazon Cognito user pools
- AWS App Runner services
- AWS Verified Access instances
- AWS Amplify

**Q3: Rule Groups vs. Web ACLs**

| Feature | Web ACL | Rule Group |
|---|---|---|
| **Definition** | Ordered policy document attached to a protected resource | Reusable collection of rules |
| **Scope** | Tied to one or more specific resources | Independent; shared across multiple web ACLs |
| **Capacity** | Measured in WCUs (Web ACL Capacity Units); default 1,500 WCUs | Consumes WCUs within any web ACL that includes it |
| **Actions** | Allow, Block, Count, CAPTCHA/Challenge | Defined per rule within the group |
| **Managed by** | Customer or AWS (via AMRs) | AWS (AMRs), third-party Marketplace vendors, or customer |

---

## Activity 3 Prep — AWS Shield Advanced (from Developer Guide)

*Source: A2-SHIELD.pdf — AWS WAF, AWS Firewall Manager, AWS Shield Advanced Developer Guide (pp. 925+)*

**Q1: OSI Layers protected by AWS Shield**

| Layer | Attack Type | Shield Tier |
|---|---|---|
| **Layer 3** (Network) | Volumetric attacks — saturate network capacity | Standard + Advanced |
| **Layer 4** (Transport) | Protocol attacks — e.g., TCP SYN floods exhausting connection state | Standard + Advanced |
| **Layer 7** (Application) | HTTP/S floods — e.g., web request floods, cache-busting | Advanced only (via WAF integration) |

**Q2: How AWS Shield detects and mitigates DDoS attacks**

**Detection:**
- Shield Advanced establishes a **baseline** of normal traffic patterns per protected resource.
- Applies **lower detection thresholds** than Standard (mitigates at 50% of calculated capacity) → faster response to slow-ramp attacks.
- **Health-based detection**: Integrates with Route 53 health checks — if the health check is unhealthy during a detected event, Shield Advanced places mitigations faster.
- For L7 (with WAF): analyses requests, not just packets, for more accurate HTTP flood detection.
- Publishes **CloudWatch metrics** (DDoS detection, mitigation status per resource) and **Shield console events** for visibility/alerting.

**Mitigation:**
- **Infrastructure-layer (L3/L4)**: Packet-level blocking at the AWS network perimeter — blocked traffic never reaches the application.
- **Application-layer (L7)**: Shield Advanced coordinates with AWS WAF; can **automatically create WAF rules** to block anomalous request patterns during active events.
- **Intermittent attack protection**: Mitigations use exponentially increasing TTL for resources that are frequently targeted.
- **SRT escalation**: During active events, customers can engage the Shield Response Team (SRT) for expert assistance.
