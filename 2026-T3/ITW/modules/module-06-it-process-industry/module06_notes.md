# Module 06 - IT Process and Industry

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 1 | Watch & summarise Vanersity Tech (2017) - Information technology processes and workflows (video) | ✅ |
| 2 | Read & summarise Alexander et al. (2020) - Ch. 3 Information security framework (pp. 39-87) | 🕐 |
| 3 | Read & summarise Bandos (2022) - The five steps of incident response | 🕐 |
| 4 | Read & summarise Canon Business Services (2023) - IT infrastructure management | 🕐 |
| 5 | Activity 1: Discussion forum post, five ITIL processes for the project (≤250 words), plus feedback on other posts | 🕐 |

> Resource rows stay 🕐 until Luis confirms the reading or viewing. The summaries below are study aids built from the local copies. Resource 1 was watched by Luis (20 Oct 2026); the 2017 video has no transcript or captions, so it has no summary here.

---

## Key Highlights

### 1. Vanersity Tech. (2017). Information technology processes and workflows.

**Citation:** Vanersity Tech. (2017). *Information technology processes and workflows* [Video]. YouTube. https://www.youtube.com/watch?v=B3a5sLpefas

**Purpose (from the course overview):** Project vs process, IT domain terminology, and why processes and service workflows should be documented.

> Watched by Luis on 20 Oct 2026. No transcript or auto-captions exist for this 2017 video, so there is no written summary.

---

### 2. Alexander, D., Finch, A., Sutton, D., & Taylor, A. (2020). Chapter 3: Information security framework.

**Citation:** Alexander, D., Finch, A., Sutton, D., & Taylor, A. (2020). *Information security management principles* (3rd ed.). BCS Learning & Development. Ch. 3, pp. 39-87.

**Purpose:** Sets out how an organisation structures information assurance: who is responsible, how policy, standards and procedures fit together, how governance proves controls work, how a programme is planned, and how incidents, law and standards shape it. Local copy: [r2_alexander-et-al-information-security-framework-ch3.pdf](r2_alexander-et-al-information-security-framework-ch3.pdf).

> The ProQuest stamp on each page reads "Taylor et al. (2013)", but the text cites GDPR, the 2018 NIS Regulations and ISO/IEC 27007:2017, so the copy is the 2020 edition the course cites.

---

#### 1. Organisation and responsibilities
- **Information security manager** (or CISO): runs day-to-day assurance, coordinates policy, tells users their duties, knows the risk appetite, reports effectiveness upward.
- **One board-level director is accountable.** Without senior support, assurance initiatives "will probably fail". They chair a **working group** (steering committee) with business heads, HR, audit, IT and key suppliers.
- **Everyone has a part:** job descriptions name scope, authority, breach reporting and confidentiality. Local coordinators act as "eyes and ears".
- **Every information asset has an owner** who understands the impact if its confidentiality, integrity or availability is lost.
- Requirements are **statutory** (law), **regulatory** (trade bodies, fines) or **advisory** (best practice).

#### 2. Policy, standard, procedure, guideline
| Document | What it does | Mandatory? | Password example |
|---|---|---|---|
| **Policy** | High-level values, goals and approach; long-lived | Yes | Each user maintains their own passwords |
| **Standard** | Quantifies what must be done; measurable | Yes | At least eight characters, mixed types |
| **Procedure** | What, when, how and by whom | Yes | Step-by-step reset instructions |
| **Guideline** | Advice where rules are hard to set | No | Working away from the office |

- Write them short, plain and positive. They must be **realistic and enforceable**, endorsed by management, and owned.
- **Acceptable use policy:** the end-user code of practice (passwords, need-to-know access, lock screens, clear desk, personal devices, report incidents).
- **Balance physical, procedural and technical controls**, layered. A £1 million control for a £10,000 asset makes no sense.
- **Defence in depth** (layers, strongest around the most sensitive data) and **defence in breadth** (every connection to suppliers, homes and partners; the weakest link is where intruders get in).

#### 3. Governance: proving it works
- Review policies on a schedule and after major change; record why each revision was made.
- Regulators want evidence: risk assessments, a **risk register**, current policies, a **register of dispensations**, test and audit results, incident reports, and plans for gaps.
- Models: **ISO/IEC 27001** (certifiable; the PDCA cycle is no longer formally part of it), SOMA (maturity levels), COSO (control objectives), plus NIST and PCI DSS.

