"""
Portfolio class
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd
from dataclasses import dataclass


@dataclass(slots=True)
class Portfolio:
    """
    Portfolio class
    contains backtest results
    """

    cash: pd.Series
    amounts: pd.DataFrame
    values: pd.DataFrame
