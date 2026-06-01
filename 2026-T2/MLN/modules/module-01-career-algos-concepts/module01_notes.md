# Module 1: Career Opportunities, Key Concepts, Applications, Types of Algorithms and Software

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Raschka et al. (2020) - Machine Learning in Python | ✅ |
| **2** | Read & summarise Pedregosa et al. (2011) - Scikit-learn: Machine Learning in Python | ✅ |
| **3** | Watch & summarise VanderPlas (2015) - Machine Learning with scikit-learn | ✅ |
| **4** | Watch & summarise S. Raschka (2016) - Introduction to ML in Python | ✅ |
| **5** | Read & summarise Townes (2017) - ML as a career skill | ✅ |
| **6** | Read & summarise Hill (2012) - Target pregnancy prediction case | ✅ |
| **7** | Read & summarise Jiang et al. (2020) - COVID-19 severity prediction | ✅ |
| **8** | Activity 1: Self-introduction and Machine Learning Jobs | ✅ |
| **9** | Activity 2: Machine Learning Applications forum post and replies | ✅ |

---

## Key Highlights

### 1. Raschka et al. (2020). Machine Learning in Python

**Citation:** Raschka, S., Patterson, J., & Nolet, C. (2020, April 4). Machine learning in Python: Main developments and technology trends in data science, machine learning and artificial intelligence. *Information, 11*(193), 1-44. https://www.mdpi.com/2078-2489/11/4/193/pdf

**Purpose:** Broad survey of the Python machine learning ecosystem, explaining why Python became the default language for data science and how classical ML, AutoML, GPU computing, deep learning, explainability, fairness, and adversarial learning fit together.

---

#### 1. Python Is the ML "Glue" Language

- **Python's appeal** comes from readability, a large community, and high-level APIs that hide much of the low-level performance complexity.
- **Performance is not pure Python:** many core libraries call optimized C, C++, Fortran, CUDA, BLAS, or LAPACK routines underneath.
- **Core stack:** NumPy for arrays, SciPy for scientific routines, Pandas for tabular data, Matplotlib/Seaborn/related tools for visualization, and scikit-learn for classical ML.
- **Jupyter notebooks** make experimentation, explanation, and reproducibility easier because code, results, notes, and charts can live together.

| Layer | Main role in ML work |
|---|---|
| NumPy | Dense arrays and linear algebra foundations |
| SciPy | Scientific algorithms, optimization, sparse matrices, statistics |
| Pandas | Data cleaning, tabular manipulation, joins, exploratory analysis |
| Matplotlib / Seaborn | Visual diagnostics and communication |
| scikit-learn | Classical ML estimators, pipelines, model selection |
| PyTorch / TensorFlow | Deep learning and differentiable programming |

#### 2. Classical ML Still Matters

- The paper separates **classical ML** from **deep learning**. Classical methods include decision trees, random forests, support vector machines, k-nearest neighbors, linear models, logistic regression, and gradient boosting.
- Classical ML is still heavily used because much real-world business data is **structured/tabular**, not images, audio, or raw text.
- Deep learning is powerful for large unstructured datasets, but it is often overkill for small to medium tabular problems.
- This matches MLN601's focus: shallow/classical learning gives the foundations for regression, classification, clustering, model selection, and interpretation.

#### 3. Scikit-learn as the Classical ML Standard

- Scikit-learn is described as the industry standard for small to medium classical ML because of its consistent API and documentation.
- The paper highlights the `fit()` / `predict()` design pattern and the pipeline API as major reasons other tools imitate scikit-learn.
- Scikit-learn includes established algorithms and leaves newer or more specialized methods to compatible extension libraries.

| scikit-learn concept | Why it matters |
|---|---|
| Estimator | A model or transformer object with a consistent interface |
| `fit()` | Learn parameters from training data |
| `predict()` | Generate outputs for unseen data |
| `transform()` | Convert data, e.g. scaling or dimensionality reduction |
| Pipeline | Chain preprocessing and modelling without leaking test data |
| Cross-validation | Estimate generalisation rather than memorisation |

