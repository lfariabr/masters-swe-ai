Dataset preprocessing
When we first dive into data science, a common mistake is expecting all the data to be very polished and with good characteristics from the very beginning. Alas, that is not the case for a very considerable percentage of cases, for many reasons such as null data, sensor errors that cause outliers and NAN, faulty registers, instrument-induced bias, and all kinds of defects that lead to poor model fitting and that must be eradicated.

The two key processes in this stage are data normalization and feature scaling. This process consists of applying simple transformations called affine that map the current unbalanced data into a more manageable shape, maintaining its integrity but providing better stochastic properties and improving the future applied model. The common goal of the standardization techniques is to bring the data distribution closer to a normal distribution, with the following techniques:

Normalization and feature scaling
One very important step in dataset preprocessing is normalization and feature scaling. Data normalization allows our optimization techniques, specially the iterative ones, to converge better, and makes the data more manageable.

Normalization or standardization
This technique aims to give the dataset the properties of a normal distribution, that is, a mean of 0 and a standard deviation of 1.

The way to obtain these properties is by calculating the so-called z scores, based on the dataset samples, with the following formula:


Let's visualize and practice this new concept with the help of scikit-learn, reading a file from the MPG dataset, which contains city-cycle fuel consumption in miles per gallon, based on the following features: mpg, cylinders, displacement,  horsepower, weight, acceleration, model year, origin, and car name.

```python
from sklearn import preprocessing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("data/mpg.csv")
plt.figure(figsize=(10,8))
print df.columns
partialcolumns = df[['acceleration', 'mpg']]
std_scale = preprocessing.StandardScaler().fit(partialcolumns)
df_std = std_scale.transform(partialcolumns)
plt.scatter(partialcolumns['acceleration'], partialcolumns['mpg'], color="grey", marker='^')
plt.scatter(df_std[:,0], df_std[:,1])
```

The following picture allows us to compare the non normalized and normalized data representations:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/ef918b28-6afa-4dee-95c6-81efa40106f2.png
Depiction of the original dataset, and its normalized counterpart.
It's very important to have an account of the denormalizing of the resulting data at the time of evaluation so that you do not lose the representative of the data, especially if the model is applied to regression, when the regressed data won't be useful if not scaled.

Model definition
If we wanted to summarize the machine learning process using just one word, it would certainly be models. This is because what we build with machine learning are abstractions or models representing and simplifying reality, allowing us to solve real-life problems based on a model that we have trained on.

The task of choosing which model to use is becoming increasingly difficult, given the increasing number of models appearing almost every day, but you can make general approximations by grouping methods by the type of task you want to perform and also the type of input data, so that the problem is simplified to a smaller set of options.

Asking ourselves the right questions
At the risk of generalizing too much, let's try to summarize a sample decision problem for a model:

Are we trying to characterize data by simply grouping information based on its characteristics, without any or a few previous hints? This is the domain of clustering techniques.
The first and most basic question: are we trying to predict the instant outcome of a variable, or to tag or classify data into groups? If the former, we are tackling a regression problem. If the latter, this is the realm of classification problems.
Having the former questions resolved, and opting for any of the options of point 2, we should ask ourselves: is the data sequential, or rather, should we take the sequence in account? Recurrent neural networks should be one of the first options.
Continuing with non-clustering techniques: is the data or pattern to discover spatially located? Convolutional neural networks are a common starting point for this kind of problem.
In the most common cases (data without a particular arrangement), if the function can be represented by a single univariate or multivariate function, we can apply linear, polynomial, or logistic regression, and if we want to upgrade the model, a multilayer neural network will provide support for more complex non-linear solutions.
How many dimensions and variables are we working on? Do we just want to extract the most useful features (and thus data dimensions), excluding the less interesting ones? This is the realm of dimensionality reduction techniques.
Do we want to learn a set of strategies with a finite set of steps aiming to reach a goal? This belongs to the field of reinforcement learning. If none of these classical methods are fit for our research, a very high number of niche techniques appear and should be subject to additional analysis.
In the following chapters, you will find additional information about how to base your decision on stronger criteria, and finally apply a model to your data. Also, if you see your answers don't relate well with the simple criteria explained in this section, you can check Chapter 8, Recent Models and Developments, for more advanced models.

Loss function definition
This machine learning process step is also very important because it provides a distinctive measure of the quality of your model, and if wrongly chosen, it could either ruin the accuracy of the model or its efficiency in the speed of convergence.

Expressed in a simple way, the loss function is a function that measures the distance from the model's estimated value to the real expected value.

