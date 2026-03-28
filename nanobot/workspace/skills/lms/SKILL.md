---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS backend via MCP tools. Use them to answer questions about labs, learners, and performance.

## Available Tools

- `mcp_lms_lms_health` — Check if the LMS backend is healthy and get item count
- `mcp_lms_lms_labs` — List all labs available in the LMS
- `mcp_lms_lms_learners` — List all learners registered in the LMS
- `mcp_lms_lms_pass_rates` — Get pass rates for a specific lab (requires `lab` parameter)
- `mcp_lms_lms_timeline` — Get submission timeline for a specific lab (requires `lab` parameter)
- `mcp_lms_lms_groups` — Get group performance for a specific lab (requires `lab` parameter)
- `mcp_lms_lms_top_learners` — Get top learners for a specific lab (requires `lab` and optional `limit` parameter)
- `mcp_lms_lms_completion_rate` — Get completion rate for a specific lab (requires `lab` parameter)
- `mcp_lms_lms_sync_pipeline` — Trigger the LMS sync pipeline

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners:

1. **Check if a lab is specified** in the user's question
2. **If no lab is specified:**
   - Call `mcp_lms_lms_labs` first to get the list of available labs
   - Use the `mcp_webchat_ui_message` tool to present the lab choices interactively
   - Use each lab's `title` field as the user-facing label
   - Pass the lab identifier (e.g., `lab-01`, `lab-02`) as the choice value
3. **If a lab is specified:**
   - Call the appropriate tool directly with the lab parameter

### When the user asks "what can you do?" or about capabilities:

Explain your current tools and limits clearly:
- You can query the LMS backend for lab information, learner data, pass rates, completion rates, group performance, and submission timelines
- You need a lab identifier for most detailed queries
- You can help them choose a lab if they're not sure which one to ask about

### Response formatting:

- Format numeric results nicely: show percentages with `%` symbol, round to 1-2 decimal places
- Keep responses concise but informative
- When presenting multiple options, use the interactive UI message tool on supported channels
- If the interactive tool is unavailable, fall back to a plain text list

### Example patterns:

**User:** "Show me the scores"
**You:** Call `mcp_lms_lms_labs`, then present choices: "Which lab would you like to see scores for?" with interactive options.

**User:** "Show me scores for lab-03"
**You:** Call `mcp_lms_lms_pass_rates` with `lab="lab-03"` and present the results.

**User:** "Which lab has the lowest pass rate?"
**You:** Call `mcp_lms_lms_labs`, then iterate through labs calling `mcp_lms_lms_pass_rates` for each, compare results, and report the answer.

**User:** "Is the backend working?"
**You:** Call `mcp_lms_lms_health` and report the status and item count.
