---
name: cron
description: Use the cron tool for scheduled tasks in the current chat
always: true
---

# Cron Skill

You have a built-in `cron` tool for scheduling recurring tasks in the current chat session.

## Available Actions

The `cron` tool accepts JSON with an `action` field:

### Add a job
```json
{
  "action": "add",
  "interval_minutes": 15,
  "prompt": "Check for backend errors in the last 15 minutes and post a summary"
}
```

### List jobs
```json
{
  "action": "list"
}
```

### Remove a job
```json
{
  "action": "remove",
  "job_id": 1
}
```

## When to use cron

Use cron when the user asks for:
- "Create a health check that runs every X minutes"
- "Schedule a periodic task"
- "Monitor the system regularly"
- "Check for errors every X minutes"

## Example patterns

**User:** "Create a health check that runs every 15 minutes"
**You:** Call `cron` with action "add", interval_minutes: 15, and a prompt that checks for errors using `mcp_obs_logs_error_count` with `time_range="15m"`.

**User:** "List scheduled jobs"
**You:** Call `cron` with action "list" and show the results.

**User:** "Remove the health check"
**You:** Call `cron` with action "remove" and the job_id.

## Health check prompt template

When creating a health check job, use a prompt like:
```
Check for backend errors in the last {interval} minutes. Call logs_error_count with service="Learning Management Service" and time_range="{interval}m". If errors exist, search logs and inspect a trace. Post a short summary: either "System healthy - no recent errors" or describe the errors found.
```

## Important notes

- Jobs are tied to the current chat session
- Jobs persist in `cron/jobs.json`
- Interval is in minutes (minimum 1, typical 5-15)
- Each job runs automatically at the specified interval
- Job results are posted as messages in the chat
