# Ollama Vision MCP Server

A Model Context Protocol (MCP) server that provides powerful computer vision capabilities using Ollama's vision models. This server enables AI assistants like Claude Desktop and development tools like Cursor IDE to analyze images locally without any API costs.

## 🌟 Features

- **Local Processing**: All image analysis happens on your machine - no cloud APIs, no costs
- **Privacy First**: Your images never leave your computer
- **Multiple Vision Models**: Support for llava-phi3, llava:7b, llava:13b, and bakllava
- **Comprehensive Tools**:
  - `analyze_image` - Custom image analysis with optional prompts
  - `describe_image` - Detailed image descriptions
  - `identify_objects` - Object detection and listing
  - `read_text` - Text extraction from images (OCR-like capabilities)
- **Flexible Input**: Supports local files, URLs, and base64 encoded images
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

### 1. Install Ollama

First, you need to install Ollama on your system:

#### Windows
Download and install from: https://ollama.ai/download/windows

#### macOS
```bash
brew install ollama
```
Or download from: https://ollama.ai/download/mac

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama

Make sure Ollama is running:
```bash
ollama serve
```

### 3. Pull a Vision Model

Download at least one vision model (llava-phi3 recommended for efficiency):
```bash
ollama pull llava-phi3
```

Other available models:
```bash
ollama pull llava:7b     # More capable, requires more RAM
ollama pull llava:13b    # Most capable, requires significant RAM
ollama pull bakllava     # Alternative vision model
```

### 4. Test Ollama

Verify everything is working:
```bash
ollama run llava-phi3 "describe a simple scene"
```

## 🚀 Installation

### Important: Use Virtual Environment (Recommended)

Using a virtual environment is strongly recommended to avoid conflicts with system Python packages:

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Option 1: Install from GitHub (Recommended)
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ollama-vision-mcp
cd ollama-vision-mcp

# Create and activate virtual environment (see above)
# Then install in development mode
pip install -e .
```

### Option 2: Install from PyPI (Coming Soon)
```bash
# Create and activate virtual environment (see above)
# Then install
pip install ollama-vision-mcp
```

### Option 3: Manual Installation
```bash
# Clone or download this repository
cd ollama-vision-mcp

# Create and activate virtual environment (see above)
# Then install dependencies
pip install -r requirements.txt
```

### Deactivating Virtual Environment
When you're done working with the project:
```bash
# Windows
deactivate

# macOS/Linux
deactivate
```

## ⚙️ Configuration

### Environment Variables

You can configure the server using environment variables:

```bash
# Ollama API URL (default: http://localhost:11434)
export OLLAMA_VISION_OLLAMA_URL=http://localhost:11434

# Default model (default: llava-phi3)
export OLLAMA_VISION_DEFAULT_MODEL=llava-phi3

# Request timeout in seconds (default: 120)
export OLLAMA_VISION_TIMEOUT=120

