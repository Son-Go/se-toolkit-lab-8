# Lab 7 — Build a Client with an AI Coding Agent

The lab gets updated regularly, so do [sync your fork with the upstream](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-branch-from-the-command-line) from time to time.

<h2>Table of contents</h2>

- [Product brief](#product-brief)
- [Requirements](#requirements)
- [Learning advice](#learning-advice)
- [Learning outcomes](#learning-outcomes)
- [Tasks](#tasks)
  - [Prerequisites](#prerequisites)
  - [Required](#required)

## Product brief

> Build a Telegram bot that lets users interact with the LMS backend through chat. Users should be able to check system health, browse labs and scores, and ask questions in plain language. The bot should use an LLM to understand what the user wants and fetch the right data. Deploy it alongside the existing backend on the VM.

This is what a customer might tell you. It's deliberately vague — it doesn't say which framework to use, how to structure the code, what the commands should be, or how to handle errors.

Your job is to turn this into a working product. You will use an AI coding agent (Qwen Code) as your development partner.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌──────────────┐     ┌──────────────────────────────────┐   │
│  │  Telegram    │────▶│  Your Bot                        │   │
│  │  User        │◀────│  (aiogram / python-telegram-bot) │   │
│  └──────────────┘     └──────┬───────────────────────────┘   │
│                              │                               │
│                              │ slash commands + plain text    │
│                              ├───────▶ /start, /help         │
│                              ├───────▶ /health, /labs        │
│                              ├───────▶ intent router ──▶ LLM │
│                              │                    │          │
│                              │                    ▼          │
│  ┌──────────────┐     ┌──────┴───────┐    tools/actions      │
│  │  Docker      │     │  LMS Backend │◀───── GET /items      │
│  │  Compose     │     │  (FastAPI)   │◀───── GET /analytics  │
│  │              │     │  + PostgreSQL│◀───── POST /sync      │
│  └──────────────┘     └──────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

## Requirements

The product brief above is how requirements start. Below is the structured version — prioritized so you know what to build first and what can wait.

### P0 — Must have

1. Bot project scaffolded with testable handler architecture (handlers work without Telegram)
2. CLI test mode: `python bot/bot.py --test "/command"` — prints response to stdout, exits
3. `/start` — welcome message
4. `/help` — lists all available commands
5. `/health` — calls backend, reports up/down status
6. `/labs` — lists available labs from the backend
7. `/scores <lab>` — shows per-task pass rates for a given lab
8. Error handling — backend down produces a friendly message, not a crash

### P1 — Should have

1. Natural language intent routing — plain text messages (no `/` prefix) interpreted by LLM
2. All 9 backend endpoints wrapped as LLM tools
3. Inline keyboard buttons for common actions
4. Multi-step reasoning (LLM chains multiple API calls to answer one question)

### P2 — Nice to have

1. Rich message formatting (tables, charts as images)
2. Response caching for expensive queries
3. Conversation context (multi-turn)

### P3 — Deployment

1. Bot containerized with Dockerfile
2. Added as a service in `docker-compose.yml` alongside the backend
3. Deployed and running on the VM
4. README documents how to deploy

Each task in this lab corresponds to a priority level. The [task specifications](#required) are the detailed engineering breakdown — they define exact deliverables, acceptance criteria, and how the autochecker verifies your work.

## Learning advice

This lab is about learning to collaborate with an AI coding agent as a development partner. You are not following step-by-step instructions — you are building a product.

Notice the progression: **product brief** (vague, natural language) → **prioritized requirements** (structured, what matters most) → **task specifications** (precise deliverables and acceptance criteria). This is how real engineering work flows — from a customer ask to something you can build and verify.

The bot you build is practical (~200-400 lines). The learning comes from the iterative process of planning, building, testing, and debugging with agent assistance.

## Learning outcomes

By the end of this lab, you should be able to:

- Turn a natural language product brief into structured requirements and then into working code.
- Use an AI coding agent to plan, implement, and debug a client application.
- Design a testable handler architecture (logic separated from transport).
- Connect a client to an existing REST API with authentication.
- Implement natural language intent routing using LLM tool/function calling.
- Deploy a multi-service system (backend + bot) on a remote VM.

In simple words, you should be able to say:
>
> 1. I turned a vague product brief into a working Telegram bot!
> 2. I can ask it questions in plain language and it fetches the right data!
> 3. I used an AI coding agent to plan and build the whole thing!

## Tasks

### Prerequisites

1. Complete the [lab setup](./lab/tasks/setup-simple.md#lab-setup)

> **Note**: If this is the first lab you are attempting in this course, you need to do the [full version of the setup](./lab/tasks/setup.md#lab-setup)

### Required

1. [Plan and Scaffold](./lab/tasks/required/task-1.md#plan-and-scaffold) — P0: project structure, `--test` mode, development plan
2. [Backend Integration](./lab/tasks/required/task-2.md#backend-integration) — P0: slash commands connected to real backend data
3. [Intent-Based Natural Language Routing](./lab/tasks/required/task-3.md#intent-based-natural-language-routing) — P1: LLM-powered plain text understanding with 9 tools
4. [Deploy and Document](./lab/tasks/required/task-4.md#deploy-and-document) — P3: containerize, deploy to VM, document
