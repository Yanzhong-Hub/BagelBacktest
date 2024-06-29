"""

Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import json
import matplotlib.pyplot as plt

from unittest import TestCase
from datetime import datetime

from BagelBacktest.feeder import BagelDatabaseFeeder
from BagelBacktest.core import Core


class TestCore(TestCase):
    def setUp(self):
        """
        setup data for tests
        """
        with open('Tests/test_db_config.json') as f:
            db_config = json.load(f)

        with open('Tests/tushare_stock_basic.csv') as f:
            codes = f.read().splitlines()[1:]

        self.feeder = BagelDatabaseFeeder(**db_config,
                                          codes=codes,
                                          start_date=datetime(2023, 1, 1),
                                          end_date=datetime(2024, 1, 1))
        self.feeder.set_cache('Tests/cached/main_board_price.csv',
                              'Tests/cached/main_board_adj_price.csv')

    def test_add_transaction(self):
        core = Core()
        core.add_feeder(self.feeder)
        core.add_transaction(datetime(2023, 1, 4),
                             '000001.SZ',
                             10000)
        portfolio = core.run()
        print(portfolio)

    def test_run(self):
        core = Core()
        core.add_feeder(self.feeder)
        portfolio = core.run()

        print(portfolio.values)
