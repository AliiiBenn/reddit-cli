"""Tests for ping and help commands."""
from typer.testing import CliRunner

from reddit_cli import app


class TestPing:
    """Test suite for ping command."""

    def test_ping_exit_code(self, runner: CliRunner):
        """ping should exit with code 0."""
        result = runner.invoke(app, ["ping"])
        assert result.exit_code == 0

    def test_ping_output(self, runner: CliRunner):
        """ping should output 'pong'."""
        result = runner.invoke(app, ["ping"])
        assert "pong" in result.output

    def test_ping_no_errors(self, runner: CliRunner):
        """ping should not raise any exceptions."""
        result = runner.invoke(app, ["ping"])
        assert result.exception is None


class TestHelp:
    """Test suite for help command."""

    def test_help_exit_code(self, runner: CliRunner):
        """help should exit with code 0."""
        result = runner.invoke(app, ["help"])
        assert result.exit_code == 0

    def test_help_output_contains_usage(self, runner: CliRunner):
        """help should show usage information."""
        result = runner.invoke(app, ["help"])
        assert "Reddit CLI" in result.output
        assert "USAGE" in result.output

    def test_help_shows_navigation_commands(self, runner: CliRunner):
        """help should list navigation commands."""
        result = runner.invoke(app, ["help"])
        assert "frontpage" in result.output
        assert "home" in result.output
        assert "best" in result.output

    def test_help_shows_browse_commands(self, runner: CliRunner):
        """help should list browse commands."""
        result = runner.invoke(app, ["help"])
        assert "browse" in result.output

    def test_help_no_errors(self, runner: CliRunner):
        """help should not raise any exceptions."""
        result = runner.invoke(app, ["help"])
        assert result.exception is None
