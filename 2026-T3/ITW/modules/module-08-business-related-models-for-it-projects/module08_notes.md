# Module 08 - Business-Related Models for IT Projects

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise: decision trees for longitudinal decisions (Coles & Rowley, 1995) | 🔥 |
| 2 | Read & summarise: cost-benefit analysis for a software upgrade (Ali, 2012) | 🔥 |
| 3 | Read & summarise: business process acceptance model (Degerli & Ozkan, 2014) | 🔥 |
| 4 | Read & summarise: teamwork delivers value (Goodpasture, 2013, Ch. 4) | 🔥 |
| 5 | Module concepts: forecasts vs budgets, project balance sheet, risk values | 🔥 |
| 6 | Activity 1: watch Wang (2018), then the Organisation X feasibility-study post, plus comments on two posts | 🔥 draft ready |

> Source corrections against the module text, checked against the PDFs (3 Nov 2026):
> - The supplied Goodpasture file is **Chapter 4, "Teamwork delivers value"**. It does not cover business cases, the project balance sheet, earned value or game theory; those live in other chapters of the book that were not supplied. Cite Chapter 4 only for teams.
> - The Chapter 13 editors are **Charles, V., & Kumar, M.** (the module lists "Vincent, C.").
> - The decision-tree authors are **Coles, S., & Rowley, J.** (the module lists "Susan, C. & Jennifer, R.", first names in place of surnames).

---

## Key Highlights

### 1. Decision trees for decisions that unfold over time

**Citation:** Coles, S., & Rowley, J. (1995). Revisiting decision trees. *Management Decision, 33*(8), 46-50.

**Purpose:** managers undervalue decision trees because the probability maths looks hard and the textbook model looks paper-bound. The authors show a tree in a spreadsheet, under several decision criteria, with sensitivity analysis (pp. 46, 50).

**How a tree works (p. 47):**

| Pass | What you do |
|---|---|
| Forward | Lay out decisions (squares), events (circles) and their order; estimate each outcome's payoff and each event's probability |
| Backward | From right to left: expected value at each event node = sum(probability x payoff); at each decision node keep the branch with the highest value; cross out the rest |

**The worked example (pp. 46-47):** build a large plant (£8m) or a small one (£5m) that can be expanded later (£4.5m). Demand is significant (P = 0.3) or moderate (P = 0.7). The tree values large at 2.5 and small at 4.2, so build small. The option to expand is what makes the small plant win.

**Themes:**

1. **Longitudinal decisions.** A decision now is followed by events and further decisions. The tree makes the sequence visible (p. 46). "All forecasting is conducted under uncertainty" (p. 46).
2. **The forward pass is worth doing on its own.** Even without numbers, laying out the branches structures thinking about future options (pp. 47-48).
3. **The criterion encodes your attitude to risk (pp. 48-49).**
   - Expected value uses all the information but ignores risk attitude.
   - Equally likely, maximax (go for it) and minimax (conservative) can flip the answer. Under equally likely, large beats small.
   - "The most appropriate decision strategy depends on the decision maker's attitude to risk" (p. 49).
4. **Payoffs need not be profit.** A tree can minimise cost or time (p. 48).
5. **Sensitivity analysis tests robustness.** In the spreadsheet, varying the probability from 0.1 to 0.5 and both profits across a range never changes the choice (pp. 49-50). A robust answer is one that survives your estimates being wrong.

**Key takeaways for ITW601:**
- **Workbook first, page later is the small plant with the option to expand.** A stakeholder-checked workbook is cheap. The portal page is the expansion you buy only once the rules hold.
- **Year 11 was a longitudinal decision.** I could build on provisional marks now, or wait for release. The event in between was "marks change". I built provisionally, then rebuilt after release: four totals moved by about one mark and the top five held. A tree would have shown that building early was the cheap branch, because the build is scripted and a rebuild is repeatable.
- **Sensitivity is the question to ask a stakeholder:** "would any plausible change in this number change the ranking?" That is the zero-difference check, said in decision-tree language.

---

### 2. Cost-benefit analysis for an IT investment

