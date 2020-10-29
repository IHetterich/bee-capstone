import argparse
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import geopandas as geo
from data_handler import DataHandler
plt.style.use('ggplot')

def geo_plot_cols(df_in, year, save_file):
    '''
    Plots the number of colonies in every state for the year indicated on a map of the US.
    It then saves the plot in the images folder with name numcols_{year}_map.png.

    Parameters
    ----------
    df_in - The dataframe our data is being pulled from for the plot.
    
    year - The year in question for plotting.

    Returns
    ----------
    None
    '''
    df = df_in[df_in['year'] == year].copy()
    df = df[df['state'] != 'HI']
    fig = df.plot(column='numcol', figsize=(13,13), legend=True, scheme='user_defined',\
         cmap='Reds', classification_kwds={'bins':[10000, 30000, 50000, 100000, 150000, 200000]})
    leg = fig.get_legend()
    leg._loc = 4
    fig.set_title(f'Number of Hives by State in {year}', fontsize=20)
    for lbl in leg.get_texts():
        label_text = lbl.get_text()
        lower = label_text.split()[0]
        upper = label_text.split()[2]
        new_text = f'{float(lower):,.0f} - {float(upper):,.0f}'
        lbl.set_text(new_text)
    plt.tick_params(                
        bottom=False,      
        left=False,         
        labelbottom=False,
        labelleft=False)

    plt.savefig(save_file)

def plot_avg_col(df, save_file):
    '''
    Plots and saves the average number of colonies over our window of time.

    Parameters
    ----------
    df - The dataframe containing our data for plotting.
    '''
    avgs = df.groupby('year').mean()

    fig, ax = plt.subplots()
    ax.plot(avgs['numcol'], linewidth=3)
    ax.set_ylim(0,75000)
    ax.set_ylabel('Average Number of Colonies', fontsize=15)
    ax.set_xlabel('Year', fontsize=15)
    ax.set_title('Average Number of Colonies per State', fontsize=20)
    plt.tight_layout()
    plt.savefig(save_file)

def avg_vs_large(df, save_file):
    '''
    Plots the national average against the colony numbers for ND, CA, SD.

    Parameters
    ----------
    df - The dataframe we're pulling our graphing data from.
    '''

    avgs = df.groupby('year').mean().reset_index()
    nd = df[df['state'] == 'ND']
    ca = df[df['state'] == 'CA']
    sd = df[df['state'] == 'SD']
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(nd['year'], nd['numcol'], label='North Dakota', color='b', linewidth=2)
    ax.plot(ca['year'], ca['numcol'], label='California', color='k', linewidth=2)
    ax.plot(sd['year'], sd['numcol'], label='South Dakota', color='m', linewidth=2)
    ax.plot(avgs['year'], avgs['numcol'], label='National Average', color='r', linewidth=2)
    ax.set_ylim(0,540000)
    ax.set_title('National Average and Outlier States', fontsize=20)
    ax.set_xlabel('Years', fontsize=15)
    ax.set_ylabel('Number of Colonies')
    ax.legend()
    plt.savefig(save_file)

def graph_p_trend(save_file):
    '''
    Graphs the p-values over a given number of years. Needs updating to 
    allow for input when called.
    '''

    p = [0.8484881181188515, 0.6774445778008072, 0.8742513963611638, 0.7554420590236682, 0.5784368740046202, 0.46686840125275564, 0.5256868182957398, 0.3941496099894497, 0.4993195517295863, 0.4217370653718848, 0.4033256486903477]
    years = list(range(2009,2020))
    fig, ax = plt.subplots()
    ax.plot(years, p, linewidth=2)
    ax.set_title('p-Values Over Time', fontsize=20)
    ax.set_xlabel('Years', fontsize=15)
    ax.set_ylabel('p-Values', fontsize=15)
    plt.savefig(save_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graphing functions')
    parser.add_argument('-d', '--data', type=str,
        default='/Users/ianhetterich/Desktop/Galvanize/capstones/bee-capstone/data/complete_data.csv', 
        help='The raw data file path')
    parser.add_argument('-g', '--graph', type=str, 
        help='The final graph file path')
    parser.add_argument('-y', '--year', type=int, default=2008, 
        help='The year in question if applicable')
    args = parser.parse_args()
    source_path = args.data
    save_path = args.graph
    year = args.year

    data = DataHandler(source_path).geo

    #To Do: Add in an additional argument and a conditional gate to 
    # specify functionality

    geo_plot_cols(data, year, save_path)
    