#### 4. Implementing an assurance programme
- Start from a risk assessment, prioritise the worst risks, look for **quick wins**, name a **sponsor** and a steering committee, plan high-level and detail later.
- Sell it as an **enabler**: plain language, a business case, ROI, certification as competitive advantage.
- **Strategy** (3-5 years, where we want to be) vs **architecture** (a consistent set of controls, grouped into domains, reused across systems).

#### 5. Incidents, law and standards
- Incidents are a matter of "when", not "if". More than half of response plans **fail when first tested**.
- Five phases: **reporting, investigation, assessment, corrective action, review**. Use a standard report form, keep a log from the first report, and appoint a trained **incident response team** with an escalation path and a note-taker.
- **Legal framework** (UK and EU focus): GDPR, monitoring and employee rights, records retention (ISO 15489-1:2016), outsourcing contracts, admissible evidence.
- **Standards:** ISO/IEC 27001 (requirements, certifiable) and 27002 (code of practice), plus 27005 (risk), 27017 (cloud) and 27799 (health).

#### Key Takeaways for ITW601
1. **Read it from Australia:** the legal section is UK and EU. My equivalents are the Privacy Act 1988, the APPs and the Notifiable Data Breaches scheme (Module 2).
2. **Asset owner:** for the awards data, the academic stakeholder is the information owner; my role is custodian. That framing belongs in the A2 managerial plan.
3. **Policy vs standard:** the written awards rules note works as a standard, measurable and agreed, and the runbook is the procedure. Naming them that way strengthens the A2 plan.
4. **Defence in depth for Student360:** server-side reads, role checks, the safe-field list and de-identified public material are separate layers.
5. **Dispensations:** the manual markbook build for Year 12 is an exception to the warehouse path, so it should be recorded as one.

---

### 3. Bandos, T. (2022). The five steps of incident response.

**Citation:** Bandos, T. (2022, December 28). *The five steps of incident response*. Digital Guardian. https://digitalguardian.com/blog/five-steps-incident-response

**Purpose:** Part 5 of a field guide series: five steps every incident response programme should cover. Local copy: [r3_fortra-five-steps-incident-response.pdf](r3_fortra-five-steps-incident-response.pdf).

> The saved page now sits on fortra.com, shows no author and reads "Posted on September 20, 2016". The course reference (Bandos, 2022) is kept here; confirm before citing it in an assessment.

---

#### 1. The five steps
| # | Step | Main actions |
|---|---|---|
| 1 | **Preparation** | Documented IR policies and agreements, communication guidelines, threat intelligence feeds, threat hunting exercises, assess detection capability |
| 2 | **Detection and reporting** | Monitor (firewalls, intrusion prevention, data loss prevention), detect (correlate alerts in a SIEM), alert (ticket, findings, classification), report (including regulatory escalation) |
| 3 | **Triage and analysis** | Most of the effort. Endpoint analysis (timeline, forensic copy, memory), binary analysis (behavioural and static), enterprise hunting (scope of compromise) |
| 4 | **Containment and neutralisation** | Coordinated shutdown, wipe and rebuild, change passwords, block attacker domains |
| 5 | **Post-incident activity** | Incident report, monitor for return, update threat intelligence, preventive measures, cross-functional buy-in |

- **Incident response is a process, not an isolated event.**

#### 2. Compared with Alexander et al.
| Alexander et al. (management view) | Bandos (security operations view) |
|---|---|
| Reporting | Detection and reporting |
| Investigation, assessment | Triage and analysis |
| Corrective action | Containment and neutralisation |
| Review | Post-incident activity |
| (plan and team prepared beforehand) | Preparation |

#### Key Takeaways for ITW601
1. Not every incident is an attack. A **data incident** for Student360 could be a ranking published with missing rows, or a cohort visible to the wrong role. Both need the same five steps.
2. **Preparation for the awards page:** who to tell, how to roll back to the last accepted view (already in the A1 proposal), and how to judge whether the Notifiable Data Breaches scheme applies.
3. The post-incident step is the same idea as Module 5's "standardise": write it down so it does not repeat.

---

### 4. Canon Business Services. (2023). How does IT infrastructure management work for an organisation?

**Citation:** Canon Business Services. (2023). *How does IT infrastructure management work for an organisation?* https://business.canon.com.au/insights/how-does-it-infrastructure-management-work-for-an-organisation

