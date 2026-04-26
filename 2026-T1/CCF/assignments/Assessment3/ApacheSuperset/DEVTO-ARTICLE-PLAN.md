# Dev.to Article Plan — Apache Superset From Scratch

## Goal

Create a first dev.to draft about deploying Apache Superset from scratch for `CCF501 Assessment 3`.

The article should read as a practical technical story, not an academic report. The core narrative is:

> CCF501 Assessment 1 taught me how to reason about cloud architecture. Assessment 3 forced me to deploy a real open-source analytics platform, secure it, document it, and prove it works.

Use ISY503 only as supporting course context: intelligent systems and analytics tools become valuable when they are deployed, accessible, governed, and usable by real people.

## Output File

```text
2026-T1/CCF/assignments/Assessment3/ApacheSuperset/DEVTO-ARTICLE-DRAFT.MD
```

> Note: original target was `docs/refs/devToRefs/ApacheSuperset.md`, but `/docs/refs` is in `.gitignore`, so the tracked draft lives alongside the deployment artefacts under `Assessment3/ApacheSuperset/` instead.

## Recommended Article Shape

Target length: `1,800-2,400 words`.

Suggested tags:

```text
#cloudcomputing #azure #apache #superset #dataengineering
```

Suggested structure:

1. **Hook**
   - Open with deploying Apache Superset from scratch on Azure.
   - Position it as the jump from architecture diagrams to a live analytics platform.

2. **Course Context**
   - Mention `CCF501 Cloud Computing Fundamentals`.
   - Explain that the course moved through cloud essentials, deployment models, service models, provider comparison, deployment case studies, security, and governance.
   - Briefly mention `ISY503 Intelligent Systems` as the parallel subject reinforcing why deployment matters for AI/intelligent systems.

3. **Assessment 1 to Assessment 3 Bridge**
   - Assessment 1: cloud architecture reasoning and provider/service selection.
   - Assessment 3: build the thing for real.
   - Keep these as narrative anchors. Do not make the article rubric-heavy.

4. **Why Apache Superset**
   - Python-native and relevant to data engineering.
   - Open-source BI and dashboarding platform.
   - Stronger portfolio differentiation than a default app choice.
   - RBAC gives meaningful governance/security material.
   - Connects to current Data Analyst trajectory and future Big Data / Analytics work.
   - Mention Metabase and MLflow only as alternatives considered, not as the focus.

5. **Architecture Walkthrough**
   - Microsoft Azure public cloud IaaS deployment.
   - Resource group: `rg-superset-ccf501`.
   - Region: Australia East.
   - Virtual network: `vnet-superset`.
   - Subnet: `snet-app`.
   - Network Security Group: `nsg-superset`.
   - VM: Ubuntu 22.04, `Standard_B2als_v2`.
   - Runtime stack: Docker Compose with Apache Superset, PostgreSQL 15, Redis 7.
   - Public validation URL during capture: `http://<public-ip>:8088`.
   - Note: the VM was stopped/deallocated after evidence capture to avoid compute charges.

6. **From-Scratch Deployment Story**
   - Azure account / subscription verification.
   - Create resource group.
   - Create VNet and subnet.
   - Apply NSG/firewall policy.
   - Launch VM.
   - SSH into VM.
   - Install Docker and Docker Compose.
   - Launch Superset stack.
   - Validate with browser and `curl -I`.
   - Upload sample CSVs.
   - Create dashboard with three charts.
   - Configure Admin / Alpha / Gamma roles.

7. **Security and Governance**
   - SSH port `22` restricted to author IP.
   - Superset port `8088` explicitly allowed.
   - Deny-all default inbound rule.
   - SSH key-based auth only.
   - Superset RBAC:
     - Admin: full control.
     - Alpha: analyst / dashboard creator.
     - Gamma: read-only viewer.
   - Environment variables / placeholder secrets, no committed live credentials.
   - Acknowledge limitation: no TLS in v1; HTTPS is a production improvement.

