import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import FunctionTransformer

from utils import log_transform, inverse_log_transform, print_ystats
from models import train_gp_model, gp_predict, get_metrics

X = pd.read_csv('../outputs/collation_4_30_24/master_collection.csv')
Y = pd.read_csv('../outputs/collation_4_30_24/yields.csv')

numeric = ['Elution pH', 'Wash pH', 'Equlibration pH', 'Elution Conductivity',
       'Wash Conductivity', 'Equilibration Conductivity', 'Sample Volume (mL)',
       'System Flowrate Elution (CV/h)', 'Sample Flowrate Elution (CV/h)']

X = X.groupby(['Pure','resin', 'serotype'])[numeric].mean().reset_index()

new_df = pd.merge(X, Y, on=['resin', 'serotype', 'Pure'])
new_df = pd.get_dummies(new_df, columns=['serotype', 'from', 'resin'])
new_df.reset_index(inplace=True, drop=True)
new_df['y_log'] = log_transform(new_df['total'])

X = new_df.drop(['total', 'Sample Volume (mL)', 'y_log'], axis=1)
Y = new_df[['total', 'y_log']]

x_train, x_test, y_train, y_test = train_test_split(X, Y['y_log'], test_size=0.2, random_state=42, shuffle=True)
x_train_total, x_test_total, y_train_total, y_test_total = train_test_split(X, Y['total'], test_size=0.2, random_state=42, shuffle=True)

scaled_experiment = False

scaler = MinMaxScaler()
y_train_scaled = scaler.fit_transform(y_train.values.reshape(-1, 1))
y_test_scaled = scaler.transform(y_test.values.reshape(-1, 1))

# print_ystats(y_train_scaled, "y_train_scaled")

if scaled_experiment:
    print('Scaled Experiment')
    gaussian_process = train_gp_model(x_train, y_train_scaled)
    mean_prediction, std_prediction = gp_predict(gaussian_process, x_test)
    print('Scaled Experiment - metrics with scaled')
    test_metrics_scaled = get_metrics(y_test_scaled, mean_prediction)
    print('Scaled Experiment - metrics with actual log scale')
    change_to_actual = scaler.inverse_transform(mean_prediction.reshape(1, -1))
    test_metrics_scaled_inverse = get_metrics(y_test.values, change_to_actual.reshape(y_test.values.shape))
else:
    print('Normal Experiment')
    gaussian_process = train_gp_model(x_train, y_train)
    mean_prediction, std_prediction = gp_predict(gaussian_process, x_test)
    test_metrics_unscaled = get_metrics(y_test, mean_prediction)
    print('Unscaled Experiment - metrics with actual total')
    change_to_actual = inverse_log_transform(mean_prediction)
    get_metrics(y_test_total.values, change_to_actual.reshape(y_test_total.values.shape))
    print_ystats(y_train_total, "y_train_total")