# Module 3 — Cloud Computing Deployment Models

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| R1 | Linthicum (2021) — LinkedIn Learning video (public/private/hybrid) | 🔥 WIP — needs manual watch (auth required) |
| R2 | Manvi & Shyam (2021) — Ch.1.3 Deployment Models + Ch.1.5 Platforms & Technologies | ✅ Read + Reviewed |
| R3 | IBM — What is a Public Cloud? | ✅ Read + Reviewed |
| R3 | IBM — What is Private Cloud? | ✅ Read + Reviewed |
| R3 | IBM — What is Hybrid Cloud? | ✅ Read + Reviewed |
| R4 | Chandrasekaran (2015) — Review questions (Ch.22, Q1/5/6/8/9) | 🔥 WIP — O'Reilly + ProQuest auth required |
| R5 | IBM — What is a Virtual Private Cloud (VPC)? | ✅ Read + Reviewed |
| A1 | Deployment Model Case Study — Discussion Forum | 🕐 Not started |
| A2 | Case Study: Optimising Cloud Costs — Discussion Forum | 🕐 Not started |

---

## Key Highlights

---

### Resource 2 — Manvi, S. & Shyam, G. K. (2021). Cloud Computing: Concepts and Technologies. CRC Press. (Ch.1.3 + Ch.1.5)

#### 1. The Four Deployment Models

Cloud deployment models represent the **category of Cloud environment**, distinguished by proprietorship, size, and access. They describe the purpose and nature of the cloud.

| Model | Definition | Key Trait |
|-------|-----------|-----------|
| **Public Cloud** | Services delivered over a network open for public usage | Multi-tenant; provider manages infrastructure |
| **Private Cloud** | Deployed in a secure environment behind a firewall, governed by the organisation's IT department | Single-tenant; greater control over data |
| **Hybrid Cloud** | Arrangement of two or more Cloud servers (private, public, or community) that are bound together but remain individual entities | Best-of-both-worlds flexibility |
| **Community Cloud** | Mutually shared between organisations from the same community (e.g., banks, trading firms) | Multi-tenant; sector-specific shared concerns |

#### 2. Characteristics of Each Model (Manvi & Shyam)

- **Public:** True representation of cloud hosting; provider renders services and infrastructure to various clients
- **Private:** Only authorised users access it; organisation has direct control over data
- **Hybrid:** Integrated cloud; can scale across environments as needed
- **Community:** Groups with similar computing concerns share the setup (e.g., compliance requirements)

#### 3. Cloud Computing Platforms (Ch.1.5)

Choosing the wrong cloud platform can negatively impact everyone involved — consider **short and long-term issues**. Key architectures:
- Amazon EC2, IBM Blue Cloud, Microsoft Azure, Sun Cloud, Salesforce Force.com, Google AppEngine

**Cloud Management Platform (CMP) options:**

| Platform | Type | Key Note |
|----------|------|----------|
| Apache CloudStack | Open-source | "Turnkey" IaaS; AWS API compatibility |
| Eucalyptus | Open-source | Strong AWS ties; enables private → hybrid cloud burst |
| Microsoft Hyper-V + System Center | Commercial | Windows Server + Azure integration |
| OpenStack | Open-source | Co-founded by Rackspace + NASA (2010); Apache 2.0 license |
| VMware vCloud Director | Commercial | Secure, multitenant cloud via vSphere environments |

**Choosing the right CMP depends on:** virtualization environment, scope of cloud strategy, business requirements, available skills, and budget.

#### 4. Cloud Computing Challenges (Ch.1.5)

| Challenge | Insight |
|-----------|---------|
| **Security** | 90% of security professionals concerned (Crowd Research Partners, 2018); top fears: data loss/leakage (67%), data privacy (61%), confidentiality breaches (53%) |
| **Lack of resources** | Skills gap; addressed via training or cloud-certified hires |
| **Governance** | 71% cite it as a challenge (RightScale); best practices and policy enforcement help |
| **Compliance** | 68% cite it as top challenge (RightScale); GDPR has amplified this |
| **Multi-cloud** | 81% of enterprises pursue multi-cloud; 51% hybrid strategy |
| **Vendor lock-in** | AWS, Azure, GCP, IBM dominate public cloud market |
| **Integration** | Legacy systems + cloud-based apps require time, skill, and resources |

