"""

Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""
import json
from unittest import TestCase
from BagelBacktest.strategy import BuyAndHoldStrategy
from BagelBacktest.feeder import BagelDatabaseFeeder
from datetime import datetime


class TestBuyAndHoldStrategy(TestCase):

    def setUp(self):
        """
        setup data for tests
        """
        with open('Tests/test_db_config.json') as f:
            db_config = json.load(f)
        feeder = BagelDatabaseFeeder(**db_config,
                                     codes=['000001.SZ', '000002.SZ'],
                                     start_date=datetime(2023, 1, 1),
                                     end_date=datetime(2024, 1, 1))

        self.price, self.adj_price = feeder.feed()

        # strategy
        self.strategy = BuyAndHoldStrategy()

    def test_generate_signal(self):
        signal = self.strategy.generate_signal(self.adj_price)
        print(signal)