**Citation:** Ali, A. (2012). A framework for using cost-benefit analysis in making the case for software upgrade. *Issues in Informing Science and Information Technology, 9*, 399-409.

**Purpose:** a CBA framework IT managers (in the paper, at universities) can use to justify a software upgrade and judge its feasibility, with ways to turn each cost and benefit into money (p. 399).

**The framework (Table 1, pp. 407-408):**

| Costs | Benefits / cost saving |
|---|---|
| Purchasing: licence, installation and troubleshooting, support | New features: immediate and future opportunities; skills graduates or staff would otherwise lack |
| Learning the new software: formal, informal and self-training | Speed: worker time saved; capacity to handle other jobs |
| Additional hardware and software, and reaching optimal performance | Competitive advantage: lower operating cost, better processes, new opportunities |

**Themes:**

1. **CBA is a persuasion tool and a planning tool.** Rank alternatives by net gain or by benefit-cost ratio (p. 401). "It works as a persuasion tool" (p. 401).
2. **The price is not the cost.** Learning-curve slowdown and late-surfacing incompatibility are real costs, and they arrive after the purchase (pp. 402-405). "The cost of software upgrade often extend beyond this" (p. 402).
3. **IT returns are hard to price.** "The return from IT expenses or investments are often difficult to quantify" (p. 402). That is the method's main weakness, and why the paper suggests a monetary proxy for each item.
4. **Feasibility is a yes or no on the net.** The framework "determines the feasibility (or lack of it)" of paying for the upgrade (pp. 399-400).
5. **Timing is a risk both ways.** Upgrading too early wastes money; waiting too long loses ground (p. 400).

**Key takeaways for ITW601:**
- **The awards page as a CBA.**
  - Costs: build time, the safe-field and table approvals, staff learning a new screen, and keeping the snapshot current.
  - Benefits: the rebuild time saved each round, fewer transcription errors, and the same answer for every staff member who opens it.
  - The honest weakness is Ali's: "fewer disputed rankings" is real but hard to put a dollar on.
- **Learning cost is the one I would have missed.** A page staff do not trust gets checked against the old workbook anyway, so the learning cost lasts until acceptance.
- **For A2:** the methodology already compares three options. Ali gives the vocabulary for why the third won: it delivers the benefit soonest for the least new cost.

---

### 3. Why people accept (or quietly ignore) a business process

**Citation:** Degerli, M., & Ozkan, S. (2014). Achieving and ensuring business process acceptance for systems and software engineering and management. In V. Charles & M. Kumar (Eds.), *Business performance measurement and management* (pp. 292-333). Cambridge Scholars.

**Purpose:** a Business Process Acceptance Model (BPAM) that explains why practitioners accept, or ignore, the processes an organisation defines. It adapts technology-acceptance models (TAM, TAM 3, UTAUT) and ends with a 41-item checklist (p. 292).

**The model in one breath:** acceptance is behavioural intention (BI), driven by perceived usefulness (PU) and perceived ease of use (PEOU). Process-specific factors feed those, including:
- audit (AUD);
- outputs and results demonstrability (OR);
- facilitating conditions (FC);
- participation in development (PD);
- subjective norm (SN), which carries organisational culture (OC);
- stability (STB);
- granularity (GRN);
- training (TRN);
- medium (MED);
- modelling (MDL).

The survey had n = 368, with 21 significant paths in the final model (pp. 303-316).

**Themes:**

1. **Acceptance decides success.** "Acceptance is the key factor that determines whether a project or system is successful or not" (p. 293).
2. **Process quality drives product quality.** The CMMI principle, quoted on p. 294.
3. **Participation is a direct path.** Practitioners who helped define a process intend to use it (PD -> BI). Results they can see make it seem useful and easy (OR -> PU, PEOU) (p. 316).
4. **Culture works through people.** Organisational culture acts on subjective norm, what colleagues expect, not on intention directly (OC -> SN, p. 316).
5. **Just enough, and not churned.** Granularity means "just the required and sufficient amount of information". Stability means updates come "not too frequently or disturbingly" (p. 299).
6. **Caveat.** The study is survey- and perception-based. Its R-squared is moderate (BI 0.367), and it does not measure project outcomes (pp. 315-317).

