# Assessment 3 Screencast Walkthrough

This screencast is evidence for the practical-skills criterion. Keep it clear, brief, and easy for the marker to map to the brief.

## Target Length

- Recommended: `2-3 minutes`
- Maximum practical target: `3 minutes`

## Goal

Show, in order:
- cloud account access
- resource group
- virtual network
- firewall / security policy
- virtual machine
- public IP / application URL
- running Apache Superset instance
- security/governance evidence

## Recording Setup

- Use full screen or one browser window only
- Close unrelated tabs and notifications
- Prepare Azure portal, VM overview, and Superset in advance
- Have the public IP ready
- Log in before recording if password entry would slow you down

## Recommended Flow

### 0:00-0:12 — Opening
Suggested phrase:

`This video demonstrates my CCF501 Assessment 3 deployment of Apache Superset on Microsoft Azure. I will show the cloud resources, security policy, public IP, and the running application.`

### 0:12-0:30 — Azure account / subscription
Show:
- Azure portal home
- active subscription, student credit, or account context

Suggested phrase:

`I am starting in the Azure portal, which confirms active account access and the subscription used for this deployment. This is the starting point required before creating any cloud resources.`

### 0:30-0:48 — Resource group
Show:
- `rg-superset-ccf501`
- Australia East

Suggested phrase:

`Here is the resource group created for the project, named rg-superset-ccf501 in Australia East. It acts as the logical container for all resources used in the deployment.`

### 0:48-1:06 — Virtual network and subnet
Show:
- `vnet-superset`
- `snet-app`
- address ranges if visible

Suggested phrase:

`This is the virtual network and application subnet. They provide logical isolation for the deployment and satisfy the assessment requirement to add a virtual network.`

### 1:06-1:30 — NSG / firewall security policy
Show:
- inbound rules
- `22` restricted to your IP
- `8088`
- deny-all default

Suggested phrase:

`This Network Security Group is the main network security policy for the environment. SSH on port 22 is restricted to my IP address, the application port is explicitly allowed, and all other inbound traffic is denied by default.`

### 1:30-1:50 — Virtual machine overview
Show:
- Ubuntu VM
- running state
- public IP

Suggested phrase:

`This is the Ubuntu virtual machine hosting the deployment. It is currently running and exposes the public IP used to access Apache Superset in the browser.`

### 1:50-2:25 — Running application
Show:
- browser hitting `http://<public-ip>:8088`
- login page
- dashboard or SQL Lab after sign-in

Suggested phrase:

`Using the VM public IP, I can access Apache Superset on port 8088. This confirms the open-source web application server has been successfully deployed and is reachable over the network.`

If logging in:

`After authentication, the application loads successfully and the dashboard confirms the platform is operational.`

### 2:25-2:45 — Governance / RBAC
Show:
- role list or user management
- `Admin`, `Alpha`, `Gamma`

Suggested phrase:

`At the application layer, Superset uses role-based access control. Here I am showing the defined roles, which support the governance requirement by separating administration, analyst activity, and read-only access.`

### 2:45-3:00 — Closing
Suggested phrase:

`This demonstration covered account access, the resource group, virtual network, security policy, virtual machine, and the deployed Apache Superset application with governance controls, satisfying the core practical requirements of the assessment.`

## Marker-Friendly Checklist

Before recording, confirm the video shows:

- Azure portal login context
- resource group
- VNet / subnet
- NSG / firewall rules
- VM overview
- public IP
- Superset login or dashboard
- RBAC or equivalent governance evidence

## Do Not Miss

- Keep the resource names visible on screen
- Show the public IP at least once
- Do not spend too long in terminal setup
- Do not narrate implementation history the marker cannot see
- Do not hide the security rules panel too quickly

## If Time Allows

Add one short terminal proof shot:
- SSH session
- `docker ps`
- or `docker compose ps`

Suggested phrase:

`For completeness, this terminal view confirms the container services backing Superset are running on the Azure VM.`
