"""APM API methods."""

from datetime import datetime, timezone
from typing import Any, Optional

from ..utils import parse_time


async def list_services(self, limit: int = 50) -> list[dict[str, Any]]:
    result = await self._request("GET", "/api/v1/services", params={"limit": limit})
    return result


async def get_service_definition(self, service_name: str) -> dict[str, Any]:
    result = await self._request("GET", f"/api/v2/services/definitions/{service_name}")
    return result


async def get_service_dependencies(
    self, service_name: str, from_ts: int, to_ts: Optional[int] = None
) -> dict[str, Any]:
    params: dict[str, Any] = {"from": from_ts}
    if to_ts:
        params["to"] = to_ts
    result = await self._request(
        "GET", f"/api/v2/services/{service_name}/dependencies", params=params
    )
    return result


async def get_all_service_dependencies(
    self, from_ts: int, to_ts: Optional[int] = None
) -> dict[str, Any]:
    params: dict[str, Any] = {"from": from_ts}
    if to_ts:
        params["to"] = to_ts
    result = await self._request("GET", "/api/v2/services/dependencies", params=params)
    return result


async def search_spans(
    self, query: str, time_range: str = "1h", limit: int = 50
) -> list[dict[str, Any]]:
    from datadog_api_client.v2.api.spans_api import SpansApi

    to_ts = int(datetime.now(timezone.utc).timestamp())
    from_ts = parse_time(time_range) if time_range else to_ts - 3600

    def _sync_search():
        api = SpansApi(self._api_client_v2)
        body = {"filter": {"query": query, "from": from_ts, "to": to_ts}, "page": {"limit": limit}}
        result = api.search_spans(body)
        return [s.to_dict() for s in (result.data or [])]

    import asyncio

    return await asyncio.to_thread(_sync_search)
