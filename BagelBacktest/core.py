"""
BagelBacktest core
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd

from dataclasses import dataclass, field
from datetime import datetime

from .feeder import Feeder
from .cleaner import Cleaner, EmptyCleaner
from .transactions import Transactions
from .strategy import Strategy, BuyAndHoldStrategy
from .portfolio import Portfolio


@dataclass(slots=True)
class Core:
    """
    BagelBacktest core

    User interface for BagelBacktest pacakage
    """

    # required parameter
    _feeder: Feeder = field(init=False)

    # optional parameter
    _initial_cash: float = 1_000_000
    _cleaner: Cleaner = field(default_factory=EmptyCleaner)  # Use default_factory for mutable type
    _strategy: Strategy = field(default_factory=BuyAndHoldStrategy)
    _transactions: Transactions = field(default_factory=Transactions)

    def add_feeder(self, feeder: Feeder):
        """Add a feeder to BagelBacktest"""
        self._feeder = feeder

    def add_strategy(self, strategy: Strategy):
        """Add a Strategy to BagelBacktest"""
        self._strategy = strategy

    def add_transaction(self, trade_date: datetime, code: str, amount: int):
        """Add a single transaction"""
        self._transactions.add_transaction(trade_date, code, amount)

    def run(self) -> Portfolio:
        """
        run backtest, generate a Portfolio object 1. load price - feed
            - data cleaning *optional
        2. generate signal
            - strategy *optional
            - transactions *optionals
        3. Calculate
            - amounts: accumulate signals
            - values: price * amounts
        4. Cash change
            - cash change = price * signal.sum(axis=1)
        """

        # load price
        price, adj_price = self._feeder.feed()
        price = self._cleaner.clean(price)
        adj_price = self._cleaner.clean(adj_price)

        # generate signal
        strategy_signal = self._strategy.generate_signal(adj_price)
        transactions_signal = self._transactions.generate_signal(strategy_signal)
        signal: pd.DataFrame = strategy_signal + transactions_signal

        # Calculate
        amounts = signal.cumsum()
        values = amounts * price

        # Cash
        cash_change: pd.DataFrame = - price * signal
        cash: pd.Series = cash_change.sum(axis=1)
        cash: pd.Series = cash.cumsum()
        cash += self._initial_cash
        cash.name = 'cash'

        return Portfolio(cash=cash,
                         values=values,
                         amounts=amounts)
