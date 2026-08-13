# Machine Learning (MLN601) Notes
## Dr. Kamran Shaukat

## Module 1 - Introduction to Machine Learning

### TLDR
Machine Learning (ML) uses data, features and statistical learning algorithms to make predictions or discover patterns without hand-coding every rule.
- MLN601 focuses on classical/shallow ML: regression, classification, SVMs, decision trees, K-means and perceptrons using Python and scikit-learn.
- Core workflow: frame the task, prepare `X` features and `y` labels, split train/test data, fit a model, predict, evaluate and explain limitations.
- Python's ML ecosystem matters because NumPy, Pandas, Jupyter, Matplotlib/Seaborn and scikit-learn make end-to-end experimentation practical.
- Real applications create value in careers, retail and healthcare, but also raise privacy, fairness, validation and governance concerns.

### Introduction
In which area are career opportunities surging and are companies growing at the fastest rate in the world? In Machine learning (ML).

ML is a subset of artificial intelligence (AI). It is a collection of algorithms and programming techniques that uses statistical models to automatically discover patterns and relationships in data. With ML algorithms, you can use historical data to make predictions of sales trends, make weather and other forecasts and conduct risk analyses. Additionally, ML algorithms can predict clusters and classify data for a range of tasks, the results of which can be used to make recommendations of places to visit and items to purchase. The hype around ML and its strong association with AI primarily stem from its predictive capability. The ability to predict is strongly associated with the intelligence of humans.

This subject focuses on classical ML or shallow learning. In shallow learning, the extraction of features (something measurable) from input data is manual and requires domain expertise. Conversely, in deep learning (DL), machines automatically learn about features (without the key characteristics having to be described), which ultimately enables them to recognise differences between different objects, animals or humans.

DL achieves an output through processes that mimic the operation of the human brain (neural networks). Multiple layers of neural networks extract knowledge and transform the raw data into higher-level features comprising an object, animal or human. It is these multiple layers that led to this type of learning being referred to as ‘deep’ learning.

DL is considered ‘cutting edge’; however, the technology is not without its drawbacks. DL requires substantial infrastructure. Further, due to its black-box–like nature, it is impossible to explain precisely what is occurring in human terms (the internal mechanism for DL is not unlike a software version of the human brain, but it is represented by layers of neural networks that cannot be readily understood). Additionally, DL magnifies the challenges facing shallow learning (ML), such as those related to the tuning of parameters for optimal learning (hyperparameter tuning) and those related to biases in data. Thus, a shallow-ML, solution-first, mindset to solving problems is essential. This subject will not cover DL any further.

