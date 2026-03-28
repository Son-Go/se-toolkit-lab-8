#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime, then execs nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def main() -> None:
    config_path = Path("/app/nanobot/config.json")
    resolved_path = Path("/tmp/config.resolved.json")
    workspace_path = Path("/app/nanobot/workspace")

    # Add MCP servers to Python path so they can be imported
    import sys
    sys.path.insert(0, "/app/mcp/mcp-lms/src")
    sys.path.insert(0, "/app/nanobot-websocket-channel/mcp-webchat/src")

    # Read base config
    config = json.loads(config_path.read_text())

    # Override LLM provider settings from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base = os.environ.get("LLM_API_BASE_URL")
    llm_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base:
        config["providers"]["custom"]["apiBase"] = llm_api_base
    if llm_model:
        config["agents"]["defaults"]["model"] = llm_model

    # Override gateway settings from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Override MCP server env vars for LMS
    # In Docker, the MCP servers are mounted from the workspace, so we use the container Python
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")
    pythonpath = os.environ.get("PYTHONPATH", "")
    venv_python = "/app/.venv/bin/python"

    if "lms" in config.get("tools", {}).get("mcpServers", {}):
        mcp_env = config["tools"]["mcpServers"]["lms"].setdefault("env", {})
        if lms_backend_url:
            mcp_env["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            mcp_env["NANOBOT_LMS_API_KEY"] = lms_api_key
        if pythonpath:
            mcp_env["PYTHONPATH"] = pythonpath
        # Use venv Python for MCP servers
        config["tools"]["mcpServers"]["lms"]["command"] = venv_python

    # Override webchat channel settings from env vars
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    webchat_access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if webchat_host or webchat_port or webchat_access_key:
        if "webchat" not in config.get("channels", {}):
            config["channels"]["webchat"] = {}
        if webchat_host:
            config["channels"]["webchat"]["host"] = webchat_host
        if webchat_port:
            config["channels"]["webchat"]["port"] = int(webchat_port)
        if webchat_access_key:
            config["channels"]["webchat"]["accessKey"] = webchat_access_key
        # Enable the channel
        config["channels"]["webchat"]["enabled"] = True

    # Override MCP server env vars for webchat UI delivery
    webchat_ui_relay = os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_URL")
    webchat_ui_token = os.environ.get("NANOBOT_WEBCHAT_UI_TOKEN")

    if "webchat" in config.get("tools", {}).get("mcpServers", {}):
        mcp_env = config["tools"]["mcpServers"]["webchat"].setdefault("env", {})
        if webchat_ui_relay:
            mcp_env["NANOBOT_WEBCHAT_UI_RELAY_URL"] = webchat_ui_relay
        if webchat_ui_token:
            mcp_env["NANOBOT_WEBCHAT_UI_TOKEN"] = webchat_ui_token
        if pythonpath:
            mcp_env["PYTHONPATH"] = pythonpath
        # Use venv Python for MCP servers
        config["tools"]["mcpServers"]["webchat"]["command"] = venv_python

    # Write resolved config
    resolved_path.write_text(json.dumps(config, indent=2))

    print(f"Using config: {resolved_path}", file=sys.stderr)

    # Exec nanobot gateway using the venv path
    nanobot_path = "/app/.venv/bin/nanobot"
    os.execvp(
        nanobot_path,
        [
            nanobot_path,
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_path),
        ],
    )


if __name__ == "__main__":
    main()
