"""Incidents tools for Datadog MCP server."""

from typing import Any, Optional
from pydantic import BaseModel, Field
from ..client import get_client
from ..utils import assert_write_allowed


class GetIncidentsParams(BaseModel):
    page_size: int = Field(10, description="Number of results per page")
    page_number: int = Field(0, description="Page number")


async def get_incidents(params: GetIncidentsParams) -> list[dict[str, Any]]:
    """List Datadog incidents.

    Retrieve a paginated list of incidents in your Datadog organization.

    Args:
        page_size: Number of results per page (default: 10)
        page_number: Page number (0-indexed, default: 0)

    Returns:
        List of incident objects
    """
    client = get_client()
    return await client.list_incidents(page_size=params.page_size, page_number=params.page_number)


class GetIncidentParams(BaseModel):
    incident_id: str = Field(..., description="Incident ID")


async def get_incident(params: GetIncidentParams) -> dict[str, Any]:
    """Get details for a Datadog incident.

    Retrieve full details for a specific incident by ID.

    Args:
        incident_id: Incident ID to retrieve

    Returns:
        Incident object with full details
    """
    client = get_client()
    return await client.get_incident(incident_id=params.incident_id)


class SearchIncidentsParams(BaseModel):
    query: str = Field(..., description="Search query")


async def search_incidents(params: SearchIncidentsParams) -> list[dict[str, Any]]:
    """Search Datadog incidents.

    Search for incidents matching a query string.

    Args:
        query: Search query string

    Returns:
        List of matching incidents
    """
    client = get_client()
    return await client.search_incidents(query=params.query)


class CreateIncidentParams(BaseModel):
    title: str = Field(..., description="Incident title")
    customer_impact: Optional[dict[str, Any]] = Field(None, description="Customer impact details")


async def create_incident(params: CreateIncidentParams) -> dict[str, Any]:
    """Create a Datadog incident.

    Create a new incident in Datadog.

    Args:
        title: Incident title
        customer_impact: Customer impact details (optional)

    Returns:
        Created incident object
    """
    assert_write_allowed()
    client = get_client()
    return await client.create_incident(title=params.title, customer_impact=params.customer_impact)


class UpdateIncidentParams(BaseModel):
    incident_id: str = Field(..., description="Incident ID")
    title: Optional[str] = Field(None, description="New title")


async def update_incident(params: UpdateIncidentParams) -> dict[str, Any]:
    """Update a Datadog incident.

    Update an existing incident's properties.

    Args:
        incident_id: Incident ID to update
        title: New title (optional)

    Returns:
        Updated incident object
    """
    assert_write_allowed()
    client = get_client()
    return await client.update_incident(incident_id=params.incident_id, title=params.title)


class DeleteIncidentParams(BaseModel):
    incident_id: str = Field(..., description="Incident ID")


async def delete_incident(params: DeleteIncidentParams) -> dict[str, Any]:
    """Delete a Datadog incident.

    Delete an incident by ID.

    Args:
        incident_id: Incident ID to delete

    Returns:
        Deletion confirmation
    """
    assert_write_allowed()
    client = get_client()
    return await client.delete_incident(incident_id=params.incident_id)
