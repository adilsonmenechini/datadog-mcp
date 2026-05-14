"""RUM API methods."""

import asyncio
from datetime import datetime, timezone
from typing import Any

from datadog_api_client.v2.api.rum_api import RUMApi

from ..utils import parse_time


async def search_rum_events(
    self, query: str, time_range: str = "1h", limit: int = 50
) -> dict[str, Any]:
    to_ts = int(datetime.now(timezone.utc).timestamp())
    from_ts = parse_time(time_range) if time_range else to_ts - 3600

    def _sync_search():
        api = RUMApi(self._api_client_v2)
        body = {
            "filter": {"query": query, "from": from_ts, "to": to_ts},
            "page": {"limit": limit},
            "sort": "@timestamp desc",
        }
        result = api.search_rum_events(body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_search)
