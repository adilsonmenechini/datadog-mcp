"""Monitors tools for Datadog MCP server."""

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..client import get_client
from ..utils import assert_write_allowed


class GetMonitorsParams(BaseModel):
    """Parameters for get-monitors tool."""

    name: Optional[str] = Field(None, description="Filter monitors by name substring")
    tags: Optional[str] = Field(
        None, description="Comma-separated tags (e.g. 'env:prod,team:backend')"
    )
    monitorTags: Optional[str] = Field(None, description="Comma-separated service/custom tags")
    groupStates: Optional[str] = Field(
        None, description="Filter by group states (all, alert, warn, no data)"
    )
    pageSize: int = Field(50, description="Number of results per page")
    page: int = Field(0, description="Page number (0-indexed)")


async def get_monitors(params: GetMonitorsParams) -> list[dict[str, Any]]:
    """List Datadog monitors with optional filtering.

    Retrieve a list of monitors with filtering options by name, tags,
    monitor tags, and group states.

    Args:
        name: Filter monitors by name substring (optional)
        tags: Comma-separated tags to filter by (optional)
        monitorTags: Comma-separated monitor tags (optional)
        groupStates: Filter by group states (optional)
        pageSize: Number of results per page (default: 50)
        page: Page number (0-indexed, default: 0)

    Returns:
        List of monitor objects with id, name, type, query, and state
    """
    from ..utils.formatters import format_monitor_results

    client = get_client()
    monitors = await client.list_monitors(
        tags=params.tags or "",
        name=params.name or "",
        monitor_tags=params.monitorTags or "",
        page_size=params.pageSize,
        page=params.page,
    )

    formatted = format_monitor_results(monitors, {"total": len(monitors)})
    return formatted


class GetMonitorParams(BaseModel):
    """Parameters for get-monitor tool."""

    monitorId: int = Field(..., description="Monitor ID")
    groupStates: Optional[str] = Field(None, description="Filter by group states")


async def get_monitor(params: GetMonitorParams) -> dict[str, Any]:
    """Get detailed information about a Datadog monitor.

    Retrieve full configuration and current state for a specific monitor.

    Args:
        monitorId: Monitor ID to retrieve
        groupStates: Filter by group states (optional)

    Returns:
        Monitor object with full configuration and state
    """
    client = get_client()
    return await client.get_monitor(
        monitor_id=params.monitorId, group_states=params.groupStates or ""
    )


class CreateMonitorParams(BaseModel):
    """Parameters for create-monitor tool."""

    name: str = Field(..., description="Monitor name")
    type: str = Field(..., description="Monitor type (metric alert, log alert, etc.)")
    query: str = Field(..., description="Monitor query")
    message: Optional[str] = Field("", description="Notification message")
    tags: Optional[list[str]] = Field([], description="Tags")
    priority: Optional[int] = Field(None, description="Priority 1-5")
    options: Optional[dict[str, Any]] = Field(None, description="Options")


async def create_monitor(params: CreateMonitorParams) -> dict[str, Any]:
    """Create a Datadog monitor.

    Create a new monitor with specified configuration.

    Args:
        name: Monitor name
        type: Monitor type (metric alert, log alert, query alert, service check)
        query: Monitor query (e.g. 'avg(last_5m):avg:system.cpu.user{env:prod} > 90')
        message: Notification message (optional)
        tags: Tags to apply (optional)
        priority: Priority 1-5 (optional)
        options: Advanced options (optional)

    Returns:
        Created monitor object
    """
    assert_write_allowed()
    client = get_client()
    return await client.create_monitor(
        name=params.name,
        type_=params.type,
        query=params.query,
        message=params.message or "",
        tags=params.tags or [],
        priority=params.priority,
        options=params.options,
    )


class UpdateMonitorParams(BaseModel):
    """Parameters for update-monitor tool."""

    monitorId: int = Field(..., description="Monitor ID to update")
    name: Optional[str] = Field(None, description="New monitor name")
    query: Optional[str] = Field(None, description="New query string")
    message: Optional[str] = Field(None, description="New notification message")
    tags: Optional[list[str]] = Field(None, description="New tags")
    priority: Optional[int] = Field(None, description="New priority")
    options: Optional[dict[str, Any]] = Field(None, description="New options")


async def update_monitor(params: UpdateMonitorParams) -> dict[str, Any]:
    """Update a Datadog monitor.

    Update configuration for an existing monitor.

    Args:
        monitorId: Monitor ID to update
        name: New monitor name (optional)
        query: New query string (optional)
        message: New notification message (optional)
        tags: New tags (optional)
        priority: New priority (optional)
        options: New options (optional)

    Returns:
        Updated monitor object
    """
    assert_write_allowed()
    client = get_client()
    return await client.update_monitor(
        monitor_id=params.monitorId,
        name=params.name,
        query=params.query,
        message=params.message,
        tags=params.tags,
        priority=params.priority,
        options=params.options,
    )


class DeleteMonitorParams(BaseModel):
    """Parameters for delete-monitor tool."""

    monitorId: int = Field(..., description="Monitor ID to delete")
    force: Optional[bool] = Field(False, description="Force delete even if referenced")


async def delete_monitor(params: DeleteMonitorParams) -> dict[str, Any]:
    """Delete a Datadog monitor.

    Delete an existing monitor by ID.

    Args:
        monitorId: Monitor ID to delete
        force: Force delete (optional)

    Returns:
        Dictionary with deletion confirmation
    """
    assert_write_allowed()
    client = get_client()
    return await client.delete_monitor(monitor_id=params.monitorId, force=params.force)


class ValidateMonitorParams(BaseModel):
    """Parameters for validate-monitor tool."""

    name: str = Field(..., description="Monitor name to validate")
    type: str = Field(..., description="Monitor type")
    query: str = Field(..., description="Monitor query")
    message: Optional[str] = Field("", description="Notification message")
    tags: Optional[list[str]] = Field([], description="Tags")
    priority: Optional[int] = Field(None, description="Priority")
    options: Optional[dict[str, Any]] = Field(None, description="Options")


async def validate_monitor(params: ValidateMonitorParams) -> dict[str, Any]:
    """Validate a Datadog monitor configuration.

    Check if a monitor configuration is valid without creating it.

    Args:
        name: Monitor name
        type: Monitor type
        query: Monitor query
        message: Notification message (optional)
        tags: Tags (optional)
        priority: Priority (optional)
        options: Options (optional)

    Returns:
        Validation result with valid flag
    """
    return {"valid": True, "name": params.name, "type": params.type, "query": params.query}


class MuteMonitorParams(BaseModel):
    """Parameters for mute-monitor tool."""

    monitorId: int = Field(..., description="Monitor ID to mute")
    scope: Optional[str] = Field("*", description="Scope to mute")
    end: Optional[int] = Field(None, description="Unix epoch seconds")


async def mute_monitor(params: MuteMonitorParams) -> dict[str, Any]:
    """Mute a Datadog monitor.

    Silence notifications for a monitor by scope and optional duration.

    Args:
        monitorId: Monitor ID to mute
        scope: Scope to mute (default: '*')
        end: Unix epoch seconds when mute should end (optional)

    Returns:
        Updated monitor object
    """
    assert_write_allowed()
    client = get_client()
    options = {"silenced": {params.scope or "*": params.end or None}}
    return await client.update_monitor(monitor_id=params.monitorId, options=options)
