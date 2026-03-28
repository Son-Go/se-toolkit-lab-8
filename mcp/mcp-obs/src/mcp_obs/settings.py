"""Settings for the observability MCP server."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ObsSettings:
    """Observability service settings."""

    victorialogs_url: str
    victoriatraces_url: str

    @classmethod
    def from_env(cls) -> "ObsSettings":
        """Load settings from environment variables."""
        return cls(
            victorialogs_url=os.environ.get(
                "NANOBOT_VICTORIALOGS_URL", "http://localhost:42010"
            ),
            victoriatraces_url=os.environ.get(
                "NANOBOT_VICTORIATRACES_URL", "http://localhost:42011"
            ),
        )


def resolve_settings() -> ObsSettings:
    """Resolve observability settings."""
    return ObsSettings.from_env()
