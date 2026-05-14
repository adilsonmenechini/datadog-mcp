"""MCP Prompts for Datadog workflows."""

from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register MCP prompts for Datadog workflows."""

    @mcp.prompt()
    def triage_incident(incident_id: str, lookback_minutes: int = 60) -> str:
        """Generate triage instructions for an incident."""
        return f"""Triage Datadog incident {incident_id} using the last {lookback_minutes} minutes of related signals.

Steps:
1. Call `get-incident` with incidentId={incident_id!r}. Capture title, severity, customer impact, created timestamp, fields/tags, and any commander info.
2. Compute the window: from = (incident created_ts) - {lookback_minutes}min, to = now (or incident resolved_ts if set).
3. Call `get-events` over that window with sources/tags from the incident (e.g. service, env) to surface deploys, alerts, and config changes.
4. Call `search-incidents` with a query targeting the same service/team to detect similar recent incidents (possible repeat / regression).
5. For monitors referenced by the incident (or matching its tags), call `analyze-monitor-state` to get current state + recent triggers + active downtimes in one shot.
6. Call `aggregate-logs` with a query like `status:error service:<incident-service>` grouped by 5-minute buckets to detect a log spike inside the window.
7. Produce a triage summary with: severity assessment, blast radius (services / users / regions), suspected root cause (deploy? config? upstream?), supporting evidence (event IDs, monitor IDs, log spike timestamps), and one recommended next action.
"""

    @mcp.prompt()
    def audit_monitor_noise(tag_filter: str = "", top_n: int = 10) -> str:
        """Generate instructions for auditing noisy monitors."""
        tag_part = f" filtered to tag '{tag_filter}'" if tag_filter else ""
        return f"""Audit Datadog monitor noise{tag_part} and rank the top {top_n} noisiest by flap rate.

Steps:
1. Call `get-monitors`{f" with monitorTags={tag_filter!r}" if tag_filter else " (no filters)"} to enumerate the candidate set. Capture id, name, type, query, current overall_state, and tags.
2. For each monitor, call `analyze-monitor-state` (incidentMinutes=1440 = 24h window) to get current state + recent triggered events + active downtimes in one call.
3. Compute flap rate per monitor: count of state oscillations (Alert↔OK or Warn↔OK transitions) in the recent events, divided by the window length in hours. Higher = noisier.
4. Sort by flap rate descending and take the top {top_n}. Tie-break by total trigger count.
5. For each, output: monitor id, name, flap rate (per hour), trigger count in window, currently muted? (active downtime), suggested action — one of: `mute-monitor` (tag-based silence), tighten threshold, add `recovery_window`, or split into multi-condition. Cite the recent triggers as evidence.
6. End with a one-paragraph recommendation: what fraction of the audited surface is noisy, and which 2-3 monitors deserve immediate attention.
"""

    @mcp.prompt()
    def analyze_rum_error_spike(application_id: str, since_minutes: int = 30) -> str:
        """Generate instructions for analyzing RUM error spikes."""
        return f"""Investigate a RUM error spike in application {application_id} over the last {since_minutes} minutes.

Steps:
1. Call `aggregate-rum` with query=`@type:error @application.id:{application_id}`, time window of {since_minutes} minutes, compute=count, groupBy=[`@error.message`] (or 5-minute time buckets) to confirm and shape the spike. Compare to the previous {since_minutes} minutes for baseline.
2. If a spike is confirmed, call `search-rum-events` with the same query, sorted by timestamp descending, limit ~100, to retrieve representative error events.
3. Group the returned events client-side by (`@error.message`, `@view.name`). For each top group, capture count, distinct `@session.id` (impacted users proxy), browser/OS spread, and first/last seen.
4. Identify the top 3-5 error patterns. For each, include: error message, primary view, impacted user count, sample stack trace if present, and one hypothesis (regression vs. third-party vs. data-driven).
5. Produce a markdown report: spike confirmation chart description, top patterns table, and a prioritized list of which patterns to escalate (highest user impact first).
"""

    @mcp.prompt()
    def investigate_slow_trace(service_name: str, latency_threshold_ms: int = 1000) -> str:
        """Generate instructions for investigating slow traces."""
        return f"""Investigate slow traces for service '{service_name}' (spans slower than {latency_threshold_ms}ms).

Steps:
1. Call `search-spans` with query=`service:{service_name} @duration:>{latency_threshold_ms}ms`, sort by duration descending, limit ~50. Use a time window of the last hour by default.
2. Pick the top 3-5 trace_ids by total duration. For each, list the span breakdown: resource name, operation name, duration, span.kind (server/client/db), and key tags (sql.query, http.url, peer.service).
3. Aggregate time spent by category across the sample: DB time (spans where `db.system` is set), network/HTTP-client time (`span.kind:client` http calls), and self/compute time (parent duration minus child sum).
4. Identify hot spots — the resource(s) contributing the most p99 latency. Note repeat patterns (N+1 query, sync fan-out, single slow downstream service).
5. Produce a report with: top slow trace_ids + Datadog APM links, the latency breakdown table (DB / network / compute), top 3 hot-spot resources, and a recommended fix per hot spot (add index, batch, cache, parallelize, etc.).
"""
