"""
Unit tests for feeder.py

Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com

"""
import json
from unittest import TestCase
from BagelBacktest.feeder import BagelDatabaseFeeder
from datetime import datetime


class TestFeeder(TestCase):
    pass


class TestDataFrameFeeder(TestCase):
    pass


class TestBagelDatabaseFeeder(TestCase):

    def setUp(self) -> None:
        """
        Set up database

        The database config store at Tests/test_db_config.json
        *DO NOT INCLUDED IN GIT REPOSITORY*
        """
        # setup database
        with open('Tests/test_db_config.json', 'r') as config_file:
            db_config = json.load(config_file)

        self.db_feeder = BagelDatabaseFeeder(**db_config)

        # setup date range
        start_date = datetime(2020, 1, 11)
        end_date = datetime(2020, 12, 31)
        self.date_range = (start_date, end_date)

    def test_no_data(self) -> None:
        with self.assertRaises(ValueError):
            self.db_feeder.feed()

    def test_pv_data(self) -> None:
        self.db_feeder.query_pv(
            codes=['000001.SZ', '000002.SZ', '000003.SZ', '000004.SZ', '000005.SZ'],
            account='close',
            table_name='daily',
            date_range=self.date_range
        )
        data = self.db_feeder.feed()
        print(data)
