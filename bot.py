import os
import qlib
import yaml
import pandas as pd
from datetime import datetime
from datetime import timedelta
from qlib.contrib.strategy import TopkDropoutStrategy
from qlib.utils import init_instance_by_config
from qlib.workflow import R
from qlib.utils.time import Freq
from qlib.backtest import backtest
from typing import Dict


class MarketBot:
    
    def __init__(self, path_to_csvs: str, path_to_bins: str):
        
        self.config = {}
        self.model = None
        self.start_account = 100000
        self.path_to_bins = path_to_bins
        self.path_to_csvs = path_to_csvs
        qlib.init(provider_uri=path_to_bins)
    
    def load_model(self, path_to_model: str):
        
        self.model = R.load_object(path_to_model)
        
    def get_states(self, dataframes: Dict, k=15):
        
        t = self.aggregate_dataframe(list(dataframes.values())[0], k=k)['date'].sort_values().astype(str).values
        end_date, start_date = t[-k - 1], t[0]
        
        for ticker in dataframes:
            self.aggregate_dataframe(dataframes[ticker], k=k).to_csv(f'{self.path_to_csvs}/{ticker}.csv', index=False)
        
        command = f'python qlib/scripts/dump_bin.py dump_all --csv_path {self.path_to_csvs} --qlib_dir {self.path_to_bins}'
        ret = os.system(command)

        if ret != 0:
            raise ValueError('???')
        
        self.generate_config(start_date, end_date)
        dataset = init_instance_by_config(task['dataset'])
        predictions = self.model.predict(dataset)
        
        strategy_obj = TopkDropoutStrategy(**self.generate_strategy(predictions))
        executor_obj = init_instance_by_config(self.config['executor_config'])

        portfolio_metric_dict, indicator_dict = backtest(
            executor=executor_obj,
            strategy=strategy_obj,
            **self.config['backtest_config']
        )
        analysis_freq = "{0}{1}".format(*Freq.parse('day'))
        _, positions_normal = portfolio_metric_dict.get(analysis_freq)
        
        return positions_normal
        
    def generate_config(self, start_date, end_date):
        
        self.config['dataset'] = {'class': 'DatasetH',
         'module_path': 'qlib.data.dataset',
         'kwargs': {'handler': {'class': 'Alpha360',
           'module_path': 'qlib.contrib.data.handler',
           'kwargs': {'start_time': a,
            'end_time': b,
                      'fit_start_time': a,
                      'fit_end_time': b,
            'instruments': 'all',
            'infer_processors': [{'class': 'RobustZScoreNorm',
              'kwargs': {'fields_group': 'feature', 'clip_outlier': True}},
             {'class': 'Fillna', 'kwargs': {'fields_group': 'feature'}}],
            'learn_processors': [{'class': 'DropnaLabel'},
             {'class': 'CSRankNorm', 'kwargs': {'fields_group': 'label'}}],
            'label': ['Ref($close, -2) / Ref($close, -1) - 1']}},
          'segments': {'test': (a, b)}}}

        self.config['executor_config'] = {
            "class": "SimulatorExecutor",
            "module_path": "qlib.backtest.executor",
            "kwargs": {
                "time_per_step": "day",
                "generate_portfolio_metrics": True,
                "verbose": False,
            }
        }
        
        self.config['backtest_config'] = {
            "start_time": start_date,
            "end_time": end_date,
            "account": self.start_account,
            "benchmark": 'YNDX',
            "exchange_kwargs": {
                "freq": 'day',
                "limit_threshold": 0.095,
                "deal_price": "close",
                "open_cost": 0.0005,
                "close_cost": 0.0015,
                "min_cost": 50,
            }
        }
        
    def generate_strategy(self, predicted):
        
        return {
            "topk": 8,
            "n_drop": 2,
            "signal": predicted
        }
    
    def aggregate_dataframe(self, dataframe, k):
        
        df = pd.concat((dataframe, dataframe.iloc[-k:]))
        df.iloc[-k:, 0] = pd.to_datetime(df.iloc[-2 * k: -k, 0] + timedelta(days=1))
        
        return df