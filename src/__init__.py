"""
Ollama Vision MCP Server
A Model Context Protocol server for computer vision using Ollama
"""

__version__ = "1.0.0"
__author__ = "Ollama Vision MCP Contributors"

from .server import OllamaVisionServer, main
from .ollama_client import OllamaClient
from .image_handler import ImageHandler
from .config import Config

__all__ = [
    "OllamaVisionServer",
    "OllamaClient", 
    "ImageHandler",
    "Config",
    "main"
]
