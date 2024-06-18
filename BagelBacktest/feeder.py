"""
Feeder
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from sqlalchemy import create_engine, Engine, text
from datetime import datetime
from typing import Iterable


class Feeder(ABC):
    """Feeder base class"""

    @abstractmethod
    def feed(self) -> pd.DataFrame:
        """Provide data to the BagelCore"""
        ...

    def data_validation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate data before feeding"""
        ...


@dataclass(slots=True, frozen=True)
class DataFrameFeeder(Feeder):
    """Feed dataframe"""

    data: pd.DataFrame

    def feed(self) -> pd.DataFrame:
        self.data_validation(df=self.data)
        return self.data


@dataclass(slots=True)
class BagelDatabaseFeeder(Feeder):
    """Mysql connectionl, please refer to TushareDownloader"""

    host: str
    port: int
    user: str
    password: str
    database: str
    data: pd.DataFrame | None = None
    engine: Engine = field(init=False)

    def __post_init__(self):
        """Connect to mysql server"""
        self.engine = create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}',
        )

    def execute(self, sql: str) -> list:
        """execute sql query"""
        with self.engine.begin() as conn:
            results = conn.execute(text(sql)).fetchall()
            if results:
                return [_ for _ in results]

    def query_pv(self,
                 codes: Iterable[str],
                 account: str,
                 table_name: str,
                 date_range: (datetime, datetime)) -> None:
        """
        Query price and volume data from database
        """
        sql = f"""
        SELECT trade_date, ts_code, {account} 
        FROM {table_name} 
        WHERE ts_code IN {tuple(codes)} 
        AND trade_date BETWEEN '{date_range[0].strftime('%Y%m%d')}' AND '{date_range[1].strftime('%Y%m%d')}'
        """
        df = pd.read_sql(sql, con=self.engine, parse_dates=['trade_date'])
        df = df.pivot(index='trade_date', columns='ts_code', values=account)
        self.data = df.sort_index()

    def feed(self) -> pd.DataFrame:
        if isinstance(self.data, pd.DataFrame):
            self.data_validation(df=self.data)
            return self.data
        else:
            raise ValueError('No data, please use BagelDatabaseFeeder.query() methods to query data first')