#### Key Takeaways for CCF501

- The **four deployment models** (Public, Private, Hybrid, Community) differ primarily in who controls the infrastructure and who can access it
- Platform choice is an **architectural decision** — wrong choices propagate long-term costs
- Open-source CMPs (OpenStack, CloudStack) offer portability; commercial options offer off-the-shelf ease
- Cloud challenges (security, governance, compliance, lock-in) remain relevant for practitioners — these appear in exams and assessments

---

### Resource 3 — IBM Cloud Education: Public / Private / Hybrid Cloud

#### 1. Public Cloud (IBM)

> "A public cloud is a type of cloud computing in which a third-party service provider makes computing resources available to users over the public internet." — IBM

**Key characteristics:**
- Provider owns and manages **all hardware and infrastructure**
- Multi-tenant environment — workloads from multiple tenants may share physical servers, but data is **logically isolated**
- Pricing models: free tier, subscription-based, or **pay-per-usage**
- Global market predicted to exceed **USD 330 billion** by end of 2022 (Gartner)

**Public cloud services (service models):**

| Model | Description |
|-------|-------------|
| **IaaS** | On-demand compute, network, storage — often virtualised |
| **PaaS** | Complete development platform (hardware + software + infrastructure) managed by provider |
| **SaaS** | Cloud-hosted software accessed via browser or API |
| **BPaaS** | Entire business process delivered as a combination of IaaS/PaaS/SaaS |
| **FaaS** | Code runs only in response to specific events (serverless subset) |

**When to choose public cloud:**
- Scalability and elasticity are priorities
- You want to avoid upfront CapEx and prefer predictable OpEx
- Workloads don't have strict security or regulatory requirements

**Security in public cloud:**
- 52% of companies report **better security in the cloud** than on-premises (McAfee)
- Gartner predicted IaaS cloud workloads would experience **60% fewer security incidents** than traditional data centres
- Requires strong access management, encryption (at rest, in transit, in use), and continuous monitoring

#### 2. Private Cloud (IBM)

> "Private cloud is a cloud computing environment in which all hardware and software resources are dedicated exclusively to (and accessible only by) a single organisation." — IBM

Also called **internal cloud** or **corporate cloud**.

**Key characteristics:**
- **Single-tenant** environment — isolated access
- Combines cloud benefits (elasticity, scalability, service delivery) with on-premises control (access control, security, customisation)
- Global private cloud services market expected to rise from **USD 124.6 billion (2025)** to **USD 618.3 billion by 2035** (Future Markets Insights)

**Private cloud architecture (three core technologies):**

| Technology | Role |
|-----------|------|
| **Virtualisation** | Abstracts IT resources from physical hardware; enables efficient sharing |
| **Cloud management software** | Centralised control over infrastructure and apps; optimises security, availability, resource use |
| **Automation** | Speeds provisioning, integration and deployment; enables self-service delivery |

**Benefits of private cloud:**

| Benefit | Detail |
|---------|--------|
| Control | Full hardware and software choice |
| Customisation | Tailor servers and software with add-ons or custom dev |
| Greater visibility | All workloads behind firewall; clear security and access oversight |
| Enhanced security | Firewalls, VPNs, encryption, API keys — required by government, law enforcement |
| Regulatory compliance | Not dependent on provider compliance; tailor to sector-specific regulations (insurance, finance) |

**Disadvantages:** High cost (hardware, software, staffing); limited flexibility after investment.

**Four types of private cloud:**

| Type | Description |
|------|-------------|
| **On-premises private cloud** | Organisation manages everything; highest CapEx + OpEx |
| **Virtual private cloud (VPC)** | Private cloud-like environment on public cloud infrastructure |
| **Hosted private cloud** | CSP owns and manages assets; bare-metal servers off-premises |
| **Managed private cloud** | Single-tenant; management outsourced to third-party provider |

#### 3. Hybrid Cloud (IBM)

> "Hybrid cloud combines and unifies public cloud, private cloud and on-premises infrastructure to create a single, flexible, cost-optimal IT infrastructure." — IBM

**Core advantage: Agility** — rapidly provision resources to respond to change and capture growth opportunities.

Global hybrid cloud market: **USD 125 billion (2023)** → projected **USD 558.6 billion by 2032** (IMARC Group).

**Critical components:**

