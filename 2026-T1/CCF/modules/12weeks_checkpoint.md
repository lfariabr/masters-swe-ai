# CCF501 Weeks 1-12 Checkpoint (30 MCQs)

## Purpose
This checkpoint tests full-subject revision across Modules 1-12 and the three assessment threads:
cloud fundamentals, deployment and service model selection, provider comparison, case-study analysis,
governance, legal obligations, security threats, and security policy implementation.

## Coverage Map
| Questions | Coverage |
| --- | --- |
| 1-2 | Module 1 - Traditional vs modern/cloud computing |
| 3-4 | Module 2 - Essentials and NIST characteristics |
| 5-6 | Module 3 - Deployment models and VPCs |
| 7-8 | Module 4 - Service models |
| 9-10 | Module 5 - Major cloud providers and comparison |
| 11-12 | Module 6 - Advanced cloud models and concepts |
| 13-14 | Module 7 - Deployment model key considerations |
| 15-16 | Module 8 - Deployment case studies and EC2 |
| 17-18 | Module 9 - Governance and legal obligations |
| 19-20 | Module 10 - Security threats and mitigation |
| 21-22 | Module 11 - Security policy planning and management |
| 23-24 | Module 12 - Security policy implementation |
| 25-30 | Assessment 1-3 and capstone integration |

## Instructions
- Answer all 30 multiple-choice questions.
- Choose one answer only for each question (A-D).
- Do not check the answer key until you finish.
- Score 1 mark per correct answer (total = 30).

## My responses
1 - B; 2 - B; 3 - C; 4 - B; 5 - A; 6 - B; 7 - B; 8 - C; 9 - C; 10 - B; 11 - B; 12 - A; 13 - B; 14 - C; 15 - B; 16 - A; 17 - A; 18 - B; 19 - A; 20 - C; 21 - B, 22 - A; 23 - A, 24 - B; 25 - B; 26 - B; 27 - B; 28 - C; 29 - A; 30 - B

*Score: 28/30*

---

### 1) Which statement best distinguishes cloud computing from traditional on-premises infrastructure?
A. Cloud computing removes the need for networking and security controls  
B. Cloud computing delivers pooled, provider-managed resources over the internet with elastic usage  
C. Traditional infrastructure always has lower total cost of ownership  
D. Traditional infrastructure automatically scales across regions without extra planning  

### 2) In capacity planning, what is the main problem with over-provisioning?
A. It prevents any future migration to cloud  
B. It wastes resources and increases operating inefficiency  
C. It removes the need for governance  
D. It guarantees higher application availability in every case  

### 3) Which NIST essential characteristic lets customers provision computing resources automatically without human interaction from the provider?
A. Broad network access  
B. Measured service  
C. On-demand self-service  
D. Resource pooling  

### 4) Which NIST characteristic best supports billing transparency, usage tracking, and chargeback/showback?
A. Rapid elasticity  
B. Measured service  
C. Broad network access  
D. Multi-tenancy  

### 5) Which deployment model is shared by organisations with common requirements, such as similar compliance or security needs?
A. Public cloud  
B. Private cloud  
C. Community cloud  
D. Single-tenant SaaS  

### 6) What is the most accurate description of a VPC?
A. A fully private data centre owned by the customer  
B. A logically isolated environment on shared public cloud infrastructure  
C. A SaaS-only environment with no network controls  
D. A physical rack reserved permanently for one customer  

### 7) A team wants to deploy custom applications but avoid managing the operating system, middleware, runtime, and infrastructure. Which service model best fits?
A. IaaS  
B. PaaS  
C. SaaS  
D. Community cloud  

### 8) Which service model usually leaves the most management responsibility with the customer?
A. SaaS  
B. PaaS  
C. IaaS  
D. FaaS  

### 9) What is the strongest provider-selection principle from the AWS/Azure/GCP comparison work?
A. AWS, Azure, and GCP are interchangeable for all workloads  
B. The cheapest provider is always the best strategic choice  
C. Provider selection should be based on workload fit, skills, ecosystem, services, cost, and governance needs  
D. A business should choose the provider with the most services even if those services are irrelevant  

### 10) In the provider case-study notes, why is a blended architecture such as EC2 plus RDS, S3, CloudFront, and SES more accurate than calling the whole solution "pure IaaS"?
A. Cloud services never map to IaaS, PaaS, or SaaS categories  
B. Real cloud architectures often combine infrastructure services with managed platform services  
C. EC2 is a SaaS product  
D. RDS and S3 require the customer to manage physical servers  

