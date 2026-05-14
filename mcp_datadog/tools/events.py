"""Events tools for Datadog MCP server."""

from typing import Any, Optional
from pydantic import BaseModel, Field
from ..client import get_client
from ..utils import assert_write_allowed


class SearchEventsParams(BaseModel):
    query: str = Field(..., description="Event search query")
    start: int = Field(..., description="Start timestamp")
    end: int = Field(..., description="End timestamp")
    limit: int = Field(100, description="Max results")
    tags: Optional[str] = Field(None, description="Filter by tags")


async def search_events(params: SearchEventsParams) -> list[dict[str, Any]]:
    """Search Datadog events.

    Search for events matching a query within a time range.

    Args:
        query: Event search query
        start: Start timestamp (Unix epoch)
        end: End timestamp (Unix epoch)
        limit: Maximum number of results (default: 100)
        tags: Filter by tags (optional)

    Returns:
        List of event objects
    """
    client = get_client()
    return await client.search_events(
        query=params.query, start=params.start, end=params.end, limit=params.limit, tags=params.tags
    )


class GetEventParams(BaseModel):
    event_id: int = Field(..., description="Event ID")


async def get_event(params: GetEventParams) -> dict[str, Any]:
    """Get event details.

    Retrieve details for a specific event.

    Args:
        event_id: Event ID to retrieve

    Returns:
        Event object with full details
    """
    client = get_client()
    return await client.get_event(event_id=params.event_id)


class CreateEventParams(BaseModel):
    title: str = Field(..., description="Event title")
    text: str = Field(..., description="Event text/content")
    alert_type: str = Field("info", description="Alert type (info, error, warning, success)")
    priority: Optional[str] = Field(None, description="Priority (normal, low)")
    tags: Optional[list[str]] = Field(None, description="Tags to attach")
    hostname: Optional[str] = Field(None, description="Hostname")


async def create_event(params: CreateEventParams) -> dict[str, Any]:
    """Create a Datadog event.

    Create a new event in Datadog.

    Args:
        title: Event title
        text: Event text/content
        alert_type: Alert type (info, error, warning, success)
        priority: Priority (optional)
        tags: Tags to attach (optional)
        hostname: Hostname (optional)

    Returns:
        Created event object
    """
    assert_write_allowed()
    client = get_client()
    return await client.create_event(
        title=params.title,
        text=params.text,
        alert_type=params.alert_type,
        priority=params.priority,
        tags=params.tags,
        hostname=params.hostname,
    )


class UpdateEventParams(BaseModel):
    event_id: int = Field(..., description="Event ID")
    title: Optional[str] = Field(None, description="New title")
    text: Optional[str] = Field(None, description="New text")


async def update_event(params: UpdateEventParams) -> dict[str, Any]:
    """Update a Datadog event.

    Update an existing event.

    Args:
        event_id: Event ID to update
        title: New title (optional)
        text: New text (optional)

    Returns:
        Updated event object
    """
    assert_write_allowed()
    client = get_client()
    return await client.update_event(event_id=params.event_id, title=params.title, text=params.text)


class DeleteEventParams(BaseModel):
    event_id: int = Field(..., description="Event ID")


async def delete_event(params: DeleteEventParams) -> dict[str, Any]:
    """Delete a Datadog event.

    Delete an event by ID.

    Args:
        event_id: Event ID to delete

    Returns:
        Deletion confirmation
    """
    assert_write_allowed()
    client = get_client()
    return await client.delete_event(event_id=params.event_id)