**Purpose:** An Australian provider explains IT infrastructure, infrastructure management and how to implement it, with a case for outsourcing it. Local copy: [r4_canon-it-infrastructure-management.pdf](r4_canon-it-infrastructure-management.pdf).

> This is a vendor's marketing page: its benefits list argues for buying its managed service. Use it for definitions, not as evidence that outsourcing is better.

---

#### 1. What infrastructure is (and is not)
- Three components: **software** (applications, operating systems), **hardware** (devices, servers, network gear, data centres), **network** (connectivity, cloud).
- Types: **traditional** (owned facilities and data centres) and **cloud** (public or private).
- **Not included:** application development (DevOps), the people and processes that use the infrastructure, and endpoints such as laptops, which belong to endpoint management or the help desk.

#### 2. Challenges
- New solutions that do not integrate with **legacy systems**; a growing cyber threat landscape; changing regulation (PCI, ISO, SOC; in Australia, APRA's CPS 230 for regulated entities).
- Teams stretched by day-to-day support have no time for capacity planning, hardening or cost control.

#### 3. Seven implementation strategies
1. Define clear objectives and scope.
2. Agree service level agreements (response times, uptime, resolution).
3. Adopt an ITSM framework such as ITIL.
4. Invest in automation and monitoring.
5. Foster collaboration and communication.
6. Implement change management (assess, plan, test, communicate).
7. Improve continually, with KPIs, audits and user feedback.

#### Key Takeaways for ITW601
1. **A2 ICT challenges:** "new solutions don't integrate with legacy systems" is the general form of my specific finding that Year 12 Trial marks never reach the warehouse.
2. **Monitoring (strategy 4)** is what the school lacks for data: a refresh can succeed while rows go missing. A coverage check per run is the monitoring control.
3. **Scope:** Student360 is application development, so by this definition it sits on the infrastructure, not in it. The infrastructure challenges are the sources and pipelines underneath.

---

### 5. Mohanakrishnan, M. (2025). ITIL processes and practices in ITIL V4 (Activity 1).

**Citation:** Mohanakrishnan, M. (2025, July 14). *ITIL processes and practices in ITIL V4*. KnowledgeHut. https://www.knowledgehut.com/blog/it-service-management/itil-process-list

**Purpose:** A training provider's overview of the ITIL 4 practices, the reading for Activity 1. Local copy: [r5_knowledgehut-itil-v4-processes-activity.pdf](r5_knowledgehut-itil-v4-processes-activity.pdf).

> The course cites "KnowledgeHut (April 12, 2022)"; the saved page names the author and shows "Updated on Jul 14, 2025". Read it critically: it says "34 processes organized into three management phases", but ITIL 4 calls them **practices**, grouped as general, service and technical, and the article also mixes in ITIL v3 lifecycle stages (service transition, service operation).

---

#### 1. The three practice groups
| Group | Count | Examples |
|---|---|---|
| **General management** | 14 | Strategy, portfolio, architecture, financial, workforce and talent, continual improvement, measurement and reporting, risk, information security, knowledge, organisational change, project, relationship, supplier |
| **Service management** | 17 | Business analysis, service catalogue, service design, service level, availability, capacity and performance, continuity, monitoring and event, service desk, incident, service request, problem, release, change enablement, service validation and testing, service configuration, IT asset |
| **Technical management** | 3 | Deployment, infrastructure and platform, software development |

- **Incident vs problem:** incident management restores service fast (the forgotten password); problem management finds and removes the cause so incidents stop recurring.

#### Key Takeaways for ITW601
1. Activity 1 picks: change enablement, service validation and testing, information security management, problem management and knowledge management. Draft: [activity01_itil-processes-for-the-project_draft.md](activity01_itil-processes-for-the-project_draft.md).
2. "Problem management" names what the awards work did with the live view that lost rows: find the cause, then route around it with the snapshot.

---

## Module 6 at a glance
```
Who and what (Alexander et al.):  accountable director -> working group -> security manager -> asset owners -> every user
                                  policy (why) -> standard (how much) -> procedure (how) · guideline (advice)
Prove it:                         risk register · dispensations · reviews · ISO/IEC 27001
When it breaks (Bandos):          prepare -> detect + report -> triage -> contain -> learn
Underneath (Canon):               software · hardware · network; integrate legacy, monitor, manage change
Run it (ITIL 4):                  34 practices: 14 general · 17 service · 3 technical
                                      \__ A2: ethics + managerial plan + the infrastructure challenges
```
