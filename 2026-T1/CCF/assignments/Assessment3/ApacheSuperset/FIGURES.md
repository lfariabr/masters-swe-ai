# Assessment 3 Figure Pack

Use this file as the evidence checklist for the report and screencast. Every figure should prove one rubric-relevant step, not just look good.

## Required Figures

### Figure 1 — Deployment Architecture Diagram
- File: `images/fig1-deploym-diagram.png`
- Purpose: Prove the deployment model/block diagram requirement in Part 2(b)
- Caption: `Figure 1: Azure deployment architecture showing the public cloud IaaS model, network boundary, virtual machine, and Apache Superset Docker stack.`

### Figure 2 — Azure Account / Subscription Confirmation
- File: `images/fig2-portal-dashboard.webp`
- Purpose: Cover the brief requirement to discuss the procedure from cloud account registration onward
- Show: signed-in Azure portal, active subscription or student credit, region context if visible
- Caption: `Figure 2: Azure portal home page confirming active account access and subscription availability before resource provisioning.`

### Figures 3A-3B — Resource Group Creation
- Files: `images/fig3-azure-resource-group-A.webp`, `images/fig3-azure-resource-group-B.webp`
- Purpose: Evidence for Task (a) create a resource group
- Show: before state with no resource groups, then after state with `rg-superset-ccf501`, region, and subscription
- Captions: `Figure 3A: Resource Groups page before creating the assessment resource group.` / `Figure 3B: Resource group rg-superset-ccf501 created in Australia East.`

### Figures 4A-4B — Virtual Network and Subnet
- Files: `images/fig4-azure-virtual-network-A.webp`, `images/fig4-azure-virtual-network-B.webp`
- Purpose: Evidence for Task (b) add a virtual network
- Show: before state with no virtual networks, then after state with `vnet-superset` in `rg-superset-ccf501`
- Captions: `Figure 4A: Virtual Networks page before creating the assessment network.` / `Figure 4B: VNet vnet-superset created in rg-superset-ccf501.`

### Figures 5A-5C — NSG / Firewall Rules
- Files: `images/fig5-azure-nsg-A.webp`, `images/fig5-azure-nsg-B.webp`, `images/fig5-azure-nsg-C.webp`
- Purpose: Evidence for Task (c) protect the network with a firewall or security policy
- Show: before state with no NSGs, after state with `nsg-superset`, then inbound rules allowing `22` from your IP and `8088`
- Captions: `Figure 5A: Network Security Groups page before creating the assessment security policy.` / `Figure 5B: Network Security Group nsg-superset created in rg-superset-ccf501.` / `Figure 5C: NSG inbound rules — allow 22 restricted to author IP and 8088, deny all else.`

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
