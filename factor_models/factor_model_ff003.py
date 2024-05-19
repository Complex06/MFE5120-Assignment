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
成交额波动系数
mean(最近K个月日度成交额序列)/std(最近K个月日度成交额序列)

'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.k = cfg['params'].get('k',1)

        '''
        load data
        '''
        self.amount_df = self.dataloader.load_dailydata('amount')


        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        # 获取k月前的日期
        date_k_month = self.trading_dates[date_idx - self.k * 20]
        # 获取k月内的amount数据
        amount_k_month_df = self.amount_df.loc[date_k_month:date_now]
        # 计算k月内的成交额波动系数
        factor_thisday = amount_k_month_df.mean()/amount_k_month_df.std()
        
        factor_thisday = factor_thisday.replace([np.inf,-np.inf],np.nan)
        return factor_thisday


