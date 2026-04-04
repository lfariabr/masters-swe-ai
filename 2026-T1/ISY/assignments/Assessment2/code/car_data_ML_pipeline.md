# Programming Task

Design and Creative Technologies, Torrens Unversity

- Student: Luis Guilherme de Barros Andrade Faria - A00187785 
- Subject Code: ISY 503 
- Subject Name: Intelligent Systems 
- Assessment No.: 2
- Title of Assessment: Programming Task
- Lecturer: Dr. Nandini Sidnal
- Date: April 2026

Copyright © 2026 by Luis G B A Faria

*Permission is hereby granted to make and distribute verbatim copies of this document provided the copyright notice and this permission notice are preserved on all copies.*


```python
# Shortcut for generating .md file:
'''
cd 2026-T1/ISY/assignments/Assessment2/code
jupyter nbconvert --to markdown car_data_ML_pipeline.ipynb
'''
```




    '\ncd 2026-T1/ISY/assignments/Assessment2/code\njupyter nbconvert --to markdown car_data_ML_pipeline.ipynb\n'



### Libraries + Setup


```python
# 1. Clear workspace (use in Jupyter/IPython)
%reset -f

# 2. Standard Imports
import numpy as np
import pandas as pd
import math
from sklearn import preprocessing, decomposition

# 3. TensorFlow Setup
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# 4. Set pandas output display settings
pd.options.display.float_format = "{:.2f}".format
pd.options.display.max_rows = 15

```

    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/compat/v2_compat.py:107: disable_resource_variables (from tensorflow.python.ops.variable_scope) is deprecated and will be removed in a future version.
    Instructions for updating:
    non-resource variables are not supported in the long term


### Loading the dataset 
The car data set we will be using in this lab is provided as a comma separated.
We will use the features of the car, to try to predict its price.



```python
# Provide the names for the columns since the CSV file with the data does
# not have a header row.
feature_names = ['symboling', 'normalized-losses', 'make', 'fuel-type',
        'aspiration', 'num-doors', 'body-style', 'drive-wheels',
        'engine-location', 'wheel-base', 'length', 'width', 'height', 'weight',
        'engine-type', 'num-cylinders', 'engine-size', 'fuel-system', 'bore',
        'stroke', 'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg',
        'highway-mpg', 'price']

# [Change #1]: dataset url
# old URL: https://storage.googleapis.com/mledu-datasets/cars_data.csv
# Load in the data from a CSV file that is comma separated using NEW URL
car_data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data',
                        sep=',', names=feature_names, header=None, encoding='latin-1')


# We'll then randomize the data, just to be sure not to get any pathological
# ordering effects that might harm the performance of Stochastic Gradient
# Descent.
car_data = car_data.reindex(np.random.permutation(car_data.index))

print("Data set loaded. Num examples: ", len(car_data))
```

    Data set loaded. Num examples:  205


*This is a really small dataset! Only 205 examples.*

*For simplicity in this codelab, we do not split the data further into training and validation. But this is a MUST do on real datasets, or else it will overfit to single dataset.*

### Task 0: data prep/exploration with pandas


```python
car_data[4:7]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symboling</th>
      <th>normalized-losses</th>
      <th>make</th>
      <th>fuel-type</th>
      <th>aspiration</th>
      <th>num-doors</th>
      <th>body-style</th>
      <th>drive-wheels</th>
      <th>engine-location</th>
      <th>wheel-base</th>
      <th>...</th>
      <th>engine-size</th>
      <th>fuel-system</th>
      <th>bore</th>
      <th>stroke</th>
      <th>compression-ratio</th>
      <th>horsepower</th>
      <th>peak-rpm</th>
      <th>city-mpg</th>
      <th>highway-mpg</th>
      <th>price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>185</th>
      <td>2</td>
      <td>94</td>
      <td>volkswagen</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>97.30</td>
      <td>...</td>
      <td>109</td>
      <td>mpfi</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>9.00</td>
      <td>85</td>
      <td>5250</td>
      <td>27</td>
      <td>34</td>
      <td>8195</td>
    </tr>
    <tr>
      <th>22</th>
      <td>1</td>
      <td>118</td>
      <td>dodge</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>fwd</td>
      <td>front</td>
      <td>93.70</td>
      <td>...</td>
      <td>90</td>
      <td>2bbl</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>6377</td>
    </tr>
    <tr>
      <th>157</th>
      <td>0</td>
      <td>91</td>
      <td>toyota</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>hatchback</td>
      <td>fwd</td>
      <td>front</td>
      <td>95.70</td>
      <td>...</td>
      <td>98</td>
      <td>2bbl</td>
      <td>3.19</td>
      <td>3.03</td>
      <td>9.00</td>
      <td>70</td>
      <td>4800</td>
      <td>30</td>
      <td>37</td>
      <td>7198</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 26 columns</p>
</div>




```python
# [Change #2]: Used to inspect data
# car_data.describe()
car_data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 205 entries, 4 to 142
    Data columns (total 26 columns):
     #   Column             Non-Null Count  Dtype  
    ---  ------             --------------  -----  
     0   symboling          205 non-null    int64  
     1   normalized-losses  205 non-null    object 
     2   make               205 non-null    object 
     3   fuel-type          205 non-null    object 
     4   aspiration         205 non-null    object 
     5   num-doors          205 non-null    object 
     6   body-style         205 non-null    object 
     7   drive-wheels       205 non-null    object 
     8   engine-location    205 non-null    object 
     9   wheel-base         205 non-null    float64
     10  length             205 non-null    float64
     11  width              205 non-null    float64
     12  height             205 non-null    float64
     13  weight             205 non-null    int64  
     14  engine-type        205 non-null    object 
     15  num-cylinders      205 non-null    object 
     16  engine-size        205 non-null    int64  
     17  fuel-system        205 non-null    object 
     18  bore               205 non-null    object 
     19  stroke             205 non-null    object 
     20  compression-ratio  205 non-null    float64
     21  horsepower         205 non-null    object 
     22  peak-rpm           205 non-null    object 
     23  city-mpg           205 non-null    int64  
     24  highway-mpg        205 non-null    int64  
     25  price              205 non-null    object 
    dtypes: float64(5), int64(5), object(16)
    memory usage: 43.2+ KB



```python
LABEL = 'price'

# numeric_feature_names = car_data[[
# 'symboling','normalized-losses','wheel-base','engine-size','bore','stroke','compression-ratio','horsepower','peak-rpm','city-mpg','highway-mpg','price']]

# [Change #3]: 
# After inspecting the dataset using car_data.describe() / car_data.info()
# I could find & adjust to 15 columns with continuous/ordinal numeric values
numeric_feature_names = [
    'symboling', 'normalized-losses', 'wheel-base',
    'length', 'width', 'height', 'weight', 'engine-size',
    'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg',
    'bore', 'stroke', 'compression-ratio'
]
categorical_feature_names = list(set(feature_names) - set(numeric_feature_names) - set([LABEL]))

# The correct solution will pass these assert statements.
assert len(numeric_feature_names) == 15
assert len(categorical_feature_names) == 10
print('Task 0 assertions passed.')
```

    Task 0 assertions passed.



```python
# Run to inspect numeric features.
car_data[numeric_feature_names]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>symboling</th>
      <th>normalized-losses</th>
      <th>wheel-base</th>
      <th>length</th>
      <th>width</th>
      <th>height</th>
      <th>weight</th>
      <th>engine-size</th>
      <th>horsepower</th>
      <th>peak-rpm</th>
      <th>city-mpg</th>
      <th>highway-mpg</th>
      <th>bore</th>
      <th>stroke</th>
      <th>compression-ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>164</td>
      <td>99.40</td>
      <td>176.60</td>
      <td>66.40</td>
      <td>54.30</td>
      <td>2824</td>
      <td>136</td>
      <td>115</td>
      <td>5500</td>
      <td>18</td>
      <td>22</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>8.00</td>
    </tr>
    <tr>
      <th>86</th>
      <td>1</td>
      <td>125</td>
      <td>96.30</td>
      <td>172.40</td>
      <td>65.40</td>
      <td>51.60</td>
      <td>2405</td>
      <td>122</td>
      <td>88</td>
      <td>5000</td>
      <td>25</td>
      <td>32</td>
      <td>3.35</td>
      <td>3.46</td>
      <td>8.50</td>
    </tr>
    <tr>
      <th>122</th>
      <td>1</td>
      <td>154</td>
      <td>93.70</td>
      <td>167.30</td>
      <td>63.80</td>
      <td>50.80</td>
      <td>2191</td>
      <td>98</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
    </tr>
    <tr>
      <th>85</th>
      <td>1</td>
      <td>125</td>
      <td>96.30</td>
      <td>172.40</td>
      <td>65.40</td>
      <td>51.60</td>
      <td>2365</td>
      <td>122</td>
      <td>88</td>
      <td>5000</td>
      <td>25</td>
      <td>32</td>
      <td>3.35</td>
      <td>3.46</td>
      <td>8.50</td>
    </tr>
    <tr>
      <th>185</th>
      <td>2</td>
      <td>94</td>
      <td>97.30</td>
      <td>171.70</td>
      <td>65.50</td>
      <td>55.70</td>
      <td>2212</td>
      <td>109</td>
      <td>85</td>
      <td>5250</td>
      <td>27</td>
      <td>34</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>78</th>
      <td>2</td>
      <td>161</td>
      <td>93.70</td>
      <td>157.30</td>
      <td>64.40</td>
      <td>50.80</td>
      <td>2004</td>
      <td>92</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
    </tr>
    <tr>
      <th>26</th>
      <td>1</td>
      <td>148</td>
      <td>93.70</td>
      <td>157.30</td>
      <td>63.80</td>
      <td>50.60</td>
      <td>1989</td>
      <td>90</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
    </tr>
    <tr>
      <th>77</th>
      <td>2</td>
      <td>161</td>
      <td>93.70</td>
      <td>157.30</td>
      <td>64.40</td>
      <td>50.80</td>
      <td>1944</td>
      <td>92</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
    </tr>
    <tr>
      <th>36</th>
      <td>0</td>
      <td>78</td>
      <td>96.50</td>
      <td>157.10</td>
      <td>63.90</td>
      <td>58.30</td>
      <td>2024</td>
      <td>92</td>
      <td>76</td>
      <td>6000</td>
      <td>30</td>
      <td>34</td>
      <td>2.92</td>
      <td>3.41</td>
      <td>9.20</td>
    </tr>
    <tr>
      <th>142</th>
      <td>0</td>
      <td>102</td>
      <td>97.20</td>
      <td>172.00</td>
      <td>65.40</td>
      <td>52.50</td>
      <td>2190</td>
      <td>108</td>
      <td>82</td>
      <td>4400</td>
      <td>28</td>
      <td>33</td>
      <td>3.62</td>
      <td>2.64</td>
      <td>9.50</td>
    </tr>
  </tbody>
</table>
<p>205 rows × 15 columns</p>
</div>




```python
# Run to inspect categorical features.
car_data[categorical_feature_names]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>aspiration</th>
      <th>fuel-system</th>
      <th>make</th>
      <th>num-cylinders</th>
      <th>drive-wheels</th>
      <th>num-doors</th>
      <th>body-style</th>
      <th>engine-type</th>
      <th>fuel-type</th>
      <th>engine-location</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>std</td>
      <td>mpfi</td>
      <td>audi</td>
      <td>five</td>
      <td>4wd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>86</th>
      <td>std</td>
      <td>2bbl</td>
      <td>mitsubishi</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>122</th>
      <td>std</td>
      <td>2bbl</td>
      <td>plymouth</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>85</th>
      <td>std</td>
      <td>2bbl</td>
      <td>mitsubishi</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>185</th>
      <td>std</td>
      <td>mpfi</td>
      <td>volkswagen</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>78</th>
      <td>std</td>
      <td>2bbl</td>
      <td>mitsubishi</td>
      <td>four</td>
      <td>fwd</td>
      <td>two</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>26</th>
      <td>std</td>
      <td>2bbl</td>
      <td>dodge</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>77</th>
      <td>std</td>
      <td>2bbl</td>
      <td>mitsubishi</td>
      <td>four</td>
      <td>fwd</td>
      <td>two</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>36</th>
      <td>std</td>
      <td>1bbl</td>
      <td>honda</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>wagon</td>
      <td>ohc</td>
      <td>gas</td>
      <td>front</td>
    </tr>
    <tr>
      <th>142</th>
      <td>std</td>
      <td>2bbl</td>
      <td>subaru</td>
      <td>four</td>
      <td>fwd</td>
      <td>four</td>
      <td>sedan</td>
      <td>ohcf</td>
      <td>gas</td>
      <td>front</td>
    </tr>
  </tbody>
</table>
<p>205 rows × 10 columns</p>
</div>




```python
# [Change #4]: Replace '?' with NaN first, then handle missing values properly.
# - Drop rows where price (the label) is missing — can't train without it.
# - Impute missing feature values with column mean — safer than 0 on a 205-row dataset.
for feature_name in numeric_feature_names + [LABEL]:
  car_data[feature_name] = pd.to_numeric(car_data[feature_name], errors='coerce')

# Drop rows with missing labels first
car_data = car_data[car_data[LABEL].notna() & (car_data[LABEL] > 0)].copy()

# Impute missing numeric features with column mean
for feature_name in numeric_feature_names:
  col_mean = car_data[feature_name].mean()
  car_data[feature_name] = car_data[feature_name].fillna(col_mean)

print(f"Rows after cleaning: {len(car_data)}")
print(f"Remaining NaNs in features: {car_data[numeric_feature_names].isna().sum().sum()}")
```

    Rows after cleaning: 201
    Remaining NaNs in features: 0


### Task 1: Make the best model with numeric features. No normalization allowed.

Modify the model provided below to achieve the lowest evaluation loss. 
You may want to change various hyperparameters:
- learning rate
- choice of optimizer
- hidden layer dimensions (make sure that choice here makes sense given the number of training examples)
- batch size
- num training steps
- anything else I can think of changing

Do not use the `normalizer_fn` arg on `numeric_column`.


