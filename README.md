# Windows Notification MCP Server

A Model Context Protocol (MCP) server that provides Windows notifications.

## Features

- **Windows Notifications**: Send notifications to Windows systems
- **Cross-Platform Support**: Falls back to console output on non-Windows systems

## Installation

```bash
# Clone the repository
git clone https://github.com/aimino/notify-mcp.git
cd notify-mcp

# Install dependencies
pip install -e .
```

## Usage

Run the notification MCP server:

```bash
python -m mcp_server_notify
```

Example prompt to send a Windows notification:

```
notify(title="Alert", message="This is an important notification", urgency="high")
```

The `urgency` parameter is optional and defaults to "normal". Valid values are "low", "normal", and "high".

## Testing

A test script is provided to verify the functionality of the MCP server:

```bash
# Test the notification server
python test_notify.py
```

## How It Works

The MCP server implements the Model Context Protocol, allowing LLMs to interact with external systems. The notification server sends notifications to Windows systems using PowerShell.

On non-Windows systems, the notification server will print the notification details to the console instead.

## Development

This project uses Python 3.10+ and follows the MCP protocol specification. The implementation is based on the Python MCP SDK.

## License

MIT
