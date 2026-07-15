# Module 7 - Class Notes (Week 7 Live Lecture)
## Autoencoders · Dr. Tayab Din Memon

> **Source:** Week 7 live lecture, 15 July 2026, ~1h25m, Dr. Tayab Din Memon (Teams recording). This file captures what the **lecture** added on top of the four readings in [module07_notes.md](module07_notes.md). Where they overlap (encoder/decoder, undercomplete, sparse/denoising/contractive, PCA equivalence) the resource notes carry the detail.

---

## TL;DR
- Autoencoder = **input → compress to latent → reconstruct**, unsupervised (input *is* the target, no labels). His analogy: a **small suitcase** - you can't fit everything, so you pack only the essentials, then "magically" unpack (reconstruct) on arrival. The essentials = the **latent space**.
- His answer to the headline question: AEs beat PCA because they learn **nonlinear** patterns (PCA/ICA are linear only), learn the features **by themselves** (neural net vs a variance calculation), and cost more **training time** in exchange for that power. *"Autoencoders outperform PCA for many non-linear problems - but it comes with a cost."*
- He walked a concrete pipeline: **flower image, 784 px (28×28×1) → 128 → 32 (latent) → 128 → 784**; reconstruction is *lossy* but recognisable.
- **Anomaly detection is confirmed** as a real application (he listed it under sparse AEs and in the applications table: manufacturing, cybersecurity) - alongside denoising, **colorization**, **watermark removal**, document/medical-image restoration, compression, and deepfakes.
- **A2 logistics changed vs the brief:** he wants **7-10 min presentation + 4-5 min Q&A**, presented **live in class in week 8 or 9**. Our group agreed to present live. If you present in class, the class recording counts as submission - just hand in **PPT + report**.
- Spent a lot of the class on **deepfake ethics** ("should society regulate deepfake technology?") - that debate is Activity 2 fuel.

---

## 0. The PCA-vs-AE question - his answer vs mine 🔴
The pre-class prompt: **"How is an autoencoder different from PCA? Both reduce dimensionality, so what additional capability does an autoencoder provide?"** He also ran a **recap quiz** on Module 6 first (PCA = reduce dimensionality while retaining variance; ICA = separate mixed signals / cocktail party; SFA = features that change slowly; sparse coding = fewer active features).

