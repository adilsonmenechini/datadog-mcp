"""Logs API methods."""

import asyncio
from datetime import datetime, timezone
from typing import Any, Optional

from datadog_api_client.v2.api.logs_api import LogsApi

from ..utils import parse_time


async def search_logs(
    self, query: str, time_range: str = "1h", limit: int = 50, cursor: Optional[str] = None
) -> dict[str, Any]:
    to_ts = int(datetime.now(timezone.utc).timestamp())
    from_ts = parse_time(time_range) if time_range else to_ts - 3600

    def _sync_search():
        api = LogsApi(self._api_client_v2)
        body = {
            "filter": {"query": query, "from": from_ts, "to": to_ts},
            "page": {"limit": limit},
            "sort": "@timestamp desc",
        }
        if cursor:
            body["page"]["cursor"] = cursor
        result = api.search_logs_events(body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_search)


async def aggregate_logs(
    self, query: str, compute: str = "count", time_range: str = "1h", group_by: Optional[str] = None
) -> dict[str, Any]:
    to_ts = int(datetime.now(timezone.utc).timestamp())
    from_ts = parse_time(time_range) if time_range else to_ts - 3600

    def _sync_aggregate():
        api = LogsApi(self._api_client_v2)
        body = {
            "filter": {"query": query, "from": from_ts, "to": to_ts},
            "compute": [{"aggregation": compute, "type": "total"}],
        }
        if group_by:
            body["group_by"] = [{"facet": group_by, "limit": 10}]
        result = api.aggregate_logs(body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_aggregate)