#### 4. Common Real-World Challenges

- **Class imbalance:** if one label dominates, accuracy can hide poor minority-class performance. Stratified splits and resampling can help.
- **Feature engineering:** many ML gains come from cleaning, encoding, scaling, selecting, and combining useful variables.
- **Hyperparameter optimization:** grid search is simple but expensive; random search and smarter methods can be more efficient.
- **Scalability:** Dask, Spark, GPU tools, and distributed libraries become relevant when data no longer fits comfortably on one machine.
- **Interpretability and fairness:** model accuracy is not enough where decisions affect people. Feature importance, LIME, SHAP, fairness metrics, and privacy-aware learning are part of responsible ML practice.

#### Key Takeaways for MLN601

1. MLN601 starts in the right place: classical ML is still essential because most applied projects begin with structured data, small-to-medium datasets, and explainable workflows.
2. The practical ML workflow is more than algorithm choice: data preparation, feature engineering, train/test discipline, evaluation, and communication matter just as much.
3. Python's ecosystem is valuable because it lets you move from exploration to modelling to explanation with one coherent toolchain.

---

### 2. Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python

**Citation:** Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., VanderPlas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*(85), 2825-2830. https://www.jmlr.org/papers/v12/pedregosa11a.html

**Purpose:** Introduces scikit-learn as a Python module for accessible, well-documented, consistent classical ML. The current stable scikit-learn documentation extends this into a full user guide covering supervised learning, unsupervised learning, model selection, preprocessing, pipelines, evaluation, visualization, and common pitfalls.

> Note: The module resource list cites this item as 2015, but the JMLR record lists the paper as 2011.

---

#### 1. Design Goal: ML for Non-Specialists

- Scikit-learn's purpose is to make a wide range of ML algorithms usable through a general-purpose, high-level Python language.
- The emphasis is on **ease of use, performance, documentation, and API consistency**.
- The library targets **medium-scale supervised and unsupervised problems**, which aligns with the hands-on notebooks in MLN601.

#### 2. The Estimator Interface

The important idea is that many algorithms can be used with the same mental model:

