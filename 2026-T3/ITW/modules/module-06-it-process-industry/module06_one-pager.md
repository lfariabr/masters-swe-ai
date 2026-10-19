# ITW601 · Module 6 - One-Pager

> **IT Processes · Security Framework · Incidents · Infrastructure · ITIL 4**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = assessment hooks + traps

---

## 🖤 The Big Idea (box it, centre of page)
> **Processes are how an organisation makes good IT behaviour repeatable: someone accountable, written rules at the right level, proof that the controls work, and a plan for when they fail.**
> (Alexander et al., 2020, Ch. 3 · Bandos, 2022)

## 🖤 Zone 1 - Who is responsible (R2)
```
BOARD DIRECTOR (accountable) -> WORKING GROUP (business heads, HR, audit, IT, suppliers)
   -> SECURITY MANAGER (day to day) -> ASSET OWNERS -> EVERY USER (acceptable use policy)
```
- 🔵 Requirements are **statutory** (law) · **regulatory** (trade bodies) · **advisory** (best practice).
- 🔴 No senior support, no programme: initiatives "will probably fail".

## 🖤 Zone 2 - The document ladder (R2)
| Policy | Standard | Procedure | Guideline |
|---|---|---|---|
| why, long-lived | how much, measurable | what, when, how, who | advice |
| mandatory | mandatory | mandatory | optional |
- 🔵 **Defence in depth** (layers) + **breadth** (every connection; the weakest link breaks first).
- 🔴 **My version:** the awards rules note is a standard; the runbook is a procedure.

## 🖤 Zone 3 - Prove it works (R2)
- 🔵 Risk register · **dispensations register** · policy reviews · audit and test results · incident reports.
- 🔵 **ISO/IEC 27001** = certifiable requirements · **27002** = code of practice.
- 🔴 **Trap:** the chapter's law is UK and EU. Mine is the Privacy Act 1988, the APPs and the NDB scheme.

## 🖤 Zone 4 - When it breaks (R3 + R2)
```
PREPARE -> DETECT + REPORT -> TRIAGE + ANALYSE -> CONTAIN + NEUTRALISE -> POST-INCIDENT (learn)
BCS:       reporting -> investigation -> assessment -> corrective action -> review
```
- 🔵 More than half of response plans **fail when first tested**. Keep a log from the first report.
- 🔴 A data incident counts too: a ranking published with missing rows, a cohort shown to the wrong role.

## 🖤 Zone 5 - Underneath and around (R4 + R5)
- 🔵 **Infrastructure** = software · hardware · network (not app development, not endpoints).
- 🔵 Hard parts: **legacy integration**, monitoring, change management, regulation.
- 🔵 **ITIL 4:** 34 practices = 14 general · 17 service · 3 technical. **Incident** restores service; **problem** removes the cause.
- 🔴 Canon is a vendor page: definitions yes, "outsource it" claims no.

## 🔴 Assessment Hook (bottom red strip)
> **A2 e-Journal: Industry Placement Interview and Project Synopsis** · 1,000 words ±10% · 35% · due **Sun 15/11/2026, 11:55pm** · SLOs **a) to e)**.
> M6 feeds the synopsis **ethical issues** and **managerial plan** (asset owner vs custodian, policy vs standard, an incident plan for a wrong ranking) and the **ICT infrastructure challenges** (legacy integration = Trial marks that never reach the warehouse; missing monitoring = refreshes that succeed while rows go missing).

## 🔴 If you only memorise 5 things
1. **One accountable person, one working group.** Then delegate.
2. **Policy → standard → procedure:** each more specific, all mandatory; guidelines are advice.
3. **Show evidence:** risk register, dispensations, reviews.
4. **Incidents will happen:** prepare, detect, triage, contain, learn.
5. **Incident ≠ problem:** restore fast, then remove the cause.

---

### Margin prompts (answer in blue - anchor to the school data work)
1. Who is the information owner for the awards data, and who is the custodian?
2. Write the first three lines of an incident procedure for "a ranking was published with missing rows".

### This-week to-dos (still 🕐 in your notes)
- [X] ✅ Watch the Vanersity Tech video (watched 20 Oct)
- [ ] 🕐 Read Alexander et al. Ch. 3 (pp. 39-87)
- [ ] 🕐 Read the incident response and infrastructure articles
- [ ] 🕐 Activity 1: review the draft, post it (≤250 words), then comment on other posts
- [ ] 🔥 Awards page in `/admin/student360`
