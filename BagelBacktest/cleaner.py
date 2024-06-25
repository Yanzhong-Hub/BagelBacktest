"""
Cleaner Module
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class Cleaner(ABC):
    """
    cleaner abstract class
    """

    @abstractmethod
    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean method
        All subclass should implement this method
        :return: cleaned data frame
        """
        pass


@dataclass(slots=True)
class EmptyCleaner(Cleaner):
    """
    No cleaner
    """

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        return data
