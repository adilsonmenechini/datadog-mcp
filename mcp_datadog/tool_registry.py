"""Tool registry for category-based filtering."""

from dataclasses import dataclass

from .config import config


CATEGORIES = [
    "metrics",
    "monitors",
    "dashboards",
    "logs",
    "apm",
    "rum",
    "incidents",
    "security",
    "synthetics",
    "ci",
    "infra",
    "fleet",
    "error_tracking",
    "events",
    "status-pages",
    "oncall",
    "teams",
    "account",
    "meta",
]


@dataclass
class ToolInfo:
    """Information about a registered tool."""

    name: str
    description: str
    category: str


class ToolRegistry:
    """Registry for tools with category-based filtering."""

    def __init__(
        self,
        enabled_categories: list[str] | None = None,
        disabled_categories: list[str] | None = None,
    ) -> None:
        self.tools: dict[str, ToolInfo] = {}
        self._enabled_categories = enabled_categories
        self._disabled_categories = disabled_categories or []

    def register(self, name: str, description: str, category: str) -> None:
        """Register a tool."""
        self.tools[name] = ToolInfo(name=name, description=description, category=category)

    def is_enabled(self, category: str) -> bool:
        """Check if a category is enabled based on config."""
        # If specific categories are enabled, only those are active
        if self._enabled_categories is not None:
            return category in self._enabled_categories
        # Otherwise, check if category is not in disabled list
        return category not in self._disabled_categories

    def get_enabled_tools(self) -> list[ToolInfo]:
        """Get list of enabled tools."""
        return [t for t in self.tools.values() if self.is_enabled(t.category)]

    def search(self, query: str) -> list[ToolInfo]:
        """Search tools by name or description."""
        query_lower = query.lower()
        return [
            t
            for t in self.tools.values()
            if query_lower in t.name.lower() or query_lower in t.description.lower()
        ]


registry = ToolRegistry(
    enabled_categories=config.enabled_categories,
    disabled_categories=config.disabled_categories,
)


def search_tools_handler(query: str) -> list[dict[str, str]]:
    """Handle search-tools meta tool."""
    results = registry.search(query) if query else list(registry.tools.values())
    return [{"name": t.name, "description": t.description, "category": t.category} for t in results]
