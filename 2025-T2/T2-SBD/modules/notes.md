# Notes for SBD403

## Module 1 - Introduction to Secure by Design: Terminology and Basic Concepts
**CIA Triad**
- **Confidentiality** refers to ensuring that information isn’t disclosed or in any other way made available to unauthorized entities (including people, organizations, or computer processes).
- **Integrity** refers to ensuring that data is both accurate and complete.
- **Availability** refers to ensuring that information, the systems used to store and process it, the communication mechanisms used to access and relay it, and all associated security controls function correctly to meet some specific benchmark.

## Takeways:
- https://dev.to/sotergreco/understanding-jwt-basics-of-authentication-and-algorithms-37k2
- https://security.stackexchange.com/questions/180208/what-is-the-difference-between-jwt-and-encrypting-some-json-manually-with-aes


## Questions for Dr. Tanvir Rahman:
- n/a

## Follow up

---

## Module 2 - Introduction to Cyber-Security Procedures and Risk Management

Expected learning outcomes
1. cybersecurity risks 
2. threats, vulnerabilities and assets
3. methods to assess risks
4. the 5 phases of risk management process
5. DREAD model (risk management framework)

**Cybersecurity Risk**
risk is the possibility of loss, damage or harm due to a cyber threat
risk = (likelihood of threat * impact) - mitigation efforts

**Threats**
a threat is an event or action that has the potential to cause harm or loss to an asset or system.

**Vulnerabilities**
a vulnerability is a weakness in a system or application that can be exploited by an attacker to gain unauthorized access or cause damage.

**Assets**
an asset is anything of value that is protected by cybersecurity measures.

**Methods to Assess Risks**
Risk Level Formula
A company is assessing the risk of a server breach
Likelihood Factor (LF): 0.2 (means the breach is expected to occur once every 5 years)
Loss Magnitue (LM): $100.000 (this is the estimated cost of the breach)
Risk: 0.2 * $100.000 = $20.000

key componentes in qualitative risk assessment
identify assets
identify threats
estimate likelihood
estimate impact
determine risk

qualitative risk matrix

|      | Impact: Low | Impact: Medium | Impact: High |
|----- |-----------|----------------|------------|
| Likelihood: Low | Medium | High | Critical |
| Likelihood: Medium | Low | Medium | High |
| Likelihood: High | Low | Low | Medium |

single loss expectancy (SLE) = asset value * exposure factor
annual loss expectancy (ALE) = SLE * frequency

**The 5 phases of risk management process**

step 1: context establishment
- define the scope and boundaries
- identify stakeholders + requirements
- establish risk criteria and evaluation metrics
- setting objectives for risks mgmt process

step 2: risk identification
- discovering and doc potential risks
- methods include: brainstorm, checklist, historical incident analysis, threat modeling
- output: comprehensive list of identified risks

step 3: risk analysis
- determining likelihood and impact of each risk
- calculating risk level using established formulas
- considering existing controls and their effectiveness
- priority risks for further evaluation

step 4: risk evaluation

step 5: risk treatment

finally... Risk Management Documentation

**DREAD Threat Assessment Model**

Framework developed by microsoft for consistent threat assessment
quantify, compare and prioritize risk of security threats

D -> Damage: how bad would an attack be?
    1. severity of attack's impact
    2. how bad could it get if vulnerability is exploited
    3. considers data loss, financial loss, reputational damage, etc.
R -> Reproducibility: how easy is it to reproduce the attack?
    1. how consistently can the attack be replicated
    2. is the attack reliable or requires specific conditions?
E -> Exploitability: how easy is it to exploit the attack?
    1. effort and expertise required to exploit vulnerability
    2. what resources, skills or tools are needed?
A -> Accessibility: how accessible is the target?
    1. scale of potential impact accros user population
    2. % of users would be affected?
D -> Discoverability: how discoverable is the target?
    1. how easily the vulnerability can be detected
    2. can attackers easily find the vulnerability?

> high score (8-10): catastrophic loss
> low score (1-3): minor loss

Sample case: 
SQL INjection vulnerabity in login form
D(8) + R(9) + E(8) + A(8) + D(8) = **40/5** = **8 (high severity)**

**Risk management in practice**

- regular risk assessment (quarterly or after significant changes)
- security awareness training for all employees
- penetration testing and vulnerability scanning
- compliance with industry regulations and standards
- executive involvement in risk management decisions

