from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from vectorbt_research.config import ARTIFACTS_DIR
from vectorbt_research.serialization import to_jsonable
from vectorbt_research.strategies.sma_cross import SmaCrossConfig
from vectorbt_research.types import PortfolioLike


def resolve_output_dir(
    strategy_name: str,
    symbol: str,
    start: str,
    end: str,
    output_dir: Path | None,
) -> Path:
    if output_dir is not None:
        return output_dir

    run_key = "__".join([sanitize(symbol), sanitize(start), sanitize(end)])
    return ARTIFACTS_DIR / strategy_name / run_key


def write_backtest_artifacts(
    *,
    strategy_name: str,
    symbol: str,
    interval: str,
    prices: pd.Series,
    config: SmaCrossConfig,
    portfolio: PortfolioLike,
    output_dir: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = portfolio.stats()
    stats_path = output_dir / "stats.json"
    trades_path = output_dir / "trades.csv"
    orders_path = output_dir / "orders.csv"

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "strategy": strategy_name,
        "symbol": symbol,
        "interval": interval,
        "price_series": {
            "rows": len(prices),
            "start": prices.index[0],
            "end": prices.index[-1],
        },
        "parameters": asdict(config),
        "stats": stats.to_dict(),
    }

    stats_path.write_text(json.dumps(to_jsonable(payload), indent=2) + "\n", encoding="utf-8")
    portfolio.trades.records_readable.to_csv(trades_path, index=False)
    portfolio.orders.records_readable.to_csv(orders_path, index=False)

    return {
        "stats": stats_path,
        "trades": trades_path,
        "orders": orders_path,
    }


def sanitize(value: str) -> str:
    return "".join(char if char.isalnum() else "-" for char in value).strip("-").lower()
