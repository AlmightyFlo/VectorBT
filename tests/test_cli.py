from typer.testing import CliRunner

from vectorbt_research.cli import app


def test_cli_help_exposes_strategy_command() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "sma-cross" in result.stdout