```python
model = SomeEstimator(...)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

| Method | Used for | Example |
|---|---|---|
| `fit(X, y)` | Learn model parameters from labelled data | Linear regression, logistic regression |
| `fit(X)` | Learn structure from unlabelled data | Clustering, scaling, PCA |
| `predict(X)` | Produce labels or continuous predictions | Classification, regression |
| `transform(X)` | Convert data using learned transformation | StandardScaler, PCA |
| `score(X, y)` | Evaluate using the estimator's default metric | Accuracy or R-squared |

#### 3. What the User Guide Covers

The current stable user guide is a roadmap for the subject:

| User guide area | MLN601 connection |
|---|---|
| Supervised learning | Regression, decision trees, classification, SVM, logistic regression, perceptron |
| Unsupervised learning | K-means and clustering |
| Model selection and evaluation | Train/test split, cross-validation, metrics, tuning |
| Dataset transformations | Preprocessing, imputation, feature extraction, pipelines |
| Common pitfalls | Data leakage, inconsistent preprocessing, randomness |
| Choosing the right estimator | Matching algorithm families to problem types |

#### 4. Why Pipelines Matter Early

- ML projects usually combine preprocessing and modelling: encode categories, scale features, reduce dimensions, fit model, evaluate model.
- A scikit-learn pipeline lets those steps be treated as one estimator.
- This is not just convenience. It prevents mistakes such as fitting a scaler on the test set or leaking information from validation folds.

#### 5. Key Pitfalls to Watch

| Pitfall | Why it damages results | Basic prevention |
|---|---|---|
| Data leakage | Model indirectly sees test information | Fit preprocessing only on training folds |
| Inconsistent preprocessing | Train and test data transformed differently | Use pipelines |
| Wrong metric | Accuracy may hide poor minority-class performance | Select metrics to match task risk |
| Uncontrolled randomness | Results cannot be reproduced | Set `random_state` where appropriate |
| Overfitting | Model learns noise, not general patterns | Cross-validation, regularization, simpler models |

#### Key Takeaways for MLN601

1. Scikit-learn is not just a library of algorithms; it teaches the standard shape of applied ML work.
2. The `fit` / `predict` / `score` pattern will keep repeating across regression, classification, clustering, and model selection.
3. For assessments, pipelines and disciplined evaluation are the difference between a notebook that merely runs and a notebook that supports a defensible result.

---

### 3. PyData / VanderPlas (2015). Machine Learning with scikit-learn

**Citation:** PyData. (2015, August 5). Jake VanderPlas. *Machine learning with scikit learn* [Video]. https://www.youtube.com/watch?v=HC0J_SPm9co

**Purpose:** Hands-on scikit-learn tutorial showing how to think about ML problems, represent data as features and samples, use estimator objects, and compare algorithms through a consistent API.

---

#### 1. Machine Learning as Generalisation

- VanderPlas frames ML as building models with tunable parameters that adapt to seen data and then generalise to unseen data.
- The point is not magic; it is modelling patterns in data well enough to make useful predictions on new examples.
- He introduces two core supervised tasks:

| Task | Target type | Example |
|---|---|---|
| Classification | Discrete labels | Red/blue class, flower species, handwritten digit |
| Regression | Continuous values | Predicting a numerical measurement |

#### 2. Data Representation: Samples x Features

- Scikit-learn expects a 2D feature matrix `X`.
- Rows are **samples**: the objects, records, images, customers, patients, or observations being modelled.
- Columns are **features**: numeric measurements or engineered variables describing each sample.
- The target array `y` stores the label or value to predict in supervised learning.

| Symbol | Meaning |
|---|---|
| `X.shape[0]` | Number of samples |
| `X.shape[1]` | Number of features |
| `y` | Target labels or continuous outputs |
| New `X` | Unseen examples for prediction |

#### 3. Feature Engineering Is Often the Hard Part

- Numeric data can often be loaded directly, but text, categories, images, dates, and messy business fields need transformation.
- VanderPlas stresses that choosing useful features requires domain knowledge.
- For example, text must be converted into quantitative features before a model can work with it.

#### 4. The Estimator Pattern

The tutorial repeatedly uses the same workflow:

```python
from sklearn.some_module import SomeEstimator

model = SomeEstimator(...)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

- Once this pattern is learned, changing algorithms becomes much easier.
- This is why scikit-learn is good for experimentation: replace a linear model with random forest, SVM, k-nearest neighbors, etc., without rewriting the whole workflow.

#### 5. Model Choice Is Conditional

- A linear model might be better when the underlying relationship is simple and noise is high.
- A flexible model such as random forest may capture nonlinear structure, but can also overfit noise.
- VanderPlas repeatedly points back to cross-validation and model selection as the way to choose quantitatively.

#### Key Takeaways for MLN601

1. Keep translating every ML problem into `X`, `y`, task type, model, prediction, and evaluation.
2. Do not treat algorithm choice as opinion. Use validation evidence to compare models.
3. For Assessment 1, the regression notebook should make feature choices, model choice, and evaluation explicit rather than only showing final output.

---

### 4. Raschka (2016). Learning scikit-learn - An Introduction to Machine Learning in Python

**Citation:** PyData. (2016, October 17). Sebastian Raschka | *Learning scikit learn - An Introduction to machine learning in Python* [Video]. https://www.youtube.com/watch?v=9fOWryQq9J8

**Purpose:** Introductory tutorial focused on predictive modelling with scikit-learn, including supervised/unsupervised/reinforcement categories, train/test splitting, hyperparameters, regression, classification, categorical encoding, scaling, and pipelines.

---

#### 1. Three Broad Types of ML