The main type of ML algorithm is the supervised learning algorithm, wherein labelled examples are provided for learning. Labels represent the object or output of our focus. The second type of ML algorithm is the unsupervised learning algorithm, which does not require the input data to be labelled. The majority of ML projects use a common set of algorithms. These algorithms and this software code are available as part of the open-source scikit-learn (https://scikit-learn.org/stable/) Python library. Classical or shallow algorithms include regression, support vector machine, decision-tree, K-mean and perceptron algorithms. During this course, you will gain hands-on experience with each of these ML algorithms.

Previously, these types of ML algorithms were the domain of university researchers and major technology vendors. However, the open-source Jupyter notebook, the Python ecosystem of libraries and the cloud services have now made cloud-based ML available to everyone.

ML and AI jobs require a similar set of skills, including knowledge of mathematics and statistics, proficiency in Python and experience in using ML frameworks, such as scikit-learn. The expectation is that you will be able to leverage your ML skills across the different cloud platforms of the major vendors.

The major vendors are:

- Amazon SageMaker: https://aws.amazon.com/machine-learning/
- Google Cloud AI Platform: https://cloud.google.com/ai-platform
- Microsoft Azure Machine Learning: https://azure.microsoft.com/en-au/services/machine-learning/

### Resources

#### 1. Machine Learning in Python
- Raschka, S., Patterson, J. & Nolet, C. (2020, 4 April). Machine learning in Python: Main Developments and technology trends in data science, machine learning and artificial intelligence. Information, 11(193), 1–44. Retrieved from https://www.mdpi.com/2078-2489/11/4/193/pdf

*Resource Overview:*

    Python in 2020 is the programming language of choice for building ML prototypes rapidly. As a general purpose language, it is very useful for building end-to-end systems. As you will see from searching job posts, Python coding skills are in high demand. The following libraries and tools are well suited to and frequently used in the development of ML models and applications:

    The Python libraries of scikit (a collection of ML algorithms);
    - Matplotlib and seaborn (for plotting and visualisation);
    - Pandas (for data manipulation);
    - NumPy (for scientific calculations);
    - Jupyter (a development environment for data analysis).
    
    This article provides not only a state of the art perspective of Python and ML but is a good primer of the vocabulary in use on ML projects. The focus of this subject and your reading is classical ML (shallow learning). Thus, do not feel compelled to dwell on DL unless you wish to do so out of interest or for completeness.

> *Status: ✅ Read + Reviewed — see [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#1-raschka-et-al-2020-machine-learning-in-python)*

#### 2. Scikit-learn—Machine Learning in Python
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., . . . Perrot, M. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/index.html

*Resource Overview:*

    Scikit-learn is the most popular open-source library for classical ML. The best way to learn about this open-source ML library is to explore the community pages. Explore the scikit-learn site, including the tutorials, user guide and how to run ML code examples in your browser. Each example in the user guide is accompanied by a code which you can download as a .ipynb file and execute as a Binder. This is a code repository that contains the code you might like to run and the actual environment required to run your code. The code environment is interactive and you can execute code a line at a time.

> *Status: ✅ Read + Reviewed — see [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#2-pedregosa-et-al-2011-scikit-learn-machine-learning-in-python)*

#### 3. PyData—Machine Learning with Scikit Learn
- PyData. (2015, 5 August). Jake VanderPlas. Machine learning with scikit learn [Video file]. Retrieved from https://www.youtube.com/watch?v=HC0J_SPm9co
- PyData. (2016, 17 October). Sebastian Raschka | Learning scikit learn—An Introduction to machine learning in Python [Video file]. Retrieved from https://www.youtube.com/watch?v=9fOWryQq9J8

*Resource Overview:*

    PyData (https://pydata.org/) provides a forum for the international community of users and developers of data analysis tools to share ideas and learn from each other. On its YouTube channel (https://www.youtube.com/user/PyDataTV), there are videos that help you stay up to date. You can view the conference videos if they are of interest.

    For this Module, you are required to watch two video tutorials (presented by Jake VanderPlas and Sebastian Raschka) that discuss gaining hands-on experience with scikit and ML. These videos help bring to life key concepts covered in this subject. The two videos cover similar ground, including an introduction to ML in Python using scikit, and the speakers reinforce different aspects in the domain of ML.

> *Status: ✅ Watched + Reviewed — see [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#3-pydata--vanderplas-2015-machine-learning-with-scikit-learn) and [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#4-raschka-2016-learning-scikit-learn---an-introduction-to-machine-learning-in-python)*

### Learning Activities

#### 1. Self-Introduction and Machine Learning Jobs
To understand where the career opportunities are emerging, consult a variety of articles from professional journals and key job sites (e.g., LinkedIn and Indeed).

So, where are the surging career opportunities?

Consider the following quotations:

- ML is the ‘... most in-demand AI skill’ (Zafarino, 2018);
- Data engineer Best job of 2019’ in the United States (Indeed, 2019);
- The number-one emerging job in the U.S. with 74 percent annual growth 2016-2020 and requiring ML skills is the ‘Artificial Intelligence Specialist’ (LinkedIn, 2020); and
- Looking to the future, ML is ‘a skill that will be in the centre of innovation for the next decades’ (Townes, 2017).
Consult the articles from which these quotations were taken (see references below) to gain more insights.

Introduce yourself to other students via the discussion forum and share some of the jobs capturing your interest

References
- Indeed. (2019, 14 March). The best jobs in the US: 2019. Retrieved from https://www.indeed.com/lead/best-jobs-2019
- LinkedIn. (n.d.) 2020emerging jobs report. Retrieved from https://business.linkedin.com/content/dam/me/business/en-us/talent-solutions/emerging-jobs-report/Emerging_Jobs_Report_U.S._FINAL.pdf
- LinkedIn. (n.d.) 2020emerging jobs report Australia. Retrieved from https://business.linkedin.com/content/dam/me/business/en-us/talent-solutions/emerging-jobs-report/AUS-TOP-EMERGING-JOBS_compressedRevised.pdf
- Townes, F. (2017, 15 June ). Why ‘skilled in machine learning’ should be the new ‘proficient in Excel’ on your resume. Quartz. Retrieved from https://qz.com/1006379/the-best-resumes-will-soon-have-skilled-in-machine-learning-instead-of-proficient-in-excel
- Zafarino, S. (2018, 27 July). The outlook for machine learning in Tech: ML and AI skills in high demand. CIO. Retrieved from. https://www.cio.com/article/3293019/the-outlook-for-machine-learning-in-tech-ml-and-ai-skills-in-high-demand.html

> *Status: ✅ Done — source notes ready in [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#5-townes-2017-why-skilled-in-machine-learning-should-be-the-new-proficient-in-excel-on-your-resume)*

#### 2. Machine Learning Applications
- Hill, K. (2012, 16 February). How Target figured out a teen girl was pregnant before her father did. Forbes. Retrieved from https://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/#7dc209fb6668
- Jiang, X., Coffee, Bari, A., Wang, J., Jiang, X., Huang, J., . . . Huang, Y. (2020). Towards an artificial intelligence framework for data-driven prediction of coronavirus clinical severity. Computers, Materials and Continua, 63(1), 537–551.Retrieved from https://www.techscience.com/cmc/v63n1/38464/pdf

An understanding of the application of ML will help you to prepare for the opportunities and gain a better understanding of the areas in which jobs are emerging. In the short term, predictive systems are attracting a lot of interest. For example, ‘How Target Figured Out A Teen Girl Was Pregnant Before Her Father Did‘ (Hill 2012).

As the article entitled ‘Artificial Intelligence Framework for Data-Driven Prediction of Coronavirus Clinical Severity ‘ (Jiang et al., 2020) shows, the systems built on ML are diverse, high profile and impactful. Review Sections 4–7 of this article to understand the predictive capability of this framework and recognise that the predictors are not the same as those publicly reported.

Plenty of other examples can be found by searching the AI Index arXiv Monitor (https://arxiv.aiindex.org/search) with the term ‘machine learning’. Spend some time to seek out the new ML predictive systems. Note that this material has not been peer-reviewed by arXiv.

Post 2–3 sentences to the discussion forum explaining what you have learned in this Module and how you can see yourself applying it; and Reply to two of your peers’ posts.

> *Status: ✅ Done — source notes ready in [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#6-hill-2012-how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did) and [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#7-jiang-et-al-2020-towards-an-artificial-intelligence-framework-for-data-driven-prediction-of-coronavirus-clinical-severity)*

---

## Module 2 - Managing Machine Learning Projects: CRISP-DM, Ethics by Design (Australasia), and Data Sets

### TLDR
**CRISP-DM** (Cross-Industry Standard Process for Data Mining) is the de-facto standard for organising ML/analytics projects — **6 iterative phases** with backtracking:
- **Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment.**
- It endures because it is **business-anchored** (starts *and* ends at business goals) and **domain-general** (Shearer, 2017).
- **CRISP-ML(Q)** (Studer et al., 2020) modernises it for ML: merges Business + Data Understanding, adds a 6th **Monitoring & Maintenance** phase, and attaches **Quality Assurance** to every task — answering the fact that **75–85% of ML projects miss expectations**.
- The same skeleton is reused as a practitioner **task checklist** (Tyagi, 2020), an **audit framework** (Clark, 2018 — bias by sampling), and an **ethics-by-design** lens (Cunningham, 2020 — one ethical question per phase).
- Recurring disciplines: honest **train/validation/test split**, watch for **class imbalance** and **data leakage**, **interpretability** (LIME/SHAP), and **fairness/bias** auditing.

> Full per-resource breakdown: [module02_notes.md](module-02-managing-ml-projects/module02_notes.md)

### Introduction
How do we know we have achieved the successful completion of a machine learning (ML) project? How do we organise a ML project? What do we need to do to ensure that the ML project being undertaken is ethical? How do we get started on ML projects?

All of these questions have one thing in common: they require an approach to help organise the multiple steps that comprise ML projects.

Notably, ML projects vary in terms of their duration and the skills they require. Thus, an approach, framework or methodology acts as an ordering mechanism for multi-step ML projects of varying durations. Additionally, a common approach allows projects to be replicated by any team member.

CRISP-DM is the most widely used analytics process standards. Thus, it is the closest thing we have to a standard model for implementing predictive analytics and ML projects. The video (below) provides an overview of the CRISP-DM process and the importance of the framework in managing predictive or ML projects.

McCormick, K. (2020, 25 February) . CRISP-DM: Established process of producing predictive models [Video file]. Retrieved from https://www.linkedin.com/learning/predictive-analytics-essential-training-for-executives/crisp-dm-established-process-of-producing-predictive-models?u=56744473

In undertaking ML projects, it is important to ensure that they have flexibility and that the ethical implications in relation to the data set being used are considered. Additionally, data sets tend to require cleaning and any missing values need to be handled. This Module will enable you to gain an understanding of these two key areas beyond the planning stages of your ML project.

### Resources

CRISP-DM is a proven approach to organising and ensuring successful completion of a ML project. As part of the approach, you will be required to understand any ethical issues pertaining to the data set and algorithms. Another important aspect of the framework is checking for missing values within your data set.

#### 1. The Timeless Value of CRISP-DM
- Houston Analytics. (2017, 7 April). Colin Shrearer: CRISP DM [Video file]. Retrieved from https://www.youtube.com/watch?v=-K-GGW9827Q

*Resource Overview:*

    This video explains the timeless value of having a methodology for ML and predictive analytics projects.

> *Status: ✅ Watched + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#1-houston-analytics-2017-the-timeless-value-of-crisp-dm)*

#### 2. A Visual Guide to CRISP-DM Methodology
- Leaper, N. (2009, 13 March). A visual guide to CRISP-DM methodology. Retrieved from https://exde.wordpress.com/2009/03/13/a-visual-guide-to-crisp-dm-methodology/

*Resource Overview:*

    This single-page visual guide sets out all the steps of the original CRISP-DM process.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#2-leaper-2009-a-visual-guide-to-crisp-dm-methodology)*

#### 3. Task Cheat Sheet for Almost Every Machine Learning Project
- Tyagi, H. (2020, 4 July). Task cheatsheet for almost every machine learning project. A checklist of tasks for building end-to-end ML projects. Retrieved from https://towardsdatascience.com/task-cheatsheet-for-almost-every-machine-learning-project-d0946861c6d0

*Resource Overview:*

    This short article serves as a reminder of the importance of maintaining a task list for ML projects. The author never references CRISP-DM directly; however, he has clearly repurposed the CRISP-DM methodology as his own. You will maintain your own task list as part of your Jupyter notebook and ML developments.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#3-tyagi-2020-task-cheat-sheet-for-almost-every-ml-project)*

#### 4. Towards CRISP-ML(Q): A Machine Learning Process Model with a Quality Assurance Methodology
- Studer, S., Bui, T. B., Drescher, C., Hanuschkin, A., Winkler, L., Peters, S. & Mueller, R. (2020, 11 March). Towards CRISP-ML(Q): A machine learning process model with quality assurance methodology. Manuscript submitted for publication. Retrieved from https://arxiv.org/pdf/2003.05155.pdf

*Resource Overview:*

    This article proposes a process model for the development of ML applications. The model expands on CRISP-DM and recognises the strong support for CRISP-DM in the industry. The article provides a good recap of the original methodology. However, the authors contend that CRISP-DM fails to address ML tasks. In conclusion, the authors state, ‘Our survey is indicative of the existence of specialist literature, but its contributions are not covered in machine learning textbooks and are not part of the academic curriculum. Hence, novices to industry practice often lack a profound state-of-the-art knowledge to ensure project success’. This commentary serves as a reminder of the importance of having a suitable approach or methodology in conducting ML projects. A complete reading of this paper will increase your understanding of the specific ML tasks that need to be undertaken to ensure the success of a project.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#4-studer-et-al-2020-towards-crisp-mlq)*

#### 5. The Machine Learning Audit—CRISP-DM Framework
- Reference: Clark, A. (2018, 6 January). The machine learning audit—CRISP-DM framework. ISACA Journal, 1, 1–6. Retrieved from https://www.isaca.org/-/media/files/isacadp/project/isaca/articles/journal/2018/volume-1/the-machine-learning-audit-crisp-dm-framework_joa_eng_0118.pdf

*Resource Overview:*

    This paper describes the CRISP-DM model as ‘the industry standard for how machine learning is conducted by practitioners’. This paper describes how CRISP-DM has been used to instruct auditors undertaking a high-level ML audit. This useful article will help you to understand how ML models, with which you may not have previously worked, come together or not (as the case maybe). The ability to audit ML projects is likely to become a highly sought-after skill.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#5-clark-2018-the-machine-learning-audit-crisp-dm-framework)*

#### 6. Ethical CRISP-DM: The Short Version
- Reference: Cunningham, C. (2020, 11 April). Ethical CRISP-DM: The short version [Web log post]. Retrieved from https://blogs.ischool.berkeley.edu/w231/2020/04/15/ethical-crisp-dm-the-short-version/

*Resource Overview:*

    This blog post appropriates the CRISP-DM framework and guides you through how ethical guardrails are built into the steps of a ML project. The key focus includes ensuring the externalities of the solution are understood, the biases in the data are known, the data are clean of biases and safety measures are implemented to ensure the model is free of outside influences. Read this relatively short post to gain an understanding of how ethics can be built into your ML projects.

> *Status: ✅ Read + Reviewed — see [module02_notes.md](module-02-managing-ml-projects/module02_notes.md#6-cunningham-2020-ethical-crisp-dm-the-short-version)*

### Learning Activities

#### 1. Loading up the CRISP-DM Template—An Essential Step to Follow for Your Assessments
A specially prepared template is available. Upload the template to your Google Colab notebook. Seek any clarifications by posting questions and engaging in discussion on the forum. This type of template will be provided for each of the assessments. Now is a good time to familiarise yourself with the stages of CRISP-DM and raise any questions that you may have.

> *Status: ✅ Draft ready — see [module02_activities.md](module-02-managing-ml-projects/module02_activities.md#activity-1--loading-up-the-crisp-dm-template)*

#### 2: Understanding CRISP-DM Using Video Game Sales Data—A Useful Exercise for Your Assessments
- Reference: Mishra, B. (2019, 23 April). Understanding CRISP-DM using video game sales data. Retrieved from https://medium.com/@imBharatMishra/understanding-crisp-dm-using-video-game-sales-data-a2d55c7a2593

This activity requires you to see how CRISP-DM will help you to follow the analysis of video games sales data that was conducted by someone else. You will have access to both the data used and the Jupyter notebook code.

This activity requires you to:
- Read the article (below) entitled ‘Understanding CRISP-DM using Video Game Sales Data’ (Mishra, 2019) and follow the steps set out therein. Note: We are going to replicate some of the analysis;
- Download the data and code, which are available at the author’s GitHub page (https://github.com/bharat-dsdev/vgsales-analysis);
- Upload the notebook file (available at https://github.com/bharat-dsdev/vgsales-analysis/blob/master/notebook/Visual_EDA_Video_Game_Console_Sales.ipynb) to your Jupyter notebook and upload the data set;
- Ensure that you can execute the code step by step. Follow the code along with the outputs in the article; and

When complete, share your complete output to the discussion forum along with a post in which you note any issues that you encountered, how you overcame those issues and comment on your overall experience.

> *Status: 🔥 Draft ready (needs notebook run + post) — see [module02_activities.md](module-02-managing-ml-projects/module02_activities.md#activity-2--understanding-crisp-dm-using-video-game-sales-data-mishra-2019)*

#### 3. CRISP-DM Implementation for Bank Marketing Campaign Data
- Reference: Moro, S., Cortez, P. & Laureano, R. (2011). Using data mining for bank direct marketing: An application of the CRISP-DM methodology. Proceedings of the European Simulation and Modelling Conference. Retrieved from https://pdfs.semanticscholar.org/1999/417377ec21ecf7f7f55af62975065f785fb2.pdf

The writer of this study uses marketing campaign data from a Portuguese bank. The data is available from the UCI Machine Learning Repository (at https://archive.ics.uci.edu/ml/datasets/Bank Marketing). The purpose of the campaign is to acquire new clients who wish to subscribe to the offered term deposit. The goals of this project are to: 1) determine the predictive model with the best performance; and 2) identify the relevant variables (features) that have a significant effect on the predictive model.

To complete this learning activity:

1. Load the notebook file (available at https://github.com/daeIy/CRISP-DM-for-Marketing-Campaign);
2. Execute the code;
3. Follow through all the CRISP-DM stages, checking that the output is error free and ends in client predictions;
4. Try to understand what the code is trying to achieve and the modelling; and
5. When complete, share your complete output to the discussion forum along with a post in which you note any issues that you encountered, how you overcame those issues and comment on your overall experience.

> *Status: 🕐 To-Do* 

#### 4. Ethics and Biases in Bank Marketing
Australia has implemented an Artificial Intelligence (AI) Ethics Framework (https://www.industry.gov.au/data-and-publications/building-australias-artificial-intelligence-capability/ai-ethics-framework) while New Zealand has a draft algorithm charter (https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-Charter-2020_Final-English-1.pdf). Both these frameworks can assist you to determine whether any biases exist in your data.

Assume that the bank mentioned in the previous activity is based either in Australia or New Zealand. Determine if the manner in which the bank generated the data contains any unethical biases. Do you foresee any ethics or transparency issues in respect of the models being used? Post your views to the discussion forum.

> *Status: 🕐 To-Do* 

---

## Module 3 - Supervised Learning and Linear Regression

### TLDR
**Supervised learning** trains a model on **labelled** data (known outputs) to predict on unseen data, and it splits into **classification** (discrete labels) and **regression** (continuous values). This module is the **regression** branch (Raschka & Mirjalili, 2019).
- **Linear regression** fits `ŷ = b₀ + b₁x` (intercept + slope) by the **method of least squares**: pick the line that minimises `Σ(yᵢ − ŷᵢ)²`, the sum of squared residuals.
- **Parameters** (slope, intercept) are *learned from data*; **hyperparameters** (e.g. regularisation) are *set by you* and tuned via cross-validation. **No Free Lunch** -> always compare a few estimators.
- **scikit-learn workflow:** `train_test_split(random_state=…)` -> `LinearRegression().fit()` -> `.predict()` -> evaluate with **R²/RMSE**. Fit preprocessing on **train only** to avoid leakage.
- The **"Choosing the Right Estimator"** map routes a continuous-target, tabular problem to the regression branch: `LinearRegression` first, then `Ridge`/`Lasso`/`ElasticNet` if overfitting appears.

> Full per-resource breakdown: [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md)

### Introduction
In Module 1, you learned that one of the main types of machine learning (ML) algorithms is the supervised learning algorithm.

This Module focuses on linear regression, a widely used supervised learning technique. Notably, linear regression is a useful mathematical tool for investigating relationships between a set of variables and predicting responses (quantitative). Linear regression has been around since the 1800s and has been the subject of numerous books and articles.

### Resources

#### 1. Intuition Behind Linear Regression
- Reference: IntuitiveML (2020, 1 August). Intuition behind linear regression [Video file]. Retrieved from https://www.youtube.com/watch?v=uAZMhpNBq8M

*Resource Overview:*

    This video explains the importance of linear regression, the method of least squares and the correlation between the data and the outcome. The video includes important examples.

> *Status: 🔥 Primer ready - needs manual watch - see [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md#1-intuitiveml-2020-intuition-behind-linear-regression-video)*

#### 2. Giving Computers the Ability to Learn from Data
- Raschka, S. & Mirjalili, V. (2019). Giving computers the ability to learn from data. In Python machine learning: Machine learning and deep learning with Python, Scikit-learn, and Tensorflow 2 (3 ed., pp. 1–17). Birmingham, England: Packt. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=6005547&ppg=30

*Resource Overview:*

    Read ‘Chapter 1: Giving Computers the Ability to Learn from Data’. This chapter provides a good but simple overview of the field of ML and outlines some of the key terminologies. As this subject encourages the use of online Notebooks, such as Google Colab, you may choose to ignore the last few pages of this chapter, which are about the installation of Python.

> *Status: ✅ Read + Reviewed - see [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md#2-raschka-s--mirjalili-v-2019-giving-computers-the-ability-to-learn-from-data)*

#### 3. Linear Regression in Real Life
- Bento, B. (2020, 8 May). Linear regression in real life real world problems solved with math. Retrieved from https://towardsdatascience.com/linear-regression-in-real-life-4a78d7159f16

*Resource Overview:*

    This article explains the linear regression model and supporting concepts through simple storytelling. The writer uses the everyday example of driving on a limited amount of petrol to explain the model and its usefulness in real life.

> *Status: 🔥 Primer ready - needs manual read - see [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md#3-bento-b-2020-linear-regression-in-real-life-article)*

#### 4. Step-by-Step Linear Regression Using Python Scikit-Learn (SkLearn)
- Reference: Fowers, R. (2019, 25 July). Linear regression Python Sklearn [From Scratch] [Video file]. Retrieved from https://www.youtube.com/watch?v=b0L47BeklTE

*Resource Overview:*

    This video provides step-by-step instructions on how to use Scikit-learn for linear regression. Follow the steps in this video to familiarise yourself with the Jupyter Notebook and Scikit-learn linear regression. Note the imports including pydataset and from Sklearn train,test split.

> *Status: 🔥 Primer ready - needs manual watch - see [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md#4-fowers-r-2019-linear-regression-python-sklearn-from-scratch-video)*

#### 5. Cheat Sheet—Choosing the Right Estimator for Scikit-learn
- Reference: Choosing the right estimator. (n.d.). Retrieved from https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html

*Resource Overview:*

    This cheat sheet provides a useful guide to the different types of ML algorithms and the problems they are best suited to solve. The cheat sheet is organised by the type of problem being solved (e.g., classification, regression, clustering) and the type of data being used (e.g., structured, unstructured). This resource will be useful for you to refer to as you progress through this subject and undertake your assessments.

> *Status: ✅ Read + Reviewed - see [module03_notes.md](module-03-supervised-learning-and-linear-regression/module03_notes.md#5-choosing-the-right-estimator-scikit-learn-ml-map)*

### Learning Activities

#### 1. SkLearn Linear Regression (Boston Housing Prices Example)—A Useful Exercise for Your Assessments
- Reference: The Semicolon. (2017, 19 January). SkLearn linear regression (housing prices example) [Video file]. Retrieved from https://www.youtube.com/watch?v=JTj-WgWLKFM

For this activity, you should follow along with your Jupyter Notebook (e.g., Google Colab). The data set is the famous Boston housing data set. This can be loaded directly into the Notebook if you follow the instructions. By the end of this 10-minute video, you should have implemented the model, trained the linear model on Boston housing data to make predictions on house prices and determined how well your predictions match the actual data.

This activity requires you to:

1. Upload the file Housing example.ipynb to your Notebook;
2. Watch the video (The Semicolon, 2017; available at https://www.youtube.com/embed/JTj-WgWLKFM) and follow each step on your Notebook;
3. Once complete, share your feedback to the discussion forum. Note the key steps that you used to acquire the data set, describe the data (e.g., the average age of house buyers) and how you implemented the model, trained the model for house prices and determined the errors in your model.

> *Status: 🕐 To-Do*

#### 2. Predicting House Prices with Linear Regression Model—A Useful Exercise for Your Assessments
- Reference: Valkov, V. (2019, 2 April). Predicting house prices with linear regression | Machine learning from scratch (Part II). Retrieved from https://towardsdatascience.com/predicting-house-prices-with-linear-regression-machine-learning-from-scratch-part-ii-47a0238aeac1

This activity requires you to build a linear regression model using Python, use your trained model to predict house sale prices and extend the model to multivariate linear regression. You will have access to both the data used and Jupyter/Google Colab notebook code.

The activity requires you to:

1. Read the article entitled ‘Predicting House Prices with Linear Regression | Machine Learning from Scratch (Part II)’ (Valkov, 2019; available at https://towardsdatascience.com/predicting-house-prices-with-linear-regression-machine-learning-from-scratch-part-ii-47a0238aeac1) and follow the steps in the article. You will be replicating the code and analysis;
2. Load the complete source code onto your Notebook (Google Colaboratory) from the article (linear_regression.ipyb);
3. Ensure that you can execute the code step by step; and
4. Once complete, share your complete output to the discussion forum, noting any issues, how you overcame them and your overall experience.

> *Status: 🕐 To-Do*

---

## Module 4 - Decision Trees

### TLDR
A **decision tree** is a **non-parametric supervised** learner that recursively splits data into **if-then rules**. It is the one family that natively does **both classification and regression** (CART), takes **numerical + categorical** features, needs **no scaling**, and is a **white-box / explainable** model.
- **Splitting:** choose the split that maximises **purity**. **ID3** uses **Entropy + Information Gain**; **CART** uses the **Gini index** (binary splits). Pick the largest impurity decrease.
- **Weakness:** a single tree **overfits** and is **unstable** (a small data change -> a different tree). Control with `max_depth`, `min_samples_leaf`, and `ccp_alpha` (pruning).
- **Ensembles fix this:** **Bagging -> Random Forest** (parallel trees, vote) and **Boosting -> Gradient Boosting -> XGBoost** (sequential weak learners, each fixing the last's errors; XGBoost adds regularisation + sparsity-awareness + parallelisation).
- **A1 link:** your **RandomForest beat LinearRegression** because trees capture the **non-linearity** a single line cannot - this module is the machinery behind that result.

> Full per-resource breakdown: [module04_notes.md](module-04-decision-trees/module04_notes.md)

### Introduction
A decision tree (DT) algorithm (like a linear regression algorithm) belongs to the family of supervised learning algorithms. Unlike other supervised learning algorithms, a DT algorithm can be used to solve prediction and classification problems. Additionally, a DT algorithm handles both categorical and numerical data.

The name ‘DT’ originates from building models drawn in the form of a tree structure diagram but upside down. Each branch represents a decision or outcome. The goal of using a DT is to create a model to predict the class or value of a target variable. This is achieved by applying learning decision rules to the data. The purpose of a DT analysis is to determine a set of if-then logical conditions to improve classification or prediction.

DTs are easy to interpret and visualise due to the tree structure and the ability to read the rules directly from the tree in terms of the path from root to leaf.

The video below highlights the flexibility and user friendly visualisation of the DT algorithm (Rose, 2018). This algorithm is also known as the Classification and Regression Trees (CART) algorithm due to its ability to handle classification and regression trees. The algorithm captures a sequence of events, which enables a target value to be predicted via the learning of simple decision rules from the data features.

Reference: Rose, D. (2018). Decision trees [Video file]. Retrieved from https://www.linkedin.com/learning/artificial-intelligence-foundations-machine-learning/decision-trees?u=56744473

### Resources
- PwC. (n.d.). Explainable AI. Driving business value through greater understanding. Retrieved from https://www.pwc.co.uk/xai

This Module explains how to use Scikit-learn to build a basic decision tree (DT) classifier (in which data are put into different categories), visualise DTs and extract rules. The use of a DT to visualise the decision rules and logic has made the DT algorithm explainable and popular. It is explainable because the decisions made by the model are interpretable by humans and do not constitute a ‘black box model’. Indeed, ‘of all the ML learning techniques, decision trees are the most explainable because you can follow the progression of branches to determine the exact factors used in making the final prediction’ (PwC, 2018).

#### 1. Introduction to Decision Trees
- Reference: Brid, R. (2018, 26 October). Introduction to decision trees. Retrieved from https://medium.com/@MrBam44/decision-trees-91f61a42c724

*Resource Overview:*

    Building on the concepts presented in the video above (Augmented Startups, 2017), this article covers the basic terminology of DTs, their applications, advantages and disadvantages, the types of DTs and THE most common algorithms. It also provides a useful narrative reference without referring to any machine learning (ML) code.

> *Status: ✅ Read + Reviewed - see [module04_notes.md](module-04-decision-trees/module04_notes.md#1-introduction-to-decision-trees-brid-2018-koli-2023)* 

#### 2. Decision Trees and Boosting, XGBoost (eXtreme Gradient Boosting)
- Reference: Two Minute Papers. (2016, 25 March). Decision trees and boosting, XGBoost | Two Minute Papers #55 [Video file]. Retrieved from https://www.youtube.com/watch?v=0Xc9LIb_HTw

*Resource Overview:*

    This short video explains boosting, a very popular technique used to combine a lot of weak learner DTs into a strong learner. Individually, a weak learner is quiet inaccurate and makes predictions that are only slightly better than random guessing. However, if you take a whole bunch of weak learner DTs, you can produce a strong learning tree or algorithm.

> *Status: ✅ Watched + Reviewed - see [module04_notes.md](module-04-decision-trees/module04_notes.md#2-decision-trees-and-boosting-xgboost-two-minute-papers-2016)* 

#### 3. XGBoost Algorithm
- Morde, V. (2019, 8 April). XGBoost algorithm: Long may she reign! Retrieved from https://towardsdatascience.com/https-medium-com-vishalmorde-xgboost-algorithm-long-she-may-rein-edd9f99be63d

*Resource Overview:*

    XGBoost or extreme gradient boosting is a DT-based ensemble ML algorithm that performs very well. This article discusses the evolution of the algorithm from DTs and the potential future of the XGBoost algorithm. The algorithm has a large open community, which contributes to XGBoost projects (https://github.com/dmlc/xgboost/). To better understand the next generation of tree algorithms, including XGBoost, an analogy is used of an interview process and hiring criteria. The approaches taken to enable XGBoost to achieve a superior performance, including algorithm enhancements, provide a strong justification for its usage. This is proven by comparing Scikit-learn’s ‘make classification’ benchmarking to other algorithms.

> *Status: 🔥 Primer ready - needs manual read - see [module04_notes.md](module-04-decision-trees/module04_notes.md#3-xgboost-algorithm-long-may-she-reign-morde-2019)* 

#### 4. Plotting XGBoost Decision Tree in Python
- Brownlee, J. (2019, 11 December). How to visualize gradient boosting decision trees with XGBoost in Python. Retrieved from https://machinelearningmastery.com/visualize-gradient-boosting-decision-trees-xgboost-python/

*Resource Overview:*

    This hands-on tutorial shows how you can plot individual DTs within a trained gradient boosting model using XGBoost in Python. A full code listing is provided to create a plot of the first DT.

> *Status: ✅ Read + Reviewed - see [module04_notes.md](module-04-decision-trees/module04_notes.md#4-plotting-xgboost-trees-in-python-brownlee-2019)* 

#### 5. Scikit-learn Decision Tree Documentation
- Reference: Pedregosa, F.; Michel, V.; Grisel, O.; Blondel, M.; Prettenhofer, P.; Weiss, R.; Vanderplas, J.; Cournapeau, D.; Pedregosa, F.; Varoquaux, G.; et al. (2015). Scikit-learn: Machine Learning in Python. J. Mach. Learn. Res. 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/index.html

*Resource Overview:*

    Scikit-learn documentation is highly readable and well presented. The documentation below will allow you to implement DT algorithms with little prior knowledge. The following resources make for useful reading:
    - Understanding the decision tree structure (https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html);
    - Decision Tree Classifier (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html); and
    - Decision Tree Regressor (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html).

> *Status: ✅ Read + Reviewed - see [module04_notes.md](module-04-decision-trees/module04_notes.md#5-scikit-learn-decision-tree-documentation-pedregosa-et-al-2015)* 

### Learning Activities

#### 1. Visualising a Decision Tree and Machine Learning —A Useful Exercise for Your Assessments
- Reference: Google Developers. (2016, 13 April). Visualizing a decision tree—Machine learning recipes #2 [Video file]. Retrieved from https://www.youtube.com/watch?v=tNa99PG8hR8

In this learning activity, you will create your own DT classifier from a real data set, visualise the nodes/edges and read the rules from the tree.

For this activity, you should follow along with your Jupyter Notebook (e.g., Google Colab). Notably, this activity will remind you of the ideal nature of DTs to be able to capture interactions between features in data.

This activity requires you to:

Upload the file visualising a decision tree #2.ipynb;
Watch the video below (Google Developers, 2016; available athttps://www.youtube.com/embed/tNa99PG8hR8) and follow along with the coding in your Notebook; and
Once complete, share any interesting applications relevant to the workplace that emerged from this experience to the discussion forum. Comment on the ease or difficulty with which you were able to generate the DT and interpret the final output rules.

> *Status: 🕐 To-Do* 

#### 2. Writing a Decision Tree Classifier from Scratch —A Useful Exercise for Your Assessments
- Google Developers. (2017, 13 September). Let’s write a decision tree classifier from scratch. Machine learning recipes #8. Retrieved from https://www.youtube.com/watch?v=LDRbO9a6XPU

This activity requires you to follow along and build a DT classifier from scratch, preview the tree and build it. Notably, the key concepts of DT learning (i.e., Gini, impurity and information gain) are covered. These are also covered in the essential resource entitled, Introduction to Decision Trees (Brid, 2018).

This activity requires you to:

Upload the complete source code file decision_tree classifier from scratch #8.ipynb to your notebook;
Ensure that you can execute the code step by step while following along with the video (Google Developers, 2017; available at,https://www.youtube.com/embed/LDRbO9a6XPU.).
Once complete, share your complete output to the discussion forum along with answers to the following questions: How realistic or useful do you consider the toy data set? What understanding do you have of the working of Gini impurity? How well did you fare in relation to the predictions?

> *Status: 🕐 To-Do* 

#### 3. Decision Tree in Scikit-learn (Wine Dataset) —A Useful Exercise for Your Assessments
- Babu, V. (2020, 13 May). Decision tree in Sklearn [Web log post]. Retrieved from https://kanoki.org/2020/05/13/decision-tree-in-sklearn/.

This learning activity requires you to follow and explore the code required to build a DT classifier.

For this learning activity, you should:

Download the DT classifier code from https://github.com/min2bro/Tree-Based-Algorithms/blob/master/Decision Tree Classifier in sklearn.ipynb.;
Follow the paper (https://kanoki.org/2020/05/13/decision-tree-in-sklearn/.), which explores the DT functionality of Scikit-learn;
Explore what the code is trying to achieve and pay attention to the visualisation;
Extract the output (DT rules) as a text report; and
Once complete, share your output in text format to the discussion forum along with your interpretation of the DT rules. Compare and contrast with the DT visualisation previously generated. Which one do you prefer and why?


> *Status: 🕐 To-Do* 

#### 4. Comparing Decision Tree Algorithms (Random Forest versus XGBoost) in Python Using the UCI Wine Dataset - —A Useful Exercise for Your Assessments
- Sblendorio, D. (2019, 14 August). Comparing decision tree algorithms: Random forest vs. XGBoost [Web log post]. Retrieved from https://www.activestate.com/blog/comparing-decision-tree-algorithms-random-forest-vs-xgboost/.

For this learning activity, you will compare the different algorithms and determine the most appropriate solution for the task at hand.

For this learning activity, you should:

- Download the Notebook code from https://gitlab.com/dsblendo/comparingrf_xgboost.;
- Read through the post below (Sblendorio, 2019; available at https://www.activestate.com/blog/comparing-decision-tree-algorithms-random-forest-vs-xgboost/.);
- Follow the suggested code snippets embedded in the article together with the comments;
- Execute the Notebook code step by step; and
- Once complete, share your thoughts to the discussion forum about your experiences with the different algorithms. Do they all perform at the same speed? Discuss which algorithm you prefer and why.

> *Status: 🕐 To-Do* 

---

## Module 5 - Classification and Bayes Rule

### TLDR
**Bayes' rule** updates a **prior** belief into a **posterior** as new **evidence** arrives: `P(H|E) = P(E|H)*P(H) / P(E)`. It is the engine of probabilistic **classification**.
- **Base-rate fallacy:** for a rare condition, a positive test is mostly *false positives* - the prior dominates (Westbury 2010).
- **Naive Bayes** is the workhorse classifier: it assumes features are **conditionally independent given the class** (naive but effective). Variants: **Gaussian** (continuous), **Multinomial** (counts), **Bernoulli** (binary).
- **Generative vs discriminative:** Naive Bayes / GDA model `P(x|y)` then apply Bayes rule, vs logistic regression learning `P(y|x)` directly.
- **MAP vs MLE:** MAP = MLE + a prior. **Probabilistic programming** (PyMC3) writes the model and auto-computes the posterior, giving **uncertainty**, not just a point estimate.

> Full per-resource breakdown: [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md)

### Introduction
The Bayesian way of thinking is the key concept discussed in this Module. Bayes’ rule is primarily used for classification. Thomas Bayes (1702–1761), the inventor of Bayes’ theorem or rule, was a statistician, philosopher and clergyman who never published his work in his lifetime. His edited and published work only became available after his death through his friend Richard Price, who was a fellow statistician and sometimes church minister. Bayes’ rule (theorem) shows you how you can make an educated guess when you do not have everything at hand. No other mathematical concept has been met with as much fervour as Bayes’ rule. The most concise description for the use of Bayes’ rule in machine learning (ML) is:

*initial model new evidence = new and improved model*

The key idea behind the rule relates to the updating of prior knowledge based on new evidence. The thinking behind it is simple; however, its applications can be found everywhere. For example, this rule has been applied to ML, self-driving cars, spam detection, search and rescue operations (e.g., the Air France Flight 447 operation), medical diagnoses, including the interpretation of COVID-19 tests and classification of benign and malignant tumours in breast cancer, election predictions and weather predictions.

### Resources

#### 1. Bayes’ Rule—Introduction
- Westbury, C. (2010, 16 November). Bayes’ rule for clinicians: An introduction. Retrieved from https://www.frontiersin.org/articles/10.3389/fpsyg.2010.00192/full

*Resource Overview:*

    This is an important resource. Bayes’ theorem is often referred to interchangeably as a hypothesis, rule, theorem or law. Most individuals find it very difficult to understand and apply Bayes’ theorem. This may be because of the simplicity of Bayes’ rule. Often, most resources expect the reader to have an unnecessary amount of knowledge about probability. No matter how simple it is, the concepts supporting Bayes take time to understand and apply comfortably. This paper has been written for clinicians. It discusses how the application of Bayes’ rule helps to better understand the probability of a diagnosis being correct taking into account prior probabilities. This paper assumes a basic understanding of probability and a little knowledge of clinical work.

> *Status: ✅ Read + Reviewed - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#1-bayes-rule-for-clinicians-westbury-2010)* 

#### 2. How Bayes’ Rule is Applied in Machine Learning Models
- Zornoza, J.(2019, 14 August). Probability learning II: How Bayes’ theorem is applied in machine learning [Web log post]. Retrieved from https://towardsdatascience.com/probability-learning-ii-how-bayes-theorem-is-applied-in-machine-learning-bd747a960962

*Resource Overview:*

    This resource focuses on the use of Bayes’ rule in ML. Zornoza, the author of this resource, note that Bayes’ rule ‘tells us how to gradually update our knowledge on something as we get more evidence or that about that something’. This resource also explains how Bayes’ rule is used to improve regression and classification models by incorporating previous knowledge.

> *Status: ✅ Read + Reviewed - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#2-how-bayes-theorem-is-applied-in-ml-zornoza-2019)* 

#### 3. Generative Algorithms
- Zhiyang, W. (2015, 10 February). Andrew Ng Naive Bayes generative learning algorithms [Video file]. Retrieved from https://www.youtube.com/watch?v=nt63k3bfXS0

*Resource Overview:*

    In this video, Andrew Ng, an Associate Professor at Stanford, who is a very high-profile computer scientist and entrepreneur whose work focuses on AI, clearly explains discriminative and generative algorithms and their benefits . Ng also discusses the application of Bayes’ rule in classification (e.g., the classification of breast cancers as benign or malignant).

> *Status: ✅ Watched + Reviewed - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#3-naive-bayes-and-generative-learning-andrew-ng)* 

#### 4. Machine Learning Applications for Bayes’ Rule
- Nelson, D.(2020, 12 March). What is Bayes theorem? [Web log post]. Retrieved from https://www.unite.ai/what-is-bayes-theorem/

*Resource Overview:*

    This resource will help you understand the most common use of Bayes’ theorem in ML; that is, the Naïve Bayes’ classifier. Some variants of this classifier are also briefly discussed. Ensure that you read this concise resource before tackling the hands-on activity about scikit-learn.

> *Status: ✅ Read + Reviewed - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#4-what-is-bayes-theorem-nelson-2020)* 

#### 5. Introduction to Modern Bayesian Learning and Probabilistic Programming
- Neiswanger, W.(2019, 16 January). Intro to modern Bayesian learning and probabilistic programming [Web log post]. Retrieved from https://medium.com/@Petuum/intro-to-modern-bayesian-learning-and-probabilistic-programming-c61830df5c50

*Resource Overview:*

    This resource takes a close look at the reasons for using Bayesian programming. It also discusses a case study and the current challenges to capture probabilistic models for machine processing. An increasingly popular probabilistic programming framework provides users with an opportunity ‘to write down a Bayesian model, including the generative process, unknown model parameters, and prior beliefs about these parameters’ (Neiswanger, 2019). Once you complete this resource, take time to write your own Bayesian model, generative model, unknown parameters and previous beliefs. Use the ‘Has my milk gone bad?’ example and graphic aid to help you devise an example.

> *Status: ✅ Read + Reviewed - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#5-modern-bayesian-learning-and-probabilistic-programming-neiswanger-2019)* 

#### 6. Bayesian Inference and Predictive Models
- Reisz, W. (Interviewer). (2018, 31 August). Mike Lee Williams on probabilistic programming, Bayesian inference, and languages like PyMC3 [Audio podcast]. Retrieved from https://soundcloud.com/infoq-channel/mike-lee-williams-on-probabilistic-programming-bayesian-inference-and-languages-like-pymc3

*Resource Overview:*

    This podcast covers the concepts of Bayes’ rule as applied to probabilistic programming and databases. It also reminds us of the key advantages of using Bayes rule. The podcast discusses a number of Bayes applications, including clinical trials. The interviewer and guest discuss some extremely useful examples of Bayes, including the use of streaming data and the benefits of Bayesian predictions that are accompanied by measures of uncertainty. Pay careful attention to the interview, as the practitioners discuss the key concepts of Bayes’ rule and its applications in predictive modelling. Python/R tools and Python extensions are available to help with abstractions of deep mathematical and statistical concepts and to help describe problems using a Bayesian approach.

> *Status: 🔥 Primer ready - needs manual listen - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#6-probabilistic-programming-and-pymc3-podcast-williams-2018)* 

#### 7. Search and rescue
- Reisz, W. (Interviewer). (2018, 31 August). Mike Lee Williams on probabilistic programming, Bayesian inference, and languages like PyMC3 [Audio podcast]. Retrieved from https://soundcloud.com/infoq-channel/mike-lee-williams-on-probabilistic-programming-bayesian-inference-and-languages-like-pymc3

*Resource Overview:*

    This video resource on the Search and Rescue Optimal Planning System (SAROPS) used by the US Coast Guard illustrates a direct use of Bayes’ theorem to locate a person or object lost at sea by updating the probabilities based on sightings (evidence). The developer of this software is Metron (https://www.metsci.com), a company that provides assistance in locating anything from missing persons, missing submarines (e.g., the Soviet and USS Scorpion), sunken ships (e.g., SS Central America) to downed passenger planes (e.g., Air France 447). The company uses Bayes’ theorem to detect patterns in data  enabling the highlighting of primary focus targets, including The Lost Cities of Ecuador.

> *Status: 🔥 Primer ready - needs manual access - see [module05_notes.md](module-05-classification-and-bayes-rule/module05_notes.md#7-search-and-rescue-with-bayes-sarops)* 

### Learning Activities

#### 1. The German Tank Problem
- https://towardsdatascience.com/the-german-tank-problem-3455237aaf43/

The German tank problem provides a real-world example of thinking differently about data, behaviors, and decisions. This problem is a way to estimate a total population size by observing a small sample. It will help you to understand how estimators learn from data in scikit-learn. This problem helped the Allies in World War II to estimate the total number of German tanks from a small number of serial numbers observed from tanks and component parts. Today, the approach helps determine estimates of the units of iPhones sold.

To complete this activity, follow these steps:
1. Upload the notebook file provided (Tank_Problem.ipynb).
2. Review the Fahey (2019) article on the German tank problem and the difference between simulators and estimators.
3. Investigate how the first estimator (i.e., the maximum serial number of the captured tanks) turned out to be the maximum likelihood estimate (MLE).
4. Review the use of a Bayesian approach to reverse (invert) the observed data (i.e., the captured serial numbers) and simulate the parameters generating the data.
5. Follow the snippets of code to understand how the estimators were built to determine the number of tanks.
6. Follow the probabilistic programming (Bayesian) using the Python library pymc3 (this should be an import of the package in the code).

Share your results to the discussion forum and discuss your experiences, including the story of the tank problem. Do you have any other ideas as to where the approach could be used? Is the use of probabilistic programming to specify the problem in Bayesian terms helpful? How else can you solve the problem?

> *Status: 🕐 To-Do* 

#### 2. Naïve Bayes Classification and Titanic Data Set
- https://github.com/pb111/Naive-Bayes-Classification-Project/blob/master/Na%C3%AFve%20Bayes%20Classification%20with%20Python%20and%20Scikit-Learn.ipynb

This activity highlights the use of scikit-learn for classification using a variant of the Naïve Bayes’ classifier. We will predict the survival of a Titanic passenger based on the fare paid. Follow these steps:

1. Read the article by Martin (2018).
2. Access the Titanic data set from the link provided (either download it or read the data directly from the URL into your notebook).
3. Implement the Gaussian Naive Bayes’ classifier on the Titanic Disaster dataset using the notebook code snippets in the article using Sklearn (scikit-learn).
4. Interpret the results.
5. Share your experiences, including your interpretation and details of any issues you encountered and how you overcame them, to the discussion forum.

> *Status: 🕐 To-Do* 

---

## Module 6 - Support Vector Machines

### TLDR
A **Support Vector Machine (SVM)** is a supervised classifier that separates two classes with the **maximum-margin hyperplane** - the boundary is defined only by the **support vectors** (the points nearest it), which makes SVM naturally **robust to outliers**.
- **Soft margin + C:** real data isn't perfectly separable, so `C` trades margin violations against boundary hardness (a bias-variance dial).
- **Kernel trick:** swap the dot-product kernel for **polynomial** or **RBF** to bend the boundary into higher dimensions without computing those coordinates. RBF adds `gamma` (influence radius) - tune `C` + `gamma` with `GridSearchCV`.
- **Use it when:** many features, few rows ("short-and-fat" data), complex boundaries, outliers. **Avoid when:** you need transparency, a fast benchmark, or have huge low-dimensional data.
- **Always** scale features (`Pipeline(StandardScaler(), SVC())`) and judge with the **confusion matrix + `classification_report`** (precision/recall/F1), not accuracy - especially on imbalanced medical data.

> Full per-resource breakdown: [module06_notes.md](module-06-support-vector-machines/module06_notes.md)

### Introduction
In this Module, we will focus our attention on the support vector machines (SVM). A SVM is a supervised machine leaning (ML) algorithm that requires labelled or classified data for training. A SVM classifies data into one of two categories by finding a separating line (or hyperplane). The two videos below introduce SVMs—the videos touch on terms such as optimal hyperplane, decision boundaries, the kernel trick, maximum margin, support vectors and also discuss the circumstances in which SVMs are used.

Source: Loukas, S. (2020, 4 June). Support vector machines (SVM) clearly explained: A Python tutorial for classification problems with 3D plots. Retrieved from https://towardsdatascience.com/support-vector-machines-svm-clearly-explained-a-python-tutorial-for-classification-problems-29c539f3ad8

Video 1: McCormick, K. (2018). Linear SVM [Video file]. Retrieved from https://www.linkedin.com/learning/machine-learning-and-ai-foundations-classification-modeling/linear-svm?u=56744473

Video 2: Jedamski, D. (2019). What is support vector machine? [Video file]. Retrieved from https://www.linkedin.com/learning/applied-machine-learning-algorithms/what-is-support-vector-machine?u=56744473

When presented with a training set of examples marked as belonging to one of two categories, a SVM builds a model that is capable of assigning new incoming data to one category or the other. Additionally, for non-linear classifications, a SVM uses the kernel trick to map the data into a higher dimensional space to tease out the categories.

To help you gain a better understanding of the topic, this Module includes some videos and tutorial commentary about hands-on applications, including an application that uses SVM to classify muffin and cupcake recipes and also some of the more common face identification and cancer diagnoses applications. All these examples include notebooks with accompanying commentary in markdown to help reinforce the use of ML in Python using scikit-learn.

### Resources

#### 1. When Should You Consider Using Support Vector Machines
- Jedamski, D. (2019, 15 May). When should you consider using SVM? [Video file]. Retrieved from https://www.linkedin.com/learning/applied-machine-learning-algorithms/when-should-you-consider-using-svm?u=56744473

*Resource Overview:*

    This short video outlines when to use and when not to use SVMs. SVMs can be used for regression and classification; however, this video notes that the SVM is best used for classification problems with a binary target variable. Another important characteristic of the SVM is its ability to use many outliers and consider very complex relationships in relation to the binary target variable. Data sets with lots of features and very little data should fit SVMs.

> *Status: ✅ Watched + Reviewed - see [module06_notes.md](module-06-support-vector-machines/module06_notes.md#1-when-should-you-consider-using-svm-jedamski-2019)* 

#### 2. Visualisation of the Kernel Trick
- Aharoni, U. (2007, 5 February). SVM with polynomial kernel visualisation [Video file]. Retrieved from https://www.youtube.com/watch?time_continue=1&v=3liCbRZPrZA&feature=emb_logo

*Resource Overview:*

    No substitute exists for a clever visualisation. This visualisation nicely demonstrates the use of the ‘kernel trick’ showing how points of two different classes (red and blue dots) cannot be linearly separated in two-dimensional (2D) space. However, the trick allows the points to become linearly separated by a transformation function into a higher dimensional space. Here, the transformation is f([x,y]) = [x,y,(x^2 y^2)]. Given that the original dimensions are x and y, we add a third-dimension z = x^2 y^2. In the subsequent learning activities, we will actually compute the transformation and see it in action for a range of points.

> *Status: 🕐 To-Do* 

#### 3. Maximal Margin Classifiers
- Kennedy, M. Jaffe, B. & Malone, K. (2017a, 4 December). Maximal margin classifiers [Audio podcast]. Retrieved from http://lineardigressions.com/episodes/2017/12/3/maximal-margin-classifiers

*Resource Overview:*

    This podcast (Kennedy, Jaffe & Malone, 2017a) is a prerequisite to understanding SVMs. Margin classifiers provide an approach to thinking about supervised learning and the decision boundary separating two classes. This in turn helps create a simple theoretical model for understanding the SVM. The margin of a linear classifier is the distance from the decision boundary to the nearest point. The decision boundary is defined by a small number of points recognised as the support vectors. What if we make the margin as wide as possible? This question helps focus our thinking around SVMs.

> *Status: 🕐 To-Do* 

#### 4. The Kernel Trick and Support Vector Machines
- Kennedy, M., Jaffe, B. & Malone, K. (2017b, 10 December). The kernel trick and support vector machines [Audio podcast]. Retrieved from http://lineardigressions.com/episodes/2017/12/10/the-kernel-trick-and-support-vector-machines

*Resource Overview:*

    This podcast (Kennedy, Jaffe & Malone, 2017b) complements the podcast above (Kennedy, Jaffe & Malone, 2017a).

    Building on maximal margin algorithms and adding the kernel trick gives us the SVM. The kernel helps us find a plane (the line in two dimensions) in a higher dimensional space and project into a lower dimensional space. The kernel helps to separate out data points belonging to different classes with a plane (i.e., a good margin line that represents the decision boundary as far as possible from the points).

> *Status: 🕐 To-Do* 

#### 5. Support Vector Machines for Machine Learning
- Brownlee, J. (2020, 15 August). Support vector machines for machine learning. Retrieved from https://machinelearningmastery.com/support-vector-machines-for-machine-learning/

*Resource Overview:*

    This article, which includes minimal mathematics, revisits the maximal-margin classifier and the soft margin classifier. Notably, it also considers how other kernels like the radial and polynomial can be used. Read this article before consulting the Scikit documentation (see the next resource).

> *Status: ✅ Read + Reviewed - see [module06_notes.md](module-06-support-vector-machines/module06_notes.md#5-support-vector-machines-for-machine-learning-brownlee-2020)* 

#### 6. Scikit Documentation—Support Vector Machines
- Pedregosa, F., Varoquaux, G.,Gramfort, A.,Michel, V., Thirion, B., Grisel, O., Blondel, M.,Prettenhofer, P., Weiss, R.,Dubourg, V.,Vanderplas, J., Passos, A.,Cournapeau, D.,Brucher, M.,Perrot, M. & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research. 12, 2825–2830.  Retrieved from https://scikit-learn.org/stable/modules/svm.html

*Resource Overview:*

    This resource is a useful SVM reference document to keep handy, as it has useful tips for practical use.

> *Status: ✅ Read + Reviewed - see [module06_notes.md](module-06-support-vector-machines/module06_notes.md#6-scikit-learn---support-vector-machines-documentation-2011)* 

#### 7. Scikit Documentation—Quantifying the Quality of Predictions: The Confusion Matrix
- Pedregosa, F., Varoquaux, G.,Gramfort, A.,Michel, V., Thirion, B., Grisel, O., Blondel, M.,Prettenhofer, P., Weiss, R.,Dubourg, V.,Vanderplas, J., Passos, A.,Cournapeau, D.,Brucher, M.,Perrot, M. & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research. 12, 2825–2830.  Retrieved from https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix

*Resource Overview:*

    This resource will help you to understand the quality of your model prediction. Determining how well your model predicted or classified data helps determine the next steps, including everything from finding alternate models to fine tuning the hyperparameters.

    For the most common cases of scoring (i.e., classification, clustering or regression), scikit-learn provides predefine functions. In this resource, we focus our attention on the confusion matrix function for evaluating classification accuracy.

> *Status: ✅ Read + Reviewed - see [module06_notes.md](module-06-support-vector-machines/module06_notes.md#7-scikit-learn---metrics--the-confusion-matrix-2011)* 

#### 8. New Machine Learning Applications to Accelerate Personalised Medicine in Breast Cancer: Rise of the Support Vector Machines
- POzer, M., Sarica, P. & Arga, K. (2020). New machine learning applications to accelerate personalized medicine in breast cancer: Rise of the support vector machines. OMICS A Journal of Integrative Biology, 24(5),241–246. Retrieved from https://doi.org/10.1089/omi.2020.0001

*Resource Overview:*

    This article reinforces the importance of SVMs in public and clinical applications and examines the prediction models of breast cancer subtypes. Ensure that you consult Figure 1 to see how SVM is centre stage in disease classification. As the authors remind us, ‘SVM is a promising approach for development and application of the best medical practices and will be encountered more frequently in 2020 and the coming decade as the concept of precision/personalized medicine moves from theory to mainstream clinical practice’ (Ozer, Sarcia & Arga, 2020).

> *Status: 🕐 To-Do* 

### Learning Activities

#### 1. Kernel Trick Using Spreadsheet
- Malakar, G. (2016, 24 July). Introduction to support vector machine (SVM) and kernel trick [Data set]. Retrieved from https://drive.google.com/file/d/0Byo-GmbU7XciMUtJalFMUnlDRnM/view

In this activity, you will see for yourself two key aspects of SVMs: 1) the ability of SVMs to work with small data; and 2) the kernel trick. As a refresher, we use the kernel trick to separate linear and non-linear space. In this activity, you will use the transformation of variables to convert non-linear space into linear space. Some other SVM concepts you should keep in the mind are the maximum margin classifier, the support vectors located closest to the other class and hyperplane classification.

To complete this learning activity, follow these steps:
1. Access your Google drive and Google Sheets or Microsoft Excel;
2. Either upload the Excel sheet (Kernel_Trick for SVM.xls; Malakar 2016) to your Google drive or read it into Excel depending upon your preference.
3. Review each of the worksheets (data and chart) from left to right (original, transformed, base_eclipse_Data,base_eclipse_Data_1 and base_eclipse_Data_2 ).
4. In each worksheet, change the data but note the transformation of non-linear space into linear space and the hyperplane.
5. Share your thoughts to the discussion forum once you have completed the activity. Did this exercise help you understand the kernel trick?

> *Status: 🕐 To-Do* 

#### 2. Classification of Muffin and Cupcake Recipes Using SVMs
- Zhao, A. (2017, 21 August). Support vector machines: A visual explanation with sample python code [Video file]. Retrieved from https://www.youtube.com/watch?v=N1vOgolbjSc

For this activity, you should follow the YouTube tutorial and the provided Jupyter Notebook file. This activity uses SVMs to classify muffin and cupcake recipes.

To complete this learning activity, follow these steps:

1. Upload the file ‘Classification of Muffin and Cupcake Recipes using SVM.ipynb’ to your Notebook.
2. Watch the first part of the video (https://www.youtube.com/embed/N1vOgolbjSc) to the 3 minute 40 seconds mark. The first part of the video will serve as a refresher, as it provides a visual explanation of SVM concepts margin, support vectors and the hyperplane.
3. Complete the case study about using SVM to classify cupcake and muffin recipes by tuning the model and using the kernel trick (examples of the code are provided in your Notebook).
4. Follow the steps in the Notebook to:
   - import the Python libraries (matplotlib, numpy, pandas and sklearn);
   - import the data (the code reads in the data directly from the URL);
   - prepare the data;
   - fit the model;
   - visualise the results; and
   - predict a new case.
5. Share your feedback to the discussion forum regarding the difference between cupcakes and muffins once you have completed the activity. Did the explanation and working example help you understand SVMs in the short time allocated? From the learnings, how would you set the best C parameter? What setting for C would you select apart from the default?

> *Status: 🕐 To-Do* 

#### 3. Breast Cancer Classification Using Support Vector Machines
- Mel, L. (2019, 19 November). Breast cancer classification using support vector machines [Web log post]. Medium. Retrieved from https://medium.com/data-py-blog/breast-cancer-classification-using-support-vector-machines-23bd4cc2790b

FThe SVM is a popular ML algorithm for industrial applications, including image, face and medical classification applications (Ozer et al., 2020). This activity focuses on breast cancer classification. After you have uploaded the Notebook code, you will find a very short narrative at: https://medium.com/data-py-blog/breast-cancer-classification-using-support-vector-machines-23bd4cc2790b.

To complete this learning activity, follow these steps:

1. Upload the file ‘Breast_Cancer_Classification_Using_SVM.ipynb’.
2. Follow the markdown steps outlined in the notebook code and execute each stage of the analysis to gain an understanding of the Python and ML code being used.
3. Consult the online scikit-learn documentation as necessary to gain an understanding of the parameter settings (e.g., the grid-searches in model tuning).
4. Execute the code step by step without error.
5. Share your thoughts to the discussion forum on the accuracy of the model and implications once you have completed the activity.

> *Status: 🕐 To-Do* 

#### 4. Face Recognition Using SVM and Pre-COVID-19 algorithms
- Pedregosa, F., Varoquaux, G.,Gramfort, A.,Michel, V., Thirion, B., Grisel, O., Blondel, M.,Prettenhofer, P., Weiss, R.,Dubourg, V.,Vanderplas, J., Passos, A.,Cournapeau, D.,Brucher, M.,Perrot, M. & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research. 12, 2825–2830.  Retrieved from https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html
- Ngan, M., Grother, P. & Hanaoka, K. (2020). Part 6A: Face recognition accuracy with masks using pre-COVID-19 algorithms. In Ongoing face recognition vendor test (FRVT). National Institute of Standards and Technology, US Department of Commerce. Retrieved from https://pages.nist.gov/frvt/reports/facemask/frvt_facemask_report.pdf
SVM is a popular ML algorithm for industrial applications, such as face classification. For this activity, we will review and analyse the ML code to train a SVM classifier to recognise faces. The source for the facial images is Labelled Faces in the Wild (LFW; http://vis-www.cs.umass.edu/lfw/). The data set contains more than 13,000 images of faces collected from the web; each face in the data set is labelled with the name of the person. The database is available through sklearn.datasets import fetch_lfw_people.

To complete this learning activity, follow these steps:

1. Upload the file ‘SVM_Face_Recognition_using_LFW.ipynb’.
2. Follow the markdown steps outlined in the notebook code and execute each stage of the analysis to gain an understanding of the Python and ML code being used.
3. Consult the online scikit-learn documentation as necessary to gain an understanding of the scikit code used in this notebook (e.g., the sklearn datasets).
4. Execute the code step by step without error.
5. Review the report entitled, ‘United States Ongoing Face Recognition Vendor Test (FRVT)’. Pay particular attention to Part 6A (which examines face recognition accuracy with masks using pre-COVID-19 algorithms). This is available at: https://pages.nist.gov/frvt/reports/facemask/frvt_facemask_report.pdf.
6. Share your thoughts to the discussion forum for SVM applications on the usefulness of the classification report for face recognition once you have completed the activity. What do you think about using eigenfaces as the pre-processing step for facial recognition? How can we improve our accuracy and thus algorithms in a world in which faces are obfuscated by masks?

> *Status: 🕐 To-Do*

#### 5. Wine Classification Using a Support Vector Machine
The SVM is a popular ML algorithm. You will not be surprised to find out that our familiar red wine data set (https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv) has been used in a wine classification exercise.

To complete this learning activity, follow these steps:

1. Upload the file ‘Wine_Classification_and_SVM’.
2. Follow the markdown steps outlined in the notebook code and execute each stage of the analysis to gain an understanding of the Python and ML code being used.
3. Go through the early stages of the notebook right through to finding correlations, with which you should be familiar by now.
4. Execute the code step by step without error.
5. Follow the steps to go from a continuous variable to a categorical variable.
6. Consult the relevant online documentation to sort data values into bins using cut().
Share your thoughts on the Wine Classification to the SVM discussion forum and describe how well your SVM model performed once you have completed the activity.

> *Status: 🕐 To-Do*

---

## Module 7 - Automated and Explainable Machine Learning

### TLDR
Two linked ideas that bookend the ML lifecycle:
- **Automated ML (Auto ML)** automates the *whole pipeline* — data cleaning, feature engineering, model selection and **hyperparameter tuning** — not just tuning. It is a **productivity tool, not a replacement** for data scientists (Olson). Modern search uses **Bayesian optimisation, genetic programming and meta-learning**; tools include **TPOT, Auto-sklearn, H2O AutoML**.
- **Explainable ML (XAI)** makes predictions justifiable — answering *why did it do that?* and *when can I trust it?* Core distinctions: **intrinsic** (linear/logistic regression, decision trees) vs **post-hoc/model-agnostic** (**SHAP, LIME, permutation importance, PDP**), and **global** (feature importance) vs **local** (SHAP on one instance). Central tension = **performance vs explainability**; DARPA's XAI aims for both. Warning: a *wrong* explanation is worse than none. Beyond technique, explainability is now a **governance requirement** — NZ's Algorithm Charter + Data Ethics Advisory Group (Sowden) make it a public-policy expectation, not optional.

### Introduction
This Module focuses on two important and related areas: the automation and explanability of Machine Learning (ML).

Automated (auto) ML accelerates the construction and production of models, from access to the data through to ML model deployment. Without human intervention, auto ML extracts the most relevant features from data, selects relevant algorithms, tunes the hyperparameters and applies the model to unseen data.

Explainability shows how data relates to the final model, prediction and features. Explainability helps build trust in the prediction and helps answer questions like, ‘Why did it do that?’ and ‘How does it work?’. Most importantly, explainability will help you to tell a story about your own analysis of the data when presenting the data to non-technical staff and other stakeholders.

For example, imagine that you apply for a bank loan online and input the necessary data. After which, you receive an answer as to whether the bank loan is likely to be approved or not. The decision is reached through the use of automated ML without human involvement. If you did not succeed in getting a bank loan, the website may not provide an explanation as to the reason why. This issue can be resolved by using the explaining the use of ML (explainability)to provide consumers with a rationale as to why they did not receive a loan.

### Resources

#### 1. The Past, Present and Future of Automated Machine Learning
- Olson, R. (2018, 15 July). The past, present, and future of automated machine learning [Video file]. Retrieved from https://www.youtube.com/watch?v=QrJlj0VCHys

*Resource Overview:*

    In this video, Dr Randal Olson discusses the benefits of automated ML, its future and provides a screen demonstration of the key concepts using scikit-learn. Dr Olson is a researcher and practitioner. He developed one of the first auto ML tools—the TPOT. Follow the narrative provided by Dr Olson as he works on his notebook. This skill of being able to use the notebook and talk out loud about what is happening as the notebook runs is extremely valuable. Try talking out loud sometime and tell the story of your data analysis. The Auto ML tools operate alongside and seamlessly with the scikit-learn environment. Having viewed the video, how much time do you think Auto ML tools will help save? Do you agree with Dr Olson’s view on the future of Auto ML?

> *Status: ✅ Read + Reviewed — see [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md)*

#### 2. Auto ML—Automated ML (in Plain English)
- Kennedy, M. Jaffe, B. & Malone, K. (2018, 29 April). AutoML [Audio podcast]. Retrieved from http://lineardigressions.com/episodes/2018/4/29/automl

*Resource Overview:*

    In this video, Dr Randal Olson discusses the benefits of automated ML, its future and provides a screen demonstration of the key concepts using scikit-learn. Dr Olson is a researcher and practitioner. He developed one of the first auto ML tools—the TPOT. Follow the narrative provided by Dr Olson as he works on his notebook. This skill of being able to use the notebook and talk out loud about what is happening as the notebook runs is extremely valuable. Try talking out loud sometime and tell the story of your data analysis. The Auto ML tools operate alongside and seamlessly with the scikit-learn environment. Having viewed the video, how much time do you think Auto ML tools will help save? Do you agree with Dr Olson’s view on the future of Auto ML?

> *Status: 🔌 Discontinued — the Resource Overview above is a copy-paste of Resource 1's (it describes Olson's video, not this podcast); audio-only with no transcript; content duplicates Olson. Rationale in [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md).*

#### 3. Awesome-Auto ML-Papers (curated)
- Mark, L. (Ed.). (2020, 15 August). Awesome-autoML-papers. Retrieved from https://github.com/hibayesian/awesome-automl-papers

*Resource Overview:*

    This resource includes a curated list of automated ML papers, articles, tutorials, slides and projects. It includes useful references in this dynamic and ever growing area of ML, provides a useful mind map that encapsulates the field of auto ML and provides the details of some projects being carried out. This is a very useful curation for exploring Auto ML beyond this subject and into the workplace.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md)*

#### 4. DARPA (US Defense Advanced Research Projects Agency) Explainable Artificial Intelligence
- Aha, D. (2019, 26 March). Artificial intelligence colloquium: Explainable AI https://www.youtube.com/watch?v=YSsYXAn_L00

*Resource Overview:*

    This talk highlights the United States defence (and non-defence) activities in explainable ML techniques. It should be noted that for this resource, the term artificial intelligence (AI) is used interchangeably with ML. The goal of the programme is to produce more explainable models while maintaining performance to enable users to understand and trust the models that power the analytics to make discoveries in the data and autonomous applications. A supporting slide pack (Gunning, 2016) helps illustrate the evaluation framework used to explain the effectiveness and sequence of steps used to conduct the evaluation. This video and slide pack highlight the importance of explainability and identify the challenges facing this emerging field, especially in high-stake decision domains, such as defence and medicine.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md)*

#### 5. Transparency and Accountability of Government Algorithms
- Snowden, M. (2018, 15 July). Transparency and accountability of government algorithms [Video file]. Retrieved from https://www.youtube.com/watch?v=Jpbd-5r3xO8

*Resource Overview:*

    In this video, Mark Sowden, Government Chief Data Steward, outlines the steps undertaken by the New Zealand (NZ) government to improve the transparency and accountability of government-used algorithms. This work builds on the Algorithm Assessment Report (Stats NZ, 2018) that recommended that algorithms and their effects on people be explainable.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md)*

#### 6. Interpretable Machine Learning
- Molnar, C. (2019). Interpretable machine learning: A guide for making black box models explainable. Retrieved from https://christophm.github.io/interpretable-ml-book/

*Resource Overview:*

    In this freely available book, the author really tries to capture how you make supervised ML models interpretable. Without reverting to any fashionable techniques, this PhD researcher tries to bring together some basic concepts and established methods. R packages (but not Python) are provided. Additionally, explanations are provided for each of the models and the accompanying examples have an easy to follow narrative. At a minimum, you should follow read Chapter 4 in one sitting to understand the explainers for each type of algorithm.

> *Status: ✅ Read + Reviewed — see [module07_notes.md](../modules/module-07-automated-explainable-ml/module07_notes.md)*

#### 7. Week 7 live lectures (not in the official resource list — the most load-bearing source in the module)
- Shaukat, K. (2026). *Week 7 - Part 1: Assessment 2 Discussion* (83 min) and *Week 7 - Part 2* (63 min) [Class recordings].

*Why it matters:*

    Part 1 is effectively the Assessment 2 specification, dictated: the target encoding (quality < 6 -> 1 = bad, so the positive class is the BAD wine), the four named grade levers (many models with rationale, SMOTE, GridSearchCV(cv=5), XAI), the four-files-no-zip submission rule, and the 7-10 min video format (notebook + webcam + student ID, no PowerPoint). Part 2 is the XAI lecture — and it never mentions Auto ML once, which reprioritises the whole module: Auto ML is readings-only, XAI is what carries marks.

> *Status: ✅ Transcribed (whisper.cpp, medium.en) + summarised — see [module07_notes-class.md](../modules/module-07-automated-explainable-ml/module07_notes-class.md)*

### Learning Activities

#### 1. Visually Probe Machine Learning Models—The Google What-If Tool

A number of ML explainable tools require that significant efforts be undertaken to install the software. The tools for this hands-on activity were selected to enable you to rapidly start to work with the tools and explore the data and algorithms for explainability. 
The number of tools and frameworks in this rapidly evolving field continues to increase. The first tool integrates directly with the Google AI platform to make the vision of explainable automated ML a reality. The What-If tool is an interactive visual interface designed to visualise data and enable the probing of ML models with little or no coding.

To complete this learning activity, follow these steps:

1. Log into your Google Colab notebook.
2. Review details of the What-if tool at the landing page: https://pair-code.github.io/what-if-tool/.
3. Execute and explore at least two of the following four notebook demonstrations (use the links below to gain access to already preconfigured notebooks). You can:
   - Train and compare wine quality models with an AI Platform https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/keras_sklearn_compare_caip_e2e.ipynb. This notebook compares the results of models run in two different Python libraries shallow (scikit-learn) and deep (Keras);
   - Explore celebrity face image smile classification https://colab.research.google.com/github/PAIR-code/what-if-tool/blob/master/WIT_Smile_Detector.ipynb.
   - Investigate the fairness of recidivism classification https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_COMPAS.ipynb; and/or
   - Compare income classification on UCI census data https://colab.research.google.com/github/pair-code/what-if-tool/blob/master/WIT_Model_Comparison.ipynb.
4. Execute ('Run all') for each of your notebook selections and follow the suggested prompts indicated within the notebooks and the exploration ideas section at the end of each notebook
5. Share your thoughts to the discussion forum once you have completed the activity. In the discussion forum, consider if the tool has the potential to avoid or at least minimise the issues you envisage emerging from running algorithms that affect humans. Now that you have an understanding of the What-if tool, expand on your understanding of using the tool within the online forum. Do you need special expertise to understand the outputs?

> *Status: ✅ Done — rebuilt locally (WIT is Colab-only), see [activity1_what_if_wine.ipynb](../modules/module-07-automated-explainable-ml/activities/activity1_what_if_wine.ipynb)*

#### 2. Bank-Loan Activity Using an Open Source Toolkit for Explainability
- IBM Research. (2019, 8 August). Making AI more trusted, by making it explainable [Video file]. Retrieved from https://www.youtube.com/watch?time_continue=3&v=dSYnNtH_8LY&feature=emb_logo
- Mojsilovic, A. (2019, 8 August). Introducing AI Explainability 360. [Web log post]. Retrieved from https://www.ibm.com/blogs/research/2019/08/ai-explainability-360/

No single approach to explaining decisions made by algorithms exists. Depending upon the perspective being sought, the consumer, front-office staff member, data scientist or regulator require different explanations when it comes to the support of algorithmic decision making. The IBM toolkit (Mojsilovic, 2019) tackles explainability through one interface. IBM positions the toolkit as an AI toolkit; however, our focus is on a subset of AI—ML algorithms.

To complete this learning activity, follow these steps:

1. Review the video (IBM Research, 2019).
2. Consider explainability in the context of a bank loaning money and making decisions to accept or reject an applicant on the basis of an algorithm.
3. Review the bank loan scenario in detail step by step using the AI Explainability 360—Demo http://aix360.mybluemix.net/data.
4. Choose each consumer type (e.g., a data scientist, a loan officer and a bank customer) and see what explanation each consumer type needs to understand when it comes to explainability.
5. As part of your discovery, explore the objectives of the Contrastive Explanations Method (CEM) explainer algorithm and Protodash explainer.
6. Peruse the notebook code for the credit approval (you do not have to load this into your own notebook, simply use the nbviewer already provided) https://nbviewer.jupyter.org/github/IBM/AIX360/blob/master/examples/tutorials/HELOC.ipynb#2.3.-Ruen-Logistic-Rule-Regression-(LogRR).
7. Share your thoughts to the discussion forum on explainability once you have completed the activity. Take the bank loan scenario one stage further when sharing your experience—assume that every time the bank decides to reject a loan application, a legal obligation exists that requires the bank to explain the basis for each loan rejection. Do you feel that with the scenario and supporting algorithms that you have the ability to sufficiently explain the basis of the machine decision? What might you be missing?

> *Status: ✅ Done — rebuilt locally (aix360.mybluemix.net is dead), see [activity2_bank_loan_explainability.ipynb](../modules/module-07-automated-explainable-ml/activities/activity2_bank_loan_explainability.ipynb)*

#### 3. SHapley Additive exPlanations (SHAP) and Explainer Dashboard
- Molnar, C. (2019). Interpretable machine learning: A guide for making black box models explainable. Retrieved from https://christophm.github.io/interpretable-ml-book/shap.html

SHapley Additive exPlanations (SHAP) is a popular and well-established model agnostic technique that is used to explain predictions. It was first proposed in 1953. The aim of SHAP ‘is to explain the prediction of an instance x by computing the contribution of each feature to the prediction’ (Molnar, 2019). This task is far from easy. Exploring and explaining the workings of an ML model likely requires a dashboard to make sense of a variety of outputs (e.g., SHAP, predictions, model performance and feature importance). The explainer dashboard is a Python package that enables a rapid build of a dashboard to explore ML. You could install this library with pip install explainer dashboard and find the documentation at: https://explainerdashboard.readthedocs.io/en/latest/; however, in the interest of time, we will use existing demonstrations of the dashboard for this activity.

To complete this learning activity, follow these steps:

1. Rapidly explore the effects of different features on model prediction.
2. Consult and keep Molnar’s (2019) text accessible as a reference (as required).
3. Apply a classifier explainer to the ML output. One popular exercise for ML in competitions is to predict which individual/s will survive the Titanic.
4. View the explainer dashboard deployment at http://titanicexplainer.herokuapp.com/classifier/. ⚠️ *(This Heroku deployment is offline - rebuilt locally, see status note below.)*
5. Review and interact with the dashboard. Pay attention to feature importances, model performance, individual predictions, feature dependence, feature interactions and decision trees.
6. View the explainer dashboard deployment at http://titanicexplainer.herokuapp.com/regression/ for the fare paid for a ticket on the Titanic. ⚠️ *(Offline - use the local rebuild in the status note below.)*
7. Repeat Step 5 for the Regression Explainer.
8. In the discussion forum, share how well you believe the model performed in predicting survival. Which parameters are the most important in relation to survival? What is the relationship between the features and the model output? What do you think about the explainer dashboard being used in the workplace or consumers having access to such a dashboard whenever a ML decision is made that affects humans?

> *Status: ✅ Done — rebuilt locally (titanicexplainer.herokuapp.com is dead), see [activity3_shap_titanic.ipynb](../modules/module-07-automated-explainable-ml/activities/activity3_shap_titanic.ipynb)*

#### 4. SHapley Additive exPlanations (SHAP) and Explainer Dashboard
- Raschka, S. (2017, 21 October). Mlxtend 0.9.0. Retrieved from https://sebastianraschka.com/pdf/software/mlxtend-latest.pdf

As you can see, explainable ML is an emerging field and a number of software packages and library routines are available for interpreting and explaining ML models. This hands-on activity considers three popular packages: 1) Explain like I am a 5-year old (Eli5); 2) Local interpretable model-agnostic explanations (Lime); and 3) Machine learning extensions with lots of useful tools (Mlxtend) (see Raschka, 2017).

To complete this learning activity, follow these steps:

1. Upload the notebook Interpretable_ML_Python_Libraries.ipynb.
2. Follow the markdown steps outlined in the notebook code and execute each of the packages of the analysis.
3. Execute the code step by step without error.
4. Inspect feature importances as a strategy for a trained model using Eli5, interpret some predictions using LIME and look at decision boundaries using Mlxtend.
5. Share your experience of using each of the tools to the discussion forum once you have completed the activity. How does having access to these tools compare with the explainer dashboard?

> *Status: ✅ Done — see [activity4_eli5_lime_mlxtend.ipynb](../modules/module-07-automated-explainable-ml/activities/activity4_eli5_lime_mlxtend.ipynb) — the explainers **contradict each other**: Eli5 reports every local sign inverted*

---

## Module 8 - Logistic Regression

### TLDR
**Logistic regression** is linear regression pushed through a **sigmoid** (`1 / (1 + e^(−z))`) so the output is a **probability in (0, 1)**, thresholded at 0.5 into a class. Despite the name, it is a **classification** algorithm — the go-to for **binary** problems.
- **Representation = coefficients**, just like linear regression: `ln(p/(1−p)) = β₀ + βᵢxᵢ`. The left side is the **log-odds / logit**; `Exp(β)` = **odds ratio** → this is what makes LR **intrinsically interpretable** (ties back to Module 7 XAI).
- Coefficients are learned by **Maximum-Likelihood Estimation** (L-BFGS/ADAM in practice; gradient descent from scratch) on a **log-loss** cost.
- **The hyperparameter that matters is `C` = 1/λ** (inverse regularisation): **smaller `C` = stronger regularisation = simpler model**. Tune it with `GridSearchCV`, alongside **`penalty`** (L1/L2) — the two dials the week 8 lecturer named. Standardise features first — regularisation needs comparable scales.
- **Sigmoid vs softmax:** sigmoid = **binary** (one probability); softmax = **multi-class** (a distribution summing to 1). Live class exercise in week 8 — see class notes.
- **Limitations:** assumes a **linear decision boundary**, **sensitive to outliers**, overfits with many features/few rows, can't handle missing values directly. And **"there is no best model"** — hence the 5-model comparison table in Assessment 2.
- **Imbalance is LR's Achilles heel:** it favours the majority class (97% "accuracy" catching zero rare cases). Fix with **SMOTE** or **`class_weight='balanced'`**, and **evaluate with the confusion matrix + precision/recall/F1**, never accuracy alone.
- **LR = one neuron** (linear core + sigmoid activation) — the foundation for neural networks.

> Full per-resource breakdown: [module08_notes.md](module-08-logistic-regression/module08_notes.md)
> Week 8 live session: [module08_notes-class.md](module-08-logistic-regression/module08_notes-class.md) · Revision sheet: [module08_one-pager.md](module-08-logistic-regression/module08_one-pager.md)

### Introduction
This Module will show you how to do machine learning (ML) using the pre-built logistic regression model from scikit-learn library. Logistic regression predates ML as a statistical approach that is ideally suited to binary classification problems. The method dates as far back as the early 19th century when it was applied to estimate population growth and chemical reactions. The types of problems have two class values (e.g., yes/no, red/white, positive or negative sentiment, pass/fail or 1/0); however, discrete (two or more classes) classification can also be handled e.g. predict the mood of a tweet or which promotion of the three is most attractive to customers? The learning activities will reinforce the importance of having the right and sufficient data for testing. You will learn the entire process for logistic regression, from inputting data to training and testing the model (see the CRISP-DM templates for a more detailed and expanded description).

### Resources

#### 1. Logistic Regression
- McCormick, K. (2018, 20 August). Logistic regression [Video file]. Retrieved from https://www.linkedin.com/learning/machine-learning-and-ai-foundations-classification-modeling/logistic-regression?resume=false&u=56744473

*Resource Overview:*

    This video provides some background to logistic regression. Notably, it discusses use of Titanic data to determine the male survivors, the coefficients of variables and the confusion matrix.

> *Status: ✅ Watched + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#1-mccormick-k-2018-logistic-regression-video)*

#### 2. Logistic Regression
- Renelle, T. (2017, 19 February). Episode #007: Logistic regression [Audio podcast]. Retrieved from https://player.fm/series/machine-learning-guide-1457335/7-logistic-regression

*Resource Overview:*

    This podcast provides an introduction to logistic regression and serves to remind you of the classification capability of logistic regression. The audio explanation is comprehensive and very understandable and does not refer to any diagrams. The podcast positions logistic regression in relation to linear regression and extensively covers the vocabulary of logistic regression (e.g., labels and error function).

> *Status: ✅ Listened + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#2-ocdevel--renelle-t-2017-mlg-007-logistic-regression-podcast)*

#### 3. What are the Key Hyperparameters to Consider in Logistic Regression?
- Jedamski, D. (2019, 15 May). What are the key hyperparameters to consider? [Video file]. Retrieved from https://www.linkedin.com/learning/applied-machine-learning-algorithms/what-are-the-key-hyperparameters-to-consider-2?u=56744473

*Resource Overview:*

    This resource helps to reinforce the importance of focusing on the C parameter when tuning your model. It also discusses the model attributes and the fit and predict methods.

> *Status: ✅ Watched + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#3-jedamski-d-2019-key-hyperparameters-to-consider-video)*

#### 4. Training a Logistic Regression Model with Scikit-Learn
- Raschka, S. & Mirjalili, V. (2019). Python machine learning: Machine learning and deep learning with python, scikit-learn, and tensorflow (3rd ed).Birmingham, UK : Packt. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=6005547&ppg=101

*Resource Overview:*

    Before coding your ML using logistic regression, you need to understand the terms, names and coefficients describing the model. When reading this chapter, ignore discussions about the perceptron, Adaline and Support Vector Machines. Pay attention to the code snippets and parameter C. You should try to read the chapter without going too deep into the statistics. Keep the chapter handy as a reference and return to it as required. See pages 72–78 (Raschka & Mirjalili, 2019 for the pages relevant to the logistic regression model).

> *Status: ✅ Read + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#4-raschka-s--mirjalili-v-2019-training-a-logistic-regression-model-with-scikit-learn)*

#### 5. Logistic Regression Everything You Need to Know for Machine Learning
- Brownlee, J. (2019, 12 August). Logistic regression for machine learning [Web log post]. Retrieved from https://machinelearningmastery.com/logistic-regression-for-machine-learning/

*Resource Overview:*

    This post requires only a limited knowledge of statistics. It will help you to come to grips with the terminology. You will also learn how to make predictions using logistic regression. Of all the resources, this resource details everything you need to know about logistic regression, including how coefficient values are estimated using Maximum Likelihood Estimation.

> *Status: ✅ Read + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#5-brownlee-j-2019-updated-2023-logistic-regression-for-machine-learning)*

#### 6. Measures of Fit for Logistic Regression
- Allison, P. (n.d.). Measures of fit for logistic regression [Web log post]. Retrieved from https://support.sas.com/resources/papers/proceedings14/1485-2014.pdf

*Resource Overview:*

    This article takes the perspective of a statistician to highlight the complexity of ensuring the goodness-of-fit of a logistics regression model. Scikit-learn can be used to generate logistic models and determine the quality of predictions. However, this does not mean a fitted model will be ideal for predictions or classifications. Having some understanding of the complexity of fitting models will be useful in your final model evaluations. This resource has been written for the popular Statistical Analysis Software (SAS).

> *Status: ✅ Read + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#6-allison-p-d-2014-measures-of-fit-for-logistic-regression)*

#### 7. Understanding Confusion Matrix
- Narkhede, S. (2018, 9 May). Understanding confusion matrix [Web log post]. Retrieved https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62

*Resource Overview:*

    To measure the effectiveness of a model, the scikit-learn user has access to a variety of metrics and scores (see https://scikit-learn.org/stable/modules/model_evaluation.html). Using data, the ability to train_test_split and validate the model via an outside data set or by splitting the available data. Taking this approach  stops the model from having to memorise the data set and performing with unseen data. The confusion matrix is the most easily available output. This resource provides a simplified overview of a confusion matrix in the context of a two classification type problem.

> *Status: ✅ Read + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#7-jayaswal-v--narkhede-s-2020-understanding-the-confusion-matrix-precision-recall-f1)*

#### 8. Scikit-learn Logistic Regression
- Pedregosa, F., Varoquaux, G.,Gramfort, A.,Michel, V., Thirion, B., Grisel, O., Blondel, M.,Prettenhofer, P., Weiss, R.,Dubourg, V.,Vanderplas, J., Passos, A.,Cournapeau, D.,Brucher, M.,Perrot, M. and Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research. 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#examples-using-sklearn-linear-model-logisticregression

*Resource Overview:*

    This resource is a useful reference when writing ML code using scikit-learn logistic regression. An example of code is provided to help you follow the scikit implementation. The user guide (available at https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) is an additional resource and worth consulting when working on a logistic problem.

> *Status: ✅ Read + Reviewed - see [module08_notes.md](module-08-logistic-regression/module08_notes.md#8-pedregosa-et-al-2011-scikit-learn-logisticregression-reference)*

### Learning Activities

#### 1. Top Machine Learning Algorithms, Frameworks, Tools and Products Used by Data Scientists
- Hayes, B. (2020, 24 July). Top machine learning algorithms, frameworks, tools and products used by data scientists. Retrieved from https://customerthink.com/top-machine-learning-algorithms-frameworks-tools-and-products-used-by-data-scientists/

The results of the Kaggle survey of nearly 20,000 data professionals reveals the most popular ML algorithms, frameworks, tools and products.

Read about the results at https://customerthink.com/top-machine-learning-algorithms-frameworks-tools-and-products-used-by-data-scientists/. Use the discussion forum to share your thinking on the algorithms, frameworks and products. Do not worry about the tools category (unless you have some experience), as we will cover this aspect in module 12. Your discussion should include your experiences with using each of the components featured in the polls. Would you wish to make any changes to the rankings, especially those the top three of each category? Please explain your views and share your thinking on the discussion forum.

> *Status: 🕐 To-Do* 

#### 2. Logistic Regression and Examination Prediction
- Dhiraj, K., (2020, 10 January). Logistic regression in Python using scikit-learn. Medium. Retrieved from https://heartbeat.fritz.ai/logistic-regression-in-python-using-scikit-learn-d34e882eebb1

This activity is about generating a logistic regression classifier for a pass/fail examination.

To complete this learning activity, follow these steps:

1. Upload Logistic_Regression_and_Exam_Prediction.ipynb. This file must be loaded to your notebook.
2. Read Dhiraj (2020).
3. Run all the code.
4. Try to accept all the default values for the model and monitor the results.
5. Add some comments to help you follow the notebook model.
6. Share your comments to the discussion forum and discuss your use of scikit-learn logistic regression. Share your commented notebook file and discuss any aspects of the modelling that required further details as indicated by your own additions. Additionally, consider answering the following questions in your post:
- Were there any major issues?
- Did you try tweaking any parameters?
- What happened when you chose all default values for the model parameters?

> *Status: 🕐 To-Do* 

#### 3. Prediction Purchase of New Launch Product
- Geeksforgeeks. (2019, 29 April). ML | Logistic regression using Python. Retrieved from https://www.geeksforgeeks.org/ml-logistic-regression-using-python/

The logistic regression model we will build will predict whether a user will purchase a product (or not) based on data from the customer database.

To complete this learning activity, follow these steps:
1. Upload Prediction Purchase New Launch Product.ipynb to your notebook.
2. Read Geeksforgeeks (2019).
3. Upload launch.csv e.g. Google Drive.
4. Run all the code.
5. Analyse or rather specify your predictions as indicated by the confusion matrix.
6. Review the accuracy of the model.
7. Look at the visualisation generated.
8. Share a post to the discussion forum detailing how well the model performs. You will need to qualify your answer with feedback on the accuracy, confusion matrix and graph.

> *Status: 🕐 To-Do* 

#### 4. Tuning Hyperparameters for Logistic Regression Using the Iris Dataset
We will now focus our attention on tuning parameters for logistic regression.

To complete this learning activity, follow these steps:

1. Upload Tuning_Hyperparameters_for_Logistic_Regression.ipynb. This file must be loaded to your notebook.
2. Walk through import of packages and load the iris dataset (further details of this data set available at https://archive.ics.uci.edu/ml/datasets/iris).
3. Visualise the data plots to show sepal width versus sepal length and petal width versus petal length.
4. Create function to plot decision surface (initalise with colour mapping relating to amount of classes in target data, parameters for graph and decision surface) 
5. Split the available dataset into two subsets comprising training data (this data will be used to train the model) and testing data (this data will be used to compare the performance of the model with the test set).
6. Test the sepal data with different regularisation values (to improve generalisation performance on unseen data).
7. Test the petal data with different regularisation values (to improve generalisation performance on unseen data).
8. Generate validation curves and commentary.
9. Share your comments to the discussion forum regarding each of the steps (i.e., Steps 1–9). Did you encounter any major issues? If so, how did you overcome them? Which parameters did you try modifying?

> *Status: 🕐 To-Do* 

#### 5. Red Wine Quality Classification with Logistic Regression
- Cortez, P., Cerdeira, A., Almeida, F., Matos, T. & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. Decision Support Systems, 47(4), 547–553. Retrieved from https://www.sciencedirect.com/science/article/abs/pii/S0167923609001377

To complete this learning activity, follow these steps:

1. Upload Red_Wine_Quality_Classification_with_Logistic_Regression.ipynb.
2. Walk through the import of packages.
3. Load red wine quality data (description available at: https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv);
4. Complete the data visualisation of the wine features (12) and values.
5. Implement models: Normalise data using the mean and standard deviation of the training data.
6. Implement models: Calculate the Sigmoid function.
7. Implement models: Perform training in the training dataset (using the gradient descent).
8. Split the available dataset into two subsets comprising training data (this data will be used to train the model) and testing data (this data will be used to compare the performance of the model with the test set).
9. Predict the results using the test dataset and evaluate the accuracy of the test dataset.
10. Describe the accuracy of the train and test datasets on the discussion forum. Do you agree with the cut-off for wine quality? Is it arbitrary? Which psychochemical properties (variables) make the wine good?
Reference

> ⚠️ **Go beyond accuracy.** The brief stops at train/test accuracy, but this module's own through-line - and Assessment 2 - require more: tune **`C`** with `GridSearchCV`, handle the **class imbalance** (the "bad" wine class is the minority) with SMOTE or `class_weight='balanced'`, and report the **confusion matrix + precision/recall/F1** on the minority class, not accuracy alone. Accuracy on imbalanced wine data is exactly the metric resource 5 warns against. See the synthesis in [module08_notes.md](module-08-logistic-regression/module08_notes.md#synthesis--how-the-eight-fit-together).

> *Status: 🕐 To-Do* 

---

## Module 9 - K-means Clustering

### TLDR
**K-means** is an **unsupervised** algorithm — no labels, no target column. You **pre-define k**, and it finds **k centroids** and assigns every point to its nearest one. This is the module's break from Modules 3-8: clustering is **discovery**, not prediction.
- **Lloyd's algorithm, 3 steps:** initialise k centroids → assign each point to the nearest → move each centroid to the mean of its points → repeat until the centroids stop moving (below tolerance).
- **The objective is inertia** = **within-cluster sum-of-squares (WCSS)** = `Σ min‖xᵢ − μⱼ‖²`. Lower is better. Centroids are **means, not data points**.
- **Choosing k is the hard part:** the **elbow method** (plot WCSS vs k, find the bend), the **silhouette coefficient** (maximise it), or the **gap statistic**. There is no single right answer — which is exactly what the discussion activities ask about.
- **Evaluation forks on ground truth.** With labels: **ARI, homogeneity, completeness, V-measure**. Without: **silhouette (−1 to 1, higher better)**, **Calinski-Harabasz (higher better)**, **Davies-Bouldin (lower better)**. ⚠️ All three are biased toward **convex** clusters.
- **Weaknesses:** must specify k up front · **sensitive to outliers** · assumes **flat geometry and even cluster sizes** · converges only to a **local** minimum (fix with `init='k-means++'` + `n_init`) · degrades in high dimensions (run **PCA** first).
- **Scale your features first** — K-means is distance-based, so an unscaled wide-range feature dominates every centroid. For big data use **`MiniBatchKMeans`**; for large k, **`BisectingKMeans`**.
- **⭐ (Week 9 lecture, beyond the readings) Distance metrics are the foundation:** **Euclidean** (square then root — kills sign, re-normalises scale); **Minkowski** is the generic form → `r=1` **Manhattan**, `r=2` **Euclidean**, `r=∞` **Chebyshev/supremum**; for binary vectors **SMC vs Jaccard** (does a 0-0 match count as similar?); for documents **cosine similarity** (uses actual counts, not just present/absent). The objective is called **SSE** in class = inertia = WCSS.
- **⭐ K-means is one of a family.** It only makes **spherical** clusters and uses the **mean** (outlier-sensitive) → **K-medoids/K-median** (median centre, robust to outliers), **DBSCAN** (density-based: eps + minPts, arbitrary shapes, handles noise, **no k needed**), **OPTICS** (DBSCAN for varying density). *Intra*-cluster similarity ↑, *inter*-cluster similarity ↓ ("**inter**state = between two states"). **Assessment 3 is regression, not clustering.**

> Full per-resource breakdown: [module09_notes.md](module-09-kmeans-clustering/module09_notes.md) · Week 9 class write-up: [module09_notes-class.md](module-09-kmeans-clustering/module09_notes-class.md)

### Introduction
- Rose, D. (2018, 29 March). Artificial intelligence foundations: Machine learning K-mean clustering [Video file]. Retrieved from https://www.linkedin.com/learning/artificial-intelligence-foundations-machine-learning/k-mean-clustering?resume=false&u=56744473

K-means clustering is an unsupervised algorithm (i.e., an algorithm that does not require labels), which is used to bring similar observations or data points into clusters. The number of clusters, K, is predefined. Common applications of K-means exist across many industries from marketing to medical technology. Some examples include applications that:

Identify viewers who like the same category of television shows (e.g., drama);
Divide a corpus of brand stories into topic areas (e.g., fashion, luxury goods or travel); and
Segment online shoppers by personality.
Watch the following video (available at: https://www.linkedin.com/learning/artificial-intelligence-foundations-machine-learning/k-mean-clustering?resume=false&u=56744473) to gain a basic understanding of K-means clustering.
 
### Resources

#### 1. Ten Interesting Use Cases for the K-Means Algorithm
- Raghupathi, K. (2018, 27 March). 10 interesting use cases for the K-means algorithm [Web log post]. Retrieved from https://dzone.com/articles/10-interesting-use-cases-for-the-k-means-algorithm

*Resource Overview:*

    This article commences with a brief recap of k-means by noting some interesting applications (e.g., Delivery Store Optimisation, Crime Locality Identification, Fantasy League Statistical Analysis, Insurance Fraud Detection, Rideshare Data Analysis and the Cyber-Profiling of Criminals). Ensure that you click on the links to the detailed papers (as available) to gain a better understanding of how the technique is applied.

> *Status: ✅ Read + Reviewed - see [module09_notes.md](module-09-kmeans-clustering/module09_notes.md#1-raghupathi-k-2018-10-interesting-use-cases-for-the-k-means-algorithm)*

#### 2. K-means Clustering Podcast 
- Reference: Data Skeptic. (2015, 20 February). K-means clustering [Audio podcast]. Retrieved from https://podcasts.apple.com/no/podcast/mini-k-means-clustering/id890348705?i=1000335938852

*Resource Overview:*

    This podcast explains K-means in a way that is easily understandable. It notes that supervised applications are more prevalent than unsupervised applications. The podcast also uses a very simple analogy free of any mathematics to help you understand the key concept of the centroid and its relationships with K-means clustering. Some key application areas are also discussed.

> *Status: 🔥 WIP - needs manual listen (no transcript available online; ~10-15 min "MINI" episode). See [module09_notes.md](module-09-kmeans-clustering/module09_notes.md#2-data-skeptic-2015-k-means-clustering-podcast-)*

#### 3. K-Means Clustering and Why It is Good For Business
- Reference: Hodgson, E. (2020, 25 February). K-means clustering and why it’s good for business [Web log post]. Retrieved from https://www.dotactiv.com/blog/why-k-means-clustering-is-good-for-business

*Resource Overview:*
    
    This easy-to-read article contextualises K-means for businesses. Three key questions are considered in the article: 1) What is k-means; 2) How can k-means (including the steps to run the algorithm) be used; and 3) What are some interesting use cases in business?

> *Status: ✅ Read + Reviewed - see [module09_notes.md](module-09-kmeans-clustering/module09_notes.md#3-hodgson-e--dotactiv-2020-k-means-clustering-and-why-its-good-for-business)*

#### 4. Clustering (Scikit Learn Documentation)
- Reference: Pedregosa, F.; Michel, V.; Grisel, O.; Blondel, M.; Prettenhofer, P.; Weiss, R.; Vanderplas, J.; Cournapeau, D.; Pedregosa, F.; Varoquaux, G.; et al. (2015). Scikit-learn: Machine Learning in Python. Journal of  Machine Learning Research 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/modules/clustering.html#homogeneity-completeness-and-v-measurecitation

*Resource Overview:*
    
    This resource examines different clustering algorithms. Focus on K-means to gain a better understanding of K-means advantages over other cluster algorithms. You can readily review other clustering algorithms on a visual basis and make comparisons with the other clustering methods that are illustrated. It is certainly worth perusing the different methods and reading more about K-means and the Mini Batch K-Means variation that helps reduce the computational time.

> *Status: ✅ Read + Reviewed - see [module09_notes.md](module-09-kmeans-clustering/module09_notes.md#4-pedregosa-et-al-scikit-learn--23-clustering)*

### Learning Activities

#### 1. Learning Activity 1: K-Means Clustering: The Pros and Cons of K-Means Clustering
- 365 Data Science, (2019, 24 January). K means clustering: Pros and cons of K means clustering [Video file]. Retrieved from https://www.youtube.com/watch?v=YIGtalP1mv0

To complete this learning activity, follow these steps:

1. Load the notebook code (ClusterAnalysis_countries.ipynb) into your notebook and data (Country clusters.csv).
2. Follow the video https://www.youtube.com/embed/YIGtalP1mv0 step by step.
3. Execute the code and perform the K-means method from scikit using the fit method.
4. Use the Within-Cluster-Sum-of-Squares (WCSS) to determine the number of clusters as shown within the code.
5. Review the pros and cons as discussed on the video and the fixes.
6. In the discussion forum, share how you established the number of clusters. Specifically, consider:
- Did everyone you are communicating with have the same number or a different number?
- If variation exists, discuss the reason/s for the difference others online.
- What differences did you note between supervised and unsupervised learning?

> *Status: 🕐 To-Do*

#### 2. Weather Data Clustering Using K-means
- Tewari, S. (2018, 11 January). Weather-data-clustering-using-K-means. Retrieved from: https://github.com/st186/Weather-Data-Clustering-Using-k-means

To complete this learning activity, follow these steps:

1. Load the notebook code (Weather_Data_Clustering_Using_K-Means.ipynb).
2. Note that this is a large data file of 1 million records comprising minute weather data (https://drive.google.com/open?id=0B8iiZ7pSaSFZb3ItQ1l4LWRMTjg).
3. Rather than downloading the large data file and ingesting it into your notebook, you can try modifying the code ‘pd.read_csv’ (name of dataset) and replace it with pd.read_csv (‘URL of the file found on google drive’ see Step 2 above).
4. Note that the code uses 12 clusters to represent the data.
5. In the discussion forum, discuss your ability to handle the large weather data set. Specifically, consider:
- Did you succeed in reading the data directly from the Google drive or did you have to download it?
- Was the K-means useful in looking at a bigger picture model of the weather?
- Is this algorithm useful for the bike-sharing ML project assessment?
Feel free to discuss key aspects of the questions noted in point 5 raised with others in the discussion forum.

> *Status: 🕐 To-Do*

---

## Module 10 - Learning Theory: PAC

### TLDR
**PAC (Probably Approximately Correct)** is the *theory of learning* — it explains **why** ML works and bounds **how much data** it needs (Valiant, 1984; Turing Award 2011).
- **Perfect learning is impossible** (label noise + finite sampling), so aim to be **approximately correct** (error ≤ **ε**) **probably** (confidence ≥ **1 − δ**). ε = accuracy, δ = confidence.
- **Learning = searching a hypothesis space H** for a good hypothesis `h` (Brownlee: `h` = one model, `H` = the set). "Model" in practice ≈ "hypothesis" in theory.
- **Occam's Razor / Occam's Bound (Daumé):** simpler hypotheses generalise — sample complexity ~ **log |H|**. This is the theoretical licence for regularisation + feature selection.
- **Sample complexity** (how many examples), **computational complexity** (how much compute), **mistake bound** — quantified by the **Haussler bound** (Sarkar): more data ⇒ lower error + higher confidence; richer H ⇒ needs more data.
- **Richer ≠ bigger H** (Sarkar): infinite straight lines still can't fit a quadratic — add the *right* term, don't just pile on parameters.
- **Infinite H → VC dimension** (max points a class can **shatter**). **Finite VC ⇔ PAC-learnable** (Worrell); SVM's **margin = complexity control** = a good PAC learner (Vapnik lineage).
- **PAC is theory-of-*learning*, not machine-learning** — Valiant's **"ecorithm"** applies it to biological evolution too (Pavlus). Module feeds SLOs `a)` + `d)` only; **no coding assessment**.

> Full per-resource breakdown: [module10_notes.md](module-10-learning-theory-pac/module10_notes.md) · Week 10 class write-up: [module10_notes-class.md](module-10-learning-theory-pac/module10_notes-class.md) · Revision sheet: [module10_one-pager.md](module-10-learning-theory-pac/module10_one-pager.md)

> **⭐ (Week 10 lecture, beyond the readings):** the **ε/4 four-strip error-region derivation** (why sample complexity carries a `4/ε` factor) and a **worked number** — 99% correctness + 95% confidence → **~1,753 samples**. Dr Kamran mapped PAC's ε/confidence directly onto the CRISP-DM **success criteria** you set in A3's business-understanding phase — state your target up front, then say whether you met it (SLO d). **Module 11 preview:** the **perceptron** + two off-curriculum unsupervised topics — **anomaly/outlier detection** and **association analysis (a priori algorithm)**.

### Introduction
This Module focuses on the mathematical and theoretical perspective of machine learning (ML). Specifically, it examines the Probably-Approximately-Correct (PAC) framework. The theoretical perspective of the PAC framework has applicability in understanding how humans acquire knowledge. The PAC framework is about the theory of ML (the theory of learning) and requires not only curiosity but some degree of attention to mathematical rigour when consulting the resources. The theoretical perspective of the PAC framework does not distinguish between ML and non-ML (humans). Most importantly, the theory of learning provides the justification and rationalisation for following the steps we take when solving a ML problem. An understanding the basics of the PAC framework helps inform the practice of ML.

### Resources

#### 1. The Probably-Approximately-Correct Framework and Machine Learning (Scikit-Learn)
- Pedregosa, F., Varoquaux, G., Gramfort, A. , Michel, V., Thirion, B. , Grisel, O. , Blondel, M. , Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J.,  Passos, A., Cournapeau, D.,  Brucher, M., Perrot, M. & Duchesnay, E (2015). Scikit-learn: Machine Learning in Python. Journal of  Machine Learning Research, 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/modules/svm.html

*Resource Overview:*
    
    Did you ever think about why we do the steps we do in ML? The PAC framework justifies the need to split our data into test and training data sets and provides the rationale for hyperparameter tuning—the learner is independent of the data distribution. This scikit-learn tutorial serves as a reminder of the different steps in ML that you will need to follow in your projects. This resource provides a context for exploring the PAC framework and will help you to understand its relationship to ML.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#1-pedregosa-et-al-2015-scikit-learn--14-support-vector-machines)*

#### 2. Learning Theory
- Daumé III, H. (2017, January). Chapter 12 Learning Theory.In A Course in Machine Learning (pp. 154-163). Retrieved from http://ciml.info/dl/v0_99/ciml-v0_99-ch12.pdf

*Resource Overview:*
    
    This book chapter will help you to understand the importance of theory in ML. The chapter explains the importance of PAC learning and its relationship to Occam’s Razor (i.e., simple solutions generalise). After reading this chapter, you will be more familiar with the terms of PAC and learning theory.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#2-daumé-iii-h-2017-learning-theory-ch12-a-course-in-machine-learning)*

#### 3. What is a Hypothesis in Machine Learning?
- Brownlee, J. (2019, 25 June). What is a hypothesis in machine learning? [Web log post]. Retrieved from https://machinelearningmastery.com/what-is-a-hypothesis-in-machine-learning/

*Resource Overview:*

    This resource helps lay the foundation for understanding the correct vocabulary when discussing the term hypothesis. The PAC framework uses this term frequently. Conversely, ML uses the term ‘model’. In ML we start with some data and build on it. When unseen data becomes available, we try to return something close to the original model. Thus, the model and hypothesis may appear to be interchangeable depending upon the area of focus. This resource serves as a reminder of the history of statistics and the importance of hypothesis testing and discusses how these led to the foundation of ML.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#3-brownlee-j-2019-what-is-a-hypothesis-in-machine-learning)*

#### 4. The Probably-Approximately-Correct Learning Theory for the Everyman
- Kelly, A. (2020, 21 April). PAC learning theory for the everyman: An uncomplicated introduction to the theory behind supervised machine learning. Retrieved from https://medium.com/swlh/pac-learning-theory-for-the-everyman-93c917c126f5

*Resource Overview:*

    This reading explains the PAC theory and puts it in the context of supervised learning. To gain a sound understanding of the PAC theory, mathematics cannot be ignored. The reading also introduces the mathematical portion of PAC learning theory in a formula and provides a link to a resource on the mathematical theory behind the PAC theory should you wish to explore it further.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#4-kelly-a-2020-pac-learning-theory-for-the-everyman)*

#### 5. The Hunt for the Algorithms that Drive Life on Earth
- Pavlus, J . (2016, 7 February). The hunt for the algorithms that drive life on earth. Wired. Retrieved from https://www.wired.com/2016/02/the-hunt-for-the-algorithms-that-drive-life-on-earth/

*Resource Overview:*

    This very-easy-to-read article will provide you with an understanding of the PAC theory and the motivations and longer-term objectives of Leslie Valiant, the computer scientist who invented the PAC theory. Ensure that you review the short video of Valiant embedded in this resource to understand the distinction between an ecorithm and an algorithm.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#5-pavlus-j-2016-the-hunt-for-the-algorithms-that-drive-life-on-earth)*

#### 6. Reaching for the Gut of Machine Learning: A Brief Introduction to Computational Learning Theory
- Sarkar, T. (2018, 15 July). Reaching for the gut of machine learning: A brief intro to CLT: Knowing the fundamentals of the computational learning theory can empower you immensely as a practitioner of machine learning [Web log post]. Retrieved from https://towardsdatascience.com/how-to-analyze-learning-short-tour-of-computational-learning-theory-9d93b15fc3e5

*Resource Overview:*

    This article examines the fundamental concepts of ML theory while providing an introduction to Computational Learning Theory (CLT) terms (e.g., data, target concept, hypothesis space and response variables). The CLT tries to answer fundamental questions about ML. The PAC theory is discussed in the context of learners and the concept of the Haussler bound. Consideration is also given to how it relates to ML practice in terms of training data, examples and hypothesis space.

> *Status: ✅ Read + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#6-sarkar-t-2018-reaching-for-the-gut-of-machine-learning-a-brief-intro-to-clt)*

#### 7. Computational Learning Theory (James Worrell)
- Worrell, J. (2019, 22 July). James Worrell: Computational learning theory I [Video file]. Retrieved from https://www.youtube.com/watch?v=DhmDnNoKoPg

*Resource Overview:*

    This video brings to life the mathematics and concepts of PAC learning and also provides some proof of PAC learnability. This video will first provide you with an understanding of some of the concepts before jumping into some complex and rigorous papers that you might wish to consult in future. You should watch the first 30 minutes of this video at least to gain an appreciation of the effects of PAC on computer science.

> *Status: ✅ Watched + Reviewed - see [module10_notes.md](module-10-learning-theory-pac/module10_notes.md#7-worrell-j-2019-computational-learning-theory-i)*

### Learning Activities

#### 1. Learning Activity 1: On-Device Machine Learning: An Algorithms and Learning Theory Perspective
- Dhar, S., Guo, J., Liu, J., Tripathi, S., Kurup, U. & Shah, M. (2020, 24 July). On-device machine learning: An algorithms and learning theory perspective. Retrieved from https://arxiv.org/pdf/1911.00623
- McMahan, B. & Ramage, D. (2017, 6 April). Federated learning: Collaborative machine learning without centralized training data [Web log post]. Retrieved from https://ai.googleblog.com/2017/04/federated-learning-collaborative.html

The importance of PAC theory in making computational advances in 2020 and beyond cannot be understated. PAC and other learning theories have majorly affected the progress of ML-powered devices. Currently, the practice of ML takes place on the cloud where access to computational resources is plentiful. However, what happens as the paradigm shifts to so-called edge computing or more specifically, ML being executed on a device rather than on the cloud? This shift to computing at the edge provides significant benefits not the least being that it removes the need to move large amounts of data around networks in near real time and opens up the vision of Federated Learning to becoming a reality. In Federated computing, the user data is no longer held in the cloud; rather, it is held at the edge device itself. Further, only the updates to the ML model are made available at the centre and the training data found on the device cannot be accessed.

To complete this learning activity, follow these steps:

1. Keep the two references (Dhar et al., 2020; McMahan & Ramage 2017) available for reference during this activity.
2. Read both these papers. Note that Dhar et al. (2020) discuss on-device ML while McMahan and Ramage (2017) introduce the term 'federated learning'.
3. Review Dhar et al. (2020) in greater detail. Pay particular attention to the role of learning theories and theoretical considerations (see Section 4.2).
4. Once you have an overall high-level understanding of the reading by Dhar et al. (2020), commence your discussions on the forum by answering these questions:
    - Why is PAC theory relevant to ML on edge devices?
    - What are the limitations of PAC theory that prevents edge devices becoming a reality?
    - Without undertaking any rigorous mathematics, can you indicate the theory propositions being discussed by the authors?
    - By linking the theory and practice of ML, can you think of any ways to help make on-device ML available?
    - What use cases do you have in mind for the devices?

> *Status: 🕐 To-Do*

---

## Module 11 - The Perceptron

### TLDR
**The perceptron** (Rosenblatt, 1958) is the **first trainable artificial neural network** (McCulloch-Pitts, 1943, modelled a neuron; Rosenblatt's is the one that *learns*) and the atom every deep net is built from.
- **Structure:** `inputs × weights + bias → weighted sum → activation → output`. The **bias** is the threshold the sum must clear (folded in as `w₀` with `x₀ = 1`).
- **Learning rule (online):** after each misclassified example, `w ← w + η·(target − pred)·x`, where **η** = learning rate. Weights update **per example**, not as a batch.
- **Perceptron Convergence Theorem:** if the data is **linearly separable**, the rule is **guaranteed** to find a separator; if not, there is **no convergence guarantee** - the updates can cycle, so you cap the epochs (Iris versicolor/virginica; the **XOR** problem).
- **The fix = depth + smooth activation:** the **XOR** limitation (Minsky-Papert, 1969) is solved by **stacking layers** and swapping the hard **step** function for a **differentiable** one (**sigmoid / tanh / ReLU / softmax**) so error can be **back-propagated** - the road to deep learning.
- **Family:** perceptron, **SVM** (max-margin; soft margin tolerates errors) and **logistic regression** (sigmoid → probability) all share the McCulloch-Pitts linear-neuron lineage, but *not* the same objective or guarantee. The perceptron's own result is **memorization, not generalization** - the perfect foil to **Module 10's PAC**.

> Full per-resource breakdown: [module11_notes.md](module-11-the-perceptron/module11_notes.md) · Week 10 lecturer preview: [module10_notes-class.md](module-10-learning-theory-pac/module10_notes-class.md)

> ⚠️ **Citation note:** the local PDFs for Resources **2** and **6** are **Bhardwaj (2020)** and **Lang (2024)**, not the **Sharma (2017)** articles cited below (same topics, different authors/years). Reconcile before quoting in an assessment.

### Introduction
This Module introduces the perceptron. The perceptron algorithm was invented by Frank Rosenblatt in 1958 and represents the first-generation artificial neural network (ANN). Rosenblatt’s inspiration for the perceptron and thus the ANN came from his desire to build a model of the brain from networks of neurons that process visual data and recognise objects. In essence, the perceptron is a computer program that learns from data. The theory or computational mechanism of the perceptron emanates from a hypothetical nervous system called a perceptron. The perceptron is an algorithm that makes a yes/no decision based on the sum of weighted inputs meeting a threshold value. Knowledge in the perceptron is captured in weights and thresholds, as no explicit rules exist.

### Resources

#### 1. History of the Perceptron and Visualisation
- Art of the Problem. (2019, 14 November). The beauty of deep neural networks (the pattern machine part 3) [Video file]. Retrieved from https://www.youtube.com/watch?v=r1U6fenGTrU

*Resource Overview:*

    The title of this video is misleading, as it only covers the first 80 years of neural network research and the history of the perceptron with some visualisations. The last few minutes of the video includes the commencement of a talk by Geoff Hinton, the key researcher of deep learning.

> *Status: ✅ Watched + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 2. Fundamentals of Perceptrons and Neural Networks
- Bhardwaj, A. (2020, 11 October). What is a perceptron? Basics of neural networks [Web log post]. Towards Data Science. *(Resource on file; the original module brief listed Sharma, S. (2017), "What the hell is perceptron?", https://towardsdatascience.com/what-the-hell-is-perceptron-626217814f53 - swap back if you prefer the brief's source.)*

*Resource Overview:*

    As a perceptron is a single-layer neural network, the importance of understanding the fundamentals is even more important outside this course. This is especially true as you move to deep learning and transition from shallow learning and single-layer neural networks. The activation determines if the neuron should be ‘fired’ (activated). This resource focuses on helping you understand how the perceptron works, commencing with the weighted sum of inputs.

> *Status: ✅ Read + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md) (local PDF: Bhardwaj 2020)*

#### 3. How to Build a Machine that Can Learn Anything (The Perceptron)
- Golden, R. (2014, 27 October). LM101-015: How to build a machine that can learn anything (The Perceptron) [Audio podcast]. Retrieved from https://www.learningmachines101.com/lm101-015-perceptron/

*Resource Overview:*

    This podcast takes a deep dive into the perceptron work of Rosenblatt and the theoretical contributions of the perceptron learning theorem. This theorem can solve any arbitrary logic problem but has fundamental limitations. The perceptron is closely related to the Support Vector Machines (SVM) and logistic regression models with computational or ML equivalence in special cases.

> *Status: ✅ Listened + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 4. The Perceptron
- Kennedy, M. Jaffe, B. & Malone, K. (2017, 10 March). The perceptron [Audio podcast]. Retrieved from https://podtail.com/en/podcast/data-skeptic/mini-the-perceptron/

*Resource Overview:*

    The above podcast (Golden, 2014) focuses on the context of the development of the perceptron. Conversely, this podcast conveys an overview of the perceptron algorithm in simple terms. Important aspects to recognise are the updating of weights after every example and the use of the step function as an activation function. Of course, the technique of using the perceptron algorithm is only suitable for linearly separable data.

> *Status: ✅ Listened + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 5. A Manual Walkthrough of the Perceptron Algorithm
- Ritvikmath. (2019, 30 January). Perceptron [Video file]. Retrieved from https://www.youtube.com/watch?v=4Gac5I64LM4

*Resource Overview:*
    
    This resource provides an overview of the perceptron algorithm using real values. This video includes a manual walkthrough, explains the development of the perceptron algorithm and includes the parameters and inputs, including the learning rate. This video also explains how the learning rate determines how fast the perceptron converges to the optimal classifier line.

> *Status: ✅ Watched + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 6. Which Activation Function Should I Use?
- Lang, N. (2024, 12 December). Activation functions in neural networks: How to choose the right one [Web log post]. Towards Data Science. *(Resource on file; the original module brief listed Sharma, S. (2017), "Activation functions in neural networks", https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6 - swap back if you prefer the brief's source.)*

*Resource Overview:*

    This resource provides a very practical explanation of the activation functions (otherwise known as transfer functions) of a perceptron or neural network. The activation determines if the neuron should be ‘fired’ (activated). This resource also discusses the difference between the different types of activations (e.g., Sigmoid, tanh, Softmax, ReLU and Leaky ReLU).

> *Status: ✅ Read + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md) (local PDF: Lang 2024)*

#### 7. Practical Application of Classification and Perceptron Algorithms
- Forsyth, J. (2014, 29 January). The noble perceptron [Web log post]. Retrieved from https://jaredforsyth.com/posts/the-noble-perceptron

*Resource Overview:*

    This resource outlines some applications of a perceptron for classification, including a heart attack classification system for a hospital, the graphs of a voting data set and the Iris data set. This resource will help you to understand the intuition behind the perceptron when dealing with a variety of different data.

> *Status: ✅ Read + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 8. The Perceptron: A Probabilistic Model for Information Storage and Organisation in The Brain (1958)
- Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. Retrieved from https://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=227D35CBBF71E5B71F159B7D5E57682E?doi=10.1.1.588.3775&rep=rep1&type=pdf

*Resource Overview:*

    This is the original paper from Rosenblatt showing the theory development of the perceptron for a hypothetical nervous system. You can see how the author positions the concepts between psychology, biophysics and the ability to predict learning curves from neurological variables.

> *Status: ✅ Read + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

#### 9. Training a Perceptron Model in Python
- Roach, J. (2016, 24 September). Training a perceptron model in Python [Web log post]. Retrieved from https://johnpatrickroach.com/2016/09/24/training-a-perceptron-model-in-python/

*Resource Overview:*

    This resource is a theory refresher that focuses on an actual Python code implementation. This reading provides the example of using the iris training set to make decisions with respect to a number of passes over the data set and the threshold for misclassification. The author refers to the old version of the Raschka book (i.e., an edition that is not the 3rd edition of the book).

> *Status: ✅ Read + Reviewed - see [module11_notes.md](module-11-the-perceptron/module11_notes.md)*

### Learning Activities

#### 1. Perceptron Settings
This activity will help you understand what is going on inside the perceptron.

To complete this learning activity, follow these steps:
1. Load perception_with_visualization.ipynb into your notebook.
2. Follow the code and markdown notes, paying attention to the input values, weights and bias, the net sum and the activation function.
3. Run the notebook.
4. To help consolidate your thinking, make a post to the discussion forum. In this post, address:
- What, in your view, is the best perceptron settings? Provide a justification for your answer.
- Discuss which settings had a greater effect on the classification if your settings differ from your peers.
- Note any other observations from your learnings from this notebook.

> *Status: 🔥 Draft ready - forum post + reproducible sweep in [module11_notes.md](module-11-the-perceptron/module11_notes.md#learning-activity-1---perceptron-settings-forum-draft); run `a1_perceptron_settings_sweep.py`. Still to post to the forum.* 

#### 2. Interactive Demonstrations of Perceptrons
This activity requires you to review and engage with some interactive perceptron demonstrations (see below) that are available online.

To complete this learning activity, follow these steps:

1. Review the proof of why the perceptron learns and generate data to see the visualisations in real time (https://owenshen24.github.io/perceptron/). Click ‘generate data’ and ‘fit perceptron’. You can alter the speed of the animation.
2. Tinker with the neural network; change the hyperparameters and see the capability of the multilayer neurons (https://playground.tensorflow.org/). The visualisations use orange for –ve and blue for ve. You can manipulate the learning rate, Epoch, activation function, regularisation rate and specify the problem type. Try flipping a few extreme values to determine the output.
3. Click on ‘Perceptron-OO’ for a new data set (https://www.khanacademy.org/computer-programming/perceptron-oo/4747053005537280).
4. Ensure that you try to touch upon the entire network architecture of the perceptron and where applicable, consider the number of layers, the different activation functions, the epoch, the learning rate, the momentum and the regularisation rate.
5. Once you have completed a run through of these interactive demonstrations, share your thoughts on hyperparameter tuning to the discussion forum. In doing so, answer the following question:
- Which variables had a direct impact on the algorithm?
- How did changing the epoch impact the perceptron?

> *Status: 🕐 To-Do* 

---

## Module 12 - Future of Machine Learning (ML): Enterprise Grade ML and Weak Supervision

### TLDR
The final module tackles the **two bottlenecks that stop ML reaching the real world**:
- **Production / the last mile.** A trained notebook model is **<20% of the job**; value only lands when it is
  **deployed, scaled, versioned, and governed** across an enterprise. Reality check: **55% of companies have never
  deployed** a model and most take **31-90 days** to ship one (**Algorithmia 2020**). Fixes = **MLOps + DevOps
  discipline**, the emerging **data-engineer** role, and Microsoft's 10-year vision - **train in the cloud, score
  inside the DBMS, govern everywhere** (**Agrawal et al. 2020**, coining **EGML**), on the insight that *"an ML model
  is software derived from data."*
- **Training data / labels.** Supervised ML starves without labels, and hand-labelling does not scale.
  **Weak supervision** (**Snorkel**) lets domain experts write noisy **labelling functions** (+1 / −1 / 0) that a
  **generative model** fuses into **probabilistic labels** to train a normal **discriminative model** - programmatically
  building large training sets (**Bell 2019**, **Ratner 2018**).
- **So what:** this is the **deployment + communication** end of CRISP-DM - the difference between a notebook and an
  enterprise system, and the theme of **Assessment 3**.

### Introduction
The future of machine learning (ML) depends heavily on projects moving from the notebook to production (the last stage of the CRISP-DM) across entire government departments or business enterprises and providing individuals other than data scientists and data analysts with access to the model.

This Module focuses on the current trends in enterprise ML, including the handoff from the data science team who build the models to the emerging role of the data engineers responsible for production deployment. If production is one major bottleneck in the use of ML models, the other major issue is the labelling of training data. One way to overcome the availability of suitable training data for models under development is to use humans to label data sets. However, manually generating labels is not only resource intensive but time consuming and subject to human error. To overcome such a human intensive activity weak supervision can be used to efficiently provide lower quality labels. This approach to using labels of varying quality could be used to help programmatically generate very large training data sets and thus become a major area of focus for the deployment of ML.

Two major challenges are holding back the widespread deployment and usage of ML model software applications within organisations and the government. The first relates to the ability to readily handover ML models generated within notebooks to IT department with an expectation of an immediate company-wide deployment. Unfortunately, considerable effort is required before the models can enter production. The second aspect relates to harnessing the weak supervision of lower quality label data sets to help generate labelled training data. Both these areas are examined in this final module.

### Resources

#### 1. Building Machine Learning Projects in the Enterprise—Episode 69
- Macey, T. (Interviewer). (2019, 11 February). Episode #69: Building machine learning projects in the enterprise [Audio podcast]. Retrieved from https://www.dataengineeringpodcast.com/prolego-ml-consulting-episode-69/

*Resource Overview:*
    
    This podcast focuses entirely on putting ML models into production. The role of the data engineer is discussed at length as is the necessity of having SQL skills. Some suggestions are made as to the positioning of the data engineering role and how this role is required to put the plumbing into place before the production deployment of the ML model.

    If you wish to work as a data engineer, you should listen to the entire podcast. If not, focus on the first 20 minutes of the podcast.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 2. Machine Learning in the Enterprise: Five Hard Truths
- Casey, K. (2020, 30 July). Machine learning in the enterprise: 5 hard truths. Retrieved from https://enterprisersproject.com/article/2020/7/machine-learning-5-lessons-learned

*Resource Overview:*

    This short article covers some lessons that have been learned in trying to put ML models into production. The lessons relate to talent, training data, managing business expectations and the automation of the production pipeline to avoid software development issues.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 3. Machine Learning in the Enterprise: Where Will the Next Trillion Dollars of Value Accrue?
- Xu, L. (2020, 15 July). Machine Learning in the enterprise: Where will the next trillion dollars of value accrue? Retrieved from https://www.forbes.com/sites/louisaxu/2020/07/15/machine-learning-in-the-enterprise-where-will-the-next-trillion-dollars-of-value-accrue/#4d75152be1aa

*Resource Overview:*

    This article looks at the companies and tools that help to overcome the issues holding back ML from having a massive impact in industries. Not only is ML being embedded across industries, but vertically integrated ML applications are impacting healthcare, industry, security and agriculture in ways not thought possible.

> *Status: 🔥 Partial (paywalled - intro only) - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 4. State of Enterprise Machine Learning in 2020: Seven Key Findings
- Bayern, M. (2019, 12 December). State of enterprise machine learning in 2020: 7 key findings. Retrieved from https://www.techrepublic.com/article/state-of-enterprise-machine-learning-in-2020-7-key-findings/

*Resource Overview:*
    
    This article provides another take on the obstacles facing companies seeking to implement ML across their enterprises. Particularly noteworthy is the length of time it takes to deploy a model. Twenty per cent of the companies consulted for the study take over 90 days to deploy a model. Of the companies, 38 per cent cited cost cutting as a major reason for ML deployment and nearly half (43 per cent) viewed scaling as a key challenge that requires individuals with a different skill set to model builders.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 5. A 10-year Prediction for Enterprise-Grade Machine Learning
- Agrawal, A. Chatterjee, R., Curino, C., Floratou, A. Gowdal, N., Interlandi, M. . . . Zhu, Y. (2019, 12 December). Cloudy with high chance of DBMS: A 10-year prediction for enterprise-grade ML. Retrieved from http://cidrdb.org/cidr2020/papers/p8-agrawal-cidr20.pdf

*Resource Overview:*

    This interesting vision paper from Microsoft experts foreshadows a transition from ML consumer applications to enterprise applications. This paper refers to an emerging class of applications (apps) referred to as Enterprise Grade Machine Learning (EGML) apps. The boldest prediction by the paper relates to models migrating into database systems. This seems to be a natural move given that databases have widespread acceptance as key components of enterprise applications. Further, the authors ‘predict that in the next 10 years, hundreds of thousands of small teams will build millions of ML-infused applications—most just moderately remunerative, but with huge collective value’.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 6. Weak Supervision: A New Paradigm for Unreliable Data
- Bell, E. (2019, 19 July). Eddie Bell: Weak supervision: A new paradigm for unreliable data [Video file]. Retrieved from https://www.youtube.com/watch?v=KRcgteDTm3k

*Resource Overview:*

    This video explains the importance of labelled training data sets for real-world tasks. To address the bottleneck of labelled training data, a set of approaches helps programmatically label the data. The context of the presentation is a fraud application ideal for the programmatic approach. You are encouraged to watch the video in its entirety. The key areas of coverage are the importance of labels and making use of unreliable labels and opportunities to engineer the labels themselves. The greatest gains in ML are expected to come from new labels and approaches to labelling (e.g., combining high-quality and low-quality labels).

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 7. Snorkel: Extracting Value from Dark Data with Alex Ratner—Episode 15
- Macey, T. (Interviewer). (2018, 22 January). Episode #15: Snorkel: Extracting value from dark data [Audio podcast]. Retrieved from https://www.dataengineeringpodcast.com/snorkel-with-alex-ratner-episode-15/

*Resource Overview:*

    Snorkel is a system for programmatically building and managing training datasets without manual labelling. In Snorkel, users can develop large training data sets in hours or days rather than hand-labelling them over weeks or months. This podcast looks at the Snorkel Python library to generate training sets for ML models. Notably, dark data relates to unstructured data. An opportunity exists to label this untapped resource for supervised ML.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

#### 8. The Cold-Start Problem with Stanford Snorkel
- Powell, A. (2020, 8 February). The cold-start problem with Stanford Snorkel. Retrieved from https://medium.com/analytics-vidhya/the-cold-start-problem-with-stanford-snorkel-6fc5b55ec216

*Resource Overview:*

    This resource provides an introduction to Snorkel and weakly supervised ML. It answers the question of what to do when you do not have training data. The author shares his experience of using the library to address real problems. The takeaways are not convincing, but the alternative is to have many humans label the data by hand. Using human labour to label data is not really tenable in the generation of very large training data sets.

> *Status: ✅ Read + Reviewed - see [module12_notes.md](module-12-future-of-ml/module12_notes.md)* 

### Learning Activities

#### 1. Microsoft Azure SQL Edge
- Microsoft. (n.d.). Azure SQL Edge. Retrieved from https://azure.microsoft.com/en-au/services/sql-edge/#product-overview
- ODSC. (2020, 4 April). What is federated learning? [Web log post]. Retrieved from https://medium.com/@ODSC/what-is-federated-learning-99c7fc9bc4f5

The paper entitled Cloudy with High Chance of DBMS: A 10-year Prediction for Enterprise-Grade ML (Agarwal et al., 2019; see the essential resources) discusses the long-term cross over between ML and database systems. The future has already arrived in the form of the Microsoft Azure SQL Edge (Preview) database (https://azure.microsoft.com/en-au/services/sql-edge/). This database is optimised for Internet of Things workloads on edge devices.

To complete this learning activity, follow these steps:

1. Watch a demo on real-time analytics over time-series data in which data from a simulation of robot sensors are inserted into a SQL database and ML algorithms are run over the data. (https://azure.microsoft.com/en-us/asset/video-player/sql-database-edge-streaming-machine-learning).
2. Review the frequently asked questions about Azure SQL Edge (https://azure.microsoft.com/en-us/services/sql-edge/#faqs) to understand its commercial availability and details.
3. Consider the deployment scenario (https://docs.microsoft.com/en-au/azure/azure-sql-edge/overview).
4. Explore ML in Azure SQL Edge (Preview) and obtain models in the Open Neural Network Exchange (ONNX) format.
5. Familiarise yourself with the ONNX open format that was built to represent machine learning models (https://onnx.ai/).
6. At the conclusion of these learning activities, share your views on the usefulness (or not) of ONNX, (v1.7) in the discussion forum and describe in detail your own deployment scenarios for the SQL Edge database. If you do not have access to the SQL Edge product, how would you try to achieve the same capability? Could SQL Edge be used to achieve Federated Learning? (OSDC, 2020).

> *Status: 🕐 To-Do* 

#### 2. Snorkel Tutorial
As mentioned in the essential resources, Snorkel is a system for programmatically building and managing training datasets without manual labelling. In Snorkel, users can develop large training datasets in hours or days rather than hand-labelling them over weeks or months.

Review the basics of writing labelling functions (https://www.snorkel.org/get-started/).

Complete the Snorkel Introduction Tutorial: Data Labelling (https://www.snorkel.org/use-cases/01-spam-tutorial).

Once complete, share details of your experience to the discussion forum. In your post, answer the following questions:
- Can you follow and comment on the approach suggested in the use of Snorkel to develop large training data sets?
- Do you have any training data sets in mind that you feel will be suitable for training?
- Can you identify any other approaches that might be suitable?

> *Status: 🕐 To-Do* 

#### 3. The Human Factor in Machine Learning Adoption
- Bell, T. (2018, 28 March). The human side of implementing AI. CIO Australia. Retrieved from https://www.cio.com/article/3263791/the-human-side-of-implementing-ai.html

Imagine that the organisation that you have joined is launching ML and its supporting applications across the entire enterprise. How can you go about ensuring the acceptance of ML in your organisation? What role will you adopt? Do you see yourself as an evangelist in the area who helps others benefit from the forthcoming implementations of ML?

Bell (2018) is a short resource that you might wish to consult to gain some ideas. Upon completion of this activity, share your thoughts with others to the online discussion forum on how best you could help the enterprise to overcome any resistance to the use of ML to create a highly productive environment.

> *Status: 🕐 To-Do* 

---

```bash
--- PLACEHOLDER:
## Module X - ...
### TLDR
### Introduction
### Resources
### Learning Activities

--- STATUS
# *Status: 🕐 To-Do*                <--- starting point
# *Status: ✅ Watched + Reviewed*   <--- for video resources
# *Status: ✅ Read + Reviewed*      <--- for articles, papers, chapters
# *Status: ✅ Done*                 <--- for activities
```
