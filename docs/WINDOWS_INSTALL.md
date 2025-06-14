# Windows Installation Guide

## Prerequisites

### 1. Install Python (if not already installed)
- Download Python 3.8+ from https://python.org
- **Important**: Check "Add Python to PATH" during installation

### 2. Install Ollama
1. Download Ollama for Windows: https://ollama.ai/download/windows
2. Run the installer
3. Open Command Prompt or PowerShell and verify:
   ```powershell
   ollama --version
   ```

### 3. Start Ollama Service
Open a new PowerShell window and run:
```powershell
ollama serve
```
Keep this window open!

### 4. Download Vision Model
Open another PowerShell window:
```powershell
ollama pull llava-phi3
```

## Installing Ollama Vision MCP

### Option 1: Install from Source (Recommended)

1. Open PowerShell in the project directory:
   ```powershell
   cd C:\Users\ekirjad\MCP\ollama-vision-mcp
   ```

2. Create a virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. Install the package:
   ```powershell
   pip install -e .
   ```

### Option 2: Direct Installation

```powershell
cd C:\Users\ekirjad\MCP\ollama-vision-mcp
pip install -r requirements.txt
```

## Configure Claude Desktop

1. Open File Explorer
2. Navigate to: `%APPDATA%\Claude`
3. Edit `claude_desktop_config.json` (create if it doesn't exist)
4. Add this configuration:

```json
{
  "mcpServers": {
    "ollama-vision": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\Users\\ekirjad\\MCP\\ollama-vision-mcp"
    }
  }
}
```

**Note**: Use double backslashes in JSON configuration files!

## Test the Installation

1. Run the test script:
   ```powershell
   cd C:\Users\ekirjad\MCP\ollama-vision-mcp
   python tests\test_server.py
   ```

2. You should see:
   - ✅ Successfully connected to Ollama
   - ✅ Found vision models
   - ✅ Successfully processed image
   - ✅ Analysis successful!

## Using with Claude Desktop

1. Restart Claude Desktop completely (close from system tray)
2. Open Claude Desktop
3. Try these commands:
   - "Describe what's in C:\Users\YourName\Pictures\photo.jpg"
   - "Read the text from C:\Documents\screenshot.png"

## Troubleshooting

### "python is not recognized"
- Reinstall Python and check "Add to PATH"
- Or use full path: `C:\Python311\python.exe`

### "ollama: command not found"
- Restart your computer after Ollama installation
- Or add Ollama to PATH manually

### "No module named 'mcp'"
```powershell
pip install mcp
```

### "Cannot connect to Ollama"
1. Make sure Ollama is running: `ollama serve`
2. Check if port 11434 is available
3. Try: `curl http://localhost:11434/api/tags`

### Performance Tips

- First analysis may take 30-60 seconds as model loads
- Subsequent analyses are much faster
- llava-phi3 is fastest, llava:13b is most accurate
- Close other applications to free RAM

## Updating

To update the server:
```powershell
cd C:\Users\ekirjad\MCP\ollama-vision-mcp
git pull
pip install -e . --upgrade
```

Then restart Claude Desktop.
