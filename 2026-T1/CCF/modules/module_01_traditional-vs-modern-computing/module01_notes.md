# Module 1: Traditional vs Modern Computing

## Task List

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise McHaney (2021) — Cloud technologies Ch.1 | ✅ |
| 2 | Watch & summarise Nishimura (2022) — Intro to AWS videos | ✅ |
| 3 | Read & summarise Eliaçık (2022) — Pros/cons of cloud computing | ✅ |
| 4 | Watch & summarise Accenture (2020) — Why cloud matters | ✅ |
| 5 | Read & summarise Manvi & Shyam (2021) — Virtualisation Ch.4 | ✅ |
| 6 | Activity 1: Introduce Yourself | 🕐 |
| 7 | Activity 2: Break the Ice | 🕐 |
| 8 | Activity 3: TCO Thinking Exercise | 🕐 |

---

## Key Highlights

### 1. McHaney, R. (2021). Cloud Technologies — Chapter 1

**Citation:** McHaney, R. (2021). Cloud technologies: An overview of cloud computing technologies for managers. Wiley. Retrieved from https://ieeexplore-ieee-org.torrens.idm.oclc.org/servlet/opac?bknumber=9820907

**Purpose:** Overview of cloud computing foundations — cost drivers, capacity planning, deployment/service models, enabling technologies (virtualisation, SOA), and historical evolution from mainframes to cloud.

---

#### 1. Core Definitions
- **Cloud computing** = Delivering computing services over the Internet (servers, storage, databases, networking, software, analytics)
- "Cloud" symbol from old flow charts representing the Internet
- Focus areas: **Cost reduction, capacity planning, business agility**

#### 2. Cost Considerations
- Two cost types: Purchase costs + Operational costs
- **Operational overhead** often exceeds upfront investment over time
- Includes: personnel, training, upgrades, utilities, security, help desk
- IT costs often viewed as "cost sink" → cloud helps eliminate many expenses

#### 3. Capacity Planning Challenges
- **Under-provisioned** = can't meet user needs
- **Over-provisioned** = waste/inefficiency
- Three strategies:
  - **Match**: Add resources incrementally
  - **Lead**: Add capacity in anticipation
  - **Lag**: Add only after capacity reached

#### 4. Deployment Models

| Model | Description | Best For |
|-------|-------------|----------|
| **Private** | Internal/enterprise cloud on-premise | Sensitive data, large orgs with IT expertise |
| **Public** | Third-party vendor managed | Shared overhead, less confidential data |
| **Hybrid** | Combines both | Mix of sensitive + flexible needs |

#### 5. Service Models (The Big 3)

**SaaS (Software as a Service)**
- **What**: Complete applications delivered via browser
- **Examples**: Salesforce, WebEx, Dropbox, Gmail
- **You manage**: Just your data/configurations
- **Benefits**: Instant access, auto-updates, any device
- **Analogy**: Taking the bus

**PaaS (Platform as a Service)**
- **What**: Development platform + runtime environment
- **Examples**: AWS, Microsoft Azure, Google App Engine
- **You manage**: Your applications
- **Includes**: Solution stacks (OS + middleware + database + dev tools)
- **Analogy**: Taking a taxi

**IaaS (Infrastructure as a Service)**
- **What**: Virtual hardware/infrastructure
- **Examples**: AWS, Google Cloud Platform, RackSpace
- **You manage**: OS, middleware, applications
- **Billing**: Pay-as-you-go (watch costs!)
- **Analogy**: Leasing a car

**Bonus: RaaS (Recovery as a Service)**
- Backup, disaster recovery, business continuity
- Multiple location backups, rapid resumption

#### 6. Key Technologies Enabling Cloud

**Virtualization**
- Commoditizes hardware by sharing resources among users
- **Hypervisor** = software layer emulating hardware (CPU, memory, I/O, networking)
- Originated from mainframe time-sharing
- Enables massive server farms with economies of scale

