"""Error Tracking tools for Datadog MCP server."""

from typing import Any
from pydantic import BaseModel, Field
from ..client import get_client


class ListErrorTrackersParams(BaseModel):
    limit: int = Field(50, description="Max results")
    offset: int = Field(0, description="Offset for pagination")


async def list_error_trackers(params: ListErrorTrackersParams) -> list[dict[str, Any]]:
    """List error trackers.

    Retrieve a list of error trackers configured in Datadog.

    Args:
        limit: Maximum number of results (default: 50)
        offset: Offset for pagination (default: 0)

    Returns:
        List of error tracker objects
    """
    client = get_client()
    return await client.list_error_trackers(limit=params.limit, offset=params.offset)


class GetErrorTrackerParams(BaseModel):
    tracker_id: str = Field(..., description="Error tracker ID")


async def get_error_tracker(params: GetErrorTrackerParams) -> dict[str, Any]:
    """Get error tracker details.

    Retrieve details for a specific error tracker.

    Args:
        tracker_id: Error tracker ID

    Returns:
        Error tracker object with details
    """
    client = get_client()
    return await client.get_error_tracker(tracker_id=params.tracker_id)


class SearchErrorEventsParams(BaseModel):
    query: str = Field(..., description="Error event query")
    time_range: str = Field("1h", description="Time range")
    limit: int = Field(50, description="Max results")


async def search_error_events(params: SearchErrorEventsParams) -> dict[str, Any]:
    """Search error events.

    Search for error events from Error Tracking.

    Args:
        query: Error event query (e.g. 'service:my-service')
        time_range: Time range (e.g. '1h', '4h', '1d')
        limit: Maximum number of results (default: 50)

    Returns:
        Dictionary containing matching error events
    """
    client = get_client()
    return await client.search_error_events(
        query=params.query, time_range=params.time_range, limit=params.limit
    )
