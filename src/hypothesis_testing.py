import argparse
from data_handler import DataHandler
import numpy as np
import pandas as pd
import scipy.stats as stats

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

def t_test(df, year1, year2):
    '''
    Takes in a dataframe and 2 years to test and returns the results 
    of a Students t-test.
    Parameters
    ----------
    df - The dataframe in question.

    year1 - One of the years to be tested.

    year2 - The other year to be tested.

    Returns
    ----------
    The results of the Student t-test, a tuple of t-statistic and p-value.
    '''

    a = restrict_to_year_col(df, year1, 'numcol')
    b = restrict_to_year_col(df, year2, 'numcol')
    return stats.ttest_ind(a,b, equal_var=False)[1]

def p_trend(df, start, end):
    '''
    Runs a t_test for the range of years input and returns a list of their p-values.

    Parameters
    ----------
    df - The dataframe we are pulling numbers from.

    start - The initial year we are comparing the other to.

    end - The final year to be tested.

    Returns
    ----------
    lst - A list of the p-values in the specified range.
    '''

    lst = []
    for year in range(start+1,end+1):
        lst.append(t_test(df, start, year))
    print(lst)
    return lst

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical functions')
    parser.add_argument('-d', '--data', type=str, 
        default='/Users/ianhetterich/Desktop/Galvanize/capstones/bee-capstone/data/complete_data.csv', 
        help='The raw data file path')
    parser.add_argument('-a', '--year_a', type=int, default=2008, 
        help='Lower year')
    parser.add_argument('-b', '--year_b', type=int, default=2008, 
        help='Higher year')
    args = parser.parse_args()
    source_path = args.data
    a_year = args.year_a
    b_year = args.year_b

    data = DataHandler(source_path).stat

    #To Do: Add in an additional argument and a conditional gate to 
    # specify graph

    p_trend(data, a_year, b_year)