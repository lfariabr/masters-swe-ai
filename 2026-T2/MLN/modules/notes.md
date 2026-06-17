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

> *Status: 🕐 To-Do* 

#### 2. Decision Trees and Boosting, XGBoost (eXtreme Gradient Boosting)
- Reference: Two Minute Papers. (2016, 25 March). Decision trees and boosting, XGBoost | Two Minute Papers #55 [Video file]. Retrieved from https://www.youtube.com/watch?v=0Xc9LIb_HTw

*Resource Overview:*

    This short video explains boosting, a very popular technique used to combine a lot of weak learner DTs into a strong learner. Individually, a weak learner is quiet inaccurate and makes predictions that are only slightly better than random guessing. However, if you take a whole bunch of weak learner DTs, you can produce a strong learning tree or algorithm.

> *Status: 🕐 To-Do* 

#### 3. XGBoost Algorithm
- Morde, V. (2019, 8 April). XGBoost algorithm: Long may she reign! Retrieved from https://towardsdatascience.com/https-medium-com-vishalmorde-xgboost-algorithm-long-she-may-rein-edd9f99be63d

*Resource Overview:*

    XGBoost or extreme gradient boosting is a DT-based ensemble ML algorithm that performs very well. This article discusses the evolution of the algorithm from DTs and the potential future of the XGBoost algorithm. The algorithm has a large open community, which contributes to XGBoost projects (https://github.com/dmlc/xgboost/). To better understand the next generation of tree algorithms, including XGBoost, an analogy is used of an interview process and hiring criteria. The approaches taken to enable XGBoost to achieve a superior performance, including algorithm enhancements, provide a strong justification for its usage. This is proven by comparing Scikit-learn’s ‘make classification’ benchmarking to other algorithms.

> *Status: 🕐 To-Do* 

#### 4. Plotting XGBoost Decision Tree in Python
- Brownlee, J. (2019, 11 December). How to visualize gradient boosting decision trees with XGBoost in Python. Retrieved from https://machinelearningmastery.com/visualize-gradient-boosting-decision-trees-xgboost-python/

*Resource Overview:*

    This hands-on tutorial shows how you can plot individual DTs within a trained gradient boosting model using XGBoost in Python. A full code listing is provided to create a plot of the first DT.

> *Status: 🕐 To-Do* 

#### 5. Scikit-learn Decision Tree Documentation
- Reference: Pedregosa, F.; Michel, V.; Grisel, O.; Blondel, M.; Prettenhofer, P.; Weiss, R.; Vanderplas, J.; Cournapeau, D.; Pedregosa, F.; Varoquaux, G.; et al. (2015). Scikit-learn: Machine Learning in Python. J. Mach. Learn. Res. 12, 2825–2830. Retrieved from https://scikit-learn.org/stable/index.html

*Resource Overview:*

    Scikit-learn documentation is highly readable and well presented. The documentation below will allow you to implement DT algorithms with little prior knowledge. The following resources make for useful reading:
    - Understanding the decision tree structure (https://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html);
    - Decision Tree Classifier (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html); and
    - Decision Tree Regressor (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html).

> *Status: 🕐 To-Do* 

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
