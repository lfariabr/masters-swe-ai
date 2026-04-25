# Screencast Script — Trimmed (2–3 min)

**Target:** 2:45–3:00 max  
**Current recording:** 5m42s → cut by removing terminal section + tightening intro/closing

---

## Pre-recording checklist (do before hitting record)

- [X] Azure portal open and logged in
- [X] Superset already open in a second tab, logged in as admin
- [X] RBAC / List Roles page already open in a third tab
- [X] Public IP visible in the VM overview tab
- [X] Close all unrelated tabs and notifications

> **Why pre-login matters:** Your current recording lost ~45s to "let me sign out first so I can show you". Pre-loading all tabs means you just switch — no live login, no fumbling.

---

## Script

### 0:00–0:10 — Opening (cut university/lecturer detail)

> "This video is my CCF501 Assessment 3 submission — deploying Apache Superset on Microsoft Azure. I'll walk through the cloud resources, security policy, and the running application."

---

### 0:10–0:25 — Azure portal + subscription

*(Show portal home with subscription tile or credit remaining)*

> "Starting in the Azure portal. This confirms active account access and the subscription used for the deployment."

---

### 0:25–0:40 — Resource group

*(Click into rg-superset-ccf501, show region = Australia East)*

> "Here is the resource group — rg-superset-ccf501 in Australia East — the logical container for all resources."

---

### 0:40–0:55 — Virtual network and subnet

*(Click vnet-superset, show snet-app subnet)*

> "This is the virtual network and application subnet, providing logical isolation for the deployment."

---

### 0:55–1:20 — NSG / firewall

*(Open nsg-superset, show inbound rules: port 22 restricted, 8088 any, deny-all default)*

> "This Network Security Group is the main security policy. SSH is restricted to my IP, port 8088 is explicitly allowed, and all other inbound traffic is denied."

---

### 1:20–1:40 — VM overview

*(Show supersetluisccf501: Ubuntu, Standard_B2als_v2, Running, public IP visible)*

> "This Ubuntu VM hosts the deployment — Standard B2als v2, currently running, with the public IP shown here."

---

### 1:40–2:15 — Running Superset

*(Switch to Superset tab already logged in — no live login needed)*

> "Using that public IP on port 8088, Apache Superset loads successfully. The application is reachable over the public network, confirming a successful deployment."

*(Show one dashboard, chart, or SQL Lab query result — even 5 seconds is enough)*

> "The platform is fully operational."

---

### 2:15–2:35 — RBAC / governance

*(Switch to List Roles tab — show Admin, Alpha, Gamma)*

> "At the application layer, Superset enforces role-based access control. Admin, Alpha, and Gamma roles separate administration, analyst activity, and read-only access — satisfying the governance requirement."

---

### 2:35–2:50 — Closing

> "That covered account access, resource group, virtual network, security policy, virtual machine, and the deployed application with governance controls — the core practical requirements of the assessment."

---

## What was cut vs. original recording

| Segment | Original | Trimmed | Saving |
|---|---|---|---|
| Intro (uni name, lecturer name) | ~20s | ~10s | 10s |
| Sign-out / re-login fumble | ~45s | 0s (pre-logged in) | 45s |
| Verbose closing + repeat | ~30s | ~15s | 15s |
| Terminal SSH + docker ps | ~90s | removed | 90s |
| **Total saved** | | | **~2m30s** |

> Terminal evidence (SSH + `docker ps`) is in your static screenshots (figx-azure-ssh-connection.webp, figx-azure-dockerps.webp). The marker can see it in the report — no need to repeat it in the screencast.
