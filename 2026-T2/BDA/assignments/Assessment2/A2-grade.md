Jul 27 at 21:21
This is a highly developed and technically careful submission. Your notebook demonstrates a strong understanding of the complete modelling workflow, including deterministic stratified splitting, training-only preprocessing, evidence-based feature selection and evaluation on an untouched test set. The handling of the blank TotalCharges records is particularly thoughtful, as you use the tenure-zero context rather than automatically applying median imputation. Your validation ablation also provides a convincing justification for removing TotalCharges.


The decision tree is clearly represented and translated into useful customer rules. Your interpretation goes beyond headline accuracy by examining churn recall, precision, F1, AUC, overfitting and the majority-class baseline. The missing-Contract experiment is another major strength, especially your recognition that almost unchanged accuracy concealed a substantial reduction in churn F1. The implemented comparisons involving threshold tuning, class weighting and Random Forest further strengthen the analysis.


The main issue is concision. The report substantially exceeds the specified word limit and includes an extensive glossary and several analyses beyond the task requirements. Future work should preserve this analytical quality while selecting only the evidence needed to answer the brief. Also avoid absolute recommendations such as spending no retention budget on a segment; model outputs represent risk rather than certainty.

- Chen Zhan

Knowledge and understanding of exploratory data analysis
15 to >12.6 pts
High Distinction(Exceptional)
Demonstrates exceptional knowledge and understanding of the exploratory data analysis. Demonstrates exemplary skills in: • Identifies both external and internal data sources. • Identifies structured, semi-structured and unstructured data sources. • Provides an exceptional quality description of the characteristics, formats and structures of the sources.
14 / 15 pts

Analytical design for data pre-processing and feature selection
15 to >12.6 pts
High Distinction(Exceptional)
Demonstrates exceptional knowledge and understanding of data pre-processing and feature selection. Completed all of the following tasks with accuracy and completeness to an exceptionally high quality: • Handling data anomalies; • Conducting the redundancy and correlation analysis; • Selecting the feature for model building. • Correctly interpreted all 3 of the above tasks. and • Relevant analytical insights were presented as part of the interpretation.
14 / 15 pts

Predictive model building
20 to >16.8 pts High Distinction(Exceptional)
Demonstrates exceptional knowledge and understanding of predictive model building. Completed all of the following tasks with accuracy and completeness to an exceptionally high quality: • Appropriately used the data for training, validation and testing; • Built a ‘decision-tree’ model using Spark’s MLlib library; • Graphically represented the decision-tree model; and • Correctly interpreted the decision-tree model. • Discovered unique observations through the interpretation of the model.
19 / 20 pts

Clarity and presentation of the notebook
8.4 to >7.4 pts
Distinction(Advanced)
• Well organised • Code is very well documented. • Charts and graphs are neat and of high quality. • Narrative texts are highly cohesive and easy to follow.
8 / 10 pts

Knowledge and understanding of missing value handling strategy
10 to >8.4 pts
High Distinction(Exceptional)
Demonstrates exceptional knowledge and understanding of a missing value handling strategy. • Correctly identifies the most important attribute from the decision tree. • The formulated strategies are accurate and complete. • The overall organisation and presentation of the report is exemplary.
9 / 10 pts

Interpretation of data analysis
30 to >25.2 pts
High Distinction(Exceptional)
The outcomes and discussions were well focused and included all of the following points: • The outcomes were measured and the related discussions were exceptional; • The analysis produced thought-provoking insights; and • Possible performance improvements were fully and correctly evaluated.
27 / 30 pts