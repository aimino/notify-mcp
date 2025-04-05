import asyncio
import json
import platform
import subprocess
import sys
import time

async def main():
    """Test the Windows notification MCP server."""
    print("Testing Windows Notification MCP Server")
    
    process = subprocess.Popen(
        [sys.executable, "-m", "mcp_server_notify"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    time.sleep(1)
    
    system_name = platform.system()
    
    notify_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_prompt",
        "params": {
            "prompt": {
                "name": "notify",
                "arguments": [
                    {
                        "name": "title",
                        "value": f"MCP Test on {system_name}"
                    },
                    {
                        "name": "message",
                        "value": "This is a test notification from the MCP server."
                    },
                    {
                        "name": "urgency",
                        "value": "normal"
                    }
                ]
            }
        }
    }
    
    print(f"\nSending notification to {system_name}:")
    print(f"Title: MCP Test on {system_name}")
    print(f"Message: This is a test notification from the MCP server.")
    
    try:
        process.stdin.write(json.dumps(notify_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print("\nServer response:")
            print(json.dumps(response, indent=2))
        else:
            print("\nNo response received from server")
    except Exception as e:
        print(f"\nError during test: {str(e)}")
    
    print("\nWaiting for notification to appear...")
    time.sleep(3)
    
    process.terminate()
    process.wait()

if __name__ == "__main__":
    asyncio.run(main())
