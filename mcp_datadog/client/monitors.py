"""Monitors API methods."""

import asyncio
from typing import Any, Optional

from datadog_api_client.v1.api.monitors_api import MonitorsApi as MonitorsApiV1


async def list_monitors(
    self, tags: str = "", name: str = "", monitor_tags: str = "", page_size: int = 50, page: int = 0
) -> list[dict[str, Any]]:
    def _sync_list():
        api = MonitorsApiV1(self._api_client_v1)
        result = api.list_monitors(
            tags=tags or None,
            name=name or None,
            monitor_tags=monitor_tags or None,
            page_size=page_size,
            page=page,
        )
        return [m.to_dict() for m in result]

    return await asyncio.to_thread(_sync_list)


async def get_monitor(self, monitor_id: int, group_states: str = "") -> dict[str, Any]:
    def _sync_get():
        api = MonitorsApiV1(self._api_client_v1)
        result = api.get_monitor(monitor_id=monitor_id, group_states=group_states or None)
        return result.to_dict()

    return await asyncio.to_thread(_sync_get)


async def create_monitor(
    self,
    name: str,
    type_: str,
    query: str,
    message: str = "",
    tags: Optional[list[str]] = None,
    priority: Optional[int] = None,
    options: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    def _sync_create():
        from datadog_api_client.v1.models import Monitor

        body = Monitor(name=name, type=type_, query=query, message=message, tags=tags or [])
        result = MonitorsApiV1(self._api_client_v1).create_monitor(body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_create)


async def update_monitor(
    self,
    monitor_id: int,
    name: Optional[str] = None,
    query: Optional[str] = None,
    message: Optional[str] = None,
    tags: Optional[list[str]] = None,
    priority: Optional[int] = None,
    options: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    def _sync_update():
        from datadog_api_client.v1.models import MonitorUpdateRequest

        body = MonitorUpdateRequest(
            name=name, query=query, message=message, tags=tags, priority=priority, options=options
        )
        result = MonitorsApiV1(self._api_client_v1).update_monitor(monitor_id=monitor_id, body=body)
        return result.to_dict()

    return await asyncio.to_thread(_sync_update)


async def delete_monitor(self, monitor_id: int, force: bool = False) -> dict[str, Any]:
    def _sync_delete():
        MonitorsApiV1(self._api_client_v1).delete_monitor(monitor_id=monitor_id, force=force)
        return {"deleted": True}

    return await asyncio.to_thread(_sync_delete)