8. **AWS Portability Note**
   - Keep this short.
   - Azure remains the main story.
   - Mention a parallel AWS deployment was completed to test portability.
   - Useful lessons:
     - Amazon Linux 2023 uses `dnf`, not `apt`.
     - Docker Compose needed a standalone binary.
     - Browser access to port `8088` can fail on some networks; SSH tunnelling fixed it.
   - Do not turn the article into a dual-cloud article.

9. **AI-Assisted Workflow**
   - Mention the workflow transparently:
     - Codex helped build the plan.
     - Claude executed the draft.
     - Final review stayed human-led.
   - Frame AI as a planning and drafting accelerator, not as a replacement for the technical work.

10. **Takeaways**
    - Architecture diagrams are useful, but deployment exposes the real trade-offs.
    - Cloud security is a layered set of decisions, not one checkbox.
    - Open-source analytics tools are excellent portfolio projects because they combine infrastructure, data, security, and usability.
    - Stopping/deallocating cloud resources matters when working with student/free credits.

## Source Files For Claude

Use these files as the factual source of truth:

```text
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/README.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/ISY/README.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/CCFAssessment1.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/CCF501_Assessment3.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/notes.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/CCF501_Assessment3_Report_Skeleton.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/TECHNICAL-ARTIFACTS.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/IMPLEMENTATION-PLAN.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/IMPLEMENTATION-PLAN-AWS.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/screencast/SCREENCAST_trimmed.md
```

Use these as style references:

```text
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/StcDatalab.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/invoiceLedger.md
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/EigenAi.md
```

## Image Placeholders

Include dev.to image placeholders in the draft. Do not embed local absolute image paths as final public URLs.

Recommended screenshot placeholders:

```markdown
![Azure deployment architecture showing Resource Group, VNet, NSG, VM, Docker, Superset, PostgreSQL, and Redis](UPLOAD_IMAGE_HERE)
![Azure portal showing the Superset VM and public IP evidence](UPLOAD_IMAGE_HERE)
![Apache Superset login screen running on Azure port 8088](UPLOAD_IMAGE_HERE)
![Apache Superset dashboard created from uploaded CSV datasets](UPLOAD_IMAGE_HERE)
![Apache Superset RBAC roles showing Admin, Alpha, and Gamma](UPLOAD_IMAGE_HERE)
![Docker ps output showing Superset, PostgreSQL, and Redis containers running](UPLOAD_IMAGE_HERE)
```

Local screenshot inventory lives here:

```text
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/2026-T1/CCF/assignments/Assessment3/ApacheSuperset/images/
```

## Claude Execution Prompt

Use this prompt with Claude:

```text
Create a dev.to draft v1 at:
/Users/luisfaria/Desktop/sEngineer/masters_SWEAI/docs/refs/devToRefs/ApacheSuperset.md

Write a technical story about deploying Apache Superset from scratch on Microsoft Azure for CCF501 Assessment 3. Use CCF501 Assessment 1 as the earlier architecture-design anchor, and briefly connect ISY503 as the Intelligent Systems course context where deployment matters.

Angle: practical technical story, not academic report.
AWS scope: brief comparison only.
Assessment depth: narrative anchors only, no rubric-heavy explanation.
Target: 1,800-2,400 words.

Use the local source files listed in DEVTO-ARTICLE-PLAN.md as factual sources. Match the writing style of the existing dev.to drafts in docs/refs/devToRefs.

Do not invent facts. Do not include real secrets, passwords, student IDs, or private account details. Use image placeholders with clear alt text where dev.to screenshots should be uploaded later.

Include title, tags, intro, course context, why Superset, architecture walkthrough, deployment steps, security/governance, AWS portability note, AI-assisted workflow, and final takeaways.
```

## Acceptance Checks

Before considering the draft done, verify:

- The article is mainly about the Azure Superset deployment.
- Assessment 1 and Assessment 3 are mentioned naturally as story anchors.
- ISY503 is supporting context only.
- AWS appears only as a short portability/pitfall comparison.
- Technical details match the local source files.
- No secrets, passwords, student IDs, live access details, or private account details are included.
- The article has image placeholders with useful alt text.
- The tone matches previous dev.to articles: personal, practical, technical, and build-in-public.

