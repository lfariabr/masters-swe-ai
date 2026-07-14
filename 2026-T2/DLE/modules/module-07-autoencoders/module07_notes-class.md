# Module 7 - Class Notes (Week 7 Live Lecture)
## Autoencoders · Dr. Tayab Din Memon

> **Source:** Week 7 live lecture (TODO: date, duration), Dr. Tayab Din Memon. This file captures what the **lecture** added on top of the four readings in [module07_notes.md](module07_notes.md). Where they overlap (encoder/decoder, undercomplete, sparse/denoising/contractive, PCA equivalence) the resource notes carry the detail. This file focuses on the **lecturer's own framing**, the **applications not in Goodfellow Ch.14** (anomaly detection), the **demos/collaborative activities** run in class, and any **Assessment 2/3 hints**.

---

## TL;DR
> *(Write this LAST, after the lecture. 4-6 lines: the framing he used, the applications he emphasised, his answer to the PCA question, and anything that changes how you write A2.)*

TODO

---

## 0. Pre-class question - his answer vs mine 🔴
He asked us to come ready to discuss: **"How is an autoencoder different from PCA? Both reduce dimensionality, so what additional capability does an autoencoder provide?"**

- **My prepared answer (from the readings):** an **undercomplete** AE with **linear** encoder/decoder and **MSE** loss *is* PCA at the global optimum (Baldi 2012 - no local minima, global min = projection onto the top-`p` eigenvectors). The additional capability is **(a) nonlinearity**, **(b) depth / stackability**, and **(c) a choice of regularizer** that shapes what the code `h` keeps (sparse / denoising / contractive).
- **What he actually said:**

TODO

- **Delta - anything I got wrong or missed:**

TODO

## 1. His framing of the module
> *(How did he set it up? What was the one-sentence version he used? Did he use a different diagram/analogy from the codec one?)*

TODO

## 2. Applications he emphasised
The email named four: **image denoising · anomaly detection · data compression · deepfake generation**. Note **anomaly detection is NOT in Goodfellow Ch.14** - so this section is where it actually gets learned.

| Application | His mechanism / example | Anything examinable |
|---|---|---|
| **Image denoising** | TODO | |
| **Anomaly detection** ⚠️ | TODO - *did he confirm: train on normal only, reconstruction error = anomaly score, threshold it?* | |
| **Data compression** | TODO | |
| **Deepfake generation** | TODO - *did he cover the shared-encoder / swapped-decoder trick?* | |

TODO - anything he added beyond these four (semantic hashing? pretraining? VAEs as a forward-look?)

## 3. The regularized variants - what the lecture added
Readings already cover: sparse (`Ω(h)`, L1/Laplace) · denoising (`L(x, g(f(x̃)))`) · contractive (`λ‖∂f/∂x‖²_F`).

- **What he added / corrected:**

TODO

- **Did he give a rule for *which variant when*?**

TODO

## 4. Demos / code walkthrough
> *(HARMONY framework - he said there'd be demonstrations. Capture the dataset, the architecture, the framework (Keras/PyTorch), and the one result that made a point.)*

TODO

## 5. Collaborative / interactive activities
> *(What was the group task? What did other students argue? Anything that sharpens Activity 1/2/3.)*

TODO

---

## 6. Assessment hints 🔴
He wrote: *"This module also provides useful knowledge that can support Assessment 2, particularly if your project involves feature extraction, dimensionality reduction, image processing, or representation learning."*

- **A2** (Project Proposal Presentation · 1000 words + 5-7 min · group · 30% · due **26/07/2026**):

TODO - *does he want an autoencoder in the proposal, or is it optional colour? Any steer on scope/datasets?*

- **A3** (Final Project · source code + 1500 words · group · 40% · due **19/08/2026**):

TODO - *the delivery schedule says M7 is where we "identify possible uses of autoencoders and investigate possible input datasets, particularly for A3."*

- **Questions I want to ask him live:**
  1. For Review Pulse (sentiment on ~1,159 reviews), is a **stacked denoising autoencoder** (Glorot et al. 2011b) a credible baseline to cite/compare against, or is it purely historical framing next to DistilBERT?
  2. TODO
  3. TODO

---

### Day-job anchors
> *(Fill in after class - how does what he said map onto the school data warehouse?)*

1. **Anomaly detection** *(pending confirmation in §2 - this is the mechanism I expect, not one he has stated yet)*: train an AE on only the "normal" nightly ETL rows; flag any row whose reconstruction error passes a **calibrated** threshold. Learned validation rules instead of hand-coded ones. **Caveats to hold onto:** a high-capacity AE will reconstruct anomalies too, near-normal anomalies slip through, and the threshold must be tuned on validation data.
2. TODO
3. TODO

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
