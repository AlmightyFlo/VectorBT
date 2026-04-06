from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from vectorbt_research.config import ensure_project_dirs
from vectorbt_research.data import download_close_series
from vectorbt_research.reports import resolve_output_dir, write_backtest_artifacts
from vectorbt_research.strategies.sma_cross import SmaCrossConfig, build_portfolio

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)


@app.callback()
def main() -> None:
    """Run VectorBT research workflows."""


@app.command("sma-cross")
def sma_cross(
    symbol: Annotated[str, typer.Option(help="Yahoo Finance symbol to backtest.")],
    start: Annotated[str, typer.Option(help="Inclusive start timestamp passed to VectorBT.")],
    end: Annotated[str, typer.Option(help="Inclusive end timestamp passed to VectorBT.")],
    fast_window: Annotated[int, typer.Option(min=1, help="Fast moving-average window.")],
    slow_window: Annotated[int, typer.Option(min=2, help="Slow moving-average window.")],
    initial_cash: Annotated[float, typer.Option(min=0.0, help="Initial portfolio cash.")],
    interval: Annotated[str, typer.Option(help="Yahoo Finance interval string.")] = "1d",
    fees: Annotated[float, typer.Option(min=0.0, help="Per-order proportional fees.")] = 0.0,
    slippage: Annotated[
        float,
        typer.Option(min=0.0, help="Per-order proportional slippage."),
    ] = 0.0,
    output_dir: Annotated[
        Path | None,
        typer.Option(
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
            help="Optional directory for generated artifacts.",
        ),
    ] = None,
) -> None:
    ensure_project_dirs()

    config = SmaCrossConfig(
        fast_window=fast_window,
        slow_window=slow_window,
        initial_cash=initial_cash,
        fees=fees,
        slippage=slippage,
    )

    try:
        prices = download_close_series(symbol=symbol, start=start, end=end, interval=interval)
        portfolio = build_portfolio(prices=prices, config=config)
    except Exception as exc:
        typer.echo(f"Backtest failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    target_dir = resolve_output_dir(
        strategy_name="sma-cross",
        symbol=symbol,
        start=start,
        end=end,
        output_dir=output_dir,
    )
    artifacts = write_backtest_artifacts(
        strategy_name="sma-cross",
        symbol=symbol,
        interval=interval,
        prices=prices,
        config=config,
        portfolio=portfolio,
        output_dir=target_dir,
    )

    typer.echo(f"Artifacts written to {target_dir}")
    typer.echo(f"Stats: {artifacts['stats']}")
    typer.echo(f"Trades: {artifacts['trades']}")
    typer.echo(f"Orders: {artifacts['orders']}")


if __name__ == "__main__":
    app()
