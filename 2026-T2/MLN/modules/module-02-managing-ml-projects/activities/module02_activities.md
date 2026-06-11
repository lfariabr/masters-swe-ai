# MLN601 · Module 2 — Learning Activity Drafts

> Draft deliverables for the two Module 2 learning activities. Personalise the `[bracketed]` parts before posting.
> Keep tone: human, specific, no corporate filler.
> Source files in this folder: `a1_template.ipynb` (Activity 1 template) · `a2.pdf` (Mishra, 2019 — Activity 2 article).

---

## Activity 1 — Loading up the CRISP-DM Template

> *Task: upload the provided CRISP-DM template to your Colab/Jupyter notebook, familiarise yourself with the six stages, and post any questions / engage in discussion on the forum. The template is the one you'll reuse for each assessment.*

**The template (`a1_template.ipynb`) mapped to the 6 CRISP-DM stages** — running example: predict **red-wine quality** from physicochemical traits.

| # | Stage | What the template asks you to fill in |
|---|-------|----------------------------------------|
| 1 | **Business Understanding** | The objective (predict wine quality), success criteria, and resources (personnel, data, compute, software/libraries) |
| 2 | **Data Understanding** | Acquire data (`pd.read_csv`), describe (`shape`, `dtypes`, `describe`, `head`), verify quality (missing values, **outliers** via IQR ± 3×IQR), initial EDA (distributions, correlations via `seaborn.pairplot`) |
| 3 | **Data Preparation** | Select attributes/records (rationale for inclusion/exclusion), clean, handle missing values |
| 4 | **Modeling** | Choose technique, state assumptions, build model + parameter settings, assess & rank models |
| 5 | **Evaluation** | Judge the model against **business** success criteria (not just accuracy), approve a model |
| 6 | **Deployment** | Deployment + monitoring strategy; for the assessment, used to conclude with **lessons learned** |

**Draft forum post (question / discussion starter):**

I've loaded the CRISP-DM template into Colab and walked through all six stages with the red-wine dataset (1,599 rows, 11 physicochemical features, target = `quality`). The template makes the *framing-first* idea from this module very concrete — Stage 1 forces you to define the objective before touching a single `read_csv`.

My question is about the jump from **Business Understanding → Modeling**: `quality` is an **ordinal integer** (roughly 3–8), and our first assessment is framed as *Regression Analysis*. So do we treat this as a regression problem (predict the number, then round) or as ordinal/multi-class classification (predict the band)? My instinct from Module 1 is that "predicting a number → regression", but quality isn't really continuous — the gap between a 5 and a 6 isn't guaranteed to be the same as between a 7 and an 8. How is everyone deciding this, and does the template's Stage 1 ("determine business objectives") change the answer — e.g. would a winemaker rather see a *predicted score* or a *pass/fail* band?

Keen to hear how others are reading the brief. 👋

---

## Activity 2 — Understanding CRISP-DM Using Video Game Sales Data (Mishra, 2019)

> *Task: read Mishra (2019), download the data + notebook from the author's GitHub, run it step-by-step, then share your output to the forum with a post noting any issues you hit, how you overcame them, and your overall experience.*

**Reference:** Mishra, B. (2019, 23 April). *Understanding CRISP-DM using video game sales data.* Medium. (PDF: `a2.pdf` in this folder.)

### How to run (replicating Mishra, 2019)

```bash
# 1. Clone the author's repo (data + notebook)
git clone https://github.com/bharat-dsdev/vgsales-analysis.git
cd vgsales-analysis

# 2. Notebook: notebook/Visual_EDA_Video_Game_Console_Sales.ipynb
#    Dataset: vgsales.csv (16,598 games scraped from vgchartz.com, also on Kaggle)

# 3. Run with the system Jupyter kernel (Homebrew py3.14, no venv)
python3 -m pip install --break-system-packages pandas numpy matplotlib seaborn scikit-learn xgboost
jupyter notebook
```

The dataset columns: `Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales`. The article answers four questions — revenue & releases per year (2008 peak), top publishers (EA by releases, Nintendo by revenue), most-loved genre (Action), and a regression to predict sales.

### ⚠️ The insight worth leading with — that 0.9999 R² is **target leakage**

Mishra reports a regression with **Training score 0.99997 and Testing score 0.99996**. That near-perfect R² should *not* feel like success — it's the classic *"suspect if the performance is too good"* red flag from the Module 2 readings (Tyagi, 2020; and the test-set-leakage risk formalised in CRISP-ML(Q), Studer et al., 2020).

The cause is structural: **`Global_Sales = NA_Sales + EU_Sales + JP_Sales + Other_Sales`**. If the regional sales columns are left in `X` while predicting `Global_Sales`, the model is just relearning addition — it has the answer baked into its features. Honest setups: either **drop the regional columns** and predict `Global_Sales` from genuine predictors (Genre, Platform, Publisher, Year), or pick a target that isn't a sum of its own features. This is *exactly* the kind of leakage CRISP-DM's Evaluation stage exists to catch before deployment.

**Draft forum post (reflection — issues, fixes, experience):**

I followed Mishra's (2019) CRISP-DM walkthrough on the VGChartz sales dataset (16,598 games) and ran his notebook end-to-end. A few things from the experience:

- **What I hit:** the notebook is from 2019, so a couple of calls needed updating for current libraries — [e.g. `seaborn`/`matplotlib` styling and a deprecated pandas argument] — and I had to point the data path at my local `vgsales.csv`. Minor, but a good reminder that *reproducibility* (a CRISP-ML(Q) quality measure) decays over time.
- **The thing that stood out:** the sales-prediction model scores ~0.9999 on both train and test. Rather than celebrate, I traced it back — `Global_Sales` is literally the sum of the four regional sales columns, so feeding those in as features is **target leakage**. When I dropped them and predicted from Genre/Platform/Publisher/Year instead, the R² fell to something realistic, which is the *honest* result. "Too good to be true" usually is.
- **Overall:** the value of the exercise wasn't the EDA charts (2008 as the peak year, Action as the top genre, EA/Nintendo leading) — it was seeing how the CRISP-DM **Evaluation** stage is the guardrail that should have flagged that score. It maps straight onto my own work: in Review Pulse I watch for the same leakage between feature construction and the label.

Happy to share my notebook output — [attach screenshots / link]. Did anyone else notice the leakage, or get a different score after cleaning the feature set?

---

### Notes for posting
- Both activities are participation-graded; substance + tying back to the module readings (CRISP-DM stages, leakage) is what's rewarded.
- Activity 1 is a **question** post — the brief explicitly asks you to "raise any questions" and engage, so leading with a genuine framing question is on-brief.
- Activity 2 needs the **real run** before you post the output — the draft reflection is grounded in the article's actual numbers, but swap the `[bracketed]` run-specific details (which API calls you fixed, your post-cleanup R²) for what you actually see.
- The leakage observation is the academic "so what" — it shows understanding, not just replication.
