"""Datadog MCP Server - Python implementation using FastMCP.

This module provides a complete MCP server for Datadog monitoring platform,
exposing metrics, monitors, logs, APM, incidents, and more.

Components:
- Tools: 48+ tools for Datadog operations
- Prompts: 4 workflow prompts for incident/response handling
- Resources: 4 template resources for direct data access
"""

__version__ = "1.0.0"

from .server import mcp, main
from .tool_registry import registry, search_tools_handler, ToolInfo

__all__ = [
    "mcp",
    "main",
    "registry",
    "search_tools_handler",
    "ToolInfo",
    "__version__",
]