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
技术因子
PSY =100*COUNT(CLOSE>CLOSE[1]),N)/N
默认:N=12

指标小于25 时关注做多机会，大于75 时关注做空机会，小于10为极度超卖，大于90为极度超买

'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',12)

        '''
        load data
        '''
        self.close_df = self.dataloader.load_dailydata('close_adj')
        self.pre_close_df = self.close_df.shift(1)

        self.delta_close_df = self.close_df - self.pre_close_df

        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        # 获取n天前的日期
        date_n = self.trading_dates[date_idx - self.n]
        # 获取n天内的delta_close数据
        delta_close_n_df = self.delta_close_df.loc[date_n:date_now]
        # 计算n天中delta_close大于0的天数并除以n
        factor_thisday = -delta_close_n_df[delta_close_n_df > 0].count()/self.n
        
        factor_thisday = factor_thisday.replace([np.inf,-np.inf],np.nan)
        return factor_thisday









