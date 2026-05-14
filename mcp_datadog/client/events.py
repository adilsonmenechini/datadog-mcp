"""Events API methods."""

import asyncio
from typing import Any, Optional

from datadog_api_client.v1.api.events_api import EventsApi as EventsApiV1


async def search_events(
    self, query: str, start: int, end: int, limit: int = 100, tags: Optional[str] = None
) -> list[dict[str, Any]]:
    def _sync_search():
        return [
            e.to_dict()
            for e in (
                EventsApiV1(self._api_client_v1)
                .search_events(start=start, end=end, limit=limit, tags=tags)
                .events
                or []
            )
        ]

    return await asyncio.to_thread(_sync_search)


async def get_event(self, event_id: int) -> dict[str, Any]:
    def _sync_get():
        return EventsApiV1(self._api_client_v1).get_event(event_id=event_id).to_dict()

    return await asyncio.to_thread(_sync_get)


async def create_event(
    self,
    title: str,
    text: str,
    alert_type: str = "info",
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
    hostname: Optional[str] = None,
) -> dict[str, Any]:
    def _sync_create():
        body = {"title": title, "text": text, "alert_type": alert_type}
        if priority:
            body["priority"] = priority
        if tags:
            body["tags"] = tags
        if hostname:
            body["hostname"] = hostname
        return EventsApiV1(self._api_client_v1).create_event(body).to_dict()

    return await asyncio.to_thread(_sync_create)


async def update_event(
    self, event_id: int, title: Optional[str] = None, text: Optional[str] = None
) -> dict[str, Any]:
    def _sync_update():
        body = {}
        if title is not None:
            body["title"] = title
        if text is not None:
            body["text"] = text
        return EventsApiV1(self._api_client_v1).update_event(event_id=event_id, body=body).to_dict()

    return await asyncio.to_thread(_sync_update)


async def delete_event(self, event_id: int) -> dict[str, Any]:
    def _sync_delete():
        EventsApiV1(self._api_client_v1).delete_event(event_id=event_id)
        return {"deleted": True}

    return await asyncio.to_thread(_sync_delete)