| Type | Input pattern | Goal | MLN601 module link |
|---|---|---|---|
| Supervised learning | Labelled examples | Predict labels or values | Regression, decision trees, Bayes, SVM, logistic regression |
| Unsupervised learning | Unlabelled data | Discover structure | K-means clustering |
| Reinforcement learning | Agent actions and rewards | Learn behaviour through feedback | Background only in this subject |

Raschka spends most of the tutorial on supervised learning because it is the fastest path into practical predictive modelling.

#### 2. Basic Supervised Workflow

1. Split data into training and test sets.
2. Fit the model on training data only.
3. Predict on withheld test data.
4. Compare predictions against true test labels.
5. After evaluation, refit the final model using the full dataset if appropriate.

The important principle is that the test set should stay hidden until evaluation. Reusing it repeatedly for tuning creates optimistic results.

#### 3. Hyperparameters vs Model Parameters

| Concept | Set by | Example |
|---|---|---|
| Model parameter | Learned from data | Linear regression coefficient, intercept |
| Hyperparameter | Chosen by practitioner or search process | Number of neighbors, regularization strength, tree depth |

- Hyperparameters can strongly change model behaviour.
- Grid search and cross-validation are standard ways to tune them.
- Default values can be reasonable for learning, but assessment-quality modelling should justify important choices.

#### 4. Regression and Classification Examples

- The regression example predicts a continuous variable and evaluates with R-squared via `score()`.
- The classification example uses Iris flower data to show labels, stratified splitting, logistic regression, and k-nearest neighbors.
- Raschka notes that classification score defaults to accuracy, but other metrics may be needed depending on the problem.

| Example | Core lesson |
|---|---|
| Linear regression | `fit`, learned coefficients, R-squared, continuous prediction |
| Logistic regression | Despite the name, used for classification |
| k-nearest neighbors | Distance-based, sensitive to feature scale |
| Iris dataset | Multi-class labels and stratified train/test split |

#### 5. Preprocessing Discipline

- Categorical variables need correct handling:
  - **Ordinal** variables can be mapped to ordered numbers if the order is meaningful.
  - **Nominal** variables should usually be one-hot encoded to avoid fake ordering.
- Many models need features on comparable scales.
  - **Min-max scaling** maps values into a bounded range.
  - **Standardisation** centers values around the mean and scales by standard deviation.
- The scaler must be fit on the training data only, then used to transform test data.

#### 6. Pipelines Prevent Leakage

- Pipelines chain transformations and a final model.
- During cross-validation or grid search, pipelines ensure each fold learns preprocessing only from its training portion.
- This is a practical safeguard, not just clean code.

#### Key Takeaways for MLN601

1. Always separate model parameters from hyperparameters in your explanation.
2. Train/test discipline is a core credibility issue in notebook assessments.
3. Pipelines are the cleanest way to combine preprocessing, modelling, and evaluation without accidental leakage.

---

### 5. Townes (2017). Why "skilled in machine learning" should be the new "proficient in Excel" on your resume

**Citation:** Townes, F. (2017, June 15). Why "skilled in machine learning" should be the new "proficient in Excel" on your resume. *Quartz*. https://qz.com/1006379/the-best-resumes-will-soon-have-skilled-in-machine-learning-instead-of-proficient-in-excel

**Purpose:** Short career-focused article arguing that ML literacy will become a general workplace skill, not only a specialist data scientist credential.

---

#### 1. ML Is Moving Toward Everyday Work

- The article compares ML skill to spreadsheet skill: once specialised, then increasingly expected across knowledge work.
- The argument is that as tools become easier, more workers will train, configure, or use ML-enabled systems without needing to build algorithms from scratch.
- This is relevant to the Activity 1 discussion because career opportunities are not only "ML engineer" roles; they include any job where prediction, automation, and data-driven decisions improve outcomes.

#### 2. Citizen Development and Automation

- Townes points to open-source work, shared algorithms, and workplace bots as signs of ML becoming more accessible.
- The practical value is time leverage: summarising information, generating reports, filtering content, identifying risk, and supporting decisions.
- The article is optimistic about natural language interfaces lowering the technical barrier to AI tools.

