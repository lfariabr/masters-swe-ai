# Module 09 - The Role of Quality in IT Projects

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise the module text: quality policy and objectives, the process approach and PDCA, monitoring, cost of quality | ✅ |
| 2 | Read & summarise: why managing quality is essential in projects (Basu, 2012, Introduction) | ✅ |
| 3 | Read & summarise: a software reliability model with testing coverage and imperfect debugging (Zhang & Pham, 2001) | ✅ |
| 4 | Read & summarise: measuring the cost of poor quality (Mahmood et al., 2014) | ✅ |
| 5 | Read & summarise: quality dimensions, perspectives and practices (Zhang, 2001) | ✅ |
| 6 | Activity 1: watch Penzenstadler (2018), then the Organisation X QA review post, plus comments on two posts | ✅ |

> Source corrections against the module text, checked against the PDFs (10 Nov 2026):
> - The supplied Pham file is **Chapter 2 by Zhang and Pham**, published in **2001** (pp. 17-31), not "Pham (2015)". Cite the chapter's authors.
> - Zhang (2001) has a subtitle, "A mapping analysis", and runs **pp. 708-721**.
> - The Basu PDF names **Taylor & Francis**, not Gower. The supplied file is the Introduction (pp. 1-12).

---

## Key Highlights

### 1. The module text: policy, process, measurement, cost

- **Quality policy and objectives.** The policy shows top management commitment and resources. The objectives make it real: set at each function, measurable, and tied to product requirements.
- **Process approach.** Every activity turns inputs into outputs, and one process's output is the next one's input. Each process runs its own **Plan-Do-Check-Act** cycle, and continuous improvement lives in the "check" and "act".
- **Monitoring.** Accuracy, timeliness, dependability, response time, cycle time, people's effectiveness, resource use, KPIs and cost.
- **Analysing data.** Measurement earns its place only if it supports decisions, shows trends and variation (control charts), and tracks milestones.
- **Cost of quality (COQ).** What you spend preventing poor quality, against what failure costs you. **Quality control** (inspecting and testing products and processes) is the compliance arm under the **quality assurance** umbrella.

**Key takeaway for ITW601:** each awards round is a PDCA cycle.
- **Plan:** the rules note.
- **Do:** the build.
- **Check:** the stakeholder review and the row-by-row comparison.
- **Act:** add the rule and rebuild.

The output of one round, the accepted workbook, is the input to the next: the portal page.

---

### 2. Why quality is the neglected side of the iron triangle

**Citation:** Basu, R. (2012). Introduction: Why managing quality is essential in project management. In *Managing quality in projects* (pp. 1-12). Taylor & Francis.

**Purpose:** project management treats quality more weakly than operations management does. The book sets out to define and measure project quality and link it to project excellence (pp. 1-7).

**Themes:**

1. **On time and on budget is not success.** Quality often gets "lip service" and tick-box compliance. Many projects hit time and cost and still fail their users (pp. 1-2).
2. **Time and cost are easy to measure; quality is not.** Turner (2002) splits it into product quality and process quality (p. 2). "If you cannot define, you cannot measure, and if you cannot measure, you cannot control, assure or improve" (p. 5).
3. **Success criteria vs success factors (pp. 8-9).**
   - Criteria are the measures that decide whether you succeeded (on time, outcomes delivered).
   - Factors are the conditions that make success likely (stakeholder management, good process).
4. **Quality is necessary, not sufficient.** Project quality is "the philosophy of the adherence of standards throughout the life cycle of a project" (p. 9). Its dimensions are "necessary but not sufficient contributors to project excellence" (p. 9).
5. **PDCA keeps it stable.** Figure I.2 (p. 10) runs plan-do-check-act around a set point (the metric): measure, compare, decide, then feed back and correct. Permanent correction means removing root causes (pp. 10-11).

**Key takeaways for ITW601:**
- **R1's "zero differences against the signed workbook" is a success criterion. The academic lead's participation is a success factor.** A2 needs both, and now has a word for the difference.
- Basu's line on page 5 is the reason every A2 requirement has an "accepted when" column.

