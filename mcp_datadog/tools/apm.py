"""APM tools for Datadog MCP server."""

from typing import Any, Optional
from pydantic import BaseModel, Field
from ..client import get_client


class SearchSpansParams(BaseModel):
    query: str = Field(..., description="Span search query")
    time_range: str = Field("1h", description="Time range")
    limit: int = Field(50, description="Max results")


async def search_spans(params: SearchSpansParams) -> list[dict[str, Any]]:
    """Search APM spans.

    Search for APM spans/traces for performance analysis.

    Args:
        query: Span search query (e.g. 'service:my-service @duration:>1000')
        time_range: Time range (e.g. '1h', '4h', '1d')
        limit: Maximum number of results (default: 50)

    Returns:
        List of span objects
    """
    from ..utils.formatters import format_span_results

    client = get_client()
    spans = await client.search_spans(
        query=params.query, time_range=params.time_range, limit=params.limit
    )
    return format_span_results(
        spans, {"query": params.query, "time_range": params.time_range, "total": len(spans)}
    )


class ListServicesParams(BaseModel):
    limit: int = Field(50, description="Max results")


async def list_services(params: ListServicesParams) -> list[dict[str, Any]]:
    """List APM services.

    Retrieve a list of services from APM.

    Args:
        limit: Maximum number of results (default: 50)

    Returns:
        List of service objects
    """
    client = get_client()
    return await client.list_services(limit=params.limit)


class GetServiceDefinitionParams(BaseModel):
    service_name: str = Field(..., description="Service name")


async def get_service_definition(params: GetServiceDefinitionParams) -> dict[str, Any]:
    """Get service definition.

    Retrieve service definition from the software catalog.

    Args:
        service_name: Service name to retrieve

    Returns:
        Service definition object
    """
    client = get_client()
    return await client.get_service_definition(service_name=params.service_name)


class GetServiceDependenciesParams(BaseModel):
    service_name: str = Field(..., description="Service name")
    from_time: int = Field(..., description="Start timestamp (Unix epoch)")
    to_time: Optional[int] = Field(None, description="End timestamp (Unix epoch)")


async def get_service_dependencies(params: GetServiceDependenciesParams) -> dict[str, Any]:
    """Get service dependencies.

    Retrieve service dependencies for an APM service showing the flow
    of requests between services.

    Args:
        service_name: Service name to get dependencies for
        from_time: Start timestamp (Unix epoch)
        to_time: End timestamp (Unix epoch, optional)

    Returns:
        Service dependencies graph
    """
    client = get_client()
    return await client.get_service_dependencies(
        service_name=params.service_name, from_ts=params.from_time, to_ts=params.to_time
    )


class GetAllServiceDependenciesParams(BaseModel):
    from_time: int = Field(..., description="Start timestamp (Unix epoch)")
    to_time: Optional[int] = Field(None, description="End timestamp (Unix epoch)")


async def get_all_service_dependencies(params: GetAllServiceDependenciesParams) -> dict[str, Any]:
    """Get all service dependencies.

    Retrieve all service dependencies showing the complete service map.

    Args:
        from_time: Start timestamp (Unix epoch)
        to_time: End timestamp (Unix epoch, optional)

    Returns:
        All service dependencies
    """
    client = get_client()
    return await client.get_all_service_dependencies(from_ts=params.from_time, to_ts=params.to_time)
