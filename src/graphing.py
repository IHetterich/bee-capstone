import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import geopandas as geo
plt.style.use('ggplot')

def get_data():
    '''
    Pulls data from the data directory and formats it into a fully usable form for graphing.
    Particularly for geoplots.

    Parameters
    ----------
    None - Some to follow when pipelining this functionality.

    Returns
    ----------
    df_geo - Our full dataset with added geometry information for geoplotting
    '''

    full = pd.read_csv('../data/full.csv')
    low_states = ['MD', 'NM', 'NV', 'OK', 'SC']
    df = full[~full.state.isin(low_states)]
    geodata = geo.read_file('../data/usa-states-census-2014.shp')
    cut_geo = geodata[['STUSPS', 'geometry']].copy()
    cut_geo.rename(columns={'STUSPS':'state'}, inplace=True)   
    df_geo = cut_geo.merge(df, how='right', on='state')
    return df_geo

def geo_plot_cols(df_in, year):
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

    plt.savefig(f'../images/numcols_{year}_map.png')

def plot_avg_col(df):
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
    plt.savefig('../images/avg_cols.png')

def avg_vs_large(df):
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
    plt.savefig('../images/avg_vs_large.png')

def plot_bootstrapping():
    mean = 36808.207
    std = 6238.71
    model = stats.norm(loc=mean, scale = std)
    alt = 45574.8
    alpha = model.ppf(.95)
    x_range = np.linspace(mean - 4*std, mean + 4*std, 250)
    fig, ax = plt.subplots()
    ax.plot(x_range, model.pdf(x_range), label='Model of 2008 distribution')
    ax.fill_between(x_range, model.pdf(x_range), where=(x_range>alpha), alpha=.2, label='alpha = .05')
    ax.axvline(alt, linestyle='--', color='b', label='Bootstrap Estimate of 2019')
    ax.set_xlabel('Average Number of Hives', fontsize=15)
    ax.set_ylabel('Likelihood', fontsize=15)
    ax.set_title('Bootstrapping Model and Result')
    ax.legend(loc=2)
    plt.savefig('../images/bootstrap.png')

def graph_p_trend():
    p = [0.8484881181188515, 0.6774445778008072, 0.8742513963611638, 0.7554420590236682, 0.5784368740046202, 0.46686840125275564, 0.5256868182957398, 0.3941496099894497, 0.4993195517295863, 0.4217370653718848, 0.4033256486903477]
    years = list(range(2009,2020))
    fig, ax = plt.subplots()
    ax.plot(years, p, linewidth=2)
    ax.set_title('p-Values Over Time', fontsize=20)
    ax.set_xlabel('Years', fontsize=15)
    ax.set_ylabel('p-Values', fontsize=15)
    plt.savefig('../images/p_value_trend.png')


if __name__ == '__main__':
    df = get_data()
    graph_p_trend()