## Module 3 - Introduction to Cyber-Security Methods

### Common Technical measures:
1. Firewall: filter traffic, block threats
2. Anti-virus: detect and remove harmful software
3. Access control: determine who can access what
4. Encryption: secure data during storage and transmission
5. Back up systems: provide recovery in case of data loss

### When Good measures backfire
Example: Disabling all internet access except during business hours
White it may stop external attacks, it disrupts email, research and collaboration
Security is important, but if users can't do their job, the system fails

### The Human Factor
1. Users may struggle with or ignore inconvenient controls
2. Complex password rules often lead to users writing them down
3. Poor usability leads to non-compliance or workarounds - and ultimately, insecurity
4. Human-centered design is essential

### CIA and IAM
**CIA**: Confidentiality, Integrity, Availability
**IAM**: Identity and Access Management

Five A's:
Authentication: verifies user identify (passwords, biometrics, MFA)
Authorization: grants access based on roles/privileges
Administration: managers user roles, permissions, credetials
Audit: records activity logs for accountabilities
Analytics: Identifies unusual patterns or access violations

> *Insight: when there's a mismatch on the behavior of users of the system, can we think about an algorithm that maps that and prompts the user to take action, like scan fingerprint or face?*

### What to do in order to keep on top of security:
Patch and Update Management
Back up and Recovery

### Physical Security Measures
- Restrict access to server rooms, endpoints and sensitive areas
- Use security cameras, access logs and lockable cabinets
- Example: locking down usb ports to prevent data theft from public kiosks
- Physical control are often the first and last line of defence

### Challenges in Org Security
Resistance rom departments due to perceived complexity
Budget limitations and lack of exec support
Lack of clarity in roles and responsibilities

Example: overlap in IT and security response causes delay
Solutions: Awareness campaigns, governance alignment and automation

### Key Takeaways
Technical countermeasures reduce risk but must fit the business context
The CIA triad is central to evaluating control effectiveness
IAM structures access and prevents abuse
Balance is needed between strict controls and operational efficiency
Strategy, training and planning are as important as tools

## Module 4 - Common Threats and Attacks

### Section I: Intro and remembering concepts
Threat: potential cause of unwanted incident resulting in harm to a system or organization
Vulnerability: weakness in the system, process or design that can be exploited by an attacker
Attack: vulnerability acted by threat actor exploiting vulnerabilities

The relationship: actor exploits vulnerability and attack.

### Section II: understanding the attacker
Motive: reason for the attack (money, revenge, politics)
Means: skills and tools necessary to conduct the attack
Method: plan for how the attack will be carried out from reckon to execution

Attacker type: 
**External**
- script kiddies: inexperienced attackeds with pre-made tools from internet
- hacktivists: motivated by political or social cause
- lone wolves: individuals who develop skills over time
- organized criminals: groups motivated by financial gain

**Internal**
- unintentional insider: accidentaly causer of breach through negligence, lack of awareness...
- malicious insider: unhappy or compromised employee who steals data, disrupts sytems

### Section III: common types of attacks
1. Malicious software
    - Malware (malicious software)
        - Spyware: steals data, tracks user activity
        - Ransomware: encrypts data and demands payment
        - Trojan: disguises as legitimate software
        - Virus: corrupts files, damage system
        - Worm: spreads without any hosts
2. Human target (social engineering - psychological manipulation)
    - Phishing: deceives users into disclosing sensitive information
    - Spear phishing: targets specific individuals
    - Whaling: targets high-value targets
    - Pretexting: creates false scenarios to deceive users
3. Network & connectivity attacks
    - DDoS: Distributed Denial of Service
    - Man in the middle: intercepts and modifies communication
4. Application and Software vulnerabilities
    - SQL Injection: attacks on databases
        * send query to sql -> 
        * stored procedure -> next time, call the query and pass the parameter, no raw-queries
        * pre compiled queries is fast and experienced
    - XSS (Cross-Site Scripting)
        - injection attack where attacker injects malicious scripts (usually JavaScript) into a trusted website

### Section IV: Takeways
1. Multiple Attack vectors exist - there's no single solution in cybersecurity
2. Humans are the biggest risk - training and awareness are critical
3. Assessment and Prioritization matter - use CVSS to focus efforts
4. Proactive defense works best - understand attackers

