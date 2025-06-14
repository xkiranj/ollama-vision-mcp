#!/usr/bin/env python3
"""
Ollama Vision MCP Server
A Model Context Protocol server providing computer vision capabilities using Ollama
"""

import asyncio
import base64
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from .ollama_client import OllamaClient
from .image_handler import ImageHandler
from .config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaVisionServer:
    def __init__(self):
        self.server = Server("ollama-vision-mcp")
        self.config = Config()
        self.ollama_client = OllamaClient(self.config)
        self.image_handler = ImageHandler()
        
        # Register handlers
        self.setup_handlers()
        
    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List all available tools"""
            return [
                types.Tool(
                    name="analyze_image",
                    description="Analyze an image and provide detailed description with optional custom prompt",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Path to image file or URL"
                            },
                            "prompt": {
                                "type": "string",
                                "description": "Optional custom prompt for analysis"
                            },
                            "model": {
                                "type": "string",
                                "description": "Optional Ollama model to use"
                            }
                        },
                        "required": ["image_path"]
                    }
                ),
                types.Tool(
                    name="describe_image",
                    description="Get a comprehensive description of what's in the image",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Path to image file or URL"
                            }
                        },
                        "required": ["image_path"]
                    }
                ),
                types.Tool(
                    name="identify_objects",
                    description="List all identifiable objects in the image",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Path to image file or URL"
                            }
                        },
                        "required": ["image_path"]
                    }
                ),
                types.Tool(
                    name="read_text",
                    description="Extract visible text from the image",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Path to image file or URL"
                            }
                        },
                        "required": ["image_path"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str,
            arguments: Optional[Dict[str, Any]] = None
        ) -> Sequence[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool execution"""
            try:
                if not arguments:
                    raise ValueError("No arguments provided")
                
                image_path = arguments.get("image_path")
                if not image_path:
                    raise ValueError("image_path is required")
                
                # Process the image
                image_data = await self.image_handler.process_image(image_path)
                
                # Call the appropriate tool
                if name == "analyze_image":
                    prompt = arguments.get("prompt", "Describe this image in detail")
                    model = arguments.get("model", self.config.default_model)
                    result = await self.ollama_client.analyze_image(image_data, prompt, model)
                    
                elif name == "describe_image":
                    prompt = "Provide a comprehensive description of this image, including all visible elements, colors, composition, and any notable details"
                    result = await self.ollama_client.analyze_image(image_data, prompt)
                    
                elif name == "identify_objects":
                    prompt = "List all identifiable objects in this image. Format as a bulleted list"
                    result = await self.ollama_client.analyze_image(image_data, prompt)
                    
                elif name == "read_text":
                    prompt = "Extract and transcribe all visible text in this image. If no text is visible, say 'No text found'"
                    result = await self.ollama_client.analyze_image(image_data, prompt)
                    
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [types.TextContent(type="text", text=result)]
                
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                error_msg = f"Error: {str(e)}"
                return [types.TextContent(type="text", text=error_msg)]
    
    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="ollama-vision-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

def main():
    """Main entry point"""
    try:
        server = OllamaVisionServer()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
