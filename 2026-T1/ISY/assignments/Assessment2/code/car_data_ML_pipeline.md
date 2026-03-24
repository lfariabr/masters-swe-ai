# Programming Task
> jupyter nbconvert --to markdown car_data_ML_pipeline.ipynb 

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

### Libraries + Setup


```python
# 1. Clear workspace (use in Jupyter/IPython)
%reset -f

# 2. Standard Imports
import numpy as np
import pandas as pd
import math
# Correct and specific sklearn imports
from sklearn import preprocessing, decomposition

# 3. TensorFlow Setup (if needed for older code)
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# 4. Set pandas output display settings
pd.options.display.float_format = '{:.2f}'.format
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
      <th>59</th>
      <td>1</td>
      <td>129</td>
      <td>mazda</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>fwd</td>
      <td>front</td>
      <td>98.80</td>
      <td>...</td>
      <td>122</td>
      <td>2bbl</td>
      <td>3.39</td>
      <td>3.39</td>
      <td>8.60</td>
      <td>84</td>
      <td>4800</td>
      <td>26</td>
      <td>32</td>
      <td>8845</td>
    </tr>
    <tr>
      <th>115</th>
      <td>0</td>
      <td>161</td>
      <td>peugot</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>rwd</td>
      <td>front</td>
      <td>107.90</td>
      <td>...</td>
      <td>120</td>
      <td>mpfi</td>
      <td>3.46</td>
      <td>3.19</td>
      <td>8.40</td>
      <td>97</td>
      <td>5000</td>
      <td>19</td>
      <td>24</td>
      <td>16630</td>
    </tr>
    <tr>
      <th>91</th>
      <td>1</td>
      <td>128</td>
      <td>nissan</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>94.50</td>
      <td>...</td>
      <td>97</td>
      <td>2bbl</td>
      <td>3.15</td>
      <td>3.29</td>
      <td>9.40</td>
      <td>69</td>
      <td>5200</td>
      <td>31</td>
      <td>37</td>
      <td>6649</td>
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
    Index: 205 entries, 155 to 183
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
      <th>155</th>
      <td>0</td>
      <td>91</td>
      <td>95.70</td>
      <td>169.70</td>
      <td>63.60</td>
      <td>59.10</td>
      <td>3110</td>
      <td>92</td>
      <td>62</td>
      <td>4800</td>
      <td>27</td>
      <td>32</td>
      <td>3.05</td>
      <td>3.03</td>
      <td>9.00</td>
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
      <th>50</th>
      <td>1</td>
      <td>104</td>
      <td>93.10</td>
      <td>159.10</td>
      <td>64.20</td>
      <td>54.10</td>
      <td>1890</td>
      <td>91</td>
      <td>68</td>
      <td>5000</td>
      <td>30</td>
      <td>31</td>
      <td>3.03</td>
      <td>3.15</td>
      <td>9.00</td>
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
      <th>59</th>
      <td>1</td>
      <td>129</td>
      <td>98.80</td>
      <td>177.80</td>
      <td>66.50</td>
      <td>53.70</td>
      <td>2385</td>
      <td>122</td>
      <td>84</td>
      <td>4800</td>
      <td>26</td>
      <td>32</td>
      <td>3.39</td>
      <td>3.39</td>
      <td>8.60</td>
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
      <th>158</th>
      <td>0</td>
      <td>91</td>
      <td>95.70</td>
      <td>166.30</td>
      <td>64.40</td>
      <td>53.00</td>
      <td>2275</td>
      <td>110</td>
      <td>56</td>
      <td>4500</td>
      <td>34</td>
      <td>36</td>
      <td>3.27</td>
      <td>3.35</td>
      <td>22.50</td>
    </tr>
    <tr>
      <th>24</th>
      <td>1</td>
      <td>148</td>
      <td>93.70</td>
      <td>157.30</td>
      <td>63.80</td>
      <td>50.60</td>
      <td>1967</td>
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
      <th>146</th>
      <td>0</td>
      <td>89</td>
      <td>97.00</td>
      <td>173.50</td>
      <td>65.40</td>
      <td>53.00</td>
      <td>2290</td>
      <td>108</td>
      <td>82</td>
      <td>4800</td>
      <td>28</td>
      <td>32</td>
      <td>3.62</td>
      <td>2.64</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>42</th>
      <td>1</td>
      <td>107</td>
      <td>96.50</td>
      <td>169.10</td>
      <td>66.00</td>
      <td>51.00</td>
      <td>2293</td>
      <td>110</td>
      <td>100</td>
      <td>5500</td>
      <td>25</td>
      <td>31</td>
      <td>3.15</td>
      <td>3.58</td>
      <td>9.10</td>
    </tr>
    <tr>
      <th>183</th>
      <td>2</td>
      <td>122</td>
      <td>97.30</td>
      <td>171.70</td>
      <td>65.50</td>
      <td>55.70</td>
      <td>2209</td>
      <td>109</td>
      <td>85</td>
      <td>5250</td>
      <td>27</td>
      <td>34</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>9.00</td>
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
      <th>engine-location</th>
      <th>fuel-system</th>
      <th>aspiration</th>
      <th>fuel-type</th>
      <th>engine-type</th>
      <th>drive-wheels</th>
      <th>num-cylinders</th>
      <th>make</th>
      <th>body-style</th>
      <th>num-doors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>155</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>4wd</td>
      <td>four</td>
      <td>toyota</td>
      <td>wagon</td>
      <td>four</td>
    </tr>
    <tr>
      <th>86</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>mitsubishi</td>
      <td>sedan</td>
      <td>four</td>
    </tr>
    <tr>
      <th>50</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>mazda</td>
      <td>hatchback</td>
      <td>two</td>
    </tr>
    <tr>
      <th>185</th>
      <td>front</td>
      <td>mpfi</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>volkswagen</td>
      <td>sedan</td>
      <td>four</td>
    </tr>
    <tr>
      <th>59</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>mazda</td>
      <td>hatchback</td>
      <td>two</td>
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
      <th>158</th>
      <td>front</td>
      <td>idi</td>
      <td>std</td>
      <td>diesel</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>toyota</td>
      <td>sedan</td>
      <td>four</td>
    </tr>
    <tr>
      <th>24</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>dodge</td>
      <td>hatchback</td>
      <td>four</td>
    </tr>
    <tr>
      <th>146</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohcf</td>
      <td>fwd</td>
      <td>four</td>
      <td>subaru</td>
      <td>wagon</td>
      <td>four</td>
    </tr>
    <tr>
      <th>42</th>
      <td>front</td>
      <td>2bbl</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>honda</td>
      <td>sedan</td>
      <td>two</td>
    </tr>
    <tr>
      <th>183</th>
      <td>front</td>
      <td>mpfi</td>
      <td>std</td>
      <td>gas</td>
      <td>ohc</td>
      <td>fwd</td>
      <td>four</td>
      <td>volkswagen</td>
      <td>sedan</td>
      <td>two</td>
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
    
    WARNING:tensorflow:From /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/ipykernel_46070/741504662.py:29: The name tf.estimator.inputs.pandas_input_fn is deprecated. Please use tf.compat.v1.estimator.inputs.pandas_input_fn instead.
    
    model_feature_columns [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
    Metal device set to: Apple M3
    
    systemMemory: 8.00 GB
    maxCacheSize: 2.67 GB
    
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:910: start_queue_runners (from tensorflow.python.training.queue_runner_impl) is deprecated and will be removed in a future version.
    Instructions for updating:
    To construct input pipelines, use the `tf.data` module.


    2026-03-25 08:47:17.002204: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:17.002321: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:17.019081: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:17.019098: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:17.023108: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
    2026-03-25 08:47:17.029280: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz
    2026-03-25 08:47:17.035291: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.071268: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.079063: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.082037: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.088933: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.093427: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...


    2026-03-25 08:47:17.567693: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:17.750730: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2410854000.0, step = 1


    2026-03-25 08:47:17.910041: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 227.318
    INFO:tensorflow:loss = 234009600.0, step = 101 (0.440 sec)
    INFO:tensorflow:global_step/sec: 260.68
    INFO:tensorflow:loss = 1255246100.0, step = 201 (0.384 sec)
    INFO:tensorflow:global_step/sec: 275.258
    INFO:tensorflow:loss = 339427200.0, step = 301 (0.363 sec)
    INFO:tensorflow:global_step/sec: 249.373
    INFO:tensorflow:loss = 685035700.0, step = 401 (0.403 sec)
    INFO:tensorflow:global_step/sec: 260.951
    INFO:tensorflow:loss = 512756700.0, step = 501 (0.382 sec)
    INFO:tensorflow:global_step/sec: 270.62
    INFO:tensorflow:loss = 1542246000.0, step = 601 (0.369 sec)
    INFO:tensorflow:global_step/sec: 199.525
    INFO:tensorflow:loss = 725255740.0, step = 701 (0.501 sec)
    INFO:tensorflow:global_step/sec: 246.807
    INFO:tensorflow:loss = 504033730.0, step = 801 (0.407 sec)
    INFO:tensorflow:global_step/sec: 182.961
    INFO:tensorflow:loss = 233271570.0, step = 901 (0.545 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 691079200.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:47:22.443849: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.486023: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:22.680346: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:22.680361: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:22.686594: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.693554: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.698890: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.704471: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.711762: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.715271: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:22.746057: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.33007s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:22
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 40438024.0, global_step = 1000, label/mean = 13207.129, loss = 625234050.0, prediction/mean = 13137.515


    2026-03-25 08:47:22.925912: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-1000
    scores {'average_loss': 40438024.0, 'label/mean': 13207.129, 'loss': 625234050.0, 'prediction/mean': 13137.515, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-1000
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1173: get_checkpoint_mtimes (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file utilities to get mtimes.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:23.359723: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:23.359737: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:23.364991: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.371187: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.376820: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.379220: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.385141: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.388437: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 1785007600.0, step = 1001


    2026-03-25 08:47:23.705686: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.804534: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:23.897507: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 230.743
    INFO:tensorflow:loss = 769561860.0, step = 1101 (0.434 sec)
    INFO:tensorflow:global_step/sec: 267.38
    INFO:tensorflow:loss = 734286400.0, step = 1201 (0.374 sec)
    INFO:tensorflow:global_step/sec: 269.633
    INFO:tensorflow:loss = 494939070.0, step = 1301 (0.371 sec)
    INFO:tensorflow:global_step/sec: 259.194
    INFO:tensorflow:loss = 830969400.0, step = 1401 (0.386 sec)
    INFO:tensorflow:global_step/sec: 238.61
    INFO:tensorflow:loss = 696387300.0, step = 1501 (0.419 sec)
    INFO:tensorflow:global_step/sec: 207.505
    INFO:tensorflow:loss = 385715840.0, step = 1601 (0.483 sec)
    INFO:tensorflow:global_step/sec: 265.914
    INFO:tensorflow:loss = 701218000.0, step = 1701 (0.376 sec)
    INFO:tensorflow:global_step/sec: 269.863
    INFO:tensorflow:loss = 571304600.0, step = 1801 (0.370 sec)
    INFO:tensorflow:global_step/sec: 244.079
    INFO:tensorflow:loss = 184310560.0, step = 1901 (0.410 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 174806930.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:28
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-2000


    2026-03-25 08:47:28.055339: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.063245: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.250831: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:28.250845: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:28.256472: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.261809: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.267406: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.273467: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.280839: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.284597: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.313724: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26907s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:28
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 30568870.0, global_step = 2000, label/mean = 13207.129, loss = 472641760.0, prediction/mean = 13447.633
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-2000
    scores {'average_loss': 30568870.0, 'label/mean': 13207.129, 'loss': 472641760.0, 'prediction/mean': 13447.633, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:28.457891: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.613062: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:28.613076: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:28.618512: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.624380: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.629927: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.632352: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.638258: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:28.641802: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...


    2026-03-25 08:47:28.961400: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:29.060228: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 956131400.0, step = 2001


    2026-03-25 08:47:29.168122: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 220.444
    INFO:tensorflow:loss = 226467840.0, step = 2101 (0.454 sec)
    INFO:tensorflow:global_step/sec: 222.507
    INFO:tensorflow:loss = 800679300.0, step = 2201 (0.450 sec)
    INFO:tensorflow:global_step/sec: 261.868
    INFO:tensorflow:loss = 472692600.0, step = 2301 (0.382 sec)
    INFO:tensorflow:global_step/sec: 274.743
    INFO:tensorflow:loss = 928718300.0, step = 2401 (0.364 sec)
    INFO:tensorflow:global_step/sec: 278.161
    INFO:tensorflow:loss = 1202778400.0, step = 2501 (0.359 sec)
    INFO:tensorflow:global_step/sec: 260.282
    INFO:tensorflow:loss = 199580880.0, step = 2601 (0.384 sec)
    INFO:tensorflow:global_step/sec: 262.87
    INFO:tensorflow:loss = 661393500.0, step = 2701 (0.381 sec)
    INFO:tensorflow:global_step/sec: 216.371
    INFO:tensorflow:loss = 158321490.0, step = 2801 (0.462 sec)
    INFO:tensorflow:global_step/sec: 186.458
    INFO:tensorflow:loss = 239453020.0, step = 2901 (0.541 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 620132860.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:33
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-3000


    2026-03-25 08:47:33.712692: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.722646: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.910582: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:33.910597: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:33.916824: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.921845: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.927385: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.932837: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.939442: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.943497: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:33.971826: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.31546s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:34
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 25131182.0, global_step = 3000, label/mean = 13207.129, loss = 388566720.0, prediction/mean = 13261.1875
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-3000
    scores {'average_loss': 25131182.0, 'label/mean': 13207.129, 'loss': 388566720.0, 'prediction/mean': 13261.1875, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.


    2026-03-25 08:47:34.153984: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:34.357214: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:34.357229: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:34.363148: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.369699: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.375759: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.378603: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.385874: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.390239: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...


    2026-03-25 08:47:34.706654: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:34.806558: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 375481280.0, step = 3001


    2026-03-25 08:47:34.935436: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 177.961
    INFO:tensorflow:loss = 276110660.0, step = 3101 (0.558 sec)
    INFO:tensorflow:global_step/sec: 265.051
    INFO:tensorflow:loss = 449660300.0, step = 3201 (0.377 sec)
    INFO:tensorflow:global_step/sec: 284.291
    INFO:tensorflow:loss = 216178900.0, step = 3301 (0.353 sec)
    INFO:tensorflow:global_step/sec: 272.499
    INFO:tensorflow:loss = 479072580.0, step = 3401 (0.367 sec)
    INFO:tensorflow:global_step/sec: 278.055
    INFO:tensorflow:loss = 179985650.0, step = 3501 (0.359 sec)
    INFO:tensorflow:global_step/sec: 274.18
    INFO:tensorflow:loss = 570207100.0, step = 3601 (0.366 sec)
    INFO:tensorflow:global_step/sec: 240.845
    INFO:tensorflow:loss = 262005120.0, step = 3701 (0.415 sec)
    INFO:tensorflow:global_step/sec: 246.002
    INFO:tensorflow:loss = 167749620.0, step = 3801 (0.406 sec)
    INFO:tensorflow:global_step/sec: 261.574
    INFO:tensorflow:loss = 221773660.0, step = 3901 (0.382 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 386885150.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:39.046813: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.053562: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.207800: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:39.207814: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:39.213390: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.218658: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.224479: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.230346: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.237147: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.240745: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.269895: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.450656: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.30222s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:39
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 22415182.0, global_step = 4000, label/mean = 13207.129, loss = 346573200.0, prediction/mean = 13618.454
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-4000
    scores {'average_loss': 22415182.0, 'label/mean': 13207.129, 'loss': 346573200.0, 'prediction/mean': 13618.454, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:39.605821: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:39.605835: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:39.611365: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.617285: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.623160: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.625878: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.632038: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:39.635423: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...


    2026-03-25 08:47:39.967797: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:40.149601: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 195464830.0, step = 4001


    2026-03-25 08:47:40.255055: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 194.416
    INFO:tensorflow:loss = 134057416.0, step = 4101 (0.514 sec)
    INFO:tensorflow:global_step/sec: 256.376
    INFO:tensorflow:loss = 515779840.0, step = 4201 (0.390 sec)
    INFO:tensorflow:global_step/sec: 257.264
    INFO:tensorflow:loss = 630633100.0, step = 4301 (0.388 sec)
    INFO:tensorflow:global_step/sec: 265.323
    INFO:tensorflow:loss = 87844370.0, step = 4401 (0.377 sec)
    INFO:tensorflow:global_step/sec: 250.668
    INFO:tensorflow:loss = 664344400.0, step = 4501 (0.400 sec)
    INFO:tensorflow:global_step/sec: 220.192
    INFO:tensorflow:loss = 224811410.0, step = 4601 (0.453 sec)
    INFO:tensorflow:global_step/sec: 240.227
    INFO:tensorflow:loss = 784634500.0, step = 4701 (0.417 sec)
    INFO:tensorflow:global_step/sec: 253.259
    INFO:tensorflow:loss = 166524320.0, step = 4801 (0.394 sec)
    INFO:tensorflow:global_step/sec: 171.494
    INFO:tensorflow:loss = 291860830.0, step = 4901 (0.583 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1064: remove_checkpoint (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file APIs to delete files with this prefix.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 167070190.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-5000


    2026-03-25 08:47:44.653063: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.688713: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.852497: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:44.852513: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:44.858322: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.863364: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.868691: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.874372: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.881175: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.884742: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:44.912938: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26834s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:45
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 20978816.0, global_step = 5000, label/mean = 13207.129, loss = 324364770.0, prediction/mean = 13381.143
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-5000
    scores {'average_loss': 20978816.0, 'label/mean': 13207.129, 'loss': 324364770.0, 'prediction/mean': 13381.143, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:45.060117: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.217287: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:45.217302: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:45.222870: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.228880: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.235043: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.237759: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.244168: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.247863: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...


    2026-03-25 08:47:45.649801: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:45.753858: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 666112830.0, step = 5001


    2026-03-25 08:47:45.851908: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 234.943
    INFO:tensorflow:loss = 414432740.0, step = 5101 (0.426 sec)
    INFO:tensorflow:global_step/sec: 251.822
    INFO:tensorflow:loss = 227168860.0, step = 5201 (0.397 sec)
    INFO:tensorflow:global_step/sec: 239.327
    INFO:tensorflow:loss = 238660450.0, step = 5301 (0.418 sec)
    INFO:tensorflow:global_step/sec: 121.634
    INFO:tensorflow:loss = 478436930.0, step = 5401 (0.824 sec)
    INFO:tensorflow:global_step/sec: 244.634
    INFO:tensorflow:loss = 329021470.0, step = 5501 (0.407 sec)
    INFO:tensorflow:global_step/sec: 222.528
    INFO:tensorflow:loss = 206765000.0, step = 5601 (0.449 sec)
    INFO:tensorflow:global_step/sec: 292.483
    INFO:tensorflow:loss = 165280960.0, step = 5701 (0.342 sec)
    INFO:tensorflow:global_step/sec: 207.705
    INFO:tensorflow:loss = 108869840.0, step = 5801 (0.483 sec)
    INFO:tensorflow:global_step/sec: 255.925
    INFO:tensorflow:loss = 208249020.0, step = 5901 (0.390 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 80804984.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:50
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:50.576038: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.584007: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.741368: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:50.741384: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:50.747447: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.752601: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.758022: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.764037: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.772787: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.776532: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:50.814211: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.31212s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:51
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 20251720.0, global_step = 6000, label/mean = 13207.129, loss = 313122750.0, prediction/mean = 13391.231
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-6000
    scores {'average_loss': 20251720.0, 'label/mean': 13207.129, 'loss': 313122750.0, 'prediction/mean': 13391.231, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:50.991178: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.148880: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:51.148896: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:51.154516: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.160458: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.166502: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.169181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.175315: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.178808: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...


    2026-03-25 08:47:51.509558: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:51.613092: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 412036260.0, step = 6001


    2026-03-25 08:47:51.742105: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 235.304
    INFO:tensorflow:loss = 512610560.0, step = 6101 (0.425 sec)
    INFO:tensorflow:global_step/sec: 271.543
    INFO:tensorflow:loss = 217503470.0, step = 6201 (0.369 sec)
    INFO:tensorflow:global_step/sec: 267.962
    INFO:tensorflow:loss = 1031329800.0, step = 6301 (0.372 sec)
    INFO:tensorflow:global_step/sec: 260.871
    INFO:tensorflow:loss = 661009300.0, step = 6401 (0.383 sec)
    INFO:tensorflow:global_step/sec: 265.339
    INFO:tensorflow:loss = 532477100.0, step = 6501 (0.378 sec)
    INFO:tensorflow:global_step/sec: 215.337
    INFO:tensorflow:loss = 113493940.0, step = 6601 (0.465 sec)
    INFO:tensorflow:global_step/sec: 136.479
    INFO:tensorflow:loss = 464054800.0, step = 6701 (0.733 sec)
    INFO:tensorflow:global_step/sec: 153.093
    INFO:tensorflow:loss = 125123930.0, step = 6801 (0.653 sec)
    INFO:tensorflow:global_step/sec: 228.2
    INFO:tensorflow:loss = 97571140.0, step = 6901 (0.437 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 176839740.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:47:56
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-7000


    2026-03-25 08:47:56.786588: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:56.794594: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:56.981342: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:56.981370: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:56.988123: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:56.993525: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:56.999193: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.005114: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.012470: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.016830: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.046232: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.28541s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:47:57
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 19809998.0, global_step = 7000, label/mean = 13207.129, loss = 306293060.0, prediction/mean = 13305.212
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-7000
    scores {'average_loss': 19809998.0, 'label/mean': 13207.129, 'loss': 306293060.0, 'prediction/mean': 13305.212, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:47:57.202761: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.362817: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:47:57.362831: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:47:57.368824: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.376064: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.382708: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.385511: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.392734: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.398813: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...


    2026-03-25 08:47:57.753134: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:47:57.855190: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 722761700.0, step = 7001


    2026-03-25 08:47:57.955777: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 199.645
    INFO:tensorflow:loss = 278853730.0, step = 7101 (0.501 sec)
    INFO:tensorflow:global_step/sec: 259.364
    INFO:tensorflow:loss = 206579120.0, step = 7201 (0.386 sec)
    INFO:tensorflow:global_step/sec: 149.868
    INFO:tensorflow:loss = 133728880.0, step = 7301 (0.672 sec)
    INFO:tensorflow:global_step/sec: 111.905
    INFO:tensorflow:loss = 292073470.0, step = 7401 (0.899 sec)
    INFO:tensorflow:global_step/sec: 227.481
    INFO:tensorflow:loss = 147415550.0, step = 7501 (0.429 sec)
    INFO:tensorflow:global_step/sec: 267.743
    INFO:tensorflow:loss = 173656380.0, step = 7601 (0.373 sec)
    INFO:tensorflow:global_step/sec: 254.588
    INFO:tensorflow:loss = 338654370.0, step = 7701 (0.393 sec)
    INFO:tensorflow:global_step/sec: 244.898
    INFO:tensorflow:loss = 73967220.0, step = 7801 (0.410 sec)
    INFO:tensorflow:global_step/sec: 245.795
    INFO:tensorflow:loss = 73481030.0, step = 7901 (0.406 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 262308380.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:48:03


    2026-03-25 08:48:03.098318: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.126814: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:03.302331: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:03.302346: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:03.308349: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.313875: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.319303: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.325255: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.332701: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.336318: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.367067: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.37115s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:48:03
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 19489510.0, global_step = 8000, label/mean = 13207.129, loss = 301337820.0, prediction/mean = 13402.268
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-8000
    scores {'average_loss': 19489510.0, 'label/mean': 13207.129, 'loss': 301337820.0, 'prediction/mean': 13402.268, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:03.613106: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.775689: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:03.775704: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:03.781944: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.788255: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.794664: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.797426: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.803472: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:03.807032: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...


    2026-03-25 08:48:04.166161: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:04.352831: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 829637900.0, step = 8001


    2026-03-25 08:48:04.457714: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 228.331
    INFO:tensorflow:loss = 134427840.0, step = 8101 (0.438 sec)
    INFO:tensorflow:global_step/sec: 248.884
    INFO:tensorflow:loss = 97132776.0, step = 8201 (0.402 sec)
    INFO:tensorflow:global_step/sec: 270.565
    INFO:tensorflow:loss = 125679120.0, step = 8301 (0.370 sec)
    INFO:tensorflow:global_step/sec: 198.902
    INFO:tensorflow:loss = 332643260.0, step = 8401 (0.503 sec)
    INFO:tensorflow:global_step/sec: 278.409
    INFO:tensorflow:loss = 894057860.0, step = 8501 (0.359 sec)
    INFO:tensorflow:global_step/sec: 119.948
    INFO:tensorflow:loss = 148510200.0, step = 8601 (0.843 sec)
    INFO:tensorflow:global_step/sec: 186.815
    INFO:tensorflow:loss = 125338930.0, step = 8701 (0.526 sec)
    INFO:tensorflow:global_step/sec: 264.339
    INFO:tensorflow:loss = 144344180.0, step = 8801 (0.378 sec)
    INFO:tensorflow:global_step/sec: 263.488
    INFO:tensorflow:loss = 186957760.0, step = 8901 (0.379 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 158082660.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:48:09


    2026-03-25 08:48:09.125176: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.156433: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:09.331648: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:09.331662: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:09.337905: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.343357: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.349234: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.355141: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.362415: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.366003: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.394328: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.34725s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:48:09
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 19230030.0, global_step = 9000, label/mean = 13207.129, loss = 297325860.0, prediction/mean = 13327.571
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-9000
    scores {'average_loss': 19230030.0, 'label/mean': 13207.129, 'loss': 297325860.0, 'prediction/mean': 13327.571, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.


    2026-03-25 08:48:09.619269: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:09.824657: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:09.824673: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:09.830458: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.837687: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.844127: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.847276: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.853823: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:09.857618: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...


    2026-03-25 08:48:10.309254: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:10.432556: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 192953180.0, step = 9001


    2026-03-25 08:48:10.546457: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 226.748
    INFO:tensorflow:loss = 142971550.0, step = 9101 (0.439 sec)
    INFO:tensorflow:global_step/sec: 257.841
    INFO:tensorflow:loss = 676183400.0, step = 9201 (0.388 sec)
    INFO:tensorflow:global_step/sec: 239.343
    INFO:tensorflow:loss = 232348200.0, step = 9301 (0.422 sec)
    INFO:tensorflow:global_step/sec: 146.184
    INFO:tensorflow:loss = 482902700.0, step = 9401 (0.680 sec)
    INFO:tensorflow:global_step/sec: 263.184
    INFO:tensorflow:loss = 343714180.0, step = 9501 (0.380 sec)
    INFO:tensorflow:global_step/sec: 187.918
    INFO:tensorflow:loss = 295162940.0, step = 9601 (0.533 sec)
    INFO:tensorflow:global_step/sec: 149.777
    INFO:tensorflow:loss = 119039790.0, step = 9701 (0.669 sec)
    INFO:tensorflow:global_step/sec: 223.28
    INFO:tensorflow:loss = 116382560.0, step = 9801 (0.448 sec)
    INFO:tensorflow:global_step/sec: 105.555
    INFO:tensorflow:loss = 542135940.0, step = 9901 (0.950 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 407506620.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:48:16


    2026-03-25 08:48:16.101207: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.112749: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:16.314571: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:16.314586: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:16.325592: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.333088: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.344496: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.352119: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.359901: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.364540: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.394760: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.32215s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:48:16
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 18976718.0, global_step = 10000, label/mean = 13207.129, loss = 293409250.0, prediction/mean = 13349.256
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-10000
    scores {'average_loss': 18976718.0, 'label/mean': 13207.129, 'loss': 293409250.0, 'prediction/mean': 13349.256, 'global_step': 10000}


    2026-03-25 08:48:16.571759: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


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

scatter_plot_inference_grid(est, x_df, numeric_feature_names)
```

    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmprmxa1_vf/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:48:16.990399: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:48:16.990413: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:48:16.994410: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:16.999132: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:17.004111: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:17.006179: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:17.010967: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:17.013806: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:48:17.029998: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.



    
