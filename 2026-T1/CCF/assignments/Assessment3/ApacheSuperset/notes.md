# CCF501 Assessment 3 — Apache Superset on Azure
> claude --resume "ccf-assessment3"
> codex resume ccf-assesment-3

- each screenshot needs to be done twice: before & after
- 2-3 minute video screencast showing Azure Portal + Superset in action (link to the recorded video in the report)

## Status
- ✅ Provider account setup — Azure account active, free credits available
- ✅ Resource group created
- ✅ VNet + subnet configured
- ✅ NSG / firewall rules applied
- 🕐 Superset deployed (Docker Compose on VM)
- ✅ Report skeleton — structure, prose, references complete; screenshots pending
- 🔥 Screenshots captured (before/after evidence started: Figures 2–5 complete; VM/Superset/RBAC pending)
- 🕐 Screencast recorded
- 🕐 Submission

## Decision Rationale
Superset over Metabase/MLflow because:
- Python-native, aligns with primary stack
- RBAC (Admin/Alpha/Gamma roles) gives rich security/governance content for the 20% rubric criterion
- Off the brief's suggested list — differentiates from cohort
- Feeds directly into BDA601 (Big Data & Analytics, T1-2027)
- Celery + Redis architecture in production mirrors Konquista — grounded analysis in 2e

## Provider: Azure
- Certification path: AZ-900 → DP-900 (recommended by Dr. Bhagwan + Dr. Shen, 2026-03-18)
- Free tier: Azure for Students or Pay-As-You-Go (B1s VM, 1 vCPU / 1 GB RAM)
- Note: Superset with Docker Compose needs at least B2s (2 vCPU / 4 GB RAM) for stable startup
  → Spin up B2s for deployment, screenshot, then scale down / deallocate to save credits

## Deployment Checklist (Brief: account registration → 4 tasks)
- [x] Task 0: Register / confirm Azure account at portal.azure.com → screenshot Figure 2
- [x] Task a: Create resource group (`rg-superset-ccf501`) → screenshots Figures 3A-3B
- [x] Task b: Add virtual network (`vnet-superset`, subnet `snet-app`) → screenshots Figures 4A-4B
- [x] Task c: NSG with rules (see security section below) → screenshots Figures 5A-5C
- [ ] Task d: Deploy Apache Superset via Docker Compose → screenshots Figures 6–8
- [ ] RBAC roles configured (Admin/Alpha/Gamma) → screenshot Figure 9

## NSG Rules Plan
| Priority | Name | Port | Protocol | Source | Destination | Action |
|---|---|---|---|---|---|---|
| 100 | Allow-SSH | 22 | TCP | My IP only | VNet | Allow |
| 110 | Allow-Superset | 8088 | TCP | Any | VNet | Allow |
| 65000 | DenyAllInbound | Any | Any | Any | Any | Deny |

## Report Skeleton — What Was Updated (2026-04-10)
- 1.2 Background rewritten: opens with concrete traditional-IT scenario, personal voice, synthesis sentence at close (A1 lesson applied)
- Table 1 (provider comparison) expanded: added cost model + resource elasticity rows (HD rubric requires these explicitly)
- 2c Deployment Procedure: account registration added as Task 0 before Task a; prose + Figure 2 placeholder
- Figures 2–8 renumbered downstream accordingly; Appendix A updated to match
- New reference added: Microsoft (n.d.-d) — Azure free account page

## Screencast Requirements
- Target length: 2-3 minutes
- Show Azure Portal dashboard (resource group, VM, NSG)
- Show Superset login screen with public IP in browser
- Show at least one dashboard or SQL Lab query running
- Show NSG inbound rules panel
- Show login credentials entry (blur password in post-edit if needed)

## Submission
- File: `studentID_CCF501_Assessment 3.docx`
- Due: 06 May 2026 (Wednesday, Week 12)
- Submit via Assessment 3 link in CCF501 navigation
