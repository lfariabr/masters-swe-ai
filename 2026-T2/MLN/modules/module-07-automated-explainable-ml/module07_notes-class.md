# Module 7 - Class Notes (Week 7 live sessions)

Transcribed locally with `whisper.cpp` (`medium.en`) from the two recordings in this folder.
Sources: `Week 7 - Part 1 - Assessment 2 Discussion.txt` (83 min) and `Week 7 - Part 2.txt` (63 min).
Facilitator: Dr Kamran Shaukat.

> **Read this before the readings.** The two files are not the same weight. Part 1 is essentially the
> **Assessment 2 specification, dictated**, and is worth more than the PDF brief. Part 2 is the module
> lecture.

---

## The headline: the lecture never mentions Auto ML

The module is titled *Automated **and** Explainable* ML, but the 63-minute lecture is **entirely
explainability**. Auto ML, TPOT, HPO, NAS, meta-learning - none of it is said out loud, not once.

**Implication for revision:** Auto ML lives in the readings and is fair game for SLO a) (evaluate and
compare key concepts), but for **Assessment 2 it carries no weight**. The graded lever in this module is
XAI. Budget your time accordingly.

The second thing he is explicit about is *depth*:

> *"What is SHAP, what is its theory - we don't need to understand and go into detail. We are more into
> **how actually this could be implemented**."*

He wants three lines of code and a paragraph of interpretation. That is a low ceiling, which is exactly
why the [`activities/`](activities/) notebooks are worth more than they cost.

---

## Part 1 - Assessment 2, as dictated

### The target variable (get this exactly right)

He defines the binarisation himself, and the encoding is **counter-intuitive**:

| `quality` | label | meaning |
|---|---|---|
| `< 6` | **1** | **bad** quality wine |
| `>= 6` | **0** | **good** quality wine |

**The positive class is the *bad* wine.** Every recall / precision / SHAP sign in the notebook must be
read against that. (The submitted A2 notebook uses `df["quality_label"] = (df["quality"] < 6).astype(int)`
- aligned. But the Module 7 **activity** notebooks use `quality >= 7` = good, i.e. the opposite polarity.
Do not copy code between the two without flipping the reading.)

Red, white, or the two combined are all acceptable. 11 features. Same dataset as Assessment 1 - A1 was
the regression, A2 is the classification.

### The four levers he explicitly names for a high mark

He separates "the minimum" from the things that lift the grade, and lists them in order:

1. **Many models, but *explained*.** Not "I ran SVM, NB, DT, LR." He wants the rationale: *why* did this
   `C` win, *why* did Bernoulli NB underperform and Gaussian NB do well? He suggests the honest answer is
   often about the data ("there are no zero values, so...").
2. **SMOTE** if the classes are imbalanced. His words: *"if you are seeking the distinction, high
   distinction."* This is the one he ties directly to a grade band.
3. **`GridSearchCV`** with `cv=5` for hyperparameter tuning. He spent ~25 minutes on this and promised to
   post the code. Report `.best_params_` and `.best_score_`.
4. **Explainable AI.** *"I will give you the code. You just have to copy paste that code and explain it."*

### Submission: four files, no zip

He repeated this three times, so it clearly went wrong in A1:

| File | Note |
|---|---|
| `.ipynb` | the notebook itself |
| `.pdf` | **the same notebook**, exported. Not a separate Word document. |
| `.txt` | download the notebook as `.py`, paste the code into a plain-text file |
| `.mp4` | the video presentation |

**No zip, no rar, no compression.** Upload the four files individually.

### The video

- **7 to 10 minutes**, hard bounds ("not less than seven, not greater than 10").
- Screen recording of the **Jupyter notebook** + **webcam**. **No PowerPoint** - he was emphatic, twice:
  *"You don't need to prepare extra PowerPoint slides."*
- Show your **student ID card** and state your name at the start, for identity verification.
- Walk the CRISP-DM stages at altitude - not line by line. "Here is the box plot, here is what it told me."
- If the file is too big to upload, an unlisted YouTube / Drive / OneDrive link is fine, **but the
  permissions must let a stranger watch it** (a second marker may be the one opening it).

### Word count

> *"You don't need to worry about the word count."*

The 1,500 words are not the axis of marking. The explanation lives **inside the notebook**, and the
notebook is what gets read. He does not want a Word document - he says explicitly he doesn't want to waste
your time there, he wants that time spent on modelling.

