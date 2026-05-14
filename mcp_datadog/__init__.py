"""Datadog MCP Server - Python implementation using FastMCP.

This module provides a complete MCP server for Datadog monitoring platform,
exposing metrics, monitors, logs, APM, incidents, and more.

Components:
- Tools: 48+ tools for Datadog operations
- Prompts: 4 workflow prompts for incident/response handling
- Resources: 4 template resources for direct data access
"""

__version__ = "1.0.0"

# Lazy imports to avoid circular dependencies when dev_server runs
def __getattr__(name: str):
    if name == "mcp":
        from .server import mcp
        return mcp
    if name == "main":
        from .server import main
        return main
    if name in ("registry", "search_tools_handler", "ToolInfo"):
        from .tool_registry import registry, search_tools_handler, ToolInfo
        return {"registry": registry, "search_tools_handler": search_tools_handler, "ToolInfo": ToolInfo}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "mcp",
    "main",
    "registry",
    "search_tools_handler",
    "ToolInfo",
    "__version__",
]