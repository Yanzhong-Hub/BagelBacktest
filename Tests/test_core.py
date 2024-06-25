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
        self.feeder = BagelDatabaseFeeder(**db_config,
                                          codes=['000001.SZ', '000002.SZ'],
                                          start_date=datetime(2023, 1, 1),
                                          end_date=datetime(2024, 1, 1))

    def test_add_transaction(self):
        core = Core(self.feeder)
        core.add_transaction(datetime(2023, 1, 4),
                             '000001.SZ',
                             10000)
        portfolio = core.run()
        print(portfolio)

    def test_run(self):
        core = Core(self.feeder)
        portfolio = core.run()
        portfolio.values.plot()
        plt.show()