### The A1 mistakes he told the cohort not to repeat

- **Didn't follow the CRISP-DM template.** Now mandatory for A2 and A3.
- **Correlation analysis with sign** - positive vs negative. *"Most of you have missed this thing."*
- **Pair plot analysis** - was advised, several skipped it. Mandatory.
- **Code without commentary.** Running the cell is not the deliverable; the induced knowledge is.
  *"It's not just you do the analysis. You have to tell us the rationale."*
- Searching for and adapting code is **encouraged** - copy-pasting it without explanation is not.
  *"The learning is where to search, how to search, then to fix that thing according to your data."*

### N-fold cross-validation (the long tangent)

Most of the middle of Part 1 is `GridSearchCV` + k-fold, prompted by a good student question about the
difference between the **validation** split and the **test** split.

His analogy is the useful bit: the **exercises at the end of each chapter are validation** (they check
your learning *while* you study); the **final exam is the test set** (it happens once, at the end, on data
the model has never touched). In a 10-fold run over 10,000 rows, each fold takes a turn as the validation
set - the held-out 1,000-row test set is never part of that rotation.

And the practical reassurance: **you do not implement the folding yourself.** `GridSearchCV(cv=5)` does it.
You still do your normal `train_test_split` first.

---

## Part 2 - the XAI lecture

### The motivation (all of it high-stakes framing)

He reuses the **balanced-accuracy** example from an earlier week: 93% accuracy that hides 3/10 recall on
COVID-positive cases. The point is that a headline metric can conceal a model that fails exactly where
failure is expensive. Same shape for malware detection and for immigration/visa screening.

Then the two questions that motivate XAI:
- **Interpretability** = observing cause and effect - *if I change this input, which way does the output
  move?*
- **Explainability** = describing, in human terms, *how the model got there under the hood*.

His worked example: fever + pain behind the eyes = seasonal flu; add vomiting = typhoid; add shivering =
malaria. That chain of if-thens is interpretability.

Domains he names: **finance** (credit decisions, loan approval, fraud), **autonomous vehicles**
(accountability after a crash), **healthcare** (diagnosis from imaging), **manufacturing**. And a nicely
close-to-home one: universities using AI to shortlist among 200 PhD applicants for a lecturer post - *"me
as an applicant want to know why my application was not shortlisted."*

He also names where you **don't** need it: low-risk, well-understood problems (the play-tennis decision
tree from the earlier module).

### The three tools he teaches

| Tool | What he shows | Scope |
|---|---|---|
| **LIME** | local interpretable model-agnostic explanations; the image example (segment the picture, score each region, the highest-probability label wins) | local |
| **SHAP** | `shap.TreeExplainer(model)` → `shap.summary_plot(shap_values, X)`; the house-price analogy (near a school, near a station, ocean view → each moves the price) | local, aggregating to global |
| **Eli5** | `eli5.show_weights()` on an XGBoost Titanic model (sex=female carries the top weight), then `show_prediction()` for a single row | global, then local |

For the wine data he states the expected result directly:

> *"Alcohol has the maximum contribution... if the alcohol value is high, then the overall quality of your
> wine would be high."*

### Two things worth checking against the activity notebooks

**1. His alcohol claim is a *global* statement, and it is correct globally.** But in
[`activity4`](activities/activity4_eli5_lime_mlxtend.ipynb), for one specific wine, SHAP ranks `alcohol`
**8th of 11**, while (broken) LIME puts it 1st. That is not a contradiction - it is precisely the
**global vs local** distinction that is the graded line in SLO a). Most of the cohort will paste
`shap.summary_plot`, see `alcohol` on top, and write "alcohol is the most important feature" - having just
made a global claim and called it an explanation of one prediction.

**2. The Eli5 function he teaches is the one whose local signs are inverted.** He presents `show_weights`
(global) and `show_prediction` (local) as the same idea at two zoom levels. `show_prediction` is the one
that returns the **class-0** decomposition regardless of `targets=`, so read as "contribution to P(good)"
every sign is backwards - demonstrated and verified by intervention in `activity4`.

Do not go and correct the lecturer in the presentation. But writing *"I cross-checked SHAP against Eli5 on
the same wine - the rankings agree (Spearman +0.98) but the directions do not, so I verified the sign by
intervening on the model"* is exactly the rigour a HD rubric asks for, and nobody else will do it.

### The activities

> *"You can just implement **any two of them**."*

Four are done. Covered with room to spare.
