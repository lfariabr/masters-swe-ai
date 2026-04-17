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
- ✅ Superset deployed (Docker Compose on VM)
- ✅ Public access validated on `http://20.11.66.254:8088`
- ✅ VM stopped/deallocated after evidence capture to avoid compute charges
- ✅ Sample CSV datasets uploaded to Superset
- ✅ Working Superset dashboard created with 3 sample charts
- ✅ Report skeleton — structure, prose, references complete; final screenshot embedding pending
- ✅ Screenshots captured (Figures 2–9 complete; optional Fig X evidence captured)
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
- Actual deployment: `Standard_B2als_v2` Linux VM in Australia East
- Note: Superset with Docker Compose needs more RAM than B1s for stable startup
  → Spin up `Standard_B2als_v2` for deployment/screenshots, then stop/deallocate to save credits

## Deployment Checklist (Brief: account registration → 4 tasks)
- [x] Task 0: Register / confirm Azure account at portal.azure.com → screenshot Figure 2
- [x] Task a: Create resource group (`rg-superset-ccf501`) → screenshots Figures 3A-3B
- [x] Task b: Add virtual network (`vnet-superset`, subnet `snet-app`) → screenshots Figures 4A-4B
- [x] Task c: NSG with rules (see security section below) → screenshots Figures 5A-5C
- [x] Task d: Deploy Apache Superset via Docker Compose → screenshots Figures 6–8
- [x] RBAC roles configured / evidenced (Admin/Alpha/Gamma) → screenshots Figures 9A-9B

## Successful Deployment Evidence (2026-04-13)
- VM name: `supersetluisccf501`
- Resource group: `rg-superset-ccf501`
- Region: Australia East
- VM size: `Standard_B2als_v2`
- Public IP during validation: `20.11.66.254`
- Superset URL during validation: `http://20.11.66.254:8088`
- Runtime stack: Apache Superset + PostgreSQL 15 + Redis 7 via Docker Compose
- Validation command: `curl -I http://20.11.66.254:8088`
- Validation result: `HTTP/1.1 302 FOUND` redirecting to `/superset/welcome/`
- Post-demo cost control: VM status confirmed as `Stopped (deallocated)`

## Superset Dashboard Evidence (2026-04-18)
- Dashboard created with uploaded CSV sample data.
- Dataset 1: `cloud_costs_demo.csv` — Azure cost by service / environment.
- Dataset 2: `superset_usage_demo.csv` — Superset activity by user role.
- Dataset 3: `security_events_demo.csv` — governance/security events by control layer.
- Chart 1: Azure Cost by Service — bar chart using `SUM(cost_aud)` by `service`, grouped by `environment`.
- Chart 2: Superset Usage by Role — line chart using `SUM(event_count)` by `date`, grouped by `user_role`.
- Chart 3: Security Events by Control Layer — stacked bar chart using event count by `control_layer`, grouped by `status`.
- Screencast angle: show uploaded datasets, working dashboard, and RBAC roles to demonstrate both deployment and application-level use.

## Screenshot Inventory
- Figure 1: `images/fig1-deploym-diagram.png` — deployment architecture
- Figure 2: `images/fig2-portal-dashboard.webp` — Azure account / portal access
- Figures 3A-3B: `images/fig3-azure-resource-group-A.webp`, `images/fig3-azure-resource-group-B.webp`
- Figures 4A-4B: `images/fig4-azure-virtual-network-A.webp`, `images/fig4-azure-virtual-network-B.webp`
- Figures 5A-5C: `images/fig5-azure-nsg-A.webp`, `images/fig5-azure-nsg-B.webp`, `images/fig5-azure-nsg-C.webp`
- Figures 6A-6B: `images/fig6-azure-vm-A.webp`, `images/fig6-azure-vm-B.webp`
- Figure 7: `images/fig7-apache-login.webp`
- Figure 8: `images/fig8-apache-running.webp`
- Figures 9A-9B: `images/fig9-apache-rbac-A.webp`, `images/fig9-apache-rbac-B.webp`
- Optional Figure X: `images/figx-azure-ssh-connection.webp` — SSH setup proof
- Optional Figure X: `images/figx-azure-dockerps.webp` — Docker runtime proof

## Report Image Notes
- Add Figures 6–9 to the report because they complete Task d and security/RBAC evidence.
- Use `figX` images only if the report needs extra proof of terminal-level implementation. They are useful for an appendix or screencast backup, but not required in the main body if the report is already close to word/page limits.
- Update report text from `B2s` to `Standard_B2als_v2` so the written deployment matches the Azure evidence.
- Do not commit live secrets from the VM `docker-compose.yml`; keep repository artifacts with placeholders.

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
