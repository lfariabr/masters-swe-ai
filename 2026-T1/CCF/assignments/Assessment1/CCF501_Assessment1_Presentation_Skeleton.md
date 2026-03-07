# Cloud Computing for ABC Enterprise — Key Contributions to Business Automation
*CCF501 Cloud Computing Fundamentals — Assessment 1 Presentation Skeleton*
*Luis G. B. A. Faria — A00187785 | Prof. Dr. Divya Leekha | March 2026*

> **Timing guide:** 11 slides × ~30–35s = ~5.5–6.5 min total

---

## Slide 1 — Title

**Content:**
- **Cloud Computing for ABC Enterprise — Key Contributions to Business Automation**
- Luis G. B. A. Faria — ID A00187785
- Subject: CCF501 Cloud Computing Fundamentals
- Prof. Dr. Divya Leekha | March 2026

**Speaker note:**
> "Today I'll walk you through how cloud computing transformed ABC Enterprise — slashing IT costs by 80%, absorbing a 10x customer surge, and turning manual operations into automated, policy-driven systems. Here's how."

**Visual:** Existing building/sky photo background — no new image prompt needed. *(~15s)*

---

## Slide 2 — What Is Cloud Computing?

**Content:**
- "On-demand delivery of compute, storage and services over the internet" (Mell & Grance, 2011; Naved et al., 2022)
- **5 NIST characteristics:** On-Demand Self-Service · Broad Network Access · Resource Pooling · Rapid Elasticity · Measured Service
- Key shift: from **owning capacity** → **renting capability**

**Speaker note:**
> "Cloud is not just hosting — it's a fundamentally different operating model with deep historical roots: from 1960s mainframes to 1970s virtualisation, 1999 Salesforce, and 2006 AWS (Naved et al., 2022). NIST defines five essential characteristics. For ABC, rapid elasticity and measured service are the ones that directly explain the 80% cost cut and the 10x surge absorption."

**Visual — 🍌 Nano Banana #5: NIST Wheel Diagram**
> Create a professional circular infographic diagram in Lucidchart flowchart style, white background. A central circle labelled "Cloud Computing (NIST, 2011)" in dark navy. Five rounded rectangles arranged radially around it, connected by lines. Labels: "On-Demand Self-Service", "Broad Network Access", "Resource Pooling", "Rapid Elasticity", "Measured Service". Each box in a different shade: blue, teal, orange, green, purple. Use clean sans-serif font. Title above diagram: "5 Essential Characteristics of Cloud Computing". Output as image.

*(~35s)*

---

## Slide 3 — Benefit 1: Cost Efficiency

**Content:**
- ~80% reduction in start-up IT costs (Eliaçık, 2022)
- **CAPEX → OPEX:** no upfront servers, no idle hardware
- Pay only for compute-hours + GB-months consumed (Mell & Grance, 2011)
- "Operational overhead — personnel, training, upgrades — often exceeds hardware cost" (McHaney, 2021)

**Speaker note:**
> "Traditional IT requires buying capacity upfront — you overprovision to be safe. Cloud flips this: ABC paid only for what it consumed, measured to the hour. That single shift cut start-up IT costs by 80%."

**Visual — 🍌 Nano Banana #6: CAPEX vs OPEX Two-Column**
> Create a professional comparison diagram in Lucidchart flowchart style, white background. Two columns side by side. Left column header "Traditional IT (CAPEX)" in dark red, right column header "Cloud — ABC (OPEX)" in dark green. Left column boxes (stacked, red fill): "Large upfront hardware purchase", "Idle capacity during low demand", "Full ops team required", "Fixed costs regardless of usage". Right column boxes (stacked, green fill): "No upfront servers", "Pay per compute-hour + GB-month", "Provider manages infrastructure", "~80% reduction in start-up IT costs". A large downward arrow between the two columns labelled "Cost Shift". Use clean sans-serif font. Title: "Traditional IT vs Cloud: Cost Model". Output as image.

*(~35s)*

---

## Slide 4 — Benefits 2 & 3: Scale Without Limits + Less Overhead

