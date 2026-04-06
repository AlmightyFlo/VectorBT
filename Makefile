PYTHON ?= 3.13

.PHONY: sync lint format typecheck test

sync:
	uv sync --python $(PYTHON) --extra dev

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src

test:
	uv run pytest
