import sys
sys.path.append(r"D:\python\vscode\Strategies\多因子\code_and_data\code\factor_cal_and_eval\framework\common")
import pandas as pd
import numpy as np
import logging

from model_base import FactorModelBase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


'''
理想振幅
近n日中股价最低的n*k天的平均振幅-股价最高的n*k天的平均振幅,k是比例，在0-1之间。


'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',20)
        self.k = cfg['params'].get('k',0.2)
        '''
        load data
        '''
        self.low_df = self.dataloader.load_dailydata('low_adj')
        self.high_df = self.dataloader.load_dailydata('high_adj')
        self.close_df = self.dataloader.load_dailydata('close_adj')
        
        self.amp_df = self.high_df / self.low_df - 1


        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        # 获取n天前的日期
        date_n = self.trading_dates[date_idx - self.n]

        tmp_close_df = self.close_df.loc[date_n:date_now]
        tmp_amp_df = self.amp_df.loc[date_n:date_now]

        tmp_rank_close_df = tmp_close_df.rank(axis=0,ascending=True,pct=True)

        top_tmp_amp_df = tmp_amp_df[tmp_rank_close_df>=1-self.k]
        bottom_tmp_amp_df = tmp_amp_df[tmp_rank_close_df<self.k]
        tmp_count = tmp_amp_df.count()
        
        factor_thisday_low = bottom_tmp_amp_df.mean().where(tmp_count>self.n*0.5)
        factor_thisday_high = top_tmp_amp_df.mean().where(tmp_count>self.n*0.5)
        factor_thisday = factor_thisday_low - factor_thisday_high

        return factor_thisday