An important fact that we have to take into account is that the objective of almost all of the models is to minimize the error function, and for this, we need it to be differentiable, and the derivative of the error function should be as simple as possible.

Another fact is that when the model gets increasingly complex, the derivative of the error will also get more complex, so we will need to approximate solutions for the derivatives with iterative methods, one of them being the well-known gradient descent.

Model fitting and evaluation
In this part of the machine learning process, we have the model and data ready, and we proceed to train and validate our model.

Dataset partitioning
At the time of training the models, we usually partition all the provided data into three sets: the training set, which will actually be used to adjust the parameters of the models; the validation set, which will be used to compare alternative models applied to that data (it can be ignored if we have just one model and architecture in mind); and the test set, which will be used to measure the accuracy of the chosen model. The proportions of these partitions are normally 70/20/10.

Common training terms –  iteration, batch, and epoch
When training the model, there are some common terms that indicate the different parts of the iterative optimization:

An iteration defines one instance of calculating the error gradient and adjusting the model parameters. When the data is fed into groups of samples, each one of these groups is called a batch.
Batches can include the whole dataset (traditional batching), or include just a tiny subset until the whole dataset is fed forward, called mini-batching. The number of samples per batch is called the batch size.
Each pass of the whole dataset is called an epoch.

Types of training – online and batch processing
The training process provides many ways of iterating over the datasets and adjusting the parameters of the models according to the input data and error minimization results.

Of course, the dataset can and will be evaluated many times and in a variety of ways during the training phase.

Parameter initialization
In order to assure a good fitting start, the model weights have to be initialized to the most effective values. Neural networks, which normally have a tanh activation function, are mainly sensitive to the range [-1,1], or [0,1]; for this reason, it's important to have the data normalized, and the parameters should also be within that range.

The model parameters should have useful initial values for the model to converge. One important decision at the start of training is the initialization values for the model parameters (commonly called weights). A canonical initial rule is not initializing variables at 0 because it prevents the models from optimizing, as they do not have a suitable function slope multiplier to adjust. A common sensible standard is to use a normal random distribution for all the values.

Using NumPy, you would normally initialize a coefficient vector with the following code:

```python
mu, sigma = 0, 1 
dist = np.random.normal(mu, sigma, 1000)
>>> dist = np.random.normal(mu, sigma, 10)
>>> print dist
[ 0.32416595 1.48067723 0.23039378 -0.59140674 1.65827372 -0.8241832
 0.86016434 -0.05996878 2.2855467 -0.19759244]
 ```

One particular source of problems at this stage is setting all of the model's parameters to zero. As many optimization techniques normally multiply the weights by a determinate coefficient to the approximate minimum, multiplying by zero will prevent any change in the model, excepting the bias terms.


Model implementation and results interpretation
No model is practical if it can't be used outside the training and test sets. This is when the model is deployed into production.

In this stage, we normally load all the model's operation and trained weights, wait for new unknown data, and when it arrives, we feed it through all the chained functions of the model, informing the outcomes of the output layer or operation via a web service, printing to standard output, and so on.

Then, we will have a final task - to interpret the results of the model in the real world to constantly check whether it works in the current conditions. In the case of generative models, the suitability of the predictions is easier to understand because the goal is normally the representation of a previously known entity.

Regression metrics
For regression metrics, a number of indicators are calculated to give a succinct idea of the fitness of the regressed model. Here is a list of the main metrics.

Mean absolute error
The mean_absolute_error function computes mean absolute error, a risk metric corresponding to the expected value of the absolute error loss, or l1-norm loss.
If ŷi is the predicted value of the ith sample, and yi is the corresponding true value, then the mean absolute error (MAE) estimated over n samples is defined as follows:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/7ef1e654-fc01-4e42-b508-45d6ee20a0e2.png

Median absolute error
The median absolute error is particularly interesting because it is robust to outliers. The loss is calculated by taking the median of all absolute differences between the target and the prediction.
If ŷ is the predicted value of the ith sample and yi is the corresponding true value, then the median absolute error estimated over n samples is defined as follows:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/ba30bba5-1677-4aa4-8e7a-cfe60962ad97.png

Mean squared error
The mean squared error (MSE) is a risk metric equal to the expected value of the squared (quadratic) error loss.

If ŷi is the predicted value of the ith sample and yi is the corresponding true value, then the MSE estimated over n samples is defined as follows:

https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/74907d35-5bc8-4633-a98f-4da226d9c69b.png

