"""Metrics API methods."""

import asyncio
from typing import Any

from datadog_api_client.v1.api.metrics_api import MetricsApi as MetricsApiV1


async def query_metrics(self, query: str, _from: int, to: int) -> dict[str, Any]:
    def _sync_query():
        result = MetricsApiV1(self._api_client_v1).query_metrics(_from=_from, to=to, query=query)
        return result.to_dict()

    return await asyncio.to_thread(_sync_query)


async def list_metrics(self, q: str = "", limit: int = 500) -> dict[str, Any]:
    def _sync_list():
        result = MetricsApiV1(self._api_client_v1).list_metrics(q=q or None, limit=limit)
        return result.to_dict()

    return await asyncio.to_thread(_sync_list)


async def get_metric_metadata(self, metric_name: str) -> dict[str, Any]:
    def _sync_get():
        result = MetricsApiV1(self._api_client_v1).get_metric_metadata(metric_name=metric_name)
        return result.to_dict()

    return await asyncio.to_thread(_sync_get)
