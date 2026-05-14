"""Core Datadog API client using official datadog-api-client library."""

import asyncio
import logging
import os
from typing import Any, Optional

import httpx
from datadog_api_client import Configuration
from datadog_api_client.v1 import ApiClient as ApiClientV1
from datadog_api_client.v2 import ApiClient as ApiClientV2

from ..utils import get_headers, get_datadog_url

logger = logging.getLogger(__name__)


class DatadogClient:
    """Datadog API client using official datadog-api-client library with httpx fallback."""

    def __init__(self):
        self.configuration = Configuration()
        self.configuration.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY", "")
        self.configuration.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY", "")

        self._http_client: Optional[httpx.AsyncClient] = None

    def _get_http_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self._http_client

    @property
    def _api_client_v1(self) -> ApiClientV1:
        if self.__dict__.get("_ApiClientV1") is None:
            self.__dict__["_ApiClientV1"] = ApiClientV1(self.configuration)
        return self.__dict__["_ApiClientV1"]

    @property
    def _api_client_v2(self) -> ApiClientV2:
        if self.__dict__.get("_ApiClientV2") is None:
            self.__dict__["_ApiClientV2"] = ApiClientV2(self.configuration)
        return self.__dict__["_ApiClientV2"]

    async def close(self):
        """Close API clients."""
        if "_ApiClientV1" in self.__dict__:
            await asyncio.to_thread(self.__dict__["_ApiClientV1"].close)
        if "_ApiClientV2" in self.__dict__:
            await asyncio.to_thread(self.__dict__["_ApiClientV2"].close)
        if self._http_client:
            await self._http_client.close()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make HTTP request to Datadog API using httpx."""
        client = self._get_http_client()
        url = f"{get_datadog_url()}{path}"
        response = await client.request(
            method, url, headers=get_headers(), params=params, json=json_data
        )
        response.raise_for_status()
        return response.json()


_client: Optional[DatadogClient] = None


def get_client() -> DatadogClient:
    global _client
    if _client is None:
        _client = DatadogClient()
    return _client
