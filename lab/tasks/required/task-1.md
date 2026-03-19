# Plan and Scaffold

Use your coding agent to create a development plan and project skeleton for the Telegram bot. This is the foundation — you will implement the actual features in Tasks 2–3.

## What you will build

A `bot/` directory inside your repo containing the scaffolded project: entry point, handler layer, configuration, dependencies, and a `--test` mode for offline verification.

```
se-toolkit-lab-7/
├── bot/                    ← NEW
│   ├── bot.py              ← entry point
│   ├── handlers/           ← command handlers (separated from Telegram transport)
│   ├── services/           ← API client, LLM client
│   ├── config.py           ← environment variable loading
│   ├── requirements.txt    ← bot dependencies
│   └── PLAN.md             ← development plan
├── backend/                ← existing
├── frontend/               ← existing
└── docker-compose.yml      ← existing
```

The entry point must support a `--test` flag for offline command verification:

```terminal
python bot/bot.py --test "/start"
```

This prints the bot's response to stdout and exits — no Telegram connection needed. The autochecker uses this to verify your bot's behavior.

## Prioritized requirements

See the [requirements section](../../README.md#requirements) in the README for the full prioritized list (P0–P3). Give these to your coding agent when creating the plan — it needs to understand the full scope across all tasks, not just Task 1.

## Test mode specification

The `--test` flag is how the autochecker verifies your bot without Telegram:

```terminal
# Slash commands
python bot/bot.py --test "/start"
python bot/bot.py --test "/help"
python bot/bot.py --test "/health"
python bot/bot.py --test "/labs"
python bot/bot.py --test "/scores lab-04"

# Natural language (Task 3)
python bot/bot.py --test "what labs are available"
python bot/bot.py --test "which lab has the lowest pass rate"
```

**Behavior:**
- Prints the bot's response text to **stdout**
- Reads configuration from `.env.agent.secret` (backend URL, API keys)
- Exits with code **0** on success, non-zero on error
- Does **not** connect to Telegram (no `BOT_TOKEN` required in test mode)

## Deliverables

### 1. Development plan (`bot/PLAN.md`)

A plan produced with your coding agent's help. Should describe the approach for all tasks (scaffold, backend integration, intent routing, deployment). At least 100 words.

### 2. Bot entry point (`bot/bot.py`)

The main entry file. Must support `--test` mode. In this task, handlers can return placeholder text — real implementation comes in Task 2.

### 3. Handler module (`bot/handlers/` or `bot/handlers.py`)

Handlers separated from the Telegram transport layer. The `--test` mode calls handlers directly without Telegram.

### 4. Dependencies (`bot/requirements.txt`)

Bot-specific Python dependencies. Must install without errors.

### 5. Bot token in env example (`.env.agent.example`)

Add `BOT_TOKEN` to the existing `.env.agent.example` file.

## Acceptance criteria

- [ ] `bot/PLAN.md` exists and has at least 100 words.
- [ ] `.env.agent.example` contains `BOT_TOKEN`.
- [ ] `bot/requirements.txt` exists and installs without errors.
- [ ] Handler module exists separately from the bot entry point.
- [ ] `python bot/bot.py --test "/start"` exits with code 0 and prints non-empty output.
- [ ] Changes follow the Git workflow (issue, branch, PR, review, merge).

## Working with your coding agent

Use your coding agent to help you plan, scaffold, and understand the architecture. Here are prompts to try at each stage:

**Understanding the architecture:**

> Explain what "testable handler architecture" means. Why should I separate handlers from the Telegram transport layer? Give me an analogy.

> What is `--test` mode and why does the autochecker need it? Walk me through what happens when I run `python bot/bot.py --test "/start"`.

**Planning:**

> Here are the requirements for my Telegram bot. Create a development plan — but first, ask me questions about anything that's unclear.

> What files and modules do I need? For each one, explain its responsibility in one sentence.

**Scaffolding:**

> Scaffold the project. For each file you create, explain why it exists and how it connects to the others.

> Show me the code path: when `--test "/start"` runs, which functions get called in what order?

**Verifying:**

> I ran `python bot/bot.py --test "/start"` and it works. Now explain: if I wanted to add a new command `/foo`, what exactly would I need to change?