| Component | Role |
|-----------|------|
| **Network connectivity** | WAN, VPN, APIs connecting environments |
| **Virtualisation** | Divides physical hardware into multiple VMs; enables flexibility |
| **Containerisation** | Packages code + OS libraries into portable containers that run consistently across infrastructure |
| **Hybrid cloud management platform** | Unified platform to discover, operate and manage resources across all environments |

**Evolution of hybrid cloud:**
- **Traditional:** Converted on-premises data centres to private cloud + connected to public cloud via middleware and management tools
- **Modern:** Focus on workload portability + automation; microservices + containers = cloud-native; private clouds now hosted off-prem via VPNs/VPCs

**Hybrid multicloud benefits (IBM IBV report):**
- Value derived from hybrid multicloud platform = **2.5× the value** of a single platform/vendor approach
- Benefits: improved developer productivity, greater infrastructure efficiency, improved regulatory compliance and security, overall business acceleration

**77% of business and IT professionals** have adopted a hybrid cloud approach (IBM Transformation Index: State of Cloud, 2022).

**4 steps to a hybrid cloud management strategy:**
1. Define policies, roles and responsibilities across the ecosystem
2. Identify workloads and decide where to locate them
3. Review cloud service level agreements (SLAs) — uptime, latency, data availability
4. Establish a **zero-trust approach** to security

**Key use cases:**
- Security and regulatory compliance (keep sensitive data on private; non-sensitive on public)
- Scalability and resilience ("cloud bursting" — scale on public without impacting private)
- Rapid adoption of new technology (AI, SaaS) without new on-prem infrastructure
- Cloud migration (lift-and-shift to public cloud)
- Resource optimisation and cost savings (predictable workloads on private; variable on public)
- Backup and disaster recovery (BDR)

#### Key Takeaways for CCF501

- **Public cloud = multi-tenant utility model** — shared infrastructure, provider-managed, pay-per-use
- **Private cloud = single-tenant, control-first** — higher cost, greater security and compliance flexibility
- **Hybrid cloud = best of both** — agility + control; the dominant enterprise strategy (~77% adoption)
- VPC is a form of private cloud hosted on public infrastructure — bridges the public/private gap
- The **cost vs. control trade-off** is central to deployment model selection

---

### Resource 5 — IBM. (n.d.). What is a Virtual Private Cloud (VPC)?

> "A VPC is a public cloud offering that lets an enterprise establish its own private cloud-like computing environment on shared public cloud infrastructure." — IBM

**Analogy:** A cloud provider's infrastructure is an apartment building. Being a public cloud tenant = sharing an apartment with roommates. Having a VPC = having your own private condominium — you hold the key, you decide who enters.

**VPC market size:** USD 38.8 billion (2022) → projected **USD 129.6 billion by 2032** (Future Market Insights).

#### 1. How VPC Achieves Logical Isolation

VPCs use **virtual network functions and security features** to give customers granular control over which IP addresses or cloud applications can access resources. This is analogous to "friends-only" privacy controls on social media.

VPC is categorised as **IaaS**. All major cloud providers offer VPC: AWS, Azure, Google Cloud, IBM Cloud, Oracle, VMware.

#### 2. Key Features

| Feature | Description |
|---------|-------------|
| **Agility** | Control virtual network size; scale cloud resources dynamically in real time |
| **Availability** | Redundant resources + fault-tolerant availability zone architectures |
| **Security** | Logically isolated network; complete control over resource access |
| **Affordability** | Leverages public cloud cost-effectiveness (lower hardware costs, reduced labour) |

#### 3. VPC vs. Related Concepts

| Concept | Relationship to VPC |
|---------|---------------------|
| **VPN (Virtual Private Network)** | Encrypts public internet connections; can be deployed as VPNaaS inside a VPC to connect subnets across multiple VPCs |
| **Private cloud** | Single-tenant, owned/operated by enterprise (usually on-prem); VPC is multi-tenant with logical isolation — not the same thing |
| **Public cloud** | Multi-tenant, no isolation; VPC adds a private isolated layer within public cloud infrastructure |

#### 4. VPC Architecture

Three categories of cloud resources deployed in a VPC:

| Category | Details |
|----------|---------|
| **Compute** | Virtual Server Instances (VSIs) — vCPUs with memory |
| **Storage** | Block storage quota per account; purchase more as needed |
| **Networking** | Public gateways, load balancers, routers, direct/dedicated links |

