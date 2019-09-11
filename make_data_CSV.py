import os
import glob
import gzip
import unzip
import pandas as pd

class MakeDataCSV:

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.df = pd.DataFrame()
        self.columns = ["STN","WBAN","YEAR","TEMP","COUNT","DEWP","COUNT","SLP","COUNT",
                   "STP","COUNT","VISIB","COUNT","WDSP","COUNT","MXSPD","GUST",
                   "MAX","MIN","PRCP","SNDP","FRSHTT"]

    def _make_list_directory(self):
        self.subdirectories = [f.name for f in os.scandir(self.dir_name) if f.is_dir()]

    def _make_list_files(self, subdir_name):
        path = self.dir_name + '/' + subdir_name
        file_list = glob.glob(path + '/*.gz')
        return file_list

    def create_csv(self):
        self._make_list_directory()

        for subdir in self.subdirectories:
            year = subdir.split('_')[1]
            os.mkdir(f'CSV/{year}')

            file_list = self._make_list205  _files(subdir)

            for file in file_list:
                with gzip.open(file) as f:
                    df = pd.read_csv(f, sep=r'\s+',skiprows=1)
                    df.columns = self.columns

                    station_name = f.name.split('-')[0].split('_')[3].replace('/', '-')
                    df.to_csv(f'CSV/{year}/{station_name}.csv', header=True, index=False)
            print(year, 'done.')
                    

unzipper = MakeDataCSV('gsod_all_years')
unzipper.create_csv()