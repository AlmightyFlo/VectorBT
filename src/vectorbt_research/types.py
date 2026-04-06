from __future__ import annotations

from typing import Protocol

import pandas as pd


class RecordsReadable(Protocol):
    records_readable: pd.DataFrame


class PortfolioLike(Protocol):
    trades: RecordsReadable
    orders: RecordsReadable

    def stats(self) -> pd.Series: ...