# Log level (default: INFO)
export OLLAMA_VISION_LOG_LEVEL=INFO
```

### Timeout Configuration for MCP Clients

When using this server with MCP clients like EricAI-MCP-Chat, you may need to configure client-side timeouts to match the server's processing time:

#### EricAI-MCP-Chat Configuration

In your `mcp_config.json`:

```json
{
  "servers": {
    "ollama-vision-mcp": {
      "enabled": true,
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\path\\to\\ollama-vision-mcp",
      "Allowed Paths": "C:\\path\\to\\allowed_folder_1; C:\\path\\to\\allowed_folder_2",
      "timeout": 10,       // General timeout for initialization (seconds)
      "toolTimeout": 120   // Timeout for image analysis operations (seconds)
    }
  }
}
```

**Note**: The `toolTimeout` should match or exceed the server's `OLLAMA_VISION_TIMEOUT` value to prevent premature disconnections during image analysis.

### Configuration File

Create `ollama-vision-config.json` in your working directory:

```json
{
  "ollama_url": "http://localhost:11434",
  "default_model": "llava-phi3",
  "timeout": 120,
  "log_level": "INFO",
  "cache_enabled": false,
  "model_preferences": [
    "llava-phi3",
    "llava:7b",
    "llava:13b",
    "bakllava"
  ]
}
```

## 🔧 Integration

### Claude Desktop

Add to your Claude Desktop configuration:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

#### Using Virtual Environment (Recommended)
```json
{
  "mcpServers": {
    "ollama-vision": {
      "command": "C:\\path\\to\\ollama-vision-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "src.server"],
      "cwd": "C:\\path\\to\\ollama-vision-mcp"
    }
  }
}
```

**macOS/Linux with venv:**
```json
{
  "mcpServers": {
    "ollama-vision": {
      "command": "/path/to/ollama-vision-mcp/venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/ollama-vision-mcp"
    }
  }
}
```

#### Without Virtual Environment
```json
{
  "mcpServers": {
    "ollama-vision": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\path\\to\\ollama-vision-mcp"
    }
  }
}
```

### Cursor IDE

Add to your Cursor settings:

```json
{
  "mcp.servers": {
    "ollama-vision": {
      "command": "ollama-vision-mcp",
      "env": {
        "OLLAMA_VISION_DEFAULT_MODEL": "llava-phi3"
      }
    }
  }
}
```

### EricAI-MCP-Chat

Add to your `config/mcp_config.json`:

#### With Virtual Environment (Recommended)
```json
{
  "servers": {
    "ollama-vision-mcp": {
      "enabled": true,
      "command": "C:\\path\\to\\ollama-vision-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "src.server"],
      "cwd": "C:\\path\\to\\ollama-vision-mcp",
      "autoStart": false,
      "description": "Ollama vision model for image analysis",
      "timeout": 10,
      "toolTimeout": 120,
      "env": {
        "OLLAMA_VISION_DEFAULT_MODEL": "llava-phi3",
        "OLLAMA_VISION_TIMEOUT": "120"
      }
    }
  }
}
```

#### Without Virtual Environment
```json
{
  "servers": {
    "ollama-vision-mcp": {
      "enabled": true,
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "C:\\path\\to\\ollama-vision-mcp",
      "autoStart": false,
      "description": "Ollama vision model for image analysis",
      "timeout": 10,
      "toolTimeout": 120,
      "env": {
        "OLLAMA_VISION_DEFAULT_MODEL": "llava-phi3",
        "OLLAMA_VISION_TIMEOUT": "120"
      }
    }
  }
}
```

**Key Configuration Notes:**
- Set `autoStart: false` to prevent automatic startup (start manually when needed)
- Configure `toolTimeout` to match or exceed the server's processing time
- Use environment variables to customize model and timeout settings

## 📖 Usage Examples

Once integrated with your MCP client, you can use natural language to analyze images:

### Basic Image Description
```
"Describe the image at /path/to/photo.jpg"
```

### Custom Analysis
```
"Analyze /path/to/diagram.png and explain the architecture"
```

### Object Detection
```
"What objects are in the image at /path/to/scene.jpg?"
```

### Text Extraction
```
"Read the text from /path/to/document.png"
```

### URL Image Analysis
```
"Describe what's in this image: https://example.com/image.jpg"
```

## 🧪 Testing

### Command Line Testing

Test the server directly:

```bash
# First activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then run your test script
python test_ollama_vision.py
```

Example test script:
```python
# test_ollama_vision.py
import asyncio
from src.server import OllamaVisionServer

async def test():
    server = OllamaVisionServer()
    # Test your implementation
    
asyncio.run(test())
```

### Run Tests
```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run tests
pytest tests/
```

## 🐛 Troubleshooting

### Common Issues

1. **"Ollama not found" Error**
   - Ensure Ollama is installed and running: `ollama serve`
   - Check if Ollama is accessible: `curl http://localhost:11434/api/tags`

2. **"No vision models available" Error**
   - Pull a vision model: `ollama pull llava-phi3`
   - List available models: `ollama list`

3. **Timeout Errors**
   - Increase timeout: `export OLLAMA_VISION_TIMEOUT=300`
   - First run may be slow as models load into memory

4. **Memory Issues**
   - llava-phi3 requires ~4GB RAM
   - llava:7b requires ~8GB RAM
   - llava:13b requires ~16GB RAM
   - Close other applications to free memory

### Debug Mode

Enable debug logging:
```bash
export OLLAMA_VISION_LOG_LEVEL=DEBUG
```

## 🔍 Performance Tips

1. **Model Selection**:
   - Use `llava-phi3` for fastest responses
   - Use larger models only when needed

2. **Image Optimization**:
   - Server automatically resizes large images
   - Pre-resize images to 1024x1024 for faster processing

3. **Hardware Acceleration**:
   - GPU acceleration significantly improves performance
   - Check Ollama GPU support for your system

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for providing local LLM capabilities
- [Model Context Protocol](https://modelcontextprotocol.io) for the MCP specification
- The open-source community for vision models like LLaVA

## 📬 Support

- **Issues**: [GitHub Issues](https://github.com/ollama-vision-mcp/ollama-vision-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ollama-vision-mcp/ollama-vision-mcp/discussions)
- **Wiki**: [Project Wiki](https://github.com/ollama-vision-mcp/ollama-vision-mcp/wiki)

---

Made with ❤️ for the MCP community
