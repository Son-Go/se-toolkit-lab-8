"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx


class ObsClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(
        self,
        victorialogs_url: str,
        victoriatraces_url: str,
        timeout: float = 30.0,
    ) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self._client = httpx.AsyncClient(timeout=timeout)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "ObsClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    # ========== VictoriaLogs API ==========

    async def logs_search(
        self,
        query: str,
        limit: int = 100,
        time_range: str = "1h",
    ) -> list[dict]:
        """
        Search logs using VictoriaLogs LogsQL query.

        Args:
            query: LogsQL query string (e.g., 'severity:ERROR')
            limit: Maximum number of log entries to return
            time_range: Time range for the query (e.g., '1h', '10m', '1d')

        Returns:
            List of log entries as dictionaries
        """
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {
            "query": f"_time:{time_range} {query}",
            "limit": limit,
        }
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def logs_error_count(
        self,
        service: str | None = None,
        time_range: str = "1h",
    ) -> dict[str, int]:
        """
        Count errors per service over a time window.

        Args:
            service: Optional service name to filter by
            time_range: Time range for the query

        Returns:
            Dictionary mapping service names to error counts
        """
        if service:
            query = f'_time:{time_range} service.name:"{service}" severity:ERROR'
        else:
            query = f"_time:{time_range} severity:ERROR"

        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {
            "query": query,
            "limit": 1000,
        }
        response = await self._client.get(url, params=params)
        response.raise_for_status()

        logs = response.json()
        error_counts: dict[str, int] = {}
        for entry in logs:
            labels = entry.get("labels", {})
            service_name = labels.get("service.name", "unknown")
            error_counts[service_name] = error_counts.get(service_name, 0) + 1

        return error_counts

    # ========== VictoriaTraces API ==========

    async def traces_list(
        self,
        service: str | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """
        List recent traces for a service.

        Args:
            service: Optional service name to filter by
            limit: Maximum number of traces to return

        Returns:
            List of trace summaries
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service

        response = await self._client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "data" in data:
            return data["data"]
        return data if isinstance(data, list) else []

    async def traces_get(self, trace_id: str) -> dict:
        """
        Fetch a specific trace by ID.

        Args:
            trace_id: The trace ID to fetch

        Returns:
            Full trace data with spans
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        response = await self._client.get(url)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "data" in data:
            traces = data["data"]
            return traces[0] if traces else {}
        return data if isinstance(data, dict) else {}
