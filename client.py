from contextlib import AsyncExitStack
import httpx

from mcp import ClientSession
from mcp.client.sse import sse_client

# 
class MCPSSEClient:
    def __init__(self, provider=None):
        # Initialize session and client objects
        self.exit_stack = AsyncExitStack()
        self.provider = provider
        self.session = None
        self._tools = None

    async def connect_to_server(self, url, **kwargs):
        try:
            sse_transport = await self.exit_stack.enter_async_context(sse_client(url, **kwargs))
            self.session = await self.exit_stack.enter_async_context(ClientSession(*sse_transport))

            response = await self.session.initialize()

            tools_response = await self.session.list_tools()

            self._tools = [tool.name for tool in tools_response.tools]

        except httpx.ConnectError as e:
            # Clean up any resources that were created before the error
            await self.cleanup()
            raise ConnectionError(f"Failed to connect to server at {url}: {str(e)}") from e

        return response

    @property
    def available_tools(self):
        return self._tools

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
