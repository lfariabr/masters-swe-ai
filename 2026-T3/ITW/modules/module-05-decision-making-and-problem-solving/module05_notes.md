# Module 05 - Decision Making and Problem-Solving Skills in Project Management

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| 1 | Read & summarise Samuel & Weir (1999) - Part 1 (Ch. 1, modelling and synthesis) and Part 2 (Ch. 6, problem-solving strategies) | 🕐 |
| 2 | Watch & summarise Wujec (2013) - Got a wicked problem? First, tell me how you make toast (TED, 9 min) | 🕐 |
| 3 | Watch & summarise RedVectorOnline (2016) - Effective decision making, problem solving and critical thinking for engineers (5 min) | 🕐 |
| 4 | Activity 1: Discussion forum post, presenting the project's problem-solving methods to stakeholders | 🕐 |

> Resource rows stay 🕐 until Luis confirms the reading or viewing. The summaries below are study aids built from the local copies and transcripts.

---

## Key Highlights

### 1a. Samuel, A. E., & Weir, J. (1999). Part 1: Modelling and synthesis (Chapter 1).

**Citation:** Samuel, A. E., & Weir, J. (1999). *Introduction to engineering design: Modelling, synthesis and problem-solving strategies*. Butterworth-Heinemann. Ch. 1, first 20 pages.

**Purpose:** Opens the book with design for structural integrity: what failure is, why engineers study it, and how estimation and simple models support judgement. Local copy: [r1a_samuel-weir-part1-modelling-and-synthesis.pdf](r1a_samuel-weir-part1-modelling-and-synthesis.pdf).

---

#### 1. Structural integrity in three words
- A component must withstand **service loads**, **effectively** (within specified stress or deflection limits) and **efficiently** (at least cost or least mass).
- **Service loads are the creative part.** They are often unknown and must be estimated before design starts, then checked by prototype or field test.
- **Design time is a cost too.** An experienced designer does not spend expensive hours saving a few grams on a cheap part.

#### 2. A model is not the real thing
- Analysis results describe **the model's behaviour, not the component's**. Experienced designers still forget this.
- **Tacoma Narrows:** wind was modelled as a static sideways load, but the light deck failed through twisting vibration nobody had modelled.
- **Comet airliner:** fatigue cracks at sharp window corners, where the designers underestimated how variable fatigue data is.

#### 3. Four propositions about failure
| # | Proposition |
|---|---|
| 1 | Engineers study failure so they can build tools that avoid it, and failures reveal cause and effect too complex to model |
| 2 | Failures are **technical** (not enough information), **operational** (wrong use) or **unpredictable** (special circumstances) |
| 3 | The incentive to prevent a failure grows with its **failure intensity**: economic, environmental or social impact |
| 4 | Any system fails under extreme enough conditions. Set specifications for acceptable risk, and cover the limits of know-how with **factors of safety** (the authors call them factors of ignorance) up to the **worst credible accident** |

