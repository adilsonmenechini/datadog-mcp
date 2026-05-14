"""Integration tests for Datadog MCP server."""

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_server_initialization():
    """Test server can be initialized."""
    with patch("mcp_datadog.config.validate_config"):
        from mcp_datadog.server import mcp

        assert mcp.name == "datadog"


@pytest.mark.asyncio
async def test_tool_registration():
    """Test tools are registered correctly."""
    with patch("mcp_datadog.config.validate_config"):
        from mcp_datadog.server import mcp

        tools = mcp._tool_manager.list_tools()
        tool_names = [t.name for t in tools]

        # Check expected tools exist
        assert "query-metrics" in tool_names
        assert "get-monitors" in tool_names
        assert "search-logs" in tool_names
        assert "search-spans" in tool_names


@pytest.mark.asyncio
async def test_search_tools():
    """Test search tools functionality."""
    with patch("mcp_datadog.config.validate_config"):
        from mcp_datadog.tool_registry import registry, search_tools_handler

        # Test empty search
        results = search_tools_handler("")
        assert len(results) == len(registry.tools)

        # Test search with query
        results = search_tools_handler("monitor")
        assert len(results) > 0
        assert any("monitor" in r["name"].lower() for r in results)


@pytest.mark.asyncio
async def test_prompts_registration():
    """Test prompts are registered correctly."""
    with patch("mcp_datadog.config.validate_config"):
        from mcp_datadog.server import mcp

        prompts = mcp._prompt_manager.list_prompts()
        prompt_names = [p.name for p in prompts]

        # Check all expected prompts exist
        assert "triage_incident" in prompt_names
        assert "audit_monitor_noise" in prompt_names
        assert "analyze_rum_error_spike" in prompt_names
        assert "investigate_slow_trace" in prompt_names
        assert len(prompts) == 4


@pytest.mark.asyncio
async def test_resource_templates_registration():
    """Test resource templates are registered correctly."""
    with patch("mcp_datadog.config.validate_config"):
        from mcp_datadog.server import mcp

        templates = mcp._resource_manager.list_templates()
        template_uris = [t.uri_template for t in templates]

        # Check expected resource templates exist
        assert "datadog://monitor/{monitor_id}" in template_uris
        assert "datadog://metric/{metric_name}/metadata" in template_uris
        assert "datadog://incident/{incident_id}" in template_uris
        assert "datadog://service/{service_name}" in template_uris
        assert len(templates) == 4