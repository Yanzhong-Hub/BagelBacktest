"""
BagelBacktest
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

from .core import Core
from .feeder import Feeder, BagelDatabaseFeeder, DataFrameFeeder
from .cleaner import Cleaner, EmptyCleaner
from .transactions import Transactions
from .strategy import Strategy, BuyAndHoldStrategy
from .portfolio import Portfolio
