# Module 2: Essentials of Cloud Computing and Characteristics

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| R1 | AWS — What is Cloud Computing? (PDF) | ✅ Read + Reviewed |
| R2 | NIST Cloud Computing Program (PDF) | ✅ Read + Reviewed |
| R3 | Naved et al. (2022) — Role of Cloud in Education (PDF) | ✅ Read + Reviewed |
| R4 | Carpenter (2020) — AWS SAA Cert Prep 1: Benefits of Cloud (LinkedIn Learning) | 🔥 WIP — needs manual access |
| R5 | Linthicum (2021) — Learning Cloud Computing: Core Concepts (LinkedIn Learning) | 🔥 WIP — needs manual access |
| R6 | Phillips (2014) — How to Avoid Death by PowerPoint (YouTube) | 🔥 WIP — needs manual access |
| A1 | Race to Fill In the Five Essentials — Discussion Forum | 🕐 To-Do |
| A2 | State of Cloud Adoption in ANZ — Discussion Forum | 🕐 To-Do |
| A3 | Key Cloud Services by Cloud Service Providers — Discussion Forum | 🕐 To-Do |

---

## Key Highlights

### R1 — Amazon Web Services: What is Cloud Computing?

**Source:** Amazon Web Services. (n.d.). *What is cloud computing?* https://aws.amazon.com/what-is-cloud-computing/

**Core Definition**
> "Cloud computing is the on-demand delivery of IT resources over the Internet with pay-as-you-go pricing."
> — AWS

Instead of buying and maintaining physical data centers and servers, organisations access compute, storage, and databases on-demand from a cloud provider.

**Benefits (AWS framework)**

| Benefit | Description |
|---------|-------------|
| **Agility** | Spin up resources in minutes — from compute to ML to data lakes — enabling faster experimentation |
| **Elasticity** | Scale resources up/down dynamically; no need to over-provision for peak loads |
| **Cost savings** | Trade fixed capex (servers, data centres) for variable opex; economies of scale reduce unit costs |
| **Deploy globally in minutes** | AWS has infrastructure worldwide; put apps closer to users to reduce latency |

**Who uses it?**
- Healthcare — personalised patient treatments
- Financial services — real-time fraud detection and prevention
- Gaming — delivering online games to millions globally
- Organisations of every type, size, and industry (backup, DR, dev/test, big data analytics, web apps)

---

### R2 — NIST Cloud Computing Program (SP 500-332)

**Source:** NIST. (2020). *The NIST Cloud Federation Reference Architecture* (Special Publication 500-332). https://doi.org/10.6028/NIST.SP.500-332

> Note: The PDF provided is SP 500-332 — the **Cloud Federation Reference Architecture**, an extension of the foundational NIST cloud definitions (originally SP 800-145). It covers how multiple cloud systems interoperate.

**Cloud Federation — Essential Characteristics**

| Characteristic | Description |
|----------------|-------------|
| **Virtual Administrative Domains** | Federations create logical groupings that span multiple physical cloud environments |
| **Federation Membership & Identity Credentials** | Members share identity credentials across domains to enable cross-cloud access control |
| **Shared Resource Metadata & Discovery** | Resources are described with metadata so consumers can find and use them across boundaries |
| **Federation Governance** | Policies and agreements govern how resources are shared, accessed, and accounted for |

**Three-Plane Model**
Federation interactions are described across three planes:
1. **Trust plane** — identity and credential management across domains
2. **Security plane** — access control, compliance, audit
3. **Resource sharing & usage plane** — actual allocation and consumption of federated resources

**Significance:** NIST standards provide vendor-neutral, authoritative definitions that governments, enterprises, and academia rely on when specifying cloud requirements.

---

### R3 — Naved et al. (2022): Role of Cloud Computing in Educational Institutions

**Source:** Naved, M., Sanchez, D. T., Dela Cruz, A. P., Jr., Peconcillo, L. B., Jr., Peteros, E. D., & Tenerife, J. J. L. (2022). Identifying the role of cloud computing technology in management of educational institutions. *Materials Today: Proceedings, 51*(8), 2309–2312. https://doi.org/10.1016/j.matpr.2021.11.414

**Brief History of Cloud Computing**
- **1950s** — Mainframes: shared access via dumb terminals (shared resource concept)
- **1970s** — Virtualisation software (VMware) → Virtual Machines (VMs)
- **Early 2000s** — Salesforce introduces SaaS; Amazon rebuilds infrastructure with cloud-first design
- **2006** — Google Docs launches cloud document sharing for end users
- **2008** — Gartner: 80% of Fortune 1000 companies planning for cloud; 30% ready to pay

**The NIST Five Essential Characteristics of Cloud Computing**

| # | Characteristic | Key Idea |
|---|----------------|----------|
| A | **On-demand self-service** | Customer provisions compute capacity (storage, server time) automatically, without human interaction with the provider |
| B | **Broad network access** | Services available over the network and accessible via diverse client devices (PC, mobile, PDA) |
| C | **Resource pooling** | Multi-tenant model: provider pools resources, dynamically assigned to consumers; location is abstracted |
| D | **Rapid elasticity** | Capabilities scale up/down automatically (or quickly); from the consumer's view, resources appear unlimited |
| E | **Measured service** | Cloud systems automatically monitor, control, and report resource usage — transparency for both provider and consumer |

**Cloud in Education — Roles**

| Role | Description |
|------|-------------|
| Personalized learning | Flexible, internet-accessible content in multiple formats; e-learning without client-side software |
| Virtual classroom | Online classes, assignments, quizzes, forums, feedback — accessible from any device |
| Reduced cost / virtualization | No upfront hardware/software capex; pay-per-use model lowers total cost of ownership |
| Greater reach | Students and teachers work from any location; cloud enables learner-centered environments |
| Secure data storage | Centralized, remote servers with access monitoring; supports exams and submissions |
| Application integration | Single integrated platform removes siloed systems; reduces IT maintenance burden |

**Cloud Adoption Challenges in Education**

| Challenge | Notes |
|-----------|-------|
| Integration & security | Service integration complexity; securing data in transit and at rest |
| Risk & compliance | Loss of data location control in shared environments; vendor lock-in risk |
| Governance | Institutions need new frameworks for cloud decision-making and policy |
| IT staffing | New skill sets required; outsourcing changes IT roles significantly |