## Module 5 - Architecture Integration with IT Systems

### Learning objectives
- Right tool for the job
- User impact by examining security measures and their effects on user experience
- Foundational security methods: firewalls and access controls
- Modern challenges: security in complex environments like public cloud and threat of advanced malware
- Culture/compliance: user training, legal frameworks (GDPR)

### Section I: Architectural Integration
- Refers to embedding security mechanisms across hardware, software and user layers
- Involve mapping business objectives with appropriate security models
- Promotos e2e protection from data input to transmission and storage
- Integration that ensures risk management and controls are consistent

### Section II: User impact
- Security measures can have a significant impact on user experience
- If systems are too complex, users may resist or bypass security controls

Context matters!

### Section III: IT Infrastructure protection
Networks, servers, storage, control systems!
- Firewalls and network segmentation
- Access control and identity management
- Encryption and data protection
- Monitoring and incident response integration

### Section IV: Diverse computing environments
- Modern IT involves multi-cloud, on-premises and hybtid systems
- Each has its own security challenges and requirements

### Section V: Regulatory and Compliance
- GDPR, HIPAA, PCI-DSS, ISO 27001

### Key takeways
- Always analyze impact of security measure
- Master the fundamentals (firewall, access controls)
- Embrace shared responsibility, with provider
- Think like an attacker: understand threats and constantly update defenses
- Build human firewall: training and awareness

## Module 6 - IT System Security Assessment

### Expected Learning Outcomes
- Explain what cybersecurity risk is and how it arises from threats and vulnerabilities
- Differentiate between threats, vulnerabilities, and attacks in a risk context
- Qualitative vs Quantitative methods
- Five phases of risk assessment
- Compliance and professional requirements

#### What is risk
possibility of loss, damage, harm due to a cyber threat

##### Componentes of risk
- Assets: what needs protection (data, systems, people, software, customer satisfaction, brand acceptance on the marke, human resources, intellectual property, etc.)
- Threats: possible dangers (malware, phishing, social engineering, insider threats)
- Vulnerabilities: weaknesses in security (unpatched software, weak passwords, loopholes intentional or accidental)

##### Small parenthesis
- Coding is an art of craftsmanship
- Even with all that liberty, **clean code** principles remain
- Technology is moving VERY fast: from cinema, to now where we record in HQ, and how about in the future? If we don't keep up, we'll be left behind.

#### Risk Assessment formula
Risk = Likelihood * Impact

- What is likehlihood: Probability or chance that a specific threat will exploit a vulnerability
- What it measures: 
- What is loss magnitude: When a threat exploits a vulnerability, what is the impact?