Classification metrics
The task of classification implies different rules for the estimation of the error. The advantage we have is that the number of outputs is discrete, so it can be determined exactly whether a prediction has failed or not in a binary way. That leads us to the main indicators.

Accuracy
The accuracy calculates either the fraction or the count of correct predictions for a model.
In multi-label classification, the function returns the subset's accuracy.

If the entire set of predicted labels for a sample strictly matches the true set of labels, then the subset's accuracy is 1.0; otherwise, it is 0.0.
If ŷi is the predicted value of the ith sample and yi is the corresponding true value, then the fraction of correct predictions over n samples is defined as follows:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/aa88df25-40d4-4786-a445-ceae24c86ec4.png

Precision score, recall, and F-measure
Precision score is as follows:


Here, tp is the number of true positives and fp is the number of false positives. The precision is the ability of the classifier to not label as positive a sample that is negative. The best value is 1 and the worst value is 0.

Recall is as follows:


Here, tp is the number of true positives and fn is the number of false negatives. The recall can be described as the ability of the classifier to find all the positive samples. Its values range from 1 (optimum) to zero.

F measure (Fβ and F1 measures) can be interpreted as a special kind of mean (weighted harmonic mean) of the precision and recall. A  Fβ measure's best value is 1 and its worst score is 0. With β = 1, Fβ and F1 are equivalent, and the recall and the precision are equally important:

Confusion matrix
Every classification task aims to predict a label or tag for new unknown data. A very efficient way of showing the classification's accuracy is through a confusion matrix, where we show [classified sample, ground truth] pairs and a detailed view of how the predictions are doing.

The expected output should be the main diagonal of the matrix with a 1.0 score; that is, all the expected values should match the real ones.

In the following code example, we will do a synthetic sample of predictions and real values, and generate a confusion matrix of the final data:

```python
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
y_true = [8,5,6,8,5,3,1,6,4,2,5,3,1,4]
y_pred = [8,5,6,8,5,2,3,4,4,5,5,7,2,6]
y = confusion_matrix(y_true, y_pred)
print y 
plt.imshow(confusion_matrix(y_true, y_pred), interpolation='nearest', cmap='plasma')
plt.xticks(np.arange(0,8), np.arange(1,9))
plt.yticks(np.arange(0,8), np.arange(1,9))
plt.show()
```

The result will be the following:
```python
[[0 1 1 0 0 0 0 0]
 [0 0 0 0 1 0 0 0]
 [0 1 0 0 0 0 1 0]
 [0 0 0 1 0 1 0 0]
 [0 0 0 0 3 0 0 0]
 [0 0 0 1 0 1 0 0]
 [0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 2]]
 ```

And the final confusion matrix graphic representation for these values will be as follows:
https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781786469878/files/assets/9b6fafc9-6534-481d-b5b6-392d08bdd22e.png

In the image, we see the high accuracy value in the (5,5) diagonal value with three correct predictions, and the (8,8) value with two. As we can see, the distribution of the accuracy by value can be intuitively extracted just by analyzing the graph.

Clustering quality measurements
Unsupervised learning techniques, understood as the labeling of data without a ground truth, makes it a bit difficult to implement significant metrics for the models. Nevertheless, there are a number of measures implemented for this kind of technique. In this section, we have a list of the most well-known ones.
Silhouette coefficient
The silhouette coefficient is a metric that doesn't need to know the labeling of the dataset. It gives an idea of the separation between clusters.

It is composed of two different elements:

The mean distance between a sample and all other points in the same class (a)
The mean distance between a sample and all other points in the nearest cluster (b)
The formula for this coefficient s is defined as follows:

Homogeneity, completeness, and V-measure
Homogeneity, completeness, and V-measure are three key related indicators of the quality of a clustering operation. In the following formulas, we will use K for the number of clusters, C for the number of classes, N for the total number of samples, and ack for the number of elements of class c in cluster k.

Homogeneity is a measure of the ratio of samples of a single class pertaining to a single cluster. The fewer different classes included in one cluster, the better. The lower bound should be 0.0 and the upper bound should be 1.0 (higher is better), and the formulation for it is expressed as follows:


Completeness measures the ratio of the member of a given class that is assigned to the same cluster:


V-measure is the harmonic mean of homogeneity and completeness, expressed by the following formula:


Summary
In this chapter, we reviewed all the main steps involved in a machine learning process. We will be, indirectly, using them throughout the book, and we hope they help you structure your future work too.

In the next chapter, we will review the programming languages and frameworks that we will be using to solve all our machine learning problems and become proficient with them before starting with the projects.