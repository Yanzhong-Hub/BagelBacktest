"""
Feeder
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd

from datetime import datetime

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from sqlalchemy import create_engine, Engine


@dataclass(slots=True)
class Feeder(ABC):
    """Feeder base class"""

    _price: pd.DataFrame = field(init=False)
    _adj_price: pd.DataFrame = field(init=False)

    def feed(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        feed price and adjust_price after valid data
        :return: (price, adjust_price)
        """
        self._valid_data()
        return self._price, self._adj_price

    def _valid_data(self) -> pd.DataFrame:
        """Validate data before feeding"""
        pass

    @abstractmethod
    def _load_data(self) -> None:
        """
        load data to self.price and self.adjust_price
        all subclass should implement this method
        """
        ...

    def __post_init__(self):
        self._load_data()


@dataclass(slots=True)
class DataFrameFeeder(Feeder):

    price: pd.DataFrame
    adjust_price: pd.DataFrame

    def _load_data(self) -> None:
        self._price = self.price
        self._adj_price = self.adjust_price


@dataclass(slots=True)
class BagelDatabaseFeeder(Feeder):
    """Mysql connectionl, please refer to TushareDownloader"""

    host: str
    port: int
    user: str
    password: str
    database: str

    codes: Iterable[str]
    start_date: datetime
    end_date: datetime

    def _load_data(self) -> None:
        engine = self._get_engine()
        self._price = self._query_price(engine)
        self._adj_price = self._query_adj_price(engine, self._price)

    def _get_engine(self) -> Engine:
        """get sqlalchemy engine"""
        return create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        )

    def _query_price(self, engine: Engine) -> pd.DataFrame:
        """query price"""
        sql = f"""
        SELECT trade_date, close, ts_code FROM daily 
        WHERE ts_code IN {tuple(self.codes)} 
        AND trade_date BETWEEN '{self.start_date.strftime("%Y%m%d")}' AND '{self.end_date.strftime("%Y%m%d")}'
        """
        price = pd.read_sql(sql, engine, parse_dates=['trade_date'])
        price = price.pivot(index='trade_date', columns='ts_code', values='close')
        return price.sort_index()

    def _query_adj_price(self, engine: Engine, price: pd.DataFrame) -> pd.DataFrame:
        """query adjust_price"""
        sql = f"""
        SELECT trade_date, adj_factor, ts_code FROM adj_factor 
        WHERE ts_code IN {tuple(self.codes)} 
        AND trade_date BETWEEN '{self.start_date.strftime("%Y%m%d")}' AND '{self.end_date.strftime("%Y%m%d")}'
        """
        adj_factor = pd.read_sql(sql, engine, parse_dates=['trade_date'])
        adj_factor = adj_factor.pivot(index='trade_date', columns='ts_code', values='adj_factor').sort_index()
        return price * adj_factor
