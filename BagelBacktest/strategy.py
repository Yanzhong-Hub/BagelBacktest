"""
Strategy Module
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod

import pandas as pd


@dataclass(slots=True)
class Strategy(ABC):
    """
    Strategy abstract base class
    """

    @abstractmethod
    def generate_signal(self, adj_price: pd.DataFrame) -> pd.DataFrame:
        """
        based on adj_price
        """
        pass


@dataclass(slots=True)
class BuyAndHoldStrategy(Strategy):
    """
    Buy and Hold Strategy
    """

    def generate_signal(self, adj_price: pd.DataFrame) -> pd.DataFrame:
        signal = pd.DataFrame(data=0, index=adj_price.index, columns=adj_price.columns)
        signal.iloc[0, :] = 100
        return signal
