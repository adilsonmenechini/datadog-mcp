"""Incidents API methods."""

import asyncio
from typing import Any, Optional

from datadog_api_client.v2.api.incidents_api import IncidentsApi


async def list_incidents(self, page_size: int = 10, page_number: int = 0) -> list[dict[str, Any]]:
    def _sync_list():
        result = IncidentsApi(self._api_client_v2).list_incidents(
            page_size=page_size, page_number=page_number
        )
        return [i.to_dict() for i in (result.data or [])]

    return await asyncio.to_thread(_sync_list)


async def get_incident(self, incident_id: str) -> dict[str, Any]:
    def _sync_get():
        return IncidentsApi(self._api_client_v2).get_incident(incident_id=incident_id).to_dict()

    return await asyncio.to_thread(_sync_get)


async def search_incidents(self, query: str) -> list[dict[str, Any]]:
    def _sync_search():
        result = IncidentsApi(self._api_client_v2).search_incidents(
            body={"filter": {"query": query}}
        )
        return [i.to_dict() for i in (result.data or [])]

    return await asyncio.to_thread(_sync_search)


async def create_incident(
    self, title: str, customer_impact: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    def _sync_create():
        body = {"data": {"attributes": {"title": title}}}
        if customer_impact:
            body["data"]["attributes"]["customer_impact"] = customer_impact
        result = IncidentsApi(self._api_client_v2).create_incident(body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_create)


async def update_incident(self, incident_id: str, title: Optional[str] = None) -> dict[str, Any]:
    def _sync_update():
        body = {"data": {"attributes": {"title": title}}}
        result = IncidentsApi(self._api_client_v2).update_incident(
            incident_id=incident_id, body=body
        )
        return result.to_dict()

    return await asyncio.to_thread(_sync_update)


async def delete_incident(self, incident_id: str) -> dict[str, Any]:
    def _sync_delete():
        IncidentsApi(self._api_client_v2).delete_incident(incident_id=incident_id)
        return {"deleted": True}

    return await asyncio.to_thread(_sync_delete)
