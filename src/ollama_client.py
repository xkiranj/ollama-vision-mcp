"""
Ollama API Client for Vision Models
Handles communication with Ollama API for image analysis
"""

import aiohttp
import asyncio
import base64
import json
import logging
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, config):
        self.config = config
        self.base_url = config.ollama_url
        self.timeout = aiohttp.ClientTimeout(total=config.timeout)
        
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """List available vision models"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        # Filter for vision models
                        vision_models = []
                        for model in models:
                            name = model.get("name", "")
                            if any(vm in name for vm in ["llava", "bakllava", "vision"]):
                                vision_models.append(name)
                        return vision_models
                    return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def analyze_image(
        self, 
        image_data: str, 
        prompt: str, 
        model: Optional[str] = None
    ) -> str:
        """Analyze an image using Ollama vision model"""
        if not model:
            model = self.config.default_model
            
        # Check if model is available
        available_models = await self.list_models()
        if model not in available_models:
            # Try to find a suitable fallback
            if available_models:
                logger.warning(f"Model {model} not found, using {available_models[0]}")
                model = available_models[0]
            else:
                raise ValueError("No vision models available. Please run 'ollama pull llava-phi3' first")
        
        # Prepare the request
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_data],
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "No response from model")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            raise Exception(f"Request timed out after {self.config.timeout} seconds")
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            raise
    
    async def ensure_model(self, model: str) -> bool:
        """Ensure a model is available, attempt to pull if not"""
        available_models = await self.list_models()
        if model in available_models:
            return True
            
        logger.info(f"Model {model} not found, attempting to pull...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model}
                ) as response:
                    if response.status == 200:
                        # Stream the response to show progress
                        async for line in response.content:
                            if line:
                                try:
                                    data = json.loads(line.decode())
                                    status = data.get("status", "")
                                    if status:
                                        logger.info(f"Pull status: {status}")
                                except:
                                    pass
                        return True
                    return False
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
