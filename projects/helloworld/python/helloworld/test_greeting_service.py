"""Unit tests for the greeting service.

These tests exercise the pure-function logic without HTTP or a database.
"""
import pytest

from app.services.greeting_service import build_greeting_message


class TestBuildGreetingMessage:
    def test_returns_hello_for_simple_name(self):
        assert build_greeting_message("World") == "Hello, World!"

    def test_strips_surrounding_whitespace(self):
        assert build_greeting_message("  Alice  ") == "Hello, Alice!"

    def test_handles_unicode_names(self):
        assert build_greeting_message("Zoë") == "Hello, Zoë!"

    @pytest.mark.parametrize("bad_name", ["", "   ", "\t\n"])
    def test_rejects_empty_or_whitespace(self, bad_name: str):
        with pytest.raises(ValueError, match="must not be empty"):
            build_greeting_message(bad_name)
