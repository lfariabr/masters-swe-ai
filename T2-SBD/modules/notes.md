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