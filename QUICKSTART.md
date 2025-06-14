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
# Navigate to the project directory
cd C:\Users\ekirjad\MCP\ollama-vision-mcp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install the package
pip install -e .
# Or just install requirements
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
      "command": "C:\\Users\\ekirjad\\MCP\\ollama-vision-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "src.server"],
      "cwd": "C:\\Users\\ekirjad\\MCP\\ollama-vision-mcp"
    }
  }
}
```

**Note**: If you installed without virtual environment, use `"command": "python"` instead.

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
