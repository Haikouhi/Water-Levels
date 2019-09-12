import os
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import floor, ceil


class GetData:

    def __init__(self, start_year=1901, stop_year=2019, station=None):
        year_range = range(start_year, stop_year+1)

        dir_list = ([int(f.name) for f in os.scandir('./CSV') if int(f.name) in year_range])

        self.dir_list = sorted(dir_list)
        self.station = str(station)
        self.isd_history = pd.read_csv('isd-history.csv')
    
    def _csvs_to_df(self, year_dir):
        list_ddf = []
        if self.station == 'None':

            csv_list = glob.glob(f'CSV/{year_dir}/*.csv')
            for csv in csv_list:
                ddf = pd.read_csv(csv)
                list_ddf.append(ddf)
        else:
            csv = glob.glob(f'CSV/{year_dir}/*-{self.station}.csv')
            ddf = pd.read_csv(csv[0])
            list_ddf.append(ddf)
        
        return pd.concat(list_ddf)

    def get_data(self):
        list_df = []
        for d in self.dir_list:
            list_df.append(self._csvs_to_df(d))
        self.df = pd.concat(list_df)
        self._clean()
    
    def _clean(self):
        self.df['YEAR'] = pd.to_datetime(self.df['YEAR'], format='%Y%m%d')
        self.df['STN'] = self.df['STN'].astype(str)
        self._format_station()
        self.df = self.df.merge(right=self.isd_history, how='left', left_on='STN', right_on='USAF')
        self.df['MAX'] = self.df['MAX'].str.strip('*').astype(float)
        self.df['MIN'] = self.df['MIN'].str.strip('*').astype(float)
        self.df = self.df[self.df['MAX'] < 1000]

    def _format_station(self):
        stations = []
        for stn in self.df['STN'].values:
            if int(stn) < 100000:
                stations.append('0' + stn)
            else:
                stations.append(stn)
        
        self.df['STN'] = stations

    def mean_temp(self):
        station_name = self.df['STATION NAME'].unique()[0]

        ax = sns.lineplot(data=self.df, x='YEAR', y='TEMP').set_title(
            f'Mean temp of station {station_name}')
        plt.show()

    def max_temp(self):
        station_name = self.df['STATION NAME'].unique()[0]

        ax = sns.lineplot(data=self.df, x='YEAR', y='MAX').set_title(
            f'Max temp of station {station_name}')
        plt.show()
    
    def min_temp(self):
        station_name = self.df['STATION NAME'].unique()[0]

        ax = sns.lineplot(data=self.df, x='YEAR', y='MIN').set_title(
            f'Max temp of station {station_name}')
        plt.show()

    def count_mean_temp(self):
        station_name = self.df['STATION NAME'].unique()[0]
        mini = self.df['TEMP'].min()
        maxi = self.df['TEMP'].max()
        order = np.arange(mini, maxi, 1)

        ax = sns.countplot(data=self.df, x='TEMP', order=order,
        palette=sns.diverging_palette(240, 10, n=100)).set_title(
            f'Most measured mean temp of station {station_name}')

        plt.xticks(rotation=90, horizontalalignment='right')

        plt.show()
    
    def count_max_temp(self):
        station_name = self.df['STATION NAME'].unique()[0]
        mini = self.df['MAX'].min()
        maxi = self.df['MAX'].max()
        order = np.arange(mini, maxi, 1)

        ax = sns.countplot(data=self.df, x='MAX', order=order,
        palette=sns.diverging_palette(240, 10, n=100)).set_title(
            f'Most measured max temp of station {station_name}')

        plt.xticks(rotation=90, horizontalalignment='right')

        plt.show()
        
