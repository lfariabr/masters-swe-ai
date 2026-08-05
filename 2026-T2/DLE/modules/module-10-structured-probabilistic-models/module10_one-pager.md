# DLE602 · Module 10 - One-Pager

> **Structured Probabilistic (Graphical) Models · why the joint table explodes · directed vs undirected · partition function & intractable inference · energy-based models / RBM · the deep-learning twist · PGMs as a scientific bridge**
> A fast, hand-write-it-yourself sheet. Built for 3 pens on a blank A4 (landscape).

**Pen legend:** 🖤 Black = skeleton / always-true · 🔵 Blue = definitions & examples · 🔴 Red = exam + assessment hooks

---

## 🖤 The Big Idea (box it, centre of page)
> **A structured probabilistic model = a graph that describes a probability distribution. Nodes = random variables, edges = *direct* interactions. The power is in the edges you LEAVE OUT - every missing edge asserts a conditional independence, which is what lets you escape the impossible `2ⁿ` joint table. Draw only the direct relationships; the indirect ones are implied for free.**
> (Goodfellow, Bengio & Courville 2016, Ch.16 · Murphy 1998 · Airoldi 2007 · **Wk 11 lecture**)

🔵 **The one-line intuition:** you can't store a table for "every combination of every variable." So you write down *only who directly talks to whom*, and let the graph imply the rest.

---

## 🖤 Zone 1 - Why the joint table explodes (and how a graph saves you) ⭐
- 🖤 **The blow-up:** a lookup table over `n` binary variables has `2ⁿ` rows - **each new variable DOUBLES the table.** `2³⁰⁷²` for a 32×32 RGB image = more rows than atoms in the universe → can't store, fill, or sum it. This is **"unstructured" modelling** (every interaction between every subset).
- 🔵 **Student framing:** 4 yes/no facts about a girl (`A` absent · `B` disengaged · `C` low maths · `D` behaviour flag) → `2⁴ = 16` rows. Scale to hundreds of signals and it's hopeless.
- 🖤 **The fix = model only DIRECT interactions.** Most variables interact only *indirectly*; drop those edges.
- 🔵 **Relay race (Alice→Bob→Carol):** Carol depends **only on the previous stage (Bob)**; once you know Bob, Alice adds nothing → **erase the Alice→Carol edge.** (= the *Markov property*.)
- 🔴 **The payoff number:** relay-race full table ≈ **1,000,000** params → with 2 edges ≈ **19,899** (×50). Cost drops `O(kⁿ) → O(kᵐ)` when each node has few parents (`m ≪ n`).
- 🔴 **Classification vs structured prediction (class agenda):** *classification* = input → **one label**, can ignore most of the input (cheap). *Structured prediction* = **interdependent outputs at once** (segment every pixel, label every word, sample a whole image) → needs the full joint → **the job graphical models exist for.** (Review Pulse: doc-level sentiment = classification; aspect-level = structured prediction.)

## 🖤 Zone 2 - The two languages: directed vs undirected ⭐ Activity 1 - THE FORUM CORE
- 🖤 Two ways to draw the direct interactions; the **edge semantics** differ:

| | **Directed** (Bayesian / belief net) | **Undirected** (Markov random field) |
|---|---|---|
| Edge | arrow `A→B` = `B`'s distribution defined by `p(B\|A)` (**factorisation**, *not* auto-causal) | plain line = symmetric **affinity**, no conditional |
| Factorises as | `p(x)=Πᵢ p(xᵢ\|Paᵢ)` | `p̃(x)=Π_C φ(C)`, then `÷ Z` |
| Use when | clear **order / one-directional** story | **mutual / symmetric**, no clear "who first" |
| Sampling | **ancestral** (cheap, in order) | **Gibbs** (expensive, multipass) |
| Can encode | immoralities (V-structures) | chordless loops ≥4 |

