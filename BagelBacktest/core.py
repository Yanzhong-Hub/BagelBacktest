"""
BagelBacktest core
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd

from dataclasses import dataclass, field

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
    _feeder: Feeder

    # optional parameter
    _initial_cash: float = 1_000_000
    _cleaner: Cleaner = EmptyCleaner()
    _strategy: Strategy = BuyAndHoldStrategy()
    _transactions: Transactions = Transactions()

    # Generated parameter
    _signals: pd.DataFrame = field(init=False)
    _amounts: pd.DataFrame = field(init=False)
    _values: pd.DataFrame = field(init=False)

    def run(self) -> Portfolio:
        """
        run backtest, generate a Portfolio object
        """
        pass
