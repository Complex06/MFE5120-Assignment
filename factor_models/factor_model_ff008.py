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
对数总市值
In(当日收盘价*当日总股本)
alpha *= -1


'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''

        '''
        load data
        '''
        self.mkt_val_df = self.dataloader.load_dailydata('S_VAL_MV')
        self.ln_mkt_val_df = np.log(self.mkt_val_df)



        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        factor_thisday = -self.ln_mkt_val_df.loc[date_now]

        return factor_thisday