**SOA (Service-Oriented Architecture)**
- Philosophy: Build **reusable, modular services** that communicate over networks
- **Lego block analogy**: Interoperable, composable, reusable, robust
- **Granularity** = level of service detail (small blocks = flexible but complex)
- Services communicate via **messages**, not procedure calls
- 7 Principles: Open standards, platform-neutral, location-transparent, peer-to-peer, loosely coupled, interface-based, coarsely grained

#### 7. Historical Evolution
```
1960s → Mainframes (centralized, dedicated)
1970s → Time-shared mainframes (virtual machines, thin clients)
1980s → PCs (desktop power, thick clients)
1990s → Client-Server + Internet/WWW
2005+ → Cloud Computing + Mobile (back to thin clients, shared resources)
```

#### 8. Benefits Summary
- Fast deployment
- Access from anywhere, any device
- Elastic scaling (up/down as needed)
- Cost efficiency for small/temp projects
- Expert infrastructure without in-house staff
- Pay-only-for-what-you-use billing

#### 9. Disadvantages to Watch
- Network dependency (no internet = no access)
- Security complexity (access control, data protection)
- Costs can accumulate (pay-as-you-go adds up)
- Vulnerability to attacks (online target)
- Loss of control (third-party governance)
- Technical problem dependency on vendor

#### Key Takeaways for CCF501

1. **Cost and capacity** are the two core business drivers for cloud adoption — directly relevant to Activity 3 (TCO exercise)
2. **Three service models** (SaaS/PaaS/IaaS) represent increasing levels of control vs. responsibility — key framework for Assessment 1
3. **SOA + Virtualisation** are the foundational enabling technologies — Manvi & Shyam (Task 5) expands on virtualisation in depth

---

### 2. Nishimura, H. (2022). Introduction to AWS for Non-Engineers: 1 Cloud Concepts

**Citation:** Nishimura, H. (2022, August 30). Introduction to AWS for non-engineers: 1 cloud concepts [Video]. LinkedIn Learning. Retrieved from https://www.linkedin.com/learning/introduction-to-aws-for-non-engineers-1-cloud-concepts-2/what-is-the-cloud

**Purpose:** Five short videos (~12 min total) introducing cloud computing through the lens of AWS — aimed at non-technical audiences. Covers what the cloud is, how cloud computing works, a brief history, and daily-life examples.

---

#### 1. What is the Cloud?

