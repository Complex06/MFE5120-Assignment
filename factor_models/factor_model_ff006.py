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
日内收益率
intraday_Ret = (close_t/open_t - 1)
alpah = intraday_Ret * -1


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
        self.open_df = self.dataloader.load_dailydata('open_adj')
        self.close_df = self.dataloader.load_dailydata('close_adj')
        self.intra_ret_df = self.close_df / self.open_df - 1


        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]

        # 获取当日的intraday_Ret
        factor_thisday = self.intra_ret_df.loc[date_now] * -1

  
        return factor_thisday


