---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

You have access to VictoriaLogs and VictoriaTraces via MCP tools. Use them to diagnose errors and inspect request flows.

## Available Tools

- `mcp_obs_logs_search` — Search logs using LogsQL query (requires `query`, optional `limit` and `time_range`)
- `mcp_obs_logs_error_count` — Count errors per service over a time window (optional `service` and `time_range`)
- `mcp_obs_traces_list` — List recent traces for a service (optional `service` and `limit`)
- `mcp_obs_traces_get` — Fetch a specific trace by ID (requires `trace_id`)

## Strategy

### When the user asks "What went wrong?" or "Check system health":

Perform a **one-shot investigation** that chains log and trace tools:

1. **Call `logs_error_count`** with a fresh time window (e.g., `time_range="10m"`)
   - Focus on the LMS backend service: `service="Learning Management Service"`

2. **Call `logs_search`** to get the actual error entries
   - Query: `severity:ERROR service.name:"Learning Management Service"`
   - Extract the `trace_id` from the most recent error log

3. **Call `traces_get`** with the extracted `trace_id`
   - Inspect the span hierarchy to find where the failure occurred

4. **Summarize findings in one coherent response** that includes:
   - **Log evidence**: What error was logged (e.g., "PostgreSQL connection refused", "SQLAlchemy error")
   - **Trace evidence**: Which span failed and what operation was being performed
   - **Root cause**: Name the affected service and the failing operation
   - **Key discrepancy**: If logs/traces show a database failure but the HTTP response was `404 Items not found`, point this out

### When the user asks about errors or problems:

1. **Start with `logs_error_count`** to quickly see if there are recent errors
   - Use a scoped time range like "10m" or "1h" depending on the question
   - If the user mentions a specific service, filter by that service

2. **If errors are found, use `logs_search`** to inspect the relevant entries
   - Query for `severity:ERROR` to see error details
   - Look for `trace_id` in the log entries

3. **If a trace_id is found, use `traces_get`** to inspect the full request flow
   - This shows the span hierarchy and where the failure occurred

4. **Summarize findings concisely** — don't dump raw JSON
   - Report what service had errors
   - Explain what went wrong (e.g., "database connection failed")
   - Mention the trace ID if relevant

### When the user asks to inspect a specific trace:

1. Use `traces_get` with the provided trace ID
2. Analyze the span hierarchy
3. Report the request flow and any errors

### When the user asks about recent activity:

1. Use `traces_list` to see recent traces
2. Optionally filter by service name
3. Summarize what requests were made

## Response formatting

- **Be concise**: Summarize findings in 2-4 sentences
- **Highlight errors**: Clearly state what failed and where
- **Include trace IDs**: When relevant, mention the trace ID for further debugging
- **Use time ranges**: Always specify the time window you queried (e.g., "in the last 10 minutes")
- **Cite both sources**: For "What went wrong?" investigations, explicitly mention both log evidence and trace evidence

## Example patterns

**User:** "What went wrong?"
**You:** 
1. Call `logs_error_count` with `time_range="10m"` and `service="Learning Management Service"`
2. Call `logs_search` with `query="severity:ERROR service.name:\"Learning Management Service\""`, `time_range="10m"`
3. Extract `trace_id` from the most recent error log
4. Call `traces_get` with that `trace_id`
5. Respond with: "Logs show [error message] at [timestamp]. Trace [trace_id] shows the request failed at [span/operation]. The root cause is [root cause]."

**User:** "Any errors in the last hour?"
**You:** Call `logs_error_count` with `time_range="1h"`. Report which services had errors and how many.

**User:** "Any LMS backend errors in the last 10 minutes?"
**You:** Call `logs_error_count` with `service="Learning Management Service"` and `time_range="10m"`. If errors exist, call `logs_search` to get details and extract trace IDs.

**User:** "Show me the trace for request abc123"
**You:** Call `traces_get` with `trace_id="abc123"`. Describe the span hierarchy and any errors.

**User:** "Why did my request fail?"
**You:**
1. Call `logs_search` with `query="severity:ERROR"` and recent `time_range`
2. Find the relevant error log and extract `trace_id`
3. Call `traces_get` with that trace ID
4. Explain where in the request flow the failure occurred

## Important notes

- Always scope queries by time range to avoid returning stale data
- When asked about a specific service, filter by that service name
- Don't dump raw JSON — summarize the findings in natural language
- If no errors are found, clearly state that (e.g., "No errors found in the last 10 minutes")
- For "What went wrong?" investigations, always chain: error_count → logs_search → traces_get → summary
