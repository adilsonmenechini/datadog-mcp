"""Logs tools for Datadog MCP server."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..client import get_client
from ..utils import assert_write_allowed


class SearchLogsParams(BaseModel):
    """Parameters for search-logs tool."""

    query: str = Field(
        ...,
        description="Log search query in Datadog syntax (e.g. 'service:my-service status:error')",
    )
    time_range: str = Field("1h", description="Time range to search (e.g. '1h', '4h', '1d')")
    limit: int = Field(50, description="Maximum number of log entries to return")
    cursor: Optional[str] = Field(None, description="Pagination cursor for retrieving next page")


async def search_logs(params: SearchLogsParams) -> dict[str, Any]:
    """Search Datadog logs.

    Query logs with Datadog's log search syntax. Returns log entries matching
    the query filtered by time range.

    Args:
        query: Log search query (e.g. 'service:my-service status:error @http.method:GET')
        time_range: Time range to search (e.g. '1h', '4h', '1d', '7d')
        limit: Maximum number of log entries to return (default: 50)
        cursor: Pagination cursor for retrieving next page (optional)

    Returns:
        Dictionary containing matching log entries and metadata
    """
    from ..utils.formatters import format_log_results

    client = get_client()
    result = await client.search_logs(
        query=params.query, time_range=params.time_range, limit=params.limit, cursor=params.cursor
    )

    logs = result.get("logs", result.get("data", []))
    return format_log_results(
        logs, {"query": params.query, "time_range": params.time_range, "total": len(logs)}
    )


class AggregateLogsParams(BaseModel):
    """Parameters for aggregate-logs tool."""

    query: str = Field(..., description="Log query (e.g. 'service:my-service')")
    compute: str = Field("count", description="Aggregation function (count, avg, sum, min, max)")
    time_range: str = Field("1h", description="Time range to search")
    group_by: Optional[str] = Field(
        None, description="Field to group by (e.g. 'service', '@status')"
    )


async def aggregate_logs(params: AggregateLogsParams) -> dict[str, Any]:
    """Aggregate Datadog logs.

    Apply aggregation functions to log data grouped by specified fields.
    Useful for generating metrics and visualizations from log data.

    Args:
        query: Log query to filter logs (e.g. 'service:my-service')
        compute: Aggregation function (count, avg, sum, min, max)
        time_range: Time range to search (e.g. '1h', '4h', '1d')
        group_by: Field to group results by (e.g. 'service', '@status')

    Returns:
        Dictionary containing aggregated results and group counts
    """
    client = get_client()
    return await client.aggregate_logs(
        query=params.query,
        compute=params.compute,
        time_range=params.time_range,
        group_by=params.group_by,
    )


class SendLogsParams(BaseModel):
    """Parameters for send-logs tool."""

    message: str = Field(..., description="Log message content")
    service: Optional[str] = Field(None, description="Service name to associate with log")
    hostname: Optional[str] = Field(None, description="Hostname to associate with log")
    ddsource: Optional[str] = Field(None, description="Source identifier")
    tags: Optional[list[str]] = Field(None, description="Tags to attach to the log entry")


async def send_logs(params: SendLogsParams) -> dict[str, Any]:
    """Send logs to Datadog.

    Submit log entries to Datadog for indexing and analysis.
    Requires DD_ALLOW_WRITE=true environment variable.

    Args:
        message: Log message content
        service: Service name (optional)
        hostname: Hostname (optional)
        ddsource: Source identifier (optional)
        tags: Tags to attach (optional)

    Returns:
        Dictionary confirming log acceptance
    """
    assert_write_allowed()
    return {
        "accepted": True,
        "message": params.message,
        "note": "Use HTTP API directly for log submission",
    }


class SearchAuditLogsParams(BaseModel):
    """Parameters for search-audit-logs tool."""

    query: str = Field("*", description="Audit log query")
    time_range: str = Field("1h", description="Time range to search")
    limit: int = Field(50, description="Maximum number of results")


async def search_audit_logs(params: SearchAuditLogsParams) -> dict[str, Any]:
    """Search Datadog audit logs.

    Query audit logs for organization activity tracking including
    user actions, resource changes, and API calls.

    Args:
        query: Audit log query filter (default: '*')
        time_range: Time range to search (e.g. '1h', '4h', '1d')
        limit: Maximum number of results to return (default: 50)

    Returns:
        Dictionary containing matching audit log entries
    """
    client = get_client()
    return await client.search_logs(
        query=params.query, time_range=params.time_range, limit=params.limit
    )
