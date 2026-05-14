"""SLOs API methods."""

import asyncio
from typing import Any, Optional

from datadog_api_client.v1.api.service_level_objectives_api import ServiceLevelObjectivesApi


async def list_slos(
    self, tags: Optional[str] = None, query: Optional[str] = None, limit: int = 100, offset: int = 0
) -> list[dict[str, Any]]:
    def _sync_list():
        result = ServiceLevelObjectivesApi(self._api_client_v1).list_slos(
            limit=limit, offset=offset
        )
        return [s.to_dict() for s in (result.data or [])]

    return await asyncio.to_thread(_sync_list)