##### Qualitative vs Quantitative methods
- Qualitative: deal with words, high, less, etc.
- Quantitative: deal with numbers, numerical data  (I don't think I have this on my assessment right now, it would be interesting to add for coverage - also check if we have all key components )

#### Risk Management Process
- Five phases of risk assessment
    - Step 1: Context Establishment
        - define scope/boundaries
        - identify stakeholders + requirements
    - Step 2: Identify the risk
        - discovering and documenting potential risks
        - methods include: brainstorming, checklists, historial incident, threat modeling (maybe add reference of book describing sorts of attacks)
    - Step 3: Risk analysis
        - likeholihood
        - risk. lvls using formulas
        - ...
    - Step 4: Risk evaluation
        - comparing analyzed risks against criteria
        - determining which risks require treatment
        - setting priorities
    - Step 5: Risk treatment
        - selecting appropriate risk treatment strategies
        - implementing controls
        - monitoring and reviewing
    - Step 6: Risk reporting
        - communicating findings to stakeholders
        - documenting risk assessment process
            incident response
            disaster recovery
            business continuity
            documents requiring regular testing and updates
        - maintaining records of risk assessment

#### DREAD framework
- Function: A method to rate the potential severity of a threat. 
- Categories: Uses five categories, each scored typically on a scale of 0–10. 
    - Damage Potential: How much harm an attack can cause. 
    - Reproducibility: How easy it is to reproduce an attack. 
    - Exploitability: How easy it is to launch an attack. 
    - Affected Users: The number of users who would be impacted. 
    - Discoverability: How easy it is to find the vulnerability. 
- Goal: To prioritize which risks to address first by calculating an overall risk score from the sum of the category scores. 
- O

#### OCTAVE
...

### Compliance requirements
- GDPR

## Module 7 - Secure Failure
> How to manage cyber incidents?

### Learning objectives
- understand principles and stages of incident reponse
- identify key elements that make incident response plan effective
- evaluate strategies to detect, contain and recover from incidents
- apply governance standars to improve org cybersecurity resilience

### Section I: Mindset / Technical prepardness
1. shift from if to when, assuming incidents will occur
2. staff awareness and readiness are as important as technology (Proactive culture)
3. regularly rehearse responses to != attack types (scenario planning)
4. ensure tools are available and staff are trained (Preparedness)

#### Key questions before incident
- How to detect suspicious activity?
- Who is in charge of incident response?
- How to recover from the incident?
- How to report the incident?

#### Technical preparation
- IDS - Intrusion Detection System
- Log management, centralized storage for investigation
- Access control: limit user privileges to reduce breach impact
- Backups: regular, tested and stored securely

### Section II: basics of incident response
1. Preparation - tools, policies, training BEFORE incidents
2. Detection & Analysis - identify and confirm incident quickly
3. Containment - stop the spread without shutting down unnecessarily
4. Eradication & Recovery - remove the threat and restore normal operations
5. Post-incident analysis - learn and improve from the incident

### Section III: crafting an IRP
1. Define scope and objectives: define incidentes covered
2. Identify key stakeholders: assign named contacts
3. Incident categories: define types of incidents
4. Response phases: define stages of response

#### Maintaining and testing IRP
- Regular updates
- Testing and drills
- Documentation
- Training

### Section IV: Building long term cybersecurity resilience
- organizational radiness beyond IRP
    - security awareness training
    - threat intelligence integration
    - vendor management (partners meet security criteria)
    - continuous monitoring detecting threats early
- linking incident response to governance
    - Framework alignment: ISO 27001, NIST or CIS controls
- measuring incident response effectiveness
    - metrics and KPIs
    - incident response metrics

### Key takeaways
- **Prepardness reduce chaos**: Planning ahead saves time and resources
- **Roles must be clear**: Avoid confusing when every second counts
- **Communication is clear**: Keep all stakeholders informed appropriately
- **Learning never stops**: Update plans and training regularly

## Module 8 - Domain Driven Design

### Section I - Introduction to Secure Software
Software is a critical component of any modern IT system, holding data and executing business logic.

- hardware: physical components that can be touched 
- software: electronic instructions that tell hardware what to do
- firmware: specific software embedded in hardware to provide basic functionality
- driver: software that allows hardware to communicate with the operating system (glue between hardware and OS)

Overview of common vulnerabilities:
- common and high-impact attacks are possible because of insecure coding practices
- insecure coding practices lead to vulnerabilities that attackers can exploit
- two of the most common are buffer overflows and code injection

#### Deep Dive on Buffer Overflow
It exploits a lack of boundary checks in a software system. Since a program allocates a specific amount of memory to store data, if the program doesn't properly check the boundaries of that memory allocation, an attacker can write data beyond the allocated space, potentially overwriting other variables or even executable code.

#### Deep Dive on Code Injection
Code injection occurs when an attacker inserts malicious code into an application, which is then executed by the system. This can happen when user input is directly used in commands or queries without proper validation or sanitization. Common types include SQL injection, command injection, and script injection.

**The solution: security by design**

### Section II - Building Security In
- Touchpoint 1&2, Planning and Designing: Abuse cases with hacker motives, potential solutions, focusing on bad points
- Touchpoint 3, Architectural Risk Analysis: Identify and mitigate architectural risks that could lead to security breaches
- Touchpoint 4, Code Review: Implement security checks in code reviews to catch vulnerabilities early (Static Analysis Security Tools - SAST)
- Touchpoints 5&6, Security Testing: Implement dynamic analysis (DAST) and penetration testing to find runtime vulnerabilities
    - Risk based security testing: Prioritize testing based on threat and impact assessment
    - Penetration testing: Simulate real attacks to find vulnerabilities
- Touchpoint 7, Security Operations: Implement continuous monitoring, incident response, and security analytics to detect and respond to threats in real-time

### Section III - Application Web Security
- OWASP Top 10: Common web application vulnerabilities (Injection, XSS, CSRF, etc.)
1. Broken Access Control: failing to enforce what authenticated users are allowed to do
    - Ex: an user changing the ID in a URL to see another user's data
2. Cryptographic Failures: weak encryption, poor key management, insecure data storage
    - Ex: storing passwords in plain text
3. Injection: SQL, NoSQL, OS, LDAP injection attacks
    - Ex: SQL injection by manipulating input fields, Cross-Site Scripting (XSS)
4. Insecure Design: a category focusing on flawed security architecture and design decisions
    - Ex: a system designed without threat modeling, lacks rate-limiting, making it vulnerable to brute force attacks
5. Security Misconfiguration: failing to implement all security controls properly
    - Ex: leaving default usernames/passwords or leaving cloud storage (S3) publicly accessible
6. Vulnerable and Outdated Components: using libraries with known vulnerabilities
    - Ex: running a website on an old version of Wordpress with known vulnerabilities
7. Idenfication and Authentication Failures: weak identification and authentication mechanisms
    - Ex: not invalidating sessions after logout or failed login attempts
8. Software and Data Integrity failures: insecure handling of software updates or data validation
    - Ex: a program that deserializes user-supplied data without verification allowing an attacker to access internal resources (**Zero Trust Framework**, Checksum-based validation of requests)
9. Security Logging & Monitoring: inadequate detection of security events
    - Ex: An attacker brute-forces a password and the system never logs the failed attempts, making the attack invisible
10. Server-Side Request Forgery (SSRF): a vulnerability where an attacker can trick the server into making requests to internal resources
    - Ex: a "generate pdf from url" feature is tricked into requesting internal resources, bypassing access controls

#### Key Takeaways
- Security is a process, not a product
- Security is everyone's job
- Start with a plan
- Use industry standards

## Module 9 - Reducing complexity

### Section I - The complexity problem
Purpose of education: Help humans grow

The downside of complexity: 
- the human brain prefers simplicity
- more components and interactions mean more potential points of failure
- maintenance, operations and change management become exponentially more complex
- it's extremely hard to create and maintain accurate documentation of a highly complex system

### Module 9 objectives:
1. understand the flaw
2. learn good practices
3. advocate for simplicity

### Section II - 

- The "Too many tools" problem
- Solution: Unified Platforms (XDR - extended detection and response, UTM - unified threat management)

#### Case Study: the password paradox
- 90% of users admit to reusing passwords
- users know this is a bad practice, but they do it anyway
- why? because remembering 100 unique passwords is not humanly possible

#### Simple, Stronger alternatives
1. Multi-factor authentication (MFA) (*something you have*)
2. Biometrics: fingerprint, face recognition, iris scan (*something you are*)
3. Passwordless: authenticator apps, removing the need for passwords

### Section IV - Practical applications
#### Simple, Effective policies
1. a security policy is not just technical doc, it's human document
2. if policy is 50-page, no one will read it

Clarity: use "don't share your password" to "all authentication tokens are non-transferable"

### Key Takeaways
1. Principles: Complexity is a hidden tax on security (maintenance, errors, usability friction).
Use a risk-based lens to apply proportionate controls, not all controls.
Unify management platforms to reduce "tools" and "alert fatigue"
2. Application: Bad, complex rules backfire by forcing insecure user behavior.Good security is usable.
The secure path should always be the easy path.
Simplicity is a feature and a sign of mature Secure By Design process.

## Module 10 - How to maintain an Enterprise - scale system

Area 1 - Cybersecurity Strategies: defines security goals aligned with business needs and sets timelines for implementation, covering response to incidents (detailed IRP)
Area 2 - Standardized Process: make sure everyone's following the same rules and procedures
Area 3 - Compliance: comply with laws, regulations, etc
Area 4 - Senior Leadership Oversight: ensure leadership is committed and involved in security decisions
Area 5 - Resources: allocate adequate budget, personnel, and tools for security operations

### Five Types of Cybersecurity Policies
1. Security policies - define the overall security framework and objectives
2. Directive policies - provide specific instructions and procedures for implementation
3. Administrative policies - govern organizational structure, roles, and responsibilities
4. Communications and technical policies - manage data flow, network security, and technical controls
5. Risk-based policies - prioritize security measures based on risk assessment and business impact

### Implementing Governance
1. Secure executive commitment
2. Conduct a gap analysis of current sec policies
3. Select a governance framework
4. Design and implement customized policies