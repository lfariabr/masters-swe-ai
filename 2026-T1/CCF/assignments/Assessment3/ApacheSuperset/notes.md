# CCF501 Assessment 3 — Apache Superset on Azure
> copilot --resume=5964f668-562e-4c32-8ae2-40f1b0d4343f
> claude --resume "ccf-assessment3"
> codex resume 019d7165-5cb5-7f20-b4da-f456276aa3ec

## Status
- 🕐 Provider account setup (Azure free tier)
- 🕐 Resource group created
- 🕐 VNet + subnet configured
- 🕐 NSG / firewall rules applied
- 🕐 Superset deployed (Docker Compose on VM)
- 🕐 Report draft
- 🕐 Screenshots captured
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

## Deployment Checklist (4 Tasks from Brief)
- [ ] Task a: Create resource group (e.g. `rg-superset-ccf501`)
- [ ] Task b: Add virtual network (`vnet-superset`, subnet `snet-app`)
- [ ] Task c: NSG with rules (see security section below)
- [ ] Task d: Deploy Apache Superset via Docker Compose

## NSG Rules Plan
| Priority | Name | Port | Protocol | Source | Destination | Action |
|---|---|---|---|---|---|---|
| 100 | Allow-SSH | 22 | TCP | My IP only | VNet | Allow |
| 110 | Allow-HTTP | 80 | TCP | Any | VNet | Allow |
| 120 | Allow-Superset | 8088 | TCP | Any | VNet | Allow |
| 65000 | DenyAllInbound | Any | Any | Any | Any | Deny |

## Screencast Requirements
- Show Azure Portal dashboard (resource group, VM, NSG)
- Show Superset login screen with public IP in browser
- Show at least one dashboard or SQL Lab query running
- Show NSG inbound rules panel
- Show login credentials entry (blur password in post-edit if needed)

## Submission
- File: `studentID_CCF501_Assessment 3.docx`
- Due: 06 May 2026 (Wednesday, Week 12)
- Submit via Assessment 3 link in CCF501 navigation
