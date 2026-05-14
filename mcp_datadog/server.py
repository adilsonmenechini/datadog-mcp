"""Main MCP server for Datadog."""

from typing import Any

from mcp.server.fastmcp import FastMCP

# Support both package import and direct execution (mcp dev)
try:
    from .config import validate_config, config as _config
    from .tool_registry import registry, search_tools_handler
    from .tools.metrics import (
        query_metrics,
        get_metrics,
        get_metric_metadata,
        list_active_metrics,
        list_metric_tags,
    )
    from .tools.monitors import (
        get_monitors,
        get_monitor,
        create_monitor,
        update_monitor,
        delete_monitor,
        validate_monitor,
        mute_monitor,
    )
    from .tools.logs import search_logs, aggregate_logs, send_logs, search_audit_logs
    from .tools.incidents import (
        get_incidents,
        get_incident,
        search_incidents,
        create_incident,
        update_incident,
        delete_incident,
    )
    from .tools.apm import (
        search_spans,
        list_services,
        get_service_definition,
        get_service_dependencies,
        get_all_service_dependencies,
    )
    from .tools.synthetics import (
        list_synthetics,
        get_synthetics_result,
        trigger_synthetics,
        create_synthetics_test,
        update_synthetics_test,
        delete_synthetics_test,
    )
    from .tools.fleet import (
        list_fleet_agents,
        get_fleet_agent_info,
        list_fleet_clusters,
        list_fleet_deployments,
        create_fleet_deployment_configure,
        cancel_fleet_deployment,
    )
    from .tools.error_tracking import list_error_trackers, get_error_tracker, search_error_events
    from .tools.events import search_events, get_event, create_event, update_event, delete_event
    from .prompts import register_prompts
    from .resources import register_resources
except ImportError:
    # Fallback for mcp dev command - use absolute imports
    from mcp_datadog.config import validate_config, config as _config
    from mcp_datadog.tool_registry import registry, search_tools_handler
    from mcp_datadog.tools.metrics import (
        query_metrics,
        get_metrics,
        get_metric_metadata,
        list_active_metrics,
        list_metric_tags,
    )
    from mcp_datadog.tools.monitors import (
        get_monitors,
        get_monitor,
        create_monitor,
        update_monitor,
        delete_monitor,
        validate_monitor,
        mute_monitor,
    )
    from mcp_datadog.tools.logs import search_logs, aggregate_logs, send_logs, search_audit_logs
    from mcp_datadog.tools.incidents import (
        get_incidents,
        get_incident,
        search_incidents,
        create_incident,
        update_incident,
        delete_incident,
    )
    from mcp_datadog.tools.apm import (
        search_spans,
        list_services,
        get_service_definition,
        get_service_dependencies,
        get_all_service_dependencies,
    )
    from mcp_datadog.tools.synthetics import (
        list_synthetics,
        get_synthetics_result,
        trigger_synthetics,
        create_synthetics_test,
        update_synthetics_test,
        delete_synthetics_test,
    )
    from mcp_datadog.tools.fleet import (
        list_fleet_agents,
        get_fleet_agent_info,
        list_fleet_clusters,
        list_fleet_deployments,
        create_fleet_deployment_configure,
        cancel_fleet_deployment,
    )
    from mcp_datadog.tools.error_tracking import list_error_trackers, get_error_tracker, search_error_events
    from mcp_datadog.tools.events import search_events, get_event, create_event, update_event, delete_event
    from mcp_datadog.prompts import register_prompts
    from mcp_datadog.resources import register_resources

# Initialize FastMCP server
mcp = FastMCP(
    name="datadog",
    instructions="Datadog MCP server - 165+ tools for metrics, monitors, logs, APM, RUM, incidents, CI/CD, and more",
)

# Validate config before starting
# When running via 'mcp dev', the module is imported directly which triggers
# the except ImportError branch. We check if keys exist before validating.
if _config.api_key and _config.app_key:
    validate_config()

# Register prompts
register_prompts(mcp)

# Register resources
register_resources(mcp)


def _register_tool(name: str, description: str, handler: Any, category: str) -> None:
    """Register a tool with category-based filtering."""
    registry.register(name, description, category)
    if registry.is_enabled(category):
        mcp.tool(name=name, description=description)(handler)


# --- Metrics Tools ---
_register_tool(
    "query-metrics", "Query time-series metric data from Datadog.", query_metrics, "metrics"
)
_register_tool(
    "get-metrics", "Search for available Datadog metrics by name pattern.", get_metrics, "metrics"
)
_register_tool(
    "get-metric-metadata",
    "Get metadata for a specific Datadog metric.",
    get_metric_metadata,
    "metrics",
)
_register_tool(
    "list-active-metrics", "List active metrics from a given time.", list_active_metrics, "metrics"
)
_register_tool("list-metric-tags", "List tags for a specific metric.", list_metric_tags, "metrics")

