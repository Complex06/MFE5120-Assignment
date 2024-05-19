import sys
sys.path.append(r"D:\python\vscode\Strategies\多因子\code_and_data\code\factor_cal_and_eval\framework\common")
import pandas as pd
import numpy as np
import logging

from quant_funcs import sma
from model_base import FactorModelBase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


'''
技术因子
ROC=(CLOSE-CLOSE[N])/CLOSE[N]
ROCMA =SMA(ROC,M)
因子值=ROCMA-ROC(反转)

需要进行close中性化处理
默认：N=12、M=6

'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',12)
        self.m = cfg['params'].get('m',6)

        '''
        load data
        '''
        self.close_df = self.dataloader.load_dailydata('close_adj')

        self.close_n_df = self.close_df.shift(self.n)
        self.ROC_df = (self.close_df - self.close_n_df) / self.close_n_df
        self.ROCMA_df = sma(self.ROC_df, self.m)

        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期
        date_now = self.trading_dates[date_idx]
        
        factor_thisday = self.ROCMA_df.loc[date_now] - self.ROC_df.loc[date_now]
        factor_thisday = factor_thisday.replace([np.inf,-np.inf],np.nan)
        return factor_thisday









