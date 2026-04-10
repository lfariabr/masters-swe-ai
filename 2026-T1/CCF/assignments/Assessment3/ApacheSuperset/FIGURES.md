# Assessment 3 Figure Pack

Use this file as the evidence checklist for the report and screencast. Every figure should prove one rubric-relevant step, not just look good.

## Required Figures

### Figure 1 — Deployment Architecture Diagram
- File: `images/fig1-deployment-architecture.png`
- Purpose: Prove the deployment model/block diagram requirement in Part 2(b)
- Caption: `Figure 1: Azure deployment architecture showing the public cloud IaaS model, network boundary, virtual machine, and Apache Superset Docker stack.`

### Figure 2 — Azure Account / Subscription Confirmation
- Suggested file: `images/00_azure_portal_home.png`
- Purpose: Cover the brief requirement to discuss the procedure from cloud account registration onward
- Show: signed-in Azure portal, active subscription or student credit, region context if visible
- Caption: `Figure 2: Azure portal home page confirming active account access and subscription availability before resource provisioning.`

### Figure 3 — Resource Group Creation
- Suggested file: `images/01_resource_group.png`
- Purpose: Evidence for Task (a) create a resource group
- Show: `rg-superset-ccf501`, region, status
- Caption: `Figure 3: Resource group rg-superset-ccf501 created in Australia East to contain all deployment resources.`

### Figure 4 — Virtual Network and Subnet
- Suggested file: `images/02_vnet.png`
- Purpose: Evidence for Task (b) add a virtual network
- Show: `vnet-superset`, `snet-app`, address space details
- Caption: `Figure 4: Virtual network vnet-superset with dedicated application subnet snet-app for logical network isolation.`

### Figure 5 — NSG / Firewall Rules
- Suggested file: `images/03_nsg_rules.png`
- Purpose: Evidence for Task (c) protect the network with a firewall or security policy
- Show: allow `22` from your IP, allow `80`, allow `8088`, deny-all default
- Caption: `Figure 5: Network Security Group inbound rules implementing least-privilege access for SSH and the Superset web interface.`

### Figure 6 — VM Overview
- Suggested file: `images/04_vm_overview.png`
- Purpose: Bridge infrastructure provisioning to application deployment
- Show: Ubuntu VM, size, running state, public IP
- Caption: `Figure 6: Azure virtual machine overview showing the Ubuntu host, running status, and public IP used for deployment access.`

### Figure 7 — Superset Login Page
- Suggested file: `images/05_superset_login.png`
- Purpose: Evidence for Task (d) deploy the open-source web application server
- Show: browser at `http://<public-ip>:8088`
- Caption: `Figure 7: Apache Superset login page accessible through the Azure VM public IP on port 8088.`

### Figure 8 — Superset Dashboard / SQL Lab
- Suggested file: `images/06_superset_dashboard.png`
- Purpose: Prove the application is operational after deployment
- Show: dashboard or SQL Lab with data loaded
- Caption: `Figure 8: Apache Superset running successfully with a connected dataset and working analytics interface.`

### Figure 9 — RBAC Role Configuration
- Suggested file: `images/07_superset_rbac.png`
- Purpose: Support the governance and security criterion
- Show: `Admin`, `Alpha`, `Gamma` roles or user permissions view
- Caption: `Figure 9: Superset role-based access control configuration showing differentiated user permissions for governance and security.`

## Optional Figures

### Figure 10 — Docker Runtime Proof
- Suggested file: `images/08_docker_ps.png`
- Purpose: Extra implementation evidence if one Azure screenshot is weak
- Show: `docker ps` or container status
- Caption: `Figure 10: Docker container status confirming the Superset, PostgreSQL, and Redis services are running on the VM.`

### Figure 11 — SSH Session / Setup Commands
- Suggested file: `images/09_ssh_setup.png`
- Purpose: Strengthen the practical skills criterion
- Show: package install or `docker compose up -d`
- Caption: `Figure 11: SSH session used to install Docker and launch the Superset application stack on the Azure VM.`

## Capture Rules

- Keep Azure labels, resource names, and the browser address visible.
- Blur passwords, secrets, and personal identifiers only.
- Crop tightly, but leave enough UI context to prove authenticity.
- Use consistent filenames so the Word export stays manageable.
- After capture, update the report appendix status from `🕐` to `✅`.
