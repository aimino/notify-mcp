import asyncio
import json
import platform
import subprocess
import sys
import time
import os

def main():
    """Test the Windows notification MCP server."""
    print("Testing Windows Notification MCP Server")
    
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    try:
        print("Starting MCP server process...")
        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server_notify"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        if process.poll() is not None:
            print(f"Process failed to start with return code: {process.returncode}")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"Error output: {stderr_output}")
            return
            
        print("Process started successfully")
        time.sleep(1)
        
        system_name = platform.system()
        print(f"System detected: {system_name}")
        
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
        
        request_json = json.dumps(notify_request)
        print(f"Request JSON: {request_json}")
        
        print("Writing to server stdin...")
        process.stdin.write(request_json + "\n")
        process.stdin.flush()
        print("Flushed stdin")
        
        print("Reading response...")
        response_line = process.stdout.readline()
        if response_line:
            print(f"Raw response: {response_line}")
            try:
                response = json.loads(response_line)
                print("\nServer response:")
                print(json.dumps(response, indent=2))
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(f"Raw response: {response_line}")
        else:
            print("\nNo response received from server")
            
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Server stderr output: {stderr_output}")
    
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\nWaiting for notification to appear...")
    time.sleep(3)
    
    print("Terminating process...")
    try:
        process.terminate()
        process.wait(timeout=2)
        print("Process terminated")
    except Exception as e:
        print(f"Error terminating process: {e}")
        try:
            process.kill()
            print("Process killed")
        except:
            print("Failed to kill process")


if __name__ == "__main__":
    asyncio.run(main())
