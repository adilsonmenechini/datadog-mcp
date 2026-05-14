"""MCP Resources for Datadog - exposes Datadog data as addressable resources."""

from typing import Any

import mcp.types as types


def register_resources(mcp):
    """Register all Datadog resources with the MCP server.

    This function must be called after the server is initialized to avoid
    circular import issues.
    """

    @mcp.resource("datadog://monitor/{monitor_id}")
    async def get_monitor_resource(monitor_id: str) -> dict[str, Any]:
        """Read a specific Datadog monitor by ID.

        Args:
            monitor_id: The monitor ID to retrieve

        Returns:
            Monitor configuration and current state
        """
        from .client import get_client

        client = get_client()
        return await client.get_monitor(monitor_id=int(monitor_id))

    @mcp.resource("datadog://metric/{metric_name}/metadata")
    async def get_metric_metadata_resource(metric_name: str) -> dict[str, Any]:
        """Read metadata for a Datadog metric.

        Args:
            metric_name: The full metric name (e.g. 'system.cpu.user')

        Returns:
            Metric metadata including description, type, unit
        """
        from .client import get_client

        client = get_client()
        return await client.get_metric_metadata(metric_name=metric_name)

    @mcp.resource("datadog://incident/{incident_id}")
    async def get_incident_resource(incident_id: str) -> dict[str, Any]:
        """Read a specific Datadog incident by ID.

        Args:
            incident_id: The incident ID to retrieve

        Returns:
            Incident details
        """
        from .client import get_client

        client = get_client()
        return await client.get_incident(incident_id=incident_id)

    @mcp.resource("datadog://service/{service_name}")
    async def get_service_resource(service_name: str) -> dict[str, Any]:
        """Read a specific APM service definition.

        Args:
            service_name: The service name to retrieve

        Returns:
            Service definition and configuration
        """
        from .client import get_client

        client = get_client()
        return await client.get_service_definition(service_name=service_name)

    return [
        "datadog://monitor/{monitor_id}",
        "datadog://metric/{metric_name}/metadata",
        "datadog://incident/{incident_id}",
        "datadog://service/{service_name}",
    ]