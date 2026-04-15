Cloud Security Handbook
by Eyal Estrin

Chapter 8: Understanding Common Security Threats to Cloud Services

In Chapters 2-7, we covered the fundamental building blocks of securing cloud services (including services for compute, storage, networking, identity and access management (IAM), auditing, threat management, and incident response), as well as looking at encryption for cloud services.

This chapter will cover the other side of the equation: common security threats to cloud services. We will also consider how to mitigate these threats.

Knowing the threats your organization faces when using cloud services will give you an understanding of what to look for and how to better protect your cloud environments in advance. Getting hacked is more a question of when rather than if, so the knowledge presented in this chapter should help you to be prepared for such an eventuality.

In this chapter, we will cover the following topics:

The MITRE ATT&CK framework
Detecting and mitigating data breaches in cloud services
Detecting and mitigating misconfigurations in cloud services
Detecting and mitigating insufficient IAM in cloud services
Detecting and mitigating account hijacking in cloud services
Detecting and mitigating insider threats in cloud services
Detecting and mitigating insecure APIs in cloud services
Detecting and mitigating the abuse of cloud services
Technical requirements
For this chapter, the reader needs to have a solid understanding of information security concepts. These include (but are not limited to) threats, mitigations, data breaches, misconfigurations, account hijacking, and others.

The MITRE ATT&CK framework
The MITRE ATT&CK framework is a knowledge base of hacking techniques. The cloud matrix of MITRE ATT&CK contains the general flow of cyber attacks:

Initial access
Execution
Persistence
Privilege escalation
Defense evasion
Credential access
Discovery
Lateral movement
Collection
Exfiltration
Impact
Understanding attack techniques allows us to understand the results of attacks. For example, using the abuse of credentials allows an attacker to gain persistent access to our system.

Another attack example is cloud object storage discovery, which may be used by an attacker to gain access to all objects inside a cloud storage instance.

Reviewing all attack techniques will allow us to understand which security controls we can implement to mitigate potential attacks in our cloud environment, whether that's built-in security tools with AWS, Azure, or GCP, or external third-party tools.

For more information, refer to the following resources:

MITRE ATT&CK, Cloud Matrix:

https://attack.mitre.org/matrices/enterprise/cloud/

MITRE ATT&CK, IaaS Matrix:

https://attack.mitre.org/matrices/enterprise/cloud/iaas/

MITRE ATT&CK, SaaS Matrix:

https://attack.mitre.org/matrices/enterprise/cloud/saas/

How to Improve Threat Detection and Hunting in the AWS Cloud Using the MITRE ATT&CK Matrix:

https://pages.awscloud.com/rs/112-TZM-766/images/How%20to%20Improve%20Threat%20Detection%20and%20Hunting%20in%20the%20AWS%20Cloud%20Using%20the%20MITRE%20ATT%26CK%C2%AE%20Matrix%20_%20Slides.pdf

MITRE ATT&CK mappings released for built-in Azure security controls:

https://www.microsoft.com/security/blog/2021/06/29/mitre-attck-mappings-released-for-built-in-azure-security-controls/

Detecting and mitigating data breaches in cloud services
A data breach, as its name implies, is the unauthorized access of an organization's data. This can result in the exposure of customer or employee personal data and lead to reputational damage for an organization. Because of the shared responsibility model of cloud computing, we need to think differently about data breaches. For example, we do not control the physical storage of our data. This presents a different threat model when compared to a traditional on-premises data center we manage. Data breaches are more likely when working with public cloud services because in this case, we don't control the physical storage of our data. Does this mean that storing our data in the cloud makes it more prone to data breaches? It depends on the cloud service model and on the maturity of the cloud service provider. According to the shared responsibility model, when using an infrastructure as a service (IaaS) solution, we (customers) are in charge of implementing most of the security controls over the operating system (OS).

In a platform as a service (PaaS) context, we rely on the cloud service provider in terms of OS hardening, patch management, and backups, but it is very common in a PaaS that we can review audit logs and set proper permissions for who has application-layer access to the service.

In a software as a service (SaaS) context, things get tricky. There is no standard for SaaS, meaning anyone who deploys an application on a virtual machine or resides on a public IaaS can declare themselves a SaaS provider.

Depending on the maturity of the SaaS provider, we may have the option to add security controls (such as data encryption at rest), configure strong authentication (such as SAML with multi-factor authentication (MFA)), connect to audit logs via REST APIs, and others.

Before talking about data breaches, let's try to focus on what data we store in the cloud. The following are a few examples of data we might store in the cloud:

Public data: Data that we can safely store on public websites. If such data is exposed by anonymous users, it will not hurt our organization (this could be news sites, currency rates, the organization's physical address from a Contact us web page, and so on).
Intellectual property/trade secrets: This is data that we must keep safe, as exposing it will hurt our business and impact our ability to achieve revenue (examples of intellectual property could be data from a pharmaceutical company developing a cure against COVID-19, data from a start-up developing new technology for allowing secure authentication without using passwords, and so on).
Personally identifiable information (PII): This includes any identifiable information about people (for example, contact details, credit card information, healthcare data, and so on).
Common consequences of data breaches
As a result of a data breach, there are a number of things that might happen to our data:

Breach of confidentiality: This could include customer financial or healthcare data being exposed, which could then be used by hackers.
Data integrity: This could include someone accessing a bank's core systems and manipulating customer financial information; as a result, a customer might notice a change in their account balance.
Availability: One of the consequences of a data breach can be the use of ransomware that encrypts the data of the target, making it unavailable.
Let's now look at some of the best practices for detecting and mitigating data breaches.

Best practices for detecting and mitigating data breaches in cloud environments
Here are some of the controls that allow us to mitigate data breaches:

Networking layer: Configure access controls (network Access Control Lists (ACLs), security groups, and more) to control who can access our resources.
Encryption: Implement encryption in transit and at rest. This allows us to keep our data confidential at all times.
Auditing: This allows us to keep track of who accessed (or tried to access) our resources and what actions have been made (for example, through APIs) related to resources.
Threat management: This allows us to review logs and detect potential threats to our services.
Recovery strategy: Prepare a disaster recovery plan. For example, technical backups and snapshots of volumes, databases, and processes. This should also include procedures for the recovery of data (for example, which systems to recover first, how to automate recovery using infrastructure as code, and more).
Here are some of the best practices to follow:

Use a secure development life cycle: Embed this as part of your development process – this includes controls such as the following:
Authentication and authorization: Enforce who can access your application and data.
Input validation: Check and validate what strings and/or data can be inserted into your application and backend database.
Application-layer attacks: Detect and mitigate attacks such as code injection attacks, cross-site scripting, and others.
Use access control lists: Set network/firewall rules to configure who can access your resources (for both inbound and outbound network traffic).
Use audit trails: These allow you to monitor the accessing of resources and the actions carried out.
Check the integrity of your data: Make sure stored data hasn't been changed.
Use change management: Check for deviations from preconfigured settings (such as services that have public access or servers that might need hardening, among others).
Use data classification: Combine this with data leakage services to assist the detection of data exfiltration.
Use encryption: Ensure the confidentiality of your data when in transit and at rest.
Configure organization-wide policies: For example, use inherited policies that enforce who can access which resources and what actions can be taken on resources, enforce auditing, enforce encryption, and so on.
Use backups: This allows you to recover your data and applications after a data breach.
In the following section, we will review common services from Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) that will allow you to detect and mitigate data breaches.

Common AWS services to assist in the detection and mitigation of data breaches
Here are some of the common AWS services that can be used to mitigate data breaches:

Use Amazon VPC controls (for example, network ACLs and security groups) and AWS Network Firewall to configure inbound and outbound network access rules.
Use AWS IAM to configure who can authenticate and access your applications, resources, and data.
Use AWS KMS to encrypt your data, to prevent data breaches.
Use AWS Secrets Manager to keep your secrets (access keys, passwords, credentials, and others) safe from data breaches.
Use AWS CloudTrail to detect API activities (for users, computers, service accounts, and so on) that might indicate a data breach.
Use Amazon CloudWatch to log and alert suspicious activities that pass certain thresholds (such as multiple failed login attempts).
Use Amazon GuardDuty to detect data breaches.
Use AWS VPC Flow Logs to review network activity that might indicate data breaches.
Use AWS Config to detect configuration changes in your environment and cloud resources.
Use Amazon Detective to detect the root cause of a data breach.
Use AWS Backup to recover your environment after a data breach.
Common Azure services to assist in the detection and mitigation of data breaches
Here are some of the common Azure services that can be used to mitigate data breaches:

Use Azure network security groups (NSGs) to configure inbound and outbound network access rules.
Use Azure Active Directory (AD) to configure who can authenticate and access your applications, resources, and data.
Use Azure Key Vault to encrypt your data to prevent data breaches.
Use Azure confidential computing to protect your data against data breaches.
Use Azure Monitor and Log Analytics to detect suspicious activities that might indicate data breaches.
Use Azure Defender (previously known as Azure Advanced Threat Protection) to detect misconfigurations that might cause data breaches.
Use Azure Network Watcher to review network activity that might indicate data breaches.
Use Azure Security Center to assist in the detection of data breaches.
Use Azure Sentinel to correlate multiple data sources to assist in the detection of data breaches.
Use Azure Backup to recover your environment after a data breach.
Common GCP services to assist in the detection and mitigation of data breaches
Here are some of the common GCP services that can be used to mitigate data breaches:

Use GCP VPC firewall rules to configure inbound and outbound network access rules.
Use Google Cloud IAM to configure who can authenticate and access your applications, resources, and data.
Use Google Cloud KMS to encrypt your data to prevent data breaches.
Use Google Secret Manager to keep your secrets (access keys, passwords, credentials, and more) safe from data breaches.
Use GCP confidential computing to protect your data against data breaches.
Use Google Cloud Logging to detect suspicious activities that might indicate data breaches.
Use GCP VPC Flow Logs to review network activity that might indicate data breaches.
Use Google Cloud Security Command Center to correlate multiple data sources to assist in the detection of data breaches.
For more information, refer to the following resources:

Beware the top three blind spots that precede cloud data breaches:

