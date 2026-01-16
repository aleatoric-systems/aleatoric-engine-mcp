#!/usr/bin/env python3
"""
Aleatoric MCP Bridge Server (Stdio)

This script acts as a local MCP server that proxies requests to the
remote Aleatoric Production API via the standard MCP JSON-RPC 2.0 protocol.
It enables compatibility with clients that require a local stdio transport
(like MCP Inspector or Claude Desktop running locally).

Protocol Version: 2024-11-05
Server Version: 0.4.7
"""

import json
import os
import sys
import httpx

# Configuration
API_BASE_URL = os.getenv("MCP_BASE_URL", "https://mcp.aleatoric.systems")
API_KEY = os.getenv("ALEATORIC_API_KEY")

if not API_KEY:
    sys.stderr.write("Error: ALEATORIC_API_KEY must be set.\n")
    sys.exit(1)

MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "aleatoric-bridge"
SERVER_VERSION = "0.4.7"


def log(msg):
    sys.stderr.write(f"[Aleatoric Bridge] {msg}\n")
    sys.stderr.flush()


def proxy_to_remote(req):
    """
    Proxy a JSON-RPC request to the remote Aleatoric MCP endpoint.
    The remote server implements the standard MCP JSON-RPC 2.0 protocol.
    """
    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(
                f"{API_BASE_URL}/mcp",
                headers={
                    "X-API-Key": API_KEY,
                    "Content-Type": "application/json",
                },
                json=req
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        log(f"HTTP error from remote: {e.response.status_code} - {e.response.text}")
        return {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {
                "code": -32603,
                "message": f"Remote server error: {e.response.status_code}"
            }
        }
    except Exception as e:
        log(f"Failed to proxy request: {e}")
        return {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {"code": -32603, "message": str(e)}
        }


def handle_request(req):
    """
    Handle an incoming JSON-RPC request.

    Local handling for initialize (to return bridge info).
    All other requests are proxied to the remote MCP endpoint.
    """
    method = req.get("method")
    params = req.get("params", {})
    msg_id = req.get("id")

    # Handle initialize locally to identify as a bridge
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                }
            }
        }

    # Notifications don't need a response
    if method == "notifications/initialized":
        return None

    # All other methods are proxied to the remote server
    # This includes: ping, tools/list, tools/call
    return proxy_to_remote(req)


def main():
    log(f"Starting stdio bridge server v{SERVER_VERSION}...")
    log(f"Remote endpoint: {API_BASE_URL}/mcp")
    log(f"Protocol version: {MCP_PROTOCOL_VERSION}")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            req = json.loads(line)
            resp = handle_request(req)

            if resp:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            log(f"Invalid JSON: {e}")
            error_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
            sys.stdout.write(json.dumps(error_resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            log(f"Loop error: {e}")
            break


if __name__ == "__main__":
    main()
