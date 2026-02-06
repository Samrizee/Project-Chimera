import json
import os
import asyncio
from typing import Dict, Any, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, config_path: str = ".cursor/mcp.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.session: Optional[ClientSession] = None
        self._exit_stack = None

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            print(f"[MCPClient] Config file not found at {self.config_path}")
            return {}
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[MCPClient] Error loading config: {e}")
            return {}

    async def connect(self, server_name: str):
        servers = self.config.get('mcpServers', {})
        if server_name not in servers:
            raise ValueError(f"Server '{server_name}' not found in configuration.")

        server_config = servers[server_name]
        url = server_config.get('url')
        headers = server_config.get('headers', {})

        if url:
             # SSE Connection
            print(f"[MCPClient] Connecting to {server_name} via SSE at {url}...")
            # Note: mcp.client.sse.sse_client is a context manager
            # We need to maintain the context
            self.sse_ctx = sse_client(url=url, headers=headers)
            self._transport = await self.sse_ctx.__aenter__()
            self._read_stream, self._write_stream = self._transport
            
            self.session_ctx = ClientSession(self._read_stream, self._write_stream)
            self.session = await self.session_ctx.__aenter__()
            
            await self.session.initialize()
            print(f"[MCPClient] Connected to {server_name}")
            
        else:
            # Fallback to Stdio (not implemented for remote URL requirement but good for completeness)
            command = server_config.get('command')
            args = server_config.get('args', [])
            env = server_config.get('env', {})
            
            print(f"[MCPClient] Connecting to {server_name} via Stdio...")
            server_params = StdioServerParameters(command=command, args=args, env=env)
            
            self.stdio_ctx = stdio_client(server_params)
            self._transport = await self.stdio_ctx.__aenter__()
            self._read_stream, self._write_stream = self._transport
            
            self.session_ctx = ClientSession(self._read_stream, self._write_stream)
            self.session = await self.session_ctx.__aenter__()
            
            await self.session.initialize()
            print(f"[MCPClient] Connected to {server_name}")

    async def list_tools(self):
        if not self.session:
            raise RuntimeError("Not connected to any MCP server.")
        return await self.session.list_tools()

    async def call_tool(self, name: str, arguments: dict):
        if not self.session:
            raise RuntimeError("Not connected to any MCP server.")
        return await self.session.call_tool(name, arguments)

    async def close(self):
        if self.session:
            await self.session_ctx.__aexit__(None, None, None)
        # Handle transport cleanup based on type
        if hasattr(self, 'sse_ctx'):
             await self.sse_ctx.__aexit__(None, None, None)
        if hasattr(self, 'stdio_ctx'):
             await self.stdio_ctx.__aexit__(None, None, None)
        print("[MCPClient] Session closed.")
