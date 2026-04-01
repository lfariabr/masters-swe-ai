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
      <th>109</th>
      <td>0</td>
      <td>?</td>
      <td>peugot</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>wagon</td>
      <td>rwd</td>
      <td>front</td>
      <td>114.20</td>
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
      <td>12440</td>
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
    <tr>
      <th>195</th>
      <td>-1</td>
      <td>74</td>
      <td>volvo</td>
      <td>gas</td>
      <td>std</td>
      <td>four</td>
      <td>wagon</td>
      <td>rwd</td>
      <td>front</td>
      <td>104.30</td>
      <td>...</td>
      <td>141</td>
      <td>mpfi</td>
      <td>3.78</td>
      <td>3.15</td>
      <td>9.50</td>
      <td>114</td>
      <td>5400</td>
      <td>23</td>
      <td>28</td>
      <td>13415</td>
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
    Index: 205 entries, 183 to 101
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
      <th>31</th>
      <td>2</td>
      <td>137</td>
      <td>86.60</td>
      <td>144.60</td>
      <td>63.90</td>
      <td>50.80</td>
      <td>1819</td>
      <td>92</td>
      <td>76</td>
      <td>6000</td>
      <td>31</td>
      <td>38</td>
      <td>2.91</td>
      <td>3.41</td>
      <td>9.20</td>
    </tr>
    <tr>
      <th>99</th>
      <td>0</td>
      <td>106</td>
      <td>97.20</td>
      <td>173.40</td>
      <td>65.20</td>
      <td>54.70</td>
      <td>2324</td>
      <td>120</td>
      <td>97</td>
      <td>5200</td>
      <td>27</td>
      <td>34</td>
      <td>3.33</td>
      <td>3.47</td>
      <td>8.50</td>
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
      <th>109</th>
      <td>0</td>
      <td>?</td>
      <td>114.20</td>
      <td>198.90</td>
      <td>68.40</td>
      <td>58.70</td>
      <td>3230</td>
      <td>120</td>
      <td>97</td>
      <td>5000</td>
      <td>19</td>
      <td>24</td>
      <td>3.46</td>
      <td>3.19</td>
      <td>8.40</td>
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
      <th>202</th>
      <td>-1</td>
      <td>95</td>
      <td>109.10</td>
      <td>188.80</td>
      <td>68.90</td>
      <td>55.50</td>
      <td>3012</td>
      <td>173</td>
      <td>134</td>
      <td>5500</td>
      <td>18</td>
      <td>23</td>
      <td>3.58</td>
      <td>2.87</td>
      <td>8.80</td>
    </tr>
    <tr>
      <th>163</th>
      <td>1</td>
      <td>168</td>
      <td>94.50</td>
      <td>168.70</td>
      <td>64.00</td>
      <td>52.60</td>
      <td>2169</td>
      <td>98</td>
      <td>70</td>
      <td>4800</td>
      <td>29</td>
      <td>34</td>
      <td>3.19</td>
      <td>3.03</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>193</th>
      <td>0</td>
      <td>?</td>
      <td>100.40</td>
      <td>183.10</td>
      <td>66.90</td>
      <td>55.10</td>
      <td>2563</td>
      <td>109</td>
      <td>88</td>
      <td>5500</td>
      <td>25</td>
      <td>31</td>
      <td>3.19</td>
      <td>3.40</td>
      <td>9.00</td>
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
      <th>101</th>
      <td>0</td>
      <td>128</td>
      <td>100.40</td>
      <td>181.70</td>
      <td>66.50</td>
      <td>55.10</td>
      <td>3095</td>
      <td>181</td>
      <td>152</td>
      <td>5200</td>
      <td>17</td>
      <td>22</td>
      <td>3.43</td>
      <td>3.27</td>
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
      <th>fuel-system</th>
      <th>num-doors</th>
      <th>aspiration</th>
      <th>fuel-type</th>
      <th>drive-wheels</th>
      <th>body-style</th>
      <th>engine-type</th>
      <th>num-cylinders</th>
      <th>engine-location</th>
      <th>make</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>183</th>
      <td>mpfi</td>
      <td>two</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>volkswagen</td>
    </tr>
    <tr>
      <th>31</th>
      <td>1bbl</td>
      <td>two</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>honda</td>
    </tr>
    <tr>
      <th>99</th>
      <td>2bbl</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>nissan</td>
    </tr>
    <tr>
      <th>77</th>
      <td>2bbl</td>
      <td>two</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>hatchback</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>mitsubishi</td>
    </tr>
    <tr>
      <th>109</th>
      <td>mpfi</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>rwd</td>
      <td>wagon</td>
      <td>l</td>
      <td>four</td>
      <td>front</td>
      <td>peugot</td>
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
      <th>202</th>
      <td>mpfi</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>rwd</td>
      <td>sedan</td>
      <td>ohcv</td>
      <td>six</td>
      <td>front</td>
      <td>volvo</td>
    </tr>
    <tr>
      <th>163</th>
      <td>2bbl</td>
      <td>two</td>
      <td>std</td>
      <td>gas</td>
      <td>rwd</td>
      <td>sedan</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>toyota</td>
    </tr>
    <tr>
      <th>193</th>
      <td>mpfi</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>wagon</td>
      <td>ohc</td>
      <td>four</td>
      <td>front</td>
      <td>volkswagen</td>
    </tr>
    <tr>
      <th>146</th>
      <td>2bbl</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>wagon</td>
      <td>ohcf</td>
      <td>four</td>
      <td>front</td>
      <td>subaru</td>
    </tr>
    <tr>
      <th>101</th>
      <td>mpfi</td>
      <td>four</td>
      <td>std</td>
      <td>gas</td>
      <td>fwd</td>
      <td>sedan</td>
      <td>ohcv</td>
      <td>six</td>
      <td>front</td>
      <td>nissan</td>
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
    
    WARNING:tensorflow:From /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/ipykernel_44079/741504662.py:29: The name tf.estimator.inputs.pandas_input_fn is deprecated. Please use tf.compat.v1.estimator.inputs.pandas_input_fn instead.
    
    model_feature_columns [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=None)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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


    2026-04-01 13:23:00.891017: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
    2026-04-01 13:23:00.896427: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz


    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 3885835000.0, step = 1
    INFO:tensorflow:global_step/sec: 819.53
    INFO:tensorflow:loss = 1143798100.0, step = 101 (0.124 sec)
    INFO:tensorflow:global_step/sec: 1751.96
    INFO:tensorflow:loss = 1501741800.0, step = 201 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1829.86
    INFO:tensorflow:loss = 1129293800.0, step = 301 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2068.82
    INFO:tensorflow:loss = 1499851800.0, step = 401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2096.69
    INFO:tensorflow:loss = 584564160.0, step = 501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1755.68
    INFO:tensorflow:loss = 556243200.0, step = 601 (0.057 sec)
    INFO:tensorflow:global_step/sec: 1732.23
    INFO:tensorflow:loss = 1072797950.0, step = 701 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1746.72
    INFO:tensorflow:loss = 354733540.0, step = 801 (0.058 sec)
    INFO:tensorflow:global_step/sec: 1488.87
    INFO:tensorflow:loss = 1192780300.0, step = 901 (0.067 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 725806100.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12160s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:02
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 38075496.0, global_step = 1000, label/mean = 13207.129, loss = 588705700.0, prediction/mean = 13524.03
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-1000
    scores {'average_loss': 38075496.0, 'label/mean': 13207.129, 'loss': 588705700.0, 'prediction/mean': 13524.03, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-1000
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1173: get_checkpoint_mtimes (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file utilities to get mtimes.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 478316160.0, step = 1001
    INFO:tensorflow:global_step/sec: 1199.8
    INFO:tensorflow:loss = 179050430.0, step = 1101 (0.084 sec)
    INFO:tensorflow:global_step/sec: 865.876
    INFO:tensorflow:loss = 264254540.0, step = 1201 (0.116 sec)
    INFO:tensorflow:global_step/sec: 1379.71
    INFO:tensorflow:loss = 400856580.0, step = 1301 (0.074 sec)
    INFO:tensorflow:global_step/sec: 1260.83
    INFO:tensorflow:loss = 354506100.0, step = 1401 (0.079 sec)
    INFO:tensorflow:global_step/sec: 1236.26
    INFO:tensorflow:loss = 136109420.0, step = 1501 (0.081 sec)
    INFO:tensorflow:global_step/sec: 1140.34
    INFO:tensorflow:loss = 124282370.0, step = 1601 (0.088 sec)
    INFO:tensorflow:global_step/sec: 1339.17
    INFO:tensorflow:loss = 563144800.0, step = 1701 (0.073 sec)
    INFO:tensorflow:global_step/sec: 1986.32
    INFO:tensorflow:loss = 829425660.0, step = 1801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2225.11
    INFO:tensorflow:loss = 458895170.0, step = 1901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 157893120.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:04
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09857s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:04
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 29043730.0, global_step = 2000, label/mean = 13207.129, loss = 449060740.0, prediction/mean = 13494.51
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-2000
    scores {'average_loss': 29043730.0, 'label/mean': 13207.129, 'loss': 449060740.0, 'prediction/mean': 13494.51, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 275169020.0, step = 2001
    INFO:tensorflow:global_step/sec: 1591.29
    INFO:tensorflow:loss = 262362940.0, step = 2101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2354.33
    INFO:tensorflow:loss = 253668000.0, step = 2201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2243.81
    INFO:tensorflow:loss = 119933840.0, step = 2301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2273.05
    INFO:tensorflow:loss = 285805000.0, step = 2401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2229.9
    INFO:tensorflow:loss = 365405250.0, step = 2501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2102.66
    INFO:tensorflow:loss = 450121400.0, step = 2601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2445.87
    INFO:tensorflow:loss = 398586050.0, step = 2701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2333.72
    INFO:tensorflow:loss = 187154690.0, step = 2801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2232.94
    INFO:tensorflow:loss = 583096300.0, step = 2901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 497730980.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:05
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09475s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:06
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 24343046.0, global_step = 3000, label/mean = 13207.129, loss = 376380930.0, prediction/mean = 13399.774
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-3000
    scores {'average_loss': 24343046.0, 'label/mean': 13207.129, 'loss': 376380930.0, 'prediction/mean': 13399.774, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 272208580.0, step = 3001
    INFO:tensorflow:global_step/sec: 1688.34
    INFO:tensorflow:loss = 747832600.0, step = 3101 (0.061 sec)
    INFO:tensorflow:global_step/sec: 2200.79
    INFO:tensorflow:loss = 153971970.0, step = 3201 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2332.05
    INFO:tensorflow:loss = 776122500.0, step = 3301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2239.69
    INFO:tensorflow:loss = 142076220.0, step = 3401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2180.46
    INFO:tensorflow:loss = 927377340.0, step = 3501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2273.91
    INFO:tensorflow:loss = 328134100.0, step = 3601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2326.23
    INFO:tensorflow:loss = 272141400.0, step = 3701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2261.95
    INFO:tensorflow:loss = 136560270.0, step = 3801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2370.72
    INFO:tensorflow:loss = 206087470.0, step = 3901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 146029860.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:07
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09246s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:07
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 22011448.0, global_step = 4000, label/mean = 13207.129, loss = 340330850.0, prediction/mean = 13288.352
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-4000
    scores {'average_loss': 22011448.0, 'label/mean': 13207.129, 'loss': 340330850.0, 'prediction/mean': 13288.352, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 72139970.0, step = 4001
    INFO:tensorflow:global_step/sec: 1504.35
    INFO:tensorflow:loss = 923327300.0, step = 4101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2400.67
    INFO:tensorflow:loss = 96992810.0, step = 4201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2299.55
    INFO:tensorflow:loss = 566480500.0, step = 4301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2244.11
    INFO:tensorflow:loss = 65247100.0, step = 4401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2318.58
    INFO:tensorflow:loss = 405201820.0, step = 4501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2071.33
    INFO:tensorflow:loss = 537208200.0, step = 4601 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2328.23
    INFO:tensorflow:loss = 174278260.0, step = 4701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2318.9
    INFO:tensorflow:loss = 215895260.0, step = 4801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2262.34
    INFO:tensorflow:loss = 73575470.0, step = 4901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    WARNING:tensorflow:From /opt/anaconda3/envs/py310_env/lib/python3.10/site-packages/tensorflow/python/training/saver.py:1064: remove_checkpoint (from tensorflow.python.checkpoint.checkpoint_management) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use standard file APIs to delete files with this prefix.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 151839420.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:08
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09296s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:08
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 20849308.0, global_step = 5000, label/mean = 13207.129, loss = 322362370.0, prediction/mean = 13279.468
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-5000
    scores {'average_loss': 20849308.0, 'label/mean': 13207.129, 'loss': 322362370.0, 'prediction/mean': 13279.468, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 799319200.0, step = 5001
    INFO:tensorflow:global_step/sec: 1562.45
    INFO:tensorflow:loss = 416251100.0, step = 5101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2066.84
    INFO:tensorflow:loss = 732295300.0, step = 5201 (0.048 sec)
    INFO:tensorflow:global_step/sec: 1935.77
    INFO:tensorflow:loss = 106798780.0, step = 5301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 1991.29
    INFO:tensorflow:loss = 161793170.0, step = 5401 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1866.37
    INFO:tensorflow:loss = 134408480.0, step = 5501 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2008.28
    INFO:tensorflow:loss = 638589800.0, step = 5601 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2278.57
    INFO:tensorflow:loss = 192108640.0, step = 5701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2114.79
    INFO:tensorflow:loss = 63535676.0, step = 5801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2034.8
    INFO:tensorflow:loss = 554605000.0, step = 5901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 124220300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:10
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10615s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:10
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 20216736.0, global_step = 6000, label/mean = 13207.129, loss = 312581860.0, prediction/mean = 13240.401
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-6000
    scores {'average_loss': 20216736.0, 'label/mean': 13207.129, 'loss': 312581860.0, 'prediction/mean': 13240.401, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 167391760.0, step = 6001
    INFO:tensorflow:global_step/sec: 1529.96
    INFO:tensorflow:loss = 759310200.0, step = 6101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2312.62
    INFO:tensorflow:loss = 138318660.0, step = 6201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2232.15
    INFO:tensorflow:loss = 476048670.0, step = 6301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1864.69
    INFO:tensorflow:loss = 1002156160.0, step = 6401 (0.053 sec)
    INFO:tensorflow:global_step/sec: 1654.26
    INFO:tensorflow:loss = 124484850.0, step = 6501 (0.061 sec)
    INFO:tensorflow:global_step/sec: 1762.84
    INFO:tensorflow:loss = 112647840.0, step = 6601 (0.056 sec)
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 6601 vs previous value: 6601. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    INFO:tensorflow:global_step/sec: 1796.88
    INFO:tensorflow:loss = 210125470.0, step = 6701 (0.055 sec)
    INFO:tensorflow:global_step/sec: 1758.06
    INFO:tensorflow:loss = 411197900.0, step = 6801 (0.056 sec)
    INFO:tensorflow:global_step/sec: 1894.58
    INFO:tensorflow:loss = 281294400.0, step = 6901 (0.053 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 370015460.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:12
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09512s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:12
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 19793346.0, global_step = 7000, label/mean = 13207.129, loss = 306035600.0, prediction/mean = 13380.607
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-7000
    scores {'average_loss': 19793346.0, 'label/mean': 13207.129, 'loss': 306035600.0, 'prediction/mean': 13380.607, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 321875100.0, step = 7001
    INFO:tensorflow:global_step/sec: 1516.23
    INFO:tensorflow:loss = 483923900.0, step = 7101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2314.49
    INFO:tensorflow:loss = 143231700.0, step = 7201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2201.57
    INFO:tensorflow:loss = 484216700.0, step = 7301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2251.3
    INFO:tensorflow:loss = 154017310.0, step = 7401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2195.19
    INFO:tensorflow:loss = 113470990.0, step = 7501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2116.95
    INFO:tensorflow:loss = 79243540.0, step = 7601 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2309.58
    INFO:tensorflow:loss = 616130560.0, step = 7701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2236.44
    INFO:tensorflow:loss = 83793650.0, step = 7801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2312.78
    INFO:tensorflow:loss = 651642200.0, step = 7901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 127675990.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:13
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08894s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:13
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 19526042.0, global_step = 8000, label/mean = 13207.129, loss = 301902660.0, prediction/mean = 13174.017
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-8000
    scores {'average_loss': 19526042.0, 'label/mean': 13207.129, 'loss': 301902660.0, 'prediction/mean': 13174.017, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 157730610.0, step = 8001
    INFO:tensorflow:global_step/sec: 1559.14
    INFO:tensorflow:loss = 862561400.0, step = 8101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2261.42
    INFO:tensorflow:loss = 642486800.0, step = 8201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2351.95
    INFO:tensorflow:loss = 189749570.0, step = 8301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2219.41
    INFO:tensorflow:loss = 220401220.0, step = 8401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2332.35
    INFO:tensorflow:loss = 486119550.0, step = 8501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2280.98
    INFO:tensorflow:loss = 445559500.0, step = 8601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2262.9
    INFO:tensorflow:loss = 552427200.0, step = 8701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2157.46
    INFO:tensorflow:loss = 342998530.0, step = 8801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1299.29
    INFO:tensorflow:loss = 288974000.0, step = 8901 (0.078 sec)
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 8901 vs previous value: 8901. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 182674600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:15
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09112s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:15
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 19219576.0, global_step = 9000, label/mean = 13207.129, loss = 297164220.0, prediction/mean = 13320.511
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-9000
    scores {'average_loss': 19219576.0, 'label/mean': 13207.129, 'loss': 297164220.0, 'prediction/mean': 13320.511, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 401267650.0, step = 9001
    INFO:tensorflow:global_step/sec: 1676.53
    INFO:tensorflow:loss = 110793820.0, step = 9101 (0.061 sec)
    INFO:tensorflow:global_step/sec: 2336.07
    INFO:tensorflow:loss = 655494140.0, step = 9201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2287.37
    INFO:tensorflow:loss = 120413810.0, step = 9301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2081.9
    INFO:tensorflow:loss = 577290940.0, step = 9401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2016.1
    INFO:tensorflow:loss = 335637570.0, step = 9501 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1992.82
    INFO:tensorflow:loss = 87814700.0, step = 9601 (0.050 sec)
    INFO:tensorflow:global_step/sec: 1965.48
    INFO:tensorflow:loss = 285650780.0, step = 9701 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2134.79
    INFO:tensorflow:loss = 431437000.0, step = 9801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1897.32
    INFO:tensorflow:loss = 466680400.0, step = 9901 (0.053 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 482921920.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:16
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11109s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:16
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 18981960.0, global_step = 10000, label/mean = 13207.129, loss = 293490300.0, prediction/mean = 13385.718
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-10000
    scores {'average_loss': 18981960.0, 'label/mean': 13207.129, 'loss': 293490300.0, 'prediction/mean': 13385.718, 'global_step': 10000}


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
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpvedsjn6r/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.



    
![png](car_data_ML_pipeline_files/car_data_ML_pipeline_16_1.png)
    


### Task 2: Take best numeric model from earlier. Add normalization.

#### Adding normalization to best numeric model from earlier

- Decide what type of normalization to add, and for which features
- Use the `normalizer_fn` arg on [`numeric_column`]
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

# Task 2.5 Standardization
# TODO: think about regressors.. how many are we using?
```

    model_feature_columns_zscore [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c6cda20>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c67e290>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c59fbe0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c57c4c0>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c558d30>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c5355a0>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c515e10>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10c4fa680>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8e50>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8af0>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9000>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8ee0>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8c10>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8ca0>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8f70>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
    graph_options {
      rewrite_options {
        meta_optimizer_iterations: ONE
      }
    }
    , '_keep_checkpoint_max': 5, '_keep_checkpoint_every_n_hours': 10000, '_log_step_count_steps': 100, '_train_distribute': None, '_device_fn': None, '_protocol': None, '_eval_distribute': None, '_experimental_distribute': None, '_experimental_max_worker_delay_secs': None, '_session_creation_timeout_secs': 7200, '_checkpoint_save_graph_def': True, '_service': None, '_cluster_spec': ClusterSpec({}), '_task_type': 'worker', '_task_id': 0, '_global_id_in_cluster': 0, '_master': '', '_evaluation_master': '', '_is_chief': True, '_num_ps_replicas': 0, '_num_worker_replicas': 1}
    model_feature_columns_minmax [NumericColumn(key='symboling', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8b80>), NumericColumn(key='normalized-losses', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf89d0>), NumericColumn(key='wheel-base', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8dc0>), NumericColumn(key='length', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9090>), NumericColumn(key='width', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9120>), NumericColumn(key='height', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf91b0>), NumericColumn(key='weight', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9240>), NumericColumn(key='engine-size', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8940>), NumericColumn(key='horsepower', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf8a60>), NumericColumn(key='peak-rpm', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf92d0>), NumericColumn(key='city-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9360>), NumericColumn(key='highway-mpg', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf93f0>), NumericColumn(key='bore', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9480>), NumericColumn(key='stroke', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf9510>), NumericColumn(key='compression-ratio', shape=(1,), default_value=None, dtype=tf.float32, normalizer_fn=<function <listcomp>.<lambda> at 0x10ccf95a0>)]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 3736645600.0, step = 1
    INFO:tensorflow:global_step/sec: 1507.16
    INFO:tensorflow:loss = 2914847700.0, step = 101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2308.56
    INFO:tensorflow:loss = 4105419000.0, step = 201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2147.31
    INFO:tensorflow:loss = 5143377400.0, step = 301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2354.09
    INFO:tensorflow:loss = 3314118000.0, step = 401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2299.07
    INFO:tensorflow:loss = 3067733000.0, step = 501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2255.15
    INFO:tensorflow:loss = 1854778100.0, step = 601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2284.68
    INFO:tensorflow:loss = 4485523500.0, step = 701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2310.69
    INFO:tensorflow:loss = 5365138400.0, step = 801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2274.95
    INFO:tensorflow:loss = 4123201300.0, step = 901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3962473700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:20
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09937s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:20
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 233017740.0, global_step = 1000, label/mean = 13207.129, loss = 3602813000.0, prediction/mean = 112.368935
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-1000
    scores_zscore {'average_loss': 233017740.0, 'label/mean': 13207.129, 'loss': 3602813000.0, 'prediction/mean': 112.368935, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 3645291800.0, step = 1001
    INFO:tensorflow:global_step/sec: 1394.23
    INFO:tensorflow:loss = 4375423000.0, step = 1101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2161.5
    INFO:tensorflow:loss = 4337558500.0, step = 1201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2337.49
    INFO:tensorflow:loss = 3778668500.0, step = 1301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2268.23
    INFO:tensorflow:loss = 5224184000.0, step = 1401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2317.13
    INFO:tensorflow:loss = 2840604000.0, step = 1501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2435.99
    INFO:tensorflow:loss = 3769899300.0, step = 1601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2284.47
    INFO:tensorflow:loss = 4752061400.0, step = 1701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2259.12
    INFO:tensorflow:loss = 1722978800.0, step = 1801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2140.05
    INFO:tensorflow:loss = 4974948400.0, step = 1901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 3613509000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11050s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:22
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 228414580.0, global_step = 2000, label/mean = 13207.129, loss = 3531640800.0, prediction/mean = 240.39438
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-2000
    scores_zscore {'average_loss': 228414580.0, 'label/mean': 13207.129, 'loss': 3531640800.0, 'prediction/mean': 240.39438, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 2769139200.0, step = 2001
    INFO:tensorflow:global_step/sec: 1343.76
    INFO:tensorflow:loss = 5504401400.0, step = 2101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2347.42
    INFO:tensorflow:loss = 2845118000.0, step = 2201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2169.45
    INFO:tensorflow:loss = 2970227000.0, step = 2301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2226.87
    INFO:tensorflow:loss = 2355455500.0, step = 2401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2363
    INFO:tensorflow:loss = 2643744800.0, step = 2501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2196.4
    INFO:tensorflow:loss = 2022740500.0, step = 2601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2322.99
    INFO:tensorflow:loss = 2762666000.0, step = 2701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2325.63
    INFO:tensorflow:loss = 3686574600.0, step = 2801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2198.34
    INFO:tensorflow:loss = 3194790000.0, step = 2901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 2975100400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:23
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09914s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:24
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 223792980.0, global_step = 3000, label/mean = 13207.129, loss = 3460183600.0, prediction/mean = 372.62466
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-3000
    scores_zscore {'average_loss': 223792980.0, 'label/mean': 13207.129, 'loss': 3460183600.0, 'prediction/mean': 372.62466, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 2146639500.0, step = 3001
    INFO:tensorflow:global_step/sec: 1483.82
    INFO:tensorflow:loss = 1921078800.0, step = 3101 (0.068 sec)
    INFO:tensorflow:global_step/sec: 2298.58
    INFO:tensorflow:loss = 5243973600.0, step = 3201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2276.88
    INFO:tensorflow:loss = 3603560400.0, step = 3301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2100.4
    INFO:tensorflow:loss = 4337103400.0, step = 3401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 1939.64
    INFO:tensorflow:loss = 5401293300.0, step = 3501 (0.051 sec)
    INFO:tensorflow:global_step/sec: 1940.76
    INFO:tensorflow:loss = 4076060400.0, step = 3601 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2216.42
    INFO:tensorflow:loss = 4951699500.0, step = 3701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2197.33
    INFO:tensorflow:loss = 2859347700.0, step = 3801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2265.35
    INFO:tensorflow:loss = 5816179700.0, step = 3901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 3166631000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:25
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09953s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:25
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 219254700.0, global_step = 4000, label/mean = 13207.129, loss = 3390015000.0, prediction/mean = 503.42017
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-4000
    scores_zscore {'average_loss': 219254700.0, 'label/mean': 13207.129, 'loss': 3390015000.0, 'prediction/mean': 503.42017, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 2791255000.0, step = 4001
    INFO:tensorflow:global_step/sec: 1106.89
    INFO:tensorflow:loss = 4176985900.0, step = 4101 (0.091 sec)
    INFO:tensorflow:global_step/sec: 1718.86
    INFO:tensorflow:loss = 3478637000.0, step = 4201 (0.059 sec)
    INFO:tensorflow:global_step/sec: 1751.5
    INFO:tensorflow:loss = 3008696300.0, step = 4301 (0.056 sec)
    INFO:tensorflow:global_step/sec: 2108.9
    INFO:tensorflow:loss = 4200434000.0, step = 4401 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2063.99
    INFO:tensorflow:loss = 6390350300.0, step = 4501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2239.73
    INFO:tensorflow:loss = 3080050400.0, step = 4601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2248
    INFO:tensorflow:loss = 3711047400.0, step = 4701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1993.54
    INFO:tensorflow:loss = 3032810000.0, step = 4801 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2049.9
    INFO:tensorflow:loss = 3169007000.0, step = 4901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 3984228900.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:27
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.12715s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:27
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 214792450.0, global_step = 5000, label/mean = 13207.129, loss = 3321021700.0, prediction/mean = 633.0871
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-5000
    scores_zscore {'average_loss': 214792450.0, 'label/mean': 13207.129, 'loss': 3321021700.0, 'prediction/mean': 633.0871, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 3468276200.0, step = 5001
    INFO:tensorflow:global_step/sec: 1436.26
    INFO:tensorflow:loss = 2785485800.0, step = 5101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2310.21
    INFO:tensorflow:loss = 2708610000.0, step = 5201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2329.26
    INFO:tensorflow:loss = 2165551000.0, step = 5301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2038.91
    INFO:tensorflow:loss = 2415681000.0, step = 5401 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1261.49
    INFO:tensorflow:loss = 2464331300.0, step = 5501 (0.081 sec)
    INFO:tensorflow:global_step/sec: 1519.39
    INFO:tensorflow:loss = 3570419000.0, step = 5601 (0.064 sec)
    INFO:tensorflow:global_step/sec: 2295.36
    INFO:tensorflow:loss = 2782646000.0, step = 5701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2140.01
    INFO:tensorflow:loss = 4093645600.0, step = 5801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1995.09
    INFO:tensorflow:loss = 2665553200.0, step = 5901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 2402160000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:29
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10797s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:29
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 210410200.0, global_step = 6000, label/mean = 13207.129, loss = 3253265700.0, prediction/mean = 761.6684
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-6000
    scores_zscore {'average_loss': 210410200.0, 'label/mean': 13207.129, 'loss': 3253265700.0, 'prediction/mean': 761.6684, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 1692129800.0, step = 6001
    INFO:tensorflow:global_step/sec: 1563.01
    INFO:tensorflow:loss = 2148994300.0, step = 6101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2386.92
    INFO:tensorflow:loss = 1985144600.0, step = 6201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2302.02
    INFO:tensorflow:loss = 2657899500.0, step = 6301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2399.42
    INFO:tensorflow:loss = 2724574700.0, step = 6401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2272.36
    INFO:tensorflow:loss = 3362461000.0, step = 6501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2257.14
    INFO:tensorflow:loss = 4915149300.0, step = 6601 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2336.61
    INFO:tensorflow:loss = 2032264100.0, step = 6701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2417.2
    INFO:tensorflow:loss = 4186199600.0, step = 6801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2106.28
    INFO:tensorflow:loss = 4312424000.0, step = 6901 (0.047 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 3117228300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:30
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09568s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:30
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 206094720.0, global_step = 7000, label/mean = 13207.129, loss = 3186541600.0, prediction/mean = 889.6801
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-7000
    scores_zscore {'average_loss': 206094720.0, 'label/mean': 13207.129, 'loss': 3186541600.0, 'prediction/mean': 889.6801, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 3195613700.0, step = 7001
    INFO:tensorflow:global_step/sec: 1442.56
    INFO:tensorflow:loss = 2880956000.0, step = 7101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2118.69
    INFO:tensorflow:loss = 2929414700.0, step = 7201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2178.46
    INFO:tensorflow:loss = 2128804100.0, step = 7301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2150.44
    INFO:tensorflow:loss = 3833934800.0, step = 7401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2245.99
    INFO:tensorflow:loss = 2819897600.0, step = 7501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1955.91
    INFO:tensorflow:loss = 3026925600.0, step = 7601 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2413.25
    INFO:tensorflow:loss = 5368183000.0, step = 7701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1366.04
    INFO:tensorflow:loss = 2377517000.0, step = 7801 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2058.63
    INFO:tensorflow:loss = 2858501600.0, step = 7901 (0.048 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 2209378300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:32
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09639s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:32
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 201860780.0, global_step = 8000, label/mean = 13207.129, loss = 3121078300.0, prediction/mean = 1016.73914
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-8000
    scores_zscore {'average_loss': 201860780.0, 'label/mean': 13207.129, 'loss': 3121078300.0, 'prediction/mean': 1016.73914, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 4369464000.0, step = 8001
    INFO:tensorflow:global_step/sec: 1353.2
    INFO:tensorflow:loss = 2047950500.0, step = 8101 (0.074 sec)
    INFO:tensorflow:global_step/sec: 2188.37
    INFO:tensorflow:loss = 3945629200.0, step = 8201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2353.94
    INFO:tensorflow:loss = 1820891600.0, step = 8301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 1898.32
    INFO:tensorflow:loss = 3470608400.0, step = 8401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2217.85
    INFO:tensorflow:loss = 1896636400.0, step = 8501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2261.25
    INFO:tensorflow:loss = 2219535400.0, step = 8601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2298.75
    INFO:tensorflow:loss = 1581093800.0, step = 8701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2200.28
    INFO:tensorflow:loss = 2467502600.0, step = 8801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2333.38
    INFO:tensorflow:loss = 3045367800.0, step = 8901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 2921651000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:34
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09614s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:34
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 197683380.0, global_step = 9000, label/mean = 13207.129, loss = 3056489000.0, prediction/mean = 1143.281
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-9000
    scores_zscore {'average_loss': 197683380.0, 'label/mean': 13207.129, 'loss': 3056489000.0, 'prediction/mean': 1143.281, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 4246730800.0, step = 9001
    INFO:tensorflow:global_step/sec: 1397.95
    INFO:tensorflow:loss = 3306273800.0, step = 9101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2379.31
    INFO:tensorflow:loss = 4954135000.0, step = 9201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2085.59
    INFO:tensorflow:loss = 2637065200.0, step = 9301 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2262.65
    INFO:tensorflow:loss = 3351370500.0, step = 9401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2385.62
    INFO:tensorflow:loss = 3987865300.0, step = 9501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2290.15
    INFO:tensorflow:loss = 2489160000.0, step = 9601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2335.09
    INFO:tensorflow:loss = 2870013400.0, step = 9701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2052.29
    INFO:tensorflow:loss = 3000328200.0, step = 9801 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2343.24
    INFO:tensorflow:loss = 1919985200.0, step = 9901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 3314891000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:35
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09521s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:35
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 193529680.0, global_step = 10000, label/mean = 13207.129, loss = 2992266800.0, prediction/mean = 1270.2664
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpfvtwejtl/model.ckpt-10000
    scores_zscore {'average_loss': 193529680.0, 'label/mean': 13207.129, 'loss': 2992266800.0, 'prediction/mean': 1270.2664, 'global_step': 10000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 0...
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 3389668600.0, step = 1
    INFO:tensorflow:global_step/sec: 1514.4
    INFO:tensorflow:loss = 3464490500.0, step = 101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2301.07
    INFO:tensorflow:loss = 5167428000.0, step = 201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2248.66
    INFO:tensorflow:loss = 3262564600.0, step = 301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2239.48
    INFO:tensorflow:loss = 2664319700.0, step = 401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2472.07
    INFO:tensorflow:loss = 3457207300.0, step = 501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2306.27
    INFO:tensorflow:loss = 2097327500.0, step = 601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2118.78
    INFO:tensorflow:loss = 3445272300.0, step = 701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2436.75
    INFO:tensorflow:loss = 2237972000.0, step = 801 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2415.6
    INFO:tensorflow:loss = 2460882400.0, step = 901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 5776439300.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:37
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09528s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:37
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 232542600.0, global_step = 1000, label/mean = 13207.129, loss = 3595466200.0, prediction/mean = 170.23247
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-1000
    scores_minmax {'average_loss': 232542600.0, 'label/mean': 13207.129, 'loss': 3595466200.0, 'prediction/mean': 170.23247, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 2737832200.0, step = 1001
    INFO:tensorflow:global_step/sec: 1528.82
    INFO:tensorflow:loss = 3717232000.0, step = 1101 (0.066 sec)
    INFO:tensorflow:global_step/sec: 2431.68
    INFO:tensorflow:loss = 6795015700.0, step = 1201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2180.17
    INFO:tensorflow:loss = 5597327400.0, step = 1301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2402.51
    INFO:tensorflow:loss = 3828832300.0, step = 1401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2059.61
    INFO:tensorflow:loss = 3052074800.0, step = 1501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2313.37
    INFO:tensorflow:loss = 4426054700.0, step = 1601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2375.58
    INFO:tensorflow:loss = 2180206000.0, step = 1701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2347.13
    INFO:tensorflow:loss = 4449070600.0, step = 1801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2231.65
    INFO:tensorflow:loss = 3448220400.0, step = 1901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 4927481000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:39
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09358s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:39
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 227919330.0, global_step = 2000, label/mean = 13207.129, loss = 3523983600.0, prediction/mean = 338.76306
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-2000
    scores_minmax {'average_loss': 227919330.0, 'label/mean': 13207.129, 'loss': 3523983600.0, 'prediction/mean': 338.76306, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 3382553600.0, step = 2001
    INFO:tensorflow:global_step/sec: 1442.1
    INFO:tensorflow:loss = 4445450000.0, step = 2101 (0.070 sec)
    INFO:tensorflow:global_step/sec: 2387.84
    INFO:tensorflow:loss = 4253312000.0, step = 2201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2289.68
    INFO:tensorflow:loss = 3502338000.0, step = 2301 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2239.04
    INFO:tensorflow:loss = 4138429000.0, step = 2401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2370.13
    INFO:tensorflow:loss = 3587597800.0, step = 2501 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2308.28
    INFO:tensorflow:loss = 3778683000.0, step = 2601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2125.9
    INFO:tensorflow:loss = 2480242700.0, step = 2701 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2350.22
    INFO:tensorflow:loss = 3924548400.0, step = 2801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 1964.41
    INFO:tensorflow:loss = 4807563000.0, step = 2901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 3902784000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:40
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09566s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:40
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 223395680.0, global_step = 3000, label/mean = 13207.129, loss = 3454040800.0, prediction/mean = 505.72018
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-3000
    scores_minmax {'average_loss': 223395680.0, 'label/mean': 13207.129, 'loss': 3454040800.0, 'prediction/mean': 505.72018, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 5804743700.0, step = 3001
    INFO:tensorflow:global_step/sec: 1566.1
    INFO:tensorflow:loss = 3560574500.0, step = 3101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2409.16
    INFO:tensorflow:loss = 2153217800.0, step = 3201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2367.6
    INFO:tensorflow:loss = 4023597000.0, step = 3301 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2301.24
    INFO:tensorflow:loss = 2975093200.0, step = 3401 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2433.43
    INFO:tensorflow:loss = 1932520300.0, step = 3501 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2462.82
    INFO:tensorflow:loss = 2616863200.0, step = 3601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2157.59
    INFO:tensorflow:loss = 1539329300.0, step = 3701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2291.84
    INFO:tensorflow:loss = 1433042200.0, step = 3801 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2169.39
    INFO:tensorflow:loss = 2144099600.0, step = 3901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 6449872000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:42
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09736s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:42
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 218963000.0, global_step = 4000, label/mean = 13207.129, loss = 3385505000.0, prediction/mean = 671.37946
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-4000
    scores_minmax {'average_loss': 218963000.0, 'label/mean': 13207.129, 'loss': 3385505000.0, 'prediction/mean': 671.37946, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 1852432500.0, step = 4001
    INFO:tensorflow:global_step/sec: 1474.2
    INFO:tensorflow:loss = 4452410400.0, step = 4101 (0.069 sec)
    INFO:tensorflow:global_step/sec: 2391.14
    INFO:tensorflow:loss = 3551087600.0, step = 4201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1898.47
    INFO:tensorflow:loss = 2200396500.0, step = 4301 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2379.42
    INFO:tensorflow:loss = 2818145800.0, step = 4401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2174.48
    INFO:tensorflow:loss = 4636538000.0, step = 4501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2438.62
    INFO:tensorflow:loss = 3095313200.0, step = 4601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2296.31
    INFO:tensorflow:loss = 6884931600.0, step = 4701 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2405.65
    INFO:tensorflow:loss = 2505297400.0, step = 4801 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2354.1
    INFO:tensorflow:loss = 3779248600.0, step = 4901 (0.043 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 3046099000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:43
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09571s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:43
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 214631380.0, global_step = 5000, label/mean = 13207.129, loss = 3318531300.0, prediction/mean = 835.3144
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-5000
    scores_minmax {'average_loss': 214631380.0, 'label/mean': 13207.129, 'loss': 3318531300.0, 'prediction/mean': 835.3144, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 2439218700.0, step = 5001
    INFO:tensorflow:global_step/sec: 1509.87
    INFO:tensorflow:loss = 2375851000.0, step = 5101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2432.2
    INFO:tensorflow:loss = 2412302300.0, step = 5201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2054.62
    INFO:tensorflow:loss = 2500778800.0, step = 5301 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2263.36
    INFO:tensorflow:loss = 3649456400.0, step = 5401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2297.1
    INFO:tensorflow:loss = 5548715000.0, step = 5501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2442
    INFO:tensorflow:loss = 3903906800.0, step = 5601 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2283.68
    INFO:tensorflow:loss = 2608113700.0, step = 5701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2150.25
    INFO:tensorflow:loss = 2747434000.0, step = 5801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2276.67
    INFO:tensorflow:loss = 2986380300.0, step = 5901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 1825018400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:45
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09489s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:45
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 210385540.0, global_step = 6000, label/mean = 13207.129, loss = 3252884000.0, prediction/mean = 998.04126
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-6000
    scores_minmax {'average_loss': 210385540.0, 'label/mean': 13207.129, 'loss': 3252884000.0, 'prediction/mean': 998.04126, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 3153027300.0, step = 6001
    INFO:tensorflow:global_step/sec: 1398
    INFO:tensorflow:loss = 5424498000.0, step = 6101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2058.29
    INFO:tensorflow:loss = 2303350800.0, step = 6201 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2086.15
    INFO:tensorflow:loss = 3306717200.0, step = 6301 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2129.38
    INFO:tensorflow:loss = 4059978800.0, step = 6401 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2335.92
    INFO:tensorflow:loss = 1913771800.0, step = 6501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2387.71
    INFO:tensorflow:loss = 2385219600.0, step = 6601 (0.042 sec)
    INFO:tensorflow:global_step/sec: 1994.3
    INFO:tensorflow:loss = 4408709600.0, step = 6701 (0.049 sec)
    INFO:tensorflow:global_step/sec: 2066.28
    INFO:tensorflow:loss = 4389825500.0, step = 6801 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2444.45
    INFO:tensorflow:loss = 2315456500.0, step = 6901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 2106170100.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:46
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11804s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:46
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 206219760.0, global_step = 7000, label/mean = 13207.129, loss = 3188475000.0, prediction/mean = 1159.7297
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-7000
    scores_minmax {'average_loss': 206219760.0, 'label/mean': 13207.129, 'loss': 3188475000.0, 'prediction/mean': 1159.7297, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 7002078000.0, step = 7001
    INFO:tensorflow:global_step/sec: 1532.1
    INFO:tensorflow:loss = 989777540.0, step = 7101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2160.44
    INFO:tensorflow:loss = 4280801800.0, step = 7201 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2142.47
    INFO:tensorflow:loss = 3399239700.0, step = 7301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2423.01
    INFO:tensorflow:loss = 1541617400.0, step = 7401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2263.15
    INFO:tensorflow:loss = 5130751500.0, step = 7501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2075.6
    INFO:tensorflow:loss = 3592200700.0, step = 7601 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2385.27
    INFO:tensorflow:loss = 2197716000.0, step = 7701 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2211.26
    INFO:tensorflow:loss = 3931728600.0, step = 7801 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2354.54
    INFO:tensorflow:loss = 2494183700.0, step = 7901 (0.042 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 1622494500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:48
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09497s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:48
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 202135620.0, global_step = 8000, label/mean = 13207.129, loss = 3125327600.0, prediction/mean = 1320.2864
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-8000
    scores_minmax {'average_loss': 202135620.0, 'label/mean': 13207.129, 'loss': 3125327600.0, 'prediction/mean': 1320.2864, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 2324705000.0, step = 8001
    INFO:tensorflow:global_step/sec: 1548.75
    INFO:tensorflow:loss = 4412857300.0, step = 8101 (0.065 sec)
    INFO:tensorflow:global_step/sec: 2280.55
    INFO:tensorflow:loss = 2776822800.0, step = 8201 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2428.71
    INFO:tensorflow:loss = 5579166700.0, step = 8301 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2252.66
    INFO:tensorflow:loss = 4771541000.0, step = 8401 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2031.24
    INFO:tensorflow:loss = 2622544400.0, step = 8501 (0.049 sec)
    INFO:tensorflow:global_step/sec: 1586.6
    INFO:tensorflow:loss = 2983721000.0, step = 8601 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2341.37
    INFO:tensorflow:loss = 3839786500.0, step = 8701 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2259.12
    INFO:tensorflow:loss = 2794496300.0, step = 8801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2187.95
    INFO:tensorflow:loss = 3199307800.0, step = 8901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 2784969200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:49
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09568s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:49
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 198142430.0, global_step = 9000, label/mean = 13207.129, loss = 3063586800.0, prediction/mean = 1479.3008
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-9000
    scores_minmax {'average_loss': 198142430.0, 'label/mean': 13207.129, 'loss': 3063586800.0, 'prediction/mean': 1479.3008, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 4190922800.0, step = 9001
    INFO:tensorflow:global_step/sec: 1095.11
    INFO:tensorflow:loss = 4348644400.0, step = 9101 (0.092 sec)
    INFO:tensorflow:global_step/sec: 2358.17
    INFO:tensorflow:loss = 2753370000.0, step = 9201 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2461.89
    INFO:tensorflow:loss = 2047054800.0, step = 9301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2330.25
    INFO:tensorflow:loss = 3630494700.0, step = 9401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2308.02
    INFO:tensorflow:loss = 3642808000.0, step = 9501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2204.4
    INFO:tensorflow:loss = 6788960000.0, step = 9601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2259.02
    INFO:tensorflow:loss = 2859459600.0, step = 9701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 1904.04
    INFO:tensorflow:loss = 3205723600.0, step = 9801 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2456.63
    INFO:tensorflow:loss = 7779707400.0, step = 9901 (0.041 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 2408236000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:23:51
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09517s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:23:51
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 194220340.0, global_step = 10000, label/mean = 13207.129, loss = 3002945300.0, prediction/mean = 1637.4926
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpyydtlfdw/model.ckpt-10000
    scores_minmax {'average_loss': 194220340.0, 'label/mean': 13207.129, 'loss': 3002945300.0, 'prediction/mean': 1637.4926, 'global_step': 10000}





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
for _ in range(num_print_statements):
    est_gd.train(train_input_fn, steps=num_training_steps // num_print_statements)                                                         
    scores_gd = est_gd.evaluate(eval_input_fn)
    print('scores_gd', scores_gd)

# Problem with Task 2.3: GradientDescentOptimizer + Z-score normalization
'''
ERROR:tensorflow:Model diverged with loss = NaN.
'''
```


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
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 2822984700.0, step = 1
    INFO:tensorflow:global_step/sec: 1858.32
    INFO:tensorflow:loss = 3446496300.0, step = 101 (0.055 sec)
    INFO:tensorflow:global_step/sec: 2508.53
    INFO:tensorflow:loss = 5168191500.0, step = 201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2941.35
    INFO:tensorflow:loss = 3568298000.0, step = 301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2857
    INFO:tensorflow:loss = 5711933000.0, step = 401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2728.13
    INFO:tensorflow:loss = 2506798800.0, step = 501 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2675.74
    INFO:tensorflow:loss = 4649361400.0, step = 601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2697.35
    INFO:tensorflow:loss = 4182385200.0, step = 701 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2791.68
    INFO:tensorflow:loss = 3222525000.0, step = 801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2969.99
    INFO:tensorflow:loss = 3872244700.0, step = 901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 4871383600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:20
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.09619s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:20
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 235318190.0, global_step = 1000, label/mean = 13207.129, loss = 3638381300.0, prediction/mean = 55.707584
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-1000
    scores_pca {'average_loss': 235318190.0, 'label/mean': 13207.129, 'loss': 3638381300.0, 'prediction/mean': 55.707584, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 3542584600.0, step = 1001
    INFO:tensorflow:global_step/sec: 1954.85
    INFO:tensorflow:loss = 2918047200.0, step = 1101 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2703.21
    INFO:tensorflow:loss = 2335144400.0, step = 1201 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2867.06
    INFO:tensorflow:loss = 2341849000.0, step = 1301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2862.95
    INFO:tensorflow:loss = 3775243800.0, step = 1401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2567.25
    INFO:tensorflow:loss = 3246102500.0, step = 1501 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2935.05
    INFO:tensorflow:loss = 3701038000.0, step = 1601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2604.59
    INFO:tensorflow:loss = 4955000000.0, step = 1701 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2506.44
    INFO:tensorflow:loss = 5462490000.0, step = 1801 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2208.97
    INFO:tensorflow:loss = 4576856000.0, step = 1901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 2632832500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:22
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.16857s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:22
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 233123090.0, global_step = 2000, label/mean = 13207.129, loss = 3604441600.0, prediction/mean = 117.108376
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-2000
    scores_pca {'average_loss': 233123090.0, 'label/mean': 13207.129, 'loss': 3604441600.0, 'prediction/mean': 117.108376, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 3190963500.0, step = 2001
    INFO:tensorflow:global_step/sec: 1868.8
    INFO:tensorflow:loss = 4577575000.0, step = 2101 (0.054 sec)
    INFO:tensorflow:global_step/sec: 2754.83
    INFO:tensorflow:loss = 3512246800.0, step = 2201 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2879.77
    INFO:tensorflow:loss = 4501397000.0, step = 2301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2899.48
    INFO:tensorflow:loss = 3650058200.0, step = 2401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2957
    INFO:tensorflow:loss = 4882476000.0, step = 2501 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2894.1
    INFO:tensorflow:loss = 7033726000.0, step = 2601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2843.75
    INFO:tensorflow:loss = 2867456000.0, step = 2701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2884.8
    INFO:tensorflow:loss = 4618662000.0, step = 2801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2824.56
    INFO:tensorflow:loss = 3029607700.0, step = 2901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 5722501000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:23
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08723s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:23
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 230906140.0, global_step = 3000, label/mean = 13207.129, loss = 3570164200.0, prediction/mean = 178.76662
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-3000
    scores_pca {'average_loss': 230906140.0, 'label/mean': 13207.129, 'loss': 3570164200.0, 'prediction/mean': 178.76662, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 3286167600.0, step = 3001
    INFO:tensorflow:global_step/sec: 1960.79
    INFO:tensorflow:loss = 4962417000.0, step = 3101 (0.051 sec)
    INFO:tensorflow:global_step/sec: 3001.29
    INFO:tensorflow:loss = 4254056400.0, step = 3201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2674.51
    INFO:tensorflow:loss = 1697162800.0, step = 3301 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2948.81
    INFO:tensorflow:loss = 2500264400.0, step = 3401 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2801.26
    INFO:tensorflow:loss = 2726297600.0, step = 3501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2938.61
    INFO:tensorflow:loss = 3362808800.0, step = 3601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2805.67
    INFO:tensorflow:loss = 3443250700.0, step = 3701 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2865.9
    INFO:tensorflow:loss = 3853674500.0, step = 3801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2881.02
    INFO:tensorflow:loss = 2123613300.0, step = 3901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 2474248700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:25
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08830s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:25
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 228675940.0, global_step = 4000, label/mean = 13207.129, loss = 3535681800.0, prediction/mean = 240.41096
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-4000
    scores_pca {'average_loss': 228675940.0, 'label/mean': 13207.129, 'loss': 3535681800.0, 'prediction/mean': 240.41096, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 4290235400.0, step = 4001
    INFO:tensorflow:global_step/sec: 1905.85
    INFO:tensorflow:loss = 3949850600.0, step = 4101 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2934.37
    INFO:tensorflow:loss = 3960533800.0, step = 4201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2889.26
    INFO:tensorflow:loss = 3940558800.0, step = 4301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2870.67
    INFO:tensorflow:loss = 2473121800.0, step = 4401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2719.39
    INFO:tensorflow:loss = 3562566000.0, step = 4501 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2750.74
    INFO:tensorflow:loss = 4058944500.0, step = 4601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2863.44
    INFO:tensorflow:loss = 4328343600.0, step = 4701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2838.88
    INFO:tensorflow:loss = 4308092000.0, step = 4801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2826.14
    INFO:tensorflow:loss = 1514110500.0, step = 4901 (0.036 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 6677186600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:26
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.16375s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:26
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 226445970.0, global_step = 5000, label/mean = 13207.129, loss = 3501203200.0, prediction/mean = 302.0357
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-5000
    scores_pca {'average_loss': 226445970.0, 'label/mean': 13207.129, 'loss': 3501203200.0, 'prediction/mean': 302.0357, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 4111745000.0, step = 5001
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 5012 vs previous value: 5012. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 5083 vs previous value: 5083. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
    INFO:tensorflow:global_step/sec: 1426.07
    INFO:tensorflow:loss = 2802896400.0, step = 5101 (0.071 sec)
    INFO:tensorflow:global_step/sec: 2140.58
    INFO:tensorflow:loss = 2675186700.0, step = 5201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2458.95
    INFO:tensorflow:loss = 3142436900.0, step = 5301 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2531.51
    INFO:tensorflow:loss = 5738563600.0, step = 5401 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2789.8
    INFO:tensorflow:loss = 1983788700.0, step = 5501 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2797.1
    INFO:tensorflow:loss = 2956128500.0, step = 5601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2858.54
    INFO:tensorflow:loss = 3311237400.0, step = 5701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2823.29
    INFO:tensorflow:loss = 1864028200.0, step = 5801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2281.21
    INFO:tensorflow:loss = 6347672600.0, step = 5901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 2225233400.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:28
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08644s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:28
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 224221170.0, global_step = 6000, label/mean = 13207.129, loss = 3466804200.0, prediction/mean = 363.59833
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-6000
    scores_pca {'average_loss': 224221170.0, 'label/mean': 13207.129, 'loss': 3466804200.0, 'prediction/mean': 363.59833, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 5175226000.0, step = 6001
    INFO:tensorflow:global_step/sec: 1950.31
    INFO:tensorflow:loss = 2143427300.0, step = 6101 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2929.45
    INFO:tensorflow:loss = 4431459300.0, step = 6201 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2974.87
    INFO:tensorflow:loss = 4248520200.0, step = 6301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2830.85
    INFO:tensorflow:loss = 2744656400.0, step = 6401 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2994.46
    INFO:tensorflow:loss = 2755443700.0, step = 6501 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2851.6
    INFO:tensorflow:loss = 2882191000.0, step = 6601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2891.33
    INFO:tensorflow:loss = 5305789000.0, step = 6701 (0.034 sec)
    INFO:tensorflow:global_step/sec: 3004.28
    INFO:tensorflow:loss = 3256545800.0, step = 6801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2809.22
    INFO:tensorflow:loss = 1988833800.0, step = 6901 (0.035 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 2661295600.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:29
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08631s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:29
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 222003740.0, global_step = 7000, label/mean = 13207.129, loss = 3432519400.0, prediction/mean = 425.0341
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-7000
    scores_pca {'average_loss': 222003740.0, 'label/mean': 13207.129, 'loss': 3432519400.0, 'prediction/mean': 425.0341, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 2160324900.0, step = 7001
    INFO:tensorflow:global_step/sec: 1603.73
    INFO:tensorflow:loss = 8125150000.0, step = 7101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2184.59
    INFO:tensorflow:loss = 3857738800.0, step = 7201 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2183.99
    INFO:tensorflow:loss = 3664234000.0, step = 7301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2430.48
    INFO:tensorflow:loss = 2796925000.0, step = 7401 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2826.14
    INFO:tensorflow:loss = 4558593500.0, step = 7501 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2964.63
    INFO:tensorflow:loss = 5313566000.0, step = 7601 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2826.92
    INFO:tensorflow:loss = 1635471400.0, step = 7701 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2840.11
    INFO:tensorflow:loss = 6258047000.0, step = 7801 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2944.38
    INFO:tensorflow:loss = 2544512500.0, step = 7901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 3792712200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:30
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08788s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:30
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 219799630.0, global_step = 8000, label/mean = 13207.129, loss = 3398440400.0, prediction/mean = 486.30286
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-8000
    scores_pca {'average_loss': 219799630.0, 'label/mean': 13207.129, 'loss': 3398440400.0, 'prediction/mean': 486.30286, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 1636901600.0, step = 8001
    INFO:tensorflow:global_step/sec: 1699.43
    INFO:tensorflow:loss = 2682674000.0, step = 8101 (0.059 sec)
    INFO:tensorflow:global_step/sec: 2872.34
    INFO:tensorflow:loss = 2079450800.0, step = 8201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2863.85
    INFO:tensorflow:loss = 2591231200.0, step = 8301 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2822.87
    INFO:tensorflow:loss = 4420414000.0, step = 8401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2896.78
    INFO:tensorflow:loss = 2780532500.0, step = 8501 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2912.41
    INFO:tensorflow:loss = 4138756000.0, step = 8601 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2839.13
    INFO:tensorflow:loss = 1663251200.0, step = 8701 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2920.82
    INFO:tensorflow:loss = 3994781200.0, step = 8801 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2865.8
    INFO:tensorflow:loss = 2423991600.0, step = 8901 (0.034 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 3513745700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:32
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08647s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:32
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 217605150.0, global_step = 9000, label/mean = 13207.129, loss = 3364510500.0, prediction/mean = 547.5032
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-9000
    scores_pca {'average_loss': 217605150.0, 'label/mean': 13207.129, 'loss': 3364510500.0, 'prediction/mean': 547.5032, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 5095286000.0, step = 9001
    INFO:tensorflow:global_step/sec: 2052.03
    INFO:tensorflow:loss = 2295491000.0, step = 9101 (0.050 sec)
    INFO:tensorflow:global_step/sec: 2783.9
    INFO:tensorflow:loss = 3365401600.0, step = 9201 (0.035 sec)
    INFO:tensorflow:global_step/sec: 2932.38
    INFO:tensorflow:loss = 2455677700.0, step = 9301 (0.034 sec)
    INFO:tensorflow:global_step/sec: 2776.32
    INFO:tensorflow:loss = 2200908000.0, step = 9401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2334.32
    INFO:tensorflow:loss = 4280295000.0, step = 9501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2296.52
    INFO:tensorflow:loss = 3186238700.0, step = 9601 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2104.63
    INFO:tensorflow:loss = 6098979000.0, step = 9701 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2391.09
    INFO:tensorflow:loss = 2908279800.0, step = 9801 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2187.22
    INFO:tensorflow:loss = 6138582000.0, step = 9901 (0.046 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 3192895500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:33
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.08726s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:33
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 215430560.0, global_step = 10000, label/mean = 13207.129, loss = 3330888000.0, prediction/mean = 608.41113
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmp0if74k76/model.ckpt-10000
    scores_pca {'average_loss': 215430560.0, 'label/mean': 13207.129, 'loss': 3330888000.0, 'prediction/mean': 608.41113, 'global_step': 10000}


### Task 3: Make your best model using only categorical features

- Look at the possible feature columns for categorical features. They begin with `categorical_column_with_` in go/tf-ops.
- You may find `dataframe[categorical_feature_names].unique()` helpful.



```python
## Your code goes here
car_data[feature_name].unique()
```




    array([ 9.  ,  9.2 ,  8.5 ,  9.4 ,  8.4 ,  9.5 ,  8.  ,  8.1 , 11.5 ,
            7.5 ,  7.  ,  9.3 ,  7.6 ,  8.3 ,  8.7 ,  8.6 , 23.  , 22.7 ,
           21.5 , 22.  , 22.5 , 10.  ,  9.6 ,  7.7 , 21.  ,  8.8 ,  9.1 ,
            9.41, 21.9 ,  9.31,  7.8 , 10.1 ])




```python
# LabelEncoder is used to convert categorical string features into numeric labels.
label_encoder = preprocessing.LabelEncoder()
for feature_name in categorical_feature_names:
  car_data[feature_name] = label_encoder.fit_transform(car_data[feature_name])

#TODO
# # Normalization / Standardization only for those ten columns of data
```


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

    model_feature_columns [IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='fuel-system', vocabulary_list=('mpfi', '1bbl', '2bbl', 'spdi', 'mfi', 'idi', 'spfi', '4bbl'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='num-doors', vocabulary_list=('two', 'four', '?'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='aspiration', vocabulary_list=('std', 'turbo'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='fuel-type', vocabulary_list=('gas', 'diesel'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='drive-wheels', vocabulary_list=('fwd', 'rwd', '4wd'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='body-style', vocabulary_list=('sedan', 'hatchback', 'wagon', 'hardtop', 'convertible'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='engine-type', vocabulary_list=('ohc', 'l', 'dohc', 'ohcv', 'ohcf', 'rotor'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='num-cylinders', vocabulary_list=('four', 'six', 'five', 'twelve', 'eight', 'three', 'two'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='engine-location', vocabulary_list=('front', 'rear'), dtype=tf.string, default_value=-1, num_oov_buckets=0)), IndicatorColumn(categorical_column=VocabularyListCategoricalColumn(key='make', vocabulary_list=('volkswagen', 'honda', 'nissan', 'mitsubishi', 'peugot', 'volvo', 'toyota', 'audi', 'jaguar', 'mazda', 'dodge', 'porsche', 'renault', 'bmw', 'plymouth', 'subaru', 'saab', 'mercedes-benz', 'isuzu', 'chevrolet', 'alfa-romero', 'mercury'), dtype=tf.string, default_value=-1, num_oov_buckets=0))]
    INFO:tensorflow:Using default config.
    WARNING:tensorflow:Using temporary folder as model directory: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u
    INFO:tensorflow:Using config: {'_model_dir': '/var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u', '_tf_random_seed': None, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_save_checkpoints_secs': 600, '_session_config': allow_soft_placement: true
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
    INFO:tensorflow:Saving checkpoints for 0 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 0...
    INFO:tensorflow:loss = 4813285400.0, step = 1
    INFO:tensorflow:global_step/sec: 1377.81
    INFO:tensorflow:loss = 6040973300.0, step = 101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2426.95
    INFO:tensorflow:loss = 2720525000.0, step = 201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2663.07
    INFO:tensorflow:loss = 3741218800.0, step = 301 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2430.66
    INFO:tensorflow:loss = 2622611500.0, step = 401 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2354.88
    INFO:tensorflow:loss = 3141782000.0, step = 501 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2516.28
    INFO:tensorflow:loss = 3798938600.0, step = 601 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2448.59
    INFO:tensorflow:loss = 6190495000.0, step = 701 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2316.32
    INFO:tensorflow:loss = 1495821600.0, step = 801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2753.23
    INFO:tensorflow:loss = 5157670000.0, step = 901 (0.036 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:Loss for final step: 3072327700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:54
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.36037s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:55
    INFO:tensorflow:Saving dict for global step 1000: average_loss = 230707890.0, global_step = 1000, label/mean = 13207.129, loss = 3567099000.0, prediction/mean = 254.6194
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 1000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-1000
    scores {'average_loss': 230707890.0, 'label/mean': 13207.129, 'loss': 3567099000.0, 'prediction/mean': 254.6194, 'global_step': 1000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-1000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 1000...
    INFO:tensorflow:Saving checkpoints for 1000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 1000...
    INFO:tensorflow:loss = 1984580100.0, step = 1001
    INFO:tensorflow:global_step/sec: 1509.69
    INFO:tensorflow:loss = 4698823700.0, step = 1101 (0.067 sec)
    INFO:tensorflow:global_step/sec: 2273.35
    INFO:tensorflow:loss = 2309706200.0, step = 1201 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2506.28
    INFO:tensorflow:loss = 4839858000.0, step = 1301 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2157.4
    INFO:tensorflow:loss = 1658192600.0, step = 1401 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2278.16
    INFO:tensorflow:loss = 2328341000.0, step = 1501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2586.38
    INFO:tensorflow:loss = 3750448600.0, step = 1601 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2557.22
    INFO:tensorflow:loss = 6815361000.0, step = 1701 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2447.2
    INFO:tensorflow:loss = 3032665000.0, step = 1801 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2704.33
    INFO:tensorflow:loss = 4140358400.0, step = 1901 (0.037 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:Loss for final step: 4202013700.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:56
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11353s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:57
    INFO:tensorflow:Saving dict for global step 2000: average_loss = 224470400.0, global_step = 2000, label/mean = 13207.129, loss = 3470657800.0, prediction/mean = 501.12558
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 2000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-2000
    scores {'average_loss': 224470400.0, 'label/mean': 13207.129, 'loss': 3470657800.0, 'prediction/mean': 501.12558, 'global_step': 2000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-2000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 2000...
    INFO:tensorflow:Saving checkpoints for 2000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 2000...
    INFO:tensorflow:loss = 5992153000.0, step = 2001
    INFO:tensorflow:global_step/sec: 1348.83
    INFO:tensorflow:loss = 1866832000.0, step = 2101 (0.075 sec)
    INFO:tensorflow:global_step/sec: 2492.35
    INFO:tensorflow:loss = 6127624700.0, step = 2201 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2706.86
    INFO:tensorflow:loss = 9004777000.0, step = 2301 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2659.3
    INFO:tensorflow:loss = 2378246100.0, step = 2401 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2087.67
    INFO:tensorflow:loss = 2671217000.0, step = 2501 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2142.48
    INFO:tensorflow:loss = 2232184800.0, step = 2601 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2484.91
    INFO:tensorflow:loss = 3659158000.0, step = 2701 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2637.69
    INFO:tensorflow:loss = 3394299400.0, step = 2801 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2538.45
    INFO:tensorflow:loss = 4110985500.0, step = 2901 (0.039 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:Loss for final step: 6573448000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:24:58
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10841s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:24:58
    INFO:tensorflow:Saving dict for global step 3000: average_loss = 218446850.0, global_step = 3000, label/mean = 13207.129, loss = 3377524500.0, prediction/mean = 743.75806
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 3000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-3000
    scores {'average_loss': 218446850.0, 'label/mean': 13207.129, 'loss': 3377524500.0, 'prediction/mean': 743.75806, 'global_step': 3000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-3000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 3000...
    INFO:tensorflow:Saving checkpoints for 3000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 3000...
    INFO:tensorflow:loss = 1520061400.0, step = 3001
    INFO:tensorflow:global_step/sec: 1325.29
    INFO:tensorflow:loss = 4773121000.0, step = 3101 (0.076 sec)
    INFO:tensorflow:global_step/sec: 2555.2
    INFO:tensorflow:loss = 2168720000.0, step = 3201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2219.65
    INFO:tensorflow:loss = 3020885500.0, step = 3301 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2227.27
    INFO:tensorflow:loss = 3067054000.0, step = 3401 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2234.19
    INFO:tensorflow:loss = 2520741000.0, step = 3501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2765.65
    INFO:tensorflow:loss = 6114738000.0, step = 3601 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2576.39
    INFO:tensorflow:loss = 4136173300.0, step = 3701 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2203.08
    INFO:tensorflow:loss = 2106347900.0, step = 3801 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2290.69
    INFO:tensorflow:loss = 2934808600.0, step = 3901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:Loss for final step: 4549290500.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:00
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11514s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:00
    INFO:tensorflow:Saving dict for global step 4000: average_loss = 212613360.0, global_step = 4000, label/mean = 13207.129, loss = 3287329500.0, prediction/mean = 983.3075
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 4000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-4000
    scores {'average_loss': 212613360.0, 'label/mean': 13207.129, 'loss': 3287329500.0, 'prediction/mean': 983.3075, 'global_step': 4000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-4000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 4000...
    INFO:tensorflow:Saving checkpoints for 4000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 4000...
    INFO:tensorflow:loss = 3314372900.0, step = 4001
    INFO:tensorflow:global_step/sec: 1386.31
    INFO:tensorflow:loss = 3655617300.0, step = 4101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2560.17
    INFO:tensorflow:loss = 2043214100.0, step = 4201 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2749.5
    INFO:tensorflow:loss = 3024963600.0, step = 4301 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2567.99
    INFO:tensorflow:loss = 2359365000.0, step = 4401 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2574.66
    INFO:tensorflow:loss = 2380664800.0, step = 4501 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2599.72
    INFO:tensorflow:loss = 2774961200.0, step = 4601 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2536.33
    INFO:tensorflow:loss = 2506297900.0, step = 4701 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2771.68
    INFO:tensorflow:loss = 1613503600.0, step = 4801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2188.52
    INFO:tensorflow:loss = 2024513400.0, step = 4901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:Loss for final step: 2841360000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:02
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10679s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:02
    INFO:tensorflow:Saving dict for global step 5000: average_loss = 206951280.0, global_step = 5000, label/mean = 13207.129, loss = 3199785200.0, prediction/mean = 1220.2997
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 5000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-5000
    scores {'average_loss': 206951280.0, 'label/mean': 13207.129, 'loss': 3199785200.0, 'prediction/mean': 1220.2997, 'global_step': 5000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-5000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 5000...
    INFO:tensorflow:Saving checkpoints for 5000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 5000...
    INFO:tensorflow:loss = 4038269400.0, step = 5001
    INFO:tensorflow:global_step/sec: 1604.46
    INFO:tensorflow:loss = 2725118000.0, step = 5101 (0.063 sec)
    INFO:tensorflow:global_step/sec: 2655.13
    INFO:tensorflow:loss = 4097829400.0, step = 5201 (0.038 sec)
    INFO:tensorflow:global_step/sec: 1487.08
    INFO:tensorflow:loss = 1471696600.0, step = 5301 (0.068 sec)
    INFO:tensorflow:global_step/sec: 1880.3
    INFO:tensorflow:loss = 2940752000.0, step = 5401 (0.053 sec)
    INFO:tensorflow:global_step/sec: 2254.27
    INFO:tensorflow:loss = 4121250000.0, step = 5501 (0.044 sec)
    INFO:tensorflow:global_step/sec: 2232.25
    INFO:tensorflow:loss = 1602989700.0, step = 5601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2540.59
    INFO:tensorflow:loss = 2907113000.0, step = 5701 (0.039 sec)
    INFO:tensorflow:global_step/sec: 2322.56
    INFO:tensorflow:loss = 2961684200.0, step = 5801 (0.043 sec)
    INFO:tensorflow:global_step/sec: 2224.99
    INFO:tensorflow:loss = 1521886000.0, step = 5901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:Loss for final step: 2953522200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:03
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.13375s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:03
    INFO:tensorflow:Saving dict for global step 6000: average_loss = 201475700.0, global_step = 6000, label/mean = 13207.129, loss = 3115124200.0, prediction/mean = 1454.0922
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 6000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-6000
    scores {'average_loss': 201475700.0, 'label/mean': 13207.129, 'loss': 3115124200.0, 'prediction/mean': 1454.0922, 'global_step': 6000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-6000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 6000...
    INFO:tensorflow:Saving checkpoints for 6000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 6000...
    INFO:tensorflow:loss = 1152493200.0, step = 6001
    INFO:tensorflow:global_step/sec: 1388.6
    INFO:tensorflow:loss = 4658452500.0, step = 6101 (0.072 sec)
    INFO:tensorflow:global_step/sec: 2411.43
    INFO:tensorflow:loss = 3289183700.0, step = 6201 (0.041 sec)
    INFO:tensorflow:global_step/sec: 2659.02
    INFO:tensorflow:loss = 5682495500.0, step = 6301 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2745.21
    INFO:tensorflow:loss = 2981850400.0, step = 6401 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2195.96
    INFO:tensorflow:loss = 4821574700.0, step = 6501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2637.28
    INFO:tensorflow:loss = 1373690900.0, step = 6601 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2627.78
    INFO:tensorflow:loss = 2252151600.0, step = 6701 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2665.1
    INFO:tensorflow:loss = 1484919000.0, step = 6801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2297.69
    INFO:tensorflow:loss = 4822449000.0, step = 6901 (0.044 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:Loss for final step: 1370179200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:05
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10802s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:05
    INFO:tensorflow:Saving dict for global step 7000: average_loss = 196175820.0, global_step = 7000, label/mean = 13207.129, loss = 3033180000.0, prediction/mean = 1684.8597
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 7000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-7000
    scores {'average_loss': 196175820.0, 'label/mean': 13207.129, 'loss': 3033180000.0, 'prediction/mean': 1684.8597, 'global_step': 7000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-7000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 7000...
    INFO:tensorflow:Saving checkpoints for 7000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 7000...
    INFO:tensorflow:loss = 4592964000.0, step = 7001
    INFO:tensorflow:global_step/sec: 1369.26
    INFO:tensorflow:loss = 4627575000.0, step = 7101 (0.073 sec)
    INFO:tensorflow:global_step/sec: 2702.71
    INFO:tensorflow:loss = 3946114000.0, step = 7201 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2395.09
    INFO:tensorflow:loss = 2351654100.0, step = 7301 (0.042 sec)
    INFO:tensorflow:global_step/sec: 2659.77
    INFO:tensorflow:loss = 2495986200.0, step = 7401 (0.038 sec)
    INFO:tensorflow:global_step/sec: 2205.9
    INFO:tensorflow:loss = 2277291500.0, step = 7501 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2242.72
    INFO:tensorflow:loss = 4614482000.0, step = 7601 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2229.9
    INFO:tensorflow:loss = 4868116000.0, step = 7701 (0.045 sec)
    INFO:tensorflow:global_step/sec: 2789.08
    INFO:tensorflow:loss = 1474170400.0, step = 7801 (0.036 sec)
    INFO:tensorflow:global_step/sec: 2204.82
    INFO:tensorflow:loss = 2780770000.0, step = 7901 (0.045 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:Loss for final step: 2915105000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:06
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.14051s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:07
    INFO:tensorflow:Saving dict for global step 8000: average_loss = 191030800.0, global_step = 8000, label/mean = 13207.129, loss = 2953630000.0, prediction/mean = 1913.3024
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 8000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-8000
    scores {'average_loss': 191030800.0, 'label/mean': 13207.129, 'loss': 2953630000.0, 'prediction/mean': 1913.3024, 'global_step': 8000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-8000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 8000...
    INFO:tensorflow:Saving checkpoints for 8000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 8000...
    INFO:tensorflow:loss = 2261327400.0, step = 8001
    INFO:tensorflow:global_step/sec: 1327.51
    INFO:tensorflow:loss = 2081886800.0, step = 8101 (0.076 sec)
    INFO:tensorflow:global_step/sec: 794.104
    INFO:tensorflow:loss = 2141028600.0, step = 8201 (0.129 sec)
    INFO:tensorflow:global_step/sec: 1011.48
    INFO:tensorflow:loss = 4425421300.0, step = 8301 (0.100 sec)
    INFO:tensorflow:global_step/sec: 1136.72
    INFO:tensorflow:loss = 5216067600.0, step = 8401 (0.084 sec)
    INFO:tensorflow:global_step/sec: 2497.19
    INFO:tensorflow:loss = 4126176500.0, step = 8501 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2718.42
    INFO:tensorflow:loss = 611853630.0, step = 8601 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2484.48
    INFO:tensorflow:loss = 1388747000.0, step = 8701 (0.040 sec)
    INFO:tensorflow:global_step/sec: 2705.85
    INFO:tensorflow:loss = 2782794800.0, step = 8801 (0.037 sec)
    INFO:tensorflow:global_step/sec: 2525.46
    INFO:tensorflow:loss = 1148323600.0, step = 8901 (0.040 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:Loss for final step: 1561123200.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:08
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.10733s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:09
    INFO:tensorflow:Saving dict for global step 9000: average_loss = 186057730.0, global_step = 9000, label/mean = 13207.129, loss = 2876738600.0, prediction/mean = 2138.5754
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 9000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-9000
    scores {'average_loss': 186057730.0, 'label/mean': 13207.129, 'loss': 2876738600.0, 'prediction/mean': 2138.5754, 'global_step': 9000}
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Create CheckpointSaverHook.
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-9000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 9000...
    INFO:tensorflow:Saving checkpoints for 9000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 9000...
    INFO:tensorflow:loss = 2810859800.0, step = 9001
    INFO:tensorflow:global_step/sec: 1144.9
    INFO:tensorflow:loss = 2521520000.0, step = 9101 (0.088 sec)
    INFO:tensorflow:global_step/sec: 2099.3
    INFO:tensorflow:loss = 3020571400.0, step = 9201 (0.048 sec)
    INFO:tensorflow:global_step/sec: 2188.57
    INFO:tensorflow:loss = 3211394600.0, step = 9301 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1941.18
    INFO:tensorflow:loss = 1653686800.0, step = 9401 (0.052 sec)
    INFO:tensorflow:global_step/sec: 2143.53
    INFO:tensorflow:loss = 4341704000.0, step = 9501 (0.046 sec)
    INFO:tensorflow:global_step/sec: 1997.09
    INFO:tensorflow:loss = 2310191900.0, step = 9601 (0.051 sec)
    INFO:tensorflow:global_step/sec: 2154.8
    INFO:tensorflow:loss = 3602088000.0, step = 9701 (0.046 sec)
    INFO:tensorflow:global_step/sec: 2092.53
    INFO:tensorflow:loss = 2738602500.0, step = 9801 (0.047 sec)
    INFO:tensorflow:global_step/sec: 2062.66
    INFO:tensorflow:loss = 2127286000.0, step = 9901 (0.050 sec)
    INFO:tensorflow:Calling checkpoint listeners before saving checkpoint 10000...
    INFO:tensorflow:Saving checkpoints for 10000 into /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt.
    INFO:tensorflow:Calling checkpoint listeners after saving checkpoint 10000...
    INFO:tensorflow:Loss for final step: 2365253000.0.
    INFO:tensorflow:Calling model_fn.
    INFO:tensorflow:Done calling model_fn.
    INFO:tensorflow:Starting evaluation at 2026-04-01T13:25:10
    INFO:tensorflow:Graph was finalized.
    INFO:tensorflow:Restoring parameters from /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-10000
    INFO:tensorflow:Running local_init_op.
    INFO:tensorflow:Done running local_init_op.
    INFO:tensorflow:Inference Time : 0.11850s
    INFO:tensorflow:Finished evaluation at 2026-04-01-13:25:10
    INFO:tensorflow:Saving dict for global step 10000: average_loss = 181233200.0, global_step = 10000, label/mean = 13207.129, loss = 2802144300.0, prediction/mean = 2361.4622
    INFO:tensorflow:Saving 'checkpoint_path' summary for global step 10000: /var/folders/c4/t_n58l316yl308hxjf5jlwsh0000gn/T/tmpxwej544u/model.ckpt-10000
    scores {'average_loss': 181233200.0, 'label/mean': 13207.129, 'loss': 2802144300.0, 'prediction/mean': 2361.4622, 'global_step': 10000}


### Task 4: Using all the features, make the best model that you can make

With all the features combined, your model should perform better than your earlier models using numerical and categorical models alone. Tune your model until that is the case.


```python
## Your code goes here

# Combine all data (take care to use normalized data)
# Run code again, to check...
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
