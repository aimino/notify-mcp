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

## Cline Integration

To use this MCP server with Cline, create a `cline_mcp_settings.json` file in your Cline configuration directory:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "python -m mcp_server_notify",
      "cwd": "/path/to/notify-mcp"
    }
  }
}
```

Replace `/path/to/notify-mcp` with the actual path to your cloned repository.

You can then use the notification functionality in Cline with:

```
/notify title="Alert" message="This is an important notification" urgency="high"
```

## How It Works

The MCP server implements the Model Context Protocol, allowing LLMs to interact with external systems. The notification server sends notifications to Windows systems using the Windows API through ctypes.

On non-Windows systems, the notification server will print the notification details to the console instead.

## Dependencies

This project requires the following dependencies:
- mcp>=1.1.3: The Model Context Protocol SDK
- Standard Python libraries (ctypes is used for Windows notifications)
- Other dependencies listed in requirements.txt

## Development

This project uses Python 3.10+ and follows the MCP protocol specification. The implementation is based on the Python MCP SDK.

## License

MIT
