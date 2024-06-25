"""
Transcation module
Author: Eric Yanzhong Huang
Email: eric.yanzhong.huang@outlook.com
"""

import pandas as pd

from datetime import datetime

from dataclasses import dataclass, field


@dataclass(slots=True)
class Transactions:
    """
    Transactions class, generate signal
    """

    transactions: dict[datetime, dict[str, int]] = field(default_factory=dict)  # trade_date, code, signal

    def add_transaction(self, trade_date: datetime, code: str, signal: int) -> None:
        """
        add single transaction into transactions
        """
        if trade_date in self.transactions:
            if code in self.transactions[trade_date]:
                self.transactions[trade_date][code] += signal
            else:
                self.transactions[trade_date][code] = signal
        else:
            self.transactions[trade_date] = {code: signal}

    def generate_signal(self, adj_price: pd.DataFrame) -> pd.DataFrame:
        """
        generate signal DataFrame
        """
        signal = pd.DataFrame(0, index=adj_price.index, columns=adj_price.columns)
        for trade_date, transaction in self.transactions.items():
            for code, value in transaction.items():
                self._validate_signal(trade_date, code, adj_price)
                signal.loc[trade_date, code] = value
        return signal

    @staticmethod
    def _validate_signal(trade_date: datetime, code: str, adj_price: pd.DataFrame) -> None:
        """
        check if trade_date and code in adj_price DataFrame
        """
        if code not in adj_price.columns:
            raise ValueError(f'{code} is not in adj_price index')
        if trade_date not in adj_price.index:
            raise ValueError(f'{trade_date} is not in adj_price column')
