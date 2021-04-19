import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import plot_partial_dependence
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from data_handler import DataHandler

plt.rc('font', size=12)

def linear_testing(data):
    '''
    An early attempt using linear regression for inferential modeling.

    Parameters
    ----------
    data - The dataset to be used for fitting the model.

    Returns
    ----------
    None
    '''
    X = data[['numcol', 'yieldpercol', 'stocks']]
    y = data['priceperlb']
    
    scalar = StandardScaler()
    new_X = pd.DataFrame(scalar.fit_transform(X), columns=X.columns)
    # print(new_X.head())

    model = LinearRegression()
    model.fit(new_X, y)
    
    print(model.coef_)

def production_plotting(model, X, axes):
    '''
    Takes in a model for inferential modeling and makes partial dependence
    plots for the two production metrics (num cols, and yield per col).

    Parameters
    ----------
    model - The instantiated and fit model to be used for plotting.
    X - The data that is used to creat the grid of values to cycle through for
        partial dependence.
    
    Returns
    ----------
    None
    '''
    plot_partial_dependence(estimator=model, X=X, features=[0,1], ax=axes)
    axes[0].set_xlabel('Number of Colonies (in Thousands)', fontsize=15)
    axes[0].set_ylabel('Partial Dependence', fontsize=15)
    axes[0].set_xticks([0, 50000, 100000, 150000, 200000, 250000])
    axes[0].set_xticklabels(['0', '50', '100', '150', '200', '250'])
    axes[0].set_title('Colonies per State', fontsize=20)
    axes[1].set_xlabel('Yield per Colony (in Lbs)', fontsize=15)
    axes[1].set_ylabel('Partial Dependence', fontsize=15)
    axes[1].set_xticks([40, 80, 120])
    axes[1].set_xticklabels(['40', '80', '120'])
    axes[1].set_title('Production per Colony', fontsize=20)

def stocks_plotting(model, X, ax):
    plot_partial_dependence(estimator=model, X=X, features=[2], ax=ax)   
    plt.xlabel('Stocked Honey (in Millions of Lbs)', fontsize=15)
    plt.ylabel('Partial Dependence', fontsize=15)
    plt.title('Stocks of Honey per State', fontsize=20)


if __name__ == '__main__':
    handler = DataHandler('data/complete_data.csv')
    # print('test')
    X, y = handler.inferential

    model = RandomForestRegressor(oob_score=True)
    model.fit(X, y)
    print(model.feature_importances_)

    plot = 'stocks'

    if plot == 'prod':
        fig, axes = plt.subplots(1, 2)
        production_plotting(model, X, axes)
        plt.tight_layout()
        plt.show()

    if plot == 'stocks':        
        fig, ax = plt.subplots()
        stocks_plotting(model, X, ax)
        plt.tight_layout()
        plt.show()
