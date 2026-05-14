# Datadog MCP Server (Python/FastMCP)

A Python implementation of the Datadog MCP server using FastMCP framework.

## Overview

This MCP server provides access to Datadog's monitoring and observability platform, enabling AI assistants to query metrics, monitors, logs, APM traces, RUM data, and more.

## MCP Components

| Component | Count | Description |
|-----------|-------|-------------|
| **Tools** | 48+ | Operations for querying and managing Datadog resources |
| **Prompts** | 4 | Workflow-guided prompts for incident response and analysis |
| **Resources** | 4 | Addressable resources for direct data access via URI |

### Tools
- Metrics (query, metadata, active metrics, tags)
- Monitors (CRUD operations, mute, validate)
- Dashboards, Logs, Events
- Incidents, APM, RUM
- SLOs, Synthetics, Downtimes
- Security monitoring, CI/CD visibility

### Prompts
- `triage_incident` - Guided Datadog incident triage workflow
- `audit_monitor_noise` - Identify noisy/flappy monitors
- `analyze_rum_error_spike` - Investigate RUM error spikes
- `investigate_slow_trace` - Analyze slow APM traces

### Resources
- `datadog://monitor/{monitor_id}` - Read monitor configuration
- `datadog://metric/{metric_name}/metadata` - Metric metadata
- `datadog://incident/{incident_id}` - Incident details
- `datadog://service/{service_name}` - APM service definition

## Installation

```bash
pip install -e .
```

## Configuration

Set the following environment variables:

```bash
export DD_API_KEY="your-datadog-api-key"
export DD_APP_KEY="your-datadog-app-key"
export DD_SITE="datadoghq.com"  # Optional, defaults to datadoghq.com
export DD_ALLOW_WRITE="true"    # Optional, enable write operations
export DD_TOOLS="metrics,monitors,logs"  # Optional, filter enabled tool categories
export DD_DISABLE="security,fleet"  # Optional, disable specific categories
```

## Usage

```bash
mcp-datadog
```

Or use with MCP client:

```python
from mcp_datadog import main
main()
```

### MCP Client Configuration

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "datadog": {
      "command": "uv",
      "args": ["run", "mcp-datadog"],
      "env": {
        "DD_API_KEY": "your-api-key",
        "DD_APP_KEY": "your-app-key"
      }
    }
  }
}
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Architecture

- **FastMCP**: Uses the official MCP Python SDK with FastMCP for easy tool registration
- **httpx**: Async HTTP client for Datadog API calls
- **Pydantic**: Schema validation for tool parameters
- **Category Filtering**: Enable/disable tool categories for focused functionality

## MCP Protocol Compliance

This server follows the [Model Context Protocol](https://modelcontextprotocol.io) specification:

- ✅ **Tools** - Functions callable by the client
- ✅ **Prompts** - Workflow-guided prompt templates
- ✅ **Resources** - Addressable data via URI templates
- ✅ **stdio Transport** - Standard input/output communication

## Credits

Original TypeScript implementation: https://github.com/us-all/datadog-mcp-server
Reference Python implementation: https://github.com/shelfio/datadog-mcp