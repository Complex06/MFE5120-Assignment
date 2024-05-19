import sys
sys.path.append(r"D:\python\vscode\Strategies\多因子\code_and_data\code\factor_cal_and_eval\framework\common")
import pandas as pd
import numpy as np
import logging

from quant_funcs import ts_argmax, stddev
from model_base import FactorModelBase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


'''
Alpha001
(rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5)

因子值取负号(从动量到反转)
(rank(-1*Ts_ArgMin(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5)

'''


class FactorModel(FactorModelBase):
    def __init__(self,cfg):
        super().__init__(cfg)

        '''
        get params set in config_factor_xxx.py
        '''
        self.n = cfg['params'].get('n',20)
        self.k = cfg['params'].get('k',5)

        '''
        load data
        '''
        self.close_df = self.dataloader.load_dailydata('close_adj')
        self.returns_df = self.dataloader.load_dailydata('returns_adj')

        logger.info(f"{cfg['factor_id']} done with initialization")

    def daily_handler(self,date_idx) -> pd.Series:
        # 获取当前日期和n+k天前的日期
        date_now = self.trading_dates[date_idx]
        date_n_k = self.trading_dates[date_idx-self.n-self.k]

        # 获取k+n天前到现在的收盘价和回报率
        tmp_close_df = self.close_df.loc[date_n_k:date_now]
        tmp_returns_df = self.returns_df.loc[date_n_k:date_now]

        # 计算stddev(returns, self.n)
        factor_stddev = stddev(tmp_returns_df, self.n)

        # 如果returns < 0, 则取stddev(returns, self.n), 否则取close
        inner = pd.DataFrame(np.where(tmp_returns_df < 0, factor_stddev, tmp_close_df), 
                             index=tmp_returns_df.index, columns=tmp_returns_df.columns)

        # 计算SignedPower
        inner = inner.pow(2)

        # 计算Ts_ArgMax并取最后一行
        factor_thisday = -ts_argmax(inner, self.k).iloc[-1]

        # 计算rank并减去0.5
        factor_thisday = factor_thisday.rank(pct=True) - 0.5

        # 处理inf
        factor_thisday = factor_thisday.replace([np.inf,-np.inf],np.nan)

        return factor_thisday









