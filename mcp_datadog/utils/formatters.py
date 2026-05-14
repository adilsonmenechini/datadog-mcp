"""Output formatters for Datadog MCP tools."""

from typing import Any


def format_log_results(logs: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format log results as human-readable text."""
    lines = []

    # Header with metadata
    lines.append("=== Log Search Results ===")
    lines.append(f"Query: {metadata.get('query', 'N/A')}")
    lines.append(f"Time Range: {metadata.get('time_range', 'N/A')}")
    lines.append(f"Total Results: {metadata.get('total', len(logs))}")

    if logs:
        lines.append(f"Showing: {len(logs)} entries")
        lines.append("")

        # Format each log entry
        for i, log in enumerate(logs[:50]):  # Limit display
            timestamp = log.get("@timestamp", "N/A")
            service = log.get("service", "unknown")
            host = log.get("host", "")
            message = log.get("message", log.get("msg", ""))

            # Truncate long messages
            if len(message) > 200:
                message = message[:200] + "..."

            lines.append(f"[{i + 1}] [{timestamp}] [{service}] {host}: {message}")

        if len(logs) > 50:
            lines.append(f"... and {len(logs) - 50} more entries")
    else:
        lines.append("No log entries found matching the query.")

    return "\n".join(lines)


def format_monitor_results(monitors: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format monitor results as human-readable text."""
    lines = []

    lines.append("=== Monitor Results ===")
    lines.append(f"Total Monitors: {metadata.get('total', len(monitors))}")

    if monitors:
        lines.append("")
        for i, monitor in enumerate(monitors[:20]):
            name = monitor.get("name", "Unnamed")
            monitor_id = monitor.get("id", "N/A")
            state = monitor.get("overall_state", "unknown")
            monitor_type = monitor.get("type", "unknown")
            tags = ", ".join(monitor.get("tags", []))

            lines.append(f"[{i + 1}] [{monitor_id}] [{state.upper()}] {name}")
            lines.append(f"     Type: {monitor_type}")
            if tags:
                lines.append(f"     Tags: {tags}")
            lines.append("")

        if len(monitors) > 20:
            lines.append(f"... and {len(monitors) - 20} more monitors")

    return "\n".join(lines)


def format_incident_results(incidents: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format incident results as human-readable text."""
    lines = []

    lines.append("=== Incident Results ===")
    lines.append(f"Total Incidents: {metadata.get('total', len(incidents))}")

    if incidents:
        lines.append("")
        for i, incident in enumerate(incidents[:20]):
            title = incident.get("title", "Untitled")
            inc_id = incident.get("id", incident.get("incident_id", "N/A"))
            severity = incident.get("severity", "unknown")
            state = incident.get("state", "open")
            created = incident.get("created_at", "N/A")

            lines.append(f"[{i + 1}] [{inc_id}] [{severity}] [{state}] {title}")
            lines.append(f"     Created: {created}")
            lines.append("")

        if len(incidents) > 20:
            lines.append(f"... and {len(incidents) - 20} more incidents")

    return "\n".join(lines)


def format_span_results(spans: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format APM span results as human-readable text."""
    lines = []

    lines.append("=== APM Span Results ===")
    lines.append(f"Query: {metadata.get('query', 'N/A')}")
    lines.append(f"Total Spans: {metadata.get('total', len(spans))}")

    if spans:
        lines.append("")
        for i, span in enumerate(spans[:20]):
            service = span.get("service", "unknown")
            operation = span.get("name", span.get("resource", "unknown"))
            duration = span.get("duration", span.get("duration_nano", 0))
            timestamp = span.get("@timestamp", "N/A")

            # Convert nanoseconds to ms if needed
            if isinstance(duration, (int, float)) and duration > 1000000:
                duration = duration / 1000000

            lines.append(f"[{i + 1}] [{service}] {operation}")
            lines.append(f"     Duration: {duration:.2f}ms | Timestamp: {timestamp}")
            lines.append("")

        if len(spans) > 20:
            lines.append(f"... and {len(spans) - 20} more spans")

    return "\n".join(lines)


def format_synthetics_results(tests: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format synthetics test results as human-readable text."""
    lines = []

    lines.append("=== Synthetics Test Results ===")
    lines.append(f"Total Tests: {metadata.get('total', len(tests))}")

    if tests:
        lines.append("")
        for i, test in enumerate(tests[:20]):
            name = test.get("name", "Unnamed")
            test_id = test.get("public_id", test.get("id", "N/A"))
            status = test.get("status", "unknown")
            test_type = test.get("type", "unknown")

            lines.append(f"[{i + 1}] [{test_id}] [{status}] {name}")
            lines.append(f"     Type: {test_type}")
            lines.append("")

        if len(tests) > 20:
            lines.append(f"... and {len(tests) - 20} more tests")

    return "\n".join(lines)


def format_fleet_results(agents: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    """Format fleet agent results as human-readable text."""
    lines = []

    lines.append("=== Fleet Agent Results ===")
    lines.append(f"Total Agents: {metadata.get('total', len(agents))}")

    if agents:
        lines.append("")
        for i, agent in enumerate(agents[:20]):
            hostname = agent.get("hostname", agent.get("name", "unknown"))
            agent_id = agent.get("id", "N/A")
            status = agent.get("status", "unknown")
            version = agent.get("agent_version", "N/A")

            lines.append(f"[{i + 1}] [{agent_id}] [{status}] {hostname}")
            lines.append(f"     Version: {version}")
            lines.append("")

        if len(agents) > 20:
            lines.append(f"... and {len(agents) - 20} more agents")

    return "\n".join(lines)


def format_error_response(error: Exception, context: str = "") -> str:
    """Format error as human-readable text."""
    lines = ["=== Error ==="]

    if context:
        lines.append(f"Context: {context}")

    lines.append(f"Error: {str(error)}")

    return "\n".join(lines)
