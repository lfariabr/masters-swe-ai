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

> *Status: 🕐 To-Do — source notes ready in [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#5-townes-2017-why-skilled-in-machine-learning-should-be-the-new-proficient-in-excel-on-your-resume)*

#### 2. Machine Learning Applications
- Hill, K. (2012, 16 February). How Target figured out a teen girl was pregnant before her father did. Forbes. Retrieved from https://www.forbes.com/sites/kashmirhill/2012/02/16/how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did/#7dc209fb6668
- Jiang, X., Coffee, Bari, A., Wang, J., Jiang, X., Huang, J., . . . Huang, Y. (2020). Towards an artificial intelligence framework for data-driven prediction of coronavirus clinical severity. Computers, Materials and Continua, 63(1), 537–551.Retrieved from https://www.techscience.com/cmc/v63n1/38464/pdf

An understanding of the application of ML will help you to prepare for the opportunities and gain a better understanding of the areas in which jobs are emerging. In the short term, predictive systems are attracting a lot of interest. For example, ‘How Target Figured Out A Teen Girl Was Pregnant Before Her Father Did‘ (Hill 2012).

As the article entitled ‘Artificial Intelligence Framework for Data-Driven Prediction of Coronavirus Clinical Severity ‘ (Jiang et al., 2020) shows, the systems built on ML are diverse, high profile and impactful. Review Sections 4–7 of this article to understand the predictive capability of this framework and recognise that the predictors are not the same as those publicly reported.

Plenty of other examples can be found by searching the AI Index arXiv Monitor (https://arxiv.aiindex.org/search) with the term ‘machine learning’. Spend some time to seek out the new ML predictive systems. Note that this material has not been peer-reviewed by arXiv.

Post 2–3 sentences to the discussion forum explaining what you have learned in this Module and how you can see yourself applying it; and Reply to two of your peers’ posts.

> *Status: 🕐 To-Do — source notes ready in [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#6-hill-2012-how-target-figured-out-a-teen-girl-was-pregnant-before-her-father-did) and [module01_notes.md](module-01-career-algos-concepts/module01_notes.md#7-jiang-et-al-2020-towards-an-artificial-intelligence-framework-for-data-driven-prediction-of-coronavirus-clinical-severity)*

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
