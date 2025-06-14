# Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Ollama (if not already installed)

**Windows**: Download from https://ollama.ai/download/windows

**macOS/Linux**:
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama & Get Vision Model

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull vision model
ollama pull llava-phi3
```

### 3. Install Ollama Vision MCP

```bash
# Option A: From source (recommended for now)
cd C:\Users\ekirjad\MCP\ollama-vision-mcp
pip install -e .

# Option B: Using pip directly
pip install -r requirements.txt
```

### 4. Test Installation

```bash
cd C:\My_Files\ollama-vision-mcp
python tests/test_server.py
```

### 5. Configure Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

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

### 6. Restart Claude Desktop

Close and reopen Claude Desktop to load the new server.

### 7. Test It!

Try these commands in Claude:
- "Describe the image at C:/path/to/your/image.jpg"
- "What objects are in this image: C:/path/to/photo.png"
- "Read the text from C:/path/to/document.png"

## ✅ Success Indicators

You'll know it's working when:
1. `ollama list` shows llava-phi3
2. Test script shows all green checkmarks
3. Claude can analyze your images

## 🔧 Troubleshooting

**"Cannot connect to Ollama"**
```bash
# Make sure Ollama is running
ollama serve
```

**"No vision models found"**
```bash
# Pull the model
ollama pull llava-phi3
```

**"Module not found"**
```bash
# Install dependencies
pip install -r requirements.txt
```