#### 4. Learn, don't blame
- Inquiries usually ask who is to blame and who pays. The authors focus on the **technical cause**, so a whole class of failure can be prevented.
- **Insurers price experience:** a new technology with no loss data is high risk until experience accumulates (their example is early space insurance).
- **Estimation:** a "back of the envelope" estimate from known facts (their example estimates a state's yearly births at 60,000 against an official 60,650) is the base of engineering judgement.
- **Structural distillation:** treat a complex structure as a set of simpler elements whose behaviour you already understand.

#### Key Takeaways for ITW601
1. "The model is not the component" is my A1 lesson in another form: a report view refreshed recently is a model of the data, not proof that the data is complete.
2. The three failure types give A2's ICT challenges a structure: technical (a report view missing some Semester 1 rows), operational (rules living inside scheduled jobs), unpredictable (an upstream system change).
3. Failure intensity justifies priority: wrong award rankings reach students and families, so they are worth checking before anything else.

---

### 1b. Samuel, A. E., & Weir, J. (1999). Part 2: Problem-solving strategies (Chapter 6).

**Citation:** Samuel, A. E., & Weir, J. (1999). *Introduction to engineering design: Modelling, synthesis and problem-solving strategies*. Butterworth-Heinemann. Ch. 6, pp. 267-286.

**Purpose:** Explains how a vague need becomes a workable design problem: the designer's role, the generic design procedure, problem evolution with the client and "enformulation". Local copy: [r1b_samuel-weir-part2-problem-solving-strategies.pdf](r1b_samuel-weir-part2-problem-solving-strategies.pdf).

---

#### 1. Design is a discipline, not a science
- Tools (CAD, decision support systems) help, but the **front end stays human**: recognising that a need exists and negotiating it into objectives, requirements and success criteria.
- A science needs testable, refutable rules. Design has none, so the design method is **sufficient but not necessary**: it helps, but nobody can prove it is the only route to a good design.
- Design has three components: the **designer** (often a team, so conflict handling matters), the **procedure** and the **product** (domain knowledge does not transfer easily).
- **Case studies teach the journey, not the destination.** Copying a similar solution misreads them.

#### 2. The designer's key skill
- Processing **large amounts of diverse information in an orderly way**, especially when many requirements are never spoken by the client.
- Choosing the best (or a satisfactory) set of **compromises**.

#### 3. The generic procedure (helicopter and mousetrap examples)
```
NEED -> DESIGN GOAL -> TECHNICAL OBJECTIVES + REQUIREMENTS (limits)
     -> SOLUTION ALTERNATIVES -> DECISION -> CLEAR SPECIFICATIONS
```
- **Evolutionary** designs improve an accepted product; **inventive** ones bring new technical content.

#### 4. Hard, soft and content-free information
| Type | Example from the chapter | What to do |
|---|---|---|
| **Hard** | A measured road-death rate compared across states | Use it to size the effort |
| **Soft** | "There are too many road deaths" | Harden it with data |
| **Content-free** | "Our public transport system is inefficient" | Avoid it; it carries no information |

- **Design vs trouble-shooting:** design plans action toward a goal and the problem evolves; trouble-shooting corrects a specific, well-defined deviation.

#### 5. Problem evolution is a negotiation
- Most problems arrive **solution-oriented** ("build a better mousetrap"). That framing is the most severe restriction on the search. Two sayings from the chapter: what you want is not necessarily what you need, and designers are always told to "fix it, but don't change a thing".
- **Need-directed** statements are vague, with goals unspoken. **Goal-directed** statements name the goal. Design cannot start until client and designer agree on goals.
- **Forward chaining:** move from need to goals, objectives and embodiments. **Backward chaining:** a design review that asks "what is the real essence of the problem?" (the car example: buy the sedan and join a racing club to get the excitement).
- **Bug list and idea-log:** list what bugs you, agree one problem as a team, and keep a dated log of ideas and sketches as the problem evolves.

#### 6. Enformulation: from soft problem to technical objectives
- Turn soft information into hard by finding **islands of certainty**: data, budget, statutory constraints and **windows of opportunity**.
- **Bicycle-theft example:** "too many bikes are stolen" became 30,000 students, about 3,000 bikes left outside, about $325,000 lost a year, a budget, a July deadline for the minor-works round, and requirements (1,000 bikes per module, cost per module, a mandatory standard).
- **Level-crossing case:** before designing, ask how serious the problem is, what it costs, how much can be spent and where effort is best placed.

#### Key Takeaways for ITW601
1. **A2 synopsis method:** "build Student360" is a solution-oriented statement. The need underneath is staff trusting one academic view, with award rules applied the same way every time. Saying this explicitly is backward chaining, and it justifies the read path first.
2. **Islands of certainty for A2:** the agreed award rules (Years 7-10 mandatory subjects only), the source map with its known gaps, and the delivery window are the hard facts the synopsis should stand on.
3. **Content-free trap:** "the data is messy" carries no information. Name the specific gap instead.
4. The control journal and evidence log are my idea-log: dated records of how the problem evolved.

---

### 2. Wujec, T. (2013). Got a wicked problem? First, tell me how you make toast.

**Citation:** Wujec, T. (2013, June). *Got a wicked problem? First, tell me how you make toast* [Video]. TED. https://www.ted.com/talks/tom_wujec_got_a_wicked_problem_first_tell_me_how_you_make_toast

**Purpose:** A designer uses a three-part drawing exercise to show how teams make their mental models visible and align on a complex problem. Transcript: [r2_wujec-wicked-problem-toast-ted-transcript.md](r2_wujec-wicked-problem-toast-ted-transcript.md).

---

#### 1. Nodes and links
- Every "how to make toast" drawing is a **systems model**: nodes (things and people) and links (how they connect). Drawing makes a private mental model visible.
- Drawings reveal **points of view**: some show the toast, some the toaster, some the people, some the supply chain.
- **Sweet spot: 5 to 13 nodes.** Fewer looks trivial; more than 13 causes "map shock".

#### 2. Three rounds of the exercise
| Round | Medium | What happens |
|---|---|---|
| 1 | Pen and paper, alone | 4 to 8 nodes, one point of view |
| 2 | Sticky notes, alone | More nodes and clearer logic, because cards are easy to move. Ease of change drives willingness to improve the model |
| 3 | Sticky notes, as a group | Messy at first, then a unified model of 20 or more nodes with no map shock, because everyone built it. Silent groups work faster |

#### 3. The practice
- Start with a question, collect nodes, refine, repeat until patterns emerge. **The conversation matters more than the model.**
- His example: a publisher's executive team mapped its whole business over three days and reported recovered revenue and better customer ratings, which he credits to alignment. That is his account, not an audited result.

#### Key Takeaways for ITW601
1. **A2 figure:** keep the Student360 data-flow diagram between 5 and 13 nodes so a sponsor reads it at a glance.
2. **Weekly checkpoint:** a model built with the academic stakeholder beats one I present to them, because they own it.
3. Movable cards are the Kanban board I already use: easy to change, so the plan keeps improving.

---

### 3. RedVectorOnline. (2016). Effective decision making, problem solving and critical thinking for engineers.

**Citation:** RedVectorOnline. (2016, April 28). *Effective decision making, problem solving and critical thinking for engineers* [Video]. YouTube. https://www.youtube.com/watch?v=Ie50Q4h4J4k

**Purpose:** A short training clip that sets out an eight-step problem-solving process, paired with the OODA loop, to reduce emotion and confirmation bias in decisions. It is the video for Activity 1. Transcript: [r3_redvector-decision-making-video-transcript.md](r3_redvector-decision-making-video-transcript.md).

---

#### 1. The goal
- Remove as much **emotion, subjectivity and bias** as possible: the habit of choosing what we already know and looking only for supporting evidence.
- Pair the eight steps with the **OODA loop** (observe, orient, decide, act), Colonel John Boyd's decision cycle. The clip's narration says "detect", but Boyd's loop is usually given as "decide".

#### 2. The eight steps
| # | Step | Key point |
|---|---|---|
| 1 | **Clarify the problem** | Four types: broken (fix it), opportunity (improve it), unexplained (find why), new initiative (make it happen). Write a problem statement covering what, where, when, who, why, how and impact |
| 2 | **Break it down, find the gap** | Collect data before solving: visit the site, talk to people, look for gaps and bottlenecks |
| 3 | **Set improvement targets** | Where do we want to be? |
| 4 | **Find root causes** | Causes, not symptoms. Ask "why" five times |
| 5 | **Develop options** | Rule of thumb: three options, judged on effectiveness, feasibility and impact |
| 6 | **See options through** | Implement, then measure against the target |
| 7 | **Confirm results and process** | If the result misses, go back to an earlier step |
| 8 | **Standardise** | The most skipped step: write a standard operating procedure so the success repeats and new staff can follow it |

#### Key Takeaways for ITW601
1. **The awards rebuild already follows the eight steps:** the problem (rankings that must match the agreed rules), data (source map), target (totals that match the rules), root cause (rules embedded in jobs), options, implementation, checks against what teachers see, and the written rules note as the standard procedure.
2. **Three options for A2:** read path on existing tables, curated layer first, or the manual workbook. Comparing all three is what the 30% plan criterion rewards.
3. **Step 8 is my Phase 2:** versioned award rules are the standard operating procedure.

---

## Module 5 at a glance
```
Frame (Samuel & Weir Ch. 6):  need -> goal -> objectives + limits -> alternatives -> decision -> spec
                              soft -> hard via islands of certainty  ·  avoid content-free statements
Judge (Samuel & Weir Ch. 1):  the model is not the thing  ·  technical / operational / unpredictable failure
Align (Wujec):                nodes + links, 5-13 nodes, build the model with the group
Decide (RedVector):           8 steps + OODA: clarify -> data -> target -> root cause -> 3 options
                              -> implement -> confirm -> standardise (SOP)
                                  \__ A2 synopsis: justify the chosen option against the others
```
