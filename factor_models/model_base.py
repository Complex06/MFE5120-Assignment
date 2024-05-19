import pandas as pd
import numpy as np
import os






class DataLoader():
    def __init__(self,data_dir:str):
        self.root_data_dir = data_dir
        self.daily_data_dir = os.path.join(self.root_data_dir,'daily_data')
        self.minute_data_dir = os.path.join(self.root_data_dir,'minute_data')

        self.event_data_dir = os.path.join(self.root_data_dir,'event_data')

    def load_dailydata(self,data_name:str) -> pd.DataFrame():
        data = pd.read_pickle(f'{os.path.join(self.daily_data_dir,data_name)}.pkl')
        data.index = pd.to_datetime(data.index)
        return data

    def load_minutedata(self,data_name:str,date:str) -> pd.DataFrame():
        data = pd.read_pickle(f'{os.path.join(os.path.join(self.minute_data_dir,date),data_name)}.pkl')
        data.index = pd.to_datetime(data.index)
        return data

    def load_eventdata(self,data_name:str) -> pd.DataFrame():
        data = pd.read_pickle(f'{os.path.join(self.event_data_dir, data_name)}.pkl')
        return data

class FactorModelBase():
    def __init__(self,cfg):
        self.univ = list(
            map(
                lambda x:x.strip(),
                open(os.path.join(cfg['meta_dir'],'universe.txt')).readlines()
            )
        )

        self.trading_dates = list(
            map(
                lambda x:x.strip(),
                open(os.path.join(cfg['meta_dir'],'trading_dates.txt')).readlines()
            )
        )

        self.dataloader = DataLoader(cfg['data_dir'])
        self.daily_factors = pd.Series(index=self.univ,dtype=np.float32)

    def daily_handler(self,date_idx:int) -> pd.Series:
        return self.daily_factors



