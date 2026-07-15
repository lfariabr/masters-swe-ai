Machine Learning Guide « »
MLG 007 Logistic Regression

The logistic regression algorithm is used for classification tasks in supervised machine learning, distinguishing items by class (such as "expensive" or "not expensive") rather than predicting continuous numerical values. Logistic regression applies a sigmoid or logistic function to a linear regression model to generate probabilities, which are then used to assign class labels through a process involving hypothesis prediction, error evaluation with a log likelihood function, and parameter optimization using gradient descent.

Links
Notes and resources at ocdevel.com/mlg/7
Try a walking desk - stay healthy & sharp while you learn & code
Classification versus Regression in Supervised Learning
Supervised learning consists of two main tasks: regression and classification.
Regression algorithms predict continuous values, while classification algorithms assign classes or categories to data points.
The Role and Nature of Logistic Regression
Logistic regression is a classification algorithm, despite its historically confusing name.
The algorithm determines the probability that an input belongs to a specific class, using outputs between zero and one.
How Logistic Regression Works
The process starts by passing inputs through a linear regression function, then applying a logistic (sigmoid) function to produce a probability.
For binary classification, results above 0.5 usually indicate a positive class (for example, "expensive"), and results below 0.5 indicate a negative class ("not expensive").
Multiclass problems assign probabilities to each class, selecting the class with the highest probability using the arg max function.
Example Application: Housing Spreadsheet
An example uses a spreadsheet of houses with features like square footage and number of bedrooms, labeling each as "expensive" (1) or "not expensive" (0).
Logistic regression uses the spreadsheet data to learn the pattern that separates expensive houses from less expensive ones.
Steps in Logistic Regression
The algorithm follows three steps: predict (infer a class), evaluate error (calculate how inaccurate the guesses were), and train (refine the underlying parameters).
Predictions are compared to actual data, and the difference (error) is calculated via a log likelihood function, which accounts for how confident the prediction was compared to the true value.
Model parameters (theta values) are updated using gradient descent, which iteratively reduces the error by adjusting these values based on the derivative of the error function.
The Mathematical Foundation
The hypothesis function is the sigmoid or logistic function, with the formula: 1 / (1 + e^(-theta^T x)), where theta represents the parameters and x the input features.
The error function (cost function) for logistic regression uses log likelihood, aggregating errors over all data points to guide model learning.
Practical Considerations
Logistic regression finds a "decision boundary" on the graph (S-curve) that best separates classes such as "expensive" versus "not expensive."
When the architecture requires a proper probability distribution (sum of probabilities equals one), a softmax function is applied to the outputs, but softmax is not covered in this episode.
Composability in Machine Learning
Machine learning architectures are highly compositional, with functions nested within other functions - logistic regression itself is a function of linear regression.
This composability underpins more complex systems like neural networks, where each "neuron" can be seen as a logistic regression unit powered by linear regression.
Building Toward Advanced Topics
Understanding logistic and linear regression forms the foundation for approaching advanced areas of machine learning such as deep learning and neural networks.
The concepts of prediction, error measurement, and iterative training recur in more sophisticated models.
Resource Recommendations
The episode recommends the Andrew Ng Coursera course for deeper study into these concepts and details, especially for further exploration of multivariate regression and error functions.