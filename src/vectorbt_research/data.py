from collections.abc import Hashable

import pandas as pd
import vectorbt as vbt


def download_close_series(
    symbol: str,
    start: str,
    end: str,
    interval: str,
) -> pd.Series:
    dataset = vbt.YFData.download(symbol, start=start, end=end, interval=interval)
    close = dataset.get("Close")

    if isinstance(close, pd.DataFrame):
        if close.shape[1] != 1:
            raise ValueError(f"Expected a single close series for {symbol}.")
        close = close.iloc[:, 0]

    if not isinstance(close, pd.Series):
        raise TypeError("VectorBT did not return a pandas Series for close prices.")

    close = close.dropna()
    if close.empty:
        raise ValueError(f"No close price data returned for {symbol}.")

    close.name = _normalize_name(close.name, fallback=symbol)
    return close


def _normalize_name(value: object, fallback: str) -> str:
    if isinstance(value, str) and value:
        return value
    if isinstance(value, Hashable) and value is not None:
        return str(value)
    return fallback