- The "cloud" = a network of remote servers hosted on the Internet that store, manage, and process data — instead of a local server or personal computer
- **Key distinction**: local computing (your hardware) vs. cloud computing (someone else's hardware, accessed via Internet)
- You already use the cloud daily: email, streaming, social media, file storage (Google Drive, iCloud)

#### 2. What is Cloud Computing?

- Cloud computing = on-demand delivery of IT resources over the Internet with pay-as-you-go pricing
- Instead of buying, owning, and maintaining physical data centres and servers, you rent access from a cloud provider (e.g., AWS, Azure, GCP)
- **Three service models** (same as McHaney): IaaS, PaaS, SaaS — Nishimura uses AWS-specific examples (EC2 for IaaS, Elastic Beanstalk for PaaS)
- **Three deployment models**: Public, Private, Hybrid — consistent with McHaney's definitions

#### 3. A Brief History of the Cloud

- **1960s**: John McCarthy proposes computing as a public utility (time-sharing on mainframes)
- **1990s**: Telecoms begin offering virtualised private network connections (VPNs) — early "cloud" concept
- **1999**: Salesforce launches as one of the first SaaS companies
- **2002–2006**: AWS launches (S3 for storage, EC2 for compute) — makes cloud accessible to startups and enterprises alike
- **2010s**: Cloud becomes mainstream; Google Cloud, Microsoft Azure expand; containers (Docker) and serverless emerge

#### 4. Cloud Computing in Daily Life

- **Streaming**: Netflix, Spotify — content delivered from cloud servers, no local storage needed
- **Email & productivity**: Gmail, Office 365 — SaaS applications accessed via browser
- **Social media**: Facebook, Instagram — massive cloud infrastructure handles billions of users
- **Smart home / IoT**: Alexa, Google Home — voice commands processed in the cloud, responses sent back
- **Business**: Startups can launch globally without buying any hardware — AWS provides instant infrastructure

#### 5. Connection to McHaney (2021)

- Nishimura reinforces McHaney's service/deployment models with AWS-specific examples
- Both emphasise the **historical evolution** from mainframes → time-sharing → PCs → cloud
- Nishimura adds the **daily-life perspective** that makes cloud concepts tangible for non-engineers

#### Key Takeaways for CCF501

1. Cloud computing is already part of daily life — the shift is not just technical, it's cultural and economic
2. AWS pioneered making cloud infrastructure affordable and accessible — directly relevant to Activity 2 (traditional IT problems → cloud alternatives)
3. The history reinforces McHaney's evolution timeline, adding the AWS/Salesforce milestones that shaped the modern cloud market

---

### 3. Eliaçık, E. (2022). The Good, Bad, and Ugly Sides of Cloud Computing

**Citation:** Eliaçık, E. (2022). The good, bad, and ugly sides of the cloud computing (2022). Dataconomy. Retrieved from https://dataconomy.com/2022/05/pros-and-cons-of-cloud-computing-2022/

**Purpose:** Practical overview of cloud computing trade-offs for businesses — structured as pros ("the good"), cons ("the bad"), and hidden risks ("the ugly"), with a focus on cost savings, security, and operational considerations.

---

#### 1. What is Cloud Computing? (Article Context)

- Cloud = virtual computing environments sharing a network of remotely accessible servers
- Concept dates back to 1960s (John McCarthy — computing as a utility like electricity/water)
- Today, 77% of organisations have at least one application or part of their infrastructure in the cloud

#### 2. Pros of Cloud Computing

| Advantage | Detail |
|-----------|--------|
| **Cost-efficient** | No upfront server costs, no IT staff for maintenance; infrastructure shared across provider's customers. Orgs save >35% on operating expenses (Global Cloud Services Market research) |
| **Unlimited storage** | Purchase as much as you need; far cheaper than buying new hardware/software regularly |
| **Backup & recovery** | Data stored in cloud is simpler to back up and restore than on physical devices; most providers handle disaster recovery |
| **No admin hassles** | Provider handles hardware procurement, installation, maintenance, and software updates automatically |
| **Endless scalability** | Scale RAM, CPU, and disk on demand without over-provisioning; IaaS protects against outages from traffic spikes |
| **HW/SW optimisation** | SaaS model means enterprise plans for group usage, no per-person licensing; no need for local server purchases |
| **Security** | Cloud host's full-time job is monitoring security — more efficient than in-house teams splitting attention across IT issues. Offsite storage also reduces risk from internal data breaches |
| **Environmentally friendly** | No physical servers on-premise = reduced energy consumption and carbon footprint |
| **Speed** | Cloud backup can rival or exceed on-site speeds with multiple servers working in parallel |
| **Work flexibility** | Work from anywhere with an internet connection; access data regardless of location or country |
| **Automation** | Cloud services automate routine backups, freeing IT staff for core business tasks |
| **Space savings** | No server rooms, dedicated breakers, HVAC systems, or backup generators needed |
| **Data control** | Centralised data from multiple offices/projects in one location; complete control without visiting physical sites |
| **Reliability** | Shared, redundant infrastructure improves application availability and service uptime |

#### 3. Cons of Cloud Computing

| Disadvantage | Detail |
|-------------|--------|
| **Hidden costs** | While some areas save money, making the shift itself can be expensive; need a solid migration strategy to categorise what moves to cloud vs. stays on-premise |
| **Technical issues / downtime** | Technology is prone to outages and malfunctions; even the best providers experience downtime |
| **Security & privacy risks** | Entrusting sensitive data to a third party means you may not detect breaches immediately; a significant concern for healthcare, finance, and publicly traded companies |
| **Vendor lock-in / lack of control** | Inflexible contracts; restricted access to system components; difficult and lengthy migration to another provider; less control over backend operations can expose data |
| **Internet dependency** | Even 99.99% availability isn't 100%; natural disasters, construction, regional outages, and data centre hacks can all interrupt service |
| **DoS vulnerability** | Users have little control over denial-of-service attacks targeting their cloud provider; underscores the need for personal data backups |
| **Bandwidth limits** | Some providers cap bandwidth; exceeding limits incurs extra charges |

#### 4. The "Ugly" — Compliance & Hidden Complexity

- Industries with strict regulations (healthcare, finance, government) face additional compliance complexity when moving to cloud
- The article stresses that **cloud is not automatically cheaper** — a thorough TCO analysis is required before migration

#### Key Takeaways for CCF501

1. The >35% operating expense savings stat is useful evidence for Activity 3 (TCO exercise) — but must be weighed against migration costs and hidden charges
2. The pros/cons framework directly mirrors McHaney's benefits/disadvantages, but adds practical nuance (vendor lock-in, compliance, bandwidth)
3. For Assessment 1: cloud adoption is not binary — it requires a strategic cost–benefit analysis balancing flexibility, security, and control

---

### 4. Accenture Technology. (2020). Why Cloud Matters

**Citation:** Accenture Technology. (2020, June 5). Why cloud matters [Video]. YouTube. Retrieved from https://www.youtube.com/watch?v=p1Nr03gtkyU&t

**Purpose:** Short explainer video on the four key business benefits of cloud computing — speed, innovation, scale, and cost savings — aimed at business decision-makers considering cloud migration.

---

#### 1. It's Fast

- Cloud offers flexibility to quickly adjust computing resources while paying only for what you use
- Lower cost and time to develop/deploy new applications → faster speed to market

#### 2. It Enables Innovation

- Affordable, unrestricted access to cutting-edge technologies and capabilities
- Reduces barriers to entry — gives businesses capabilities that would normally be out of reach

#### 3. You Choose the Scale

- Scale up or down as needed
- Provides tools for global business — data and apps accessible to people around the world

#### 4. It'll Save You Money

- Building proprietary IT infrastructure and staffing it is incredibly expensive and may not be fully utilised
- With an optimised cloud environment, companies can focus on core business and pay only for resources used

#### Key Takeaways for CCF501

1. The four benefits (speed, innovation, scale, cost) map directly to McHaney's benefits summary — useful as a concise "elevator pitch" for cloud adoption
2. The innovation point is key for Assessment 1: cloud levels the playing field for smaller businesses
3. Complements Eliaçık's more nuanced view — Accenture presents the optimistic case; Eliaçık adds the caveats

---

### 5. Manvi, S., & Shyam, G. K. (2021). Cloud Computing: Concepts and Technologies — Chapter 4 (Virtualisation)

**Citation:** Manvi, S., & Shyam, G. K. (2021). Cloud computing: Concepts and technologies. CRC Press. Retrieved from https://learning-oreilly-com.torrens.idm.oclc.org/library/view/cloud-computing/9781000338058/xhtml/04chap_04.xhtml#sec4_1

**Purpose:** Technical overview of virtualisation technology — the foundational enabler of cloud computing. Covers definitions, architecture, characteristics that make virtualisation ideal for cloud, and pros/cons. Focus on Sections 4.1 and 4.4.

---

#### 1. What is Virtualisation?

- **Virtualisation** = abstraction of computer resources; hides the physical characteristics of computing resources from users/applications
- Term coined in the 1960s from the IBM M44/44X experimental system ("virtual machine" / "pseudo machine")
- Platform virtualisation is performed by host software (a **control program**) which creates a simulated computer environment — a **VM** — for its guest software
- Guest software executes as if running directly on physical hardware

#### 2. Key Terms

| Term | Definition |
|------|-----------|
| **Virtualisation** | Abstraction of computer resources; hides physical characteristics from users |
| **Hypervisor / VMM** | Software that creates and runs VMs; allows one host to support multiple guest VMs by sharing resources (memory, CPU) |
| **Emulation** | Using a program/device to imitate the behaviour of another program/device |
| **Containers** | Lightweight virtual environments (OS virtualisation) that group and isolate processes and resources from the host |
| **OS Virtualisation** | A server is split into containers under one OS, each handling an application |
| **Hardware Virtualisation** | Multiple copies of the same or different OS run on one computer; VMs are isolated from each other |
| **Network/Storage Virtualisation** | Multiple devices consolidated into a logical view managed from a single console |

#### 3. Virtualisation Architecture

```
┌─────────────────────────┐
│   Guest Operating System │  ← Runs applications; invokes VM instances
├─────────────────────────┤
│       Hypervisor         │  ← Creates VMs; manages resource allocation
├─────────────────────────┤
│   Host Operating System  │  ← Supports both layers above
└─────────────────────────┘
```

- The VM is a software computer that runs an OS and applications just like a physical computer
- The hypervisor serves as the platform for running VMs and consolidating resources

#### 4. Characteristics of Virtualisation in Cloud

| Characteristic | Description |
|---------------|-------------|
| **Partitioning** | Many applications and OSes supported on a single physical system by partitioning resources |
| **Isolation** | Each VM is isolated; if one crashes, others are unaffected; data is not shared between containers |
| **Encapsulation** | A VM can be represented as a single file; protects applications from interfering with each other |
| **Consolidation** | Multiple OS can run on the same server; eliminates need for dedicated hardware per application |
| **Development flexibility** | Developers can run/test apps in heterogeneous OS environments on one virtualised machine |
| **Migration & cloning** | VMs can be moved between sites to balance workload or recover from hardware failure; cloned VMs deploy easily |
| **Stability & security** | Host OS hosts multiple isolated guest OSes; VMs don't interfere with each other, improving security |

#### 5. Pros and Cons of Virtualisation (Section 4.4)

| Pros | Cons |
|------|------|
| **Cheaper** — no physical hardware needed; buy licence or access from provider | **High implementation cost** — for providers, setting up virtualisation infrastructure is expensive |
| **Predictable costs** — third-party providers offer subscription pricing | **Security risk** — data is a target; frequent attacks on virtualised assets |
| **Reduced workload** — providers handle hardware/software updates automatically | **Availability concerns** — if you can't connect, you can't access your data |
| **Better uptime** — providers offer 99.99%+ availability | **Scalability limits** — may not scale exactly as needed when starting out |
| **Faster deployment** — no physical machines to set up, no local networks to create | **Chain dependency** — multiple links must work together; loss of full local control |
| **Digital entrepreneurship** — anyone can start a business with virtualised infrastructure | **Time cost** — saves time in implementation but can cost time in long-run management |
| **Energy savings** — no local hardware = lower energy consumption, improved ROI | **Application limitations** — not every app/server works in a virtualised environment; may need hybrid systems |

#### Key Takeaways for CCF501

1. **Virtualisation is the foundational enabling technology** for all cloud service models (SaaS/PaaS/IaaS) — without it, cloud computing as we know it wouldn't exist
2. The characteristics (partitioning, isolation, encapsulation, consolidation) explain *how* cloud providers can serve millions of customers on shared physical infrastructure
3. The pros/cons complement Eliaçık's cloud-level analysis — virtualisation trade-offs cascade up to cloud trade-offs (e.g., vendor availability → cloud downtime)
4. For Activity 3 (TCO): virtualisation's cost predictability and reduced workload are key TCO advantages, but implementation costs and chain dependencies are TCO risks