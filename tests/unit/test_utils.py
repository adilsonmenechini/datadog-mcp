"""Unit tests for Datadog MCP server."""

import pytest

from mcp_datadog.config import Config, validate_config, parse_list
from mcp_datadog.tool_registry import ToolRegistry
from mcp_datadog.utils import WriteBlockedError, assert_write_allowed, sanitize_error_message


class TestConfig:
    """Tests for configuration module."""

    def test_parse_list_with_valid_input(self):
        """Test parsing comma-separated string."""
        assert parse_list("a, b, c") == ["a", "b", "c"]
        assert parse_list("metrics, monitors") == ["metrics", "monitors"]

    def test_parse_list_with_empty_input(self):
        """Test parsing empty or None input."""
        assert parse_list("") is None
        assert parse_list(None) is None

    def test_parse_list_with_whitespace(self):
        """Test parsing with extra whitespace."""
        assert parse_list("  a , b  , c  ") == ["a", "b", "c"]

    def test_config_attributes(self):
        """Test Config has expected attributes."""
        config = Config()
        assert hasattr(config, "api_key")
        assert hasattr(config, "app_key")
        assert hasattr(config, "site")
        assert hasattr(config, "allow_write")
        assert hasattr(config, "enabled_categories")
        assert hasattr(config, "disabled_categories")


class TestValidateConfig:
    """Tests for configuration validation."""

    def test_validate_config_with_keys(self, monkeypatch):
        """Test validation passes with keys set."""
        monkeypatch.setenv("DD_API_KEY", "test-key")
        monkeypatch.setenv("DD_APP_KEY", "test-app-key")
        # Should not raise
        validate_config()

    def test_validate_config_missing_api_key(self, monkeypatch):
        """Test validation fails without API key."""
        monkeypatch.setenv("DD_API_KEY", "")
        monkeypatch.setenv("DD_APP_KEY", "test")
        from mcp_datadog.config import config as cfg

        cfg.api_key = ""
        cfg.app_key = "test"
        with pytest.raises(ValueError, match="DD_API_KEY"):
            validate_config()


class TestToolRegistry:
    """Tests for tool registry."""

    def test_registry_initialization(self):
        """Test registry can be initialized."""
        registry = ToolRegistry()
        assert registry.tools == {}

    def test_registry_register(self):
        """Test registering a tool."""
        registry = ToolRegistry()
        registry.register("test-tool", "A test tool", "metrics")
        assert "test-tool" in registry.tools
        assert registry.tools["test-tool"].category == "metrics"

    def test_registry_is_enabled_no_filter(self):
        """Test tool is enabled when no filter specified."""
        registry = ToolRegistry()
        assert registry.is_enabled("metrics") is True
        assert registry.is_enabled("unknown") is True

    def test_registry_is_enabled_with_enabled_list(self):
        """Test tool is enabled only when in enabled list."""
        registry = ToolRegistry(enabled_categories=["metrics", "monitors"])
        assert registry.is_enabled("metrics") is True
        assert registry.is_enabled("monitors") is True
        assert registry.is_enabled("logs") is False

    def test_registry_is_enabled_with_disabled_list(self):
        """Test tool is disabled when in disabled list."""
        registry = ToolRegistry(disabled_categories=["security"])
        assert registry.is_enabled("metrics") is True
        assert registry.is_enabled("security") is False

    def test_registry_search(self):
        """Test searching tools."""
        registry = ToolRegistry()
        registry.register("query-metrics", "Query Datadog metrics", "metrics")
        registry.register("create-monitor", "Create a monitor", "monitors")
        registry.register("delete-monitor", "Delete a monitor", "monitors")

        results = registry.search("metric")
        assert len(results) == 1
        assert results[0].name == "query-metrics"

        results = registry.search("monitor")
        assert len(results) == 2


class TestWriteBlockedError:
    """Tests for WriteBlockedError."""

    def test_error_message(self):
        """Test error has correct message."""
        err = WriteBlockedError()
        assert err.message is not None
        assert "disabled" in err.message.lower()
        assert err.name == "WriteBlockedError"

    def test_assert_write_allowed_raises(self, monkeypatch):
        """Test assert_write_allowed raises when disabled."""
        monkeypatch.setenv("DD_ALLOW_WRITE", "false")
        from mcp_datadog.config import config as cfg

        cfg.allow_write = False
        with pytest.raises(WriteBlockedError):
            assert_write_allowed()

    def test_assert_write_allowed_passes(self, monkeypatch):
        """Test assert_write_allowed passes when enabled."""
        monkeypatch.setenv("DD_ALLOW_WRITE", "true")
        from mcp_datadog.config import config as cfg

        cfg.allow_write = True
        assert_write_allowed()  # Should not raise


class TestSanitizeErrorMessage:
    """Tests for error message sanitization."""

    def test_sanitize_api_key(self):
        """Test API key is redacted."""
        msg = sanitize_error_message("Failed with DD_API_KEY=secret123")
        assert "DD_API_KEY=[REDACTED]" in msg
        assert "secret123" not in msg

    def test_sanitize_app_key(self):
        """Test APP key is redacted."""
        msg = sanitize_error_message("Error: DD_APP_KEY=mykey")
        assert "DD_APP_KEY=[REDACTED]" in msg

    def test_sanitize_bearer(self):
        """Test Bearer token is redacted."""
        msg = sanitize_error_message("Auth failed: Bearer abc123")
        assert "Bearer [REDACTED]" in msg

    def test_sanitize_no_secrets(self):
        """Test message without secrets passes through."""
        msg = sanitize_error_message("Something went wrong")
        assert msg == "Something went wrong"


class TestParseTime:
    """Tests for parse_time function."""

    def test_parse_time_now(self):
        """Test parsing 'now' returns current timestamp."""
        from mcp_datadog.client import parse_time
        import time

        result = parse_time("now")
        now = int(time.time())
        assert abs(result - now) < 2  # Within 2 seconds

    def test_parse_time_relative_hours(self):
        """Test parsing relative hours."""
        from mcp_datadog.client import parse_time
        import time

        now = int(time.time())
        assert parse_time("1h") == now - 3600
        assert parse_time("24h") == now - 86400

    def test_parse_time_relative_minutes(self):
        """Test parsing relative minutes."""
        from mcp_datadog.client import parse_time
        import time

        now = int(time.time())
        assert parse_time("10m") == now - 600
        assert parse_time("30m") == now - 1800

    def test_parse_time_relative_days(self):
        """Test parsing relative days."""
        from mcp_datadog.client import parse_time
        import time

        now = int(time.time())
        assert parse_time("1d") == now - 86400
        assert parse_time("7d") == now - 604800

    def test_parse_time_relative_seconds(self):
        """Test parsing relative seconds."""
        from mcp_datadog.client import parse_time
        import time

        now = int(time.time())
        assert parse_time("30s") == now - 30
        assert parse_time("60s") == now - 60

    def test_parse_time_iso8601(self):
        """Test parsing ISO 8601 format."""
        from mcp_datadog.client import parse_time

        # Known timestamp: 2026-01-07T15:30:00Z
        result = parse_time("2026-01-07T15:30:00Z")
        assert result == 1767799800

    def test_parse_time_empty(self):
        """Test parsing empty string returns current time."""
        from mcp_datadog.client import parse_time
        import time

        result = parse_time("")
        now = int(time.time())
        assert abs(result - now) < 2
