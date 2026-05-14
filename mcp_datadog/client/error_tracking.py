"""Error Tracking API methods."""

from datetime import datetime, timezone
from typing import Any

from ..utils import parse_time


async def list_error_trackers(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
    result = await self._request(
        "GET", "/api/v2/error_trackers", params={"limit": limit, "offset": offset}
    )
    return result.get("data", [])


async def get_error_tracker(self, tracker_id: str) -> dict[str, Any]:
    result = await self._request("GET", f"/api/v2/error_trackers/{tracker_id}")
    return result.get("data", {})


async def search_error_events(
    self, query: str, time_range: str = "1h", limit: int = 50
) -> dict[str, Any]:
    to_ts = int(datetime.now(timezone.utc).timestamp())
    from_ts = parse_time(time_range) if time_range else to_ts - 3600

    body = {
        "filter": {"query": query, "from": from_ts, "to": to_ts},
        "page": {"limit": limit},
        "sort": "-@timestamp",
    }
    return await self._request("POST", "/api/v2/error_events", json_data=body)
