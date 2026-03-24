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

### Libraries + Setup


```python
%reset -f
import numpy as np
import pandas as pd
import math

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# Set pandas output display to have one digit for decimal places and limit it to
# printing 15 rows.
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
      <th>77</th>
      <td>2</td>
      <td>161</td>
      <td>mitsubishi</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>hatchback</td>
      <td>fwd</td>
      <td>front</td>
      <td>93.70</td>
      <td>...</td>
      <td>92</td>
      <td>2bbl</td>
      <td>2.97</td>
      <td>3.23</td>
      <td>9.40</td>
      <td>68</td>
      <td>5500</td>
      <td>31</td>
      <td>38</td>
      <td>6189</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0</td>
      <td>81</td>
      <td>chevrolet</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>sedan</td>
      <td>fwd</td>
      <td>front</td>
      <td>94.50</td>
      <td>...</td>
      <td>90</td>
      <td>2bbl</td>
      <td>3.03</td>
      <td>3.11</td>
      <td>9.60</td>
      <td>70</td>
      <td>5400</td>
      <td>38</td>
      <td>43</td>
      <td>6575</td>
    </tr>
    <tr>
      <th>16</th>
      <td>0</td>
      <td>?</td>
      <td>bmw</td>
      <td>gas</td>
      <td>std</td>
      <td>two</td>
      <td>sedan</td>
      <td>rwd</td>
      <td>front</td>
      <td>103.50</td>
      <td>...</td>
      <td>209</td>
      <td>mpfi</td>
      <td>3.62</td>
      <td>3.39</td>
      <td>8.00</td>
      <td>182</td>
      <td>5400</td>
      <td>16</td>
      <td>22</td>
      <td>41315</td>
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
    Index: 205 entries, 201 to 190
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
      <th>201</th>
      <td>-1</td>
      <td>95</td>
      <td>109.10</td>
      <td>188.80</td>
      <td>68.80</td>
      <td>55.50</td>
      <td>3049</td>
      <td>141</td>
      <td>160</td>
      <td>5300</td>
      <td>19</td>
      <td>25</td>
      <td>3.78</td>
      <td>3.15</td>
      <td>8.70</td>
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
    <tr>
      <th>35</th>
      <td>0</td>
      <td>110</td>
      <td>96.50</td>
      <td>163.40</td>
      <td>64.00</td>
      <td>54.50</td>
      <td>2010</td>
      <td>92</td>
      <td>76</td>
      <td>6000</td>
      <td>30</td>
      <td>34</td>
      <td>2.91</td>
      <td>3.41</td>
      <td>9.20</td>
    </tr>
    <tr>
      <th>203</th>
      <td>-1</td>
      <td>95</td>
      <td>109.10</td>
      <td>188.80</td>
      <td>68.90</td>
      <td>55.50</td>
      <td>3217</td>
      <td>145</td>
      <td>106</td>
      <td>4800</td>
      <td>26</td>
      <td>27</td>
      <td>3.01</td>
      <td>3.40</td>
      <td>23.00</td>
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
      <th>58</th>
      <td>3</td>
      <td>150</td>
      <td>95.30</td>
      <td>169.00</td>
      <td>65.70</td>
      <td>49.60</td>
      <td>2500</td>
      <td>80</td>
      <td>135</td>
      <td>6000</td>
      <td>16</td>
      <td>23</td>
      <td>?</td>
      <td>?</td>
      <td>9.40</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2</td>
      <td>121</td>
      <td>88.40</td>
      <td>141.10</td>
      <td>60.30</td>
      <td>53.20</td>
      <td>1488</td>
      <td>61</td>
      <td>48</td>
      <td>5100</td>
      <td>47</td>
      <td>53</td>
      <td>2.91</td>
      <td>3.03</td>
      <td>9.50</td>
    </tr>
    <tr>
      <th>14</th>
      <td>1</td>
      <td>?</td>
      <td>103.50</td>
      <td>189.00</td>
      <td>66.90</td>
      <td>55.70</td>
      <td>3055</td>
      <td>164</td>
      <td>121</td>
      <td>4250</td>
      <td>20</td>
      <td>25</td>
      <td>3.31</td>
      <td>3.19</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>180</th>
      <td>-1</td>
      <td>90</td>
      <td>104.50</td>
      <td>187.80</td>
      <td>66.50</td>
      <td>54.10</td>
      <td>3131</td>
      <td>171</td>
      <td>156</td>
      <td>5200</td>
      <td>20</td>
      <td>24</td>
      <td>3.27</td>
      <td>3.35</td>
      <td>9.20</td>
    </tr>
    <tr>
      <th>190</th>
      <td>3</td>
      <td>256</td>
      <td>94.50</td>
      <td>165.70</td>
      <td>64.00</td>
      <td>51.40</td>
      <td>2221</td>
      <td>109</td>
      <td>90</td>
      <td>5500</td>
      <td>24</td>
      <td>29</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>8.50</td>
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
      <th>fuel-system</th>
      <th>make</th>
      <th>aspiration</th>
      <th>num-cylinders</th>
      <th>num-doors</th>
      <th>fuel-type</th>
      <th>engine-location</th>
      <th>body-style</th>
      <th>engine-type</th>
      <th>drive-wheels</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>201</th>
      <td>mpfi</td>
      <td>volvo</td>
      <td>turbo</td>
      <td>four</td>
      <td>four</td>
      <td>gas</td>
      <td>front</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>rwd</td>
    </tr>
    <tr>
      <th>183</th>
      <td>mpfi</td>
      <td>volkswagen</td>
      <td>std</td>
      <td>four</td>
      <td>two</td>
      <td>gas</td>
      <td>front</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>fwd</td>
    </tr>
    <tr>
      <th>35</th>
      <td>1bbl</td>
      <td>honda</td>
      <td>std</td>
      <td>four</td>
      <td>four</td>
      <td>gas</td>
      <td>front</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>fwd</td>
    </tr>
    <tr>
      <th>203</th>
      <td>idi</td>
      <td>volvo</td>
      <td>turbo</td>
      <td>six</td>
      <td>four</td>
      <td>diesel</td>
      <td>front</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>rwd</td>
    </tr>
    <tr>
      <th>77</th>
      <td>2bbl</td>
      <td>mitsubishi</td>
      <td>std</td>
      <td>four</td>
      <td>two</td>
      <td>gas</td>
      <td>front</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>fwd</td>
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
      <th>58</th>
      <td>mpfi</td>
      <td>mazda</td>
      <td>std</td>
      <td>two</td>
      <td>two</td>
      <td>gas</td>
      <td>front</td>
      <td>hatchback</td>
      <td>rotor</td>
      <td>rwd</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2bbl</td>
      <td>chevrolet</td>
      <td>std</td>
      <td>three</td>
      <td>two</td>
      <td>gas</td>
      <td>front</td>
      <td>hatchback</td>
      <td>l</td>
      <td>fwd</td>
    </tr>
    <tr>
      <th>14</th>
      <td>mpfi</td>
      <td>bmw</td>
      <td>std</td>
      <td>six</td>
      <td>four</td>
      <td>gas</td>
      <td>front</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>rwd</td>
    </tr>
    <tr>
      <th>180</th>
      <td>mpfi</td>
      <td>toyota</td>
      <td>std</td>
      <td>six</td>
      <td>four</td>
      <td>gas</td>
      <td>front</td>
      <td>sedan</td>
      <td>dohc</td>
      <td>rwd</td>
    </tr>
    <tr>
      <th>190</th>
      <td>mpfi</td>
      <td>volkswagen</td>
      <td>std</td>
      <td>four</td>
      <td>two</td>
      <td>gas</td>
      <td>front</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>fwd</td>
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
    
    WARNING:tensorflow:From /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/ipykernel_24013/741504662.py:29: The name tf.estimator.inputs.pandas_input_fn is deprecated. Please use tf.compat.v1.estimator.inputs.pandas_input_fn instead.
    
    model_feature_columns [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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


    2026-03-24 18:53:42.737021: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:42.737133: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:42.751413: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:42.751425: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:42.754854: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
    2026-03-24 18:53:42.760539: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz
    2026-03-24 18:53:42.767612: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:42.799047: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:42.805398: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:42.807911: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:42.813819: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:42.817320: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...


    2026-03-24 18:53:43.491289: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:43.587791: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 1874729500.0, step = 1


    2026-03-24 18:53:44.973599: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 244.821
    INFO:tensorflow:loss = 1469892500.0, step = 101 (0.408 sec)
    INFO:tensorflow:global_step/sec: 310.362
    INFO:tensorflow:loss = 173305580.0, step = 201 (0.322 sec)
    INFO:tensorflow:global_step/sec: 312.764
    INFO:tensorflow:loss = 807437400.0, step = 301 (0.320 sec)
    INFO:tensorflow:global_step/sec: 314.005
    INFO:tensorflow:loss = 984429060.0, step = 401 (0.319 sec)
    INFO:tensorflow:global_step/sec: 311.441
    INFO:tensorflow:loss = 958179700.0, step = 501 (0.321 sec)
    INFO:tensorflow:global_step/sec: 315.471
    INFO:tensorflow:loss = 542195300.0, step = 601 (0.317 sec)
    INFO:tensorflow:global_step/sec: 309.562
    INFO:tensorflow:loss = 690635100.0, step = 701 (0.323 sec)
    INFO:tensorflow:global_step/sec: 313.813
    INFO:tensorflow:loss = 628799360.0, step = 801 (0.319 sec)
    INFO:tensorflow:global_step/sec: 314.378
    INFO:tensorflow:loss = 658373300.0, step = 901 (0.318 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 356326940.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:53:48
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:48.398052: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.408308: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.548476: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:48.548490: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:48.553767: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.559065: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.563940: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.569091: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.575374: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.578808: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:48.607529: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.60237s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:53:49
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 34788468.0, global_step = 1000, label/mean = 13207.129, loss = 537883200.0, prediction/mean = 13005.149


    2026-03-24 18:53:49.032599: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-1000
    scores {'average_loss': 34788468.0, 'label/mean': 13207.129, 'loss': 537883200.0, 'prediction/mean': 13005.149, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-1000
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1173: get_checkpoint_mtimes (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file utilities to get mtimes.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:49.462500: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:49.462514: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:49.467711: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.473689: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.478869: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.481085: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.486580: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.489823: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...


    2026-03-24 18:53:49.778693: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:49.928368: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 693680100.0, step = 1001


    2026-03-24 18:53:50.012077: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 272.789
    INFO:tensorflow:loss = 504104200.0, step = 1101 (0.367 sec)
    INFO:tensorflow:global_step/sec: 317.092
    INFO:tensorflow:loss = 280671360.0, step = 1201 (0.315 sec)
    INFO:tensorflow:global_step/sec: 319.409
    INFO:tensorflow:loss = 412695200.0, step = 1301 (0.313 sec)
    INFO:tensorflow:global_step/sec: 319.072
    INFO:tensorflow:loss = 118491780.0, step = 1401 (0.313 sec)
    INFO:tensorflow:global_step/sec: 321.539
    INFO:tensorflow:loss = 97732760.0, step = 1501 (0.311 sec)
    INFO:tensorflow:global_step/sec: 322.134
    INFO:tensorflow:loss = 1059139000.0, step = 1601 (0.311 sec)
    INFO:tensorflow:global_step/sec: 322.298
    INFO:tensorflow:loss = 1022688600.0, step = 1701 (0.310 sec)
    INFO:tensorflow:global_step/sec: 321.557
    INFO:tensorflow:loss = 266987200.0, step = 1801 (0.311 sec)
    INFO:tensorflow:global_step/sec: 318.867
    INFO:tensorflow:loss = 413633200.0, step = 1901 (0.314 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 528289180.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:53:53
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:53.269673: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.275156: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.419302: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:53.419317: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:53.424296: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.429170: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.434058: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.439675: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.446102: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.469337: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.23675s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:53:53
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 25741366.0, global_step = 2000, label/mean = 13207.129, loss = 398001120.0, prediction/mean = 13261.74
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-2000
    scores {'average_loss': 25741366.0, 'label/mean': 13207.129, 'loss': 398001120.0, 'prediction/mean': 13261.74, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:53:53.480512: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.599712: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:53.742383: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:53.742398: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:53.747471: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.752945: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.758315: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.760649: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.766124: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:53.769614: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 185333970.0, step = 2001


    2026-03-24 18:53:54.120547: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:54.216050: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:54.300619: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 262.36
    INFO:tensorflow:loss = 276159420.0, step = 2101 (0.381 sec)
    INFO:tensorflow:global_step/sec: 297.998
    INFO:tensorflow:loss = 292038750.0, step = 2201 (0.336 sec)
    INFO:tensorflow:global_step/sec: 290.538
    INFO:tensorflow:loss = 207943920.0, step = 2301 (0.344 sec)
    INFO:tensorflow:global_step/sec: 306.741
    INFO:tensorflow:loss = 437351300.0, step = 2401 (0.326 sec)
    INFO:tensorflow:global_step/sec: 307.088
    INFO:tensorflow:loss = 377883900.0, step = 2501 (0.326 sec)
    INFO:tensorflow:global_step/sec: 309.138
    INFO:tensorflow:loss = 587373250.0, step = 2601 (0.324 sec)
    INFO:tensorflow:global_step/sec: 308.974
    INFO:tensorflow:loss = 407790050.0, step = 2701 (0.324 sec)
    INFO:tensorflow:global_step/sec: 309.577
    INFO:tensorflow:loss = 261551520.0, step = 2801 (0.323 sec)
    INFO:tensorflow:global_step/sec: 308.637
    INFO:tensorflow:loss = 608837950.0, step = 2901 (0.324 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 418417300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:53:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:57.766355: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.772015: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.914244: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:57.914258: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:57.919486: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.924728: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.929951: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.935239: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.941820: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:57.945311: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.23294s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:53:58
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 22264896.0, global_step = 3000, label/mean = 13207.129, loss = 344249540.0, prediction/mean = 13495.587
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-3000
    scores {'average_loss': 22264896.0, 'label/mean': 13207.129, 'loss': 344249540.0, 'prediction/mean': 13495.587, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:53:57.973061: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.095181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:53:58.237181: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:53:58.237195: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:53:58.242392: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.247867: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.253258: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.255544: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.261431: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.264635: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 103963950.0, step = 3001


    2026-03-24 18:53:58.573869: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.672040: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:53:58.756392: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 248.721
    INFO:tensorflow:loss = 282125440.0, step = 3101 (0.403 sec)
    INFO:tensorflow:global_step/sec: 273.275
    INFO:tensorflow:loss = 234628140.0, step = 3201 (0.366 sec)
    INFO:tensorflow:global_step/sec: 291.724
    INFO:tensorflow:loss = 536921200.0, step = 3301 (0.343 sec)
    INFO:tensorflow:global_step/sec: 263.701
    INFO:tensorflow:loss = 92726380.0, step = 3401 (0.379 sec)
    INFO:tensorflow:global_step/sec: 309.06
    INFO:tensorflow:loss = 886974850.0, step = 3501 (0.324 sec)
    INFO:tensorflow:global_step/sec: 308.855
    INFO:tensorflow:loss = 169892460.0, step = 3601 (0.324 sec)
    INFO:tensorflow:global_step/sec: 304.754
    INFO:tensorflow:loss = 81300536.0, step = 3701 (0.328 sec)
    INFO:tensorflow:global_step/sec: 302.792
    INFO:tensorflow:loss = 581114500.0, step = 3801 (0.330 sec)
    INFO:tensorflow:global_step/sec: 302.565
    INFO:tensorflow:loss = 776753100.0, step = 3901 (0.331 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 316241340.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:02.381941: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.388224: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.534888: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:02.534903: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:02.540178: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.545042: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.549888: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.555016: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.561612: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.565067: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.23450s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:02
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 20803628.0, global_step = 4000, label/mean = 13207.129, loss = 321656100.0, prediction/mean = 13314.607
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-4000
    scores {'average_loss': 20803628.0, 'label/mean': 13207.129, 'loss': 321656100.0, 'prediction/mean': 13314.607, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:54:02.592826: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.718048: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:02.860390: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:02.860405: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:02.865958: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.871653: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.877032: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.879345: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.885019: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:02.888379: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...


    2026-03-24 18:54:03.188150: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:03.349607: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 69778080.0, step = 4001


    2026-03-24 18:54:03.436510: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 256.764
    INFO:tensorflow:loss = 156312510.0, step = 4101 (0.390 sec)
    INFO:tensorflow:global_step/sec: 295.378
    INFO:tensorflow:loss = 485041120.0, step = 4201 (0.338 sec)
    INFO:tensorflow:global_step/sec: 309.077
    INFO:tensorflow:loss = 1183421700.0, step = 4301 (0.323 sec)
    INFO:tensorflow:global_step/sec: 306.988
    INFO:tensorflow:loss = 422433570.0, step = 4401 (0.326 sec)
    INFO:tensorflow:global_step/sec: 309.249
    INFO:tensorflow:loss = 388537100.0, step = 4501 (0.323 sec)
    INFO:tensorflow:global_step/sec: 302.285
    INFO:tensorflow:loss = 657063600.0, step = 4601 (0.331 sec)
    INFO:tensorflow:global_step/sec: 299.123
    INFO:tensorflow:loss = 99003020.0, step = 4701 (0.334 sec)
    INFO:tensorflow:global_step/sec: 296.478
    INFO:tensorflow:loss = 329217630.0, step = 4801 (0.337 sec)
    INFO:tensorflow:global_step/sec: 301.374
    INFO:tensorflow:loss = 246312830.0, step = 4901 (0.332 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1064: remove_checkpoint (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file APIs to delete files with this prefix.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 453677440.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:54:06.915690: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:06.987531: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:07
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:07.204817: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:07.204832: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:07.210918: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.217460: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.222969: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.228662: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.235661: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.239136: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.268247: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.38643s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:07
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 20106588.0, global_step = 5000, label/mean = 13207.129, loss = 310878800.0, prediction/mean = 13282.719
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-5000
    scores {'average_loss': 20106588.0, 'label/mean': 13207.129, 'loss': 310878800.0, 'prediction/mean': 13282.719, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-5000


    2026-03-24 18:54:07.519885: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.700949: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:07.700965: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:07.708006: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.715273: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:07.722379: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.725361: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.732329: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:07.736443: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...


    2026-03-24 18:54:08.099707: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:08.282129: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 235083250.0, step = 5001


    2026-03-24 18:54:08.407653: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 170.928
    INFO:tensorflow:loss = 523824900.0, step = 5101 (0.585 sec)
    INFO:tensorflow:global_step/sec: 204.297
    INFO:tensorflow:loss = 191893180.0, step = 5201 (0.490 sec)
    INFO:tensorflow:global_step/sec: 202.037
    INFO:tensorflow:loss = 279412500.0, step = 5301 (0.495 sec)
    INFO:tensorflow:global_step/sec: 197.258
    INFO:tensorflow:loss = 373805220.0, step = 5401 (0.507 sec)
    INFO:tensorflow:global_step/sec: 218.289
    INFO:tensorflow:loss = 195732960.0, step = 5501 (0.458 sec)
    INFO:tensorflow:global_step/sec: 197.803
    INFO:tensorflow:loss = 72016500.0, step = 5601 (0.506 sec)
    INFO:tensorflow:global_step/sec: 203.196
    INFO:tensorflow:loss = 555343600.0, step = 5701 (0.492 sec)
    INFO:tensorflow:global_step/sec: 185.932
    INFO:tensorflow:loss = 645110340.0, step = 5801 (0.541 sec)
    INFO:tensorflow:global_step/sec: 151.067
    INFO:tensorflow:loss = 237045250.0, step = 5901 (0.664 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 118105770.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-6000


    2026-03-24 18:54:13.697365: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.726851: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.891927: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:13.891940: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:13.897879: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.902893: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.909989: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.916294: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.923271: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.926964: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:13.958435: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.091147: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.25646s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:14
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 19675874.0, global_step = 6000, label/mean = 13207.129, loss = 304219300.0, prediction/mean = 13336.821
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-6000
    scores {'average_loss': 19675874.0, 'label/mean': 13207.129, 'loss': 304219300.0, 'prediction/mean': 13336.821, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:14.245196: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:14.245211: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:14.250503: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.256286: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.262143: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.264585: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.270528: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.273787: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...


    2026-03-24 18:54:14.605591: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:14.764832: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 178838980.0, step = 6001


    2026-03-24 18:54:14.856108: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 261.352
    INFO:tensorflow:loss = 116535690.0, step = 6101 (0.383 sec)
    INFO:tensorflow:global_step/sec: 300.687
    INFO:tensorflow:loss = 149428820.0, step = 6201 (0.332 sec)
    INFO:tensorflow:global_step/sec: 303.895
    INFO:tensorflow:loss = 292281020.0, step = 6301 (0.329 sec)
    INFO:tensorflow:global_step/sec: 299.282
    INFO:tensorflow:loss = 911454700.0, step = 6401 (0.334 sec)
    INFO:tensorflow:global_step/sec: 263.393
    INFO:tensorflow:loss = 212434600.0, step = 6501 (0.379 sec)
    INFO:tensorflow:global_step/sec: 300.674
    INFO:tensorflow:loss = 973313400.0, step = 6601 (0.333 sec)
    INFO:tensorflow:global_step/sec: 303.759
    INFO:tensorflow:loss = 786097700.0, step = 6701 (0.330 sec)
    INFO:tensorflow:global_step/sec: 302.066
    INFO:tensorflow:loss = 90296630.0, step = 6801 (0.331 sec)
    INFO:tensorflow:global_step/sec: 302.745
    INFO:tensorflow:loss = 59995908.0, step = 6901 (0.330 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 477567900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:18


    2026-03-24 18:54:18.353295: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.359044: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:18.563809: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:18.563823: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:18.570371: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.575443: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.580434: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.585969: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.592518: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.596365: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.625179: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.756222: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.30681s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:18
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 19375176.0, global_step = 7000, label/mean = 13207.129, loss = 299570020.0, prediction/mean = 13404.261
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-7000
    scores {'average_loss': 19375176.0, 'label/mean': 13207.129, 'loss': 299570020.0, 'prediction/mean': 13404.261, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:18.900422: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:18.900439: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:18.905613: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.911162: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.917441: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.919948: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.925743: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:18.929141: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 168198200.0, step = 7001


    2026-03-24 18:54:19.237002: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:19.334471: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:19.429118: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 261.967
    INFO:tensorflow:loss = 165614160.0, step = 7101 (0.382 sec)
    INFO:tensorflow:global_step/sec: 305.385
    INFO:tensorflow:loss = 741823940.0, step = 7201 (0.327 sec)
    INFO:tensorflow:global_step/sec: 306.739
    INFO:tensorflow:loss = 119313380.0, step = 7301 (0.326 sec)
    INFO:tensorflow:global_step/sec: 306.536
    INFO:tensorflow:loss = 329650270.0, step = 7401 (0.326 sec)
    INFO:tensorflow:global_step/sec: 308.9
    INFO:tensorflow:loss = 169146220.0, step = 7501 (0.324 sec)
    INFO:tensorflow:global_step/sec: 311.227
    INFO:tensorflow:loss = 117424880.0, step = 7601 (0.321 sec)
    INFO:tensorflow:global_step/sec: 308.709
    INFO:tensorflow:loss = 413625440.0, step = 7701 (0.324 sec)
    INFO:tensorflow:global_step/sec: 306.978
    INFO:tensorflow:loss = 312711230.0, step = 7801 (0.326 sec)
    INFO:tensorflow:global_step/sec: 307.373
    INFO:tensorflow:loss = 440025540.0, step = 7901 (0.325 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 165403490.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:23
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:22.886164: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:22.891897: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.039165: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:23.039180: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:23.044649: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.049483: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.054689: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.060170: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.066775: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.070190: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.25039s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:23
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 19137228.0, global_step = 8000, label/mean = 13207.129, loss = 295890980.0, prediction/mean = 13233.995
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-8000
    scores {'average_loss': 19137228.0, 'label/mean': 13207.129, 'loss': 295890980.0, 'prediction/mean': 13233.995, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:54:23.098342: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.232654: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:23.382690: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:23.382706: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:23.388121: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.394046: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.399524: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.401912: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.407877: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.411324: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 180997740.0, step = 8001


    2026-03-24 18:54:23.717786: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.815377: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:23.904677: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 270.405
    INFO:tensorflow:loss = 96743230.0, step = 8101 (0.370 sec)
    INFO:tensorflow:global_step/sec: 315.735
    INFO:tensorflow:loss = 321755780.0, step = 8201 (0.317 sec)
    INFO:tensorflow:global_step/sec: 317.503
    INFO:tensorflow:loss = 448485730.0, step = 8301 (0.315 sec)
    INFO:tensorflow:global_step/sec: 318.053
    INFO:tensorflow:loss = 412517900.0, step = 8401 (0.315 sec)
    INFO:tensorflow:global_step/sec: 314.09
    INFO:tensorflow:loss = 100277460.0, step = 8501 (0.318 sec)
    INFO:tensorflow:global_step/sec: 318.922
    INFO:tensorflow:loss = 330578800.0, step = 8601 (0.314 sec)
    INFO:tensorflow:global_step/sec: 313.527
    INFO:tensorflow:loss = 187899940.0, step = 8701 (0.319 sec)
    INFO:tensorflow:global_step/sec: 316.932
    INFO:tensorflow:loss = 195691740.0, step = 8801 (0.315 sec)
    INFO:tensorflow:global_step/sec: 318.368
    INFO:tensorflow:loss = 121289760.0, step = 8901 (0.314 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 163443740.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:27
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:27.267972: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.273615: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.420497: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:27.420514: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:27.425993: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.431270: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.436557: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.441956: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.448751: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.452217: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.23593s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:27
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 18924906.0, global_step = 9000, label/mean = 13207.129, loss = 292608200.0, prediction/mean = 13216.465
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-9000
    scores {'average_loss': 18924906.0, 'label/mean': 13207.129, 'loss': 292608200.0, 'prediction/mean': 13216.465, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.


    2026-03-24 18:54:27.480580: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.602859: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:27.752953: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:27.752967: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:27.758521: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.764244: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.769916: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.772371: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.778310: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:27.781649: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 161337860.0, step = 9001


    2026-03-24 18:54:28.091630: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:28.188350: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:28.276450: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 266.08
    INFO:tensorflow:loss = 107877900.0, step = 9101 (0.376 sec)
    INFO:tensorflow:global_step/sec: 311.086
    INFO:tensorflow:loss = 342167800.0, step = 9201 (0.322 sec)
    INFO:tensorflow:global_step/sec: 309.076
    INFO:tensorflow:loss = 175355740.0, step = 9301 (0.323 sec)
    INFO:tensorflow:global_step/sec: 307.634
    INFO:tensorflow:loss = 121066820.0, step = 9401 (0.325 sec)
    INFO:tensorflow:global_step/sec: 304.684
    INFO:tensorflow:loss = 141107840.0, step = 9501 (0.328 sec)
    INFO:tensorflow:global_step/sec: 309.841
    INFO:tensorflow:loss = 191325440.0, step = 9601 (0.323 sec)
    INFO:tensorflow:global_step/sec: 290.124
    INFO:tensorflow:loss = 142781550.0, step = 9701 (0.345 sec)
    INFO:tensorflow:global_step/sec: 313.028
    INFO:tensorflow:loss = 707623300.0, step = 9801 (0.320 sec)
    INFO:tensorflow:global_step/sec: 309.288
    INFO:tensorflow:loss = 144580700.0, step = 9901 (0.323 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 405119200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T18:54:31
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 18:54:31.727665: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.733204: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.881711: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 18:54:31.881725: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 18:54:31.887250: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.892043: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.897883: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.903600: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.910221: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:31.913846: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.24396s
    INFO:tensorflow:Finished evaluation at 2026-03-24-18:54:32
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 18720354.0, global_step = 10000, label/mean = 13207.129, loss = 289445470.0, prediction/mean = 13424.241
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-10000
    scores {'average_loss': 18720354.0, 'label/mean': 13207.129, 'loss': 289445470.0, 'prediction/mean': 13424.241, 'global_step': 10000}


    2026-03-24 18:54:31.943084: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 18:54:32.071350: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


### Visualize model's predictions

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
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpjvstsxlo/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:06:53.235097: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:06:53.235124: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:06:53.272707: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.377682: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.386048: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.391993: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.403933: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.423053: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:06:53.433509: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.



    
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

### Training model with numeric features + normalization


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
for _ in range(num_print_statements):
  est_zscore.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_zscore = est_zscore.evaluate(eval_input_fn)
  print('scores_zscore', scores_zscore)
for _ in range(num_print_statements):
  est_minmax.train(train_input_fn, steps=num_training_steps // num_print_statements)
  scores_minmax = est_minmax.evaluate(eval_input_fn)
  print('scores_minmax', scores_minmax)

# → pick the winner of 2.1 vs 2.2 based on final avg_loss and RMSE

# Task 2.3 try GradientDescentOptimizer with the same config → answers the lab's embedded question
# Task 2.3: GradientDescentOptimizer + Z-score normalization
# Hypothesis: with balanced gradients (Z-score), plain GD may now converge.
# lr=0.01 is too small for GD — using 0.5 to compensate for smaller gradient magnitudes post-normalisation.                                                
'''
cell below has details for Task 2.3
'''
```

    model_feature_columns_zscore [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301112560>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3011128c0>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3011131c0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280ca0>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280d30>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280c10>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280dc0>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280e50>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280ee0>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301280f70>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281000>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281090>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281120>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012811b0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281240>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    model_feature_columns_minmax [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012812d0>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281480>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012813f0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281510>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012815a0>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281630>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012816c0>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281750>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x3012817e0>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281870>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281900>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281990>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281a20>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281ab0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x301281b40>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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


    2026-03-24 19:22:21.275222: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:21.275275: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:21.316751: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.374534: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.387596: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.394642: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.409559: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.416719: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...


    2026-03-24 19:22:21.828995: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:21.952558: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2385768400.0, step = 1


    2026-03-24 19:22:22.141252: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 247.798
    INFO:tensorflow:loss = 3578241500.0, step = 101 (0.403 sec)
    INFO:tensorflow:global_step/sec: 245.112
    INFO:tensorflow:loss = 3453006800.0, step = 201 (0.408 sec)
    INFO:tensorflow:global_step/sec: 294.513
    INFO:tensorflow:loss = 3897490200.0, step = 301 (0.339 sec)
    INFO:tensorflow:global_step/sec: 290.613
    INFO:tensorflow:loss = 3909164000.0, step = 401 (0.344 sec)
    INFO:tensorflow:global_step/sec: 296.473
    INFO:tensorflow:loss = 4313395000.0, step = 501 (0.337 sec)
    INFO:tensorflow:global_step/sec: 294.148
    INFO:tensorflow:loss = 4531253000.0, step = 601 (0.340 sec)
    INFO:tensorflow:global_step/sec: 295.797
    INFO:tensorflow:loss = 6566283000.0, step = 701 (0.338 sec)
    INFO:tensorflow:global_step/sec: 296.424
    INFO:tensorflow:loss = 3363509200.0, step = 801 (0.337 sec)
    INFO:tensorflow:global_step/sec: 291.847
    INFO:tensorflow:loss = 8322281500.0, step = 901 (0.343 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3472619500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.


    2026-03-24 19:22:25.766723: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:25.805516: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:26
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:26.077212: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:26.077229: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:26.083690: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.090333: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.095566: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.101864: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.109054: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.112580: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.147871: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.270785: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.28475s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:26
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 232202900.0, global_step = 1000, label/mean = 13207.129, loss = 3590214000.0, prediction/mean = 143.37833
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-1000
    scores_zscore {'average_loss': 232202900.0, 'label/mean': 13207.129, 'loss': 3590214000.0, 'prediction/mean': 143.37833, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:26.662742: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:26.662756: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:26.668551: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.674407: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.680276: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.683492: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.690421: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:26.694036: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.


    2026-03-24 19:22:27.092745: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 3373830100.0, step = 1001


    2026-03-24 19:22:27.366032: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:27.489984: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 168.903
    INFO:tensorflow:loss = 4543638000.0, step = 1101 (0.592 sec)
    INFO:tensorflow:global_step/sec: 222.491
    INFO:tensorflow:loss = 2659392800.0, step = 1201 (0.450 sec)
    INFO:tensorflow:global_step/sec: 176.354
    INFO:tensorflow:loss = 1856305400.0, step = 1301 (0.574 sec)
    INFO:tensorflow:global_step/sec: 173.157
    INFO:tensorflow:loss = 5021828000.0, step = 1401 (0.574 sec)
    INFO:tensorflow:global_step/sec: 275.338
    INFO:tensorflow:loss = 2942186500.0, step = 1501 (0.359 sec)
    INFO:tensorflow:global_step/sec: 289.011
    INFO:tensorflow:loss = 3277020700.0, step = 1601 (0.346 sec)
    INFO:tensorflow:global_step/sec: 288.791
    INFO:tensorflow:loss = 5163257000.0, step = 1701 (0.346 sec)
    INFO:tensorflow:global_step/sec: 169.883
    INFO:tensorflow:loss = 2310058800.0, step = 1801 (0.590 sec)
    INFO:tensorflow:global_step/sec: 238.907
    INFO:tensorflow:loss = 3749071600.0, step = 1901 (0.417 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 4214552000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:32


    2026-03-24 19:22:32.173872: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.187810: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:32.379500: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:32.379517: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:32.386594: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.395619: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.402507: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.409293: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.416620: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.421107: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.457098: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.575880: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.27330s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:32
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 226840510.0, global_step = 2000, label/mean = 13207.129, loss = 3507303400.0, prediction/mean = 294.19873
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-2000
    scores_zscore {'average_loss': 226840510.0, 'label/mean': 13207.129, 'loss': 3507303400.0, 'prediction/mean': 294.19873, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:32.781584: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:32.781600: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:32.788404: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.796588: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.803567: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.807270: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.817883: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:32.826209: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.


    2026-03-24 19:22:33.304913: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 4105496000.0, step = 2001


    2026-03-24 19:22:33.517750: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:33.611621: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 250.235
    INFO:tensorflow:loss = 3259637500.0, step = 2101 (0.400 sec)
    INFO:tensorflow:global_step/sec: 292.692
    INFO:tensorflow:loss = 5335044000.0, step = 2201 (0.343 sec)
    INFO:tensorflow:global_step/sec: 194.511
    INFO:tensorflow:loss = 3212178400.0, step = 2301 (0.514 sec)
    INFO:tensorflow:global_step/sec: 217.711
    INFO:tensorflow:loss = 3152341200.0, step = 2401 (0.460 sec)
    INFO:tensorflow:global_step/sec: 219.451
    INFO:tensorflow:loss = 4605198300.0, step = 2501 (0.454 sec)
    INFO:tensorflow:global_step/sec: 201.024
    INFO:tensorflow:loss = 5102614000.0, step = 2601 (0.497 sec)
    INFO:tensorflow:global_step/sec: 265.971
    INFO:tensorflow:loss = 4042186800.0, step = 2701 (0.376 sec)
    INFO:tensorflow:global_step/sec: 294.138
    INFO:tensorflow:loss = 2135076700.0, step = 2801 (0.340 sec)
    INFO:tensorflow:global_step/sec: 288.923
    INFO:tensorflow:loss = 3523210000.0, step = 2901 (0.347 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 2166341600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:37
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:22:37.781381: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:37.787872: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:37.962514: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:37.962530: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:37.969382: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:37.974763: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:37.980905: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:37.987206: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:37.995224: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.000629: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.088205: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.31554s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:38
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 221591340.0, global_step = 3000, label/mean = 13207.129, loss = 3426143000.0, prediction/mean = 443.58072
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-3000
    scores_zscore {'average_loss': 221591340.0, 'label/mean': 13207.129, 'loss': 3426143000.0, 'prediction/mean': 443.58072, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:38.219844: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.393866: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:38.393880: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:38.399712: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.405743: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.412162: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.415927: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.422578: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:38.427545: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.


    2026-03-24 19:22:38.788143: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 6215642000.0, step = 3001


    2026-03-24 19:22:39.022511: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:39.136739: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 174.837
    INFO:tensorflow:loss = 2569671200.0, step = 3101 (0.570 sec)
    INFO:tensorflow:global_step/sec: 216.289
    INFO:tensorflow:loss = 4270257200.0, step = 3201 (0.462 sec)
    INFO:tensorflow:global_step/sec: 293.951
    INFO:tensorflow:loss = 2698637300.0, step = 3301 (0.340 sec)
    INFO:tensorflow:global_step/sec: 294.525
    INFO:tensorflow:loss = 3127115300.0, step = 3401 (0.339 sec)
    INFO:tensorflow:global_step/sec: 291.281
    INFO:tensorflow:loss = 3612695000.0, step = 3501 (0.343 sec)
    INFO:tensorflow:global_step/sec: 291.006
    INFO:tensorflow:loss = 5785264000.0, step = 3601 (0.344 sec)
    INFO:tensorflow:global_step/sec: 291.057
    INFO:tensorflow:loss = 3115710500.0, step = 3701 (0.344 sec)
    INFO:tensorflow:global_step/sec: 273.983
    INFO:tensorflow:loss = 3352952300.0, step = 3801 (0.365 sec)
    INFO:tensorflow:global_step/sec: 290.17
    INFO:tensorflow:loss = 2725387800.0, step = 3901 (0.345 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 3202238000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:43


    2026-03-24 19:22:43.062407: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.071023: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:43.272498: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:43.272512: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:43.281406: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.288169: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.294372: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.301532: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.309754: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.315073: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.352647: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.32312s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:43
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 216429890.0, global_step = 4000, label/mean = 13207.129, loss = 3346339000.0, prediction/mean = 591.80774
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-4000
    scores_zscore {'average_loss': 216429890.0, 'label/mean': 13207.129, 'loss': 3346339000.0, 'prediction/mean': 591.80774, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-4000


    2026-03-24 19:22:43.525612: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.715606: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:43.715621: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:43.722029: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:43.728447: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.735387: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.739445: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.745946: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:43.750533: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.


    2026-03-24 19:22:44.137641: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 2282615300.0, step = 4001


    2026-03-24 19:22:44.362460: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:44.481460: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 188.617
    INFO:tensorflow:loss = 4459066000.0, step = 4101 (0.530 sec)
    INFO:tensorflow:global_step/sec: 285.875
    INFO:tensorflow:loss = 2965186600.0, step = 4201 (0.350 sec)
    INFO:tensorflow:global_step/sec: 258.329
    INFO:tensorflow:loss = 4750317000.0, step = 4301 (0.387 sec)
    INFO:tensorflow:global_step/sec: 196.775
    INFO:tensorflow:loss = 4001790500.0, step = 4401 (0.508 sec)
    INFO:tensorflow:global_step/sec: 234.051
    INFO:tensorflow:loss = 2479652900.0, step = 4501 (0.427 sec)
    INFO:tensorflow:global_step/sec: 288.876
    INFO:tensorflow:loss = 1806749000.0, step = 4601 (0.346 sec)
    INFO:tensorflow:global_step/sec: 239.002
    INFO:tensorflow:loss = 3462546000.0, step = 4701 (0.419 sec)
    INFO:tensorflow:global_step/sec: 240.851
    INFO:tensorflow:loss = 2273031200.0, step = 4801 (0.415 sec)
    INFO:tensorflow:global_step/sec: 291.226
    INFO:tensorflow:loss = 3561656800.0, step = 4901 (0.343 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 2753644300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:48
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:22:48.651760: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.659262: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.832005: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:48.832019: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:48.838678: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.844209: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.850635: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:48.857413: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.866162: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.873729: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:48.912528: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.033168: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.25807s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:49
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 211321300.0, global_step = 5000, label/mean = 13207.129, loss = 3267352300.0, prediction/mean = 739.10144
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-5000
    scores_zscore {'average_loss': 211321300.0, 'label/mean': 13207.129, 'loss': 3267352300.0, 'prediction/mean': 739.10144, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:49.209192: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:49.209208: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:49.215258: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.221455: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.227288: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.231181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.237907: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.241632: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...


    2026-03-24 19:22:49.617258: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:49.737780: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2952367400.0, step = 5001


    2026-03-24 19:22:49.849740: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 179.822
    INFO:tensorflow:loss = 2875754800.0, step = 5101 (0.556 sec)
    INFO:tensorflow:global_step/sec: 269.617
    INFO:tensorflow:loss = 3005632500.0, step = 5201 (0.371 sec)
    INFO:tensorflow:global_step/sec: 291.24
    INFO:tensorflow:loss = 3827310000.0, step = 5301 (0.343 sec)
    INFO:tensorflow:global_step/sec: 292.441
    INFO:tensorflow:loss = 2540977700.0, step = 5401 (0.342 sec)
    INFO:tensorflow:global_step/sec: 289.808
    INFO:tensorflow:loss = 3609678800.0, step = 5501 (0.345 sec)
    INFO:tensorflow:global_step/sec: 295.494
    INFO:tensorflow:loss = 3539777800.0, step = 5601 (0.339 sec)
    INFO:tensorflow:global_step/sec: 213.709
    INFO:tensorflow:loss = 3030731300.0, step = 5701 (0.468 sec)
    INFO:tensorflow:global_step/sec: 265.537
    INFO:tensorflow:loss = 1900827400.0, step = 5801 (0.377 sec)
    INFO:tensorflow:global_step/sec: 251.958
    INFO:tensorflow:loss = 3552449800.0, step = 5901 (0.397 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 1439330600.0.
    INFO:tensorflow:Calling model_fn.


    2026-03-24 19:22:53.968090: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:53.974299: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:22:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:54.213309: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:54.213324: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:54.220236: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.225684: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.233014: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.239844: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.247934: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.252500: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.290432: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.31263s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:22:54
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 206325470.0, global_step = 6000, label/mean = 13207.129, loss = 3190109200.0, prediction/mean = 884.5667
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-6000
    scores_zscore {'average_loss': 206325470.0, 'label/mean': 13207.129, 'loss': 3190109200.0, 'prediction/mean': 884.5667, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.


    2026-03-24 19:22:54.458436: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:22:54.689896: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:22:54.689911: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:22:54.697277: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.705997: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.714737: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.719233: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.727514: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:54.744009: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...


    2026-03-24 19:22:55.315971: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:22:55.487379: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 4964247600.0, step = 6001


    2026-03-24 19:22:55.589840: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 175.96
    INFO:tensorflow:loss = 2117236100.0, step = 6101 (0.570 sec)
    INFO:tensorflow:global_step/sec: 234.087
    INFO:tensorflow:loss = 2975028700.0, step = 6201 (0.426 sec)
    INFO:tensorflow:global_step/sec: 198.053
    INFO:tensorflow:loss = 6470882300.0, step = 6301 (0.505 sec)
    INFO:tensorflow:global_step/sec: 178.592
    INFO:tensorflow:loss = 3595606000.0, step = 6401 (0.560 sec)
    INFO:tensorflow:global_step/sec: 138.418
    INFO:tensorflow:loss = 1800840000.0, step = 6501 (0.723 sec)
    INFO:tensorflow:global_step/sec: 227.805
    INFO:tensorflow:loss = 2453970400.0, step = 6601 (0.438 sec)
    INFO:tensorflow:global_step/sec: 266.434
    INFO:tensorflow:loss = 2442843600.0, step = 6701 (0.375 sec)
    INFO:tensorflow:global_step/sec: 286.271
    INFO:tensorflow:loss = 5467075600.0, step = 6801 (0.349 sec)
    INFO:tensorflow:global_step/sec: 288.194
    INFO:tensorflow:loss = 1751736200.0, step = 6901 (0.347 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 3628447700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:00
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-7000


    2026-03-24 19:23:00.466442: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.473512: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.656329: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:00.656344: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:00.663411: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:00.669309: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.675521: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.683686: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.699404: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.704720: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.739179: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:00.865369: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26965s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:00
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 201417840.0, global_step = 7000, label/mean = 13207.129, loss = 3114229800.0, prediction/mean = 1029.0739
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-7000
    scores_zscore {'average_loss': 201417840.0, 'label/mean': 13207.129, 'loss': 3114229800.0, 'prediction/mean': 1029.0739, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:01.053861: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:01.053876: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:01.059781: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.065698: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.073286: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.076163: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.082562: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.087449: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...


    2026-03-24 19:23:01.457174: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:01.568908: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3258411000.0, step = 7001


    2026-03-24 19:23:01.664891: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 189.855
    INFO:tensorflow:loss = 1458634800.0, step = 7101 (0.528 sec)
    INFO:tensorflow:global_step/sec: 205.224
    INFO:tensorflow:loss = 3386465300.0, step = 7201 (0.487 sec)
    INFO:tensorflow:global_step/sec: 202.244
    INFO:tensorflow:loss = 4947926500.0, step = 7301 (0.495 sec)
    INFO:tensorflow:global_step/sec: 165.342
    INFO:tensorflow:loss = 2716434400.0, step = 7401 (0.605 sec)
    INFO:tensorflow:global_step/sec: 255.004
    INFO:tensorflow:loss = 4165231900.0, step = 7501 (0.392 sec)
    INFO:tensorflow:global_step/sec: 287.022
    INFO:tensorflow:loss = 1642617300.0, step = 7601 (0.348 sec)
    INFO:tensorflow:global_step/sec: 236.872
    INFO:tensorflow:loss = 2620071400.0, step = 7701 (0.422 sec)
    INFO:tensorflow:global_step/sec: 179.157
    INFO:tensorflow:loss = 3548527000.0, step = 7801 (0.558 sec)
    INFO:tensorflow:global_step/sec: 283.381
    INFO:tensorflow:loss = 1635979300.0, step = 7901 (0.353 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 2732360200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:06


    2026-03-24 19:23:06.448609: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.456972: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:06.674651: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:06.674668: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:06.689594: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.698464: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.705535: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.711890: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.721273: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.727248: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:06.762964: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.35829s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:06
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 196636160.0, global_step = 8000, label/mean = 13207.129, loss = 3040297500.0, prediction/mean = 1171.7957
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-8000
    scores_zscore {'average_loss': 196636160.0, 'label/mean': 13207.129, 'loss': 3040297500.0, 'prediction/mean': 1171.7957, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.


    2026-03-24 19:23:06.935871: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:07.151350: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:07.151366: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:07.159224: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.166572: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.173733: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.176597: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.183305: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.187627: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...


    2026-03-24 19:23:07.572399: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:07.683220: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2777729500.0, step = 8001


    2026-03-24 19:23:07.774773: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 250.322
    INFO:tensorflow:loss = 2994704400.0, step = 8101 (0.400 sec)
    INFO:tensorflow:global_step/sec: 244.989
    INFO:tensorflow:loss = 1494462300.0, step = 8201 (0.408 sec)
    INFO:tensorflow:global_step/sec: 184.97
    INFO:tensorflow:loss = 3486764800.0, step = 8301 (0.541 sec)
    INFO:tensorflow:global_step/sec: 194.516
    INFO:tensorflow:loss = 2394225400.0, step = 8401 (0.515 sec)
    INFO:tensorflow:global_step/sec: 171.762
    INFO:tensorflow:loss = 2622241800.0, step = 8501 (0.581 sec)
    INFO:tensorflow:global_step/sec: 250.843
    INFO:tensorflow:loss = 2183117300.0, step = 8601 (0.398 sec)
    INFO:tensorflow:global_step/sec: 288.035
    INFO:tensorflow:loss = 3973632500.0, step = 8701 (0.347 sec)
    INFO:tensorflow:global_step/sec: 289.921
    INFO:tensorflow:loss = 3516562000.0, step = 8801 (0.345 sec)
    INFO:tensorflow:global_step/sec: 288.386
    INFO:tensorflow:loss = 2508073500.0, step = 8901 (0.347 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 2000966000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:12


    2026-03-24 19:23:12.113168: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.146845: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:12.340304: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:12.340321: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:12.348437: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.354802: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.361064: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.367980: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.375559: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.380138: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.414181: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.535545: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26605s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:12
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 191930100.0, global_step = 9000, label/mean = 13207.129, loss = 2967534600.0, prediction/mean = 1313.795
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-9000
    scores_zscore {'average_loss': 191930100.0, 'label/mean': 13207.129, 'loss': 2967534600.0, 'prediction/mean': 1313.795, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:12.707342: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:12.707356: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:12.714063: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.720221: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.726113: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.729821: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.736281: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:12.740081: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.


    2026-03-24 19:23:13.173015: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 3688002800.0, step = 9001


    2026-03-24 19:23:13.470248: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:13.589306: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 157.475
    INFO:tensorflow:loss = 4167891200.0, step = 9101 (0.636 sec)
    INFO:tensorflow:global_step/sec: 275.572
    INFO:tensorflow:loss = 2696352000.0, step = 9201 (0.362 sec)
    INFO:tensorflow:global_step/sec: 295.159
    INFO:tensorflow:loss = 1595183900.0, step = 9301 (0.339 sec)
    INFO:tensorflow:global_step/sec: 294.239
    INFO:tensorflow:loss = 4743180300.0, step = 9401 (0.340 sec)
    INFO:tensorflow:global_step/sec: 295.301
    INFO:tensorflow:loss = 1905428600.0, step = 9501 (0.339 sec)
    INFO:tensorflow:global_step/sec: 294.993
    INFO:tensorflow:loss = 3519519000.0, step = 9601 (0.339 sec)
    INFO:tensorflow:global_step/sec: 293.368
    INFO:tensorflow:loss = 2675734000.0, step = 9701 (0.341 sec)
    INFO:tensorflow:global_step/sec: 294.774
    INFO:tensorflow:loss = 2434888700.0, step = 9801 (0.339 sec)
    INFO:tensorflow:global_step/sec: 296.387
    INFO:tensorflow:loss = 2785156900.0, step = 9901 (0.338 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 2967459600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:17
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:17.395058: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.401229: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.569842: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:17.569856: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:17.576371: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.581622: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.588013: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.594041: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.25166s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:17
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 187324060.0, global_step = 10000, label/mean = 13207.129, loss = 2896318200.0, prediction/mean = 1454.8345
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmphp82oc5n/model.ckpt-10000


    2026-03-24 19:23:17.605934: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.638280: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.647720: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:17.763973: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    scores_zscore {'average_loss': 187324060.0, 'label/mean': 13207.129, 'loss': 2896318200.0, 'prediction/mean': 1454.8345, 'global_step': 10000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:18.166107: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:18.166123: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:18.173473: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.182804: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.190053: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.192991: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.199679: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.204134: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...


    2026-03-24 19:23:18.569806: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:18.681406: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2707964000.0, step = 1


    2026-03-24 19:23:18.773627: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 249.876
    INFO:tensorflow:loss = 3364904000.0, step = 101 (0.401 sec)
    INFO:tensorflow:global_step/sec: 292.018
    INFO:tensorflow:loss = 1530160400.0, step = 201 (0.343 sec)
    INFO:tensorflow:global_step/sec: 294.539
    INFO:tensorflow:loss = 4652916700.0, step = 301 (0.339 sec)
    INFO:tensorflow:global_step/sec: 296.474
    INFO:tensorflow:loss = 4816668000.0, step = 401 (0.337 sec)
    INFO:tensorflow:global_step/sec: 293.246
    INFO:tensorflow:loss = 2752913700.0, step = 501 (0.341 sec)
    INFO:tensorflow:global_step/sec: 294.91
    INFO:tensorflow:loss = 4218645200.0, step = 601 (0.339 sec)
    INFO:tensorflow:global_step/sec: 295.609
    INFO:tensorflow:loss = 6545966600.0, step = 701 (0.338 sec)
    INFO:tensorflow:global_step/sec: 195.701
    INFO:tensorflow:loss = 3838125000.0, step = 801 (0.511 sec)
    INFO:tensorflow:global_step/sec: 217.236
    INFO:tensorflow:loss = 3392277500.0, step = 901 (0.463 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3431394000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-1000


    2026-03-24 19:23:22.788330: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:22.795604: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:22.971051: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:22.971066: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:22.977640: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:22.983397: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:22.990077: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.057290: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.073634: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.078369: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.114874: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.42284s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:23
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 232308110.0, global_step = 1000, label/mean = 13207.129, loss = 3591840800.0, prediction/mean = 178.30788


    2026-03-24 19:23:23.334497: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-1000
    scores_minmax {'average_loss': 232308110.0, 'label/mean': 13207.129, 'loss': 3591840800.0, 'prediction/mean': 178.30788, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:23.811278: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:23.811293: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:23.816894: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.822830: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.829342: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.832223: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.838601: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:23.842424: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...


    2026-03-24 19:23:24.235830: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:24.344958: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 5391618600.0, step = 1001


    2026-03-24 19:23:24.440446: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 251.434
    INFO:tensorflow:loss = 6735295500.0, step = 1101 (0.398 sec)
    INFO:tensorflow:global_step/sec: 288.707
    INFO:tensorflow:loss = 2885263000.0, step = 1201 (0.346 sec)
    INFO:tensorflow:global_step/sec: 234.236
    INFO:tensorflow:loss = 5037987000.0, step = 1301 (0.427 sec)
    INFO:tensorflow:global_step/sec: 219.402
    INFO:tensorflow:loss = 4450662400.0, step = 1401 (0.456 sec)
    INFO:tensorflow:global_step/sec: 238.427
    INFO:tensorflow:loss = 2237241600.0, step = 1501 (0.419 sec)
    INFO:tensorflow:global_step/sec: 286.161
    INFO:tensorflow:loss = 2283651300.0, step = 1601 (0.350 sec)
    INFO:tensorflow:global_step/sec: 292.838
    INFO:tensorflow:loss = 4717850600.0, step = 1701 (0.341 sec)
    INFO:tensorflow:global_step/sec: 293.646
    INFO:tensorflow:loss = 4335523000.0, step = 1801 (0.340 sec)
    INFO:tensorflow:global_step/sec: 295.529
    INFO:tensorflow:loss = 4100831000.0, step = 1901 (0.339 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 3701924900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:28
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-2000


    2026-03-24 19:23:28.425179: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.437597: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.619410: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:28.619424: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:28.630125: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.637693: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.646964: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.657816: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.669494: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.713992: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:28.729221: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.28877s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:28
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 227530460.0, global_step = 2000, label/mean = 13207.129, loss = 3517971000.0, prediction/mean = 352.43335
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-2000
    scores_minmax {'average_loss': 227530460.0, 'label/mean': 13207.129, 'loss': 3517971000.0, 'prediction/mean': 352.43335, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:28.842651: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.013204: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:29.013221: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:29.020025: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.026679: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.033345: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.036313: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.043427: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.047516: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...


    2026-03-24 19:23:29.431107: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:29.542511: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 5743795000.0, step = 2001


    2026-03-24 19:23:29.635083: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 185.4
    INFO:tensorflow:loss = 3484483800.0, step = 2101 (0.540 sec)
    INFO:tensorflow:global_step/sec: 265.835
    INFO:tensorflow:loss = 1569616600.0, step = 2201 (0.376 sec)
    INFO:tensorflow:global_step/sec: 288.149
    INFO:tensorflow:loss = 2619928300.0, step = 2301 (0.347 sec)
    INFO:tensorflow:global_step/sec: 270.284
    INFO:tensorflow:loss = 1843820800.0, step = 2401 (0.370 sec)
    INFO:tensorflow:global_step/sec: 232.61
    INFO:tensorflow:loss = 2431519500.0, step = 2501 (0.430 sec)
    INFO:tensorflow:global_step/sec: 241.221
    INFO:tensorflow:loss = 2719114200.0, step = 2601 (0.415 sec)
    INFO:tensorflow:global_step/sec: 256.087
    INFO:tensorflow:loss = 4086583300.0, step = 2701 (0.390 sec)
    INFO:tensorflow:global_step/sec: 286.651
    INFO:tensorflow:loss = 3087568400.0, step = 2801 (0.349 sec)
    INFO:tensorflow:global_step/sec: 226.717
    INFO:tensorflow:loss = 3896713700.0, step = 2901 (0.441 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 1380517400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:34
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:23:33.870788: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:33.877932: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.047398: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:34.047415: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:34.054016: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.059435: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.065280: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:34.072808: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.083674: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.088019: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.122685: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.243138: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.25425s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:34
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 222870460.0, global_step = 3000, label/mean = 13207.129, loss = 3445920300.0, prediction/mean = 524.51697
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-3000
    scores_minmax {'average_loss': 222870460.0, 'label/mean': 13207.129, 'loss': 3445920300.0, 'prediction/mean': 524.51697, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:34.414971: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:34.414986: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:34.420710: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.426815: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.434162: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.437322: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.443957: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:34.447932: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.


    2026-03-24 19:23:34.723136: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 4288328200.0, step = 3001


    2026-03-24 19:23:34.967302: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:35.086088: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 165.245
    INFO:tensorflow:loss = 2536829400.0, step = 3101 (0.606 sec)
    INFO:tensorflow:global_step/sec: 199.515
    INFO:tensorflow:loss = 4032559000.0, step = 3201 (0.501 sec)
    INFO:tensorflow:global_step/sec: 234.942
    INFO:tensorflow:loss = 1687240800.0, step = 3301 (0.425 sec)
    INFO:tensorflow:global_step/sec: 294.903
    INFO:tensorflow:loss = 1803423400.0, step = 3401 (0.339 sec)
    INFO:tensorflow:global_step/sec: 294.969
    INFO:tensorflow:loss = 4277240000.0, step = 3501 (0.339 sec)
    INFO:tensorflow:global_step/sec: 296.709
    INFO:tensorflow:loss = 3382985200.0, step = 3601 (0.337 sec)
    INFO:tensorflow:global_step/sec: 295.854
    INFO:tensorflow:loss = 3309995500.0, step = 3701 (0.338 sec)
    INFO:tensorflow:global_step/sec: 297.825
    INFO:tensorflow:loss = 3015987000.0, step = 3801 (0.336 sec)
    INFO:tensorflow:global_step/sec: 299.19
    INFO:tensorflow:loss = 4658426000.0, step = 3901 (0.334 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 3852405800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:23:39.074209: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.081006: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.247168: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:39.247183: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:39.258087: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.264755: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.273054: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:39.279803: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.289769: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.295143: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.334456: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.462144: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.27219s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:39
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 218313600.0, global_step = 4000, label/mean = 13207.129, loss = 3375464200.0, prediction/mean = 694.99744
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-4000
    scores_minmax {'average_loss': 218313600.0, 'label/mean': 13207.129, 'loss': 3375464200.0, 'prediction/mean': 694.99744, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:39.641855: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:39.641869: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:39.647727: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.653813: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.661148: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.664110: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.670859: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:39.675165: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...


    2026-03-24 19:23:40.094336: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:40.292633: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3620953600.0, step = 4001


    2026-03-24 19:23:40.392402: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 249.835
    INFO:tensorflow:loss = 4083547600.0, step = 4101 (0.400 sec)
    INFO:tensorflow:global_step/sec: 228.516
    INFO:tensorflow:loss = 3253644300.0, step = 4201 (0.439 sec)
    INFO:tensorflow:global_step/sec: 172.933
    INFO:tensorflow:loss = 3160359400.0, step = 4301 (0.579 sec)
    INFO:tensorflow:global_step/sec: 286.999
    INFO:tensorflow:loss = 3242220800.0, step = 4401 (0.346 sec)
    INFO:tensorflow:global_step/sec: 225.73
    INFO:tensorflow:loss = 2234396200.0, step = 4501 (0.443 sec)
    INFO:tensorflow:global_step/sec: 288.85
    INFO:tensorflow:loss = 2449406700.0, step = 4601 (0.346 sec)
    INFO:tensorflow:global_step/sec: 287.48
    INFO:tensorflow:loss = 3041886200.0, step = 4701 (0.348 sec)
    INFO:tensorflow:global_step/sec: 280.638
    INFO:tensorflow:loss = 1912577000.0, step = 4801 (0.356 sec)
    INFO:tensorflow:global_step/sec: 288.337
    INFO:tensorflow:loss = 4999368700.0, step = 4901 (0.347 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 2817235200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:44
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-5000


    2026-03-24 19:23:44.610975: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.617774: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.800348: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:44.800363: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:44.807744: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:44.813402: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.820353: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.827813: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.837270: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.868949: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:44.879117: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.001881: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26483s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:45
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 213847760.0, global_step = 5000, label/mean = 13207.129, loss = 3306415400.0, prediction/mean = 864.2611
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-5000
    scores_minmax {'average_loss': 213847760.0, 'label/mean': 13207.129, 'loss': 3306415400.0, 'prediction/mean': 864.2611, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:45.185585: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:45.185600: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:45.191593: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.197967: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.203836: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.206639: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.214013: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.218625: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...


    2026-03-24 19:23:45.653762: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:45.765677: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3094915300.0, step = 5001


    2026-03-24 19:23:45.861452: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 220.924
    INFO:tensorflow:loss = 6758137300.0, step = 5101 (0.453 sec)
    INFO:tensorflow:global_step/sec: 291.163
    INFO:tensorflow:loss = 4424719000.0, step = 5201 (0.343 sec)
    INFO:tensorflow:global_step/sec: 282.451
    INFO:tensorflow:loss = 4470210000.0, step = 5301 (0.354 sec)
    INFO:tensorflow:global_step/sec: 199.196
    INFO:tensorflow:loss = 2122934300.0, step = 5401 (0.505 sec)
    INFO:tensorflow:global_step/sec: 200.898
    INFO:tensorflow:loss = 3665750500.0, step = 5501 (0.495 sec)
    INFO:tensorflow:global_step/sec: 203.215
    INFO:tensorflow:loss = 5489412000.0, step = 5601 (0.492 sec)
    INFO:tensorflow:global_step/sec: 203.69
    INFO:tensorflow:loss = 3166592000.0, step = 5701 (0.491 sec)
    INFO:tensorflow:global_step/sec: 207.733
    INFO:tensorflow:loss = 4319330300.0, step = 5801 (0.481 sec)
    INFO:tensorflow:global_step/sec: 202.634
    INFO:tensorflow:loss = 2666020900.0, step = 5901 (0.493 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 3094835700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:50


    2026-03-24 19:23:50.592077: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.599473: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:50.893472: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:50.893486: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:50.901047: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.907137: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.914052: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.921824: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.930451: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.936023: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:50.973120: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.43767s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:51
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 209481650.0, global_step = 6000, label/mean = 13207.129, loss = 3238908400.0, prediction/mean = 1031.9263
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-6000
    scores_minmax {'average_loss': 209481650.0, 'label/mean': 13207.129, 'loss': 3238908400.0, 'prediction/mean': 1031.9263, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-6000


    2026-03-24 19:23:51.147655: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:51.334124: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:51.334139: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:51.340822: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:51.347959: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:51.353941: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:51.358278: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:51.367879: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:51.371737: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.


    2026-03-24 19:23:51.655070: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 1779591700.0, step = 6001


    2026-03-24 19:23:51.925071: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:52.044368: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 144.744
    INFO:tensorflow:loss = 5974015500.0, step = 6101 (0.693 sec)
    INFO:tensorflow:global_step/sec: 160.962
    INFO:tensorflow:loss = 1249763600.0, step = 6201 (0.620 sec)
    INFO:tensorflow:global_step/sec: 252.707
    INFO:tensorflow:loss = 2097605000.0, step = 6301 (0.396 sec)
    INFO:tensorflow:global_step/sec: 183.553
    INFO:tensorflow:loss = 2735048400.0, step = 6401 (0.548 sec)
    INFO:tensorflow:global_step/sec: 205.579
    INFO:tensorflow:loss = 1640607900.0, step = 6501 (0.484 sec)
    INFO:tensorflow:global_step/sec: 249.936
    INFO:tensorflow:loss = 2191155500.0, step = 6601 (0.401 sec)
    INFO:tensorflow:global_step/sec: 238.633
    INFO:tensorflow:loss = 3110732800.0, step = 6701 (0.419 sec)
    INFO:tensorflow:global_step/sec: 250.325
    INFO:tensorflow:loss = 3453934600.0, step = 6801 (0.399 sec)
    INFO:tensorflow:global_step/sec: 261.196
    INFO:tensorflow:loss = 1476959400.0, step = 6901 (0.383 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 3185977900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.


    2026-03-24 19:23:56.855831: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:56.886762: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Starting evaluation at 2026-03-24T19:23:57
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:57.098628: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:57.098647: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:57.105893: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.111136: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.118202: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.124764: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.132692: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.136775: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.170086: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.28202s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:23:57
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 205193260.0, global_step = 7000, label/mean = 13207.129, loss = 3172603400.0, prediction/mean = 1198.7794
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-7000
    scores_minmax {'average_loss': 205193260.0, 'label/mean': 13207.129, 'loss': 3172603400.0, 'prediction/mean': 1198.7794, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:23:57.307450: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.491223: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:23:57.491237: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:23:57.497249: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.503297: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:23:57.510047: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.512875: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.519363: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:57.523900: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...


    2026-03-24 19:23:57.932752: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:23:58.044166: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 3600454700.0, step = 7001


    2026-03-24 19:23:58.137513: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 245.822
    INFO:tensorflow:loss = 3624924200.0, step = 7101 (0.407 sec)
    INFO:tensorflow:global_step/sec: 273.303
    INFO:tensorflow:loss = 2951922200.0, step = 7201 (0.366 sec)
    INFO:tensorflow:global_step/sec: 280.183
    INFO:tensorflow:loss = 2424380400.0, step = 7301 (0.357 sec)
    INFO:tensorflow:global_step/sec: 285.322
    INFO:tensorflow:loss = 4862558000.0, step = 7401 (0.351 sec)
    INFO:tensorflow:global_step/sec: 286.89
    INFO:tensorflow:loss = 4278317600.0, step = 7501 (0.349 sec)
    INFO:tensorflow:global_step/sec: 287.087
    INFO:tensorflow:loss = 5091986400.0, step = 7601 (0.348 sec)
    INFO:tensorflow:global_step/sec: 289.3
    INFO:tensorflow:loss = 2236421600.0, step = 7701 (0.346 sec)
    INFO:tensorflow:global_step/sec: 289.11
    INFO:tensorflow:loss = 2503281700.0, step = 7801 (0.346 sec)
    INFO:tensorflow:global_step/sec: 230.549
    INFO:tensorflow:loss = 5396820000.0, step = 7901 (0.434 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 3576304400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:24:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.


    2026-03-24 19:24:01.991688: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:01.997979: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.169320: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:24:02.169338: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:24:02.176080: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.181145: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.187383: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:24:02.194398: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.203263: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.207598: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.241444: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.364352: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.26031s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:24:02
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 201007150.0, global_step = 8000, label/mean = 13207.129, loss = 3107879700.0, prediction/mean = 1363.8331
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-8000
    scores_minmax {'average_loss': 201007150.0, 'label/mean': 13207.129, 'loss': 3107879700.0, 'prediction/mean': 1363.8331, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:24:02.532460: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:24:02.532476: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:24:02.538490: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.544489: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.551167: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.554021: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.560311: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:02.564261: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...


    2026-03-24 19:24:02.956111: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:03.065497: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:loss = 2595307500.0, step = 8001


    2026-03-24 19:24:03.159915: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 237.605
    INFO:tensorflow:loss = 2832776000.0, step = 8101 (0.422 sec)
    INFO:tensorflow:global_step/sec: 267.878
    INFO:tensorflow:loss = 3315480600.0, step = 8201 (0.372 sec)
    INFO:tensorflow:global_step/sec: 274.649
    INFO:tensorflow:loss = 3051352000.0, step = 8301 (0.364 sec)
    INFO:tensorflow:global_step/sec: 283.555
    INFO:tensorflow:loss = 1656426900.0, step = 8401 (0.353 sec)
    INFO:tensorflow:global_step/sec: 278.397
    INFO:tensorflow:loss = 1765827200.0, step = 8501 (0.361 sec)
    INFO:tensorflow:global_step/sec: 281.078
    INFO:tensorflow:loss = 2158169600.0, step = 8601 (0.354 sec)
    INFO:tensorflow:global_step/sec: 273.73
    INFO:tensorflow:loss = 4217526500.0, step = 8701 (0.365 sec)
    INFO:tensorflow:global_step/sec: 290.716
    INFO:tensorflow:loss = 1902677600.0, step = 8801 (0.344 sec)
    INFO:tensorflow:global_step/sec: 273.299
    INFO:tensorflow:loss = 3827160000.0, step = 8901 (0.366 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 1676418800.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-03-24T19:24:07
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:24:06.911043: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:06.917593: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.081404: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:24:07.081419: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:24:07.087562: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.092835: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.099279: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.105330: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.24656s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:24:07
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 196899170.0, global_step = 9000, label/mean = 13207.129, loss = 3044364000.0, prediction/mean = 1527.954
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-9000


    2026-03-24 19:24:07.113581: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.117984: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.156278: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.272597: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    scores_minmax {'average_loss': 196899170.0, 'label/mean': 13207.129, 'loss': 3044364000.0, 'prediction/mean': 1527.954, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:24:07.445683: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:24:07.445700: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:24:07.451601: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.457725: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.464108: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.467527: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.473959: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:07.477776: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.


    2026-03-24 19:24:07.865329: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 1556693200.0, step = 9001


    2026-03-24 19:24:08.107760: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:08.204305: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:global_step/sec: 238.442
    INFO:tensorflow:loss = 1777701600.0, step = 9101 (0.420 sec)
    INFO:tensorflow:global_step/sec: 228.878
    INFO:tensorflow:loss = 2864099600.0, step = 9201 (0.441 sec)
    INFO:tensorflow:global_step/sec: 162.543
    INFO:tensorflow:loss = 1175585700.0, step = 9301 (0.611 sec)
    INFO:tensorflow:global_step/sec: 175.477
    INFO:tensorflow:loss = 3418104300.0, step = 9401 (0.570 sec)
    INFO:tensorflow:global_step/sec: 199.792
    INFO:tensorflow:loss = 4219117000.0, step = 9501 (0.503 sec)
    INFO:tensorflow:global_step/sec: 198.11
    INFO:tensorflow:loss = 5389369300.0, step = 9601 (0.502 sec)
    INFO:tensorflow:global_step/sec: 198.978
    INFO:tensorflow:loss = 5002651600.0, step = 9701 (0.506 sec)
    INFO:tensorflow:global_step/sec: 206.299
    INFO:tensorflow:loss = 3129825800.0, step = 9801 (0.484 sec)
    INFO:tensorflow:global_step/sec: 204.13
    INFO:tensorflow:loss = 3351028700.0, step = 9901 (0.487 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 3127799300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.


    2026-03-24 19:24:13.342157: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.370767: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Starting evaluation at 2026-03-24T19:24:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.


    2026-03-24 19:24:13.579733: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:306] Could not identify NUMA node of platform GPU ID 0, defaulting to 0. Your kernel may not have been built with NUMA support.
    2026-03-24 19:24:13.579748: I tensorflow/core/common_runtime/pluggable_device/pluggable_device_factory.cc:272] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 0 MB memory) -> physical PluggableDevice (device: 0, name: METAL, pci bus id: <undefined>)
    2026-03-24 19:24:13.587322: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.593484: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.600039: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.606675: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.616079: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.647136: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.
    2026-03-24 19:24:13.658210: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.


    INFO:tensorflow:Inference Time : 0.34809s
    INFO:tensorflow:Finished evaluation at 2026-03-24-19:24:13
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 192884350.0, global_step = 10000, label/mean = 13207.129, loss = 2982289000.0, prediction/mean = 1690.5135
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0eiyau27/model.ckpt-10000
    scores_minmax {'average_loss': 192884350.0, 'label/mean': 13207.129, 'loss': 2982289000.0, 'prediction/mean': 1690.5135, 'global_step': 10000}


    2026-03-24 19:24:13.853638: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:114] Plugin optimizer for device_type GPU is enabled.



```python
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
---------------------------------------------------------------------------
NanLossDuringTrainingError                Traceback (most recent call last)
Cell In[16], line 9
      7 num_training_steps = 10000                                                    
      8 for _ in range(num_print_statements):
----> 9     est_gd.train(train_input_fn, steps=num_training_steps // num_print_statements)                                                         
     10     scores_gd = est_gd.evaluate(eval_input_fn)
     11     print('scores_gd', scores_gd)

File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:360, in Estimator.train(self, input_fn, hooks, steps, max_steps, saving_listeners)
    357 hooks.extend(self._convert_train_steps_to_hooks(steps, max_steps))
    359 saving_listeners = _check_listeners_type(saving_listeners)
--> 360 loss = self._train_model(input_fn, hooks, saving_listeners)
    361 logging.info('Loss for final step: %s.', loss)
    362 return self

File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:1186, in Estimator._train_model(self, input_fn, hooks, saving_listeners)
   1184   return self._train_model_distributed(input_fn, hooks, saving_listeners)
   1185 else:
-> 1186   return self._train_model_default(input_fn, hooks, saving_listeners)

File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:1217, in Estimator._train_model_default(self, input_fn, hooks, saving_listeners)
   1214 estimator_spec = self._call_model_fn(features, labels, ModeKeys.TRAIN,
   1215                                      self.config)
   1216 global_step_tensor = tf.compat.v1.train.get_global_step(g)
...
--> 785   raise NanLossDuringTrainingError
    786 else:
    787   logging.warning(failure_message)

NanLossDuringTrainingError: NaN loss during training.
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
'''
```

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



    ---------------------------------------------------------------------------

    NanLossDuringTrainingError                Traceback (most recent call last)

    Cell In[16], line 9
          7 num_training_steps = 10000                                                    
          8 for _ in range(num_print_statements):
    ----> 9     est_gd.train(train_input_fn, steps=num_training_steps // num_print_statements)                                                         
         10     scores_gd = est_gd.evaluate(eval_input_fn)
         11     print('scores_gd', scores_gd)


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:360, in Estimator.train(self, input_fn, hooks, steps, max_steps, saving_listeners)
        357 hooks.extend(self._convert_train_steps_to_hooks(steps, max_steps))
        359 saving_listeners = _check_listeners_type(saving_listeners)
    --> 360 loss = self._train_model(input_fn, hooks, saving_listeners)
        361 logging.info('Loss for final step: %s.', loss)
        362 return self


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:1186, in Estimator._train_model(self, input_fn, hooks, saving_listeners)
       1184   return self._train_model_distributed(input_fn, hooks, saving_listeners)
       1185 else:
    -> 1186   return self._train_model_default(input_fn, hooks, saving_listeners)


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:1217, in Estimator._train_model_default(self, input_fn, hooks, saving_listeners)
       1214 estimator_spec = self._call_model_fn(features, labels, ModeKeys.TRAIN,
       1215                                      self.config)
       1216 global_step_tensor = tf.compat.v1.train.get_global_step(g)
    -> 1217 return self._train_with_estimator_spec(estimator_spec, worker_hooks,
       1218                                        hooks, global_step_tensor,
       1219                                        saving_listeners)


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow_estimator/python/estimator/estimator.py:1533, in Estimator._train_with_estimator_spec(self, estimator_spec, worker_hooks, hooks, global_step_tensor, saving_listeners)
       1530   # just as keras(https://github.com/tensorflow/tensorflow/blob/v2.4.1/tensorflow/python/keras/engine/training.py#L1093),
       1531   # trace should be enabled for every step
       1532   with trace.Trace('train', step_num=current_step, _r=1):
    -> 1533     _, loss = mon_sess.run([estimator_spec.train_op, estimator_spec.loss])
       1534 if current_step == 0:
       1535   tf.compat.v1.logging.warn('Training with estimator made no steps. '
       1536                             'Perhaps input is empty or misspecified.')


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:778, in _MonitoredSession.run(self, fetches, feed_dict, options, run_metadata)
        764 def run(self, fetches, feed_dict=None, options=None, run_metadata=None):
        765   """Run ops in the monitored session.
        766 
        767   This method is completely compatible with the `tf.Session.run()` method.
       (...)
        776     Same as `tf.Session.run()`.
        777   """
    --> 778   return self._sess.run(
        779       fetches,
        780       feed_dict=feed_dict,
        781       options=options,
        782       run_metadata=run_metadata)


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:1307, in _RecoverableSession.run(self, fetches, feed_dict, options, run_metadata)
       1305   if not self._sess:
       1306     self._sess = self._create_session()
    -> 1307   return self._sess.run(
       1308       fetches,
       1309       feed_dict=feed_dict,
       1310       options=options,
       1311       run_metadata=run_metadata)
       1312 except _PREEMPTION_ERRORS as e:
       1313   logging.info(
       1314       'An error was raised. This may be due to a preemption in '
       1315       'a connected worker or parameter server. The current '
       (...)
       1320       'increasing the number of parameter servers assigned to '
       1321       'the job. Error: %s', e)


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:1397, in _CoordinatedSession.run(self, *args, **kwargs)
       1395 def run(self, *args, **kwargs):
       1396   try:
    -> 1397     return self._sess.run(*args, **kwargs)
       1398   except _PREEMPTION_ERRORS:
       1399     raise


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/monitored_session.py:1472, in _HookedSession.run(self, fetches, feed_dict, options, run_metadata)
       1464 outputs = _WrappedSession.run(
       1465     self,
       1466     fetches=actual_fetches,
       1467     feed_dict=feed_dict,
       1468     options=options,
       1469     run_metadata=run_metadata)
       1471 for hook in self._hooks:
    -> 1472   hook.after_run(
       1473       run_context,
       1474       session_run_hook.SessionRunValues(
       1475           results=outputs[hook] if hook in outputs else None,
       1476           options=options,
       1477           run_metadata=run_metadata))
       1478 self._should_stop = self._should_stop or run_context.stop_requested
       1480 return outputs['caller']


    File /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/basic_session_run_hooks.py:785, in NanTensorHook.after_run(self, run_context, run_values)
        783 if self._fail_on_nan_loss:
        784   logging.error(failure_message)
    --> 785   raise NanLossDuringTrainingError
        786 else:
        787   logging.warning(failure_message)


    NanLossDuringTrainingError: NaN loss during training.


### Task 3: Make your best model using only categorical features

- Look at the possible feature columns for categorical features. They begin with `categorical_column_with_` in go/tf-ops.
- You may find `dataframe[categorical_feature_names].unique()` helpful.



```python
## Your code goes here
car_data[categorical_feature_names].unique()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/ipykernel_62111/2079637233.py in ?()
          1 ## Your code goes here
    ----> 2 car_data[categorical_feature_names].unique()
    

    /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/pandas/core/generic.py in ?(self, name)
       6317             and name not in self._accessors
       6318             and self._info_axis._can_hold_identifiers_and_holds_name(name)
       6319         ):
       6320             return self[name]
    -> 6321         return object.__getattribute__(self, name)
    

    AttributeError: 'DataFrame' object has no attribute 'unique'



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
