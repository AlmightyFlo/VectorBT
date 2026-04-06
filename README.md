# VectorBT Research Workspace

This repository is scaffolded as a Python package for research and backtesting with
[`vectorbt`](https://vectorbt.dev/). It intentionally does not ship fake symbols,
demo datasets, or sample credentials.

## Stack

- `uv` for environment and dependency management
- `vectorbt` for data ingestion and portfolio simulation
- `typer` for the command-line interface
- `ruff`, `mypy`, and `pytest` for quality gates

## Layout

```text
src/vectorbt_research/
  cli.py
  config.py
  data.py
  reports.py
  serialization.py
  strategies/
tests/
```

## Setup

1. Install the pinned project environment:

   ```bash
   make sync
   ```

2. Inspect the available CLI command:

   ```bash
   uv run vectorbt-backtest --help
   uv run vectorbt-backtest sma-cross --help
   ```

3. Run the quality checks:

   ```bash
   make lint
   make typecheck
   make test
   ```

## Backtest Workflow

The scaffold currently exposes a single strategy command:

- `sma-cross`: downloads market data through VectorBT's Yahoo Finance integration,
  builds a moving-average crossover portfolio, and writes JSON/CSV artifacts under
  `artifacts/`.

The command requires the symbol, date range, moving-average windows, and capital
inputs explicitly so strategy runs are driven by real parameters rather than baked-in
defaults.
