# Adapted from backend/Dockerfile and qwen-code-api/Dockerfile
# Also see https://docs.astral.sh/uv/guides/integration/docker/

# ---
# Stage 1: build the application in the `/app` directory.
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads - use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy root workspace files for resolving workspace dependencies
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy all workspace members needed by nanobot from workspace context
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms
COPY --from=workspace mcp/mcp-obs /app/mcp/mcp-obs
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat
COPY --from=workspace nanobot-websocket-channel/mcp-webchat /app/nanobot-websocket-channel/mcp-webchat
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol
COPY --from=workspace nanobot /app/nanobot

# Sync the entire workspace
WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package nanobot --package mcp-lms --package mcp-obs --package mcp-webchat --package nanobot-webchat --package nanobot-channel-protocol --package nanobot-ai

# Copy workspace from source (already in place)

# Copy entrypoint from host (will be mounted separately)

# ---
# Stage 2: use a final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure we use UTF-8 encoding
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Setup a non-root user with configurable UID/GID
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd --system --gid "${APP_GID}" appuser \
    && useradd --system --gid "${APP_GID}" --uid "${APP_UID}" --create-home appuser

# Copy the application from the builder
COPY --from=builder --chown=appuser:appuser /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the app user to run our application
USER appuser

# Use `/app/nanobot` as the working directory
WORKDIR /app/nanobot

# Run the nanobot gateway via entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