### 11) What does serverless computing primarily change for developers and operators?
A. It removes all code execution from the cloud  
B. It dynamically provisions and deprovisions infrastructure so teams focus more on functions/events than servers  
C. It guarantees no security responsibilities remain for the customer  
D. It requires fixed-capacity virtual machines for every workload  

### 12) What is the best distinction between edge computing and fog computing?
A. Edge pushes computation closer to devices; fog adds a distributed layer between devices and central cloud  
B. Edge is only for SaaS; fog is only for IaaS  
C. Edge always means private cloud; fog always means public cloud  
D. Edge removes the need for networking; fog removes the need for storage  

### 13) What is the key difference between hybrid cloud and multicloud?
A. Hybrid cloud uses only SaaS; multicloud uses only IaaS  
B. Hybrid cloud integrates public and private environments; multicloud uses services from multiple cloud providers  
C. Hybrid cloud is always cheaper than multicloud  
D. Multicloud requires all workloads to run in one region  

### 14) A regulated organisation wants sensitive data under strict control, but also wants elastic capacity for variable workloads. Which deployment strategy is usually the best fit?
A. Public cloud only  
B. Private cloud only  
C. Hybrid cloud  
D. No cloud adoption  

### 15) What lesson did the Twitter ad engagement analytics case show?
A. Migration should always move every layer at once  
B. Cloud migration can improve performance when storage, serving, and processing services are selected for the workload  
C. Homegrown systems are always faster than managed cloud services  
D. Analytics workloads cannot use cloud-native services  

### 16) Which EC2 pricing model is best suited for interruption-tolerant workloads that can tolerate capacity being reclaimed?
A. On-demand instances  
B. Reserved instances  
C. Spot instances  
D. Dedicated hosts only  

### 17) In the Australian legal-obligations material, which two laws were highlighted as especially relevant to cloud providers and consumers?
A. Privacy Act 1988 and Australian Consumer Law  
B. Copyright Act and Corporations Act only  
C. Freedom of Information Act and Spam Act only  
D. Tax law and employment law only  

### 18) What was the main shared-responsibility lesson from the FlexBooker exposed S3 bucket case?
A. AWS is responsible for every customer bucket configuration  
B. Customer-side cloud misconfiguration can expose data even when the provider infrastructure is secure  
C. Object storage cannot be secured  
D. Encryption is unnecessary if a bucket is in the cloud  

### 19) Which group best matches common cloud security threats from Module 10?
A. Human error, misconfiguration, credential theft, API attacks, and data exfiltration  
B. Only physical server theft and power outages  
C. Printer failure, local disk fragmentation, and desktop monitor damage  
D. Governance documentation, training, and audit logs  

### 20) What is the recommended principle for an AWS root account?
A. Use it for daily development because it has full access  
B. Share it with administrators to reduce IAM complexity  
C. Protect it with MFA and reserve it for setup, billing, and exceptional account-level tasks  
D. Store its access keys in application code for convenience  

### 21) What is the main advantage of a classification-based cloud security policy?
A. It applies identical controls to every data type regardless of sensitivity  
B. It scales controls according to sensitivity tiers and business risk  
C. It removes the need for compliance mapping  
D. It works only in private cloud environments  

### 22) What is the best distinction between a control and a guardrail?
A. A control addresses a risk; a guardrail proactively prevents unsafe actions from occurring  
B. A guardrail is always manual; a control is always automated  
C. Controls are only legal documents; guardrails are only training slides  
D. There is no difference  

### 23) Which pairing is correct for AWS security policy implementation?
A. AWS Shield protects against infrastructure-layer DDoS attacks; AWS WAF filters application-layer HTTP/S requests  
B. AWS Shield manages relational databases; AWS WAF provisions virtual machines  
C. AWS WAF replaces IAM; AWS Shield replaces encryption  
D. AWS Shield is only for SaaS apps; AWS WAF is only for billing controls  

### 24) What is the correct high-level order of the NIST Risk Management Framework cycle?
A. Monitor, Authorise, Assess, Implement, Select, Categorise  
B. Categorise, Select, Implement, Assess, Authorise, Monitor  
C. Select, Categorise, Monitor, Authorise, Implement, Assess  
D. Assess, Implement, Categorise, Monitor, Select, Authorise  

### 25) For Assessment 1's ABC Enterprise scenario, which recommendation logic best fits the report direction?
A. Avoid cloud because start-ups should always buy fixed hardware first  
B. Use cloud to support automation through elastic scaling, managed services, and pay-as-you-grow cost alignment  
C. Use SaaS only and avoid all architecture design  
D. Select a provider before considering workload, cost, or security requirements  

