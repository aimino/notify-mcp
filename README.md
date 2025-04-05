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
      "command": "python",
      "args": [
        "-m",
        "mcp_server_notify"
      ],
      "env": {
        "PYTHONPATH": "E:\\path\\to\\notify-mcp"
      },
      "disabled": false
    }
  }
}
```

For Windows users, use the following format with absolute paths:

```json
{
  "mcpServers": {
    "notify-mcp": {
      "command": "C:\\Users\\username\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
      "args": [
        "E:\\path\\to\\notify-mcp\\cline_server.py"
      ],
      "disabled": false
    }
  }
}
```

Important notes:
1. Replace `C:\\Users\\username\\AppData\\Local\\Programs\\Python\\Python312\\python.exe` with the absolute path to your Python executable
2. Replace `E:\\path\\to\\notify-mcp` with the absolute path to your cloned repository
3. Use double backslashes (`\\`) in Windows paths
4. The `disabled` field should be set to `false`
5. Note that `command` and `args` are separate fields, not combined into one string

You can then use the notification functionality in Cline with:

```
/notify title="Alert" message="This is an important notification" urgency="high"
```

## How It Works

The MCP server implements the Model Context Protocol, allowing LLMs to interact with external systems. The notification server sends notifications to Windows systems using the win10toast library for toast notifications.

On non-Windows systems, the notification server will print the notification details to the console instead.

## Dependencies

This project requires the following dependencies:
- mcp>=1.1.3: The Model Context Protocol SDK
- win10toast>=0.9.0: For Windows toast notifications
- Other dependencies listed in requirements.txt

## Development

This project uses Python 3.10+ and follows the MCP protocol specification. The implementation is based on the Python MCP SDK.

## License

MIT
