import numpy as np
import pandas as pd
import scipy.stats as stats

def restrict(df):
    '''
    Removes the information for states that do not have data for the full span of years, as well as outliers.

    Parameters
    ----------
    df - A Pandas Dataframe containing the full dataset.

    Returns
    ----------
    A Pandas Dataframe with 5 states removed.
    '''

    removal_states = ['MD', 'NM', 'NV', 'OK', 'SC', 'ND', 'CA', 'SD']
    return df[~df.state.isin(removal_states)]

def restrict_to_year_col(df, year, col):
    '''
    Restricts the input dataframe to the data of the given year and column and returns it
    as a Numpy ndarray.

    Parameters
    ----------
    df - A Pandas Dataframe with multiple years of data.
    
    year - An Int of the year in question to restrict the data to.

    col - A string of the column in question to restrict the data to.

    Returns
    ----------
    A Numpy ndarray with just the requested data.
    '''

    return df[df['year'] == year][col].to_numpy()

def bootstrap_mean(data, samples=10**6):
    '''
    Bootstraps a given sample to find an approximation of the mean of the population and 
    returns that mean and the standard deviation of that bootstrapped mean.

    Parameters
    ----------
    data - An ndarray of the sample we are bootstrapping.

    samples - The number of bootstraps to take, defaulted at 10,000.

    Returns
    ----------
    mean - The result of the bootstrapped mean.

    std - The standard deviation of the bootstrapped mean.
    '''

    bootstrap = []
    for i in range(samples):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrap.append(np.mean(sample))
    return np.mean(bootstrap), np.std(bootstrap)

def hypothesis_testing(df, null_year, test_year, col):
    '''
    Takes in a dataframe, a year for the null hypothesis, a year for an alternate hypothesis
    and a column to test in the data frame. Pulls relevant data from the dataframe and then 
    bootstraps a mean to contruct a normally distributed fit for generating a p-value. It then
    prints out the p-value that was found, as well as the mean and std from the bootstrapping.

    Parameters
    ----------
    df - A dataframe containing all the data in question.

    null_year - The year of data we are using to construct our null hypothesis.

    test_year - The year of data we are using to test out null hypothesis.

    col - The column of data fro the dataframe that we are testing.
    '''
    null_data = restrict_to_year_col(restrict(df), null_year, col)
    test_data = restrict_to_year_col(restrict(df), test_year, col)

    null_mean, null_std = bootstrap_mean(null_data)
    test_mean, test_std = bootstrap_mean(test_data)

    null_dist = stats.norm(loc=null_mean, scale = null_std)
    p = 1 - null_dist.cdf(test_mean)

    print(f'p-Value: {p}')
    print(f'Null hypothesis\nMean: {null_mean}\nSTD: {null_std}')
    print(f'Test Data\nMean: {test_mean}\nSTD: {test_std}')

if __name__ == '__main__':
    data = pd.read_csv('data/full.csv')
    hypothesis_testing(data, 2008, 2019, 'numcol')