- **My prepared answer (from the readings):** an **undercomplete** AE with **linear** encoder/decoder + **MSE** loss *is* PCA at the global optimum (Baldi 2012). The extra capability is **nonlinearity**, **depth/stackability**, and **a choice of regularizer**.
- **What he actually said:** the difference he stressed is **linear vs nonlinear** and **maths-based vs learned**. He showed a PCA-vs-AE slide/table:

  | | PCA / ICA | Autoencoder |
  |---|---|---|
  | Method | mathematical - checks **variance** | **neural network** - learns features itself |
  | Relationship | **linear** only | **nonlinear** (the key advantage) |
  | Speed | **fast** (it's just maths) | **slower** - needs training time |
  | Power | limited to linear structure | more powerful, learns reconstruction |

- **Delta - what he did NOT go into (so my notes are the deeper version):** he did **not** state the Baldi result (linear AE ≡ PCA at the optimum, no local minima, top-`p` eigenvectors). He kept it applied/intuitive and deliberately **stripped the maths out** ("I have taken out the mathematical equations... you may not be using them"). So Zone 2 of the one-pager is *more rigorous than the lecture* - good for a written answer, but in the forum keep it at his level: linear+fast+variance vs nonlinear+slower+learned.

## 1. His framing + the suitcase analogy
- Module opened with a **Module 6 recap** (why reduce dimensions: computational cost + keep only what matters for variance), then: *why two encoders / why autoencoders → how they work → applications → ethics → activities → assessment link.*
- **The suitcase analogy (worth reusing):** big thing won't fit → keep only essential parts → unpack and reconstruct on arrival. Input → compress → store essentials → reconstruct. The "essentials" are the **latent space**.
- **The problem statement he used:** real data is *large, noisy, redundant, hard to process* → learn a **compact representation that preserves the most important information** → cheaper computation.
- **Bottleneck = the central question:** *"how many features are sufficient to reconstruct the original image?"* More compression → more information loss. He used the **4K photo → 4 numbers** thought experiment (would you still recognise the person?) to make the compression-vs-quality trade-off concrete.

## 2. Encoder + decoder - when do you need both? 🔴
He asked this explicitly and it landed on **my** point:
- **Training + validation:** you need **both** (Nomayer's answer - decoder must produce something, error is computed, weights adjust, repeat until reconstruction is acceptable).
- **Inference / a downstream task:** you may only need the **encoder** - e.g. **use the compressed code to train a classifier** (my point in class; he confirmed it, framed it as semi-supervised use). *This is exactly the "decoder is scaffolding for representation use" line in the one-pager - now lecturer-confirmed.*

## 3. Applications he emphasised
The email named four; the lecture broadened them into a table. **Anomaly detection is confirmed** (no longer pending).

| Application | His example |
|---|---|
| **Compression** | reduce storage size; the core motivation |
| **Image denoising** | remove image noise; reconstruct clean from noisy |
| **Colorization** 🆕 | convert grayscale → colour |
| **Watermark removal** 🆕 | restore images (Nomayer said he'd used a tool for this) |
| **Document / medical-image restoration** | denoising AE application |
| **Anomaly detection** ✅ | listed under **sparse AEs**; domains = **manufacturing, cybersecurity** |
| **Deepfake generation** | "first generation" of this tech; the whole ethics segment |

- ⚠️ **Nuance for honesty:** he named anomaly detection as an *application area* (esp. for sparse AEs) but did **not** drill into the **reconstruction-error-as-score** mechanism. That mechanism (train on normal only → high reconstruction error = anomaly) is my/textbook framing, not something he stated - keep them separate in a written answer.
- He did **not** cover semantic hashing, and did **not** detail the two-AE-shared-encoder deepfake mechanism (that stays sourced to Dickson 2020).

## 4. The variants - how he described them
Kept deliberately maths-light. His one-liners:
- **Basic AE** - learn, compress, reconstruct (compression + feature learning).
- **Undercomplete** - latent smaller than input → forces keeping only the most important info (dimensionality reduction + representation learning; the one he paired directly with PCA).
- **Sparse** - keep only a **small number of neurons active** (L1 regularization); feature extraction, anomaly detection.
- **Denoising** - reconstruct **clean output from noisy input**; *"learns a projection from a neighbourhood of the training data back onto the training data"* (his words = the manifold/score idea, stated intuitively).
- **Contractive** - learn **stable features that don't change when the input changes slightly** (reduce sensitivity). His example: a **face-recognition system should still recognise the same person if the image is slightly brighter, darker, or shifted**.
- **Overfitting prevention:** *"autoencoder avoids memorising data by using the bottleneck layer"* + regularization (L1 / contractive penalty) controlling how much info passes. → this is his Activity 3 answer in one line.

## 5. Class discussion (fuel for the activities)
- **Deepfake ethics debate** ran long: *"should society regulate deepfake technology?"* Risks he named: **fraud, identity theft, political misinformation**, voice cloning, misuse in low-governance regions. Good material for Activity 2's *ethical* framing (lead with consent/regulation).
- **Nomayer's tangent** (video → marketing insights) and my Reddit-tool share - not examinable, but shows he rewards active contribution ("thank you for making this class interactive").
- **Supervised vs unsupervised** got re-confirmed live: AE is unsupervised because **input = target, no labels**.

---

## 6. Assessment - what actually changed 🔴🔴
**This supersedes the README's A2 row for logistics** (the brief still governs word count / weighting):

- **Format:** **7-10 min presentation (max) + 4-5 min feedback / discussion / Q&A.** (README says "5-7 minute presentation" - his in-class number is **7-10**; go with his.)
- **When:** present **live in class, week 8 (next week) or week 9** (class is Wednesday). **Our group (Luis / Victor / Juan) agreed to present live.**
- **Three accepted options:** (1) present live in class ← his preference, (2) record it, play it in class, discuss, then submit, (3) record and just submit (no discussion). Options 1-2 preferred for peer learning + instant feedback.
- **If presenting live:** no need to separately record/upload - **the class recording counts as the submission.** Deliverables = **PPT file + report.**
- **If recording:** your **face must be present**, at least the first minute.
- **Deadline unchanged:** A2 due **26/07/2026** · 1000-word report ±10% · group · 30%.

- **A3** (Final Project · source code + 1500 words · group · 40% · due **19/08/2026**): still the module where we *"identify possible uses of autoencoders and investigate possible input datasets."* No new constraints given this class.

- **Questions still worth asking him:**
  1. For Review Pulse (sentiment on ~1,159 reviews), is a **stacked denoising autoencoder** (Glorot et al. 2011b) a credible baseline to cite/compare against, or purely historical next to DistilBERT?
  2. Does he want an autoencoder *in* the A2 proposal, or is the M7 material background context?

### The three discussion-forum questions (he wants ALL THREE answered, before leaving class)
1. **How do autoencoders differ from PCA, and when would you prefer one over the other?** (= Activity 1 Comparison)
2. **Describe an ethical application of deepfake technology that could benefit society.** (= Activity 2 Fake to Real)
3. **Do you agree that autoencoders can overfit? Justify your answer with an example.** (= Activity 3 Discussion)

---

### Day-job anchors
1. **Anomaly detection** *(his confirmed application; the reconstruction-error mechanism below is my framing, not his exact words)*: train an AE on only the "normal" nightly ETL rows; flag any row whose reconstruction error passes a **calibrated** threshold. Learned validation rules instead of hand-coded ones. Caveats: a high-capacity AE reconstructs anomalies too, near-normal anomalies slip through, threshold needs validation tuning.
2. **The suitcase = your warehouse star schema.** You don't ship every raw column to the model; you keep the essential features that reconstruct the signal. An AE learns *which* essentials automatically instead of you hand-picking them.
3. **PCA vs AE trade-off = your "SQL view vs trained model" choice.** PCA/a SQL aggregation is fast and linear; an AE is slower but captures nonlinear structure in the student indicators. Pick by whether the relationship is linear and whether you can afford the training cost.

---

## References
Full citations, links and page-level detail live in **[module07_notes.md](module07_notes.md)**. The shorthand used above resolves as:

- **Goodfellow, Ch.14** - Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep learning.* Cambridge, MA: MIT Press. https://www.deeplearningbook.org/
- **Baldi (2012)** - Baldi, P. (2012). Autoencoders, unsupervised learning and deep architectures. *PMLR 27*, 37-49. http://proceedings.mlr.press/v27/baldi12a/baldi12a.pdf
- **Bengio (2012)** - Bengio, Y. (2012). Deep learning of representations for unsupervised and transfer learning. *PMLR 27*, 17-36. http://proceedings.mlr.press/v27/bengio12a/bengio12a.pdf
- **Glorot et al. (2011b)** - cited *in* Bengio (2012); stacked denoising autoencoders with sparse rectifiers for domain adaptation in sentiment classification.
- **Dickson (2020)** - Dickson, B. (2020, 5 March). What is a deepfake? *PCMag Australia.* https://au.pcmag.com/news/65869/what-is-a-deepfake
- **Alain & Bengio (2013)** - the small-noise result linking DAE reconstruction to the data score.
- **Dr Tayab Din Memon** - week-7 pre-class email (applications list; pre-class PCA question).