**Content:**
- **Rapid Elasticity:** 10x customer surge in one month — absorbed automatically, no procurement delay (McHaney, 2021)
  - Auto Scaling provisions/terminates instances based on demand signals
- **Resource Pooling:** Providers consolidate workloads — ABC borrows enterprise-grade resilience (Manvi & Shyam, 2021)
- More customers ≠ more headcount — the linear relationship is broken

**Speaker note:**
> "In traditional IT, a 10x surge would mean a procurement cycle — hardware arrives after the opportunity passes. Traditional IT locks teams into a *lead strategy*: procure capacity ahead of demand to avoid shortfalls (McHaney, 2021). Cloud enables a *lag strategy* instead — resources provision only as demand arrives, eliminating idle capital spend. With cloud auto-scaling, ABC's capacity became a policy, not a purchase order. And through resource pooling, ABC gets enterprise-grade infrastructure it couldn't afford to build alone."

**Visual — 🍌 Nano Banana #7: 10x Surge Growth Chart**
> Create a professional bar chart diagram in Lucidchart flowchart style, white background. X-axis: "Month 0" and "Month 1". Two grouped bars per month. Bar 1 (dark blue): "Infrastructure Capacity". Bar 2 (orange): "Customer Demand". At Month 0, both bars equal height. At Month 1, Customer Demand bar is 10x taller while Infrastructure Capacity bar auto-matches it with a dashed "Auto Scaled" line at the top. Add annotation arrow pointing to Month 1: "10x surge — no manual intervention". Title: "Rapid Elasticity: ABC's 10x Growth Absorbed by Auto Scaling". Output as image.

*(~35s)*

---

## Slide 5 — Challenges + Mitigation

**Content (two-column layout):**

| Challenge | Mitigation |
|-----------|------------|
| **Security & PII** — payments + customer data exposed to third party (Eliaçık, 2022) | Least-privilege IAM, MFA, encryption at rest/in transit, shared responsibility model |
| **Cost Volatility** — pay-as-you-go can spiral without guardrails (Bittok, 2022) | FinOps: budget alerts, resource tagging, rightsizing, reserved pricing |
| **Vendor Lock-in + Skills Gap** — migration cost + mindset shift (McHaney, 2021) | Portability-first (containers, standard DBs), targeted cloud upskilling |

**Speaker note:**
> "Cloud adoption is not risk-free. Three challenges dominate for ABC — and industry data makes them concrete: 90% of security professionals cite security as their top concern, with governance (71%) and compliance (68%) close behind (Manvi & Shyam, 2021). The good news: each has a direct mitigation. Security follows a shared responsibility model — the provider secures the infrastructure, ABC secures what it deploys on top (Shore, 2020)."

**Visual — 🍌 Nano Banana #8: Challenge vs Mitigation Table**
> Create a professional two-column comparison table diagram in Lucidchart flowchart style, white background. Three rows. Left column header "Challenge" in dark red, right column header "Mitigation" in dark green. Row 1: "Security & Privacy — PII + payment data" | "IAM least-privilege, MFA, encryption, shared responsibility model". Row 2: "Cost Volatility — pay-as-you-go sprawl" | "FinOps: budget alerts, tagging, rightsizing, reserved pricing". Row 3: "Vendor Lock-in + Skills Gap" | "Containers + standard DBs for portability; cloud upskilling programme". Alternating row backgrounds (white / light grey). Title: "Cloud Challenges and Mitigations for ABC Enterprise". Output as image.

*(~40s)*

---

## Slide 6 — Recommended Models

**Content:**
- **Service model:** IaaS + PaaS blend — IaaS for compute flexibility, PaaS for managed DB, load balancing, serverless
- **Deployment model:** Public cloud — scalability, global availability, built-in automation (Mell & Grance, 2011)
  - Private: ❌ over-engineered for a start-up
  - Hybrid: ⚠️ premature complexity
- **Why public?** ABC is consumer-facing, high-growth, no regulatory mandate for private infrastructure

