## Question 1 - Parameter vs hyperparameter
parameter = actual weights, coefficients or split values the model calculates once looks at the dataset

hyperparameter =  structural settings of the machine like like learning rate, how big tree can grow, how many to build, size of steps, etc 

parameters are a knob/setting chosen before calling .fit() and the other is internal config the model computes during .fit() by examining the training data.

## Question 2 - Crisp DM and leakage
(had to cheat on the list)
1. Business understanding
2. Data understanding
3. Data preparation
4. Modeling
5. Evaluation
6. Deployment

I remember that these were video game sales we studied, but np idea on the case, but what I understand about catching leakage on the data is prevented on data preparation, with cross validation making sure to keep a held-out test set to be used in testing. The leakage happens when we feed some of the data that was supposed to be used only on testing, on training, allowing model to have a sneek peek on the information and gain advantage over that.
R squared of 0.99 means almost 100% accuracy of the model, which we humans know it is very unlikely to happen in the real word. All data has noise, making near-perfect correlation extremely rare. The model is very likely overfitting or with leakage.

## Question 3 - Regression metrics
mean average error of 0.40 means the model gets off by 0.40 on its guesses, on average. Example score is 8.0, model is getting somewhere between 7.6-8.4 range
rmse is root mean squared error squares the errors before averaging and taking the square root, which penalizes heavily outliers and large mistakes
the fact that rmse is bigger than mae (almost double) tells us that models makes some mistakes due to outliers
r square of 0.55 means that 55% of the variation in target wine variable is explained by the input features and the remaining comes from factors not included on the model. Explaining more than half (55%) of the variance is generally considered a moderate-to-good result in many real-world datasets, especially for subjective measures like human taste or wine quality

## Question 4 - Trees and ensembles
Gini impurity measures the chance of wrong labelling for a random item in a group

Bagging and boosting are ensemble learning techniques that combine multiple decision trees to create a single, more accurate machine learning model. 
- Bagging focuses on reducing variance (overfitting) by training independent trees at the same time.
- Boosting focuses on reducing bias (underfitting) by training dependent trees one after the other.

| | Bagging (Random Forest) | Boosting (XGBoost) |
|---|---|---|
| Trees trained... | in parallel | in sequence |
| Cures... | overfittigng (high var) | underfitting (high bias) |
| Combine predictions by... | majority voting/averaging | weighted sum of all trees |

## Question 5 - Bayes' rules

## Question 6 -  SVM
C parameter controls the penalty for making classification mistakes.
- low `C` allows a wider margin with more misclassifications (regularization)
- high `C` forces a narrow margin to minimize errors, risking overfitting

## Question 7 - Explainable ML quadrant

## Question 8 - LR

## Queston 9 - K-means

## Question 10 - PAC learning theory

## Question 11 - Perceptron

## Question 12 - Enterprise ML grande and snorkel