### 26) What was the strongest cross-case lesson from Assessment 2?
A. One cloud provider and one service model should be recommended for every organisation  
B. Service and deployment model choices depend on business context, constraints, existing systems, and desired outcomes  
C. Public cloud always removes the need for governance  
D. Case studies should ignore deployment models and discuss only brand names  

### 27) Which set best describes the Assessment 3 Apache Superset deployment artefact?
A. A local-only spreadsheet with no cloud infrastructure  
B. Apache Superset deployed on cloud infrastructure with networking, security rules, Docker/runtime evidence, and RBAC/dashboard proof  
C. A SaaS subscription with no deployment steps  
D. A private data centre migration with no public cloud provider  

### 28) Which statement best captures the shared responsibility model across the subject?
A. The cloud provider owns all security duties once data enters the cloud  
B. The customer owns all physical data centre security duties  
C. The provider secures the underlying cloud infrastructure, while the customer remains responsible for data, identities, configurations, and application-level decisions  
D. Shared responsibility applies only to SaaS  

### 29) Which governance action should happen before and after cloud migration?
A. Inventory data, define policies/contracts, map compliance obligations, then continuously monitor and improve  
B. Move workloads first and document risks only if a breach occurs  
C. Give every user administrator access to speed up adoption  
D. Disable audit logs to reduce storage cost  

### 30) Which capstone statement best represents CCF501's full subject arc?
A. Cloud computing is mainly about cheaper servers and removes the need for governance  
B. Cloud value comes from elastic resources, managed services, provider fit, secure deployment, and continuous governance/security policy  
C. Cloud adoption is complete once a VM is running  
D. Security policy is separate from cloud architecture and should be handled only after incidents  

---

## Answer Key
1. B - Cloud is defined by pooled, network-accessible, elastic, provider-managed resources.  
2. B - Over-provisioning wastes paid-for capacity and creates inefficiency.  
3. C - On-demand self-service is automatic provisioning without provider human interaction.  
4. B - Measured service enables usage monitoring and transparent billing.  
5. C - Community cloud serves groups with shared concerns or compliance needs.  
6. B - A VPC gives logical isolation on shared public cloud infrastructure.  
7. B - PaaS lets the customer focus on application/data while the provider manages the platform.  
8. C - IaaS leaves the customer responsible for more configuration and operations than PaaS or SaaS.  
9. C - Provider fit is contextual, not universal.  
10. B - Real cloud solutions commonly mix IaaS and managed platform services.  
11. B - Serverless abstracts server provisioning around events/functions.  
12. A - Edge is close to devices; fog is a distributed intermediary layer.  
13. B - Hybrid integrates public/private; multicloud uses multiple CSPs.  
14. C - Hybrid cloud balances control with burst/elastic capacity.  
15. B - The Twitter case showed performance gains through appropriate managed cloud services.  
16. C - Spot instances suit interruption-tolerant workloads.  
17. A - The notes highlighted the Privacy Act 1988 and Australian Consumer Law.  
18. B - Misconfigured customer resources can expose data under shared responsibility.  
19. A - These are core cloud threat categories from Module 10.  
20. C - Root should be locked down and used only for exceptional account-level tasks.  
21. B - Classification-based policy scales controls to data sensitivity and risk.  
22. A - Controls address risk; guardrails prevent unsafe actions up front.  
23. A - Shield handles DDoS at L3/L4; WAF handles L7 HTTP/S filtering.  
24. B - NIST RMF: Categorise, Select, Implement, Assess, Authorise, Monitor.  
25. B - Assessment 1 centred cloud value for ABC around automation, elasticity, and cost alignment.  
26. B - Assessment 2 required context-based service/deployment model analysis.  
27. B - Assessment 3 evidenced a real cloud deployment with infrastructure, security, runtime, and app proof.  
28. C - Providers and customers split responsibilities across infrastructure, data, identity, configuration, and apps.  
29. A - Governance is lifecycle work: plan, contract, comply, monitor, improve.  
30. B - The subject combines cloud fundamentals, architecture, provider selection, deployment, security, and governance.

## Score Interpretation
- 0-14: Early revision stage; rebuild the core definitions, NIST characteristics, and service/deployment model comparisons.
- 15-22: Developing; strengthen applied scenario reasoning, provider selection, and security/governance links.
- 23-27: Strong; review the modules where you missed marks and practise explaining answers in assessment language.
- 28-30: Final-checkpoint ready; focus on concise justification and cross-module synthesis.