**Speaker note:**
> "The recommendation is a blended IaaS-PaaS model on public cloud. Public cloud also delivers stronger security outcomes than many expect — IBM (n.d.), citing Gartner, reports IaaS workloads experience 60% fewer security incidents than traditional data centres. Private cloud would give control ABC doesn't need yet at a cost it can't justify. As ABC scales, a Virtual Private Cloud (VPC) — isolated private networking on public cloud infrastructure — is a viable intermediate step without the full overhead of a dedicated private cluster."

**Visual — 🍌 Nano Banana #9: Service + Deployment Model Spectrum**
> Create a professional two-section infographic in Lucidchart flowchart style, white background. Top section header: "Service Model — ABC Recommendation". Three horizontally arranged boxes: "IaaS" (dark blue, labelled "Compute + config flexibility"), "PaaS ✅" (green, labelled "Managed DB, LB, serverless — recommended"), "SaaS" (grey, labelled "Limited customisation"). An arrow under them labelled "Control ← → Managed". Bottom section header: "Deployment Model — ABC Recommendation". Three horizontally arranged boxes: "Private Cloud" (red, labelled "High cost, limited elasticity ❌"), "Hybrid Cloud" (amber, labelled "Premature complexity ⚠️"), "Public Cloud ✅" (green, labelled "Scalable, automated, cost-effective"). Title: "Recommended Cloud Models for ABC Enterprise". Output as image.

*(~35s)*

---

## Slide 7 — Recommended Cost Model

**Content:**
- Three levers: **Pay-as-you-go · Reserved/committed · Spot/preemptible** (Bittok, 2022)
- **Recommendation — Hybrid Cost Model:**
  - **Reserved capacity:** stable tiers (web/app servers, databases)
  - **Pay-as-you-go:** demand spikes via Auto Scaling
  - **Spot instances:** background jobs + analytics pipelines
- "Cloud adoption is about better ROI — less downtime, faster launches, automation" (Bittok, 2022)

**Speaker note:**
> "Cost model is not just about the cheapest bill. ABC needs predictability for stable workloads and flexibility for spikes. Reserved for base, pay-as-you-go for surges, spot for batch jobs. TCO includes not just cloud fees but migration cost, security tooling and engineering effort."

**Visual:** Reuse 🍌 Nano Banana #6 (CAPEX vs OPEX) — or describe a simple 3-tier cost pyramid in speaker notes: Base (Reserved) → Middle (Pay-as-you-go) → Top (Spot). No new prompt needed.

*(~30s)*

---

## Slide 8 — Why AWS?

**Content:**
- Shortlist: Azure (Microsoft-aligned), GCP (analytics-first), **AWS (broadest catalogue)**
- ABC already uses Route 53 — AWS architecture already in place (Nishimura, 2022)
- AWS: deepest automation-ready managed-service catalogue for ABC's workloads

| Provider | Ecosystem | ABC Alignment |
|----------|-----------|---------------|
| **AWS** | Broadest catalogue | ✅ Route 53 already in stack |
| Azure | Microsoft / enterprise | ⚠️ No MS signals |
| GCP | Analytics-first | ❌ No analytics workloads yet |

**Speaker note:**
> "The realistic shortlist is AWS, Azure, or GCP — all cover the technical baseline. The differentiator for ABC is that Route 53 is already in the architecture, and AWS has the deepest automation-ready services for exactly the workflows ABC runs."

**Visual — 🍌 Reuse Nano Banana #4** (provider comparison table — from report plan). No new prompt needed.

*(~35s)*

---

## Slide 9 — AWS in Action: Three Automation Elements

**Content:**
- **ELB (Elastic Load Balancing):** Routes traffic + health-checks across EC2 without operator intervention — critical for delivery + taxi services where latency = churn
- **Auto Scaling:** Provisions/terminates EC2 on demand signals — the 10x surge required zero manual action — capacity is policy, not a purchase order
- **AWS Lambda:** Event-driven — order placed → delivery assigned; payment confirmed → restaurant notified. Zero server management. Scales to zero when idle.

**Speaker note:**
> "Three services — three automation wins for ABC. ELB keeps the app responsive for delivery and taxi users. Auto Scaling means the team sleeps through a 10x surge. Lambda turns ABC's workflows into code — order placed triggers delivery assignment automatically."

