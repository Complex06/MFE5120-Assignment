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
Alpha1

(-1 * CORR(RANK(DELTA(LOG(VOLUME), 1)), RANK(((CLOSE - OPEN) / OPEN)), 6))

'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',6)

        '''
        load data
        '''
        self.close_df = self.dataloader.load_dailydata('close_adj')
        self.open_df = self.dataloader.load_dailydata('open_adj')
        self.volume_df = self.dataloader.load_dailydata('volume')

        self.volume_df = self.volume_df.fillna(1e-6)
        self.delta_log_vol_df = np.log(self.volume_df) - np.log(self.volume_df).shift(1)
        self.rank1_df = self.delta_log_vol_df.rank(pct=True)

        self.rank2_df = ((self.close_df - self.open_df) / self.open_df).rank(pct=True)


        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期和n天前的日期
        date_now = self.trading_dates[date_idx]
        date_n = self.trading_dates[date_idx-self.n]

        # 获取n天内的数据
        tmp_rank1_df = self.rank1_df.loc[date_n:date_now]
        tmp_rank2_df = self.rank2_df.loc[date_n:date_now]

        # 计算corr
        factor_thisday = -1 * tmp_rank1_df.corrwith(tmp_rank2_df)

        # 处理inf
        factor_thisday = factor_thisday.replace([np.inf,-np.inf],np.nan)

        return factor_thisday