#### 3. Critical Reading

- The article is a professional commentary, not peer-reviewed evidence.
- It is useful for career framing, but its claims should be balanced against actual job ads, current skills data, and the reality that robust ML still requires data quality, evaluation, governance, and ethics.
- For a forum post, it works best as a prompt: "ML literacy is becoming useful across roles" rather than "everyone will be an ML specialist."

#### Key Takeaways for MLN601

1. The most employable version of ML skill is practical: Python, notebooks, scikit-learn, data cleaning, evaluation, and clear communication.
2. ML can augment non-technical roles when people understand what predictions mean and what their limits are.
3. Your forum self-introduction can link your software engineering background to ML-enabled automation, product analytics, cloud AI services, or responsible AI delivery.

---

### 6. Hill (2012). How Target Figured Out A Teen Girl Was Pregnant Before Her Father Did

**Citation:** Hill, K. (2012, February 16). How Target figured out a teen girl was pregnant before her father did. *Forbes*. https://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/

**Purpose:** Retail analytics case study showing how purchase-pattern prediction can create business value while raising privacy, consent, and ethical concerns.

---

#### 1. The ML Application Pattern

- Target linked customer transactions and demographic data to a persistent customer identifier.
- Analysts looked for patterns among customers who had baby registries and then searched for similar purchase signals in other customers.
- The result was a pregnancy prediction score and likely timing window for targeted marketing.

| ML concept | Target case example |
|---|---|
| Historical labelled data | Customers known to be pregnant through registries |
| Features | Purchased products, timing, quantities, demographic attributes |
| Prediction | Pregnancy likelihood and expected stage |
| Business action | Timed coupons and targeted promotions |

#### 2. Predictive Power Can Feel Invasive

- The system inferred a sensitive life event from ordinary purchases.
- Even if data collection is legal, the prediction can violate customer expectations.
- The case shows that "accurate" is not the same as "acceptable."

#### 3. Hiding the Prediction Is an Ethical Warning Sign

- The article describes the retailer disguising targeted baby-product coupons among unrelated products so the targeting appeared random.
- This is a useful ethics point: when an organisation feels pressure to conceal how a prediction was made or used, the system likely has a trust problem.
- In modern ML language, this touches privacy, transparency, consent, profiling, and manipulative personalisation.

#### 4. Links to MLN601 Concepts

- It is a classification/ranking problem: identify customers likely to belong to a sensitive segment.
- Feature engineering matters: no single product proves pregnancy, but combinations and timing can be predictive.
- Evaluation should not stop at accuracy. The system also needs governance around acceptable use.

#### Key Takeaways for MLN601

1. ML creates value by finding non-obvious patterns, but those patterns can expose private information.
2. Predictive applications need stakeholder analysis: customer, company, family members, regulators, and society may see the same prediction differently.
3. For the Activity 2 forum, this is a strong example of why applied ML requires ethics, not only technical performance.

---

### 7. Jiang et al. (2020). Towards an Artificial Intelligence Framework for Data-Driven Prediction of Coronavirus Clinical Severity

**Citation:** Jiang, X., Coffee, M., Bari, A., Wang, J., Jiang, X., Huang, J., Shi, J., Dai, J., Cai, J., Zhang, T., Wu, Z., He, G., & Huang, Y. (2020). Towards an artificial intelligence framework for data-driven prediction of coronavirus clinical severity. *Computers, Materials & Continua, 63*(1), 537-551. https://www.techscience.com/cmc/v63n1/38464/pdf

**Purpose:** Early COVID-19 case study using predictive analytics to identify which patients were more likely to progress to acute respiratory distress syndrome (ARDS), supporting clinical triage and resource allocation.

---

#### 1. Problem Framing

- The clinical problem: most COVID-19 cases appeared mild at first, but a minority progressed to severe illness.
- The ML task: predict later ARDS risk using features available at initial presentation.
- The operational goal: support triage when hospital resources are constrained and clinician experience with a novel disease is still developing.

