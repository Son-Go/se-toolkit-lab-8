# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question 1: "What is the agentic loop?"**

The agentic loop is the core reasoning cycle that enables AI agents to act autonomously. It consists of four main phases:

1. **Observe** — Perceive the current state (user input, file contents, API responses, environment)
2. **Think** — Reason about what to do next (analyze, plan, decide on actions)
3. **Act** — Execute tools or actions (read/write files, run commands, call APIs)
4. **Reflect** — Evaluate outcomes and decide whether to continue or stop

Loop: Observe → Think → Act → Reflect → (repeat or complete)

This is what makes agents autonomous rather than just reactive chatbots.

**Question 2: "What labs are available in our LMS?"**

The bare agent **cannot** access live LMS data. It reads local files instead and returns information from the README:

> Based on my exploration of the workspace, here are the available labs in your LMS:
> 
> **Required Labs (Lab 8):**
> 1. Task 1: Set Up the Agent — install nanobot, configure Qwen API, add MCP tools, write skill prompt
> 2. Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket channel + Flutter chat UI
> 3. Task 3: Give the Agent New Eyes — explore observability data, write log/trace MCP tools
> 4. Task 4: Diagnose a Failure and Make the Agent Proactive — investigate a failure, schedule in-chat health checks, fix a planted bug
>
> **Optional Labs (Lab 8):**
> 1. Task 1: Add a Telegram Bot Client — same agent, different interface

The agent describes the lab tasks from documentation but has **no live backend access** yet.

## Task 1B — Agent with LMS tools

**Question 1: "What labs are available?"**

After connecting the MCP server, the agent now returns **real data** from the LMS backend:

> Here are the available labs:
>
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 — Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. lab-08

The agent called the `mcp_lms_lms_labs` MCP tool and returned actual lab names from the database.

**Question 2: "Is the LMS backend healthy?"**

> Yes, the LMS backend is healthy. It currently has 56 items in the system.

The agent called `mcp_lms_lms_health` and reported the real item count from the backend.

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

With the LMS skill prompt, the agent now follows the correct strategy:

> I'll help you see the scores! First, let me get the list of available labs.
>
> Here are the available labs. Which one would you like to see the scores for?
>
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 — Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. Lab 08 — lab-08
>
> Just let me know which lab (e.g., "lab-04" or "Lab 04") and I'll show you the pass rates!

The skill prompt teaches the agent to:
1. Call `mcp_lms_lms_labs` first when no lab is specified
2. List all available labs
3. Ask the user to choose which lab they want to see scores for

This is the expected behavior — the agent asks for clarification instead of guessing or failing.

## Task 2A — Deployed agent

Nanobot gateway startup logs showing successful deployment:

```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
MCP server 'lms': connected, 9 tools registered
MCP: registered tool 'mcp_webchat_ui_message' from server 'webchat'
MCP server 'webchat': connected, 1 tools registered
Agent loop started
```

## Task 2B — Web client

**WebSocket test response:**

```json
{
  "type": "text",
  "content": "Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy\n4. **Lab 04** — Testing, Front-end, and AI Agents\n5. **Lab 05** – Data Pipeline and Analytics Dashboard\n6. **Lab 06** – Build Your Own Agent\n7. **Lab 07** – Build a Client with an AI Coding Agent\n8. **Lab 08** – lab-08\n\nWould you like to see details about any specific lab, such as pass rates, completion rates, or top learners?",
  "format": "markdown"
}
```

The agent returned **real LMS data** via the WebSocket endpoint at `ws://localhost:42002/ws/chat?access_key=lab8`.

**Flutter web client:** Accessible at `http://localhost:42002/flutter/`

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