**Key takeaways for ITW601:**
- **Participation in development is why the rules note worked.** The academic lead corrected a rule within a day of seeing it. A rule she helped write is a rule she defends.
- **Outputs and results demonstrability is the workbook.** She can check a named student's row before any page exists. That is OR -> PU in practice.
- **Stability is a warning for the awards rules.** Three rules added between 9 and 30 October are fine while the rules are being found. After acceptance, changes need a gate, or the rules stop being trusted.
- **For A2:** acceptance is the R1 criterion's real subject. The model explains why acceptance runs through the workbook, not the page.

---

### 4. Teams, groups and virtual teams

**Citation:** Goodpasture, J. C. (2013). Teamwork delivers value. In *Maximizing project value: A project manager's guide* (Ch. 4). Berrett-Koehler.

**Purpose:** how groups differ from teams, how co-located and virtual teams deliver value differently, and where a single creative leader (the "auteur" model) fits.

**Themes:**

1. **Crowd, group, team.**
   - "Crowds are not groups."
   - A group has a common purpose, roles, norms and processes.
   - A team adds a common goal, collective commitment, and individual success tied to team success.
   - "A team is a social structure wherein all members individually and mutually collaborate toward the achievement of a common goal" (pp. 3-4, ebook pages).
   - Many executive teams are really groups (p. 4).
2. **Seven team values:** trust, commitment, accountability, continuity, simplicity, clarity and certainty. Certainty is defined as the absence of unmitigated risk (pp. 4-5).
3. **Proximity drives communication.** Co-location gives "communication by osmosis", and communication falls off with distance (pp. 6-7).
4. **Virtual teams pay a "productivity discount".** Trust forms slowly, which "is a risk to the near-term schedule and perhaps the associated budget" (p. 9).
5. **Innovation test (TACOS):** trialability, advantage, compatibility, observability and simplicity (p. 11).

**Key takeaways for ITW601:**
- **My project is a group that has to act like a team.** The academic lead, the reporting coordinator, the ICT sponsor and I share a purpose but not one goal or one success measure. The shared goal is a fair ranking that everyone can explain.
- **TACOS fits the awards page.**
  - Trialability: fictional data first.
  - Observability: source and run-date labels.
  - Compatibility: it reproduces the workbook the stakeholder already trusts.

---

### 5. Module concepts: forecasts, budgets, the project balance sheet and risk values

> No supplied reading covers these directly, so this section stays at concept level and is uncited. Read the module text and its other Goodpasture chapters before citing any of it.

- **A forecast is a best estimate of what will happen. A budget is a committed allocation you are held to.** A forecast updates as you learn; a budget changes only through approval. Coles and Rowley's point applies to both: every forecast is made under uncertainty.
- **The project balance sheet (concept).** What the business expects from the project has to balance what the project can deliver plus the risk the project carries. When expectations exceed capability, the gap is risk, and someone has to own it.
- **Risk values.** Probability x impact gives a risk an expected value, the same arithmetic as a decision-tree branch. That makes risks comparable and lets a contingency be sized, not guessed.

**Key takeaways for ITW601:**
- **My early estimate for the awards page was a forecast, and it slipped.** Treating it as a forecast, re-stated as I learned, is honest. Treating it as a budget would have meant cutting scope to hold the date.
- **The balance-sheet gap is visible in A2's Appendix D.** The sponsor expects an accepted, enabled page. Delivered so far: an accepted workbook. The gap (table approval, safe fields, portal checks) is the project's risk, and the appendix names who owns each part.

---

## Links to the rest of the term

```
Module 6 (process)      -> Module 7 (communicate)    -> Module 8 (justify and decide)
policy, gate, evidence     check it landed (step 5)     tree the options, price them (CBA),
                                                         and design for acceptance (BPAM)
```

- **A2 (due 15 Nov):** SLOs a), b) and d) map here.
  - The methodology's three options are a decision tree with no numbers.
  - The option chosen is the CBA winner.
  - R1 acceptance is the BPAM outcome, earned through participation and visible results.
- **A3 (due 2 Dec):** "what I would justify differently" can use the forecast-versus-budget distinction and the expand option.