| ML element | Study version |
|---|---|
| Samples | 53 confirmed COVID-19 patients |
| Target label | Development of ARDS |
| Features | Symptoms, labs, demographics, imaging-related variables |
| Evaluation | 10-fold cross-validation |
| Practical decision | Identify patients needing closer attention and resources |

#### 2. Feature Engineering and Selection

The study used feature selection methods to reduce many clinical measurements to features with higher predictive value:

| Method | Idea |
|---|---|
| Entropy / information gain | Rank features by how much information they add about the target |
| Gini index | Prefer splits that produce cleaner class separation |
| Chi-squared statistics | Measure dependence between a feature and the target |
| Forward selection | Add features greedily while performance improves |

Top-ranked predictive features included:

1. ALT
2. Myalgias
3. Hemoglobin
4. Gender
5. Temperature
6. Sodium
7. Potassium
8. Lymphocyte count
9. Creatinine
10. Age
11. White blood count

#### 3. Model Results

| Algorithm | Reported accuracy |
|---|---|
| Logistic regression | 50% |
| k-nearest neighbors, k=5 | 80% |
| Decision tree, gain ratio | 70% |
| Decision tree, Gini index | 70% |
| Random forest | 70% |
| Support vector machine | 80% |

- The paper reports overall predictive accuracy around 70-80% for this population.
- A decision tree using ALT alone reached 70% accuracy.
- KNN and SVM were the strongest reported models, but the dataset was very small.

#### 4. Important Clinical Interpretation

- The most predictive features were not necessarily the most obvious clinical severity markers.
- Fever, cough, and imaging findings helped identify COVID-19, but did not strongly separate who would progress to ARDS in this dataset.
- Mild ALT elevation, myalgias, and hemoglobin were underappreciated signals in the model.
- Predictive features do not need to be causal. They can be useful correlations, but clinicians still need to interpret them carefully.

#### 5. Limitations

- The dataset had only 53 patients and incomplete values for some fields.
- Only 5 patients developed ARDS, so the positive class was very small.
- The patient population had a limited severity range and no deaths.
- External validation was needed before clinical deployment.
- The study is valuable as an early demonstration of predictive analytics, not as a final clinical tool.

#### Key Takeaways for MLN601

1. This case study maps directly to the ML workflow: define target, build feature matrix, select features, compare models, evaluate, and communicate limitations.
2. Accuracy alone is insufficient in healthcare. Class imbalance, false negatives, validation, and clinical consequences matter.
3. ML can augment expert judgement, but black-box predictions should not replace clinical reasoning or governance.

---

## Module Synthesis

### Core Vocabulary

| Term | Meaning |
|---|---|
| AI | Broad field of systems performing tasks associated with human intelligence |
| Machine learning | Algorithms that learn patterns from data instead of only following explicit rules |
| Classical / shallow ML | Feature-driven methods such as regression, SVM, decision trees, random forest, KNN, clustering |
| Deep learning | Neural-network-based learning that can learn representations from raw data |
| Feature | Measurable input variable used by a model |
| Label / target | Output the model learns to predict |
| Training set | Data used to fit model parameters |
| Test set | Withheld data used to estimate performance on unseen examples |
| Hyperparameter | Model setting chosen before or during tuning |
| Model parameter | Value learned from data during fitting |

### The Module 1 Mental Model

```text
Problem -> Data -> Features/labels -> Train/test split -> Model.fit()
        -> Model.predict() -> Evaluate -> Interpret -> Communicate limits
```

### Short Assessment Link

Assessment 1 is regression-focused, so the most relevant habits from Module 1 are:

1. State the prediction target clearly.
2. Explain the feature matrix and preprocessing choices.
3. Use a clean train/test or cross-validation strategy.
4. Report suitable regression metrics, not only charts.
5. Discuss overfitting, limitations, and what the model can or cannot support.
