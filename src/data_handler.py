import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import geopandas as geo

class DataHandler(object):

    def __init__(self, filepath):
        self.full = pd.read_csv(filepath)
        self.trim = self.trim_data(self.full)
        self.stat = self.trim_large(self.trim)
        self.geo = self.geo_data(self.full)
    
    def trim_data(self, df):
        '''
        Trims down full data to just states that have data points for all years.

        Parameters
        ----------
        df - A dataframe with all states represented.

        Returns
        ----------
        A dataframe that has had several specific states eliminated.
        '''

        removal_states = ['MD', 'NM', 'NV', 'OK', 'SC']
        return df[~df.state.isin(removal_states)]

    def trim_large(self,df):
        '''
        Removes the 3 outlier states of ND, CA, and SD.

        Parameters
        ----------
        df - A dataframe still contianing the outlier states

        Returns
        ----------
        A dataframe with the specified states removed.
        '''

        removal_states = ['ND', 'CA', 'SD']
        return df[~df.state.isin(removal_states)]

    def geo_data(self,df):
        '''
        Adds in spacial data for geoplotting. Adds on a state by state basis.

        Parameters
        ----------
        df - A dataframe in need of geospacial data for plotting.

        Returns
        ----------
        df_geo - A dataframe with a geometry column containing plotting info.
        '''
        df = self.trim_data(df)

        geodata = geo.read_file('/Users/ianhetterich/Desktop/Galvanize/capstones/bee-capstone/data/usa-states-census-2014.shp')
        cut_geo = geodata[['STUSPS', 'geometry']].copy()
        cut_geo.rename(columns={'STUSPS':'state'}, inplace=True)

        #A right merge is done to maintain geoframe datatype  
        df_geo = cut_geo.merge(df, how='right', on='state')

        return df_geo