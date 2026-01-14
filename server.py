#!/usr/bin/env python3
"""
Aleatoric MCP Bridge Server (Stdio)

This script acts as a local MCP server that proxies requests to the 
remote Aleatoric Production API. It enables compatibility with 
clients that require a local stdio transport (like MCP Inspector 
or Claude Desktop running locally).
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

def log(msg):
    sys.stderr.write(f"[Aleatoric Bridge] {msg}\n")
    sys.stderr.flush()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    msg_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2025-11-25",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "aleatoric-bridge",
                    "version": "0.1.0"
                }
            }
        }
    
    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        # Fetch manifest from remote
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(f"{API_BASE_URL}/.well-known/mcp.json")
                resp.raise_for_status()
                manifest = resp.json()
                
                # Transform to MCP structure
                tools = []
                for t in manifest.get("tools", []):
                    # Schema needs to be fetched or mocked if not in manifest
                    # The simple manifest lacks inputSchema. 
                    # We'll fetch full schema from /mcp/config/schema for validate
                    input_schema = {
                        "type": "object", 
                        "properties": {},
                        "required": []
                    }
                    
                    if t["name"] == "generate_dataset":
                         input_schema = {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string"},
                                "duration_seconds": {"type": "integer"},
                                "seed": {"type": "integer"}
                            },
                            "required": ["symbol"]
                        }
                    
                    tools.append({
                        "name": t["name"],
                        "description": t["description"],
                        "inputSchema": input_schema
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": tools
                    }
                }
        except Exception as e:
            log(f"Failed to fetch tools: {e}")
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32603, "message": str(e)}}

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "generate_dataset":
            # Proxy to /data/generate
            try:
                payload = {
                    "config": {
                        "symbol": args.get("symbol"),
                        "seed": args.get("seed"),
                    },
                    "duration_seconds": int(args.get("duration_seconds", 60))
                }
                
                with httpx.Client(timeout=60.0) as client:
                    resp = client.post(
                        f"{API_BASE_URL}/data/generate",
                        headers={"X-API-Key": API_KEY},
                        json=payload
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{
                                "type": "text",
                                "text": json.dumps(data, indent=2)
                            }]
                        }
                    }
            except Exception as e:
                 return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32603, "message": str(e)}}

    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    log("Starting stdio server...")
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
                
        except Exception as e:
            log(f"Loop error: {e}")
            break

if __name__ == "__main__":
    main()