```
Directed (relay race):        Undirected (cold spreads):
  [Alice]->[Bob]->[Carol]       [Roommate]--[You]--[Coworker]
  arrows = ordered/causal        lines = mutual, either direction
```
- 🔴 **Neither dominates** - each encodes independences the other can't. Convert directed→undirected by **moralization** ("marry" co-parents); undirected→directed by **triangulation** (add chords). Each conversion *loses* some independence info.
- 🔴 **Trap:** a directed arrow is **NOT** intrinsically causal - "A causes B" is an *optional interpretation* you assume when the domain justifies it (formally it just means `B`'s CPD conditions on `A`).

## 🖤 Zone 3 - The machinery & the headaches (why it's hard)
- 🔵 **Undirected models store affinity scores, not probabilities.** To make them sum to 1 you divide by the **partition function `Z` = the sum of scores over ALL combinations** - which is *exactly* the astronomical thing you were avoiding → **`Z` is usually intractable** in deep learning.
- 🔵 **Energy-based models (EBMs):** write `p̃(x)=exp(−E(x))` → always positive, unconstrained optimisation. Any such form = a **Boltzmann distribution**; each energy term = an **"expert"** (product of experts).
- 🖤 **Separation / d-separation** = reading conditional independence off the graph. **Undirected:** path active iff *every* middle node is unobserved. **Directed flips at colliders:** active iff every non-collider unobserved **AND** every collider observed (or has an observed descendant).
- 🔴 **Explaining away (the star phenomenon):** V-structure `a→s←b`. `a`,`b` independent **until you observe `s`** - then they *compete* to explain it (= Berkson's / selection bias).
```
     [sick]      [vacation]        Observe "absent" -> sick & vacation
        \           /              become dependent: learn she's on
         v         v               vacation -> P(sick) drops.
        [absent = collider s]      (Observing a descendant does it too.)
```
- 🔴 **Exact inference is `#P-hard`** even with structure → deep learning **approximates**: **Gibbs sampling** (sample instead of summing), **variational inference** (swap the impossible `p(h\|v)` for a tractable `q`). Recurring trio across all 3 readings: **MCMC · EM · variational.**

## 🖤 Zone 4 - The deep-learning twist + the RBM ⭐ SLO c) (§16.7)
- 🖤 DL uses graphical models **very differently** from classical stats:

| Traditional GMs | Deep-learning GMs |
|---|---|
| few, hand-designed, **interpretable** latent nodes | **many** latent vars, training *invents* their meaning |
| sparse, hand-picked edges | dense, **matrix-parametrised** layers |
| exact / loopy belief propagation | **Gibbs / variational** (loopy BP almost never) |
| simplify until exactly computable | **tolerate the unknown** - grow power until *just* trainable |

- 🔴 **RBM (Restricted Boltzmann Machine) = the canonical example:** energy `E(v,h)=−bᵀv−cᵀh−vᵀWh`. **"Restricted" = no visible-visible or hidden-hidden edges** → `p(h\|v)` and `p(v\|h)` are **factorial** → efficient **block Gibbs sampling** + easy gradients (`∂E/∂Wᵢⱼ=−vᵢhⱼ`). Learns `h` as a representation (`E[h\|v]`).
```
  h1   h2   h3     <- hidden (latent); NO edges within a layer
   |\ /|\  /|
   | X | X  |      dense v<->h (one matrix W), sparse within-layer = the "restriction"
   |/ \|/ \ |
  v1   v2   v3     <- visible (observed)
```
- 🔴 **This is the 4th family from Module 9's thesis** - "*deep probabilistic models*" = graphical models. Module 10 is the *language* under RBMs/DBNs, HMMs, every latent-variable model.

## 🖤 Zone 5 - PGMs as a scientific bridge (Murphy + Airoldi) ⭐ Activity 3
- 🔵 **Murphy - directed models in the wild:** the **water sprinkler** net (`Cloudy→{Sprinkler,Rain}→WetGrass`), CPTs, diagnostic (bottom-up) vs generative (top-down) reasoning; fielded systems: **QMR-DT** (disease→symptom medical diagnosis), NASA **Vista**, MS Office assistant.
- 🔵 **Murphy - the 4 learning cases:** {structure known/unknown} × {full/partial observability} → **MLE · EM · search · Structural-EM**. Structure learning is NP-hard (BIC ≈ MDL penalty, asymptotically).
- 🔴 **Airoldi - the bridge (Activity 3 answer):** PGMs = "a common conceptual architecture where domain + mathematical objects share one formalism." Workflow: cartoon model → split **observable vs latent** → translate to RVs + dependencies → fit → interpret → new hypotheses. **COVID benefits** the same way genomics did: observable (PCR, symptoms, genome sequences) + latent (true infection state, transmission chains, variant lineages) → transmission-network inference + variant phylogenetics (cite the HIV-mutation & phylogenetic-tree precedents).

## 🔴 Assessment Hook (bottom red strip)
> **Assessment 3 - Deep Learning Final Project** · source code + 1500-word report (±10%) · **group** · **40%** · due **19/08/2026** · SLOs **c) d) e)**.
> Module 10 feeds A3 via *"consider structured and unstructured modelling where applicable"* (SLOs c/e). 🔴 **How to use it:** name the **representation-cost** argument (why you don't model every interaction) and, if you discuss generative/latent structure, use the graphical-model vocabulary (directed vs undirected, latent variables, why exact inference is intractable → you approximate). For **Review Pulse** the honest line: sentiment is a *discriminative* `p(y|x)` task, so a full generative graphical model is overkill - but the **latent-variable / distributed-representation** framing (your BiLSTM/embedding is `h`, an `E[h|v]` feature map) is exactly §16.5's argument.
> 🔴 **Tayab's pre-class reflection — *"does your project have variables that influence/depend on one another, representable as a graph?"*** Answer **yes, but shallowly**: words within a review depend on each other sequentially, and your **BiLSTM already IS an implicit chain graph** (HMM relative). Go **aspect-level (ATAE-LSTM v3.0.0)** → genuine **structured prediction** (interdependent aspect outputs per review, where a CRF-style graph would help). That is the non-forced Module 10 → A3 link.

## 🔴 If you only memorise 5 things
1. **The joint table has `2ⁿ` rows - doubles per variable.** A graph escapes it by drawing only **direct** interactions; every missing edge = a conditional independence = the saving.
2. **Directed (arrows, ordered/`p(B|A)`) vs undirected (lines, mutual/affinity).** Neither dominates; an arrow is **not** automatically causal.
3. **`Z` (partition function) + exact inference are intractable (`#P-hard`)** → approximate with **Gibbs / variational** (trio: MCMC · EM · variational).
4. **RBM = energy-based, "restricted" (no within-layer edges) → factorial conditionals → cheap block Gibbs.** The canonical DL graphical model.
5. **Explaining away:** observing a common child (V-structure) makes independent causes **compete** → they become dependent.

---

### Margin prompts (answer in blue while you write - anchor to your day job at St Cat's)
1. **Explaining away is your "why is this girl flagged?" problem.** *Absent today* has two competing causes: genuinely disengaged vs a one-off sick day. Write the V-structure, then say: once you confirm she had a medical certificate, what happens to your belief she's disengaged - and which real St Cat's signal is the "observed descendant" that would re-open the suspicion?
2. **Directed or undirected?** Classify two St Cat's relationships: (a) *effort mark → subject grade*; (b) *two friends in the same class both getting behaviour flags*. Which is an arrow, which is a plain line, and what's your one-sentence justification for each? (hint: can you name "who comes first / causes"?)

### This-week to-dos (still 🕐 in your notes)
- [ ] 🕐 **Activity 1** - Directed versus Undirected (≤100 words, forum): why do BOTH exist? → directed = ordered/causal story + cheap ancestral sampling; undirected = symmetric interactions + natural for approx inference. Neither dominates.
- [ ] 🕐 **Activity 2** - Advantages of Structured Modelling (≤100 words, forum): cheaper representation ⇒ fewer params ⇒ less data/memory + tractable-ish inference ⇒ DL can **scale** to images/audio/text a lookup table never could.
- [ ] 🕐 **Activity 3** - Graphical Models for COVID-19 (≤100 words, forum): yes - same observable/latent object split as Airoldi's genomics; use for transmission networks + variant phylogenetics.
