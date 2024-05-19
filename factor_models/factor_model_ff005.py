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
隔夜跳空
absRet_night = -1* Σ_n abs(ln(open_t/close_t-1))

默认：n=20


'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',20)

        '''
        load data
        '''
        self.open_df = self.dataloader.load_dailydata('open_adj')
        self.pre_close_df = self.dataloader.load_dailydata('close_adj').shift(1)
        self.abs_night_ret_df = np.log(self.open_df / self.pre_close_df).abs()


        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        # 获取n日前的日期
        date_n = self.trading_dates[date_idx - self.n]
        # 获取n日内的absRet_night数据
        abs_night_ret_n_df = self.abs_night_ret_df.loc[date_n:date_now]
        # 计算n日内的隔夜跳空
        factor_thisday = -abs_night_ret_n_df.sum(axis=0,skipna=True)

  
        return factor_thisday