```python
# [Change #5]: Replaced GradientDescentOptimizer with AdagradOptimizer.
# GradientDescentOptimizer uses a single global learning rate for all parameters.
# With unscaled features (weight ~3000 vs bore ~2.9), large-scale features produce
# large gradients that explode under a fixed lr=0.01, causing NaN loss.
# AdagradOptimizer maintains a per-parameter learning rate that shrinks as gradients
# accumulate — large-gradient parameters get a smaller effective lr automatically,
# handling the scale variance without requiring explicit normalization (Task 1 constraint).

# > GradientDescent is blind to feature scale. Adagrad isn't. On an unscaled dataset, that difference alone is worth an 83% reduction in loss.

# [Change #6]: Hyperparameter variables for easy tuning.
batch_size_parameter = 16
learning_rate_parameter = 0.01
hidden_units_parameter = [64]
optimizer_parameter = tf.train.AdagradOptimizer(learning_rate=learning_rate_parameter)

# Test results
# Run       │             Config             │ Final avg_loss │  RMSE (sqrt of avg_loss)
# *Run 1*   │ batch=16, hidden=[64], lr=0.01 │ 10,822,464     │ ~$3,290
# Run 2     │ batch=32, hidden=[32], lr=0.1  │ 12,703,589     │ ~$3,565
# Run 3     │ batch=32, hidden=[64], lr=0.01 │ 18,289,694     │ ~$4,276
# Run 4     │ batch=16, hidden=[64], lr=0.1  │ 19,032,338     │ ~$4,362

print(numeric_feature_names)
x_df = car_data[numeric_feature_names]
y_series = car_data['price']

# Create input_fn's so that the estimator knows how to read in your data.
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    y=y_series,
    batch_size=batch_size_parameter,
    num_epochs=None,
    shuffle=True)

eval_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    y=y_series,
    batch_size=batch_size_parameter,
    shuffle=False)

predict_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    batch_size=batch_size_parameter,
    shuffle=False)

# Feature columns allow the model to parse the data, perform common
# preprocessing, and automatically generate an input layer for the tf.Estimator.
model_feature_columns = [
    tf.feature_column.numeric_column(feature_name) for feature_name in numeric_feature_names
]
print('model_feature_columns', model_feature_columns)

est = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=hidden_units_parameter,
    optimizer=optimizer_parameter,
  )

# TRAIN
num_print_statements = 10
num_training_steps = 10000
for _ in range(num_print_statements):
  est.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores = est.evaluate(eval_input_fn)

  # The `scores` dictionary has several metrics auto-gen by canned Estimator.
  # `average_loss` is the average loss for an individual example.
  # `loss` is the summed loss for the batch.
  print('scores', scores)
```

    ['symboling', 'normalized-losses', 'wheel-base', 'length', 'width', 'height', 'weight', 'engine-size', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'bore', 'stroke', 'compression-ratio']
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/util/lazy_loader.py:59: The name tf.estimator.inputs is deprecated. Please use tf.compat.v1.estimator.inputs instead.
    
    WARNING:tensorflow:From /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/ipykernel_83872/741504662.py:29: The name tf.estimator.inputs.pandas_input_fn is deprecated. Please use tf.compat.v1.estimator.inputs.pandas_input_fn instead.
    
    model_feature_columns [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/training_util.py:396: Variable.initialized_value (from tensorflow.python.ops.variables) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use Variable.read_value. Variables in 2.X are initialized automatically both in eager and graph (inside tf.defun) contexts.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/inputs/queues/feeding_queue_runner.py:60: QueueRunner.__init__ (from tensorflow.python.training.queue_runner_impl) is deprecated and will be removed in a future version.
    Instructions for updating:
    To construct input pipelines, use the `tf.data` module.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/inputs/queues/feeding_functions.py:491: add_queue_runner (from tensorflow.python.training.queue_runner_impl) is deprecated and will be removed in a future version.
    Instructions for updating:
    To construct input pipelines, use the `tf.data` module.
    INFO:tensorflow:Calling model_fn.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/adagrad.py:138: calling Constant.__init__ (from tensorflow.python.ops.init_ops) with dtype is deprecated and will be removed in a future version.
    Instructions for updating:
    Call initializer instance with the dtype argument instead of passing it to the constructor
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:910: start_queue_runners (from tensorflow.python.training.queue_runner_impl) is deprecated and will be removed in a future version.
    Instructions for updating:
    To construct input pipelines, use the `tf.data` module.


    2026-04-03 17:05:53.988083: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
    2026-04-03 17:05:53.995398: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 1491789800.0, step = 1
    INFO:tensorflow:global_step/sec: 1159.78
    INFO:tensorflow:loss = 946620400.0, step = 101 (0.088 sec)
    INFO:tensorflow:global_step/sec: 966.755
    INFO:tensorflow:loss = 418638750.0, step = 201 (0.104 sec)
    INFO:tensorflow:global_step/sec: 1927.08
    INFO:tensorflow:loss = 251833120.0, step = 301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1816.57
    INFO:tensorflow:loss = 462638200.0, step = 401 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2011.27
    INFO:tensorflow:loss = 389854080.0, step = 501 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2055.45
    INFO:tensorflow:loss = 315524400.0, step = 601 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1909.57
    INFO:tensorflow:loss = 324723620.0, step = 701 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2286.76
    INFO:tensorflow:loss = 394393470.0, step = 801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2233.64
    INFO:tensorflow:loss = 559090200.0, step = 901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 171457500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:05:55
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09905s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:05:55
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 42476050.0, global_step = 1000, label/mean = 13207.129, loss = 656745000.0, prediction/mean = 13535.442
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-1000
    scores {'average_loss': 42476050.0, 'label/mean': 13207.129, 'loss': 656745000.0, 'prediction/mean': 13535.442, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-1000
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1173: get_checkpoint_mtimes (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file utilities to get mtimes.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 328676480.0, step = 1001
    INFO:tensorflow:global_step/sec: 1552.12
    INFO:tensorflow:loss = 339973630.0, step = 1101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2298.8
    INFO:tensorflow:loss = 292686300.0, step = 1201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2353.65
    INFO:tensorflow:loss = 707129700.0, step = 1301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2275.52
    INFO:tensorflow:loss = 441305800.0, step = 1401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2264.66
    INFO:tensorflow:loss = 585287040.0, step = 1501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2298.79
    INFO:tensorflow:loss = 755556000.0, step = 1601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2344.78
    INFO:tensorflow:loss = 871869000.0, step = 1701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2372.02
    INFO:tensorflow:loss = 276781220.0, step = 1801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2227.38
    INFO:tensorflow:loss = 773229700.0, step = 1901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 371737340.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:05:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08939s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:05:57
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 33550836.0, global_step = 2000, label/mean = 13207.129, loss = 518747520.0, prediction/mean = 13383.915
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-2000
    scores {'average_loss': 33550836.0, 'label/mean': 13207.129, 'loss': 518747520.0, 'prediction/mean': 13383.915, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 777318600.0, step = 2001
    INFO:tensorflow:global_step/sec: 1658.3
    INFO:tensorflow:loss = 686294850.0, step = 2101 (0.061 sec)
    INFO:tensorflow:global_step/sec: 2446.3
    INFO:tensorflow:loss = 1180038000.0, step = 2201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2306.74
    INFO:tensorflow:loss = 667893500.0, step = 2301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2326.68
    INFO:tensorflow:loss = 545661000.0, step = 2401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2370.79
    INFO:tensorflow:loss = 467756830.0, step = 2501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2182.07
    INFO:tensorflow:loss = 183197010.0, step = 2601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2377.51
    INFO:tensorflow:loss = 245723040.0, step = 2701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2414.7
    INFO:tensorflow:loss = 252077230.0, step = 2801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2010.25
    INFO:tensorflow:loss = 861587200.0, step = 2901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 241465400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:05:58
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08969s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:05:58
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 27460392.0, global_step = 3000, label/mean = 13207.129, loss = 424579900.0, prediction/mean = 13465.35
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-3000
    scores {'average_loss': 27460392.0, 'label/mean': 13207.129, 'loss': 424579900.0, 'prediction/mean': 13465.35, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 197814750.0, step = 3001
    INFO:tensorflow:global_step/sec: 1620.9
    INFO:tensorflow:loss = 199488860.0, step = 3101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2372.53
    INFO:tensorflow:loss = 232379580.0, step = 3201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2333.4
    INFO:tensorflow:loss = 1098135300.0, step = 3301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2212.38
    INFO:tensorflow:loss = 107763520.0, step = 3401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2147.21
    INFO:tensorflow:loss = 687318900.0, step = 3501 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2390.87
    INFO:tensorflow:loss = 614972800.0, step = 3601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2259.16
    INFO:tensorflow:loss = 114842260.0, step = 3701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2334.11
    INFO:tensorflow:loss = 335761600.0, step = 3801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2335.63
    INFO:tensorflow:loss = 353039870.0, step = 3901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 467248670.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:00
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08896s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:00
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 23918460.0, global_step = 4000, label/mean = 13207.129, loss = 369816200.0, prediction/mean = 13366.906
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-4000
    scores {'average_loss': 23918460.0, 'label/mean': 13207.129, 'loss': 369816200.0, 'prediction/mean': 13366.906, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 108436450.0, step = 4001
    INFO:tensorflow:global_step/sec: 1630.55
    INFO:tensorflow:loss = 180359840.0, step = 4101 (0.062 sec)
    INFO:tensorflow:global_step/sec: 2309.36
    INFO:tensorflow:loss = 163573180.0, step = 4201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2314.7
    INFO:tensorflow:loss = 827838850.0, step = 4301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2361.44
    INFO:tensorflow:loss = 1023360800.0, step = 4401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2330.4
    INFO:tensorflow:loss = 564897600.0, step = 4501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2281.71
    INFO:tensorflow:loss = 147350480.0, step = 4601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2258.3
    INFO:tensorflow:loss = 154311710.0, step = 4701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2352.23
    INFO:tensorflow:loss = 283512830.0, step = 4801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2240.94
    INFO:tensorflow:loss = 108446056.0, step = 4901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1064: remove_checkpoint (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file APIs to delete files with this prefix.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 104588690.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:01
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09053s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:01
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 21976566.0, global_step = 5000, label/mean = 13207.129, loss = 339791520.0, prediction/mean = 13462.928
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-5000
    scores {'average_loss': 21976566.0, 'label/mean': 13207.129, 'loss': 339791520.0, 'prediction/mean': 13462.928, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 127493380.0, step = 5001
    INFO:tensorflow:global_step/sec: 1676.64
    INFO:tensorflow:loss = 293340220.0, step = 5101 (0.061 sec)
    INFO:tensorflow:global_step/sec: 2268.65
    INFO:tensorflow:loss = 766369200.0, step = 5201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2054.36
    INFO:tensorflow:loss = 528954300.0, step = 5301 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1990.33
    INFO:tensorflow:loss = 354338430.0, step = 5401 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2410.45
    INFO:tensorflow:loss = 653068100.0, step = 5501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2328.84
    INFO:tensorflow:loss = 66789204.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2351.05
    INFO:tensorflow:loss = 188194160.0, step = 5701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2312.84
    INFO:tensorflow:loss = 144234420.0, step = 5801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2194.47
    INFO:tensorflow:loss = 554253060.0, step = 5901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 437569600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08848s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:03
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 20946808.0, global_step = 6000, label/mean = 13207.129, loss = 323869900.0, prediction/mean = 13260.156
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-6000
    scores {'average_loss': 20946808.0, 'label/mean': 13207.129, 'loss': 323869900.0, 'prediction/mean': 13260.156, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 83132750.0, step = 6001
    INFO:tensorflow:global_step/sec: 1580.33
    INFO:tensorflow:loss = 359557380.0, step = 6101 (0.064 sec)
    INFO:tensorflow:global_step/sec: 2058.72
    INFO:tensorflow:loss = 624929000.0, step = 6201 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2367.03
    INFO:tensorflow:loss = 128453670.0, step = 6301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2352.49
    INFO:tensorflow:loss = 554366500.0, step = 6401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2465.5
    INFO:tensorflow:loss = 111942850.0, step = 6501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2348.74
    INFO:tensorflow:loss = 167232670.0, step = 6601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2268.2
    INFO:tensorflow:loss = 360182800.0, step = 6701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2297.15
    INFO:tensorflow:loss = 621974340.0, step = 6801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2258
    INFO:tensorflow:loss = 100938650.0, step = 6901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 414461440.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:04
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08954s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:04
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 20312712.0, global_step = 7000, label/mean = 13207.129, loss = 314065800.0, prediction/mean = 13314.888
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-7000
    scores {'average_loss': 20312712.0, 'label/mean': 13207.129, 'loss': 314065800.0, 'prediction/mean': 13314.888, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 503046100.0, step = 7001
    INFO:tensorflow:global_step/sec: 1210.78
    INFO:tensorflow:loss = 129420560.0, step = 7101 (0.089 sec)
    INFO:tensorflow:global_step/sec: 1338.01
    INFO:tensorflow:loss = 1018421900.0, step = 7201 (0.070 sec)
    INFO:tensorflow:global_step/sec: 1200.38
    INFO:tensorflow:loss = 622424060.0, step = 7301 (0.084 sec)
    INFO:tensorflow:global_step/sec: 1650.68
    INFO:tensorflow:loss = 168925060.0, step = 7401 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1810.25
    INFO:tensorflow:loss = 157746980.0, step = 7501 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1758
    INFO:tensorflow:loss = 390494140.0, step = 7601 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1346.8
    INFO:tensorflow:loss = 531666560.0, step = 7701 (0.074 sec)
    INFO:tensorflow:global_step/sec: 1890.47
    INFO:tensorflow:loss = 260011260.0, step = 7801 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1778.28
    INFO:tensorflow:loss = 242618800.0, step = 7901 (0.056 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 566995400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:06
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12933s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:06
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 19902674.0, global_step = 8000, label/mean = 13207.129, loss = 307725950.0, prediction/mean = 13344.985
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-8000
    scores {'average_loss': 19902674.0, 'label/mean': 13207.129, 'loss': 307725950.0, 'prediction/mean': 13344.985, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 596311400.0, step = 8001
    INFO:tensorflow:global_step/sec: 1526.18
    INFO:tensorflow:loss = 86831210.0, step = 8101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 1923.78
    INFO:tensorflow:loss = 244620220.0, step = 8201 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1945.07
    INFO:tensorflow:loss = 127609460.0, step = 8301 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1938.96
    INFO:tensorflow:loss = 501255520.0, step = 8401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1835.9
    INFO:tensorflow:loss = 440882050.0, step = 8501 (0.054 sec)
    INFO:tensorflow:global_step/sec: 1925.34
    INFO:tensorflow:loss = 535798400.0, step = 8601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1966.02
    INFO:tensorflow:loss = 903512800.0, step = 8701 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1942.62
    INFO:tensorflow:loss = 515851140.0, step = 8801 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2037.66
    INFO:tensorflow:loss = 638670400.0, step = 8901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 101181630.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:08
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11533s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:08
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 19613454.0, global_step = 9000, label/mean = 13207.129, loss = 303254180.0, prediction/mean = 13248.078
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-9000
    scores {'average_loss': 19613454.0, 'label/mean': 13207.129, 'loss': 303254180.0, 'prediction/mean': 13248.078, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 125537620.0, step = 9001
    INFO:tensorflow:global_step/sec: 1483.96
    INFO:tensorflow:loss = 524195330.0, step = 9101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2264.44
    INFO:tensorflow:loss = 198264690.0, step = 9201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2288.86
    INFO:tensorflow:loss = 574075260.0, step = 9301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2287.46
    INFO:tensorflow:loss = 204862240.0, step = 9401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2293.84
    INFO:tensorflow:loss = 692801400.0, step = 9501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2398.25
    INFO:tensorflow:loss = 107144740.0, step = 9601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2367.54
    INFO:tensorflow:loss = 89429010.0, step = 9701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2344.5
    INFO:tensorflow:loss = 184545840.0, step = 9801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2397.46
    INFO:tensorflow:loss = 152185740.0, step = 9901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 230778990.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:09
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10234s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:09
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 19334088.0, global_step = 10000, label/mean = 13207.129, loss = 298934750.0, prediction/mean = 13344.923
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjb1ml488/model.ckpt-10000
    scores {'average_loss': 19334088.0, 'label/mean': 13207.129, 'loss': 298934750.0, 'prediction/mean': 13344.923, 'global_step': 10000}


#### Visualize model's predictions

After you have a trained model, it may be helpful to understand how your model's inference differs from the actual data.

This helper function `scatter_plot_inference` does that for you. Real data is in grey. Your model's predictions are in orange.



```python
from matplotlib import pyplot as plt


def scatter_plot_inference_grid(est, x_df, feature_names):
  """Plots the predictions of the model against each feature.

  Args:
    est: The trained tf.Estimator.
    x_df: The pandas dataframe with the input data (used to create
      predict_input_fn).
    feature_names: An iterable of string feature names to plot.
  """
  def scatter_plot_inference(axis,
                             x_axis_feature_name,
                             y_axis_feature_name,
                             predictions):
    """Generate one subplot."""
    # Plot the real data in grey.
    y_axis_feature_name = 'price'
    axis.set_ylabel(y_axis_feature_name)
    axis.set_xlabel(x_axis_feature_name)
    axis.scatter(car_data[x_axis_feature_name],
                 car_data[y_axis_feature_name],
                 c='grey')

    # Plot the predicted data in orange.
    axis.scatter(car_data[x_axis_feature_name], predictions, c='orange')

  predict_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    batch_size=batch_size_parameter,
    shuffle=False)

  predictions = [
    x['predictions'][0]
    for x in est.predict(predict_input_fn)
  ]

  num_cols = 3
  num_rows = int(math.ceil(len(feature_names)/float(num_cols)))
  f, axarr = plt.subplots(num_rows, num_cols)
  size = 4.5
  f.set_size_inches(num_cols*size, num_rows*size)

  for i, feature_name in enumerate(numeric_feature_names):
    axis = axarr[int(i/num_cols), i%num_cols]
    scatter_plot_inference(axis, feature_name, 'price', predictions)
  plt.show()

# scatter_plot_inference_grid(est, x_df, numeric_feature_names)
```


```python
# [Change #11]: Regressor exploration — LinearRegressor baseline + deeper DNNs                        
# Reuses model_feature_columns, train_input_fn, eval_input_fn from Task 1.                            
                                                                                                        
# T1.5 — LinearRegressor (does a linear model suffice, or does the DNN add value?)                    
est_linear = tf.estimator.LinearRegressor(                                                            
    feature_columns=model_feature_columns,                                                            
    optimizer=tf.train.AdagradOptimizer(learning_rate=learning_rate_parameter),                       
)                                                                                                     
for _ in range(num_print_statements):                                                                 
    est_linear.train(train_input_fn, steps=num_training_steps // num_print_statements)                
    scores_linear = est_linear.evaluate(eval_input_fn)                                                
    print('scores_linear', scores_linear)                                                             
                                                                                                    
# T1.6 — Deeper DNN [64, 32]                                                                          
est_deep1 = tf.estimator.DNNRegressor(                                                                
    feature_columns=model_feature_columns,                                                            
    hidden_units=[64, 32],                                                                            
    optimizer=optimizer_parameter,                                                                    
)                                                                                                     
for _ in range(num_print_statements):                                                                 
    est_deep1.train(train_input_fn, steps=num_training_steps // num_print_statements)                 
    scores_deep1 = est_deep1.evaluate(eval_input_fn)                                                  
    print('scores_deep1', scores_deep1)                                                               
                                                                                                    
# T1.7 — Wider DNN [128, 64]                                                                          
est_deep2 = tf.estimator.DNNRegressor(                                                                
    feature_columns=model_feature_columns,                                                            
    hidden_units=[128, 64],                                                                           
    optimizer=optimizer_parameter,                                                                    
)                                                                                                     
for _ in range(num_print_statements):                                                                 
    est_deep2.train(train_input_fn, steps=num_training_steps // num_print_statements)                 
    scores_deep2 = est_deep2.evaluate(eval_input_fn)                                                  
    print('scores_deep2', scores_deep2)                                                               
                                                                                                    
# Results (fill in after running):                                                                    
# Model         │ hidden_units │ avg_loss │ RMSE                                                      
# LinearReg     │ —            │          │                                                           
# DNN [64, 32]  │ [64, 32]     │          │                                                           
# DNN [128, 64] │ [128, 64]    │          │
```

    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 4867740700.0, step = 1
    INFO:tensorflow:global_step/sec: 1403.51
    INFO:tensorflow:loss = 2462930400.0, step = 101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2365.19
    INFO:tensorflow:loss = 4487678000.0, step = 201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2445.94
    INFO:tensorflow:loss = 4838490000.0, step = 301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1993.85
    INFO:tensorflow:loss = 1508902900.0, step = 401 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2014.56
    INFO:tensorflow:loss = 2217576700.0, step = 501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2281.34
    INFO:tensorflow:loss = 1773181700.0, step = 601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2102.11
    INFO:tensorflow:loss = 1160468900.0, step = 701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1979.3
    INFO:tensorflow:loss = 1261087400.0, step = 801 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2375.97
    INFO:tensorflow:loss = 2584458200.0, step = 901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 2544060200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12484s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:13
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 130147570.0, global_step = 1000, label/mean = 13207.129, loss = 2012281600.0, prediction/mean = 4766.975
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-1000
    scores_linear {'average_loss': 130147570.0, 'label/mean': 13207.129, 'loss': 2012281600.0, 'prediction/mean': 4766.975, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 2011251100.0, step = 1001
    INFO:tensorflow:global_step/sec: 1406.21
    INFO:tensorflow:loss = 1999123000.0, step = 1101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 1845.16
    INFO:tensorflow:loss = 874496260.0, step = 1201 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2216.27
    INFO:tensorflow:loss = 974589700.0, step = 1301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2027.94
    INFO:tensorflow:loss = 1310732300.0, step = 1401 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2097.76
    INFO:tensorflow:loss = 1201009700.0, step = 1501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2323.62
    INFO:tensorflow:loss = 3520565800.0, step = 1601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2444.87
    INFO:tensorflow:loss = 2546770200.0, step = 1701 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2348.7
    INFO:tensorflow:loss = 2203506700.0, step = 1801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2177.98
    INFO:tensorflow:loss = 697168300.0, step = 1901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 1495942300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:16
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.15221s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:16
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 102318744.0, global_step = 2000, label/mean = 13207.129, loss = 1582005100.0, prediction/mean = 6513.459
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-2000
    scores_linear {'average_loss': 102318744.0, 'label/mean': 13207.129, 'loss': 1582005100.0, 'prediction/mean': 6513.459, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2555903200.0, step = 2001
    INFO:tensorflow:global_step/sec: 1228.91
    INFO:tensorflow:loss = 388899460.0, step = 2101 (0.082 sec)
    INFO:tensorflow:global_step/sec: 1918.2
    INFO:tensorflow:loss = 633065000.0, step = 2201 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1921.2
    INFO:tensorflow:loss = 701675700.0, step = 2301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1920.64
    INFO:tensorflow:loss = 2986471400.0, step = 2401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2316.74
    INFO:tensorflow:loss = 4176973800.0, step = 2501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2385.27
    INFO:tensorflow:loss = 3838492200.0, step = 2601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2284.35
    INFO:tensorflow:loss = 375816640.0, step = 2701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1939.34
    INFO:tensorflow:loss = 1087795300.0, step = 2801 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2209.37
    INFO:tensorflow:loss = 1349377900.0, step = 2901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 295584220.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:19
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12465s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:19
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 86679416.0, global_step = 3000, label/mean = 13207.129, loss = 1340197100.0, prediction/mean = 7718.372
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-3000
    scores_linear {'average_loss': 86679416.0, 'label/mean': 13207.129, 'loss': 1340197100.0, 'prediction/mean': 7718.372, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 2323441200.0, step = 3001
    INFO:tensorflow:global_step/sec: 1228.97
    INFO:tensorflow:loss = 1959166000.0, step = 3101 (0.082 sec)
    INFO:tensorflow:global_step/sec: 2176.56
    INFO:tensorflow:loss = 1128292400.0, step = 3201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2122.82
    INFO:tensorflow:loss = 2100156700.0, step = 3301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2219.02
    INFO:tensorflow:loss = 305110900.0, step = 3401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2206.92
    INFO:tensorflow:loss = 4663068700.0, step = 3501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2219.65
    INFO:tensorflow:loss = 998739200.0, step = 3601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2254.29
    INFO:tensorflow:loss = 2450433300.0, step = 3701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2256.92
    INFO:tensorflow:loss = 219034600.0, step = 3801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2152.17
    INFO:tensorflow:loss = 473759100.0, step = 3901 (0.047 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 984912260.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:21
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12860s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:22
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 76653870.0, global_step = 4000, label/mean = 13207.129, loss = 1185186800.0, prediction/mean = 8641.864
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-4000
    scores_linear {'average_loss': 76653870.0, 'label/mean': 13207.129, 'loss': 1185186800.0, 'prediction/mean': 8641.864, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 1019200800.0, step = 4001
    INFO:tensorflow:global_step/sec: 1269.02
    INFO:tensorflow:loss = 2076785500.0, step = 4101 (0.080 sec)
    INFO:tensorflow:global_step/sec: 2348.57
    INFO:tensorflow:loss = 1433766500.0, step = 4201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2197.04
    INFO:tensorflow:loss = 602866200.0, step = 4301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2169.1
    INFO:tensorflow:loss = 1599833500.0, step = 4401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2007.09
    INFO:tensorflow:loss = 348100350.0, step = 4501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1920.94
    INFO:tensorflow:loss = 226985150.0, step = 4601 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2155.49
    INFO:tensorflow:loss = 212518660.0, step = 4701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2431.2
    INFO:tensorflow:loss = 155481600.0, step = 4801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2283.06
    INFO:tensorflow:loss = 1027534600.0, step = 4901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 889470850.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:24
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12428s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:24
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 69892240.0, global_step = 5000, label/mean = 13207.129, loss = 1080641700.0, prediction/mean = 9376.069
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-5000
    scores_linear {'average_loss': 69892240.0, 'label/mean': 13207.129, 'loss': 1080641700.0, 'prediction/mean': 9376.069, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 177022380.0, step = 5001
    INFO:tensorflow:global_step/sec: 1370.56
    INFO:tensorflow:loss = 1220348400.0, step = 5101 (0.074 sec)
    INFO:tensorflow:global_step/sec: 2347.47
    INFO:tensorflow:loss = 1485530600.0, step = 5201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2369.84
    INFO:tensorflow:loss = 1017375360.0, step = 5301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2255.71
    INFO:tensorflow:loss = 550475200.0, step = 5401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2344.01
    INFO:tensorflow:loss = 1281211300.0, step = 5501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2328.19
    INFO:tensorflow:loss = 926133500.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2242.5
    INFO:tensorflow:loss = 1054400260.0, step = 5701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2191.06
    INFO:tensorflow:loss = 1074718700.0, step = 5801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2195.38
    INFO:tensorflow:loss = 3254703600.0, step = 5901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 922770900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:27
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12846s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:27
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 65132268.0, global_step = 6000, label/mean = 13207.129, loss = 1007045060.0, prediction/mean = 9979.491
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-6000
    scores_linear {'average_loss': 65132268.0, 'label/mean': 13207.129, 'loss': 1007045060.0, 'prediction/mean': 9979.491, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 1315003400.0, step = 6001
    INFO:tensorflow:global_step/sec: 1332.56
    INFO:tensorflow:loss = 1103857800.0, step = 6101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2130.32
    INFO:tensorflow:loss = 110427870.0, step = 6201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2301.45
    INFO:tensorflow:loss = 301240320.0, step = 6301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2359.98
    INFO:tensorflow:loss = 525034000.0, step = 6401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2279.05
    INFO:tensorflow:loss = 981180700.0, step = 6501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2377.44
    INFO:tensorflow:loss = 2565706500.0, step = 6601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2254.13
    INFO:tensorflow:loss = 1343937700.0, step = 6701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2036.62
    INFO:tensorflow:loss = 1156109200.0, step = 6801 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2092.88
    INFO:tensorflow:loss = 771091400.0, step = 6901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 277450100.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:29
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12404s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:29
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 61726720.0, global_step = 7000, label/mean = 13207.129, loss = 954390100.0, prediction/mean = 10479.733
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-7000
    scores_linear {'average_loss': 61726720.0, 'label/mean': 13207.129, 'loss': 954390100.0, 'prediction/mean': 10479.733, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 797220600.0, step = 7001
    INFO:tensorflow:global_step/sec: 1262.28
    INFO:tensorflow:loss = 435482700.0, step = 7101 (0.080 sec)
    INFO:tensorflow:global_step/sec: 2320.78
    INFO:tensorflow:loss = 445783840.0, step = 7201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2104.33
    INFO:tensorflow:loss = 1136186600.0, step = 7301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1288.43
    INFO:tensorflow:loss = 2984645600.0, step = 7401 (0.078 sec)
    INFO:tensorflow:global_step/sec: 2309.49
    INFO:tensorflow:loss = 1268283300.0, step = 7501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2194.57
    INFO:tensorflow:loss = 492404400.0, step = 7601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2400.15
    INFO:tensorflow:loss = 425123000.0, step = 7701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2298.59
    INFO:tensorflow:loss = 1213094500.0, step = 7801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2301.22
    INFO:tensorflow:loss = 1101849100.0, step = 7901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 144669280.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:32
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12651s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:32
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 59219856.0, global_step = 8000, label/mean = 13207.129, loss = 915630100.0, prediction/mean = 10903.753
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-8000
    scores_linear {'average_loss': 59219856.0, 'label/mean': 13207.129, 'loss': 915630100.0, 'prediction/mean': 10903.753, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 1010302500.0, step = 8001
    INFO:tensorflow:global_step/sec: 1268.46
    INFO:tensorflow:loss = 799578600.0, step = 8101 (0.079 sec)
    INFO:tensorflow:global_step/sec: 2032.53
    INFO:tensorflow:loss = 849397400.0, step = 8201 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2303.61
    INFO:tensorflow:loss = 1278341400.0, step = 8301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1912.01
    INFO:tensorflow:loss = 1253259800.0, step = 8401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2180.26
    INFO:tensorflow:loss = 988554200.0, step = 8501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2314.92
    INFO:tensorflow:loss = 561580900.0, step = 8601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2018.33
    INFO:tensorflow:loss = 145239860.0, step = 8701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2341.49
    INFO:tensorflow:loss = 282267700.0, step = 8801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2287.33
    INFO:tensorflow:loss = 837667800.0, step = 8901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 308580350.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:34
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13621s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:34
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 57377044.0, global_step = 9000, label/mean = 13207.129, loss = 887137340.0, prediction/mean = 11260.364
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-9000
    scores_linear {'average_loss': 57377044.0, 'label/mean': 13207.129, 'loss': 887137340.0, 'prediction/mean': 11260.364, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 507526660.0, step = 9001
    INFO:tensorflow:global_step/sec: 1248.72
    INFO:tensorflow:loss = 651741950.0, step = 9101 (0.081 sec)
    INFO:tensorflow:global_step/sec: 1941.83
    INFO:tensorflow:loss = 1829479300.0, step = 9201 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2330.89
    INFO:tensorflow:loss = 971676700.0, step = 9301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2067.47
    INFO:tensorflow:loss = 1317478800.0, step = 9401 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2046.87
    INFO:tensorflow:loss = 1063828900.0, step = 9501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2262.76
    INFO:tensorflow:loss = 1514280600.0, step = 9601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1958.87
    INFO:tensorflow:loss = 553413000.0, step = 9701 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2374.65
    INFO:tensorflow:loss = 612639600.0, step = 9801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2333.34
    INFO:tensorflow:loss = 95845620.0, step = 9901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 1436008700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:37
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12659s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:37
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 56007930.0, global_step = 10000, label/mean = 13207.129, loss = 865968800.0, prediction/mean = 11560.951
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpf6j6fkog/model.ckpt-10000
    scores_linear {'average_loss': 56007930.0, 'label/mean': 13207.129, 'loss': 865968800.0, 'prediction/mean': 11560.951, 'global_step': 10000}
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 5749579000.0, step = 1
    INFO:tensorflow:global_step/sec: 1535.32
    INFO:tensorflow:loss = 145904510.0, step = 101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2249.26
    INFO:tensorflow:loss = 247216700.0, step = 201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2331.54
    INFO:tensorflow:loss = 838908800.0, step = 301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2381.12
    INFO:tensorflow:loss = 232710700.0, step = 401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2395.21
    INFO:tensorflow:loss = 629222100.0, step = 501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2187.85
    INFO:tensorflow:loss = 855592450.0, step = 601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2346.98
    INFO:tensorflow:loss = 486011550.0, step = 701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2291.53
    INFO:tensorflow:loss = 560987800.0, step = 801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2268.23
    INFO:tensorflow:loss = 596382850.0, step = 901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 806050900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09420s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:39
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 36403304.0, global_step = 1000, label/mean = 13207.129, loss = 562851100.0, prediction/mean = 13711.541
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-1000
    scores_deep1 {'average_loss': 36403304.0, 'label/mean': 13207.129, 'loss': 562851100.0, 'prediction/mean': 13711.541, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 460966530.0, step = 1001
    INFO:tensorflow:global_step/sec: 1478.11
    INFO:tensorflow:loss = 225279040.0, step = 1101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2425.13
    INFO:tensorflow:loss = 309892220.0, step = 1201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2392.47
    INFO:tensorflow:loss = 461337200.0, step = 1301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2402.98
    INFO:tensorflow:loss = 220898300.0, step = 1401 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2234.84
    INFO:tensorflow:loss = 135669820.0, step = 1501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2130.65
    INFO:tensorflow:loss = 261351550.0, step = 1601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2221.58
    INFO:tensorflow:loss = 212965140.0, step = 1701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2327.91
    INFO:tensorflow:loss = 428566560.0, step = 1801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2160.34
    INFO:tensorflow:loss = 592152700.0, step = 1901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 1050385600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:41
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09378s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:41
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 22663206.0, global_step = 2000, label/mean = 13207.129, loss = 350408030.0, prediction/mean = 13389.901
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-2000
    scores_deep1 {'average_loss': 22663206.0, 'label/mean': 13207.129, 'loss': 350408030.0, 'prediction/mean': 13389.901, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 120495310.0, step = 2001
    INFO:tensorflow:global_step/sec: 1612.39
    INFO:tensorflow:loss = 130401500.0, step = 2101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2152.61
    INFO:tensorflow:loss = 196812290.0, step = 2201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2307.17
    INFO:tensorflow:loss = 360414340.0, step = 2301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2137.17
    INFO:tensorflow:loss = 567704900.0, step = 2401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2367.26
    INFO:tensorflow:loss = 178948860.0, step = 2501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2258.77
    INFO:tensorflow:loss = 283485950.0, step = 2601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2460.51
    INFO:tensorflow:loss = 190818000.0, step = 2701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2414.81
    INFO:tensorflow:loss = 447824540.0, step = 2801 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2361.5
    INFO:tensorflow:loss = 149744930.0, step = 2901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 115663340.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:42
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09317s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:42
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 20120238.0, global_step = 3000, label/mean = 13207.129, loss = 311089820.0, prediction/mean = 13308.1
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-3000
    scores_deep1 {'average_loss': 20120238.0, 'label/mean': 13207.129, 'loss': 311089820.0, 'prediction/mean': 13308.1, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 526639100.0, step = 3001
    INFO:tensorflow:global_step/sec: 1494.25
    INFO:tensorflow:loss = 188010770.0, step = 3101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2192.84
    INFO:tensorflow:loss = 242768430.0, step = 3201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2451.83
    INFO:tensorflow:loss = 793790340.0, step = 3301 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2365.57
    INFO:tensorflow:loss = 801659000.0, step = 3401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2288.22
    INFO:tensorflow:loss = 91498850.0, step = 3501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2151.19
    INFO:tensorflow:loss = 312219100.0, step = 3601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2342.26
    INFO:tensorflow:loss = 166905500.0, step = 3701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2238.54
    INFO:tensorflow:loss = 89431980.0, step = 3801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2103.94
    INFO:tensorflow:loss = 712388500.0, step = 3901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 206623310.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09386s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:44
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 19272752.0, global_step = 4000, label/mean = 13207.129, loss = 297986370.0, prediction/mean = 13306.852
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-4000
    scores_deep1 {'average_loss': 19272752.0, 'label/mean': 13207.129, 'loss': 297986370.0, 'prediction/mean': 13306.852, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 527391040.0, step = 4001
    INFO:tensorflow:global_step/sec: 1607.07
    INFO:tensorflow:loss = 277287170.0, step = 4101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2387.37
    INFO:tensorflow:loss = 517912260.0, step = 4201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2278
    INFO:tensorflow:loss = 451657380.0, step = 4301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2371.81
    INFO:tensorflow:loss = 156720720.0, step = 4401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2262.45
    INFO:tensorflow:loss = 118525250.0, step = 4501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2118.11
    INFO:tensorflow:loss = 164619580.0, step = 4601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2015.18
    INFO:tensorflow:loss = 183757440.0, step = 4701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2172.27
    INFO:tensorflow:loss = 183372370.0, step = 4801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2359.77
    INFO:tensorflow:loss = 813203700.0, step = 4901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 146241900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:45
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09411s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:46
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 18656756.0, global_step = 5000, label/mean = 13207.129, loss = 288462140.0, prediction/mean = 13345.35
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-5000
    scores_deep1 {'average_loss': 18656756.0, 'label/mean': 13207.129, 'loss': 288462140.0, 'prediction/mean': 13345.35, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 84264800.0, step = 5001
    INFO:tensorflow:global_step/sec: 1407.82
    INFO:tensorflow:loss = 335361540.0, step = 5101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2175.62
    INFO:tensorflow:loss = 406984160.0, step = 5201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1997.36
    INFO:tensorflow:loss = 152681950.0, step = 5301 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2439.73
    INFO:tensorflow:loss = 143690100.0, step = 5401 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2219.07
    INFO:tensorflow:loss = 72230210.0, step = 5501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2319.38
    INFO:tensorflow:loss = 271471260.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2082.55
    INFO:tensorflow:loss = 112824300.0, step = 5701 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2378.86
    INFO:tensorflow:loss = 108195384.0, step = 5801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2299.11
    INFO:tensorflow:loss = 173838220.0, step = 5901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 157877870.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:47
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09447s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:47
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 18168266.0, global_step = 6000, label/mean = 13207.129, loss = 280909340.0, prediction/mean = 13410.453
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-6000
    scores_deep1 {'average_loss': 18168266.0, 'label/mean': 13207.129, 'loss': 280909340.0, 'prediction/mean': 13410.453, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 653003260.0, step = 6001
    INFO:tensorflow:global_step/sec: 1380.37
    INFO:tensorflow:loss = 135441260.0, step = 6101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2313.96
    INFO:tensorflow:loss = 100800740.0, step = 6201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2285.4
    INFO:tensorflow:loss = 114250290.0, step = 6301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2348.79
    INFO:tensorflow:loss = 201802430.0, step = 6401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2296.96
    INFO:tensorflow:loss = 184064480.0, step = 6501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2131.74
    INFO:tensorflow:loss = 185403740.0, step = 6601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2046.15
    INFO:tensorflow:loss = 64761930.0, step = 6701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2422.07
    INFO:tensorflow:loss = 270815740.0, step = 6801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2361.33
    INFO:tensorflow:loss = 669277440.0, step = 6901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 566816900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:49
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09520s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:49
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 17811292.0, global_step = 7000, label/mean = 13207.129, loss = 275389980.0, prediction/mean = 13538.767
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-7000
    scores_deep1 {'average_loss': 17811292.0, 'label/mean': 13207.129, 'loss': 275389980.0, 'prediction/mean': 13538.767, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 182582780.0, step = 7001
    INFO:tensorflow:global_step/sec: 1520.31
    INFO:tensorflow:loss = 280962850.0, step = 7101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2348.8
    INFO:tensorflow:loss = 136304140.0, step = 7201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2421.65
    INFO:tensorflow:loss = 148291420.0, step = 7301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2340
    INFO:tensorflow:loss = 333131970.0, step = 7401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2392.68
    INFO:tensorflow:loss = 257716140.0, step = 7501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2121.75
    INFO:tensorflow:loss = 511072300.0, step = 7601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2113.4
    INFO:tensorflow:loss = 247650750.0, step = 7701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2210.33
    INFO:tensorflow:loss = 81975200.0, step = 7801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2468.22
    INFO:tensorflow:loss = 58268630.0, step = 7901 (0.041 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 146527150.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:50
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09379s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:50
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 17423056.0, global_step = 8000, label/mean = 13207.129, loss = 269387260.0, prediction/mean = 13305.626
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-8000
    scores_deep1 {'average_loss': 17423056.0, 'label/mean': 13207.129, 'loss': 269387260.0, 'prediction/mean': 13305.626, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 481584100.0, step = 8001
    INFO:tensorflow:global_step/sec: 1454.74
    INFO:tensorflow:loss = 208849840.0, step = 8101 (0.069 sec)
    INFO:tensorflow:global_step/sec: 2258.56
    INFO:tensorflow:loss = 595580700.0, step = 8201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2404.48
    INFO:tensorflow:loss = 315154940.0, step = 8301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2367.03
    INFO:tensorflow:loss = 342508900.0, step = 8401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2021.59
    INFO:tensorflow:loss = 56060730.0, step = 8501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2417.02
    INFO:tensorflow:loss = 64468564.0, step = 8601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2298.17
    INFO:tensorflow:loss = 77104980.0, step = 8701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2331.22
    INFO:tensorflow:loss = 159009060.0, step = 8801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2263.88
    INFO:tensorflow:loss = 175239940.0, step = 8901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 177209170.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:52
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09426s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:52
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 17124800.0, global_step = 9000, label/mean = 13207.129, loss = 264775760.0, prediction/mean = 13360.295
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-9000
    scores_deep1 {'average_loss': 17124800.0, 'label/mean': 13207.129, 'loss': 264775760.0, 'prediction/mean': 13360.295, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 85342640.0, step = 9001
    INFO:tensorflow:global_step/sec: 1512.49
    INFO:tensorflow:loss = 122623096.0, step = 9101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2357.44
    INFO:tensorflow:loss = 357866620.0, step = 9201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2419.78
    INFO:tensorflow:loss = 218582690.0, step = 9301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2418.72
    INFO:tensorflow:loss = 68170024.0, step = 9401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2257.39
    INFO:tensorflow:loss = 138000220.0, step = 9501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2274.38
    INFO:tensorflow:loss = 232552030.0, step = 9601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2150.81
    INFO:tensorflow:loss = 313161100.0, step = 9701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2398.76
    INFO:tensorflow:loss = 536184400.0, step = 9801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2308.2
    INFO:tensorflow:loss = 232178600.0, step = 9901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 115960270.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:53
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09454s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:53
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 16951908.0, global_step = 10000, label/mean = 13207.129, loss = 262102600.0, prediction/mean = 13054.23
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvce3jk6d/model.ckpt-10000
    scores_deep1 {'average_loss': 16951908.0, 'label/mean': 13207.129, 'loss': 262102600.0, 'prediction/mean': 13054.23, 'global_step': 10000}
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 7090094000.0, step = 1
    INFO:tensorflow:global_step/sec: 1500.31
    INFO:tensorflow:loss = 494838140.0, step = 101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2001.92
    INFO:tensorflow:loss = 251981280.0, step = 201 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2363.61
    INFO:tensorflow:loss = 521555070.0, step = 301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1317.11
    INFO:tensorflow:loss = 223981460.0, step = 401 (0.077 sec)
    INFO:tensorflow:global_step/sec: 2269.37
    INFO:tensorflow:loss = 193330850.0, step = 501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2093.06
    INFO:tensorflow:loss = 169140100.0, step = 601 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1951.45
    INFO:tensorflow:loss = 475062080.0, step = 701 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2030.66
    INFO:tensorflow:loss = 192199550.0, step = 801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1948.72
    INFO:tensorflow:loss = 144885650.0, step = 901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 211257000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:55
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09325s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:55
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 20036336.0, global_step = 1000, label/mean = 13207.129, loss = 309792580.0, prediction/mean = 13192.678
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-1000
    scores_deep2 {'average_loss': 20036336.0, 'label/mean': 13207.129, 'loss': 309792580.0, 'prediction/mean': 13192.678, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 158378180.0, step = 1001
    INFO:tensorflow:global_step/sec: 1390.34
    INFO:tensorflow:loss = 285026560.0, step = 1101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2033.79
    INFO:tensorflow:loss = 814318460.0, step = 1201 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2193.86
    INFO:tensorflow:loss = 105827030.0, step = 1301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2262.8
    INFO:tensorflow:loss = 323191870.0, step = 1401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2415
    INFO:tensorflow:loss = 489346600.0, step = 1501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2190.72
    INFO:tensorflow:loss = 273105100.0, step = 1601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2293.42
    INFO:tensorflow:loss = 261561580.0, step = 1701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1955.37
    INFO:tensorflow:loss = 280401380.0, step = 1801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2100.5
    INFO:tensorflow:loss = 615960800.0, step = 1901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 458250000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09382s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:57
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 18391582.0, global_step = 2000, label/mean = 13207.129, loss = 284362140.0, prediction/mean = 13444.444
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-2000
    scores_deep2 {'average_loss': 18391582.0, 'label/mean': 13207.129, 'loss': 284362140.0, 'prediction/mean': 13444.444, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 369519600.0, step = 2001
    INFO:tensorflow:global_step/sec: 1400.29
    INFO:tensorflow:loss = 210607070.0, step = 2101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2368.27
    INFO:tensorflow:loss = 986795800.0, step = 2201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2044.33
    INFO:tensorflow:loss = 169948380.0, step = 2301 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1959.97
    INFO:tensorflow:loss = 330961470.0, step = 2401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2125.85
    INFO:tensorflow:loss = 636489860.0, step = 2501 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1943.97
    INFO:tensorflow:loss = 598409600.0, step = 2601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2237.19
    INFO:tensorflow:loss = 117569850.0, step = 2701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2391.25
    INFO:tensorflow:loss = 82521620.0, step = 2801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1924.08
    INFO:tensorflow:loss = 125826776.0, step = 2901 (0.053 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 58145690.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:06:58
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09594s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:06:59
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 17465512.0, global_step = 3000, label/mean = 13207.129, loss = 270043680.0, prediction/mean = 13595.98
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-3000
    scores_deep2 {'average_loss': 17465512.0, 'label/mean': 13207.129, 'loss': 270043680.0, 'prediction/mean': 13595.98, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 185604770.0, step = 3001
    INFO:tensorflow:global_step/sec: 1403.04
    INFO:tensorflow:loss = 69055060.0, step = 3101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2057.91
    INFO:tensorflow:loss = 318494340.0, step = 3201 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2337.39
    INFO:tensorflow:loss = 319532860.0, step = 3301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2198.27
    INFO:tensorflow:loss = 385518430.0, step = 3401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2079.61
    INFO:tensorflow:loss = 404738300.0, step = 3501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2278.88
    INFO:tensorflow:loss = 146065140.0, step = 3601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2146.53
    INFO:tensorflow:loss = 485424580.0, step = 3701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2372.93
    INFO:tensorflow:loss = 347286050.0, step = 3801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1955.37
    INFO:tensorflow:loss = 654655940.0, step = 3901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 96449600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:00
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09384s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:00
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 16631732.0, global_step = 4000, label/mean = 13207.129, loss = 257152160.0, prediction/mean = 13260.665
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-4000
    scores_deep2 {'average_loss': 16631732.0, 'label/mean': 13207.129, 'loss': 257152160.0, 'prediction/mean': 13260.665, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 206837900.0, step = 4001
    INFO:tensorflow:global_step/sec: 1393.34
    INFO:tensorflow:loss = 64174560.0, step = 4101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2110.25
    INFO:tensorflow:loss = 217092590.0, step = 4201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1957.21
    INFO:tensorflow:loss = 193442660.0, step = 4301 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1957.94
    INFO:tensorflow:loss = 54793830.0, step = 4401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1906.94
    INFO:tensorflow:loss = 102015380.0, step = 4501 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1958.02
    INFO:tensorflow:loss = 107960680.0, step = 4601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1960.28
    INFO:tensorflow:loss = 199376140.0, step = 4701 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2331.81
    INFO:tensorflow:loss = 85131810.0, step = 4801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1958.98
    INFO:tensorflow:loss = 459461340.0, step = 4901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 673267300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09367s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:02
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 16055291.0, global_step = 5000, label/mean = 13207.129, loss = 248239500.0, prediction/mean = 13622.427
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-5000
    scores_deep2 {'average_loss': 16055291.0, 'label/mean': 13207.129, 'loss': 248239500.0, 'prediction/mean': 13622.427, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 390073280.0, step = 5001
    INFO:tensorflow:global_step/sec: 1561.01
    INFO:tensorflow:loss = 142354510.0, step = 5101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2202.64
    INFO:tensorflow:loss = 305289500.0, step = 5201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2351.95
    INFO:tensorflow:loss = 414740930.0, step = 5301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2309.47
    INFO:tensorflow:loss = 468163170.0, step = 5401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1927.45
    INFO:tensorflow:loss = 118194370.0, step = 5501 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2302.5
    INFO:tensorflow:loss = 142504020.0, step = 5601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2026.02
    INFO:tensorflow:loss = 50566724.0, step = 5701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1957.7
    INFO:tensorflow:loss = 31335892.0, step = 5801 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2389.55
    INFO:tensorflow:loss = 339214430.0, step = 5901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 171567550.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:03
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09391s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:03
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 15419202.0, global_step = 6000, label/mean = 13207.129, loss = 238404590.0, prediction/mean = 13126.41
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-6000
    scores_deep2 {'average_loss': 15419202.0, 'label/mean': 13207.129, 'loss': 238404590.0, 'prediction/mean': 13126.41, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 207683970.0, step = 6001
    INFO:tensorflow:global_step/sec: 1437.73
    INFO:tensorflow:loss = 64899224.0, step = 6101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2427.96
    INFO:tensorflow:loss = 125496024.0, step = 6201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2044.33
    INFO:tensorflow:loss = 121526790.0, step = 6301 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1958.87
    INFO:tensorflow:loss = 222593460.0, step = 6401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2283.25
    INFO:tensorflow:loss = 158059180.0, step = 6501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2043.44
    INFO:tensorflow:loss = 116175680.0, step = 6601 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2032.77
    INFO:tensorflow:loss = 155935780.0, step = 6701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1964.59
    INFO:tensorflow:loss = 106733250.0, step = 6801 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1957.14
    INFO:tensorflow:loss = 410581700.0, step = 6901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 71845980.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:05
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09383s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:05
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 14837309.0, global_step = 7000, label/mean = 13207.129, loss = 229407630.0, prediction/mean = 13325.296
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-7000
    scores_deep2 {'average_loss': 14837309.0, 'label/mean': 13207.129, 'loss': 229407630.0, 'prediction/mean': 13325.296, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 97635100.0, step = 7001
    INFO:tensorflow:global_step/sec: 1376.33
    INFO:tensorflow:loss = 146274110.0, step = 7101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2003.16
    INFO:tensorflow:loss = 135112140.0, step = 7201 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1981.29
    INFO:tensorflow:loss = 164062420.0, step = 7301 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1930.65
    INFO:tensorflow:loss = 78941290.0, step = 7401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1932.51
    INFO:tensorflow:loss = 222898720.0, step = 7501 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2117.08
    INFO:tensorflow:loss = 330950140.0, step = 7601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2340.55
    INFO:tensorflow:loss = 166120000.0, step = 7701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2391.61
    INFO:tensorflow:loss = 72070610.0, step = 7801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1947.19
    INFO:tensorflow:loss = 313267140.0, step = 7901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 126197810.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:06
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09394s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:07
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 14377571.0, global_step = 8000, label/mean = 13207.129, loss = 222299380.0, prediction/mean = 13348.768
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-8000
    scores_deep2 {'average_loss': 14377571.0, 'label/mean': 13207.129, 'loss': 222299380.0, 'prediction/mean': 13348.768, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 114838400.0, step = 8001
    INFO:tensorflow:global_step/sec: 1559.16
    INFO:tensorflow:loss = 203397360.0, step = 8101 (0.064 sec)
    INFO:tensorflow:global_step/sec: 1989.69
    INFO:tensorflow:loss = 171066980.0, step = 8201 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1920.28
    INFO:tensorflow:loss = 66454900.0, step = 8301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1952.7
    INFO:tensorflow:loss = 436118400.0, step = 8401 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1949.54
    INFO:tensorflow:loss = 323209730.0, step = 8501 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1981.11
    INFO:tensorflow:loss = 109288910.0, step = 8601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2042.48
    INFO:tensorflow:loss = 65633024.0, step = 8701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2081.67
    INFO:tensorflow:loss = 286014080.0, step = 8801 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2233.06
    INFO:tensorflow:loss = 121147464.0, step = 8901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 368934270.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:08
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11643s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:08
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 14009647.0, global_step = 9000, label/mean = 13207.129, loss = 216610700.0, prediction/mean = 13115.373
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-9000
    scores_deep2 {'average_loss': 14009647.0, 'label/mean': 13207.129, 'loss': 216610700.0, 'prediction/mean': 13115.373, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 130184940.0, step = 9001
    INFO:tensorflow:global_step/sec: 1430.9
    INFO:tensorflow:loss = 148468640.0, step = 9101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2357.6
    INFO:tensorflow:loss = 107799630.0, step = 9201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1940.16
    INFO:tensorflow:loss = 225478190.0, step = 9301 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2232.45
    INFO:tensorflow:loss = 436617860.0, step = 9401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1604.41
    INFO:tensorflow:loss = 364440930.0, step = 9501 (0.063 sec)
    INFO:tensorflow:global_step/sec: 1939.52
    INFO:tensorflow:loss = 66790256.0, step = 9601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2118.24
    INFO:tensorflow:loss = 111009576.0, step = 9701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2069.63
    INFO:tensorflow:loss = 284546900.0, step = 9801 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1988.91
    INFO:tensorflow:loss = 134926480.0, step = 9901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 113909900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:10
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09613s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:10
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 13641751.0, global_step = 10000, label/mean = 13207.129, loss = 210922460.0, prediction/mean = 13237.663
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfurtv48l/model.ckpt-10000
    scores_deep2 {'average_loss': 13641751.0, 'label/mean': 13207.129, 'loss': 210922460.0, 'prediction/mean': 13237.663, 'global_step': 10000}



```python
# [Change #13]: Optimizer exploration — AdamOptimizer vs Adagrad on numeric features (no normalization)
# Reuses model_feature_columns, train_input_fn, eval_input_fn from Task 1.
#
# Why Adam?
#   Adagrad accumulates squared gradients forever — effective lr shrinks monotonically.
#   Adam uses exponential moving averages of both the gradient (1st moment) and its
#   square (2nd moment), so the denominator can decay, allowing recovery from early
#   large gradients. On small datasets (201 rows) this typically improves convergence
#   speed vs Adagrad (Kingma & Ba, 2015).
#
# lr=0.001 is Adam's standard default — no tuning needed for a first comparison.

# T1.8 — AdamOptimizer (lr=0.001)
est_adam = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=[64],
    optimizer=tf.train.AdamOptimizer(learning_rate=0.001),
)
for _ in range(num_print_statements):
    est_adam.train(train_input_fn, steps=num_training_steps // num_print_statements)
    scores_adam = est_adam.evaluate(eval_input_fn)
    print("scores_adam", scores_adam)

# Results (fill in after running):
# Model    │ Optimizer │  lr   │ avg_loss   │  RMSE
# DNN [64] │ Adagrad   │ 0.01  │ 10,822,464 │ ~$3,290  ← T1 best (reference)
# DNN [64] │ Adam      │ 0.001 │            │

```

    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 4131636200.0, step = 1
    INFO:tensorflow:global_step/sec: 1448.31
    INFO:tensorflow:loss = 1197342500.0, step = 101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2223.16
    INFO:tensorflow:loss = 332461120.0, step = 201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2208.87
    INFO:tensorflow:loss = 577664500.0, step = 301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1864.35
    INFO:tensorflow:loss = 1239014800.0, step = 401 (0.054 sec)
    INFO:tensorflow:global_step/sec: 1990.4
    INFO:tensorflow:loss = 659270460.0, step = 501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2131.15
    INFO:tensorflow:loss = 1029418200.0, step = 601 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2114.8
    INFO:tensorflow:loss = 1279462100.0, step = 701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2142.56
    INFO:tensorflow:loss = 493016860.0, step = 801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2274.32
    INFO:tensorflow:loss = 1077107700.0, step = 901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 415172740.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:12
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11990s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:12
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 33747096.0, global_step = 1000, label/mean = 13207.129, loss = 521782050.0, prediction/mean = 13300.732
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-1000
    scores_adam {'average_loss': 33747096.0, 'label/mean': 13207.129, 'loss': 521782050.0, 'prediction/mean': 13300.732, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 325937440.0, step = 1001
    INFO:tensorflow:global_step/sec: 892.244
    INFO:tensorflow:loss = 792764700.0, step = 1101 (0.113 sec)
    INFO:tensorflow:global_step/sec: 1940.43
    INFO:tensorflow:loss = 588110850.0, step = 1201 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2006.02
    INFO:tensorflow:loss = 619334300.0, step = 1301 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1858.46
    INFO:tensorflow:loss = 165961300.0, step = 1401 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1880.51
    INFO:tensorflow:loss = 195856030.0, step = 1501 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1947.42
    INFO:tensorflow:loss = 258622450.0, step = 1601 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1860.08
    INFO:tensorflow:loss = 172338780.0, step = 1701 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2003.85
    INFO:tensorflow:loss = 133271030.0, step = 1801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1636.37
    INFO:tensorflow:loss = 290063870.0, step = 1901 (0.062 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 350297860.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:14
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09465s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:14
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 20104114.0, global_step = 2000, label/mean = 13207.129, loss = 310840500.0, prediction/mean = 13184.521
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-2000
    scores_adam {'average_loss': 20104114.0, 'label/mean': 13207.129, 'loss': 310840500.0, 'prediction/mean': 13184.521, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 458645100.0, step = 2001
    INFO:tensorflow:global_step/sec: 1378.72
    INFO:tensorflow:loss = 438977600.0, step = 2101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2137.53
    INFO:tensorflow:loss = 169205200.0, step = 2201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2039.15
    INFO:tensorflow:loss = 175523420.0, step = 2301 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2115.42
    INFO:tensorflow:loss = 105852160.0, step = 2401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2264.9
    INFO:tensorflow:loss = 469860480.0, step = 2501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2314.92
    INFO:tensorflow:loss = 175653070.0, step = 2601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2191.45
    INFO:tensorflow:loss = 185148780.0, step = 2701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2243.36
    INFO:tensorflow:loss = 378245630.0, step = 2801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2091.65
    INFO:tensorflow:loss = 111531390.0, step = 2901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 527597500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:16
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09480s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:16
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 18457720.0, global_step = 3000, label/mean = 13207.129, loss = 285384770.0, prediction/mean = 13302.213
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-3000
    scores_adam {'average_loss': 18457720.0, 'label/mean': 13207.129, 'loss': 285384770.0, 'prediction/mean': 13302.213, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 425865600.0, step = 3001
    INFO:tensorflow:global_step/sec: 1356.95
    INFO:tensorflow:loss = 126298870.0, step = 3101 (0.074 sec)
    INFO:tensorflow:global_step/sec: 2341.71
    INFO:tensorflow:loss = 500095900.0, step = 3201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1993.7
    INFO:tensorflow:loss = 637732000.0, step = 3301 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1919.94
    INFO:tensorflow:loss = 130200220.0, step = 3401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1989.41
    INFO:tensorflow:loss = 167917860.0, step = 3501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2265.57
    INFO:tensorflow:loss = 108880820.0, step = 3601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2207.9
    INFO:tensorflow:loss = 59902860.0, step = 3701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2013.86
    INFO:tensorflow:loss = 138183840.0, step = 3801 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2081.12
    INFO:tensorflow:loss = 554153600.0, step = 3901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 347883070.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:17
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09671s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:17
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 17417744.0, global_step = 4000, label/mean = 13207.129, loss = 269305120.0, prediction/mean = 12901.45
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-4000
    scores_adam {'average_loss': 17417744.0, 'label/mean': 13207.129, 'loss': 269305120.0, 'prediction/mean': 12901.45, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 70808330.0, step = 4001
    INFO:tensorflow:global_step/sec: 1371.52
    INFO:tensorflow:loss = 128870940.0, step = 4101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 1860.74
    INFO:tensorflow:loss = 178418600.0, step = 4201 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2002.51
    INFO:tensorflow:loss = 830214400.0, step = 4301 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2212.5
    INFO:tensorflow:loss = 418443260.0, step = 4401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2282.17
    INFO:tensorflow:loss = 199525180.0, step = 4501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2316.14
    INFO:tensorflow:loss = 56447884.0, step = 4601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2359.21
    INFO:tensorflow:loss = 539735400.0, step = 4701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1994.74
    INFO:tensorflow:loss = 382063300.0, step = 4801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2289.2
    INFO:tensorflow:loss = 150327540.0, step = 4901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 445760670.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:19
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09285s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:19
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 16133445.0, global_step = 5000, label/mean = 13207.129, loss = 249447870.0, prediction/mean = 13062.104
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-5000
    scores_adam {'average_loss': 16133445.0, 'label/mean': 13207.129, 'loss': 249447870.0, 'prediction/mean': 13062.104, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 839731840.0, step = 5001
    INFO:tensorflow:global_step/sec: 1403.21
    INFO:tensorflow:loss = 518776830.0, step = 5101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 1887.97
    INFO:tensorflow:loss = 504403140.0, step = 5201 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1899.11
    INFO:tensorflow:loss = 187802340.0, step = 5301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2178.56
    INFO:tensorflow:loss = 199855730.0, step = 5401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1921.6
    INFO:tensorflow:loss = 483387330.0, step = 5501 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2229.1
    INFO:tensorflow:loss = 324984860.0, step = 5601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1407.94
    INFO:tensorflow:loss = 146104580.0, step = 5701 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2339.67
    INFO:tensorflow:loss = 100313144.0, step = 5801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1836.21
    INFO:tensorflow:loss = 210297700.0, step = 5901 (0.054 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 153900540.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:20
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09349s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:21
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 15024997.0, global_step = 6000, label/mean = 13207.129, loss = 232309570.0, prediction/mean = 13422.854
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-6000
    scores_adam {'average_loss': 15024997.0, 'label/mean': 13207.129, 'loss': 232309570.0, 'prediction/mean': 13422.854, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 524337730.0, step = 6001
    INFO:tensorflow:global_step/sec: 1357.85
    INFO:tensorflow:loss = 263423230.0, step = 6101 (0.074 sec)
    INFO:tensorflow:global_step/sec: 2288.91
    INFO:tensorflow:loss = 275285400.0, step = 6201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1873.89
    INFO:tensorflow:loss = 131535890.0, step = 6301 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2001.92
    INFO:tensorflow:loss = 77408410.0, step = 6401 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1945.29
    INFO:tensorflow:loss = 115446480.0, step = 6501 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1913.73
    INFO:tensorflow:loss = 112488420.0, step = 6601 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1983.54
    INFO:tensorflow:loss = 176045150.0, step = 6701 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1778.02
    INFO:tensorflow:loss = 480570800.0, step = 6801 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1872.98
    INFO:tensorflow:loss = 484541540.0, step = 6901 (0.053 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 116738880.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11107s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:22
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 14115017.0, global_step = 7000, label/mean = 13207.129, loss = 218239890.0, prediction/mean = 13256.011
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-7000
    scores_adam {'average_loss': 14115017.0, 'label/mean': 13207.129, 'loss': 218239890.0, 'prediction/mean': 13256.011, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 373379740.0, step = 7001
    INFO:tensorflow:global_step/sec: 1292.21
    INFO:tensorflow:loss = 189768020.0, step = 7101 (0.078 sec)
    INFO:tensorflow:global_step/sec: 2035
    INFO:tensorflow:loss = 94848824.0, step = 7201 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1373.27
    INFO:tensorflow:loss = 190982880.0, step = 7301 (0.072 sec)
    INFO:tensorflow:global_step/sec: 1933.6
    INFO:tensorflow:loss = 268110940.0, step = 7401 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1905.96
    INFO:tensorflow:loss = 192702080.0, step = 7501 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1956.96
    INFO:tensorflow:loss = 157975180.0, step = 7601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1902.87
    INFO:tensorflow:loss = 130984420.0, step = 7701 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1729.51
    INFO:tensorflow:loss = 151031000.0, step = 7801 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1970.63
    INFO:tensorflow:loss = 247960380.0, step = 7901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 191344900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:24
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10452s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:24
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 13542818.0, global_step = 8000, label/mean = 13207.129, loss = 209392800.0, prediction/mean = 12881.844
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-8000
    scores_adam {'average_loss': 13542818.0, 'label/mean': 13207.129, 'loss': 209392800.0, 'prediction/mean': 12881.844, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 122365200.0, step = 8001
    INFO:tensorflow:global_step/sec: 1456.48
    INFO:tensorflow:loss = 94836260.0, step = 8101 (0.069 sec)
    INFO:tensorflow:global_step/sec: 2306.86
    INFO:tensorflow:loss = 243301330.0, step = 8201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2153.08
    INFO:tensorflow:loss = 158738220.0, step = 8301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2308.79
    INFO:tensorflow:loss = 159017180.0, step = 8401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2128.84
    INFO:tensorflow:loss = 144881760.0, step = 8501 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2116.75
    INFO:tensorflow:loss = 176955180.0, step = 8601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2344.89
    INFO:tensorflow:loss = 125791770.0, step = 8701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2250.94
    INFO:tensorflow:loss = 225316380.0, step = 8801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2242.09
    INFO:tensorflow:loss = 53728104.0, step = 8901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 212062300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:25
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09406s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:25
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 12877006.0, global_step = 9000, label/mean = 13207.129, loss = 199098340.0, prediction/mean = 13200.527
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-9000
    scores_adam {'average_loss': 12877006.0, 'label/mean': 13207.129, 'loss': 199098340.0, 'prediction/mean': 13200.527, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 280211650.0, step = 9001
    INFO:tensorflow:global_step/sec: 1437.94
    INFO:tensorflow:loss = 146115230.0, step = 9101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2028.93
    INFO:tensorflow:loss = 140009000.0, step = 9201 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2285.24
    INFO:tensorflow:loss = 297612350.0, step = 9301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2201.01
    INFO:tensorflow:loss = 264165380.0, step = 9401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2178.3
    INFO:tensorflow:loss = 147677000.0, step = 9501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2360.45
    INFO:tensorflow:loss = 267116460.0, step = 9601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1908.72
    INFO:tensorflow:loss = 70730696.0, step = 9701 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2226.73
    INFO:tensorflow:loss = 352974000.0, step = 9801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1930.28
    INFO:tensorflow:loss = 162785890.0, step = 9901 (0.051 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 115021290.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T17:07:27
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09502s
    INFO:tensorflow:Finished evaluation at 2026-04-03-17:07:27
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 12662486.0, global_step = 10000, label/mean = 13207.129, loss = 195781520.0, prediction/mean = 12851.8125
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp5q6ugfhj/model.ckpt-10000
    scores_adam {'average_loss': 12662486.0, 'label/mean': 13207.129, 'loss': 195781520.0, 'prediction/mean': 12851.8125, 'global_step': 10000}


### Task 2: Take best numeric model from earlier. Add normalization.

#### Adding normalization to best numeric model from earlier

- Decide what type of normalization to add, and for which features
- Use the `normalizer_fn` arg on [`numeric_column`]
- You will need to retune the hyperparameters from earlier.


**Does normalization improve model quality on this dataset? Why or why not?**

#### Training model with numeric features + normalization


```python
## [Change #7]: Added this section to outline the next steps for Task 2.
# epsilon is used in the normalizer_fn to prevent division by zero in case of zero std deviation or zero range.
epsilon = 0.000001

# Task 2.1 config (batch=16, hidden=[64], lr=0.01, Adagrad) + Z-score →baseline comparison
model_feature_columns_zscore = [
    tf.feature_column.numeric_column(feature_name,
                                    #  normalizer_fn=lambda val: (val - x_df.mean()[feature_name]) / (epsilon + x_df.std()[feature_name]))
                                    normalizer_fn=lambda val, fn=feature_name: (val - x_df.mean()[fn]) / (epsilon + x_df.std()[fn]))
    for feature_name in numeric_feature_names
]
print('model_feature_columns_zscore', model_feature_columns_zscore)

est_zscore = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns_zscore,
    hidden_units=hidden_units_parameter,
    optimizer=optimizer_parameter,
  )

# Task 2.2 config (batch=16, hidden=[64], lr=0.01, Adagrad) + Min-max normalization →baseline comparison
model_feature_columns_minmax = [
    tf.feature_column.numeric_column(feature_name,
                                    #  normalizer_fn=lambda val: (val - x_df[feature_name].min()) / (epsilon + x_df[feature_name].max() - x_df[feature_name].min()))
                                    normalizer_fn=lambda val, fn=feature_name: (val - x_df[fn].min()) / (epsilon + x_df[fn].max() - x_df[fn].min()))
    for feature_name in numeric_feature_names
]
print('model_feature_columns_minmax', model_feature_columns_minmax)

est_minmax = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns_minmax,
    hidden_units=hidden_units_parameter,
    optimizer=optimizer_parameter,
  )

# TRAIN and EVAL Task 2.1 and Task 2.2 → compare results with Task 2.3
# - Run the same training loop for est_zscore and est_minmax as we did for
#   est, and print out the scores for each. 
num_print_statements = 10
num_training_steps = 10000

# Task 2.1 - Z-score normalization
for _ in range(num_print_statements):
  est_zscore.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_zscore = est_zscore.evaluate(eval_input_fn)
  print('scores_zscore', scores_zscore)

# Task 2.2 - Min-max normalization
for _ in range(num_print_statements):
  est_minmax.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_minmax = est_minmax.evaluate(eval_input_fn)
  print('scores_minmax', scores_minmax)

# → pick the winner of 2.1 vs 2.2 based on final avg_loss and RMSE

# Task 2.3: GradientDescentOptimizer + Z-score normalization to answers the lab's embedded question
# Hypothesis: with balanced gradients (Z-score), plain GD may now converge.
# lr=0.01 is too small for GD — using 0.5 to compensate for smaller gradient magnitudes post-normalisation.

# Task 2.4: Feature Engineering with PCA to explore dimensionality reduction as an alternative 
# to normalization for handling scale variance and improving convergence.
'''
cell blocks below has details for Task 2.3 and Task 2.4
'''
```

    model_feature_columns_zscore [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17e67b520>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17e62fd90>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17e55d750>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17e50dfc0>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17e4ca830>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17c586f80>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17c587640>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17c587f40>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17c587d00>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13fb50>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13eb00>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f9a0>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e950>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13ff40>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13fe20>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    model_feature_columns_minmax [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f7f0>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f640>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13ea70>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e9e0>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e8c0>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e830>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e5f0>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13fbe0>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13fa30>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f880>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f6d0>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13f490>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e560>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e4d0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x17b13e440>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 3227795000.0, step = 1
    INFO:tensorflow:global_step/sec: 1521.51
    INFO:tensorflow:loss = 1995706200.0, step = 101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2194.39
    INFO:tensorflow:loss = 2581473300.0, step = 201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2330.95
    INFO:tensorflow:loss = 2553911800.0, step = 301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2247.34
    INFO:tensorflow:loss = 3031851000.0, step = 401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2468.17
    INFO:tensorflow:loss = 3617760300.0, step = 501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2283.41
    INFO:tensorflow:loss = 3831916000.0, step = 601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2304.79
    INFO:tensorflow:loss = 4118789000.0, step = 701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2334.06
    INFO:tensorflow:loss = 8143354400.0, step = 801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2482.85
    INFO:tensorflow:loss = 2595260400.0, step = 901 (0.041 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 4608072000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09626s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:39
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 232978240.0, global_step = 1000, label/mean = 13207.129, loss = 3602202000.0, prediction/mean = 129.58905
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-1000
    scores_zscore {'average_loss': 232978240.0, 'label/mean': 13207.129, 'loss': 3602202000.0, 'prediction/mean': 129.58905, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 3163829200.0, step = 1001
    INFO:tensorflow:global_step/sec: 1481.53
    INFO:tensorflow:loss = 2630648300.0, step = 1101 (0.069 sec)
    INFO:tensorflow:global_step/sec: 2296.25
    INFO:tensorflow:loss = 4415191600.0, step = 1201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2212.24
    INFO:tensorflow:loss = 2499320800.0, step = 1301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2337.75
    INFO:tensorflow:loss = 2313998000.0, step = 1401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2362.91
    INFO:tensorflow:loss = 4266482000.0, step = 1501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2423.82
    INFO:tensorflow:loss = 3808734200.0, step = 1601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2317.38
    INFO:tensorflow:loss = 2582999000.0, step = 1701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2184.56
    INFO:tensorflow:loss = 4184366600.0, step = 1801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2356.72
    INFO:tensorflow:loss = 3446043600.0, step = 1901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 5134809600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:41
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10236s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:41
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 228216220.0, global_step = 2000, label/mean = 13207.129, loss = 3528574000.0, prediction/mean = 272.74252
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-2000
    scores_zscore {'average_loss': 228216220.0, 'label/mean': 13207.129, 'loss': 3528574000.0, 'prediction/mean': 272.74252, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2078030300.0, step = 2001
    INFO:tensorflow:global_step/sec: 1399.72
    INFO:tensorflow:loss = 6684398600.0, step = 2101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2427.82
    INFO:tensorflow:loss = 3959319600.0, step = 2201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2256.77
    INFO:tensorflow:loss = 3378825700.0, step = 2301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1967.82
    INFO:tensorflow:loss = 3157236700.0, step = 2401 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2446.06
    INFO:tensorflow:loss = 2895277600.0, step = 2501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2180.6
    INFO:tensorflow:loss = 3540884500.0, step = 2601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2404.36
    INFO:tensorflow:loss = 2120080300.0, step = 2701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2249
    INFO:tensorflow:loss = 5818807300.0, step = 2801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2130.93
    INFO:tensorflow:loss = 3792995600.0, step = 2901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 4997153000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:42
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09682s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:43
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 223472770.0, global_step = 3000, label/mean = 13207.129, loss = 3455232800.0, prediction/mean = 415.77942
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-3000
    scores_zscore {'average_loss': 223472770.0, 'label/mean': 13207.129, 'loss': 3455232800.0, 'prediction/mean': 415.77942, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 2459250700.0, step = 3001
    INFO:tensorflow:global_step/sec: 1347.27
    INFO:tensorflow:loss = 2961327000.0, step = 3101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2187.94
    INFO:tensorflow:loss = 4039485400.0, step = 3201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2199.94
    INFO:tensorflow:loss = 1594309600.0, step = 3301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2155.49
    INFO:tensorflow:loss = 4736258000.0, step = 3401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2065.44
    INFO:tensorflow:loss = 5237991000.0, step = 3501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1721.5
    INFO:tensorflow:loss = 4388744700.0, step = 3601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 786.194
    INFO:tensorflow:loss = 2374746600.0, step = 3701 (0.127 sec)
    INFO:tensorflow:global_step/sec: 1875.71
    INFO:tensorflow:loss = 3174005200.0, step = 3801 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2316.96
    INFO:tensorflow:loss = 3226389000.0, step = 3901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 3086372400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09758s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:44
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 218784640.0, global_step = 4000, label/mean = 13207.129, loss = 3382747100.0, prediction/mean = 557.6714
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-4000
    scores_zscore {'average_loss': 218784640.0, 'label/mean': 13207.129, 'loss': 3382747100.0, 'prediction/mean': 557.6714, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 1836838400.0, step = 4001
    INFO:tensorflow:global_step/sec: 1407.48
    INFO:tensorflow:loss = 3334444500.0, step = 4101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2249.52
    INFO:tensorflow:loss = 2763768300.0, step = 4201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2338.47
    INFO:tensorflow:loss = 7401947000.0, step = 4301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2144.99
    INFO:tensorflow:loss = 4763294700.0, step = 4401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2092.11
    INFO:tensorflow:loss = 5295110000.0, step = 4501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2253.77
    INFO:tensorflow:loss = 2357154800.0, step = 4601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2375.58
    INFO:tensorflow:loss = 3673275400.0, step = 4701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2152.89
    INFO:tensorflow:loss = 2469611000.0, step = 4801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2358.99
    INFO:tensorflow:loss = 4054808600.0, step = 4901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 3244690200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:46
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09674s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:46
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 214186910.0, global_step = 5000, label/mean = 13207.129, loss = 3311659300.0, prediction/mean = 698.05365
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-5000
    scores_zscore {'average_loss': 214186910.0, 'label/mean': 13207.129, 'loss': 3311659300.0, 'prediction/mean': 698.05365, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 1689526000.0, step = 5001
    INFO:tensorflow:global_step/sec: 1507.93
    INFO:tensorflow:loss = 3249511200.0, step = 5101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2122.38
    INFO:tensorflow:loss = 3945123600.0, step = 5201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2084.46
    INFO:tensorflow:loss = 3447213800.0, step = 5301 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2284.73
    INFO:tensorflow:loss = 1813545700.0, step = 5401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2282.42
    INFO:tensorflow:loss = 6449525000.0, step = 5501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2357.16
    INFO:tensorflow:loss = 1407871500.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2415.75
    INFO:tensorflow:loss = 4915648500.0, step = 5701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2294.64
    INFO:tensorflow:loss = 1659102500.0, step = 5801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2057.99
    INFO:tensorflow:loss = 4418903000.0, step = 5901 (0.049 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 3199325700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:47
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09554s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:47
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 209648080.0, global_step = 6000, label/mean = 13207.129, loss = 3241481700.0, prediction/mean = 837.62274
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-6000
    scores_zscore {'average_loss': 209648080.0, 'label/mean': 13207.129, 'loss': 3241481700.0, 'prediction/mean': 837.62274, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 3391262700.0, step = 6001
    INFO:tensorflow:global_step/sec: 1337.12
    INFO:tensorflow:loss = 2866826200.0, step = 6101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2434.92
    INFO:tensorflow:loss = 3438751000.0, step = 6201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2234.78
    INFO:tensorflow:loss = 2985640200.0, step = 6301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2168.63
    INFO:tensorflow:loss = 3000367400.0, step = 6401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2056.47
    INFO:tensorflow:loss = 2843705000.0, step = 6501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2439.67
    INFO:tensorflow:loss = 3773091300.0, step = 6601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2252.41
    INFO:tensorflow:loss = 3899072500.0, step = 6701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2128.88
    INFO:tensorflow:loss = 1435256000.0, step = 6801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2441.59
    INFO:tensorflow:loss = 4095225000.0, step = 6901 (0.041 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 1703611300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:49
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09573s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:49
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 205177040.0, global_step = 7000, label/mean = 13207.129, loss = 3172352500.0, prediction/mean = 976.5386
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-7000
    scores_zscore {'average_loss': 205177040.0, 'label/mean': 13207.129, 'loss': 3172352500.0, 'prediction/mean': 976.5386, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 2631589600.0, step = 7001
    INFO:tensorflow:global_step/sec: 1481.33
    INFO:tensorflow:loss = 2962697700.0, step = 7101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2132.34
    INFO:tensorflow:loss = 2956949000.0, step = 7201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2219.76
    INFO:tensorflow:loss = 2541273600.0, step = 7301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2279.87
    INFO:tensorflow:loss = 1737163400.0, step = 7401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2432.03
    INFO:tensorflow:loss = 1462503400.0, step = 7501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2415.39
    INFO:tensorflow:loss = 4452904400.0, step = 7601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2114.31
    INFO:tensorflow:loss = 3927818000.0, step = 7701 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2173.77
    INFO:tensorflow:loss = 2803525400.0, step = 7801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2396.35
    INFO:tensorflow:loss = 1896296700.0, step = 7901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 3780349000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:51
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09559s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:51
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 200748460.0, global_step = 8000, label/mean = 13207.129, loss = 3103880200.0, prediction/mean = 1116.7444
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-8000
    scores_zscore {'average_loss': 200748460.0, 'label/mean': 13207.129, 'loss': 3103880200.0, 'prediction/mean': 1116.7444, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 3070263300.0, step = 8001
    INFO:tensorflow:global_step/sec: 1434.22
    INFO:tensorflow:loss = 4787546600.0, step = 8101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2132.8
    INFO:tensorflow:loss = 3682269200.0, step = 8201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2180.97
    INFO:tensorflow:loss = 3301548500.0, step = 8301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2064.53
    INFO:tensorflow:loss = 4144569300.0, step = 8401 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2146.12
    INFO:tensorflow:loss = 5679082000.0, step = 8501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2112.2
    INFO:tensorflow:loss = 2329474800.0, step = 8601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1994.77
    INFO:tensorflow:loss = 2323651300.0, step = 8701 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2388.8
    INFO:tensorflow:loss = 4625655300.0, step = 8801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2280.98
    INFO:tensorflow:loss = 2643412500.0, step = 8901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 2641208800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:52
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09541s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:52
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 196402880.0, global_step = 9000, label/mean = 13207.129, loss = 3036690700.0, prediction/mean = 1256.0472
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-9000
    scores_zscore {'average_loss': 196402880.0, 'label/mean': 13207.129, 'loss': 3036690700.0, 'prediction/mean': 1256.0472, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 4539393000.0, step = 9001
    INFO:tensorflow:global_step/sec: 1425.45
    INFO:tensorflow:loss = 3333264400.0, step = 9101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2197.81
    INFO:tensorflow:loss = 3545617400.0, step = 9201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1957.56
    INFO:tensorflow:loss = 2032281200.0, step = 9301 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2225.19
    INFO:tensorflow:loss = 2762028500.0, step = 9401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2265.51
    INFO:tensorflow:loss = 1570628100.0, step = 9501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2180.37
    INFO:tensorflow:loss = 1517193700.0, step = 9601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2288.69
    INFO:tensorflow:loss = 3737949400.0, step = 9701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2281.34
    INFO:tensorflow:loss = 2802164700.0, step = 9801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2375.58
    INFO:tensorflow:loss = 2318275600.0, step = 9901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 4463257600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09595s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:54
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 192143300.0, global_step = 10000, label/mean = 13207.129, loss = 2970831000.0, prediction/mean = 1394.1438
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpefu74uht/model.ckpt-10000
    scores_zscore {'average_loss': 192143300.0, 'label/mean': 13207.129, 'loss': 2970831000.0, 'prediction/mean': 1394.1438, 'global_step': 10000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 4553334000.0, step = 1
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 32 vs previous value: 32. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    INFO:tensorflow:global_step/sec: 792.79
    INFO:tensorflow:loss = 4445100000.0, step = 101 (0.127 sec)
    INFO:tensorflow:global_step/sec: 2082.76
    INFO:tensorflow:loss = 3802730000.0, step = 201 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2067
    INFO:tensorflow:loss = 1913286100.0, step = 301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2189.63
    INFO:tensorflow:loss = 3031078100.0, step = 401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1980.44
    INFO:tensorflow:loss = 2866782200.0, step = 501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2273.87
    INFO:tensorflow:loss = 2037503500.0, step = 601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2196.4
    INFO:tensorflow:loss = 3264907300.0, step = 701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2114.34
    INFO:tensorflow:loss = 3222431700.0, step = 801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2121.84
    INFO:tensorflow:loss = 6379778600.0, step = 901 (0.047 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 2192969200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:56
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09943s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:56
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 231536240.0, global_step = 1000, label/mean = 13207.129, loss = 3579906600.0, prediction/mean = 206.57153
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-1000
    scores_minmax {'average_loss': 231536240.0, 'label/mean': 13207.129, 'loss': 3579906600.0, 'prediction/mean': 206.57153, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 7247201300.0, step = 1001
    INFO:tensorflow:global_step/sec: 1145.67
    INFO:tensorflow:loss = 2944647400.0, step = 1101 (0.085 sec)
    INFO:tensorflow:global_step/sec: 2304.37
    INFO:tensorflow:loss = 2159559200.0, step = 1201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2163.75
    INFO:tensorflow:loss = 5500589000.0, step = 1301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1900.12
    INFO:tensorflow:loss = 4511936000.0, step = 1401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2383.68
    INFO:tensorflow:loss = 3437321200.0, step = 1501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2185.56
    INFO:tensorflow:loss = 2473846300.0, step = 1601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2402.51
    INFO:tensorflow:loss = 4420741000.0, step = 1701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2136.79
    INFO:tensorflow:loss = 2680383500.0, step = 1801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2287.51
    INFO:tensorflow:loss = 3584015400.0, step = 1901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 2259323000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:58
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09865s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:58
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 226066800.0, global_step = 2000, label/mean = 13207.129, loss = 3495340500.0, prediction/mean = 406.66852
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-2000
    scores_minmax {'average_loss': 226066800.0, 'label/mean': 13207.129, 'loss': 3495340500.0, 'prediction/mean': 406.66852, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 5376226300.0, step = 2001
    INFO:tensorflow:global_step/sec: 588.852
    INFO:tensorflow:loss = 3357006300.0, step = 2101 (0.170 sec)
    INFO:tensorflow:global_step/sec: 2319.97
    INFO:tensorflow:loss = 2209456000.0, step = 2201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2319.06
    INFO:tensorflow:loss = 3097553400.0, step = 2301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2403.21
    INFO:tensorflow:loss = 3096068600.0, step = 2401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2247.17
    INFO:tensorflow:loss = 5926417400.0, step = 2501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2072.55
    INFO:tensorflow:loss = 1508095000.0, step = 2601 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1955.68
    INFO:tensorflow:loss = 1862554600.0, step = 2701 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2222.62
    INFO:tensorflow:loss = 2107038500.0, step = 2801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2426.25
    INFO:tensorflow:loss = 4380902000.0, step = 2901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 1675805400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:27:59
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10730s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:27:59
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 220735620.0, global_step = 3000, label/mean = 13207.129, loss = 3412912400.0, prediction/mean = 604.637
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-3000
    scores_minmax {'average_loss': 220735620.0, 'label/mean': 13207.129, 'loss': 3412912400.0, 'prediction/mean': 604.637, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 3570507000.0, step = 3001
    INFO:tensorflow:global_step/sec: 1319.12
    INFO:tensorflow:loss = 5577387000.0, step = 3101 (0.077 sec)
    INFO:tensorflow:global_step/sec: 2232.56
    INFO:tensorflow:loss = 2299129600.0, step = 3201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2057.77
    INFO:tensorflow:loss = 3199267800.0, step = 3301 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2201.64
    INFO:tensorflow:loss = 2689746200.0, step = 3401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2235.33
    INFO:tensorflow:loss = 2602402600.0, step = 3501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2214.15
    INFO:tensorflow:loss = 5651629000.0, step = 3601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2296.52
    INFO:tensorflow:loss = 2909186600.0, step = 3701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2259.38
    INFO:tensorflow:loss = 4714234000.0, step = 3801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2383.01
    INFO:tensorflow:loss = 1892519200.0, step = 3901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 4325721600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:01
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11258s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:01
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 215526160.0, global_step = 4000, label/mean = 13207.129, loss = 3332366000.0, prediction/mean = 800.9941
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-4000
    scores_minmax {'average_loss': 215526160.0, 'label/mean': 13207.129, 'loss': 3332366000.0, 'prediction/mean': 800.9941, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 4636751400.0, step = 4001
    INFO:tensorflow:global_step/sec: 1349.47
    INFO:tensorflow:loss = 2715454500.0, step = 4101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2372.09
    INFO:tensorflow:loss = 4474642000.0, step = 4201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2154.1
    INFO:tensorflow:loss = 3465191400.0, step = 4301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2261.73
    INFO:tensorflow:loss = 3933554700.0, step = 4401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2196.75
    INFO:tensorflow:loss = 2541934600.0, step = 4501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2170.56
    INFO:tensorflow:loss = 2538250200.0, step = 4601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2070.77
    INFO:tensorflow:loss = 4783450000.0, step = 4701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2286.82
    INFO:tensorflow:loss = 1971006800.0, step = 4801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2040.82
    INFO:tensorflow:loss = 3894800000.0, step = 4901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 2882810000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:03
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10183s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:03
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 210441900.0, global_step = 5000, label/mean = 13207.129, loss = 3253755600.0, prediction/mean = 995.53546
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-5000
    scores_minmax {'average_loss': 210441900.0, 'label/mean': 13207.129, 'loss': 3253755600.0, 'prediction/mean': 995.53546, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 4967492600.0, step = 5001
    INFO:tensorflow:global_step/sec: 1401.17
    INFO:tensorflow:loss = 4425624600.0, step = 5101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2483.92
    INFO:tensorflow:loss = 3354596000.0, step = 5201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2361.01
    INFO:tensorflow:loss = 3353476600.0, step = 5301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2162.25
    INFO:tensorflow:loss = 4990527500.0, step = 5401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2402.51
    INFO:tensorflow:loss = 3889606700.0, step = 5501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2321.16
    INFO:tensorflow:loss = 3884293000.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2392.07
    INFO:tensorflow:loss = 3549995000.0, step = 5701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2320.56
    INFO:tensorflow:loss = 2333379000.0, step = 5801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2331.27
    INFO:tensorflow:loss = 5250700300.0, step = 5901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 2153117700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:04
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09676s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:04
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 205473540.0, global_step = 6000, label/mean = 13207.129, loss = 3176937000.0, prediction/mean = 1188.5481
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-6000
    scores_minmax {'average_loss': 205473540.0, 'label/mean': 13207.129, 'loss': 3176937000.0, 'prediction/mean': 1188.5481, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 1536130600.0, step = 6001
    INFO:tensorflow:global_step/sec: 1533.25
    INFO:tensorflow:loss = 4498168000.0, step = 6101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2380.54
    INFO:tensorflow:loss = 3528313600.0, step = 6201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2435.18
    INFO:tensorflow:loss = 2224330800.0, step = 6301 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2120.08
    INFO:tensorflow:loss = 3526836200.0, step = 6401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2274.27
    INFO:tensorflow:loss = 4526459000.0, step = 6501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2253.11
    INFO:tensorflow:loss = 1526715100.0, step = 6601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2225.99
    INFO:tensorflow:loss = 4472866300.0, step = 6701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2271.94
    INFO:tensorflow:loss = 1751228000.0, step = 6801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2287.92
    INFO:tensorflow:loss = 3980123400.0, step = 6901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 3498799600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:06
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10100s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:06
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 200628580.0, global_step = 7000, label/mean = 13207.129, loss = 3102026500.0, prediction/mean = 1379.6613
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-7000
    scores_minmax {'average_loss': 200628580.0, 'label/mean': 13207.129, 'loss': 3102026500.0, 'prediction/mean': 1379.6613, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 3414478800.0, step = 7001
    INFO:tensorflow:global_step/sec: 1296.14
    INFO:tensorflow:loss = 4614067000.0, step = 7101 (0.078 sec)
    INFO:tensorflow:global_step/sec: 2372.87
    INFO:tensorflow:loss = 2587561700.0, step = 7201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2179.65
    INFO:tensorflow:loss = 2348044300.0, step = 7301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2097.71
    INFO:tensorflow:loss = 2691150800.0, step = 7401 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2454.23
    INFO:tensorflow:loss = 3061585700.0, step = 7501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2407.85
    INFO:tensorflow:loss = 6798165000.0, step = 7601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2407.19
    INFO:tensorflow:loss = 2521064000.0, step = 7701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2363.08
    INFO:tensorflow:loss = 2243060500.0, step = 7801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2149.83
    INFO:tensorflow:loss = 4815791000.0, step = 7901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 2569850600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:07
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09852s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:08
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 195899250.0, global_step = 8000, label/mean = 13207.129, loss = 3028903700.0, prediction/mean = 1569.101
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-8000
    scores_minmax {'average_loss': 195899250.0, 'label/mean': 13207.129, 'loss': 3028903700.0, 'prediction/mean': 1569.101, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 3954461700.0, step = 8001
    INFO:tensorflow:global_step/sec: 1479.66
    INFO:tensorflow:loss = 3109755000.0, step = 8101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2289.95
    INFO:tensorflow:loss = 5992079400.0, step = 8201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2159.03
    INFO:tensorflow:loss = 3928689200.0, step = 8301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2301.97
    INFO:tensorflow:loss = 3061497300.0, step = 8401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1972.82
    INFO:tensorflow:loss = 3015432700.0, step = 8501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2323.91
    INFO:tensorflow:loss = 3830019800.0, step = 8601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2283.36
    INFO:tensorflow:loss = 918558460.0, step = 8701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2144.08
    INFO:tensorflow:loss = 1609484300.0, step = 8801 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2242.06
    INFO:tensorflow:loss = 4149076700.0, step = 8901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 1924786800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:09
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10295s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:09
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 191291180.0, global_step = 9000, label/mean = 13207.129, loss = 2957656000.0, prediction/mean = 1756.5621
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-9000
    scores_minmax {'average_loss': 191291180.0, 'label/mean': 13207.129, 'loss': 2957656000.0, 'prediction/mean': 1756.5621, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 2855544800.0, step = 9001
    INFO:tensorflow:global_step/sec: 1404.24
    INFO:tensorflow:loss = 2509020200.0, step = 9101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2228.12
    INFO:tensorflow:loss = 1742415700.0, step = 9201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2289.79
    INFO:tensorflow:loss = 3871083500.0, step = 9301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2039.52
    INFO:tensorflow:loss = 1444026000.0, step = 9401 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2073.11
    INFO:tensorflow:loss = 3762825500.0, step = 9501 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2093.75
    INFO:tensorflow:loss = 5101354000.0, step = 9601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2225.39
    INFO:tensorflow:loss = 2352405000.0, step = 9701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2240.39
    INFO:tensorflow:loss = 3490497500.0, step = 9801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2451.03
    INFO:tensorflow:loss = 2351283700.0, step = 9901 (0.041 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 3587883500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:11
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09731s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:11
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 186784880.0, global_step = 10000, label/mean = 13207.129, loss = 2887981600.0, prediction/mean = 1942.7328
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpevqrq0mr/model.ckpt-10000
    scores_minmax {'average_loss': 186784880.0, 'label/mean': 13207.129, 'loss': 2887981600.0, 'prediction/mean': 1942.7328, 'global_step': 10000}





    '\ncell blocks below has details for Task 2.3 and Task 2.4\n'




```python
# Task 2.3: GradientDescentOptimizer + Z-score normalization
est_gd = tf.estimator.DNNRegressor(                                           
    feature_columns=model_feature_columns_zscore,  # ← normalized, not raw    
    hidden_units=hidden_units_parameter,
    optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.0001)            
)                                                                             
num_print_statements = 10
num_training_steps = 10000                                                    

# This for loop has been commented out to prevent the NaN loss error from crashing the notebook. 
# You can uncomment it to see the results, but be aware that it will likely produce NaN losses due to the reasons explained in the comments.
# for _ in range(num_print_statements):
#     est_gd.train(train_input_fn, steps=num_training_steps // num_print_statements)                                                         
#     scores_gd = est_gd.evaluate(eval_input_fn)
#     print('scores_gd', scores_gd)

# Problem with Task 2.3: GradientDescentOptimizer + Z-score normalization
'''
ERROR:tensorflow:Model diverged with loss = NaN.
'''
```

    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpeict4mh5
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpeict4mh5', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}





    '\nERROR:tensorflow:Model diverged with loss = NaN.\n'




```python
# [Change #8]: # Task 2.4: Feature Engineering with PCA + Adagrad

# The 15 numeric features are heavily correlated:
# engine-size, horsepower, weight, length -> all move together. 
# PCA merges that redundancy into orthogonal components. 
# With ~95% variance explained we'll likely get 5–7 components instead of 15.

# Implementation note: PCA doesn't fit into normalizer_fn. I'm doing it outside TF

from sklearn.preprocessing import StandardScaler  
from sklearn.decomposition import PCA

scaler = StandardScaler()
pca = PCA(n_components=0.95)  # keep 95% variance

X_scaled = scaler.fit_transform(car_data[numeric_feature_names])  # → 15 columns
X_pca = pca.fit_transform(X_scaled)   # → n_components columns

# Then build numeric_column for each PC
pc_names = [f'PC{i+1}' for i in range(X_pca.shape[1])]
x_df_pca = pd.DataFrame(X_pca, columns=pc_names)
model_feature_columns_pca = [
    tf.feature_column.numeric_column(pc_name) for pc_name in pc_names
]
print('model_feature_columns_pca', model_feature_columns_pca)

y_series = car_data['price'].reset_index(drop=True) 
   
train_input_fn_pca = tf.estimator.inputs.pandas_input_fn(
    x=x_df_pca,
    y=y_series,      
    batch_size=batch_size_parameter, 
    num_epochs=None,
    shuffle=True
)
eval_input_fn_pca = tf.estimator.inputs.pandas_input_fn(
    x=x_df_pca,      
    y=y_series,
    batch_size=batch_size_parameter,
    shuffle=False      
)

est_pca = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns_pca,
    hidden_units=hidden_units_parameter,   
    optimizer=optimizer_parameter,   
)

# For Loop for Task 2.4 - PCA + Adagrad
num_print_statements = 10
num_training_steps = 10000
for _ in range(num_print_statements):
    est_pca.train(train_input_fn_pca, steps=num_training_steps //      
num_print_statements)
    scores_pca = est_pca.evaluate(eval_input_fn_pca)     
    print('scores_pca', scores_pca)
```

    model_feature_columns_pca [NumericColumn(key='PC1', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC2', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC3', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC4', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC5', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC6', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC7', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC8', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC9', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 2091349900.0, step = 1
    INFO:tensorflow:global_step/sec: 1213.69
    INFO:tensorflow:loss = 1534947800.0, step = 101 (0.083 sec)
    INFO:tensorflow:global_step/sec: 2745.5
    INFO:tensorflow:loss = 5062113300.0, step = 201 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2734.33
    INFO:tensorflow:loss = 3720717800.0, step = 301 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2813.74
    INFO:tensorflow:loss = 3109013000.0, step = 401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2775.53
    INFO:tensorflow:loss = 3827390000.0, step = 501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2799.17
    INFO:tensorflow:loss = 2314593300.0, step = 601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2754.5
    INFO:tensorflow:loss = 4323034600.0, step = 701 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2625.3
    INFO:tensorflow:loss = 4072804400.0, step = 801 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2592.5
    INFO:tensorflow:loss = 2646758000.0, step = 901 (0.039 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 5204432400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:12
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08792s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:12
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 235356370.0, global_step = 1000, label/mean = 13207.129, loss = 3638971400.0, prediction/mean = 57.835403
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-1000
    scores_pca {'average_loss': 235356370.0, 'label/mean': 13207.129, 'loss': 3638971400.0, 'prediction/mean': 57.835403, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 6912843300.0, step = 1001
    INFO:tensorflow:global_step/sec: 2029.39
    INFO:tensorflow:loss = 4536922000.0, step = 1101 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2879.28
    INFO:tensorflow:loss = 5455348000.0, step = 1201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2899.8
    INFO:tensorflow:loss = 2503908400.0, step = 1301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2933.86
    INFO:tensorflow:loss = 3263463000.0, step = 1401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2958.46
    INFO:tensorflow:loss = 1693317400.0, step = 1501 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2904.72
    INFO:tensorflow:loss = 3774456800.0, step = 1601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2933.41
    INFO:tensorflow:loss = 4165911000.0, step = 1701 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2832.76
    INFO:tensorflow:loss = 1755848700.0, step = 1801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2940.75
    INFO:tensorflow:loss = 2673536800.0, step = 1901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 3867731000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:14
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08412s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:14
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 233279040.0, global_step = 2000, label/mean = 13207.129, loss = 3606852900.0, prediction/mean = 118.857925
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-2000
    scores_pca {'average_loss': 233279040.0, 'label/mean': 13207.129, 'loss': 3606852900.0, 'prediction/mean': 118.857925, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2404740600.0, step = 2001
    INFO:tensorflow:global_step/sec: 1937.39
    INFO:tensorflow:loss = 3010348800.0, step = 2101 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2831.5
    INFO:tensorflow:loss = 4348500000.0, step = 2201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2936.32
    INFO:tensorflow:loss = 3474673700.0, step = 2301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2969.82
    INFO:tensorflow:loss = 3343020000.0, step = 2401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2718.95
    INFO:tensorflow:loss = 6204774400.0, step = 2501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2775.79
    INFO:tensorflow:loss = 3717620700.0, step = 2601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2844.04
    INFO:tensorflow:loss = 2417049600.0, step = 2701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2609.87
    INFO:tensorflow:loss = 2452829200.0, step = 2801 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2948.03
    INFO:tensorflow:loss = 7713747500.0, step = 2901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 1229316700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:15
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08272s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:15
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 231152220.0, global_step = 3000, label/mean = 13207.129, loss = 3573969000.0, prediction/mean = 180.81714
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-3000
    scores_pca {'average_loss': 231152220.0, 'label/mean': 13207.129, 'loss': 3573969000.0, 'prediction/mean': 180.81714, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 2648503300.0, step = 3001
    INFO:tensorflow:global_step/sec: 2088.42
    INFO:tensorflow:loss = 4694061000.0, step = 3101 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2996.17
    INFO:tensorflow:loss = 3718283000.0, step = 3201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2900.99
    INFO:tensorflow:loss = 3103564800.0, step = 3301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2821.5
    INFO:tensorflow:loss = 4856468000.0, step = 3401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 3030.87
    INFO:tensorflow:loss = 1902353700.0, step = 3501 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2960.49
    INFO:tensorflow:loss = 5457479700.0, step = 3601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2841.32
    INFO:tensorflow:loss = 3243481600.0, step = 3701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2947.43
    INFO:tensorflow:loss = 2292566800.0, step = 3801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2952.82
    INFO:tensorflow:loss = 1931785500.0, step = 3901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 4430297600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:16
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08314s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:16
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 229026140.0, global_step = 4000, label/mean = 13207.129, loss = 3541096700.0, prediction/mean = 242.6689
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-4000
    scores_pca {'average_loss': 229026140.0, 'label/mean': 13207.129, 'loss': 3541096700.0, 'prediction/mean': 242.6689, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 2043244800.0, step = 4001
    INFO:tensorflow:global_step/sec: 1879.74
    INFO:tensorflow:loss = 2279418400.0, step = 4101 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2997.97
    INFO:tensorflow:loss = 3006335000.0, step = 4201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2894
    INFO:tensorflow:loss = 5090577000.0, step = 4301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2992.6
    INFO:tensorflow:loss = 4467495000.0, step = 4401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2822.3
    INFO:tensorflow:loss = 6843233000.0, step = 4501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2673.23
    INFO:tensorflow:loss = 1971712500.0, step = 4601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2948.52
    INFO:tensorflow:loss = 3016760800.0, step = 4701 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2980.98
    INFO:tensorflow:loss = 2059273300.0, step = 4801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2855.04
    INFO:tensorflow:loss = 2936385800.0, step = 4901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 2045931000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:17
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08283s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:17
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 226918380.0, global_step = 5000, label/mean = 13207.129, loss = 3508507100.0, prediction/mean = 304.06763
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-5000
    scores_pca {'average_loss': 226918380.0, 'label/mean': 13207.129, 'loss': 3508507100.0, 'prediction/mean': 304.06763, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 5261445000.0, step = 5001
    INFO:tensorflow:global_step/sec: 1008.4
    INFO:tensorflow:loss = 3885198000.0, step = 5101 (0.100 sec)
    INFO:tensorflow:global_step/sec: 2932.65
    INFO:tensorflow:loss = 3850084400.0, step = 5201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2899.14
    INFO:tensorflow:loss = 4388633000.0, step = 5301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2672.72
    INFO:tensorflow:loss = 1484497900.0, step = 5401 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2762.66
    INFO:tensorflow:loss = 4427099600.0, step = 5501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2778.07
    INFO:tensorflow:loss = 5199862300.0, step = 5601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2758.1
    INFO:tensorflow:loss = 2938176000.0, step = 5701 (0.037 sec)
    INFO:tensorflow:global_step/sec: 1617.83
    INFO:tensorflow:loss = 5330774500.0, step = 5801 (0.063 sec)
    INFO:tensorflow:global_step/sec: 1728.82
    INFO:tensorflow:loss = 2616705000.0, step = 5901 (0.058 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 3661680000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:19
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08845s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:19
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 224826320.0, global_step = 6000, label/mean = 13207.129, loss = 3476160800.0, prediction/mean = 365.0682
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-6000
    scores_pca {'average_loss': 224826320.0, 'label/mean': 13207.129, 'loss': 3476160800.0, 'prediction/mean': 365.0682, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 6287373300.0, step = 6001
    INFO:tensorflow:global_step/sec: 1910.91
    INFO:tensorflow:loss = 3818425600.0, step = 6101 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2896.3
    INFO:tensorflow:loss = 7085949000.0, step = 6201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2928.59
    INFO:tensorflow:loss = 3591928000.0, step = 6301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2936.34
    INFO:tensorflow:loss = 2827624400.0, step = 6401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2604.58
    INFO:tensorflow:loss = 6908069000.0, step = 6501 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2972.03
    INFO:tensorflow:loss = 4547336000.0, step = 6601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2920.48
    INFO:tensorflow:loss = 6157676500.0, step = 6701 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2934.09
    INFO:tensorflow:loss = 4499115000.0, step = 6801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2897.72
    INFO:tensorflow:loss = 4365544000.0, step = 6901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 4394992000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:20
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08576s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:20
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 222743900.0, global_step = 7000, label/mean = 13207.129, loss = 3443963400.0, prediction/mean = 425.93372
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-7000
    scores_pca {'average_loss': 222743900.0, 'label/mean': 13207.129, 'loss': 3443963400.0, 'prediction/mean': 425.93372, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 4147759000.0, step = 7001
    INFO:tensorflow:global_step/sec: 1988.08
    INFO:tensorflow:loss = 1362376300.0, step = 7101 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2952.36
    INFO:tensorflow:loss = 2623644200.0, step = 7201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2953.78
    INFO:tensorflow:loss = 4736493600.0, step = 7301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2853.97
    INFO:tensorflow:loss = 3735169500.0, step = 7401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2369.28
    INFO:tensorflow:loss = 3399397600.0, step = 7501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2616.44
    INFO:tensorflow:loss = 2515442200.0, step = 7601 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2910.12
    INFO:tensorflow:loss = 3111591200.0, step = 7701 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2865.9
    INFO:tensorflow:loss = 3217986800.0, step = 7801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2862.95
    INFO:tensorflow:loss = 4751655000.0, step = 7901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 6225330000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:21
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08404s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:21
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 220676300.0, global_step = 8000, label/mean = 13207.129, loss = 3411995100.0, prediction/mean = 486.54764
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-8000
    scores_pca {'average_loss': 220676300.0, 'label/mean': 13207.129, 'loss': 3411995100.0, 'prediction/mean': 486.54764, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 4164426800.0, step = 8001
    INFO:tensorflow:global_step/sec: 2037.6
    INFO:tensorflow:loss = 5808765400.0, step = 8101 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2935.48
    INFO:tensorflow:loss = 2189817600.0, step = 8201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2528.78
    INFO:tensorflow:loss = 3865996500.0, step = 8301 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2924.74
    INFO:tensorflow:loss = 5645223000.0, step = 8401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2707.24
    INFO:tensorflow:loss = 2514249200.0, step = 8501 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2718.21
    INFO:tensorflow:loss = 3668864000.0, step = 8601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2770.31
    INFO:tensorflow:loss = 2266616800.0, step = 8701 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2872.57
    INFO:tensorflow:loss = 3257662000.0, step = 8801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2902.75
    INFO:tensorflow:loss = 4378941400.0, step = 8901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 4102020900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:23
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08482s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:23
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 218624800.0, global_step = 9000, label/mean = 13207.129, loss = 3380275700.0, prediction/mean = 546.8516
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-9000
    scores_pca {'average_loss': 218624800.0, 'label/mean': 13207.129, 'loss': 3380275700.0, 'prediction/mean': 546.8516, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 3497058000.0, step = 9001
    INFO:tensorflow:global_step/sec: 1847.16
    INFO:tensorflow:loss = 2364483000.0, step = 9101 (0.055 sec)
    INFO:tensorflow:global_step/sec: 2703.73
    INFO:tensorflow:loss = 2239648800.0, step = 9201 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2862.95
    INFO:tensorflow:loss = 3068128800.0, step = 9301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2734.85
    INFO:tensorflow:loss = 3249217800.0, step = 9401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2883.1
    INFO:tensorflow:loss = 2287459300.0, step = 9501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2925.86
    INFO:tensorflow:loss = 1835903500.0, step = 9601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2830.7
    INFO:tensorflow:loss = 2316944100.0, step = 9701 (0.035 sec)
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 9714 vs previous value: 9714. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    INFO:tensorflow:global_step/sec: 2796.72
    INFO:tensorflow:loss = 4532899000.0, step = 9801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2980.09
    INFO:tensorflow:loss = 2991913000.0, step = 9901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 2166401500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:24
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09794s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:24
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 216592700.0, global_step = 10000, label/mean = 13207.129, loss = 3348856600.0, prediction/mean = 606.8623
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp2iay0z00/model.ckpt-10000
    scores_pca {'average_loss': 216592700.0, 'label/mean': 13207.129, 'loss': 3348856600.0, 'prediction/mean': 606.8623, 'global_step': 10000}


### Task 3: Make your best model using only categorical features

- Look at the possible feature columns for categorical features. They begin with `categorical_column_with_` in go/tf-ops.
- You may find `dataframe[categorical_feature_names].unique()` helpful.



```python
## Checking unique values of categorical features
car_data[feature_name].unique()
```




    array([ 7.8 ,  8.5 ,  8.4 ,  9.  ,  8.1 ,  9.3 ,  9.2 ,  8.6 ,  9.5 ,
            8.8 , 21.5 ,  9.4 ,  7.6 , 23.  ,  8.  ,  7.  ,  9.31,  8.7 ,
            9.41,  7.7 ,  9.6 ,  7.5 , 21.  , 10.  , 22.7 , 10.1 , 11.5 ,
            8.3 , 22.5 ,  9.1 , 21.9 , 22.  ])




```python
# [Change #9]: Added this section to outline the next steps for Task 3.
# We have the full list of values that each feature takes on, and the list is
# relatively small so we use categorical_column_with_vocabulary_list.
# encoding is already handled by vocabulary_list internally, so, no LabelEncoder needed
# -> indicator_column + categorical_column_with_vocabulary_list (TF-native one-hot encoding)

# Final score at 10k steps: avg_loss = 181M, RMSE ~$13,464, prediction/mean = $2,361 (vs label/mean $13,207)
# This indicates that the model is heavily underfitting — prediction mean is only 18% of the actual mean price

batch_size = 16

x_df = car_data[categorical_feature_names]
y_series = car_data['price']

train_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    y=y_series,
    batch_size=batch_size,
    num_epochs=None,
    shuffle=True)

eval_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    y=y_series,
    batch_size=batch_size,
    shuffle=False)

predict_input_fn = tf.estimator.inputs.pandas_input_fn(
    x=x_df,
    batch_size=batch_size,
    shuffle=False)

model_feature_columns = [
    tf.feature_column.indicator_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            feature_name, vocabulary_list=car_data[feature_name].unique()))
    for feature_name in categorical_feature_names
]
print('model_feature_columns', model_feature_columns)

# [Change #10]: Added two new estimators to compare different learning rates with Adagrad.
# - est_lr1: Adagrad with lr=0.01 (same as baseline)
# - est_lr2: Adagrad with lr=0.5 (to test if a higher learning rate can help convergence given the sparse gradients from one-hot encoding)


est_lr1 = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=[64],
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.01),
  )

est_lr2 = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=[64],
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.5),
  )

num_print_statements = 10
num_training_steps = 10000

# TRAIN lr=0.01 + Adagrad
for _ in range(num_print_statements):
  est_lr1.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores = est_lr1.evaluate(eval_input_fn)
  print('scores', scores)

# TRAIN lr=0.5 + Adagrad
for _ in range(num_print_statements):
  est_lr2.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores = est_lr2.evaluate(eval_input_fn)
  print('scores', scores)
```

    model_feature_columns [IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='drive-wheels', vocabulary_list=('rwd', 'fwd', '4wd'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='make', vocabulary_list=('nissan', 'volkswagen', 'peugot', 'toyota', 'jaguar', 'isuzu', 'mazda', 'subaru', 'bmw', 'mercedes-benz', 'honda', 'mitsubishi', 'dodge', 'audi', 'saab', 'plymouth', 'renault', 'volvo', 'alfa-romero', 'chevrolet', 'porsche', 'mercury'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='engine-type', vocabulary_list=('ohcv', 'ohc', 'l', 'dohc', 'ohcf', 'rotor'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='aspiration', vocabulary_list=('turbo', 'std'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='num-doors', vocabulary_list=('two', 'four', '?'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='fuel-system', vocabulary_list=('mpfi', '2bbl', 'spfi', 'idi', '1bbl', '4bbl', 'spdi', 'mfi'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='engine-location', vocabulary_list=('front', 'rear'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='num-cylinders', vocabulary_list=('six', 'four', 'five', 'two', 'eight', 'three', 'twelve'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='body-style', vocabulary_list=('hatchback', 'sedan', 'wagon', 'convertible', 'hardtop'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='fuel-type', vocabulary_list=('gas', 'diesel'), dtype=tf.string, default_value=-1, num_oov_buckets=0))]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 2074685800.0, step = 1
    INFO:tensorflow:global_step/sec: 1343.02
    INFO:tensorflow:loss = 3480320500.0, step = 101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2570.69
    INFO:tensorflow:loss = 3786669600.0, step = 201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2378.53
    INFO:tensorflow:loss = 4928569300.0, step = 301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2297.68
    INFO:tensorflow:loss = 2109347100.0, step = 401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2804.34
    INFO:tensorflow:loss = 5098363000.0, step = 501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2790.96
    INFO:tensorflow:loss = 2095156000.0, step = 601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2193.8
    INFO:tensorflow:loss = 2751653400.0, step = 701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2839.55
    INFO:tensorflow:loss = 4308797000.0, step = 801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2470.71
    INFO:tensorflow:loss = 1595364100.0, step = 901 (0.040 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 2728464600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:26
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10805s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:26
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 229822290.0, global_step = 1000, label/mean = 13207.129, loss = 3553406000.0, prediction/mean = 289.12692
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-1000
    scores {'average_loss': 229822290.0, 'label/mean': 13207.129, 'loss': 3553406000.0, 'prediction/mean': 289.12692, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 3908443600.0, step = 1001
    INFO:tensorflow:global_step/sec: 1455.26
    INFO:tensorflow:loss = 2324871200.0, step = 1101 (0.069 sec)
    INFO:tensorflow:global_step/sec: 2464.76
    INFO:tensorflow:loss = 6086023000.0, step = 1201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2274.53
    INFO:tensorflow:loss = 4505281500.0, step = 1301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2661.28
    INFO:tensorflow:loss = 5467554300.0, step = 1401 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2708.64
    INFO:tensorflow:loss = 6042677000.0, step = 1501 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2754.37
    INFO:tensorflow:loss = 3150361000.0, step = 1601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2838.46
    INFO:tensorflow:loss = 4416460000.0, step = 1701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2696.45
    INFO:tensorflow:loss = 3707106800.0, step = 1801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2268.6
    INFO:tensorflow:loss = 2684582400.0, step = 1901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 2537524700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:28
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10604s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:28
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 222792980.0, global_step = 2000, label/mean = 13207.129, loss = 3444722200.0, prediction/mean = 567.8734
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-2000
    scores {'average_loss': 222792980.0, 'label/mean': 13207.129, 'loss': 3444722200.0, 'prediction/mean': 567.8734, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2385329700.0, step = 2001
    INFO:tensorflow:global_step/sec: 1426.47
    INFO:tensorflow:loss = 5461056000.0, step = 2101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2263.73
    INFO:tensorflow:loss = 2289942800.0, step = 2201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2282.48
    INFO:tensorflow:loss = 1537691600.0, step = 2301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2833.19
    INFO:tensorflow:loss = 1877944000.0, step = 2401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2269.68
    INFO:tensorflow:loss = 2604046300.0, step = 2501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2825.42
    INFO:tensorflow:loss = 3622515000.0, step = 2601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2266.25
    INFO:tensorflow:loss = 2080137100.0, step = 2701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2643.05
    INFO:tensorflow:loss = 3914600000.0, step = 2801 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2276.19
    INFO:tensorflow:loss = 1916211000.0, step = 2901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 1965323400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:30
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10361s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:30
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 216015600.0, global_step = 3000, label/mean = 13207.129, loss = 3339933400.0, prediction/mean = 842.4378
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-3000
    scores {'average_loss': 216015600.0, 'label/mean': 13207.129, 'loss': 3339933400.0, 'prediction/mean': 842.4378, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 2910873300.0, step = 3001
    INFO:tensorflow:global_step/sec: 1555.36
    INFO:tensorflow:loss = 5514338300.0, step = 3101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2443.61
    INFO:tensorflow:loss = 4093763800.0, step = 3201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2427.96
    INFO:tensorflow:loss = 2693934000.0, step = 3301 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2270.97
    INFO:tensorflow:loss = 3599096600.0, step = 3401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2805.74
    INFO:tensorflow:loss = 2893600300.0, step = 3501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2591.22
    INFO:tensorflow:loss = 3347894800.0, step = 3601 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2503.31
    INFO:tensorflow:loss = 2955465200.0, step = 3701 (0.040 sec)
    INFO:tensorflow:global_step/sec: 985.979
    INFO:tensorflow:loss = 6308279300.0, step = 3801 (0.102 sec)
    INFO:tensorflow:global_step/sec: 2226.48
    INFO:tensorflow:loss = 4617566700.0, step = 3901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 5129311000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:31
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10745s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:32
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 209499230.0, global_step = 4000, label/mean = 13207.129, loss = 3239180500.0, prediction/mean = 1112.418
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-4000
    scores {'average_loss': 209499230.0, 'label/mean': 13207.129, 'loss': 3239180500.0, 'prediction/mean': 1112.418, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 2935810600.0, step = 4001
    INFO:tensorflow:global_step/sec: 1418.62
    INFO:tensorflow:loss = 2416485000.0, step = 4101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2830.68
    INFO:tensorflow:loss = 2932308000.0, step = 4201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2863.92
    INFO:tensorflow:loss = 3572833800.0, step = 4301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2338.76
    INFO:tensorflow:loss = 2061998200.0, step = 4401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2313.47
    INFO:tensorflow:loss = 1278791400.0, step = 4501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2838.9
    INFO:tensorflow:loss = 4139437000.0, step = 4601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2848.35
    INFO:tensorflow:loss = 2560946200.0, step = 4701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2825.25
    INFO:tensorflow:loss = 2619428400.0, step = 4801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2272.99
    INFO:tensorflow:loss = 3708104200.0, step = 4901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 1063128060.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:33
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10363s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:33
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 203217520.0, global_step = 5000, label/mean = 13207.129, loss = 3142055400.0, prediction/mean = 1378.4725
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-5000
    scores {'average_loss': 203217520.0, 'label/mean': 13207.129, 'loss': 3142055400.0, 'prediction/mean': 1378.4725, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 1617964300.0, step = 5001
    INFO:tensorflow:global_step/sec: 1430.31
    INFO:tensorflow:loss = 4306600400.0, step = 5101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2270.87
    INFO:tensorflow:loss = 2482842000.0, step = 5201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2782.79
    INFO:tensorflow:loss = 3091594800.0, step = 5301 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2262.08
    INFO:tensorflow:loss = 2132948600.0, step = 5401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2801.69
    INFO:tensorflow:loss = 3264389600.0, step = 5501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2682.26
    INFO:tensorflow:loss = 6370328000.0, step = 5601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2273.35
    INFO:tensorflow:loss = 1576796400.0, step = 5701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2260.45
    INFO:tensorflow:loss = 2463148800.0, step = 5801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2651.47
    INFO:tensorflow:loss = 2386436400.0, step = 5901 (0.038 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 3241043700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:35
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10352s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:35
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 197148800.0, global_step = 6000, label/mean = 13207.129, loss = 3048223700.0, prediction/mean = 1641.2034
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-6000
    scores {'average_loss': 197148800.0, 'label/mean': 13207.129, 'loss': 3048223700.0, 'prediction/mean': 1641.2034, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 2295571200.0, step = 6001
    INFO:tensorflow:global_step/sec: 1430.9
    INFO:tensorflow:loss = 1865936400.0, step = 6101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2256.62
    INFO:tensorflow:loss = 5004117500.0, step = 6201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2690.05
    INFO:tensorflow:loss = 3010555100.0, step = 6301 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2275.79
    INFO:tensorflow:loss = 1321218000.0, step = 6401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2842.67
    INFO:tensorflow:loss = 6403764700.0, step = 6501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2271.39
    INFO:tensorflow:loss = 2023386500.0, step = 6601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2574.27
    INFO:tensorflow:loss = 3438875100.0, step = 6701 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2488.18
    INFO:tensorflow:loss = 3020680700.0, step = 6801 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2276.19
    INFO:tensorflow:loss = 1769905400.0, step = 6901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 3836571100.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:36
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10363s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:37
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 191310140.0, global_step = 7000, label/mean = 13207.129, loss = 2957949200.0, prediction/mean = 1899.7373
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-7000
    scores {'average_loss': 191310140.0, 'label/mean': 13207.129, 'loss': 2957949200.0, 'prediction/mean': 1899.7373, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 4350463000.0, step = 7001
    INFO:tensorflow:global_step/sec: 1545.05
    INFO:tensorflow:loss = 2631744800.0, step = 7101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2568.56
    INFO:tensorflow:loss = 7896692700.0, step = 7201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2835.85
    INFO:tensorflow:loss = 2080700700.0, step = 7301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2554.29
    INFO:tensorflow:loss = 2946929000.0, step = 7401 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2856.71
    INFO:tensorflow:loss = 2256595700.0, step = 7501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2231.4
    INFO:tensorflow:loss = 1764660500.0, step = 7601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2261.26
    INFO:tensorflow:loss = 2319895000.0, step = 7701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2353.27
    INFO:tensorflow:loss = 4443385000.0, step = 7801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2270.47
    INFO:tensorflow:loss = 1213975600.0, step = 7901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 2149900000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:38
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10801s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:38
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 185665500.0, global_step = 8000, label/mean = 13207.129, loss = 2870674400.0, prediction/mean = 2155.289
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-8000
    scores {'average_loss': 185665500.0, 'label/mean': 13207.129, 'loss': 2870674400.0, 'prediction/mean': 2155.289, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 4026558500.0, step = 8001
    INFO:tensorflow:global_step/sec: 1390.32
    INFO:tensorflow:loss = 5200996400.0, step = 8101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2235.7
    INFO:tensorflow:loss = 3248698600.0, step = 8201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2770.6
    INFO:tensorflow:loss = 3099179500.0, step = 8301 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2670.53
    INFO:tensorflow:loss = 3794869200.0, step = 8401 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2500.3
    INFO:tensorflow:loss = 3471056400.0, step = 8501 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2426.67
    INFO:tensorflow:loss = 1140047700.0, step = 8601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2379.87
    INFO:tensorflow:loss = 3793471000.0, step = 8701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2750.44
    INFO:tensorflow:loss = 2275362800.0, step = 8801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2544.01
    INFO:tensorflow:loss = 3411059200.0, step = 8901 (0.039 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 3091213300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:40
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11273s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:40
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 180237650.0, global_step = 9000, label/mean = 13207.129, loss = 2786751500.0, prediction/mean = 2406.739
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-9000
    scores {'average_loss': 180237650.0, 'label/mean': 13207.129, 'loss': 2786751500.0, 'prediction/mean': 2406.739, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 2911357200.0, step = 9001
    INFO:tensorflow:global_step/sec: 1596.04
    INFO:tensorflow:loss = 2581942800.0, step = 9101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2474.27
    INFO:tensorflow:loss = 2792654300.0, step = 9201 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2238.73
    INFO:tensorflow:loss = 3512153600.0, step = 9301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2787.77
    INFO:tensorflow:loss = 3497043500.0, step = 9401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2532.23
    INFO:tensorflow:loss = 3608611300.0, step = 9501 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2584.7
    INFO:tensorflow:loss = 3709823000.0, step = 9601 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2420.02
    INFO:tensorflow:loss = 2249182000.0, step = 9701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2712.62
    INFO:tensorflow:loss = 1941240200.0, step = 9801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2776.38
    INFO:tensorflow:loss = 2730375700.0, step = 9901 (0.036 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 3886416400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:42
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10987s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:42
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 175011040.0, global_step = 10000, label/mean = 13207.129, loss = 2705940000.0, prediction/mean = 2654.4385
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpd_xrbdno/model.ckpt-10000
    scores {'average_loss': 175011040.0, 'label/mean': 13207.129, 'loss': 2705940000.0, 'prediction/mean': 2654.4385, 'global_step': 10000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 4638553000.0, step = 1
    INFO:tensorflow:global_step/sec: 1435.48
    INFO:tensorflow:loss = 340228540.0, step = 101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2378.18
    INFO:tensorflow:loss = 98471140.0, step = 201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2599.76
    INFO:tensorflow:loss = 262608910.0, step = 301 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2644.51
    INFO:tensorflow:loss = 124887710.0, step = 401 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2530.18
    INFO:tensorflow:loss = 282156220.0, step = 501 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2770.4
    INFO:tensorflow:loss = 85043140.0, step = 601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2646.12
    INFO:tensorflow:loss = 128489120.0, step = 701 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2208.14
    INFO:tensorflow:loss = 125240330.0, step = 801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2221.92
    INFO:tensorflow:loss = 132811940.0, step = 901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 292038240.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10539s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:44
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 9072093.0, global_step = 1000, label/mean = 13207.129, loss = 140268510.0, prediction/mean = 13172.017
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-1000
    scores {'average_loss': 9072093.0, 'label/mean': 13207.129, 'loss': 140268510.0, 'prediction/mean': 13172.017, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 65074410.0, step = 1001
    INFO:tensorflow:global_step/sec: 1409.64
    INFO:tensorflow:loss = 90398390.0, step = 1101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2698.24
    INFO:tensorflow:loss = 213939140.0, step = 1201 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2526.98
    INFO:tensorflow:loss = 97266570.0, step = 1301 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2536.73
    INFO:tensorflow:loss = 70011260.0, step = 1401 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2534.84
    INFO:tensorflow:loss = 210824430.0, step = 1501 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2585.58
    INFO:tensorflow:loss = 132787384.0, step = 1601 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2664.45
    INFO:tensorflow:loss = 49976490.0, step = 1701 (0.038 sec)
    INFO:tensorflow:global_step/sec: 1056.54
    INFO:tensorflow:loss = 53801696.0, step = 1801 (0.095 sec)
    INFO:tensorflow:global_step/sec: 2639.7
    INFO:tensorflow:loss = 112887624.0, step = 1901 (0.038 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 461099840.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:45
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10972s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:46
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 6869323.0, global_step = 2000, label/mean = 13207.129, loss = 106210300.0, prediction/mean = 13260.6045
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-2000
    scores {'average_loss': 6869323.0, 'label/mean': 13207.129, 'loss': 106210300.0, 'prediction/mean': 13260.6045, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 81591270.0, step = 2001
    INFO:tensorflow:global_step/sec: 1483.9
    INFO:tensorflow:loss = 41821120.0, step = 2101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2769.69
    INFO:tensorflow:loss = 56029016.0, step = 2201 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2738.23
    INFO:tensorflow:loss = 58753376.0, step = 2301 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2240.8
    INFO:tensorflow:loss = 38898270.0, step = 2401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2852.18
    INFO:tensorflow:loss = 55769250.0, step = 2501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2297.9
    INFO:tensorflow:loss = 63972364.0, step = 2601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2400.27
    INFO:tensorflow:loss = 107520340.0, step = 2701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2691.57
    INFO:tensorflow:loss = 131209736.0, step = 2801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2789.17
    INFO:tensorflow:loss = 73612220.0, step = 2901 (0.036 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 374438530.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:47
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10230s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:47
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 6035702.0, global_step = 3000, label/mean = 13207.129, loss = 93321230.0, prediction/mean = 13121.049
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-3000
    scores {'average_loss': 6035702.0, 'label/mean': 13207.129, 'loss': 93321230.0, 'prediction/mean': 13121.049, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 111052616.0, step = 3001
    INFO:tensorflow:global_step/sec: 1409.54
    INFO:tensorflow:loss = 106940220.0, step = 3101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2757.49
    INFO:tensorflow:loss = 313749060.0, step = 3201 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2835.35
    INFO:tensorflow:loss = 41166536.0, step = 3301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2692.73
    INFO:tensorflow:loss = 38202804.0, step = 3401 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2653.25
    INFO:tensorflow:loss = 42315736.0, step = 3501 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2855
    INFO:tensorflow:loss = 66239108.0, step = 3601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 1272.83
    INFO:tensorflow:loss = 129680210.0, step = 3701 (0.079 sec)
    INFO:tensorflow:global_step/sec: 2741.59
    INFO:tensorflow:loss = 55981612.0, step = 3801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2752.64
    INFO:tensorflow:loss = 44248350.0, step = 3901 (0.036 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 24244464.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:49
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10399s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:49
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 5578987.5, global_step = 4000, label/mean = 13207.129, loss = 86259730.0, prediction/mean = 13194.636
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-4000
    scores {'average_loss': 5578987.5, 'label/mean': 13207.129, 'loss': 86259730.0, 'prediction/mean': 13194.636, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 25534112.0, step = 4001
    INFO:tensorflow:global_step/sec: 1406.03
    INFO:tensorflow:loss = 73413400.0, step = 4101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2562.13
    INFO:tensorflow:loss = 70226160.0, step = 4201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2818.01
    INFO:tensorflow:loss = 56000720.0, step = 4301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2256.69
    INFO:tensorflow:loss = 47526370.0, step = 4401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2822.05
    INFO:tensorflow:loss = 28607228.0, step = 4501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2358.5
    INFO:tensorflow:loss = 40613360.0, step = 4601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2831.73
    INFO:tensorflow:loss = 42729250.0, step = 4701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2243.46
    INFO:tensorflow:loss = 44744640.0, step = 4801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2610.22
    INFO:tensorflow:loss = 51911276.0, step = 4901 (0.038 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 133118190.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:50
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10401s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:50
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 5316894.5, global_step = 5000, label/mean = 13207.129, loss = 82207370.0, prediction/mean = 13185.577
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-5000
    scores {'average_loss': 5316894.5, 'label/mean': 13207.129, 'loss': 82207370.0, 'prediction/mean': 13185.577, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 146099470.0, step = 5001
    INFO:tensorflow:global_step/sec: 1677.46
    INFO:tensorflow:loss = 32068208.0, step = 5101 (0.060 sec)
    INFO:tensorflow:global_step/sec: 2521.04
    INFO:tensorflow:loss = 44495496.0, step = 5201 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2301.5
    INFO:tensorflow:loss = 58240480.0, step = 5301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2344.6
    INFO:tensorflow:loss = 65661724.0, step = 5401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2774.47
    INFO:tensorflow:loss = 30117256.0, step = 5501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2308.51
    INFO:tensorflow:loss = 72681420.0, step = 5601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2514.9
    INFO:tensorflow:loss = 64278188.0, step = 5701 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2664.96
    INFO:tensorflow:loss = 38883164.0, step = 5801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2844.79
    INFO:tensorflow:loss = 67859410.0, step = 5901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 52800510.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:52
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10279s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:52
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 5156783.0, global_step = 6000, label/mean = 13207.129, loss = 79731790.0, prediction/mean = 13211.641
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-6000
    scores {'average_loss': 5156783.0, 'label/mean': 13207.129, 'loss': 79731790.0, 'prediction/mean': 13211.641, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 36823016.0, step = 6001
    INFO:tensorflow:global_step/sec: 1670.48
    INFO:tensorflow:loss = 38849224.0, step = 6101 (0.060 sec)
    INFO:tensorflow:global_step/sec: 2279.35
    INFO:tensorflow:loss = 27325416.0, step = 6201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2843.02
    INFO:tensorflow:loss = 26587512.0, step = 6301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2822.72
    INFO:tensorflow:loss = 87302460.0, step = 6401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2277.42
    INFO:tensorflow:loss = 25564992.0, step = 6501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2575.74
    INFO:tensorflow:loss = 57266160.0, step = 6601 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2859.18
    INFO:tensorflow:loss = 27031520.0, step = 6701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2276.4
    INFO:tensorflow:loss = 52341170.0, step = 6801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2275.06
    INFO:tensorflow:loss = 92311120.0, step = 6901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 24936486.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10360s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:54
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 5056413.5, global_step = 7000, label/mean = 13207.129, loss = 78179930.0, prediction/mean = 13171.156
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-7000
    scores {'average_loss': 5056413.5, 'label/mean': 13207.129, 'loss': 78179930.0, 'prediction/mean': 13171.156, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 45536176.0, step = 7001
    INFO:tensorflow:global_step/sec: 1407.62
    INFO:tensorflow:loss = 53646244.0, step = 7101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 1533.96
    INFO:tensorflow:loss = 105954376.0, step = 7201 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2207.89
    INFO:tensorflow:loss = 57126304.0, step = 7301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2255.77
    INFO:tensorflow:loss = 44170910.0, step = 7401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2844.46
    INFO:tensorflow:loss = 67559820.0, step = 7501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2414.35
    INFO:tensorflow:loss = 53097636.0, step = 7601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2278.05
    INFO:tensorflow:loss = 71786200.0, step = 7701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2280.98
    INFO:tensorflow:loss = 37554420.0, step = 7801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2761.52
    INFO:tensorflow:loss = 40251850.0, step = 7901 (0.037 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 194320290.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:55
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10330s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:55
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 4988311.5, global_step = 8000, label/mean = 13207.129, loss = 77126970.0, prediction/mean = 13244.511
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-8000
    scores {'average_loss': 4988311.5, 'label/mean': 13207.129, 'loss': 77126970.0, 'prediction/mean': 13244.511, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 71893200.0, step = 8001
    INFO:tensorflow:global_step/sec: 1490.49
    INFO:tensorflow:loss = 45112296.0, step = 8101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2293
    INFO:tensorflow:loss = 176147780.0, step = 8201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2511.12
    INFO:tensorflow:loss = 50080236.0, step = 8301 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2884.41
    INFO:tensorflow:loss = 54261650.0, step = 8401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2351.57
    INFO:tensorflow:loss = 52113596.0, step = 8501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2759.92
    INFO:tensorflow:loss = 49339760.0, step = 8601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2281.27
    INFO:tensorflow:loss = 99255520.0, step = 8701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2861.23
    INFO:tensorflow:loss = 66359264.0, step = 8801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2829
    INFO:tensorflow:loss = 22991620.0, step = 8901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 52129840.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10359s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:57
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 4944019.0, global_step = 9000, label/mean = 13207.129, loss = 76442136.0, prediction/mean = 13233.59
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-9000
    scores {'average_loss': 4944019.0, 'label/mean': 13207.129, 'loss': 76442136.0, 'prediction/mean': 13233.59, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 29010324.0, step = 9001
    INFO:tensorflow:global_step/sec: 1408.81
    INFO:tensorflow:loss = 98450050.0, step = 9101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2603.09
    INFO:tensorflow:loss = 68318300.0, step = 9201 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2632.2
    INFO:tensorflow:loss = 73461630.0, step = 9301 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2794.15
    INFO:tensorflow:loss = 63407860.0, step = 9401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2650.83
    INFO:tensorflow:loss = 92509790.0, step = 9501 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2251.79
    INFO:tensorflow:loss = 30234202.0, step = 9601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2844.54
    INFO:tensorflow:loss = 43211760.0, step = 9701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2838.82
    INFO:tensorflow:loss = 28492966.0, step = 9801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2384.13
    INFO:tensorflow:loss = 97266230.0, step = 9901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 44569744.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T06:28:59
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10204s
    INFO:tensorflow:Finished evaluation at 2026-04-03-06:28:59
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 4912855.0, global_step = 10000, label/mean = 13207.129, loss = 75960300.0, prediction/mean = 13181.497
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp7c49enkr/model.ckpt-10000
    scores {'average_loss': 4912855.0, 'label/mean': 13207.129, 'loss': 75960300.0, 'prediction/mean': 13181.497, 'global_step': 10000}


### Task 4: Using all the features, make the best model that you can make

With all the features combined, your model should perform better than your earlier models using numerical and categorical models alone. Tune your model until that is the case.


```python
## Your code goes here

# Combine all data (take care to use normalized data)
# Run code again, to check...

# What the code does:
#  - Z-score normalization on 15 numeric features
#  - indicator_column on 10 categorical features
#  - Same Adagrad lr=0.01 config

#  Critical bug in the Task 4 template (line ~3570):
#  normalizer_fn=lambda val: (val - x_df.mean()[feature_name]) / (epsilon + x_df.std()[feature_name])
#  Python closure captures feature_name by reference — by the time the lambda runs, feature_name will be the
#   LAST value in the loop. All 15 numeric columns will normalize using the last feature's stats.

#  This was fixed in Task 2.1/2.2 with fn=feature_name pattern:
#  normalizer_fn=lambda val, fn=feature_name: (val - x_df.mean()[fn]) / (epsilon + x_df.std()[fn])
#  Need to fix this before running, otherwise normalization will be wrong.
```


```python
# The fix is pre-computing means/stds from numeric columns only (before the mixed x_df is defined). 
# Also adds lr=0.5 as a second estimator:                                                                   
                                                                                                        
# [Change #12]: Task 4 — all features combined (numeric Z-score + categorical indicator)              
# Fix: pre-compute numeric stats BEFORE x_df is defined as mixed-type.                                
# x_df.mean() on a mixed DataFrame (numeric + strings) raises TypeError — compute from numeric only.  
                                                                                                    
batch_size = 16                                                                                       
epsilon = 0.000001                                                                                    
                                                                                                    
# Pre-compute stats from numeric columns only                                                         
numeric_means = car_data[numeric_feature_names].mean()                                                
numeric_stds  = car_data[numeric_feature_names].std()                                                 
                                                                                                    
x_df = car_data[numeric_feature_names + categorical_feature_names]                                    
y_series = car_data['price']                                                                          
                                                                                                    
train_input_fn = tf.estimator.inputs.pandas_input_fn(                                                 
    x=x_df, y=y_series, batch_size=batch_size, num_epochs=None, shuffle=True)                         
eval_input_fn = tf.estimator.inputs.pandas_input_fn(                                                  
    x=x_df, y=y_series, batch_size=batch_size, shuffle=False)                                         
                                                                                                    
model_feature_columns = [                                                                             
    tf.feature_column.indicator_column(                                                               
        tf.feature_column.categorical_column_with_vocabulary_list(                                    
            feature_name, vocabulary_list=car_data[feature_name].unique()))                           
    for feature_name in categorical_feature_names                                                     
] + [                                                                                                 
    tf.feature_column.numeric_column(                                                                 
        feature_name,                                                                                 
        normalizer_fn=lambda val, fn=feature_name, m=numeric_means, s=numeric_stds: (val - m[fn]) /   
(epsilon + s[fn]))                                                                                    
    for feature_name in numeric_feature_names                                                         
]                                                                                                     
                                                                                                    
# T4.1 — lr=0.01 (baseline, same as T1 best config)                                                   
est_t4_lr1 = tf.estimator.DNNRegressor(                                                               
    feature_columns=model_feature_columns,                                                            
    hidden_units=[64],                                                                                
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.01),                                          
)                                                                                                     
for _ in range(num_print_statements):                                                                 
    est_t4_lr1.train(train_input_fn, steps=num_training_steps // num_print_statements)                
    scores = est_t4_lr1.evaluate(eval_input_fn)                                                       
    print('scores_t4_lr1', scores)                                                                    
                                                                                                    
# T4.2 — lr=0.5 (T3 showed higher lr helps with sparse/normalised inputs)                             
est_t4_lr2 = tf.estimator.DNNRegressor(                                                               
    feature_columns=model_feature_columns,                                                            
    hidden_units=[64],                                                                                
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.5),                                           
)                                                                                                     
for _ in range(num_print_statements):                                                                 
    est_t4_lr2.train(train_input_fn, steps=num_training_steps // num_print_statements)                
    scores = est_t4_lr2.evaluate(eval_input_fn)                                                       
    print('scores_t4_lr2', scores)
```

    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 5215286300.0, step = 1
    INFO:tensorflow:global_step/sec: 1036.56
    INFO:tensorflow:loss = 4202886700.0, step = 101 (0.097 sec)
    INFO:tensorflow:global_step/sec: 746.535
    INFO:tensorflow:loss = 3296886300.0, step = 201 (0.135 sec)
    INFO:tensorflow:global_step/sec: 1260.35
    INFO:tensorflow:loss = 2448789000.0, step = 301 (0.079 sec)
    INFO:tensorflow:global_step/sec: 1612.78
    INFO:tensorflow:loss = 4370744300.0, step = 401 (0.062 sec)
    INFO:tensorflow:global_step/sec: 1707.22
    INFO:tensorflow:loss = 3762483500.0, step = 501 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1476.49
    INFO:tensorflow:loss = 2580474600.0, step = 601 (0.068 sec)
    INFO:tensorflow:global_step/sec: 1673
    INFO:tensorflow:loss = 3315981800.0, step = 701 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1716.56
    INFO:tensorflow:loss = 2974525700.0, step = 801 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1753.34
    INFO:tensorflow:loss = 4767961000.0, step = 901 (0.058 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3560374800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13885s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:39
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 225749840.0, global_step = 1000, label/mean = 13207.129, loss = 3490439700.0, prediction/mean = 355.79456
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-1000
    scores_t4_lr1 {'average_loss': 225749840.0, 'label/mean': 13207.129, 'loss': 3490439700.0, 'prediction/mean': 355.79456, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 5774993400.0, step = 1001
    INFO:tensorflow:global_step/sec: 570.142
    INFO:tensorflow:loss = 2113478400.0, step = 1101 (0.177 sec)
    INFO:tensorflow:global_step/sec: 1808.28
    INFO:tensorflow:loss = 2078189300.0, step = 1201 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1795.88
    INFO:tensorflow:loss = 4346737000.0, step = 1301 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1768.76
    INFO:tensorflow:loss = 1492607200.0, step = 1401 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1734.99
    INFO:tensorflow:loss = 3588052500.0, step = 1501 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1726.88
    INFO:tensorflow:loss = 2892609500.0, step = 1601 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1622.41
    INFO:tensorflow:loss = 2091936800.0, step = 1701 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1749.62
    INFO:tensorflow:loss = 3865644300.0, step = 1801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1783.39
    INFO:tensorflow:loss = 1754850300.0, step = 1901 (0.056 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 3229018400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:42
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13607s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:42
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 214545140.0, global_step = 2000, label/mean = 13207.129, loss = 3317197800.0, prediction/mean = 709.8951
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-2000
    scores_t4_lr1 {'average_loss': 214545140.0, 'label/mean': 13207.129, 'loss': 3317197800.0, 'prediction/mean': 709.8951, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2941900300.0, step = 2001
    INFO:tensorflow:global_step/sec: 1051.6
    INFO:tensorflow:loss = 3853325000.0, step = 2101 (0.096 sec)
    INFO:tensorflow:global_step/sec: 1762.33
    INFO:tensorflow:loss = 3346003000.0, step = 2201 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1644.93
    INFO:tensorflow:loss = 3990199800.0, step = 2301 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1793.33
    INFO:tensorflow:loss = 5547458600.0, step = 2401 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1768.97
    INFO:tensorflow:loss = 4075517200.0, step = 2501 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1768.09
    INFO:tensorflow:loss = 2923630300.0, step = 2601 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1740.5
    INFO:tensorflow:loss = 3921968400.0, step = 2701 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1792.6
    INFO:tensorflow:loss = 1388437400.0, step = 2801 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1779.89
    INFO:tensorflow:loss = 3954540000.0, step = 2901 (0.056 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 3357063200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12857s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:44
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 203791410.0, global_step = 3000, label/mean = 13207.129, loss = 3150928600.0, prediction/mean = 1057.9777
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-3000
    scores_t4_lr1 {'average_loss': 203791410.0, 'label/mean': 13207.129, 'loss': 3150928600.0, 'prediction/mean': 1057.9777, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 1734011300.0, step = 3001
    INFO:tensorflow:global_step/sec: 1016.03
    INFO:tensorflow:loss = 2402243000.0, step = 3101 (0.100 sec)
    INFO:tensorflow:global_step/sec: 1664.28
    INFO:tensorflow:loss = 4920218600.0, step = 3201 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1794.27
    INFO:tensorflow:loss = 3158195000.0, step = 3301 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1772.04
    INFO:tensorflow:loss = 2443672000.0, step = 3401 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1796.88
    INFO:tensorflow:loss = 4070345700.0, step = 3501 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1783.22
    INFO:tensorflow:loss = 2427896000.0, step = 3601 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1826.95
    INFO:tensorflow:loss = 5088678400.0, step = 3701 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1818.15
    INFO:tensorflow:loss = 2993993700.0, step = 3801 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1741.16
    INFO:tensorflow:loss = 2010656000.0, step = 3901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 1922708500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:46
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13268s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:46
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 193566450.0, global_step = 4000, label/mean = 13207.129, loss = 2992835000.0, prediction/mean = 1398.7234
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-4000
    scores_t4_lr1 {'average_loss': 193566450.0, 'label/mean': 13207.129, 'loss': 2992835000.0, 'prediction/mean': 1398.7234, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 3737114600.0, step = 4001
    INFO:tensorflow:global_step/sec: 1083.34
    INFO:tensorflow:loss = 2600906200.0, step = 4101 (0.094 sec)
    INFO:tensorflow:global_step/sec: 1776.58
    INFO:tensorflow:loss = 2544385500.0, step = 4201 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1718.87
    INFO:tensorflow:loss = 3265040400.0, step = 4301 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1790.16
    INFO:tensorflow:loss = 1455749600.0, step = 4401 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1735.69
    INFO:tensorflow:loss = 2561936000.0, step = 4501 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1696.81
    INFO:tensorflow:loss = 1902626200.0, step = 4601 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1718.72
    INFO:tensorflow:loss = 3503933400.0, step = 4701 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1733.61
    INFO:tensorflow:loss = 2840712400.0, step = 4801 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1757.96
    INFO:tensorflow:loss = 3067082200.0, step = 4901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 1851720200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:48
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13237s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:48
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 183781630.0, global_step = 5000, label/mean = 13207.129, loss = 2841546800.0, prediction/mean = 1734.0907
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-5000
    scores_t4_lr1 {'average_loss': 183781630.0, 'label/mean': 13207.129, 'loss': 2841546800.0, 'prediction/mean': 1734.0907, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 2221769200.0, step = 5001
    INFO:tensorflow:global_step/sec: 1045.74
    INFO:tensorflow:loss = 1628488400.0, step = 5101 (0.097 sec)
    INFO:tensorflow:global_step/sec: 1761.83
    INFO:tensorflow:loss = 3244763400.0, step = 5201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1751.65
    INFO:tensorflow:loss = 3071818200.0, step = 5301 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1762.24
    INFO:tensorflow:loss = 1268549500.0, step = 5401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1777.44
    INFO:tensorflow:loss = 2860211500.0, step = 5501 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1766.34
    INFO:tensorflow:loss = 2114910700.0, step = 5601 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1711.51
    INFO:tensorflow:loss = 2590686700.0, step = 5701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1718.83
    INFO:tensorflow:loss = 2500606200.0, step = 5801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1732.72
    INFO:tensorflow:loss = 2969946000.0, step = 5901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 3125607400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:50
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12897s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:50
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 174405580.0, global_step = 6000, label/mean = 13207.129, loss = 2696578600.0, prediction/mean = 2064.4639
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-6000
    scores_t4_lr1 {'average_loss': 174405580.0, 'label/mean': 13207.129, 'loss': 2696578600.0, 'prediction/mean': 2064.4639, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 3572470000.0, step = 6001
    INFO:tensorflow:global_step/sec: 1078.9
    INFO:tensorflow:loss = 2075414700.0, step = 6101 (0.094 sec)
    INFO:tensorflow:global_step/sec: 1756.64
    INFO:tensorflow:loss = 1998248100.0, step = 6201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1627.6
    INFO:tensorflow:loss = 2806096000.0, step = 6301 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1742.98
    INFO:tensorflow:loss = 3429664300.0, step = 6401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1753.52
    INFO:tensorflow:loss = 3302383000.0, step = 6501 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1782.16
    INFO:tensorflow:loss = 3255296800.0, step = 6601 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1751.59
    INFO:tensorflow:loss = 2186480000.0, step = 6701 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1810.57
    INFO:tensorflow:loss = 3971611600.0, step = 6801 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1765.08
    INFO:tensorflow:loss = 2631325700.0, step = 6901 (0.058 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 1699994800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:52
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13026s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:52
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 165468800.0, global_step = 7000, label/mean = 13207.129, loss = 2558402300.0, prediction/mean = 2388.7908
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-7000
    scores_t4_lr1 {'average_loss': 165468800.0, 'label/mean': 13207.129, 'loss': 2558402300.0, 'prediction/mean': 2388.7908, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 2355270100.0, step = 7001
    INFO:tensorflow:global_step/sec: 976.523
    INFO:tensorflow:loss = 2620957400.0, step = 7101 (0.104 sec)
    INFO:tensorflow:global_step/sec: 1742.19
    INFO:tensorflow:loss = 2953608400.0, step = 7201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1738.9
    INFO:tensorflow:loss = 2049504800.0, step = 7301 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1804.4
    INFO:tensorflow:loss = 3121649700.0, step = 7401 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1742.1
    INFO:tensorflow:loss = 2017339100.0, step = 7501 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1873.36
    INFO:tensorflow:loss = 1949150800.0, step = 7601 (0.054 sec)
    INFO:tensorflow:global_step/sec: 1720.64
    INFO:tensorflow:loss = 3665413400.0, step = 7701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1807.62
    INFO:tensorflow:loss = 3112323300.0, step = 7801 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1809.34
    INFO:tensorflow:loss = 4589686000.0, step = 7901 (0.055 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 3180702700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13122s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:55
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 156954770.0, global_step = 8000, label/mean = 13207.129, loss = 2426762200.0, prediction/mean = 2707.1555
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-8000
    scores_t4_lr1 {'average_loss': 156954770.0, 'label/mean': 13207.129, 'loss': 2426762200.0, 'prediction/mean': 2707.1555, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 1767195600.0, step = 8001
    INFO:tensorflow:global_step/sec: 1075.56
    INFO:tensorflow:loss = 1364251600.0, step = 8101 (0.094 sec)
    INFO:tensorflow:global_step/sec: 1699.91
    INFO:tensorflow:loss = 1663753000.0, step = 8201 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1765.62
    INFO:tensorflow:loss = 2125949400.0, step = 8301 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1697.1
    INFO:tensorflow:loss = 1615780700.0, step = 8401 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1646.04
    INFO:tensorflow:loss = 1710716300.0, step = 8501 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1715.53
    INFO:tensorflow:loss = 3975209000.0, step = 8601 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1692.59
    INFO:tensorflow:loss = 1860030800.0, step = 8701 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1730.34
    INFO:tensorflow:loss = 2626411000.0, step = 8801 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1762.37
    INFO:tensorflow:loss = 2323767800.0, step = 8901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 2445445400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.36101s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:57
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 148838900.0, global_step = 9000, label/mean = 13207.129, loss = 2301278200.0, prediction/mean = 3019.87
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-9000
    scores_t4_lr1 {'average_loss': 148838900.0, 'label/mean': 13207.129, 'loss': 2301278200.0, 'prediction/mean': 3019.87, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 2898239500.0, step = 9001
    INFO:tensorflow:global_step/sec: 1067.51
    INFO:tensorflow:loss = 2087746800.0, step = 9101 (0.095 sec)
    INFO:tensorflow:global_step/sec: 1799.98
    INFO:tensorflow:loss = 1417988400.0, step = 9201 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1775.92
    INFO:tensorflow:loss = 2286892800.0, step = 9301 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1758.46
    INFO:tensorflow:loss = 2864817200.0, step = 9401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1778.12
    INFO:tensorflow:loss = 2017174900.0, step = 9501 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1672.04
    INFO:tensorflow:loss = 1757441300.0, step = 9601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1715.86
    INFO:tensorflow:loss = 2309043200.0, step = 9701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1691.61
    INFO:tensorflow:loss = 3012063200.0, step = 9801 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1679.77
    INFO:tensorflow:loss = 2120175600.0, step = 9901 (0.060 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 2438551600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:51:59
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13073s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:51:59
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 141106200.0, global_step = 10000, label/mean = 13207.129, loss = 2181719000.0, prediction/mean = 3326.9646
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprzcs23ux/model.ckpt-10000
    scores_t4_lr1 {'average_loss': 141106200.0, 'label/mean': 13207.129, 'loss': 2181719000.0, 'prediction/mean': 3326.9646, 'global_step': 10000}
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 3044527000.0, step = 1
    INFO:tensorflow:global_step/sec: 987.653
    INFO:tensorflow:loss = 145491400.0, step = 101 (0.103 sec)
    INFO:tensorflow:global_step/sec: 1599.16
    INFO:tensorflow:loss = 102658984.0, step = 201 (0.062 sec)
    INFO:tensorflow:global_step/sec: 1688.79
    INFO:tensorflow:loss = 37234824.0, step = 301 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1670.87
    INFO:tensorflow:loss = 40607750.0, step = 401 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1726.46
    INFO:tensorflow:loss = 55960596.0, step = 501 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1699.64
    INFO:tensorflow:loss = 58856610.0, step = 601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1752.17
    INFO:tensorflow:loss = 92238400.0, step = 701 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1795.54
    INFO:tensorflow:loss = 27189424.0, step = 801 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1712.27
    INFO:tensorflow:loss = 47611660.0, step = 901 (0.059 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 22762944.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13961s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:02
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 2080236.0, global_step = 1000, label/mean = 13207.129, loss = 32163648.0, prediction/mean = 13246.783
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-1000
    scores_t4_lr2 {'average_loss': 2080236.0, 'label/mean': 13207.129, 'loss': 32163648.0, 'prediction/mean': 13246.783, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 38768020.0, step = 1001
    INFO:tensorflow:global_step/sec: 992.634
    INFO:tensorflow:loss = 13696528.0, step = 1101 (0.103 sec)
    INFO:tensorflow:global_step/sec: 1689.13
    INFO:tensorflow:loss = 45970932.0, step = 1201 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1737.98
    INFO:tensorflow:loss = 25039080.0, step = 1301 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1707.97
    INFO:tensorflow:loss = 10332328.0, step = 1401 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1775.34
    INFO:tensorflow:loss = 80540536.0, step = 1501 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1728.28
    INFO:tensorflow:loss = 31337788.0, step = 1601 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1775.19
    INFO:tensorflow:loss = 75579250.0, step = 1701 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1751.65
    INFO:tensorflow:loss = 23054024.0, step = 1801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1712.01
    INFO:tensorflow:loss = 19690954.0, step = 1901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 23187704.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:04
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13462s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:04
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 1460725.4, global_step = 2000, label/mean = 13207.129, loss = 22585060.0, prediction/mean = 13246.719
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-2000
    scores_t4_lr2 {'average_loss': 1460725.4, 'label/mean': 13207.129, 'loss': 22585060.0, 'prediction/mean': 13246.719, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 28506100.0, step = 2001
    INFO:tensorflow:global_step/sec: 994.769
    INFO:tensorflow:loss = 7768243.5, step = 2101 (0.101 sec)
    INFO:tensorflow:global_step/sec: 1747.03
    INFO:tensorflow:loss = 22755238.0, step = 2201 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1761.25
    INFO:tensorflow:loss = 16436171.0, step = 2301 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1760.87
    INFO:tensorflow:loss = 101142460.0, step = 2401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1726.61
    INFO:tensorflow:loss = 7772650.5, step = 2501 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1792.83
    INFO:tensorflow:loss = 9420072.0, step = 2601 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1721.47
    INFO:tensorflow:loss = 24828136.0, step = 2701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1725.89
    INFO:tensorflow:loss = 50591096.0, step = 2801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1717.41
    INFO:tensorflow:loss = 20400576.0, step = 2901 (0.059 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 5242590.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:06
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13561s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:07
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 1240005.9, global_step = 3000, label/mean = 13207.129, loss = 19172398.0, prediction/mean = 13240.694
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-3000
    scores_t4_lr2 {'average_loss': 1240005.9, 'label/mean': 13207.129, 'loss': 19172398.0, 'prediction/mean': 13240.694, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 26216634.0, step = 3001
    INFO:tensorflow:global_step/sec: 1038.63
    INFO:tensorflow:loss = 31884194.0, step = 3101 (0.098 sec)
    INFO:tensorflow:global_step/sec: 1740.1
    INFO:tensorflow:loss = 13221606.0, step = 3201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1744.55
    INFO:tensorflow:loss = 10053805.0, step = 3301 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1680.76
    INFO:tensorflow:loss = 29665166.0, step = 3401 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1600.72
    INFO:tensorflow:loss = 11441669.0, step = 3501 (0.062 sec)
    INFO:tensorflow:global_step/sec: 1716.23
    INFO:tensorflow:loss = 16575272.0, step = 3601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1372.44
    INFO:tensorflow:loss = 17976416.0, step = 3701 (0.077 sec)
    INFO:tensorflow:global_step/sec: 1220.65
    INFO:tensorflow:loss = 17933308.0, step = 3801 (0.079 sec)
    INFO:tensorflow:global_step/sec: 1340.73
    INFO:tensorflow:loss = 20323128.0, step = 3901 (0.075 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 15191492.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:09
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13754s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:09
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 1119757.9, global_step = 4000, label/mean = 13207.129, loss = 17313180.0, prediction/mean = 13281.651
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-4000
    scores_t4_lr2 {'average_loss': 1119757.9, 'label/mean': 13207.129, 'loss': 17313180.0, 'prediction/mean': 13281.651, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 10407410.0, step = 4001
    INFO:tensorflow:global_step/sec: 986.786
    INFO:tensorflow:loss = 7168920.0, step = 4101 (0.103 sec)
    INFO:tensorflow:global_step/sec: 1627.47
    INFO:tensorflow:loss = 30956696.0, step = 4201 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1465.87
    INFO:tensorflow:loss = 16275822.0, step = 4301 (0.068 sec)
    INFO:tensorflow:global_step/sec: 1752.51
    INFO:tensorflow:loss = 6736461.5, step = 4401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1669.59
    INFO:tensorflow:loss = 21012978.0, step = 4501 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1761.71
    INFO:tensorflow:loss = 13492484.0, step = 4601 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1743.23
    INFO:tensorflow:loss = 18214792.0, step = 4701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1570.28
    INFO:tensorflow:loss = 25926668.0, step = 4801 (0.063 sec)
    INFO:tensorflow:global_step/sec: 1746.3
    INFO:tensorflow:loss = 11249541.0, step = 4901 (0.058 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 15873754.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:11
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13209s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:11
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 1028005.2, global_step = 5000, label/mean = 13207.129, loss = 15894542.0, prediction/mean = 13228.391
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-5000
    scores_t4_lr2 {'average_loss': 1028005.2, 'label/mean': 13207.129, 'loss': 15894542.0, 'prediction/mean': 13228.391, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 42124670.0, step = 5001
    INFO:tensorflow:global_step/sec: 1045.77
    INFO:tensorflow:loss = 8459801.0, step = 5101 (0.097 sec)
    INFO:tensorflow:global_step/sec: 1728.73
    INFO:tensorflow:loss = 12298661.0, step = 5201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1711.74
    INFO:tensorflow:loss = 18201638.0, step = 5301 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1758.61
    INFO:tensorflow:loss = 16538589.0, step = 5401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1668.89
    INFO:tensorflow:loss = 5879009.5, step = 5501 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1753.19
    INFO:tensorflow:loss = 44185096.0, step = 5601 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1753.35
    INFO:tensorflow:loss = 11208056.0, step = 5701 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1753.21
    INFO:tensorflow:loss = 56795830.0, step = 5801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1761.34
    INFO:tensorflow:loss = 17617072.0, step = 5901 (0.057 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 20870824.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13655s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:14
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 968390.5, global_step = 6000, label/mean = 13207.129, loss = 14972807.0, prediction/mean = 13189.287
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-6000
    scores_t4_lr2 {'average_loss': 968390.5, 'label/mean': 13207.129, 'loss': 14972807.0, 'prediction/mean': 13189.287, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 14310515.0, step = 6001
    INFO:tensorflow:global_step/sec: 802.589
    INFO:tensorflow:loss = 17597746.0, step = 6101 (0.127 sec)
    INFO:tensorflow:global_step/sec: 1529.73
    INFO:tensorflow:loss = 12712258.0, step = 6201 (0.065 sec)
    INFO:tensorflow:global_step/sec: 1600.82
    INFO:tensorflow:loss = 15764417.0, step = 6301 (0.062 sec)
    INFO:tensorflow:global_step/sec: 1601.61
    INFO:tensorflow:loss = 17499120.0, step = 6401 (0.063 sec)
    INFO:tensorflow:global_step/sec: 1619.33
    INFO:tensorflow:loss = 6244007.0, step = 6501 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1691.02
    INFO:tensorflow:loss = 18889532.0, step = 6601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1726.79
    INFO:tensorflow:loss = 4854438.5, step = 6701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1653.9
    INFO:tensorflow:loss = 8085075.5, step = 6801 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1662.18
    INFO:tensorflow:loss = 48396132.0, step = 6901 (0.060 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 12429512.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:16
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.14399s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:16
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 924982.75, global_step = 7000, label/mean = 13207.129, loss = 14301657.0, prediction/mean = 13173.552
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-7000
    scores_t4_lr2 {'average_loss': 924982.75, 'label/mean': 13207.129, 'loss': 14301657.0, 'prediction/mean': 13173.552, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 9225154.0, step = 7001
    INFO:tensorflow:global_step/sec: 867.025
    INFO:tensorflow:loss = 21784070.0, step = 7101 (0.118 sec)
    INFO:tensorflow:global_step/sec: 1418.14
    INFO:tensorflow:loss = 8069539.0, step = 7201 (0.070 sec)
    INFO:tensorflow:global_step/sec: 1393.53
    INFO:tensorflow:loss = 18118908.0, step = 7301 (0.072 sec)
    INFO:tensorflow:global_step/sec: 1416.23
    INFO:tensorflow:loss = 10246185.0, step = 7401 (0.070 sec)
    INFO:tensorflow:global_step/sec: 1472.06
    INFO:tensorflow:loss = 19200700.0, step = 7501 (0.067 sec)
    INFO:tensorflow:global_step/sec: 1205.24
    INFO:tensorflow:loss = 14698351.0, step = 7601 (0.084 sec)
    INFO:tensorflow:global_step/sec: 1323.54
    INFO:tensorflow:loss = 9131552.0, step = 7701 (0.076 sec)
    INFO:tensorflow:global_step/sec: 1029.75
    INFO:tensorflow:loss = 15154276.0, step = 7801 (0.099 sec)
    INFO:tensorflow:global_step/sec: 772.575
    INFO:tensorflow:loss = 3646606.5, step = 7901 (0.131 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 10118460.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:19
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.17598s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:19
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 888571.94, global_step = 8000, label/mean = 13207.129, loss = 13738689.0, prediction/mean = 13232.301
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-8000
    scores_t4_lr2 {'average_loss': 888571.94, 'label/mean': 13207.129, 'loss': 13738689.0, 'prediction/mean': 13232.301, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 11744453.0, step = 8001
    INFO:tensorflow:global_step/sec: 905.934
    INFO:tensorflow:loss = 19461188.0, step = 8101 (0.112 sec)
    INFO:tensorflow:global_step/sec: 1674.66
    INFO:tensorflow:loss = 11941408.0, step = 8201 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1734.09
    INFO:tensorflow:loss = 8916643.0, step = 8301 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1748.04
    INFO:tensorflow:loss = 5988021.0, step = 8401 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1768.47
    INFO:tensorflow:loss = 4606203.0, step = 8501 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1678.31
    INFO:tensorflow:loss = 11842065.0, step = 8601 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1658.92
    INFO:tensorflow:loss = 8769953.0, step = 8701 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1594.03
    INFO:tensorflow:loss = 17459536.0, step = 8801 (0.063 sec)
    INFO:tensorflow:global_step/sec: 1544.02
    INFO:tensorflow:loss = 4490634.5, step = 8901 (0.066 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 27414442.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.14314s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:22
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 857750.44, global_step = 9000, label/mean = 13207.129, loss = 13262142.0, prediction/mean = 13205.127
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-9000
    scores_t4_lr2 {'average_loss': 857750.44, 'label/mean': 13207.129, 'loss': 13262142.0, 'prediction/mean': 13205.127, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 13519642.0, step = 9001
    INFO:tensorflow:global_step/sec: 1028.79
    INFO:tensorflow:loss = 16821718.0, step = 9101 (0.099 sec)
    INFO:tensorflow:global_step/sec: 1663.45
    INFO:tensorflow:loss = 13129866.0, step = 9201 (0.060 sec)
    INFO:tensorflow:global_step/sec: 1713.15
    INFO:tensorflow:loss = 8264646.5, step = 9301 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1753.74
    INFO:tensorflow:loss = 34200530.0, step = 9401 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1746.42
    INFO:tensorflow:loss = 11726894.0, step = 9501 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1738.56
    INFO:tensorflow:loss = 9096429.0, step = 9601 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1726.49
    INFO:tensorflow:loss = 20442070.0, step = 9701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1753.43
    INFO:tensorflow:loss = 17343754.0, step = 9801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1732.78
    INFO:tensorflow:loss = 12208158.0, step = 9901 (0.056 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 8499705.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-03T07:52:24
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13260s
    INFO:tensorflow:Finished evaluation at 2026-04-03-07:52:24
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 835841.5, global_step = 10000, label/mean = 13207.129, loss = 12923396.0, prediction/mean = 13242.1045
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpc9v7j0hh/model.ckpt-10000
    scores_t4_lr2 {'average_loss': 835841.5, 'label/mean': 13207.129, 'loss': 12923396.0, 'prediction/mean': 13242.1045, 'global_step': 10000}



```python
# codex resume ISY-assessment2
# claude --resume "ISY-assessment2"
```
