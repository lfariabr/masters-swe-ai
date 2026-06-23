# DLE602 Assessment 2 - Team Brief

*One-pager to get us aligned before we start writing. Read in 3 minutes, reply with your surname + student ID and any pushback.*

## The project (one sentence)

> **Review Pulse v2** - an aspect-based sentiment analysis (ABSA) system that predicts sentiment **per aspect** of a customer review (e.g. *food = positive, service = negative*), comparing an **attention-LSTM** with a **fine-tuned transformer**, plus an **attention-visualisation** layer for interpretability.

**Why this topic.** Normal sentiment models give one label per review. A real review like *"the food was great but the service was slow"* needs two opposite labels - one per aspect. That gap is the whole point, and it is the natural deep-learning successor to the sentence-level sentiment work from Assessment 1.

## What A2 actually is (important)

A2 is a **proposal**, not the build. The build is A3 (same project, implemented in Python). So this assessment is about **reading good papers, writing a sharp proposal, and planning A3 well** - not coding yet.

| Item | Detail |
|---|---|
| Deliverable | 1,000-word report (+/-10%) **+ 5-7 min audio-visual presentation** (PDF slides) |
| Type / weight | Group (the three of us) / 30% |
| Due | Sunday end of Module 8 - **26/07/2026, 11:55pm AEST** |
| Format must-haves | Cover page (names + IDs + project name), table of contents, abstract, page numbers in footer, captioned figures/tables, word count before references, **APA** referencing |

## Where the marks are (so we spend effort right)

| Criterion | Weight | Owner (proposed) |
|---|---:|---|
| Analysis & synthesis of literature | **25%** | Lit lead |
| Project planning & management (plan + risk + contingency) | **25%** | PM lead |
| Problem statement & aim | 20% | Impl lead |
| Overall structure & flow | 15% | PM lead |
| Audio-visual presentation | 15% | All three (equal speaking time - required) |

Half the marks are literature synthesis + project planning. We invest there.

## Suggested roles (adjust freely)

- **Luis - Implementation / methods lead.** Problem statement, aim + research questions, methods section (models, datasets, evaluation), technical feasibility into A3.
- **Member B - Literature lead.** The critical synthesis (the 25% section): compare CNN vs attention-LSTM vs BERT vs the recent LLM/generative work, position our project in the gap. Own the APA reference list.
- **Member C - Project management lead.** Activity plan + milestones to A3, risk register + contingency, document assembly (cover, ToC, formatting, word count, page numbers).
- **All three** present for roughly equal time and review each other's sections before submission.

## Timeline (mapped to the modules - it lines up on purpose)

| Window | Module | What we do |
|---|---|---|
| ~30 Jun | M5 (CNN) | Lock the 4-6 paper set; each owner drafts their section |
| ~7 Jul | M6 | Assemble first full draft of all sections |
| ~14 Jul | M7 | Internal review, cut to 1,000 words, build the 6-slide deck |
| ~21-26 Jul | M8 (RNN/LSTM) | Record the presentation, APA pass, submit by Sun 26/07 |

By the time we submit we will have covered CNN (M5) and LSTM (M8) - exactly the two model families we compare.

## Two decisions to confirm with the group

1. **Topic Modelling** - do we include it? Recommendation: keep it as an **optional/stretch** stage (a neural topic model that *discovers* aspects when there are no gold labels) plus an exploratory topic-map figure. It strengthens the story but must not threaten the core deliverable. It becomes "RQ4" only if we all want it as a first-class contribution.
2. **Scope** - we classify sentiment on **given (gold) aspects** (SemEval-2014 Restaurants/Laptops). Full aspect extraction stays a stretch goal so A3 is feasible on free Colab.

## What I need from each of you this week

1. **Your surname + student ID** for the cover page.
2. A thumbs-up (or pushback) on the topic and the Topic Modelling decision.
3. Which role you want.

Full working plan with the literature spine, methods, and risk register is in the repo: `Assessment2/DLE602_Assessment2_Proposal_Skeleton.md`.