**Visual — 🍌 Reuse Nano Banana #1** (AWS architecture diagram — from report plan). No new prompt needed.

*(~45s)*

---

## Slide 10 — Conclusion

**Content:**
- **Recommended stack:** Public cloud · IaaS+PaaS · Hybrid cost model · AWS
- Key outcomes unlocked:
  - 80% cost reduction (measured service)
  - 10x surge absorbed (rapid elasticity)
  - Zero-headcount scaling (resource pooling + Auto Scaling)
  - Workflow automation (Lambda event triggers)
- "ABC's infrastructure stops being a bottleneck and becomes a competitive advantage" (Eliaçık, 2022)

**Speaker note:**
> "Cloud transformed ABC from a company constrained by infrastructure into one that scales as fast as its product-market fit allows. The recommended stack is public cloud, IaaS-PaaS blend, hybrid cost model, and AWS — with ELB, Auto Scaling and Lambda as the three automation anchors."

**Visual:** Summary bullet slide — no image prompt needed. *(~30s)*

---

## Slide 11 — References

**Content (key sources — full list in report):**
- Mell, P., & Grance, T. (2011). *NIST SP 800-145: The NIST definition of cloud computing*. NIST.
- McHaney, R. (2021). *Cloud Technologies*. Wiley.
- Eliaçık, E. (2022). The good, bad, and ugly sides of cloud computing. *Dataconomy*.
- Manvi, S., & Shyam, G. K. (2021). *Cloud Computing: Concepts and Technologies*. CRC Press.
- Bittok, T. (2022). Cloud Total Cost of Ownership. *LinkedIn Pulse*.
- Amazon Web Services. (n.d.-a). *AWS Well-Architected Framework*. AWS.
- Nishimura, H. (2022). *Introduction to AWS for Non-Engineers* [Course]. LinkedIn Learning.
- Accenture Technology. (2020). *Why Cloud Matters* [Video]. YouTube.
- Carpenter, T. (2020). *AWS SAA-C02 Cert Prep 1: Cloud Services Overview* [Video]. LinkedIn Learning.
- Naved, M., et al. (2022). Identifying the role of cloud computing in educational institutions. *Materials Today: Proceedings*.
- IBM. (n.d.-a). *SaaS, PaaS, IaaS explained.* IBM Cloud.
- IBM. (n.d.-b). *What is a public cloud?* IBM.
- IBM. (n.d.-c). *What is a virtual private cloud (VPC)?* IBM.
- Shore, J. (2020). *Cybersecurity with Cloud Computing: Service Models* [Video]. LinkedIn Learning.
- Linthicum, D. (2021). *Learning Cloud Computing: Core Concepts* [Video]. LinkedIn Learning.

**Visual:** Plain reference slide — no image prompt needed. *(~10s)*

---

## Nano Banana Summary

| # | Slide | Description | Status |
|---|-------|-------------|--------|
| #1 | 9 | AWS architecture diagram | Reuse from report |
| #4 | 8 | Provider comparison table | Reuse from report |
| #5 | 2 | NIST 5 characteristics wheel | New — prompt above |
| #6 | 3 | CAPEX vs OPEX two-column | New — prompt above |
| #7 | 4 | 10x surge bar chart | New — prompt above |
| #8 | 5 | Challenges vs Mitigation table | New — prompt above |
| #9 | 6 | Service + Deployment model spectrum | New — prompt above |

---

## Verification Checklist

- [ ] 11 slides total — timed at 5.5–6.5 min
- [ ] Every key report section (§2–§7) represented
- [ ] AWS services (ELB, Auto Scaling, Lambda) on their own slide (Slide 9)
- [ ] Each slide has: title, bullet content, speaker note, visual instruction
- [ ] Nano banana prompts #5–#9 are Lucidchart style, image output
- [ ] Existing prompts #1 and #4 reused — no duplication

---

## Design Notes (v1 Style Reference)

- **Background:** Dark navy + building photo
- **Title styling:** Orange drop-cap first letter, orange horizontal rule under title
- **Content boxes:** Dark semi-transparent background, white text
- **Logo:** Torrens logo bottom-right
- **Image prompts:** Target dark navy + orange colour palette where applicable
