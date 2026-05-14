"""Fleet automation tools for Datadog MCP server."""

from typing import Any, Optional
from pydantic import BaseModel, Field
from ..utils import assert_write_allowed
import httpx
import os


def get_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": os.getenv("DD_API_KEY", ""),
        "DD-APPLICATION-KEY": os.getenv("DD_APP_KEY", ""),
    }


def get_url() -> str:
    return f"https://api.{os.getenv('DD_SITE', 'datadoghq.com')}"


class ListFleetAgentsParams(BaseModel):
    filter: Optional[str] = Field(None, description="Filter expression")
    page_size: int = Field(50, description="Page size")


async def list_fleet_agents(params: ListFleetAgentsParams) -> dict[str, Any]:
    """List fleet agents.

    Retrieve a list of fleet agents managed by Datadog Fleet Automation.

    Args:
        filter: Filter expression (optional)
        page_size: Number of results per page (default: 50)

    Returns:
        Dictionary containing list of fleet agents
    """
    url = f"{get_url()}/api/v2/fleet-agents"
    params_dict = {"page[size]": params.page_size}
    if params.filter:
        params_dict["filter"] = params.filter

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers(), params=params_dict)
        response.raise_for_status()
        return response.json()


class GetFleetAgentInfoParams(BaseModel):
    agent_id: str = Field(..., description="Agent ID")


async def get_fleet_agent_info(params: GetFleetAgentInfoParams) -> dict[str, Any]:
    """Get fleet agent info.

    Retrieve detailed information for a specific fleet agent.

    Args:
        agent_id: Agent ID to retrieve

    Returns:
        Dictionary containing agent details
    """
    url = f"{get_url()}/api/v2/fleet-agents/{params.agent_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()


class ListFleetClustersParams(BaseModel):
    page_size: int = Field(50, description="Page size")


async def list_fleet_clusters(params: ListFleetClustersParams) -> dict[str, Any]:
    """List fleet clusters.

    Retrieve a list of clusters managed by Datadog Fleet Automation.

    Args:
        page_size: Number of results per page (default: 50)

    Returns:
        Dictionary containing list of fleet clusters
    """
    url = f"{get_url()}/api/v2/fleet-clusters"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers=get_headers(), params={"page[size]": params.page_size}
        )
        response.raise_for_status()
        return response.json()


class ListFleetDeploymentsParams(BaseModel):
    page_size: int = Field(50, description="Page size")


async def list_fleet_deployments(params: ListFleetDeploymentsParams) -> dict[str, Any]:
    """List fleet deployments.

    Retrieve a list of fleet deployments.

    Args:
        page_size: Number of results per page (default: 50)

    Returns:
        Dictionary containing list of fleet deployments
    """
    url = f"{get_url()}/api/v2/fleet-deployments"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers=get_headers(), params={"page[size]": params.page_size}
        )
        response.raise_for_status()
        return response.json()


class CreateFleetDeploymentConfigureParams(BaseModel):
    filter: str = Field(..., description="Host filter")
    config: dict[str, Any] = Field(..., description="Configuration to apply")


async def create_fleet_deployment_configure(
    params: CreateFleetDeploymentConfigureParams,
) -> dict[str, Any]:
    """Create fleet deployment.

    Create a new fleet deployment for configuration management.

    Args:
        filter: Host filter expression
        config: Configuration to apply

    Returns:
        Dictionary containing created deployment info
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v2/fleet-deployments"

    body = {"filter": params.filter, "config": params.config}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers(), json=body)
        response.raise_for_status()
        return response.json()


class CancelFleetDeploymentParams(BaseModel):
    deployment_id: str = Field(..., description="Deployment ID")


async def cancel_fleet_deployment(params: CancelFleetDeploymentParams) -> dict[str, Any]:
    """Cancel a fleet deployment.

    Cancel a running fleet deployment.

    Args:
        deployment_id: Deployment ID to cancel

    Returns:
        Dictionary containing cancellation confirmation
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v2/fleet-deployments/{params.deployment_id}/cancel"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
