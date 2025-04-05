import asyncio
import sys
import platform
from mcp.client.stdio import stdio_client

async def main():
    """Test the Windows notification MCP server."""
    print("Testing Windows Notification MCP Server")
    
    async with stdio_client(["python", "-m", "mcp_server_notify"]) as client:
        tools = await client.get_tools()
        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print("  Arguments:")
            for arg in tool.arguments:
                print(f"    - {arg.name}: {arg.description} (required: {arg.required})")
        
        system_name = platform.system()
        result = await client.get_prompt(
            name="notify",
            arguments=[
                {"name": "title", "value": f"MCP Test on {system_name}"},
                {"name": "message", "value": "This is a test notification from the MCP server."},
                {"name": "urgency", "value": "normal"}
            ]
        )
        
        print("\nNotification result:")
        for message in result.messages:
            print(message.content.text)

if __name__ == "__main__":
    asyncio.run(main())
