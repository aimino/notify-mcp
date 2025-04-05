import subprocess
import sys
import os
import time
import json
import traceback

def test_mcp_server():
    """Test the MCP server using direct JSON-RPC requests to debug Cline connection issues."""
    print("Testing MCP Server for Cline compatibility")
    
    print("\nStarting MCP server process...")
    process = subprocess.Popen(
        [sys.executable, "-m", "mcp_server_notify"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffered
    )
    
    time.sleep(2)
    
    stderr_output = ""
    while process.stderr.readable() and not process.stderr.closed:
        line = process.stderr.readline()
        if not line:
            break
        stderr_output += line
    
    if stderr_output:
        print(f"STDERR during startup:\n{stderr_output}")
    
    if process.poll() is not None:
        print(f"ERROR: Server process exited prematurely with code {process.poll()}")
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"STDERR: {stderr_output}")
        return
    
    print("\nSending get_tools request...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_tools",
        "params": {}
    }
    
    try:
        request_str = json.dumps(tools_request) + "\n"
        print(f"Request: {request_str.strip()}")
        
        process.stdin.write(request_str)
        process.stdin.flush()
        
        print("Waiting for response...")
        response_line = process.stdout.readline().strip()
        
        if not response_line:
            print("ERROR: No response received from server")
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"STDERR: {stderr_output}")
        else:
            print("\nTools Response:")
            print(response_line)
            
            try:
                response_json = json.loads(response_line)
                print("\nParsed Response:")
                print(json.dumps(response_json, indent=2))
                
                print("\nSending notify request...")
                notify_request = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "get_prompt",
                    "params": {
                        "prompt": {
                            "name": "notify",
                            "arguments": [
                                {
                                    "name": "title",
                                    "value": "Cline Test"
                                },
                                {
                                    "name": "message",
                                    "value": "Testing notification from Cline debug script"
                                },
                                {
                                    "name": "urgency",
                                    "value": "normal"
                                }
                            ]
                        }
                    }
                }
                
                request_str = json.dumps(notify_request) + "\n"
                print(f"Request: {request_str.strip()}")
                process.stdin.write(request_str)
                process.stdin.flush()
                
                print("Waiting for notify response...")
                response_line = process.stdout.readline().strip()
                
                if not response_line:
                    print("ERROR: No response received for notify request")
                    stderr_output = process.stderr.read()
                    if stderr_output:
                        print(f"STDERR: {stderr_output}")
                else:
                    print("\nNotify Response:")
                    print(response_line)
                    
                    try:
                        response_json = json.loads(response_line)
                        print("\nParsed Notify Response:")
                        print(json.dumps(response_json, indent=2))
                    except json.JSONDecodeError as e:
                        print(f"ERROR: Failed to parse notify response as JSON: {e}")
                
            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to parse response as JSON: {e}")
    
    except Exception as e:
        print(f"ERROR during test: {e}")
        traceback.print_exc()
    
    finally:
        print("\nWaiting for notifications to appear...")
        time.sleep(3)
        
        print("\nTerminating server process...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("WARNING: Process did not terminate gracefully, killing...")
            process.kill()
        
        stdout_remainder = process.stdout.read()
        if stdout_remainder:
            print(f"\nRemaining STDOUT: {stdout_remainder}")
        
        stderr_remainder = process.stderr.read()
        if stderr_remainder:
            print(f"\nRemaining STDERR: {stderr_remainder}")

if __name__ == "__main__":
    test_mcp_server()
