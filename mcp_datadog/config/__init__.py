"""Configuration and environment variables for Datadog MCP server."""

import os
from typing import Optional


def parse_list(raw: Optional[str]) -> Optional[list[str]]:
    """Parse comma-separated string into list."""
    if not raw:
        return None
    return [s.strip().lower() for s in raw.split(",") if s.strip()]


class Config:
    """Configuration class for Datadog API credentials and settings."""

    def __init__(self) -> None:
        self.api_key: str = os.environ.get("DD_API_KEY", "")
        self.app_key: str = os.environ.get("DD_APP_KEY", "")
        self.site: str = os.environ.get("DD_SITE", "datadoghq.com")
        self.allow_write: bool = os.environ.get("DD_ALLOW_WRITE", "false").lower() == "true"
        self.enabled_categories: Optional[list[str]] = parse_list(os.environ.get("DD_TOOLS"))
        self.disabled_categories: Optional[list[str]] = parse_list(os.environ.get("DD_DISABLE"))


config = Config()


def validate_config() -> None:
    """Validate that required configuration is present."""
    if not config.api_key:
        raise ValueError("DD_API_KEY environment variable is required")
    if not config.app_key:
        raise ValueError("DD_APP_KEY environment variable is required")
