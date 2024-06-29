"""
Unit tests for feeder.py

Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import json
import pandas as pd
from unittest import TestCase
from datetime import datetime

from BagelBacktest.feeder import BagelDatabaseFeeder, DataFrameFeeder


class TestDataFrameFeeder(TestCase):

    def setUp(self):
        """
        setup test_price and test_adj_price dataframe
        """
        self.test_price = pd.DataFrame({'000001.SZ': [1, 2]},
                                       index=[pd.date_range(start='20240101', periods=2)])
        self.test_adj_price = pd.DataFrame({'000001.SZ': [3, 4]},
                                           index=[pd.date_range(start='20240101', periods=2)])

    def test_DataFrameFeeder(self):
        df_feeder = DataFrameFeeder(self.test_price, self.test_adj_price)
        price, adjusted_price = df_feeder.feed()
        print(price, adjusted_price)


class TestBagelDatabaseFeeder(TestCase):

    def setUp(self) -> None:
        """
        Set up database

        The database config store at Tests/test_db_config.json
        *DO NOT INCLUDED IN GIT REPOSITORY*

        Sample test_db_config.json
        {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "<YOUR_PASSWORD_HERE>",
            "database": "tushare"
        }
        """
        # setup date range
        start_date = datetime(2020, 1, 11)
        end_date = datetime(2020, 12, 31)
        codes = ['000001.SZ', '000002.SZ']
        # setup database
        with open('Tests/test_db_config.json', 'r') as config_file:
            db_config = json.load(config_file)

        self.db_feeder = BagelDatabaseFeeder(**db_config,
                                             codes=codes,
                                             start_date=start_date,
                                             end_date=end_date)

    def test_pv_data(self) -> None:
        price, adj_price = self.db_feeder.feed()
        print(f'price: {price}, adj_price: {adj_price}')

    def test_cache_feeder(self) -> None:
        start_date = datetime(2000, 1, 11)
        end_date = datetime(2023, 12, 31)
        with open('Tests/test_db_config.json', 'r') as config_file:
            db_config = json.load(config_file)
        with open('Tests/tushare_stock_basic.csv', 'r') as f:
            codes = f.read().splitlines()[1:]
        feeder = BagelDatabaseFeeder(**db_config,
                                     codes=codes,
                                     start_date=start_date,
                                     end_date=end_date)
        feeder.set_cache('Tests/cached/main_board_price.csv',
                         'Tests/cached/main_board_adj_price.csv')
        price, adj_price = feeder.feed()
        print(f'price: {price}, adj_price: {adj_price}')