**Other key terms:**
- **Regions:** Geographical locations where services are deployed
- **Availability zones:** Logically/physically isolated within a region; independent power, cooling, networking (no shared single point of failure)
- **Subnets:** Logical IP partitions within a VPC; private IP addresses not publicly accessible
- **Route tables:** Rules controlling network traffic per subnet/gateway
- **Flow logs:** Capture IP traffic to/from network interfaces
- **DNS services:** Private DNS zones for improved security and privacy

#### 5. Three-Tier Architecture in a VPC

Most software applications use a three-tier architecture:

```
[Presentation Tier]  ←→  [Application Tier]  ←→  [Database Tier]
    Web browser              Business logic          Data storage
    or GUI                   (most processing)
```

In a VPC, each tier gets its own **subnet** (own IP address range) and **unique ACL (Access Control List)**.

Communication always goes through the **application tier** — presentation and data tiers cannot communicate directly.

#### 6. VPC Security

Two types of network access controls:

| Control | Description |
|---------|-------------|
| **Access Control Lists (ACLs)** | Rules limiting who can access a specific subnet; defined by IP addresses or applications |
| **Security Groups** | Virtual firewalls for groups of resources across multiple subnets; assign uniform access rules |

#### 7. VPC Use Cases

- **Web hosting:** Control network traffic reaching VPC resources from the internet
- **Cloud migration:** Move sensitive on-prem assets to isolated private cloud within public cloud
- **Hybrid cloud strategy:** Connect VPCs to public cloud or on-prem infrastructure via VPN
- **Multicloud deployment:** Connect VPCs across cloud providers
- **DevOps practices:** Cloud-native tools accelerate software development lifecycle
- **High-performance computing (HPC):** Fast-provisioning compute + secure networking for finance/healthcare
- **Regulatory compliance:** Built-in encryption, data residency controls, compliance tools
- **BCDR:** Replicate VPC infrastructure across regions for disaster recovery
- **Edge computing/IoT:** Secure, scalable cloud environments for IoT device connectivity

#### Key Takeaways for CCF501

- A **VPC ≠ private cloud** — it's a public cloud offering with logical isolation; more affordable and easier to manage than a true private cloud
- VPC bridges the **public/private trade-off**: public cloud economics + private cloud security
- Three core VPC networking components: subnets, route tables, security groups/ACLs
- Three-tier architecture (presentation → application → database) maps naturally to VPC subnet isolation
- All major CSPs offer VPC — it's an industry-standard IaaS pattern

---

### Activity 2 Reference — Cheema et al. (2019). IT@Intel Brief: A Holistic Cloud Approach for Big Savings. Intel.

> Note: Do not use this resource in Assessment 1.

#### 1. Business Challenges Associated with Higher Cloud Costs

- **Shadow IT risk:** When business units bypass centralised IT to engage cloud providers directly, it creates governance gaps and "common challenges and lack best-known methods" for cost management
- Without deliberate planning, organisations struggle with cost control, governance, and optimisation across cloud environments
- Decentralised cloud adoption leads to duplication, inconsistent security policies, and unmanaged spend

#### 2. Cost Reduction Strategies Adopted by Intel

| Strategy | Description |
|----------|-------------|
| **Centralised management** | Unified oversight of all cloud accounts, applications, and workloads across the organisation |
| **Planned cost reduction** | A structured, proactive approach rather than reactive spending controls |
| **Cloud-broker strategy** | Internal guidance directing business groups toward optimal cloud solutions based on workload fit |

#### 3. Key Result

- **~USD 940,000 in savings** achieved by Intel IT in 2016 through this comprehensive multi-cloud strategy

#### 4. Strategic Foundation

Intel's approach reflects a broader "data center transformation strategy" focused on **workload optimisation** — ensuring "the right workload in the right place" across infrastructure options (on-premises and cloud).

#### Key Takeaways for CCF501

- Cost optimisation requires **governance and centralisation**, not just technical choices
- Shadow IT is a concrete, measurable business risk in cloud deployments
- A cloud-broker model (internal advisory function) can drive significant savings at scale
- Intel's case demonstrates that hybrid + multi-cloud strategies need intentional management to deliver ROI
