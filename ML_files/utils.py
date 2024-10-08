import numpy as np

import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import metrics



def log_transform(x):
    """
    Log transform the input x
    
    Parameters
    ----------
    x : float
        input value
        
    Returns
    -------
    float: log transformed value
    """
    return np.log1p(x)

def inverse_log_transform(x):
    """
    Inverse log transform the input x

    Parameters
    ----------
    x : float
        input value
    
    Returns
    -------
    float: inverse log transformed value
    """
    return np.expm1(x)

def get_metrics(y_test, prediction):
    test_mse = round(metrics.mean_squared_error(y_test, prediction), 2)
    test_mae = round(metrics.mean_absolute_error(y_test, prediction), 2)
    test_rmse = round(metrics.mean_squared_error(y_test, prediction, squared=False), 2)
    test_mape = round(metrics.mean_absolute_percentage_error(y_test, prediction), 2)
    test_r2 = round(metrics.r2_score(y_test, prediction), 2)
    print(f'MSE : {round(metrics.mean_squared_error(y_test, prediction), 2)}')
    print(f'MAE :  {round(metrics.mean_absolute_error(y_test, prediction), 2)}')
    print(f'RMSE : {round(metrics.mean_squared_error(y_test, prediction, squared=False), 2)}')
    print(f'MAPE : {round(metrics.mean_absolute_percentage_error(y_test, prediction), 2)}')
    print(f'R2 : {round(metrics.r2_score(y_test, prediction), 2)}')
    return {'mse': test_mse, 'mae': test_mae, 'rmse': test_rmse, 'mape': test_mape, 'r2': test_r2}

def plot_ystats(Y, x_text_pos, y_text_pos, text_str):
    """
    Plot the histogram of the log transformed Y and display the statistics

    Parameters
    ----------
    Y : pd.DataFrame
        DataFrame containing the target variable
    x_text_pos : float
        x position of the text
    y_text_pos : float
        y position of the text
    text_str : str
        text to display

    Returns
    -------
    None
    """
    Y['y_log'].describe()
    mean = Y['y_log'].mean()
    std = Y['y_log'].std()
    max = Y['y_log'].max()
    min = Y['y_log'].min()
    count = Y['y_log'].count()
    text_str = f"Mean: {mean}\nSTD: {std}\nMax: {max}\nMin: {min}\nCount: {count}"
    sns.histplot(Y['y_log'])
    plt.text(x_text_pos, y_text_pos, text_str, fontsize=12, ha='center')