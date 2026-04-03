"""Tests for reddit_cli.errors module."""
import pytest
import httpx
import typer
from unittest.mock import MagicMock, patch

from reddit_cli.errors import (
    handle_api_error,
    handle_validation_error,
    handle_interrupt,
    EXIT_GENERAL_ERROR,
    EXIT_USAGE_ERROR,
    EXIT_INTERRUPTED,
)


class TestHandleApiError:
    def test_timeout_exception(self):
        exc = httpx.TimeoutException("Connection timed out")
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_connect_error(self):
        exc = httpx.ConnectError("Could not connect")
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_400(self):
        response = MagicMock()
        response.status_code = 400
        exc = httpx.HTTPStatusError("Bad Request", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_401(self):
        response = MagicMock()
        response.status_code = 401
        exc = httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_403(self):
        response = MagicMock()
        response.status_code = 403
        exc = httpx.HTTPStatusError("Forbidden", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_404(self):
        response = MagicMock()
        response.status_code = 404
        exc = httpx.HTTPStatusError("Not Found", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_429(self):
        response = MagicMock()
        response.status_code = 429
        exc = httpx.HTTPStatusError("Too Many Requests", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_500(self):
        response = MagicMock()
        response.status_code = 500
        exc = httpx.HTTPStatusError("Internal Server Error", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_502(self):
        response = MagicMock()
        response.status_code = 502
        exc = httpx.HTTPStatusError("Bad Gateway", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_503(self):
        response = MagicMock()
        response.status_code = 503
        exc = httpx.HTTPStatusError("Service Unavailable", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_http_status_error_other(self):
        response = MagicMock()
        response.status_code = 418
        exc = httpx.HTTPStatusError("I am a teapot", request=MagicMock(), response=response)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR

    def test_typer_exit_reraised(self):
        exc = typer.Exit(code=42)
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == 42

    def test_generic_exception(self):
        exc = ValueError("Something went wrong")
        with pytest.raises(typer.Exit) as exc_info:
            handle_api_error(exc)
        assert exc_info.value.exit_code == EXIT_GENERAL_ERROR


class TestHandleValidationError:
    def test_single_valid_value(self):
        with pytest.raises(typer.Exit) as exc_info:
            handle_validation_error("sort", ["hot"], "invalid")
        assert exc_info.value.exit_code == EXIT_USAGE_ERROR

    def test_multiple_valid_values(self):
        with pytest.raises(typer.Exit) as exc_info:
            handle_validation_error("sort", ["hot", "new", "top", "rising"], "invalid")
        assert exc_info.value.exit_code == EXIT_USAGE_ERROR

    def test_empty_valid_values(self):
        with pytest.raises(typer.Exit) as exc_info:
            handle_validation_error("sort", [], "invalid")
        assert exc_info.value.exit_code == EXIT_USAGE_ERROR

    def test_special_characters_in_value(self):
        with pytest.raises(typer.Exit) as exc_info:
            handle_validation_error("sort", ["hot", "new"], "invalid<script>")
        assert exc_info.value.exit_code == EXIT_USAGE_ERROR


class TestHandleInterrupt:
    def test_keyboard_interrupt(self):
        with pytest.raises(typer.Exit) as exc_info:
            handle_interrupt()
        assert exc_info.value.exit_code == EXIT_INTERRUPTED

    def test_interrupt_message(self):
        with patch("reddit_cli.errors.typer.echo") as mock_echo:
            try:
                handle_interrupt()
            except typer.Exit:
                pass
            mock_echo.assert_called_once_with("Interrupted by user.", err=True)


class TestExitCodeConstants:
    def test_exit_codes(self):
        assert EXIT_GENERAL_ERROR == 1
        assert EXIT_USAGE_ERROR == 2
        assert EXIT_INTERRUPTED == 130
