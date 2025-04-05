import asyncio
import platform
import subprocess
import sys

async def main():
    """Test the Windows notification MCP server."""
    print("Testing Windows Notification MCP Server")
    
    process = subprocess.Popen(
        [sys.executable, "-m", "mcp_server_notify"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    system_name = platform.system()
    print(f"\nSending notification to {system_name}:")
    print(f"Title: MCP Test on {system_name}")
    print(f"Message: This is a test notification from the MCP server.")
    
    process.terminate()
    process.wait()

if __name__ == "__main__":
    asyncio.run(main())