---

### 3. Testing coverage and imperfect debugging

**Citation:** Zhang, X., & Pham, H. (2001). A software reliability model with testing coverage and imperfect debugging. In H. Pham (Ed.), *Recent advances in reliability and quality engineering* (pp. 17-31). World Scientific.

**Purpose:** a reliability growth model that combines testing coverage with imperfect debugging. It estimates the faults remaining and supports the decision about when to stop testing and release (p. 17).

**The model in plain words (pp. 18-23):**
- Failures are found faster when more faults remain.
- Fixing a fault can introduce a new one (**imperfect debugging**), but less often as testers learn.
- **Testing coverage**, the share of code exercised, grows in an S-curve: slow start, fast middle, flat tail.
- From these, the model estimates how many faults existed at the start, so it can tell you how many are left.

**Themes:**

1. **Reliability is a quality measure.** It supports "determining when to stop testing and release software on the basis of predetermined reliability objectives" (p. 17).
2. **Fixes are not free.** Earlier models assumed perfect debugging. Real fixes sometimes add faults (pp. 17-18).
3. **Coverage tells you how much is left.** It shows "how much of the software has been executed and how much more effort is needed for further improvement" (p. 30).
4. **It held up on real data.**
   - IBM data-entry package: the initial-fault estimate stayed stable (about 60 after 17 days and after all 21), where other models' estimates moved (pp. 23-26).
   - Real-time control system: prediction error 9.37 against 102.66 for the next best model (Table 7, p. 29).
5. **No cost model.** The release decision is against a reliability target set in advance. The chapter does not price it (p. 30).

**Key takeaways for ITW601:**
- **Every rule change is a fix that can break something.** The awards build reruns its self-test and checks that the Year 12 output is unchanged after each Year 11 rule. That is a guard against imperfect debugging.
- **Coverage in the access tests.** The cohort test now lists all seven roles, so a new role cannot slip in untested. That is coverage made explicit.
- **"Predetermined reliability objectives"** are what A2 calls acceptance criteria. Set them before the page exists, not after.

---

### 4. The cost of poor quality, measured

**Citation:** Mahmood, S., Ahmed, S. M., Panthi, K., & Kureshi, N. I. (2014). Determining the cost of poor quality and its impact on productivity and profitability. *Built Environment Project and Asset Management, 4*(3), 296-311. https://doi.org/10.1108/BEPAM-09-2013-0034

**Purpose:** test a cost-appraisal system that measures the cost of poor quality (COPQ) on a construction project, and relate COPQ to labour productivity and profitability (p. 296).

**Cost of quality, as the paper lays it out (pp. 297-298):**

| Cost of good quality | Cost of poor quality (COPQ) |
|---|---|
| **Prevention:** stopping defects before they happen | **Internal failure:** rework, scrap, waste and downtime before delivery |
| **Appraisal:** inspection and checking | **External failure:** complaints, warranty and recalls after delivery |

**The measure (Eq. 1, p. 300):** COPQ = lost material + lost labour hours + lost machinery hours + lost overhead days, each multiplied by its rate.

**Themes:**

1. **COPQ is hidden.** Normal accounting does not show it, and "COPQ cannot be controlled until it is identified and measured" (p. 297).
2. **It is big.** Twenty-one studies average about 27.5% of project value (Table I, pp. 298-299).
3. **Measuring it changed it.** On a 60-day bridge project, the first 15 days were the benchmark (COPQ 40.43% of work done). Weekly COPQ reports to management followed. In the last quarter COPQ was 16.65%, down 47.53% in dollars (Tables II-III, pp. 302-304).
4. **Productivity and profit rose together.** Labour productivity rose 16.88% and profitability 10.45% (Tables IV-V, p. 305). The authors credit part of the early drop to the Hawthorne effect (people work differently when measured) (p. 307).
5. **Caveat.** The abstract says COPQ fell "about 24%", which does not match the tables. Cite the tables. Only internal failure was measured.

