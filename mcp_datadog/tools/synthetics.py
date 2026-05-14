"""Synthetics tools for Datadog MCP server."""

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


class ListSyntheticsParams(BaseModel):
    limit: int = Field(50, description="Max results")


async def list_synthetics(params: ListSyntheticsParams) -> list[dict[str, Any]]:
    """List synthetics tests.

    Retrieve a list of synthetic tests configured in Datadog.

    Args:
        limit: Maximum number of results to return (default: 50)

    Returns:
        List of synthetics test objects
    """
    url = f"{get_url()}/api/v1/synthetics/tests"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers(), params={"limit": params.limit})
        response.raise_for_status()
        return response.json().get("tests", [])


class GetSyntheticsResultParams(BaseModel):
    public_id: str = Field(..., description="Test public ID")


async def get_synthetics_result(params: GetSyntheticsResultParams) -> dict[str, Any]:
    """Get synthetics test results.

    Retrieve recent results for a specific synthetics test.

    Args:
        public_id: Public ID of the synthetics test

    Returns:
        Dictionary containing test results
    """
    url = f"{get_url()}/api/v1/synthetics/tests/{params.public_id}/results"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()


class TriggerSyntheticsParams(BaseModel):
    public_ids: list[str] = Field(..., description="Test public IDs to trigger")


async def trigger_synthetics(params: TriggerSyntheticsParams) -> dict[str, Any]:
    """Trigger synthetics tests.

    Manually trigger one or more synthetics tests.

    Args:
        public_ids: List of public IDs of tests to trigger

    Returns:
        Dictionary containing trigger results
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v1/synthetics/tests/trigger"

    body = {"tests": [{"public_id": pid} for pid in params.public_ids]}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers(), json=body)
        response.raise_for_status()
        return response.json()


class CreateSyntheticsTestParams(BaseModel):
    type: str = Field(..., description="Test type")
    request_url: str = Field(..., description="URL to test")
    name: str = Field(..., description="Test name")


async def create_synthetics_test(params: CreateSyntheticsTestParams) -> dict[str, Any]:
    """Create a synthetics test.

    Create a new synthetic test for monitoring endpoint availability.

    Args:
        type: Test type (api, browser, etc.)
        request_url: URL to test
        name: Test name

    Returns:
        Created test object
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v1/synthetics/tests"

    body = {
        "type": params.type,
        "request": {"url": params.request_url},
        "name": params.name,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_headers(), json=body)
        response.raise_for_status()
        return response.json()


class UpdateSyntheticsTestParams(BaseModel):
    public_id: str = Field(..., description="Test public ID")
    name: Optional[str] = Field(None, description="New name")


async def update_synthetics_test(params: UpdateSyntheticsTestParams) -> dict[str, Any]:
    """Update a synthetics test.

    Update configuration for an existing synthetics test.

    Args:
        public_id: Public ID of test to update
        name: New test name (optional)

    Returns:
        Updated test object
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v1/synthetics/tests/{params.public_id}"

    body = {}
    if params.name:
        body["name"] = params.name

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=get_headers(), json=body)
        response.raise_for_status()
        return response.json()


class DeleteSyntheticsTestParams(BaseModel):
    public_id: str = Field(..., description="Test public ID")


async def delete_synthetics_test(params: DeleteSyntheticsTestParams) -> dict[str, Any]:
    """Delete a synthetics test.

    Delete a synthetics test permanently.

    Args:
        public_id: Public ID of test to delete

    Returns:
        Deletion confirmation
    """
    assert_write_allowed()
    url = f"{get_url()}/api/v1/synthetics/tests/{params.public_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=get_headers())
        response.raise_for_status()
        return {"deleted": True}
