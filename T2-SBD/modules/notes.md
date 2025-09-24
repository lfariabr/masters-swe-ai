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