https://itwire.com/guest-articles/guest-opinion/beware-the-top-three-blind-spots-that-precede-cloud-data-breaches.html

36% of organizations suffered a serious cloud security data leak or a breach in the past year:

https://www.helpnetsecurity.com/2021/07/27/cloud-security-data-leak/

Top Cloud Security Breaches and How to Protect Your Organization:

https://cloud.netapp.com/blog/cis-blg-top-cloud-security-breaches-and-how-to-protect-your-organization

Nearly 80% of Companies Experienced a Cloud Data Breach in Past 18 Months:

https://www.securitymagazine.com/articles/92533-nearly-80-of-companies-experienced-a-cloud-data-breach-in-past-18-months

Detecting and mitigating misconfigurations in cloud services
Misconfigurations are a common threat when using cloud services. Under the shared responsibility model, some of the common reasons for misconfigurations in cloud services that fall under the customer's responsibility are as follows:

Lack of knowledge in operating cloud services
Human error
Default settings being left in an unsecured state
Large and complex environments being deployed in a very short time
Fast and unmanaged changes to cloud environments
Here are some common examples of misconfigurations in cloud services:

Having overly broad IAM policies (or role-based access control policies) – for example, default permissions that allow users to conduct actions on sensitive resources, or having more permissions than needed to accomplish their daily tasks
Object storage being publicly accessible to anyone on the internet
Snapshots and VM images being publicly accessible to anyone on the internet
Databases being publicly accessible to anyone on the internet
Virtual servers being publicly accessible to anyone on the internet using Secure Shell (SSH) or Remote Desktop Protocol (RDP) ports
Unpatched servers and databases
Here are some best practices for detecting and mitigating misconfigurations in cloud environments:

Use organizational configuration policies to enforce the desired configurations, such as encrypted storage, blocking public access to resources, and more (as explained in Chapter 13, Security in Large-Scale Environments).
Use infrastructure as code for automation and standard configurations (as explained in Chapter 13, Security in Large-Scale Environments).
Use Cloud Security Posture Management (CSPM) to detect misconfigurations (as explained in Chapter 12, Managing Multi-Cloud Environments).
Scan for misconfigurations (such as the use of vulnerable components) as part of the build process.
Use change management to check for deviations from preconfigured settings (such as services which might have public access or servers which might need hardening, and more)
Limit access to production environments to the minimum required (both by using minimal permissions and using network access controls) – do not allow developers or end users access to production environments.
Conduct employee training on the proper use of the various cloud services.
Review which identities exist in your organization that require access to cloud resources and manage these as required.
In the following section, we will review common services from AWS, Azure, and GCP that will allow you to detect and mitigate misconfigurations.

Common AWS services to assist in the detection and mitigation of misconfigurations
Here are some AWS services that can mitigate misconfigurations:

Use AWS IAM to configure who can authenticate and access your applications, resources, and data.
Use AWS IAM Access Analyzer to detect users who haven't used their accounts for a long time, such as cross-account access on AWS with public access to resources such as Amazon S3 and AWS KMS.
Use Amazon GuardDuty to detect misconfigurations, such as AWS EC2 trying to access command-and-control (C&C) networks, an S3 bucket being publicly accessible to the internet, and more.
Use AWS Config to detect configuration changes in your environment and cloud resources and compare them against relevant compliance policies.
Use AWS Security Hub to track events from multiple AWS services and detect misconfiguration against policy standards.
Use AWS Amazon Inspector to detect misconfigurations, such as deviations from Centre for Internet Security (CIS) hardening benchmarks, missing security patches, and so on.
Use AWS Audit Manager to detect misconfigurations against compliance standards.
Use AWS Trusted Advisor to review common security misconfigurations.
Use AWS Control Tower to centrally enforce configurations on entire AWS organization levels (for example, blocking S3 public access, blocking user abilities such as deploying virtual servers, and so on).
Use AWS CloudFormation to deploy new cloud environments in a standardized way.
Let's now look at the detection and mitigation of misconfigurations in Azure cloud services.

Common Azure services to assist in the detection and mitigation of misconfigurations
Here are some Azure services that can mitigate misconfigurations:

Use Azure AD to configure who can authenticate and access your applications, resources, and data.
Use the Azure Activity log, which is a part of Azure Monitor, to detect what actions were made in your Azure environment.
Use Microsoft Defender for Cloud to detect security misconfigurations in various Azure services.
Use Azure Advisor to review common security misconfigurations.
Use Azure Policy and Azure management groups to centrally enforce configurations on entire Azure tenant levels (for example, blocking blob storage public access, blocking user abilities such as deploying virtual servers, and so on).
Use Azure Resource Manager to deploy new environments in a standard way.
Let's now look at the detection and mitigation of misconfigurations in GCP.

Common GCP services to assist in the detection and mitigation of misconfigurations
Here are some common GCP services that can be used to mitigate misconfigurations:

Use Google Cloud IAM to configure who can authenticate and access your applications, resources, and data.
Use Google Cloud Logging to detect what actions were made in your GCP environment.
Use Google Cloud Security Command Center to detect security misconfigurations in various GCP services.
Use GCP Resource Manager to centrally enforce configurations for entire GCP organization levels (for example, restricting service account creation, restricting resource locations, and more).
Use Google Cloud Deployment Manager to deploy new environments in a standard way.
For more information, please refer to the following resources:

Cloud misconfigurations surge, organizations need continuous controls:

https://www.helpnetsecurity.com/2020/02/20/cloud-misconfigurations/

Misconfigurations: A Hidden but Preventable Threat to Cloud Data:

https://securityintelligence.com/articles/misconfigurations-hidden-threat-to-cloud-data/

Cloud misconfiguration, a major risk for cloud security:

https://securityaffairs.co/wordpress/117305/security/cloud-misconfiguration-risks.html

Detecting and mitigating insufficient IAM and key management in cloud services
Insufficient IAM can happen in a scenario where we have a large number of user identities (such as in an enterprise organization) but we fail to properly manage the identities. Or we might use cryptography to protect sensitive data but fail to follow key rotation best practices, and as a result, increase the chance of data exposure by unauthorized persons.

Here are some common consequences of insufficient IAM and key management:

Failing to follow the principle of least privileged, which leads to excessive permissions being granted
Failing to configure access controls – for example, allowing unauthorized access to sensitive data (such as PII, credit card data, healthcare data, and so on), which leads to exposed credentials
Not enforcing the password policy (for example, allowing short passwords, not enforcing password changes, allowing password reuse, and so on), which leads to password brute force attacks
Encrypting data but keeping the same cryptographic key without key rotation, which can potentially lead to breaches in data confidentiality
Not enforcing the use of MFA, which can lead to unauthorized access to resources and data
Embedding credentials or cryptographic keys inside code and scripts, which can lead to exposure of credentials
Not configuring audit trails, which leads to a lack of visibility of which identities have access to which resources
Here are some best practices for detecting and mitigating insufficient IAM in cloud environments:

Manage the entire identity life cycle for your employees and any sub-contractors who have access to your systems and data – this should include recruitment, account provisioning, access management to resources, and finally, account deprovisioning when an employee or sub-contractor has left the organization or no longer needs access to systems and data.
Use a central repository for identities, where you provision and deprovision accounts and set password policies.
Use federation to allow access from on-premises environments to cloud environments and resources, and between external partners' or customers' IAM systems and your cloud environments.
Block the use of weak and legacy authentication protocols (such as New Technology LAN Manager (NTLM) and clear text Lightweight Directory Access Protocol (LDAP)).
Enforce the use of a password policy (for example, by stipulating a minimum password length, minimum and maximum password age, password history, complex passwords, account lockout and release settings, and more).
Enforce the use of MFA.
Audit users' actions and correlate their activities using a Security Information and Event Management (SIEM) system that will allow you to detect anomalous behavior (such as user logins after working hours, users trying to access resources for the first time, and so on).
Review user login activities. If a user hasn't used their account for several weeks, perhaps it is time to lock or disable the account due to inactivity, which is also a part of the least privilege principle.
Implement identity governance – do the right users have the right roles at the right time?
Review user access privileges, locate accounts with default or increased permissions that are not needed, and fine-tune the accounts' privileges.
Follow the principle of least privilege when granting permissions to resources.
Follow the concept of segregation of duties to avoid single users having privileges to conduct sensitive actions (such as a user with the permissions both to generate encryption keys and use encryption keys).
Use a secure and central repository for generating, storing, retrieving, and rotating encryption keys.
Use a secrets management service to generate, store, retrieve, and rotate secrets, passwords, API keys, and access keys inside code to access resources, while keeping secrets secured and encrypted.
Encrypt all sensitive information (such as PII, credit card numbers, healthcare data, and so on).
In the following section, we will review common services from AWS, Azure, and GCP that will allow you to detect and mitigate insufficient IAM in your cloud services.

Common AWS services to assist in the detection and mitigation of insufficient IAM and key management
Here are some common AWS services that can be used to mitigate insufficient IAM and key management:

Use AWS IAM to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use AWS IAM Access Analyzer to detect users who haven't used their accounts for a long time.
Use AWS Directory Service to configure who can authenticate and access your legacy (based on Kerberos authentication) servers and applications and to enforce password policies.
Enforce the use of MFA to avoid the successful use of your users' credentials to access your applications and systems.
Use AWS KMS to generate, store, and rotate encryption keys.
Use AWS Secrets Manager to generate, store, and rotate secrets (for example, credentials, access keys, passwords, and more).
Use AWS CloudTrail to detect API activities, such as failed login attempts.
Common Azure services to assist in the detection and mitigation of insufficient IAM and key management
Here are some common Azure services that can be used to mitigate insufficient IAM and key management:

Use Azure AD to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use Azure AD Domain Services to configure who can authenticate and access your legacy (Kerberos-based) servers, applications, resources, and data, and use it to enforce password policies.
Enforce the use of MFA to avoid the successful use of your users' credentials to access your applications and systems.
Use Azure AD Conditional Access to enforce different access and authentication methods when users are connecting from the corporate network versus an unknown IP address.
Use Azure Privileged Identity Management (PIM) to restrict users' permissions to your Azure resources.
Use Azure Key Vault to generate, store, and rotate encryption keys and secrets (for example, credentials, access keys, passwords, and more).
Enable Azure AD audit logs and use Azure Log Analytics to detect activities such as failed login attempts.
Use Azure Information Protection to detect authentication failure events.
Use Azure Sentinel to correlate logs from multiple log sources to detect failed login attempts.
Use Azure Customer Lockbox to detect login attempts by Microsoft support engineers.
Common GCP services to assist in the detection and mitigation of insufficient IAM and key management
Here are some common GCP services that can be used to mitigate insufficient identity and access management:

Use Google Cloud IAM to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use the Google Managed Service for Microsoft Active Directory to configure who can authenticate and access your legacy (Kerberos-based) servers and applications, resources, and data, and use it to enforce password policies.
Enforce the use of MFA to avoid successful but unauthorized use of your users' credentials to access your applications and systems.
Use Google Cloud KMS to generate, store, and rotate encryption keys.
Use Google Secret Manager to generate, store, and rotate secrets (for example, credentials, access keys, passwords, and more).
Use Google Cloud Logging to detect activities such as failed login attempts.
Use Google Cloud Security Command Center to correlate logs from multiple log sources to detect failed login attempts.
Use Google Access Transparency and Access Approval to detect login attempts by Google support engineers.
For more information, refer to the following resources:

Are Your Cloud Environments Protected from Identity-Based Attacks?:

https://www.eweek.com/cloud/are-your-cloud-environments-protected-from-identity-based-attacks/

Top 9 Identity & Access Management Challenges with Your Hybrid IT Environment:

https://www.okta.com/resources/whitepaper/top-9-iam-challenges-with-your-hybrid-it-environment/

Major threats to cloud infrastructure security include a lack of visibility and inadequate IAM:

https://www.helpnetsecurity.com/2021/06/30/cloud-infrastructure-security/

7 Best Practices for Identity Access Management:

https://www.sailpoint.com/identity-library/7-best-practices-for-identity-access-management/

Detecting and mitigating account hijacking in cloud services
Account hijacking happens when an account (either belonging to a human or a system/application/service account) is compromised and an unauthorized person gains access to use resources and data on behalf of the (usually high-privileged) compromised account.

Here are some common consequences of account hijacking:

Unauthorized access to resources
Data exposure and leakage
Data deletion
System compromise
Identity theft
Ransomware or malicious code infection
Account lock-out
Denial of services
Denial of wallet (there could be a huge cloud spend due to resource misuses such as Bitcoin mining)
Website defacement
Some common methods of account hijacking are as follows:

Phishing attacks against a system administrator's account, allowing an attacker to gain access to databases with customer data
Access keys for a privileged account stored on an S3 bucket that was publicly accessible and as a result, hackers being able to use the access keys to deploy multiple expensive virtual machines for bitcoin mining
Weak administrator passwords allowing attackers to gain control over the administrator privileges and change permissions to allow public access to backups containing customer financial details
Here are some best practices for detecting and mitigating account hijacking:

Enforce the use of strong passwords (for example, by stipulating a minimum password length, minimum and maximum password age, password history, complex passwords, account lockout and release settings, and more)
Enforce the use of MFA.
Audit user actions and correlate their activities using an SIEM system that will allow you to detect anomalous behavior (such as user logins after working hours, users trying to access resources for the first time, and so on).
Follow the principle of least privilege when granting permissions to resources.
Follow the concept of segregation of duties to avoid single user having the privilege to conduct sensitive actions (such as a user with the permissions both to generate encryption keys and use encryption keys).
Invest in employee awareness to allow all your employees to detect phishing attempts, avoid opening emails from unknown sources, avoid running unknown executables, and avoid plugging in removable media from unknown sources.
Invest in business continuity planning to prepare for recovery after a system is compromised (for example, rebuilding systems, recovering data from backups, changing credentials, and so on).
In the following section, we will review common services from AWS, Azure, and GCP that will allow you to detect and mitigate account hijacking.

Common AWS services to assist in the detection and mitigation of account hijacking
Some common AWS services to protect against account hijacking are as follows:

Use AWS IAM to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use AWS IAM Access Analyzer to detect users who haven't used their accounts for a long time.
Use AWS Directory Service to configure who can authenticate and access your legacy (Kerberos-based) servers and applications and to enforce password policies.
Enforce the use of MFA to avoid the successful use of your users' credentials to access your applications and systems.
Use Amazon GuardDuty to detect account compromise.
Use AWS CloudTrail to detect API activities such as failed login attempts.
Use AWS Backup to recover your cloud environment after an account is hijacked.
Common Azure services to assist in the detection and mitigation of account hijacking
Some common Azure services to protect against account hijacking are as follows:

Use Azure AD to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use Azure AD Domain Services to configure who can authenticate and access your legacy (Kerberos-based) servers and applications, resources, and data, and use it to enforce password policies.
Enforce the use of MFA to avoid the successful use of your users' credentials to access your applications and systems.
Use Azure AD Conditional Access to enforce different levels of access and different authentication methods when users are connecting from the corporate network versus an unknown IP address.
Use Azure PIM to restrict users' permissions to your Azure resources.
Enable Azure AD audit logs and use Azure Log Analytics to detect activities such as failed login attempts.
Use Azure Information Protection to detect authentication failure events.
Use Azure Sentinel to correlate logs from multiple log sources to detect failed login attempts.
Use Azure Backup to recover your cloud environment after an account is hijacked.
Common GCP services to assist in the detection and mitigation of account hijacking
Here are some GCP services that can protect against account hijacking:

Use Google Cloud IAM to configure who can authenticate and access your applications, resources, and data and to enforce password policies.
Use the Google Managed Service for Microsoft Active Directory to configure who can authenticate and access your legacy (Kerberos-based) servers and applications, resources, and data, and use it to enforce password policies.
Enforce the use of MFA to avoid the successful use of your users' credentials to access your applications and systems.
Use Google Cloud Logging to detect activities such as failed login attempts.
Use Google Cloud Security Command Center to correlate logs from multiple log sources to detect failed login attempts.
For more information, refer to the following resources:

CLOUD-JACKING: AN EVOLVING AND DANGEROUS CYBERSECURITY THREAT:

https://techgenix.com/cloud-jacking/

Prevent cloud account hijacking with 3 key strategies:

https://searchcloudsecurity.techtarget.com/tip/Prevent-cloud-account-hijacking-with-3-key-strategies

What Is Cloud Jacking? How to Keep Your Cloud-Stored Data Safe:

https://www.magnify247.com/cloud-jacking-keep-safe/

Detecting and mitigating insider threats in cloud services
Insider threat is a concept where an authorized employee (that is, an insider) performs an action (either maliciously or accidentally) that they are not supposed to. Some common consequences of insider threats are as follows:

Loss of data
Data leakage
System downtime
Loss of company reputation
Monetary loss due to lawsuits
Some common examples of insider threats are as follows:

An administrator clicks on a phishing email from an unknown source, and as a result, a file server gets infected by ransomware, and all the files are encrypted.
An employee with the privilege to access an accounting system leaves their laptop unattended and an unauthorized person takes over his laptop and steals customer data.
A sub-contractor with access to databases with customer email addresses exports customer data and sells it on the dark web.
An administrator with access to backup files decides to delete all backup files before leaving the organization out of spite.
Some best practices for detecting and mitigating insider threats in cloud environments are as follows:

Invest in background screening before hiring employees or sub-contractors.
Enforce the use of strong passwords (for example, by stipulating a minimum password length, minimum and maximum password age, password history, complex passwords, account lockout and release settings, and more).
Audit user actions and correlate their activities using an SIEM system that will allow you to detect anomalous behavior (such as user logins after working hours, users trying to access resources for the first time, and so on).
Follow the principle of least privilege when granting permissions to resources.
Follow the concept of segregation of duties to avoid single users having the privilege to conduct sensitive actions (such as a user with the permissions both to generate encryption keys and use encryption keys).
Enforce the use of MFA to minimize the risk of attackers taking control of an internal employee's account without the employee's knowledge to access internal systems and data.
Invest in employee awareness to allow all your employees to detect phishing attempts, avoid opening emails from unknown sources, avoid running unknown executables, and avoid plugging in removable media from unknown sources.
Invest in business continuity planning to prepare for recovery after a system is compromised (for example, rebuilding systems, recovering data from backups, changing credentials, and so on).
Encrypt sensitive customer data and make sure access to encryption keys is limited to authorized personnel only, with audits for the entire key encryption/decryption process.
Store backups off-site and audit all access to backups.
In the following section, we will review common services from AWS, Azure, and GCP that will allow you to detect and mitigate insider threats.

Common AWS services to assist in the detection and mitigation of insider threats
Here are some AWS services that can protect against insider threats:

Use Amazon GuardDuty to detect anomalous behavior across your accounts.
Use AWS CloudTrail to detect API activities such as authorized users accessing a system after working hours or performing excessive actions, such as multiple file downloads, large select actions from databases, and so on.
Use AWS KMS to encrypt your data and control who has access to the encryption keys.
Use AWS Secrets Manager to store secrets (for example, credentials, access keys, passwords, and so on) and control who has access to the secrets.
Once an account compromise is detected, be sure to replace credentials, secrets, and encryption keys as appropriate.
Common Azure services to assist in the detection and mitigation of insider threats
Here are some Azure services that can protect against insider threats:

Use Azure AD Conditional Access to enforce different access and authentication methods when users are connecting from the corporate network versus an unknown IP address.
Use Azure PIM to restrict users' permissions to your Azure resources.
Enable Azure AD audit logs and use Azure Log Analytics to detect activities such as failed login attempts.
Use Azure Sentinel to correlate logs from multiple log sources to detect activities such as authorized users accessing a system after working hours or performing excessive actions, such as multiple file downloads, large select actions from databases, and so on.
Use Azure Key Vault to encrypt your data and control who has access to the encryption keys.
Use Azure Key Vault to store secrets (for example, credentials, access keys, passwords, and so on) and control who has access to the secrets.
Once an account compromise is detected, replace credentials, secrets, and encryption keys as appropriate.
Common GCP services to assist in the detection and mitigation of insider threats
Here are some GCP services that can protect against insider threats:

Use Google Cloud Logging to detect activities such as failed login attempts.
Use Google Cloud Security Command Center to correlate logs from multiple log sources to detect failed login attempts.
Use GCP Cloud KMS to encrypt your data and control who has access to the encryption keys.
Use Google Secret Manager to store secrets (for example, credentials, access keys, passwords, and more) and control who has access to the secrets.
Once an account compromise is detected, replace credentials, secrets, and encryption keys as appropriate.
For more information, refer to the following resources:

Five Tips for Protecting Cloud Resources from Internal Threats:

https://morpheusdata.com/cloud-blog/five-tips-for-protecting-cloud-resources-from-internal-threats

Don't let insider threats rain on your cloud deployment:

https://www.synopsys.com/blogs/software-security/insider-threats-cloud/

6 Insider Cloud Security Threats to Look Out for in 2021:

https://n.gatlabs.com/blogpost/insider-cloud-security-threats-watch-out-for/

What is an Insider Threat?:

https://www.code42.com/glossary/what-is-insider-threat/

Detecting and mitigating insecure APIs in cloud services
In today's world, all modern developments are based on Application Programming Interfaces (APIs) to communicate between system components, mostly based on web services (using Simple Object Access Protocol (SOAP)) or REST APIs. The fact that APIs are publicly exposed makes them an easy target for attackers trying to access a system and cause damage. Some common consequences of insecure APIs are as follows:

Data breaches
Data leakage
Damage to data integrity
Denial of service
Some common examples of attacks exploiting insecure APIs are as follows:

Due to a lack of input validation, an attacker can misuse an exposed API and inject malicious code through the API into a backend database.
Due to a lack of input validation, an attacker can perform an SQL injection through an exposed API and exfiltrate customer data from a retail site.
Due to a lack of application access control mechanisms, an attacker can use an API to penetrate a cloud service by using a low-privilege account.
An attacker located an API key stored in an open source code repository and was able to run remote commands against an internal system, using the permissions that the API key had.
Here are some best practices for detecting and mitigating against insecure APIs in cloud environments:

Use a secure development life cycle: Embed this as part of your development process – this includes controls such as the following:
Authentication and authorization: Enforce who can access the API.
Input validation: Check and validate what strings and/or data can be inserted into the API.
Application layer attacks: Detect and mitigate attacks such as injection attacks, cross-site scripting, and so on.
Conduct code reviews for all your APIs.
Encrypt data in transit by default for all APIs.
Sign each message through the API using a cryptographic key to avoid data tampering or changes to data integrity.
Use a web application firewall (WAF) to protect against well-known application-layer attacks.
Use distributed denial of service (DDoS) protection services to protect the API service from denial-of-service attacks.
Use an XML gateway to protect the service against SOAP or REST API-based attacks.
Enforce a rate limit on the API to decrease the chance of automated attacks.
Limit the type of HTTP methods to the minimum required (for example, GET without POST or DELETE).
Audit the use of exposed APIs and the backend systems to detect anomalous behavior (such as brute force attacks or data exfiltration).
Perform schema validation at the server side to make sure only well-known field sizes, characters, or regular expressions can pass through the API.
In the following section, we will review common services from AWS, Azure, and GCP that will allow you to detect and mitigate insecure APIs.

Common AWS services to assist in the detection and mitigation of insecure APIs
Here are some AWS services that can provide protection against insecure APIs:

Use Amazon API Gateway to allow inbound access to APIs in your cloud environment.
Use AWS WAF to detect and protect against application-layer attacks.
Use AWS Shield to detect and protect against DDoS attacks.
Use AWS IAM to authorize access to APIs.
Use Amazon CloudWatch to detect spikes in API requests.
Use AWS CloudTrail to detect who can conduct API activity through the API gateway.
Use Amazon GuardDuty to detect potential hacking activities using your APIs.
Use AWS Secrets Manager to generate, store, and rotate API keys.
Common Azure services to assist in the detection and mitigation of insecure APIs
Here are some Azure services that can provide protection against insecure APIs:

Use Azure API Management to allow inbound access to APIs in your cloud environment.
Use Azure WAF to detect and protect against application-layer attacks.
Use Azure DDoS Protection to detect and protect against DDoS attacks.
Use Azure Active Directory to authorize access to APIs.
Use Azure Monitor to detect spikes in API requests.
Use Azure Key Vault to generate, store, and rotate API keys.
Use Azure Sentinel to correlate multiple data sources to assist in detecting potential attacks against APIs.
Common GCP services to assist in the detection and mitigation of insecure APIs
Here are some GCP services that can provide protection against insecure APIs:

Use Google API Gateway to allow inbound access to APIs in your cloud environment.
Use Google Cloud Armor to detect and protect against both application-layer attacks and DDoS attacks.
Use Google Cloud IAM to authorize access to APIs.
Use Google Cloud Audit Logs to monitor API Gateway activities.
For more information, refer to the following resources:

Insecure API Cloud Computing: The Causes and Solutions:

https://cybersecurityasean.com/expert-opinions-opinion-byline/insecure-api-cloud-computing-causes-and-solutions

API Security Top 10 2019:

https://owasp.org/www-project-api-security/

As API Threats Multiply, Cybersecurity Lags:

https://containerjournal.com/features/as-api-threats-multiply-cybersecurity-lags/

Detecting and mitigating the abuse of cloud services
The abuse of cloud services is about using the scale of the cloud provider's resources and the multi-tenancy architecture to conduct malicious activities. Some common consequences of the abuse of cloud services are as follows:

Loss of service availability due to DDoS attacks
Monetary loss due to the use of cloud resources being exploited for bitcoin mining without the customer's awareness
Some common examples of the abuse of cloud services are as follows:

Using the cloud to deploy multiple servers and conducting DDoS attacks
Using the cloud to deploy multiple expensive servers for bitcoin mining
Using the cloud to spread email spam and phishing attacks
Using the cloud for brute force attacks on passwords
Some best practices for detecting and mitigating against the abuse of cloud services are as follows:

Configure billing alerts to get notified in advance about any increase in resource consumption.
Follow the concept of segregation of duties to avoid single users having the privileges to conduct damaging actions (such as a user with the permissions both to deploy an expensive virtual machine and to log in to the machine for ongoing maintenance).
Use access control lists and set network/firewall rules to configure who can access your resources (for both inbound and outbound network traffic).
Use IAM to control who has access to your cloud environments.
Rotate credentials to avoid misuse.
Use audit trails to allow you to monitor the access of resources and the actions carried out.
Use DDoS protection services to protect your cloud environment from denial-of-service attacks.
Use WAF services to detect and protect against application-layer attacks.
Invest in employee awareness regarding the cloud provider's terms of acceptable use.
Common AWS services to assist in the detection and mitigation of the abuse of cloud services
Here are some common AWS services that can protect against the abuse of cloud services:

Use Amazon CloudWatch to configure billing alerts and get notifications when certain thresholds have been passed.
Use AWS IAM to configure who can authenticate and access your applications, resources, and data.
Use AWS Config to detect configuration changes in your environment and cloud resources.
Use AWS WAF to detect and protect against application-layer attacks.
Use AWS Shield to detect and protect against DDoS attacks.
Use AWS CloudTrail to detect API activities (for users, computers, service accounts, and others) that might indicate the misuse of resources in your cloud environment.
Use Amazon GuardDuty to detect any anomalous behavior across your cloud resources (such as bitcoin mining).
Use Amazon VPC controls (for example, network ACLs and security groups) and AWS Network Firewall to configure inbound and outbound network access rules.
Use AWS Systems Manager Patch Manager to automatically deploy security patches for servers in your cloud environment.
Common Azure services to assist in the detection and mitigation of the abuse of cloud services
Here are some common Azure services that can protect against the abuse of cloud services:

Use Azure budgets to configure billing alerts and get notifications when certain thresholds have been passed.
Use Azure AD to configure who can authenticate and access your applications, resources, and data.
Use Azure Monitor to detect activities (for users, computers, service accounts, and others) that might indicate the misuse of resources in your cloud environment.
Use Microsoft Defender for Cloud to detect and send alerts about possible misuse of resources in your cloud environment.
Use Azure WAF to detect and protect against application-layer attacks.
Use Azure DDoS Protection to detect and protect against DDoS attacks.
Use Azure NSGs to configure inbound and outbound network access rules.
Use Azure Customer Lockbox to detect login attempts by Microsoft support engineers.
Use Azure Update Management to automatically deploy security patches for servers in your cloud environment.
Common GCP services to assist in the detection and mitigation of the abuse of cloud services
Here are some common GCP services that can protect against the abuse of cloud services:

Use GCP Billing budgets to configure billing alerts and get notifications when certain thresholds have been passed.
Use Google Cloud IAM to configure who can authenticate and access your applications, resources, and data.
Use Google Cloud Logging to detect suspicious activities that might indicate the misuse of resources in your cloud environment.
Use Google Cloud Armor to detect and protect against both application layer and DDoS attacks.
Use Google Cloud Security Command Center to correlate multiple data sources to assist in detecting the misuse of resources in your cloud environment.
Use GCP VPC firewall rules to configure inbound and outbound network access rules.
Use Google Access Transparency and Access Approval to detect login attempts by Google support engineers.
Use Google OS patch management to automatically deploy security patches for servers in your cloud environment.
For more information, refer to the following resources:

Abuse in the Cloud:

https://cloudsecurityalliance.org/blog/2021/02/12/abuse-in-the-cloud/

Abusing cloud services to fly under the radar:

https://research.nccgroup.com/2021/01/12/abusing-cloud-services-to-fly-under-the-radar/

Summary
In this chapter, we focused on common security threats to cloud services.

For each of the identified threats, we reviewed potential consequences of the threat, a common example of the threat, and the best practices to detect and mitigate the threat, and after that, we reviewed the built-in services from AWS, Azure, and GCP that allow you to protect your cloud environment.

Knowing the most common threats you face when using cloud services and the various built-in cloud service capabilities will allow you to better protect your cloud environment.

In the next chapter, we will review compliance standards for cloud security (such as ISO 27001, Security Operations Centre (SOC), Cloud Security Alliance (CSA) Star, and more) and the European GDPR privacy regulation, the PCI DSS, and the HIPAA laws.