![png](car_data_ML_pipeline_files/car_data_ML_pipeline_16_2.png)
    


### Task 2: Take best numeric model from earlier. Add normalization.

#### Adding normalization to best numeric model from earlier

- Decide what type of normalization to add, and for which features
- Use the `normalizer_fn` arg on [`numeric_column`](https://g3doc.corp.google.com/learning/brain/public/g3doc/api_docs/python/tf/feature_column/numeric_column.md?cl=head)
    - An example of a silly normalizer_fn that shifts inputs down by 1, and then negates the value:
    
         normalizer_fn = lambda x: tf.neg(tf.subtract(x, 1))
- You may find these pandas functions helpful:
    - dataframe.mean()['your_feature_name']
    - dataframe.std()['your_feature_name']
- You will need to retune the hyperparameters from earlier.


**Does normalization improve model quality on this dataset? Why or why not?**


```python
# This 1D visualization of each numeric feature might inform your normalization
# decisions.
for feature_name in numeric_feature_names:
  car_data.hist(column=feature_name)
```

#### Training model with numeric features + normalization


```python
## [Change #7]: Added this section to outline the next steps for Task 2.
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

# Training loop for task 2.1 - Z-score normalization
for _ in range(num_print_statements):
  est_zscore.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_zscore = est_zscore.evaluate(eval_input_fn)
  print('scores_zscore', scores_zscore)

# Training loop for task 2.2 - Min-max normalization
for _ in range(num_print_statements):
  est_minmax.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_minmax = est_minmax.evaluate(eval_input_fn)
  print('scores_minmax', scores_minmax)

# → pick the winner of 2.1 vs 2.2 based on final avg_loss and RMSE

# Task 2.3 try GradientDescentOptimizer with the same config → answers the lab's embedded question
# Task 2.3: GradientDescentOptimizer + Z-score normalization
# Hypothesis: with balanced gradients (Z-score), plain GD may now converge.
# lr=0.01 is too small for GD — using 0.5 to compensate for smaller gradient magnitudes post-normalisation.

# Task 2.4 try PCA to explore dimensionality reduction as an alternative 
# to normalization for handling scale variance and improving convergence.
'''
cell blocks below has details for Task 2.3 and Task 2.4
'''
```

    model_feature_columns_zscore [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028ee0>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028d30>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028ca0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028c10>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028b80>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d028af0>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x33d0297e0>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x300940940>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a5489d0>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548a60>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548af0>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548b80>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548c10>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548ca0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548d30>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    model_feature_columns_minmax [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548dc0>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548f70>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a548ee0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549000>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549090>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549120>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a5491b0>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549240>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a5492d0>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549360>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a5493f0>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549480>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549510>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a5495a0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x31a549630>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpiz6bux0d
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpiz6bux0d', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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


    2026-03-25 08:49:27.471652: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:27.471705: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:27.508305: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:27.608862: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:27.622017: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:27.625661: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:27.633621: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:27.643152: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...


    2026-03-25 08:49:28.368164: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:28.542859: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2703831600.0, step = 1


    2026-03-25 08:49:28.779464: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 158.658
    INFO:tensorflow:loss = 3441020400.0, step = 101 (0.633 sec)
    INFO:tensorflow:global_step/sec: 132.576
    INFO:tensorflow:loss = 2183020500.0, step = 201 (0.751 sec)
    INFO:tensorflow:global_step/sec: 276.462
    INFO:tensorflow:loss = 5252879400.0, step = 301 (0.361 sec)
    INFO:tensorflow:global_step/sec: 279.505
    INFO:tensorflow:loss = 5549051000.0, step = 401 (0.358 sec)
    INFO:tensorflow:global_step/sec: 167.718
    INFO:tensorflow:loss = 4430748000.0, step = 501 (0.596 sec)
    INFO:tensorflow:global_step/sec: 203.975
    INFO:tensorflow:loss = 4517037000.0, step = 601 (0.490 sec)
    INFO:tensorflow:global_step/sec: 303.762
    INFO:tensorflow:loss = 2215752400.0, step = 701 (0.329 sec)
    INFO:tensorflow:global_step/sec: 295.674
    INFO:tensorflow:loss = 2532620800.0, step = 801 (0.338 sec)
    INFO:tensorflow:global_step/sec: 284.413
    INFO:tensorflow:loss = 3862636300.0, step = 901 (0.352 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3371098000.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:49:33.624771: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.638420: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:49:33
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:33.863779: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:33.863794: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:33.874199: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.883327: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.890892: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.896998: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.904420: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.909016: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:33.946026: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.30678s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:49:34
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 232010270.0, global_step = 1000, label/mean = 13207.129, loss = 3587235800.0, prediction/mean = 136.59427


    2026-03-25 08:49:34.076341: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-1000
    scores_zscore {'average_loss': 232010270.0, 'label/mean': 13207.129, 'loss': 3587235800.0, 'prediction/mean': 136.59427, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:34.584206: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:34.584222: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:34.590248: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:34.596473: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:34.603352: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:34.606438: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:34.613196: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:34.617657: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...


    2026-03-25 08:49:34.998191: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:35.116683: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 4357034000.0, step = 1001


    2026-03-25 08:49:35.216979: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 163.999
    INFO:tensorflow:loss = 4505171500.0, step = 1101 (0.610 sec)
    INFO:tensorflow:global_step/sec: 287.016
    INFO:tensorflow:loss = 4606261000.0, step = 1201 (0.348 sec)
    INFO:tensorflow:global_step/sec: 284.728
    INFO:tensorflow:loss = 5596901400.0, step = 1301 (0.351 sec)
    INFO:tensorflow:global_step/sec: 288.948
    INFO:tensorflow:loss = 5236906000.0, step = 1401 (0.346 sec)
    INFO:tensorflow:global_step/sec: 291.549
    INFO:tensorflow:loss = 3388610600.0, step = 1501 (0.343 sec)
    INFO:tensorflow:global_step/sec: 256.231
    INFO:tensorflow:loss = 1774627300.0, step = 1601 (0.390 sec)
    INFO:tensorflow:global_step/sec: 192.263
    INFO:tensorflow:loss = 3575206400.0, step = 1701 (0.520 sec)
    INFO:tensorflow:global_step/sec: 300.727
    INFO:tensorflow:loss = 4234334000.0, step = 1801 (0.333 sec)
    INFO:tensorflow:global_step/sec: 204.592
    INFO:tensorflow:loss = 1762663700.0, step = 1901 (0.489 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 3237426000.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:49:39.496613: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.538164: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:49:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:39.878585: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:39.878602: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:39.886027: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.897805: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.904688: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.912063: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.919763: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.923928: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:39.960744: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.29607s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:49:40
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 226335570.0, global_step = 2000, label/mean = 13207.129, loss = 3499496000.0, prediction/mean = 284.56757
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-2000
    scores_zscore {'average_loss': 226335570.0, 'label/mean': 13207.129, 'loss': 3499496000.0, 'prediction/mean': 284.56757, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.


    2026-03-25 08:49:40.092202: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.272002: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:40.272017: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:40.278174: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.284533: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.291386: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:40.294101: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.300448: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.304458: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...


    2026-03-25 08:49:40.758870: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:40.890891: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2106966000.0, step = 2001


    2026-03-25 08:49:41.017491: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 147.88
    INFO:tensorflow:loss = 3546580700.0, step = 2101 (0.677 sec)
    INFO:tensorflow:global_step/sec: 217.464
    INFO:tensorflow:loss = 4239756500.0, step = 2201 (0.463 sec)
    INFO:tensorflow:global_step/sec: 239.743
    INFO:tensorflow:loss = 3177113000.0, step = 2301 (0.413 sec)
    INFO:tensorflow:global_step/sec: 278.578
    INFO:tensorflow:loss = 1733953800.0, step = 2401 (0.359 sec)
    INFO:tensorflow:global_step/sec: 252.495
    INFO:tensorflow:loss = 3249148400.0, step = 2501 (0.396 sec)
    INFO:tensorflow:global_step/sec: 274.561
    INFO:tensorflow:loss = 3217189400.0, step = 2601 (0.364 sec)
    INFO:tensorflow:global_step/sec: 238.712
    INFO:tensorflow:loss = 2319728600.0, step = 2701 (0.419 sec)
    INFO:tensorflow:global_step/sec: 261.767
    INFO:tensorflow:loss = 3825121300.0, step = 2801 (0.382 sec)
    INFO:tensorflow:global_step/sec: 265.53
    INFO:tensorflow:loss = 7909309000.0, step = 2901 (0.377 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 4838910000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:49:45


    2026-03-25 08:49:45.330464: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.364259: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:45.553505: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:45.553521: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:45.561428: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.567455: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.575331: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.582583: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.591126: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.595281: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.630410: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.27872s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:49:45
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 220560380.0, global_step = 3000, label/mean = 13207.129, loss = 3410203000.0, prediction/mean = 435.927
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-3000
    scores_zscore {'average_loss': 220560380.0, 'label/mean': 13207.129, 'loss': 3410203000.0, 'prediction/mean': 435.927, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-3000


    2026-03-25 08:49:45.763851: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.951605: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:45.951620: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:45.958137: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.964752: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:45.971435: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.974793: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.983437: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:45.987718: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.


    2026-03-25 08:49:46.411348: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...


    2026-03-25 08:49:46.625700: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 1986662400.0, step = 3001


    2026-03-25 08:49:46.896433: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 179.816
    INFO:tensorflow:loss = 3005432800.0, step = 3101 (0.546 sec)
    INFO:tensorflow:global_step/sec: 171.838
    INFO:tensorflow:loss = 2932922400.0, step = 3201 (0.583 sec)
    INFO:tensorflow:global_step/sec: 108.775
    INFO:tensorflow:loss = 4353791500.0, step = 3301 (0.921 sec)
    INFO:tensorflow:global_step/sec: 89.8588
    INFO:tensorflow:loss = 3169898000.0, step = 3401 (1.162 sec)
    INFO:tensorflow:global_step/sec: 120.634
    INFO:tensorflow:loss = 1636995600.0, step = 3501 (0.779 sec)
    INFO:tensorflow:global_step/sec: 166.37
    INFO:tensorflow:loss = 2413145300.0, step = 3601 (0.601 sec)
    INFO:tensorflow:global_step/sec: 246.923
    INFO:tensorflow:loss = 3729774300.0, step = 3701 (0.404 sec)
    INFO:tensorflow:global_step/sec: 162.008
    INFO:tensorflow:loss = 2152848000.0, step = 3801 (0.619 sec)
    INFO:tensorflow:global_step/sec: 166.271
    INFO:tensorflow:loss = 4784595000.0, step = 3901 (0.601 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 4918385000.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:49:53.810524: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:53.892881: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:49:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:54.214295: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:54.214314: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:54.225957: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.240917: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.251613: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.259823: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.269145: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.274235: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.320663: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.40123s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:49:54
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 214844940.0, global_step = 4000, label/mean = 13207.129, loss = 3321833200.0, prediction/mean = 587.6216
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-4000
    scores_zscore {'average_loss': 214844940.0, 'label/mean': 13207.129, 'loss': 3321833200.0, 'prediction/mean': 587.6216, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:49:54.512561: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:49:54.761306: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:49:54.761323: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:49:54.768873: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.778509: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.787210: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.790774: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.801401: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:49:54.806904: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.


    2026-03-25 08:49:55.447043: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...


    2026-03-25 08:49:55.810649: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3931484700.0, step = 4001


    2026-03-25 08:49:56.056100: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 103.624
    INFO:tensorflow:loss = 3160464400.0, step = 4101 (0.973 sec)
    INFO:tensorflow:global_step/sec: 121.235
    INFO:tensorflow:loss = 1690692900.0, step = 4201 (0.814 sec)
    INFO:tensorflow:global_step/sec: 272.875
    INFO:tensorflow:loss = 2615530000.0, step = 4301 (0.367 sec)
    INFO:tensorflow:global_step/sec: 294.791
    INFO:tensorflow:loss = 2568972300.0, step = 4401 (0.338 sec)
    INFO:tensorflow:global_step/sec: 298.225
    INFO:tensorflow:loss = 1693962200.0, step = 4501 (0.335 sec)
    INFO:tensorflow:global_step/sec: 284.791
    INFO:tensorflow:loss = 1655920500.0, step = 4601 (0.351 sec)
    INFO:tensorflow:global_step/sec: 162.489
    INFO:tensorflow:loss = 4199228200.0, step = 4701 (0.615 sec)
    INFO:tensorflow:global_step/sec: 257.358
    INFO:tensorflow:loss = 3834107000.0, step = 4801 (0.390 sec)
    INFO:tensorflow:global_step/sec: 276.474
    INFO:tensorflow:loss = 7594466300.0, step = 4901 (0.360 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 3260832300.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:50:01.154573: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.220613: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:50:01
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:01.519683: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:01.519698: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:01.529234: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.536653: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.543458: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.549917: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.557157: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.561052: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.597094: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.30761s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:50:01
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 209242720.0, global_step = 5000, label/mean = 13207.129, loss = 3235214300.0, prediction/mean = 738.382
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-5000
    scores_zscore {'average_loss': 209242720.0, 'label/mean': 13207.129, 'loss': 3235214300.0, 'prediction/mean': 738.382, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:50:01.734807: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:01.971363: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:01.971377: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:01.977315: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.983420: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.989673: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.992318: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:01.998651: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:02.002291: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...


    2026-03-25 08:50:02.465250: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:02.577641: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2646477300.0, step = 5001


    2026-03-25 08:50:02.680265: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 229.766
    INFO:tensorflow:loss = 4284608000.0, step = 5101 (0.436 sec)
    INFO:tensorflow:global_step/sec: 201.808
    INFO:tensorflow:loss = 3077374000.0, step = 5201 (0.496 sec)
    INFO:tensorflow:global_step/sec: 283.228
    INFO:tensorflow:loss = 3317009200.0, step = 5301 (0.352 sec)
    INFO:tensorflow:global_step/sec: 219.403
    INFO:tensorflow:loss = 4732129300.0, step = 5401 (0.459 sec)
    INFO:tensorflow:global_step/sec: 245.668
    INFO:tensorflow:loss = 3271278600.0, step = 5501 (0.404 sec)
    INFO:tensorflow:global_step/sec: 225.77
    INFO:tensorflow:loss = 3314002000.0, step = 5601 (0.442 sec)
    INFO:tensorflow:global_step/sec: 292.307
    INFO:tensorflow:loss = 2360761300.0, step = 5701 (0.342 sec)
    INFO:tensorflow:global_step/sec: 290.293
    INFO:tensorflow:loss = 3543361000.0, step = 5801 (0.344 sec)
    INFO:tensorflow:global_step/sec: 283.453
    INFO:tensorflow:loss = 3310237200.0, step = 5901 (0.353 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 5017698300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:50:07
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.


    2026-03-25 08:50:06.916682: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:06.924777: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.098564: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:07.098580: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:07.106004: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.111533: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:07.117298: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.123501: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.130603: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.134180: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.176716: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.313732: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.27543s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:50:07
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 203775730.0, global_step = 6000, label/mean = 13207.129, loss = 3150686500.0, prediction/mean = 887.8102
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-6000
    scores_zscore {'average_loss': 203775730.0, 'label/mean': 13207.129, 'loss': 3150686500.0, 'prediction/mean': 887.8102, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:07.488405: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:07.488421: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:07.494818: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.500792: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.506809: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.509462: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.516582: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:07.520486: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...


    2026-03-25 08:50:07.944407: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:08.055840: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3603491300.0, step = 6001


    2026-03-25 08:50:08.177149: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 213.407
    INFO:tensorflow:loss = 1454033200.0, step = 6101 (0.469 sec)
    INFO:tensorflow:global_step/sec: 263.764
    INFO:tensorflow:loss = 3210459000.0, step = 6201 (0.378 sec)
    INFO:tensorflow:global_step/sec: 272.926
    INFO:tensorflow:loss = 3760255000.0, step = 6301 (0.366 sec)
    INFO:tensorflow:global_step/sec: 270.752
    INFO:tensorflow:loss = 1389368000.0, step = 6401 (0.369 sec)
    INFO:tensorflow:global_step/sec: 281.915
    INFO:tensorflow:loss = 1844463200.0, step = 6501 (0.355 sec)
    INFO:tensorflow:global_step/sec: 220.252
    INFO:tensorflow:loss = 5172850700.0, step = 6601 (0.454 sec)
    INFO:tensorflow:global_step/sec: 272.743
    INFO:tensorflow:loss = 2151711700.0, step = 6701 (0.367 sec)
    INFO:tensorflow:global_step/sec: 276.342
    INFO:tensorflow:loss = 1934275800.0, step = 6801 (0.362 sec)
    INFO:tensorflow:global_step/sec: 147.792
    INFO:tensorflow:loss = 3306747400.0, step = 6901 (0.687 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 1989383200.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:50:12.773172: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:12.833253: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:50:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:13.366190: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:13.366217: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:13.375555: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.390236: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.400578: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.409848: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.424470: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.431563: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.531050: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.37079s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:50:13
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 198445090.0, global_step = 7000, label/mean = 13207.129, loss = 3068266200.0, prediction/mean = 1036.474
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-7000
    scores_zscore {'average_loss': 198445090.0, 'label/mean': 13207.129, 'loss': 3068266200.0, 'prediction/mean': 1036.474, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-7000


    2026-03-25 08:50:13.671689: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.856652: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:13.856667: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:13.862651: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.869029: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:13.875397: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.878454: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.884835: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:13.888794: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.


    2026-03-25 08:50:14.162359: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 1882300400.0, step = 7001


    2026-03-25 08:50:14.384759: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:14.492079: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 248.17
    INFO:tensorflow:loss = 4120292400.0, step = 7101 (0.403 sec)
    INFO:tensorflow:global_step/sec: 262.075
    INFO:tensorflow:loss = 1889781000.0, step = 7201 (0.381 sec)
    INFO:tensorflow:global_step/sec: 293.391
    INFO:tensorflow:loss = 3098143500.0, step = 7301 (0.341 sec)
    INFO:tensorflow:global_step/sec: 280.481
    INFO:tensorflow:loss = 5121974300.0, step = 7401 (0.357 sec)
    INFO:tensorflow:global_step/sec: 264.952
    INFO:tensorflow:loss = 4380130300.0, step = 7501 (0.377 sec)
    INFO:tensorflow:global_step/sec: 280.779
    INFO:tensorflow:loss = 2564111400.0, step = 7601 (0.356 sec)
    INFO:tensorflow:global_step/sec: 282.471
    INFO:tensorflow:loss = 3289488600.0, step = 7701 (0.354 sec)
    INFO:tensorflow:global_step/sec: 282.325
    INFO:tensorflow:loss = 2929448700.0, step = 7801 (0.354 sec)
    INFO:tensorflow:global_step/sec: 276.303
    INFO:tensorflow:loss = 6628274700.0, step = 7901 (0.362 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 4517939700.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:50:18.629659: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:18.677880: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:50:18
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:18.961994: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:18.962008: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:18.969072: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:18.975072: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:18.982818: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:18.989926: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:18.998398: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.002879: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.039607: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.30708s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:50:19
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 193175900.0, global_step = 8000, label/mean = 13207.129, loss = 2986796500.0, prediction/mean = 1186.957
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-8000
    scores_zscore {'average_loss': 193175900.0, 'label/mean': 13207.129, 'loss': 2986796500.0, 'prediction/mean': 1186.957, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.


    2026-03-25 08:50:19.195083: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.376254: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:19.376270: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:19.382450: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.389537: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:19.396415: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.400095: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.407363: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:19.413532: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.


    2026-03-25 08:50:19.898529: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 4083445200.0, step = 8001


    2026-03-25 08:50:20.222755: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:20.322120: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 248.91
    INFO:tensorflow:loss = 2486308900.0, step = 8101 (0.402 sec)
    INFO:tensorflow:global_step/sec: 273.391
    INFO:tensorflow:loss = 2614432300.0, step = 8201 (0.366 sec)
    INFO:tensorflow:global_step/sec: 112.79
    INFO:tensorflow:loss = 2949862100.0, step = 8301 (0.895 sec)
    INFO:tensorflow:global_step/sec: 229.242
    INFO:tensorflow:loss = 1998830300.0, step = 8401 (0.428 sec)
    INFO:tensorflow:global_step/sec: 257.328
    INFO:tensorflow:loss = 2866318800.0, step = 8501 (0.388 sec)
    INFO:tensorflow:global_step/sec: 287.73
    INFO:tensorflow:loss = 2358667800.0, step = 8601 (0.348 sec)
    INFO:tensorflow:global_step/sec: 242.572
    INFO:tensorflow:loss = 1606827800.0, step = 8701 (0.413 sec)
    INFO:tensorflow:global_step/sec: 259.528
    INFO:tensorflow:loss = 3220313600.0, step = 8801 (0.385 sec)
    INFO:tensorflow:global_step/sec: 238.367
    INFO:tensorflow:loss = 2401312800.0, step = 8901 (0.420 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 3661232600.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-25 08:50:24.966659: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:24.999301: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-25T08:50:25
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:25.236297: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:25.236313: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-25 08:50:25.243539: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.249527: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.256233: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.263818: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.271956: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.276625: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.313097: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.28510s
    INFO:tensorflow:Finished evaluation at 2026-03-25-08:50:25
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 188037380.0, global_step = 9000, label/mean = 13207.129, loss = 2907347200.0, prediction/mean = 1336.1647
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-9000
    scores_zscore {'average_loss': 188037380.0, 'label/mean': 13207.129, 'loss': 2907347200.0, 'prediction/mean': 1336.1647, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpoz81x_b8/model.ckpt-9000


    2026-03-25 08:50:25.447624: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.644123: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-25 08:50:25.644139: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-25 08:50:25.651016: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.657700: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.665689: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.670672: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.677919: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-25 08:50:25.684777: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.



```python
# Task 2.3: GradientDescentOptimizer + Z-score normalization

est_gd = tf.estimator.DNNRegressor(                                           
    feature_columns=model_feature_columns_zscore,  # ← normalized, not raw    
    hidden_units=hidden_units_parameter,
    optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.0001)            
)                                                                             
num_print_statements = 10
num_training_steps = 10000                                                    
for _ in range(num_print_statements):
    est_gd.train(train_input_fn, steps=num_training_steps // num_print_statements)                                                         
    scores_gd = est_gd.evaluate(eval_input_fn)
    print('scores_gd', scores_gd)

# Problems:
'''
INFO:tensorflow:Using default config.
WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpq0x4wm70
INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpq0x4wm70', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
2026-03-24 19:34:23.927537: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-24 19:34:23.927555: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-24 19:34:23.934181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:23.945405: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:23.952080: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:23.955222: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:23.960736: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:23.964980: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpq0x4wm70/model.ckpt.
2026-03-24 19:34:24.329553: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
INFO:tensorflow:loss = 3667000000.0, step = 1
2026-03-24 19:34:24.597086: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:24.725839: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
ERROR:tensorflow:Model diverged with loss = NaN.
2026-03-24 19:34:24.806420: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-24 19:34:24.823401: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
'''
```


```python
# [Change #8]: # Task 2.4: PCA + Adagrad

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
'''
model_feature_columns_pca [NumericColumn(key='PC1', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC2', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC3', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC4', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC5', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC6', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC7', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC8', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='PC9', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
INFO:tensorflow:Using default config.
WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw
INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
2026-03-25 08:51:46.481689: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:46.481708: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:46.487462: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:46.494577: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:46.513193: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:46.518380: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:46.527131: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:46.532882: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
2026-03-25 08:51:47.177448: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:47.294704: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:loss = 1693591200.0, step = 1
2026-03-25 08:51:47.475056: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 193.38
INFO:tensorflow:loss = 3004683800.0, step = 101 (0.515 sec)
INFO:tensorflow:global_step/sec: 330.138
INFO:tensorflow:loss = 4712327000.0, step = 201 (0.303 sec)
INFO:tensorflow:global_step/sec: 340.847
INFO:tensorflow:loss = 8281215500.0, step = 301 (0.293 sec)
INFO:tensorflow:global_step/sec: 340.541
INFO:tensorflow:loss = 5409115000.0, step = 401 (0.294 sec)
INFO:tensorflow:global_step/sec: 346.76
INFO:tensorflow:loss = 4037581300.0, step = 501 (0.288 sec)
INFO:tensorflow:global_step/sec: 342.609
INFO:tensorflow:loss = 2843140900.0, step = 601 (0.292 sec)
INFO:tensorflow:global_step/sec: 347.951
INFO:tensorflow:loss = 2655443200.0, step = 701 (0.287 sec)
INFO:tensorflow:global_step/sec: 343.45
INFO:tensorflow:loss = 1535879800.0, step = 801 (0.291 sec)
INFO:tensorflow:global_step/sec: 343.361
INFO:tensorflow:loss = 3149246000.0, step = 901 (0.291 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
INFO:tensorflow:Loss for final step: 3940059400.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:51:50
2026-03-25 08:51:50.707147: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.739823: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-1000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:50.911263: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:50.911279: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:50.916898: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.923218: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.928665: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.935756: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.943976: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.947626: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:50.972807: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.089480: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.23931s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:51:51
INFO:tensorflow:Saving dict for global step 1000: average_loss = 235170930.0, global_step = 1000, label/mean = 13207.129, loss = 3636104200.0, prediction/mean = 59.900124
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-1000
scores_pca {'average_loss': 235170930.0, 'label/mean': 13207.129, 'loss': 3636104200.0, 'prediction/mean': 59.900124, 'global_step': 1000}
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-1000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:51.548723: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:51.548740: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:51.553982: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.559887: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.565759: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.568783: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.574995: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:51.578217: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:51:51.789633: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
INFO:tensorflow:loss = 3391310000.0, step = 1001
2026-03-25 08:51:52.019580: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:52.112012: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 308.432
INFO:tensorflow:loss = 2326131200.0, step = 1101 (0.325 sec)
INFO:tensorflow:global_step/sec: 351.128
INFO:tensorflow:loss = 3549499400.0, step = 1201 (0.285 sec)
INFO:tensorflow:global_step/sec: 352.396
INFO:tensorflow:loss = 3436810200.0, step = 1301 (0.284 sec)
INFO:tensorflow:global_step/sec: 349.951
INFO:tensorflow:loss = 3984403200.0, step = 1401 (0.286 sec)
INFO:tensorflow:global_step/sec: 351.429
INFO:tensorflow:loss = 4400571400.0, step = 1501 (0.284 sec)
INFO:tensorflow:global_step/sec: 354.808
INFO:tensorflow:loss = 2211620000.0, step = 1601 (0.282 sec)
INFO:tensorflow:global_step/sec: 350.265
INFO:tensorflow:loss = 2900972300.0, step = 1701 (0.285 sec)
INFO:tensorflow:global_step/sec: 356.508
INFO:tensorflow:loss = 3520660200.0, step = 1801 (0.281 sec)
INFO:tensorflow:global_step/sec: 354.543
INFO:tensorflow:loss = 2693598200.0, step = 1901 (0.282 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
INFO:tensorflow:Loss for final step: 3081627600.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:51:55
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-2000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:55.065142: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.071372: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.213145: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:55.213183: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:55.218308: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.223099: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.228366: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.234425: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.241982: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.245170: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.23581s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:51:55
INFO:tensorflow:Saving dict for global step 2000: average_loss = 232974130.0, global_step = 2000, label/mean = 13207.129, loss = 3602138400.0, prediction/mean = 120.58655
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-2000
scores_pca {'average_loss': 232974130.0, 'label/mean': 13207.129, 'loss': 3602138400.0, 'prediction/mean': 120.58655, 'global_step': 2000}
INFO:tensorflow:Calling model_fn.
2026-03-25 08:51:55.270515: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.392106: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-2000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:55.538518: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:55.538532: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:55.544485: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.550226: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.555805: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.558617: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.564614: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:55.568007: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:51:55.782313: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
INFO:tensorflow:loss = 4486459400.0, step = 2001
2026-03-25 08:51:56.003726: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:56.086862: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 263.816
INFO:tensorflow:loss = 3898317600.0, step = 2101 (0.380 sec)
INFO:tensorflow:global_step/sec: 356.887
INFO:tensorflow:loss = 2002719100.0, step = 2201 (0.280 sec)
INFO:tensorflow:global_step/sec: 350.532
INFO:tensorflow:loss = 2535827000.0, step = 2301 (0.285 sec)
INFO:tensorflow:global_step/sec: 346.897
INFO:tensorflow:loss = 6716141600.0, step = 2401 (0.288 sec)
INFO:tensorflow:global_step/sec: 349.317
INFO:tensorflow:loss = 2691210800.0, step = 2501 (0.286 sec)
INFO:tensorflow:global_step/sec: 347.567
INFO:tensorflow:loss = 5333090300.0, step = 2601 (0.288 sec)
INFO:tensorflow:global_step/sec: 359.46
INFO:tensorflow:loss = 4423546000.0, step = 2701 (0.278 sec)
INFO:tensorflow:global_step/sec: 365.484
INFO:tensorflow:loss = 5078761500.0, step = 2801 (0.274 sec)
INFO:tensorflow:global_step/sec: 360.655
INFO:tensorflow:loss = 3472384500.0, step = 2901 (0.277 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
INFO:tensorflow:Loss for final step: 2802656800.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:51:59
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-3000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:59.074587: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.081397: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.226649: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:59.226665: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:59.231738: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.236484: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.242046: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.247540: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.254940: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.258513: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.23740s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:51:59
INFO:tensorflow:Saving dict for global step 3000: average_loss = 230710560.0, global_step = 3000, label/mean = 13207.129, loss = 3567140400.0, prediction/mean = 182.55902
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-3000
scores_pca {'average_loss': 230710560.0, 'label/mean': 13207.129, 'loss': 3567140400.0, 'prediction/mean': 182.55902, 'global_step': 3000}
INFO:tensorflow:Calling model_fn.
2026-03-25 08:51:59.283674: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.402934: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-3000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:51:59.544257: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:51:59.544272: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:51:59.549690: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.555397: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.561613: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.564043: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.570288: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:51:59.573561: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:51:59.786083: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
INFO:tensorflow:loss = 5568259000.0, step = 3001
2026-03-25 08:52:00.009469: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:00.104753: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 288.208
INFO:tensorflow:loss = 2657609700.0, step = 3101 (0.347 sec)
INFO:tensorflow:global_step/sec: 363.524
INFO:tensorflow:loss = 2960504300.0, step = 3201 (0.275 sec)
INFO:tensorflow:global_step/sec: 330.237
INFO:tensorflow:loss = 2480222700.0, step = 3301 (0.303 sec)
INFO:tensorflow:global_step/sec: 365.754
INFO:tensorflow:loss = 3576817700.0, step = 3401 (0.273 sec)
INFO:tensorflow:global_step/sec: 359.895
INFO:tensorflow:loss = 3334047000.0, step = 3501 (0.278 sec)
INFO:tensorflow:global_step/sec: 361.868
INFO:tensorflow:loss = 2383469000.0, step = 3601 (0.277 sec)
INFO:tensorflow:global_step/sec: 360.942
INFO:tensorflow:loss = 3146690300.0, step = 3701 (0.277 sec)
INFO:tensorflow:global_step/sec: 364.857
INFO:tensorflow:loss = 3484867300.0, step = 3801 (0.274 sec)
INFO:tensorflow:global_step/sec: 365.145
INFO:tensorflow:loss = 3740801500.0, step = 3901 (0.274 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
INFO:tensorflow:Loss for final step: 2773127700.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:03
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-4000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:03.030783: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.039854: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.186258: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:03.186273: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:03.191958: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.196869: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.202349: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.208122: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.214849: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.22921s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:03
INFO:tensorflow:Saving dict for global step 4000: average_loss = 228449630.0, global_step = 4000, label/mean = 13207.129, loss = 3532182800.0, prediction/mean = 244.41115
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-4000
scores_pca {'average_loss': 228449630.0, 'label/mean': 13207.129, 'loss': 3532182800.0, 'prediction/mean': 244.41115, 'global_step': 4000}
INFO:tensorflow:Calling model_fn.
2026-03-25 08:52:03.237091: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.245474: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.357515: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-4000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:03.505334: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:03.505350: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:03.510358: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.516042: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.521901: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.524525: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.530867: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:03.533954: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:52:03.749654: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
INFO:tensorflow:loss = 3113526800.0, step = 4001
2026-03-25 08:52:03.976450: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:04.059136: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 280.778
INFO:tensorflow:loss = 2530833700.0, step = 4101 (0.357 sec)
INFO:tensorflow:global_step/sec: 343.384
INFO:tensorflow:loss = 3083841000.0, step = 4201 (0.291 sec)
INFO:tensorflow:global_step/sec: 360.727
INFO:tensorflow:loss = 2940479500.0, step = 4301 (0.277 sec)
INFO:tensorflow:global_step/sec: 360.906
INFO:tensorflow:loss = 3296260900.0, step = 4401 (0.277 sec)
INFO:tensorflow:global_step/sec: 358.37
INFO:tensorflow:loss = 3889569000.0, step = 4501 (0.279 sec)
INFO:tensorflow:global_step/sec: 360.149
INFO:tensorflow:loss = 1740139300.0, step = 4601 (0.278 sec)
INFO:tensorflow:global_step/sec: 357.1
INFO:tensorflow:loss = 4450991600.0, step = 4701 (0.280 sec)
INFO:tensorflow:global_step/sec: 356.063
INFO:tensorflow:loss = 5171094500.0, step = 4801 (0.281 sec)
INFO:tensorflow:global_step/sec: 358.805
INFO:tensorflow:loss = 4111746300.0, step = 4901 (0.279 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
INFO:tensorflow:Loss for final step: 3743067100.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:07
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-5000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:07.011014: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.017288: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.162108: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:07.162123: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:07.169554: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.174640: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.179611: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.186092: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.193435: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.196593: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.23643s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:07
INFO:tensorflow:Saving dict for global step 5000: average_loss = 226191630.0, global_step = 5000, label/mean = 13207.129, loss = 3497270800.0, prediction/mean = 306.14865
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-5000
scores_pca {'average_loss': 226191630.0, 'label/mean': 13207.129, 'loss': 3497270800.0, 'prediction/mean': 306.14865, 'global_step': 5000}
INFO:tensorflow:Calling model_fn.
2026-03-25 08:52:07.227105: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.342640: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-5000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:07.488062: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:07.488077: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:07.493717: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.499465: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.505181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.507812: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.513576: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:07.517212: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:52:07.730862: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
INFO:tensorflow:loss = 1847405300.0, step = 5001
2026-03-25 08:52:07.956539: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:08.042130: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 308.106
INFO:tensorflow:loss = 2561151000.0, step = 5101 (0.325 sec)
INFO:tensorflow:global_step/sec: 358.831
INFO:tensorflow:loss = 3405713000.0, step = 5201 (0.279 sec)
INFO:tensorflow:global_step/sec: 360.317
INFO:tensorflow:loss = 3890040300.0, step = 5301 (0.278 sec)
INFO:tensorflow:global_step/sec: 358.21
INFO:tensorflow:loss = 3786860300.0, step = 5401 (0.279 sec)
INFO:tensorflow:global_step/sec: 345.817
INFO:tensorflow:loss = 2344774100.0, step = 5501 (0.289 sec)
INFO:tensorflow:global_step/sec: 360.366
INFO:tensorflow:loss = 4290479600.0, step = 5601 (0.278 sec)
INFO:tensorflow:global_step/sec: 360.566
INFO:tensorflow:loss = 3059039500.0, step = 5701 (0.277 sec)
INFO:tensorflow:global_step/sec: 362.185
INFO:tensorflow:loss = 3488011000.0, step = 5801 (0.276 sec)
INFO:tensorflow:global_step/sec: 364.551
INFO:tensorflow:loss = 3387624700.0, step = 5901 (0.274 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
INFO:tensorflow:Loss for final step: 4146583600.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:11
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-6000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:10.950893: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:10.964473: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.108961: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:11.108977: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:11.114161: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.119447: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.125029: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.130676: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.138176: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.141579: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.22692s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:11
INFO:tensorflow:Saving dict for global step 6000: average_loss = 223955460.0, global_step = 6000, label/mean = 13207.129, loss = 3462696000.0, prediction/mean = 367.53073
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-6000
scores_pca {'average_loss': 223955460.0, 'label/mean': 13207.129, 'loss': 3462696000.0, 'prediction/mean': 367.53073, 'global_step': 6000}
INFO:tensorflow:Calling model_fn.
2026-03-25 08:52:11.167072: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.280211: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-6000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:11.481750: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:11.481766: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:11.486563: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.492345: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.498157: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.501311: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.507546: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:11.510772: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:52:11.725305: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
INFO:tensorflow:loss = 2075737300.0, step = 6001
2026-03-25 08:52:11.976217: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:12.072067: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 308.318
INFO:tensorflow:loss = 3829544400.0, step = 6101 (0.325 sec)
INFO:tensorflow:global_step/sec: 358.875
INFO:tensorflow:loss = 2505177000.0, step = 6201 (0.279 sec)
INFO:tensorflow:global_step/sec: 352.55
INFO:tensorflow:loss = 2158346800.0, step = 6301 (0.284 sec)
INFO:tensorflow:global_step/sec: 355.394
INFO:tensorflow:loss = 4479153700.0, step = 6401 (0.281 sec)
INFO:tensorflow:global_step/sec: 356.53
INFO:tensorflow:loss = 5098366500.0, step = 6501 (0.280 sec)
INFO:tensorflow:global_step/sec: 336.973
INFO:tensorflow:loss = 3648151600.0, step = 6601 (0.297 sec)
INFO:tensorflow:global_step/sec: 364.151
INFO:tensorflow:loss = 4922632000.0, step = 6701 (0.275 sec)
INFO:tensorflow:global_step/sec: 364.627
INFO:tensorflow:loss = 2585335600.0, step = 6801 (0.274 sec)
INFO:tensorflow:global_step/sec: 361.195
INFO:tensorflow:loss = 2642967600.0, step = 6901 (0.277 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
INFO:tensorflow:Loss for final step: 3983103200.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:15
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-7000
2026-03-25 08:52:15.129164: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.161631: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.323357: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:15.323373: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
INFO:tensorflow:Inference Time : 0.22676s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:15
INFO:tensorflow:Saving dict for global step 7000: average_loss = 221735540.0, global_step = 7000, label/mean = 13207.129, loss = 3428372500.0, prediction/mean = 428.69946
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-7000
2026-03-25 08:52:15.329826: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.334986: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.343018: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.349450: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.356974: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.360681: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.385122: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.492096: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
scores_pca {'average_loss': 221735540.0, 'label/mean': 13207.129, 'loss': 3428372500.0, 'prediction/mean': 428.69946, 'global_step': 7000}
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-7000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:15.640316: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:15.640332: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:15.645195: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.650932: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.656676: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.659725: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.665532: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:15.668641: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:52:15.885706: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
INFO:tensorflow:loss = 2629463600.0, step = 7001
2026-03-25 08:52:16.182521: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:16.261941: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 267.888
INFO:tensorflow:loss = 2163977200.0, step = 7101 (0.374 sec)
INFO:tensorflow:global_step/sec: 361.594
INFO:tensorflow:loss = 1644896500.0, step = 7201 (0.276 sec)
INFO:tensorflow:global_step/sec: 353.34
INFO:tensorflow:loss = 3462255000.0, step = 7301 (0.283 sec)
INFO:tensorflow:global_step/sec: 366
INFO:tensorflow:loss = 2045560300.0, step = 7401 (0.273 sec)
INFO:tensorflow:global_step/sec: 364.385
INFO:tensorflow:loss = 1818657400.0, step = 7501 (0.275 sec)
INFO:tensorflow:global_step/sec: 280.255
INFO:tensorflow:loss = 3233012200.0, step = 7601 (0.357 sec)
INFO:tensorflow:global_step/sec: 313.153
INFO:tensorflow:loss = 4024751900.0, step = 7701 (0.319 sec)
INFO:tensorflow:global_step/sec: 254.093
INFO:tensorflow:loss = 3453770800.0, step = 7801 (0.393 sec)
INFO:tensorflow:global_step/sec: 260.717
INFO:tensorflow:loss = 3583072000.0, step = 7901 (0.384 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
INFO:tensorflow:Loss for final step: 2795315200.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:19
2026-03-25 08:52:19.664477: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.691334: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-8000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:19.893519: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:19.893535: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:19.899583: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.904509: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.911693: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.918239: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.926104: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.929227: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:19.955614: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.087548: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.26323s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:20
INFO:tensorflow:Saving dict for global step 8000: average_loss = 219522670.0, global_step = 8000, label/mean = 13207.129, loss = 3394158300.0, prediction/mean = 489.83163
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-8000
scores_pca {'average_loss': 219522670.0, 'label/mean': 13207.129, 'loss': 3394158300.0, 'prediction/mean': 489.83163, 'global_step': 8000}
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-8000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:20.247288: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:20.247305: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:20.252660: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.259099: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.266191: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.269778: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.276559: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:20.279868: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
2026-03-25 08:52:20.557630: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
INFO:tensorflow:loss = 4510650400.0, step = 8001
2026-03-25 08:52:20.949683: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:21.060578: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 302.9
INFO:tensorflow:loss = 4622812000.0, step = 8101 (0.330 sec)
INFO:tensorflow:global_step/sec: 375.099
INFO:tensorflow:loss = 4961518600.0, step = 8201 (0.267 sec)
INFO:tensorflow:global_step/sec: 376.501
INFO:tensorflow:loss = 1894230300.0, step = 8301 (0.266 sec)
INFO:tensorflow:global_step/sec: 371.789
INFO:tensorflow:loss = 2071780700.0, step = 8401 (0.269 sec)
INFO:tensorflow:global_step/sec: 303.535
INFO:tensorflow:loss = 5827272000.0, step = 8501 (0.331 sec)
INFO:tensorflow:global_step/sec: 304.064
INFO:tensorflow:loss = 2608309800.0, step = 8601 (0.328 sec)
INFO:tensorflow:global_step/sec: 304.707
INFO:tensorflow:loss = 3162104300.0, step = 8701 (0.328 sec)
INFO:tensorflow:global_step/sec: 251.589
INFO:tensorflow:loss = 3034514400.0, step = 8801 (0.399 sec)
INFO:tensorflow:global_step/sec: 275.431
INFO:tensorflow:loss = 2491714800.0, step = 8901 (0.362 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
INFO:tensorflow:Loss for final step: 3870081300.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:24
2026-03-25 08:52:24.341531: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.370119: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-9000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:24.546037: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:24.546051: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:24.552266: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.560012: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.567717: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.574960: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.582365: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.585660: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.610252: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.733026: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.25250s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:24
INFO:tensorflow:Saving dict for global step 9000: average_loss = 217329600.0, global_step = 9000, label/mean = 13207.129, loss = 3360250000.0, prediction/mean = 550.6421
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-9000
scores_pca {'average_loss': 217329600.0, 'label/mean': 13207.129, 'loss': 3360250000.0, 'prediction/mean': 550.6421, 'global_step': 9000}
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Create CheckpointSaverHook.
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-9000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:24.889014: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:24.889030: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:24.894306: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.900102: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.905622: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.908277: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.914062: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:24.917893: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
INFO:tensorflow:loss = 7368299000.0, step = 9001
2026-03-25 08:52:25.341301: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:25.438447: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:25.515474: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:global_step/sec: 316.717
INFO:tensorflow:loss = 4305154000.0, step = 9101 (0.316 sec)
INFO:tensorflow:global_step/sec: 364.759
INFO:tensorflow:loss = 1948509000.0, step = 9201 (0.275 sec)
INFO:tensorflow:global_step/sec: 357.919
INFO:tensorflow:loss = 2436993000.0, step = 9301 (0.279 sec)
INFO:tensorflow:global_step/sec: 356.767
INFO:tensorflow:loss = 2793172000.0, step = 9401 (0.280 sec)
INFO:tensorflow:global_step/sec: 366.199
INFO:tensorflow:loss = 4266612200.0, step = 9501 (0.273 sec)
INFO:tensorflow:global_step/sec: 361.914
INFO:tensorflow:loss = 3998146600.0, step = 9601 (0.276 sec)
INFO:tensorflow:global_step/sec: 368.638
INFO:tensorflow:loss = 3401011700.0, step = 9701 (0.271 sec)
INFO:tensorflow:global_step/sec: 370.269
INFO:tensorflow:loss = 3072115200.0, step = 9801 (0.270 sec)
INFO:tensorflow:global_step/sec: 371.122
INFO:tensorflow:loss = 4841378000.0, step = 9901 (0.269 sec)
INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt.
INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
INFO:tensorflow:Loss for final step: 4222898200.0.
INFO:tensorflow:Calling model_fn.
INFO:tensorflow:Done calling model_fn.
INFO:tensorflow:Starting evaluation at 2026-03-25T08:52:28
INFO:tensorflow:Graph was finalized.
INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-10000
INFO:tensorflow:Running local_init_op.
INFO:tensorflow:Done running local_init_op.
2026-03-25 08:52:28.374326: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.380763: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.519290: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
2026-03-25 08:52:28.519304: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
2026-03-25 08:52:28.524502: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.529224: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.534775: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.540287: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.547766: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.551380: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
INFO:tensorflow:Inference Time : 0.21718s
INFO:tensorflow:Finished evaluation at 2026-03-25-08:52:28
INFO:tensorflow:Saving dict for global step 10000: average_loss = 215141230.0, global_step = 10000, label/mean = 13207.129, loss = 3326414600.0, prediction/mean = 611.4599
INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpe18ds6yw/model.ckpt-10000
scores_pca {'average_loss': 215141230.0, 'label/mean': 13207.129, 'loss': 3326414600.0, 'prediction/mean': 611.4599, 'global_step': 10000}
2026-03-25 08:52:28.576262: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
2026-03-25 08:52:28.681926: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
'''
```

### Task 3: Make your best model using only categorical features

- Look at the possible feature columns for categorical features. They begin with `categorical_column_with_` in go/tf-ops.
- You may find `dataframe[categorical_feature_names].unique()` helpful.



```python
## Your code goes here
car_data[feature_name].unique()
```




    array([21.  ,  9.6 ,  8.1 ,  9.2 ,  9.4 ,  8.8 , 21.9 ,  7.5 ,  7.  ,
            8.5 , 23.  , 10.1 ,  8.7 ,  9.3 ,  8.4 ,  7.6 ,  9.  ,  8.3 ,
            9.5 ,  8.6 ,  8.  ,  9.41, 21.5 , 22.5 ,  7.7 ,  7.8 , 11.5 ,
            9.1 , 10.  , 22.7 , 22.  ,  9.31])




```python
#@title Possible solution
# We have the full list of values that each feature takes on, and the list is
# relatively small so we use categorical_column_with_vocabulary_list.

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

est = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=[64],
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.01),
  )

# TRAIN
num_print_statements = 10
num_training_steps = 10000
for _ in range(num_print_statements):
  est.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores = est.evaluate(eval_input_fn)

  # The `scores` dictionary has several metrics automatically generated by the
  # canned Estimator.
  # `average_loss` is the average loss for an individual example.
  # `loss` is the summed loss for the batch.
  # In addition to these scalar losses, you may find the visualization functions
  # in the next cell helpful for debugging model quality.
  print('scores', scores)


```

### Task 4: Using all the features, make the best model that you can make

With all the features combined, your model should perform better than your earlier models using numerical and categorical models alone. Tune your model until that is the case.


```python
## Your code goes here
```


```python
#@title Possible solution
# This is a first pass at a model that uses all the features.
# Do you have any improvements?

batch_size = 16

x_df = car_data[numeric_feature_names + categorical_feature_names]
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

epsilon = 0.000001
model_feature_columns = [
    tf.feature_column.indicator_column(
        tf.feature_column.categorical_column_with_vocabulary_list(
            feature_name, vocabulary_list=car_data[feature_name].unique()))
    for feature_name in categorical_feature_names
] + [
    tf.feature_column.numeric_column(feature_name,
                                     normalizer_fn=lambda val: (val - x_df.mean()[feature_name]) / (epsilon + x_df.std()[feature_name]))
    for feature_name in numeric_feature_names
]


print('model_feature_columns', model_feature_columns)

est = tf.estimator.DNNRegressor(
    feature_columns=model_feature_columns,
    hidden_units=[64],
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.01),
  )

# TRAIN
num_print_statements = 10
num_training_steps = 10000
for _ in range(num_print_statements):
  est.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores = est.evaluate(eval_input_fn)

  # The `scores` dictionary has several metrics automatically generated by the
  # canned Estimator.
  # `average_loss` is the average loss for an individual example.
  # `loss` is the summed loss for the batch.
  # In addition to these scalar losses, you may find the visualization functions
  # in the next cell helpful for debugging model quality.
  print('scores', scores)


```
