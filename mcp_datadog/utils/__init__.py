"""Utility functions for tool handlers."""

import json
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any


class WriteBlockedError(Exception):
    """Raised when a write operation is attempted without DD_ALLOW_WRITE=true."""

    def __init__(self) -> None:
        self.message = "Write operations are disabled. Set DD_ALLOW_WRITE=true to enable."
        super().__init__(self.message)
        self.name = "WriteBlockedError"


def assert_write_allowed() -> None:
    """Assert that write operations are allowed."""
    from ..config import config

    if not config.allow_write:
        raise WriteBlockedError()


def extract_datadog_error(body: Any) -> Any:
    """Extract error information from Datadog API error response."""
    try:
        parsed = json.loads(body) if isinstance(body, str) else body
        if isinstance(parsed, dict):
            if "errors" in parsed:
                return parsed["errors"]
            if "message" in parsed and isinstance(parsed["message"], str):
                return parsed["message"]
        return body if isinstance(body, str) else json.dumps(body)
    except (json.JSONDecodeError, TypeError):
        return str(body)


def sanitize_error_message(message: str) -> str:
    """Sanitize sensitive patterns from error messages."""
    patterns = [
        (r"DD_API_KEY[=:\s]*[^\s,\]\}]+", "DD_API_KEY=[REDACTED]"),
        (r"DD_APP_KEY[=:\s]*[^\s,\]\}]+", "DD_APP_KEY=[REDACTED]"),
        (r"api_key[=:\s]*[^\s,\]\}]+", "api_key=[REDACTED]"),
        (r"Bearer\s+[^\s]+", "Bearer [REDACTED]"),
    ]
    for pattern, replacement in patterns:
        message = re.sub(pattern, replacement, message)
    return message


def format_error_response(error: Exception) -> dict[str, Any]:
    """Format an error into a structured response."""
    error_dict: dict[str, Any] = {"message": sanitize_error_message(str(error))}

    # Check if it's an API exception with additional fields
    if hasattr(error, "status"):
        error_dict["status"] = error.status  # type: ignore
    if hasattr(error, "body"):
        error_dict["datadogError"] = extract_datadog_error(error.body)  # type: ignore
    if hasattr(error, "request_id"):
        error_dict["requestId"] = error.request_id  # type: ignore

    return {"error": error_dict}


def apply_extract_fields(data: Any, fields: str) -> Any:
    """Apply field extraction to response data."""
    if not fields:
        return data
    field_list = [f.strip() for f in fields.split(",")]
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k in field_list}
    if isinstance(data, list):
        return [{k: v for k, v in item.items() if k in field_list} for item in data]
    return data


# Default Datadog site (US1)
DEFAULT_DD_SITE = "datadoghq.com"

# Supported Datadog sites
VALID_DD_SITES = {
    DEFAULT_DD_SITE,
    "us3.datadoghq.com",
    "us5.datadoghq.com",
    "datadoghq.eu",
    "ap1.datadoghq.com",
    "ddog-gov.com",
}


def parse_time(time_str: str) -> int:
    """Parse time string to Unix timestamp.

    Accepts formats:
    - ISO 8601: 2026-01-07T15:30:00Z
    - Relative: 1h, 24h, 7d, 1w, 10m, 30s
    - 'now' for current time

    Args:
        time_str: Time string in ISO 8601 or relative format

    Returns:
        Unix timestamp in seconds
    """
    if not time_str:
        return int(datetime.now(timezone.utc).timestamp())

    time_str = time_str.strip()

    # Handle 'now'
    if time_str == "now":
        return int(datetime.now(timezone.utc).timestamp())

    # Handle relative formats (e.g., '1h', '24h', '7d', '1w', '30m', '45s')
    relative_match = re.match(r"^(\d+)([smhdw])$", time_str.lower())
    if relative_match:
        value, unit = int(relative_match.group(1)), relative_match.group(2)
        now = datetime.now(timezone.utc)
        if unit == "s":
            delta = timedelta(seconds=value)
        elif unit == "m":
            delta = timedelta(minutes=value)
        elif unit == "h":
            delta = timedelta(hours=value)
        elif unit == "d":
            delta = timedelta(days=value)
        elif unit == "w":
            delta = timedelta(weeks=value)
        else:
            delta = timedelta(hours=value)
        return int((now - delta).timestamp())

    # Handle ISO 8601 format
    try:
        # Handle 'Z' suffix
        if time_str.endswith("Z"):
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(time_str)

        # If no timezone, assume UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return int(dt.timestamp())
    except ValueError:
        # Fallback to 'now' for invalid formats
        return int(datetime.now(timezone.utc).timestamp())


def get_dd_site() -> str:
    """Get and validate DD_SITE environment variable."""
    dd_site = os.getenv("DD_SITE", DEFAULT_DD_SITE)
    if not dd_site or not re.match(r"^[a-z0-9.-]+$", dd_site):
        raise ValueError(
            f"Invalid DD_SITE value: '{dd_site}'. "
            f"Must be one of: {', '.join(sorted(VALID_DD_SITES))}"
        )
    return dd_site


def get_datadog_url() -> str:
    """Get base Datadog API URL."""
    return f"https://api.{get_dd_site()}"


def get_headers() -> dict[str, str]:
    """Get API headers with authentication."""
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": os.getenv("DD_API_KEY", ""),
        "DD-APPLICATION-KEY": os.getenv("DD_APP_KEY", ""),
    }
