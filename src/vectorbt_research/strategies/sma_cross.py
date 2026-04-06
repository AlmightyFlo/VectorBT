from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pandas as pd
import vectorbt as vbt

from vectorbt_research.types import PortfolioLike


@dataclass(frozen=True, slots=True)
class SmaCrossConfig:
    fast_window: int
    slow_window: int
    initial_cash: float
    fees: float
    slippage: float

    def validate(self) -> None:
        if self.fast_window >= self.slow_window:
            raise ValueError("fast_window must be smaller than slow_window.")
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be greater than zero.")
        if self.fees < 0:
            raise ValueError("fees cannot be negative.")
        if self.slippage < 0:
            raise ValueError("slippage cannot be negative.")


def build_portfolio(prices: pd.Series, config: SmaCrossConfig) -> PortfolioLike:
    config.validate()

    fast_ma = vbt.MA.run(prices, window=config.fast_window, short_name="fast")
    slow_ma = vbt.MA.run(prices, window=config.slow_window, short_name="slow")

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    if not bool(entries.any()):
        raise ValueError("Strategy generated no entry signals for the supplied inputs.")

    return cast(
        PortfolioLike,
        vbt.Portfolio.from_signals(
            prices,
            entries,
            exits,
            init_cash=config.initial_cash,
            fees=config.fees,
            slippage=config.slippage,
        ),
    )
