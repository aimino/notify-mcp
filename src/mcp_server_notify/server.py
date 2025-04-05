from typing import Annotated, Tuple
import platform
import subprocess
import os
import time
from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field

class NotificationRequest(BaseModel):
    title: str = Field(..., description="Title of the notification")
    message: str = Field(..., description="Content of the notification")
    urgency: str = Field("normal", description="Urgency level (low, normal, high)")

def send_windows_notification(title: str, message: str, urgency: str = "normal") -> bool:
    """Send a notification to Windows.
    
    Args:
        title: Title of the notification
        message: Content of the notification
        urgency: Urgency level (low, normal, high)
        
    Returns:
        True if notification was sent successfully, False otherwise
    """
    if platform.system() != "Windows":
        print(f"NOTIFICATION [{urgency.upper()}]:")
        print(f"Title: {title}")
        print(f"Message: {message}")
        return True
    
    try:
        from win10toast import ToastNotifier
        
        toaster = ToastNotifier()
        
        duration = 5  # Default duration in seconds
        if urgency == "low":
            duration = 3
        elif urgency == "high":
            duration = 10
        
        toaster.show_toast(
            title=title,
            msg=message,
            duration=duration,
            threaded=True  # Run in a separate thread so it doesn't block
        )
        
        time.sleep(0.5)
        
        return True
    except Exception as e:
        print(f"Error sending Windows notification: {str(e)}")
        print(f"NOTIFICATION [{urgency.upper()}]:")
        print(f"Title: {title}")
        print(f"Message: {message}")
        return False

class NotifyServer(Server):
    """MCP server that provides Windows notifications."""
    
    def __init__(self):
        super().__init__(name="notify")
        
    async def handle_prompt(self, prompt: Prompt) -> GetPromptResult:
        """Handle a prompt from the client."""
        
        if prompt.name == "notify":
            try:
                title_arg = next((arg for arg in prompt.arguments if arg.name == "title"), None)
                message_arg = next((arg for arg in prompt.arguments if arg.name == "message"), None)
                urgency_arg = next((arg for arg in prompt.arguments if arg.name == "urgency"), None)
                
                if not title_arg:
                    return GetPromptResult(
                        error=ErrorData(
                            code=INVALID_PARAMS,
                            message="Missing required 'title' argument",
                        )
                    )
                
                if not message_arg:
                    return GetPromptResult(
                        error=ErrorData(
                            code=INVALID_PARAMS,
                            message="Missing required 'message' argument",
                        )
                    )
                
                title = title_arg.value
                message = message_arg.value
                urgency = urgency_arg.value if urgency_arg else "normal"
                
                success = send_windows_notification(title, message, urgency)
                
                if success:
                    response_text = f"""
Notification sent successfully:
- **Title**: {title}
- **Message**: {message}
- **Urgency**: {urgency}
"""
                else:
                    response_text = "Failed to send notification."
                
                return GetPromptResult(
                    messages=[
                        PromptMessage(
                            content=TextContent(text=response_text),
                        )
                    ]
                )
                
            except Exception as e:
                return GetPromptResult(
                    error=ErrorData(
                        code=INTERNAL_ERROR,
                        message=f"Error processing notification request: {str(e)}",
                    )
                )
        
        else:
            return GetPromptResult(
                error=ErrorData(
                    code=INVALID_PARAMS,
                    message=f"Unknown prompt: {prompt.name}",
                )
            )

    async def get_tools(self) -> list[Tool]:
        """Return the list of tools provided by this server."""
        return [
            Tool(
                name="notify",
                description="Send a notification to Windows",
                arguments=[
                    PromptArgument(
                        name="title",
                        description="Title of the notification",
                        required=True,
                    ),
                    PromptArgument(
                        name="message",
                        description="Content of the notification",
                        required=True,
                    ),
                    PromptArgument(
                        name="urgency",
                        description="Urgency level (low, normal, high)",
                        required=False,
                    ),
                ],
            ),
        ]

def main():
    """Run the notification MCP server."""
    stdio_server(NotifyServer())

if __name__ == "__main__":
    main()
