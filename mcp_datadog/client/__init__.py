"""Datadog API client - unified interface."""

import logging
from typing import Optional

from .core import DatadogClient
from ..utils import parse_time, get_headers, get_datadog_url

# Import all method modules to extend the class
from . import apm, events, incidents, logs, metrics, monitors, rum, slost, error_tracking

# Configure logging
logger = logging.getLogger(__name__)

# Extend DatadogClient with all API methods
# Monitors
DatadogClient.list_monitors = monitors.list_monitors
DatadogClient.get_monitor = monitors.get_monitor
DatadogClient.create_monitor = monitors.create_monitor
DatadogClient.update_monitor = monitors.update_monitor
DatadogClient.delete_monitor = monitors.delete_monitor

# Metrics
DatadogClient.query_metrics = metrics.query_metrics
DatadogClient.list_metrics = metrics.list_metrics
DatadogClient.get_metric_metadata = metrics.get_metric_metadata

# APM
DatadogClient.list_services = apm.list_services
DatadogClient.get_service_definition = apm.get_service_definition
DatadogClient.get_service_dependencies = apm.get_service_dependencies
DatadogClient.get_all_service_dependencies = apm.get_all_service_dependencies
DatadogClient.search_spans = apm.search_spans

# Logs
DatadogClient.search_logs = logs.search_logs
DatadogClient.aggregate_logs = logs.aggregate_logs

# Incidents
DatadogClient.list_incidents = incidents.list_incidents
DatadogClient.get_incident = incidents.get_incident
DatadogClient.search_incidents = incidents.search_incidents
DatadogClient.create_incident = incidents.create_incident
DatadogClient.update_incident = incidents.update_incident
DatadogClient.delete_incident = incidents.delete_incident

# SLOs
DatadogClient.list_slos = slost.list_slos

# RUM
DatadogClient.search_rum_events = rum.search_rum_events

# Events
DatadogClient.search_events = events.search_events
DatadogClient.get_event = events.get_event
DatadogClient.create_event = events.create_event
DatadogClient.update_event = events.update_event
DatadogClient.delete_event = events.delete_event

# Error Tracking
DatadogClient.list_error_trackers = error_tracking.list_error_trackers
DatadogClient.get_error_tracker = error_tracking.get_error_tracker
DatadogClient.search_error_events = error_tracking.search_error_events

# Export the client, factory function, and utility functions
__all__ = [
    "DatadogClient",
    "get_client",
    "parse_time",
    "get_headers",
    "get_datadog_url",
]


# Global client instance
_client: Optional[DatadogClient] = None


def get_client() -> DatadogClient:
    """Get or create global client instance."""
    global _client
    if _client is None:
        _client = DatadogClient()
    return _client