# --- Monitor Tools ---
_register_tool(
    "get-monitors", "List Datadog monitors with optional filtering.", get_monitors, "monitors"
)
_register_tool(
    "get-monitor",
    "Get detailed information about a specific Datadog monitor.",
    get_monitor,
    "monitors",
)
_register_tool("create-monitor", "Create a new Datadog monitor.", create_monitor, "monitors")
_register_tool("update-monitor", "Update an existing Datadog monitor.", update_monitor, "monitors")
_register_tool("delete-monitor", "Delete a Datadog monitor.", delete_monitor, "monitors")
_register_tool("validate-monitor", "Validate a monitor definition.", validate_monitor, "monitors")
_register_tool("mute-monitor", "Mute a Datadog monitor.", mute_monitor, "monitors")

# --- Logs Tools ---
_register_tool("search-logs", "Search Datadog logs.", search_logs, "logs")
_register_tool("aggregate-logs", "Aggregate Datadog logs.", aggregate_logs, "logs")
_register_tool("send-logs", "Send logs to Datadog.", send_logs, "logs")
_register_tool("search-audit-logs", "Search Datadog audit logs.", search_audit_logs, "logs")

# --- Incident Tools ---
_register_tool("get-incidents", "List Datadog incidents.", get_incidents, "incidents")
_register_tool("get-incident", "Get incident details.", get_incident, "incidents")
_register_tool("search-incidents", "Search incidents.", search_incidents, "incidents")
_register_tool("create-incident", "Create a Datadog incident.", create_incident, "incidents")
_register_tool("update-incident", "Update a Datadog incident.", update_incident, "incidents")
_register_tool("delete-incident", "Delete a Datadog incident.", delete_incident, "incidents")

# --- APM Tools ---
_register_tool("search-spans", "Search APM spans.", search_spans, "apm")
_register_tool("list-services", "List APM services.", list_services, "apm")
_register_tool("get-service-definition", "Get service definition.", get_service_definition, "apm")
_register_tool(
    "get-service-dependencies", "Get service dependencies.", get_service_dependencies, "apm"
)
_register_tool(
    "get-all-service-dependencies",
    "Get all service dependencies.",
    get_all_service_dependencies,
    "apm",
)

# --- Synthetics Tools ---
_register_tool("list-synthetics", "List synthetics tests.", list_synthetics, "synthetics")
_register_tool(
    "get-synthetics-result", "Get synthetics test results.", get_synthetics_result, "synthetics"
)
_register_tool("trigger-synthetics", "Trigger synthetics tests.", trigger_synthetics, "synthetics")
_register_tool(
    "create-synthetics-test", "Create a synthetics test.", create_synthetics_test, "synthetics"
)
_register_tool(
    "update-synthetics-test", "Update a synthetics test.", update_synthetics_test, "synthetics"
)
_register_tool(
    "delete-synthetics-test", "Delete a synthetics test.", delete_synthetics_test, "synthetics"
)

# --- Fleet Tools ---
_register_tool("list-fleet-agents", "List fleet agents.", list_fleet_agents, "fleet")
_register_tool("get-fleet-agent-info", "Get fleet agent info.", get_fleet_agent_info, "fleet")
_register_tool("list-fleet-clusters", "List fleet clusters.", list_fleet_clusters, "fleet")
_register_tool("list-fleet-deployments", "List fleet deployments.", list_fleet_deployments, "fleet")
_register_tool(
    "create-fleet-deployment-configure",
    "Create fleet deployment.",
    create_fleet_deployment_configure,
    "fleet",
)
_register_tool(
    "cancel-fleet-deployment", "Cancel a fleet deployment.", cancel_fleet_deployment, "fleet"
)

# --- Error Tracking Tools ---
_register_tool("list-error-trackers", "List error trackers.", list_error_trackers, "error_tracking")
_register_tool(
    "get-error-tracker", "Get error tracker details.", get_error_tracker, "error_tracking"
)
_register_tool("search-error-events", "Search error events.", search_error_events, "error_tracking")

# --- Events Tools ---
_register_tool("search-events", "Search Datadog events.", search_events, "events")
_register_tool("get-event", "Get event details.", get_event, "events")
_register_tool("create-event", "Create a Datadog event.", create_event, "events")
_register_tool("update-event", "Update a Datadog event.", update_event, "events")
_register_tool("delete-event", "Delete a Datadog event.", delete_event, "events")


# --- Meta tool ---
@mcp.tool()
def search_tools(query: str = "") -> dict[str, Any]:
    """Discover available tools by natural language query."""
    return {"tools": search_tools_handler(query)}


def main() -> None:
    """Main entry point."""
    mcp.run()


if __name__ == "__main__":
    main()