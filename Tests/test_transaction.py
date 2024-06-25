"""
Tests for the Transaction class.

Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import json

from unittest import TestCase
from datetime import datetime

from BagelBacktest.transactions import Transactions
from BagelBacktest.feeder import BagelDatabaseFeeder


class TestTransactions(TestCase):

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

    def test_add_transaction(self):
        # set up transactions
        transactions = Transactions()
        transactions.add_transaction(datetime(2023, 1, 3),
                                     '000001.SZ',
                                     100)
        print(transactions)

    def test_generate_signal(self):
        # set up transactions
        transactions = Transactions()
        transactions.add_transaction(datetime(2023, 1, 3),
                                     '000001.SZ',
                                     100)
        signal = transactions.generate_signal(self.adj_price)
        print(signal)

    def test_generate_signal_no_transactions(self):
        # set up transactions
        transactions = Transactions()
        signal = transactions.generate_signal(self.adj_price)
        print(signal)

    def test_generate_signal_outside_date_range(self):
        # set up transactions
        transactions = Transactions()
        transactions.add_transaction(datetime(2023, 1, 1),
                                     '000001.SZ',
                                     100)
        self.assertRaises(ValueError, transactions.generate_signal, self.adj_price)

    def test_generate_signal_invalid_code(self):
        # set up transactions
        transactions = Transactions()
        transactions.add_transaction(datetime(2023, 1, 3),
                                     'test_code',
                                     100)
        self.assertRaises(ValueError, transactions.generate_signal, self.adj_price)
