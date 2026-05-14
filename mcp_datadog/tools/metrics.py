"""Metrics tools for Datadog MCP server."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..client import get_client


class QueryMetricsParams(BaseModel):
    """Parameters for query-metrics tool."""

    query: str = Field(
        ..., description="Datadog metric query (e.g. 'avg:system.cpu.user{host:myhost} by {env}')"
    )
    from_: int = Field(..., alias="from", description="Start time as Unix epoch seconds")
    to: int = Field(..., description="End time as Unix epoch seconds")


async def query_metrics(params: QueryMetricsParams) -> dict[str, Any]:
    """Query time-series metrics from Datadog.

    Query metric data using Datadog's metric query syntax. Supports aggregations,
    filtering, and grouping operations on time-series data.

    Args:
        query: Metric query string (e.g. 'avg:system.cpu.user{host:myhost} by {env}')
        from_: Start time as Unix epoch seconds
        to: End time as Unix epoch seconds

    Returns:
        Dictionary containing metric series data with timestamps and values
    """
    client = get_client()
    response = await client.query_metrics(query=params.query, _from=params.from_, to=params.to)

    series = response.get("series", [])
    results = [
        {
            "metric": s.get("metric"),
            "displayName": s.get("display_name"),
            "unit": s.get("unit"),
            "scope": s.get("scope"),
            "pointCount": len(s.get("pointlist", [])),
            "points": [{"timestamp": ts, "value": val} for ts, val in s.get("pointlist", [])],
        }
        for s in series
    ]

    return {
        "query": response.get("query"),
        "seriesCount": len(series),
        "series": results,
    }


class GetMetricsParams(BaseModel):
    """Parameters for get-metrics tool."""

    q: str = Field(..., description="Search query to filter metrics (e.g. 'system.cpu')")


async def get_metrics(params: GetMetricsParams) -> dict[str, Any]:
    """List available metrics from Datadog.

    Search for metrics by name pattern. Returns the list of metrics
    that match the provided query string.

    Args:
        q: Search query to filter metrics by name (e.g. 'system.cpu', 'aws.rds')

    Returns:
        Dictionary containing list of matching metric names
    """
    client = get_client()
    response = await client.list_metrics(q=params.q)
    return {"metrics": response.get("metrics", [])}


class GetMetricMetadataParams(BaseModel):
    """Parameters for get-metric-metadata tool."""

    metricName: str = Field(..., description="Full metric name (e.g. 'system.cpu.user')")


async def get_metric_metadata(params: GetMetricMetadataParams) -> dict[str, Any]:
    """Get metadata for a Datadog metric.

    Retrieve metadata including type, unit, description, and other properties
    for a specific metric.

    Args:
        metricName: Full metric name (e.g. 'system.cpu.user', 'aws.ec2.cpuutilization')

    Returns:
        Dictionary containing metric metadata (description, type, unit, etc.)
    """
    client = get_client()
    response = await client.get_metric_metadata(metric_name=params.metricName)
    return {
        "name": params.metricName,
        "description": response.get("description"),
        "type": response.get("type"),
        "unit": response.get("unit"),
        "perUnit": response.get("per_unit"),
        "shortName": response.get("short_name"),
        "integration": response.get("integration"),
        "statsdInterval": response.get("statsd_interval"),
    }


class ListActiveMetricsParams(BaseModel):
    """Parameters for list-active-metrics tool."""

    from_: int = Field(
        ..., alias="from", description="Unix epoch seconds - metrics active since this time"
    )
    host: Optional[str] = Field(None, description="Filter by hostname")
    tagFilter: Optional[str] = Field(None, description="Filter by tag (e.g. 'env:prod')")


async def list_active_metrics(params: ListActiveMetricsParams) -> dict[str, Any]:
    """List active metrics from a given time.

    Return metrics that have reported data since a specified time,
    optionally filtered by host or tag.

    Args:
        from_: Unix epoch seconds - metrics active since this time
        host: Filter by hostname (optional)
        tagFilter: Filter by tag (e.g. 'env:prod') (optional)

    Returns:
        Dictionary containing list of active metrics
    """
    return {"metrics": [], "from": params.from_, "note": "Endpoint not yet implemented in client"}


class ListMetricTagsParams(BaseModel):
    """Parameters for list-metric-tags tool."""

    metricName: str = Field(..., description="Full metric name (e.g. 'system.cpu.user')")
    windowSeconds: Optional[int] = Field(
        None, description="Look-back window in seconds (default: 14400)"
    )


async def list_metric_tags(params: ListMetricTagsParams) -> dict[str, Any]:
    """List available tags for a metric.

    Return all unique tag keys and values for a specific metric
    within a time window.

    Args:
        metricName: Full metric name (e.g. 'system.cpu.user')
        windowSeconds: Look-back window in seconds (default: 14400 = 4h)

    Returns:
        Dictionary containing metric name and list of available tags
    """
    return {
        "metric": params.metricName,
        "tags": [],
        "note": "Endpoint not yet implemented in client",
    }
