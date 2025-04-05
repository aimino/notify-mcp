import platform
import subprocess
import sys
import time
import os

def main():
    """Test the Windows notification MCP server directly."""
    print("Testing Windows Notification MCP Server")
    
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    system_name = platform.system()
    print(f"System detected: {system_name}")
    
    cmd = [
        sys.executable, 
        "-c", 
        f"""
import sys
from mcp_server_notify.server import send_windows_notification

success = send_windows_notification(
    title="MCP Test on {system_name}",
    message="This is a test notification from the MCP server.",
    urgency="normal"
)

print(f"Notification sent: {{success}}")
sys.exit(0 if success else 1)
        """
    ]
    
    print("\nSending notification directly...")
    print(f"Title: MCP Test on {system_name}")
    print(f"Message: This is a test notification from the MCP server.")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        print("\nCommand output:")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("Notification sent successfully!")
        else:
            print("Failed to send notification.")
    
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\nWaiting for notification to appear...")
    time.sleep(3)
    print("Test completed.")


if __name__ == "__main__":
    main()
