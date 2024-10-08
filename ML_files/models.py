from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import *
from sklearn import svm

from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor


def train_svm_model(x_train, y_train):
    params = {'C': 30, 'gamma': 0.1, 'kernel': 'rbf'}
    SVC = svm.SVR(**params)
    SVC.fit(x_train, y_train)
    return SVC

def svm_predict(model, x_test):
    svm_preds = model.predict(x_test)
    return svm_preds

def train_gp_model(x_train, y_train):
    kernel = Sum(DotProduct(sigma_0=0.01, sigma_0_bounds=(1e-6, 1e6)),\
                  RationalQuadratic(alpha=0.01, length_scale=0.01,length_scale_bounds=(1e-6, 1e6))) \
                + Matern(length_scale=0.1, nu=1.5,length_scale_bounds=(1e-6, 1e6))
    kernel = Exponentiation(kernel, exponent=1)
    gaussian_process = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=50)
    gaussian_process.fit(x_train, y_train)
    return gaussian_process

def gp_predict(model, x_test):
    mean_prediction, std_prediction = model.predict(x_test, return_std=True)
    return mean_prediction, std_prediction

def train_xgboost_model(x_train, y_train):
    params = {'colsample_bytree': 0.8, 'gamma': 0.2, 'max_depth': 9, 'min_child_weight': 1, 'n_estimators': 30, 'subsample': 0.9}
    xgb_r = XGBRegressor(objective='reg:squarederror', seed=42, **params)
    xgb_r.fit(x_train, y_train, verbose=False)
    return xgb_r

def xgboost_predict(model, x_test):
    xg_preds = model.predict(x_test)
    return xg_preds

def train_random_forest_model(x_train, y_train):
    params = {'max_depth': 20, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 15}
    rf = RandomForestRegressor(random_state=42, **params)
    rf.fit(x_train, y_train)
    return rf

def random_forest_predict(model, x_test):
    rf_preds = model.predict(x_test)
    return rf_preds