**Key takeaways for ITW601:**
- **The awards work has every category.**
  - Prevention: the written rules note.
  - Appraisal: the mark-by-mark comparison after release, and the zero-difference check.
  - Internal failure: the Year 11 rebuild on provisional marks.
  - External failure: the seven-versus-four unranked claim that reached the stakeholder before I corrected it.
- **Measuring changes behaviour.** Margin question for the Hawthorne point: has logging every rebuild and correction changed how quickly I call a round final?

---

### 5. Quality means different things to different people

**Citation:** Zhang, Q. (2001). Quality dimensions, perspectives and practices: A mapping analysis. *International Journal of Quality & Reliability Management, 18*(7), 708-721.

**Purpose:** a framework that relates how quality is defined (dimensions), viewed (perspectives) and managed (practices), so a firm can position its quality management (p. 708).

**The map (pp. 714-718):** two axes, **internal vs external focus** and **objective vs subjective measurement**.
- Objective measures reduce uncertainty: more data, such as defect rates and conformance.
- Subjective measures resolve ambiguity: shared interpretation, such as customer satisfaction.
- Garvin's eight dimensions sit across the map: performance, features, reliability, conformance, durability, serviceability, aesthetics, perceived quality. Conformance is internal and objective; perceived quality is external and subjective (p. 709, Fig. 4).

**Themes:**

1. **People along the delivery chain value different dimensions** (P1). Design cares about features; production cares about conformance.
2. **Successful firms integrate both kinds of measure** (P3, P4).
3. **Internal quality comes first.** "The internal focus on quality is the precondition to achieving the external focus" (p. 719, P5).
4. **Measurement makes work visible.** "Measurement provides a scorecard for business performance and makes accomplishments visible to everyone" (p. 715).
5. **TQM is never done.** "TQM organization is dynamic and is constantly striving to improve" (p. 714).

**Key takeaways for ITW601:**
- **Penzenstadler's two routes are Zhang's two axes.** A countable metric is objective. A user group's rating is subjective.
- **For the awards page:**
  - R1 (zero differences) is internal and objective, and it has to hold first (P5).
  - The academic lead calling the ranking fair is external and subjective. A2 needs both.

---

## Activity 1 video: quality requirements (Penzenstadler, 2018)

Penzenstadler opens with an iPhone against an Android phone: quality is not absolute, so first choose a quality model. ISO 25010 is the standard starting point. Then write every quality requirement in four parts:

| Part | Performance example | Usability example |
|---|---|---|
| Description | The system should respond fast | The system should be easy to use |
| Metric | Response under half a second | 90% of test users rate ease of use 9/10 |
| Measurement | 25 test users run use cases 34 and 35 | 100 beta testers rate it after 15 minutes |
| Rationale (the why) | Otherwise users switch service | User retention |

A qualitative requirement has two routes: break it into countable sub-requirements (font size, contrast, under seven clicks), or keep it qualitative and define who rates it and how.

**For ITW601:** R4 (source and run date on every view) in this format:
- Description: staff can see how old the data is.
- Metric: both labels present on every view.
- Measurement: a test per view, and the review check.
- Rationale: fitness for use is judged by the consumer.

---

## Links to the rest of the term

```
Module 7 (communicate)  -> Module 8 (justify)         -> Module 9 (assure quality)
check it landed            tree, CBA, acceptance        PDCA per process, COQ,
                                                         quality requirements with a why
```

- **A2 (due Sun 15 Nov):** the R1-R4 table is a set of quality requirements. Each has a description and an acceptance check, and the rationale sits in §3. Basu's success criteria vs factors and Mahmood's prevention vs failure costs are optional one-line upgrades if words allow.
- **A3 (due 2 Dec):** the activity says this module feeds the "elicitation requirements aspect" of A3. The Project Synopsis Review can restate R1-R4 in Penzenstadler's four parts and report plan against execution as a COPQ ledger: what was prevented, what was caught in appraisal, what failed internally, what reached a stakeholder.
