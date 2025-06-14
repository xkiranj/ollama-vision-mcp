"""
Image Handler for Ollama Vision MCP
Handles image loading, validation, and preprocessing
"""

import base64
import io
import logging
import mimetypes
import os
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

import aiohttp
import aiofiles
from PIL import Image

logger = logging.getLogger(__name__)

class ImageHandler:
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
    
    def __init__(self):
        """Initialize the image handler"""
        pass
    
    async def process_image(self, image_path: str) -> str:
        """
        Process an image from various sources and return base64 encoded data
        
        Args:
            image_path: Path to local file, URL, or base64 string
            
        Returns:
            Base64 encoded image data
        """
        # Check if already base64
        if self._is_base64(image_path):
            return image_path
            
        # Check if URL
        if self._is_url(image_path):
            return await self._download_and_encode(image_path)
            
        # Handle local file
        return await self._load_local_image(image_path)
    
    def _is_base64(self, data: str) -> bool:
        """Check if string is base64 encoded"""
        try:
            if len(data) > 100 and ',' in data:
                # Check for data URL format
                if data.startswith('data:image'):
                    return True
            # Try to decode
            base64.b64decode(data, validate=True)
            return True
        except:
            return False
    
    def _is_url(self, path: str) -> bool:
        """Check if string is a URL"""
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    async def _download_and_encode(self, url: str) -> str:
        """Download image from URL and encode to base64"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to download image: HTTP {response.status}")
                    
                    content = await response.read()
                    if len(content) > self.MAX_IMAGE_SIZE:
                        raise ValueError(f"Image too large: {len(content)} bytes")
                    
                    # Validate image format
                    content_type = response.headers.get('content-type', '')
                    if not content_type.startswith('image/'):
                        raise ValueError(f"Invalid content type: {content_type}")
                    
                    # Process and encode
                    return await self._process_image_bytes(content)
                    
        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            raise
    
    async def _load_local_image(self, path: str) -> str:
        """Load and encode a local image file"""
        try:
            # Resolve path
            file_path = Path(path).resolve()
            
            # Check if file exists
            if not file_path.exists():
                raise FileNotFoundError(f"Image file not found: {path}")
            
            # Check file extension
            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported image format: {file_path.suffix}")
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > self.MAX_IMAGE_SIZE:
                raise ValueError(f"Image too large: {file_size} bytes")
            
            # Read and encode
            async with aiofiles.open(file_path, 'rb') as f:
                content = await f.read()
                return await self._process_image_bytes(content)
                
        except Exception as e:
            logger.error(f"Error loading local image {path}: {e}")
            raise
    
    async def _process_image_bytes(self, content: bytes) -> str:
        """Process image bytes and return base64 encoded string"""
        try:
            # Open image with PIL for validation and potential preprocessing
            image = Image.open(io.BytesIO(content))
            
            # Convert RGBA to RGB if needed (for JPEG compatibility)
            if image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            
            # Resize if too large (optional optimization)
            max_dimension = 2048
            if max(image.size) > max_dimension:
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                logger.info(f"Resized image to {image.size}")
            
            # Convert back to bytes
            buffer = io.BytesIO()
            format = 'JPEG' if image.mode == 'RGB' else 'PNG'
            image.save(buffer, format=format, quality=95 if format == 'JPEG' else None)
            buffer.seek(0)
            
            # Encode to base64
            encoded = base64.b64encode(buffer.read()).decode('utf-8')
            return encoded
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise
    
    def validate_image_path(self, path: str) -> bool:
        """Validate if path points to a valid image"""
        try:
            if self._is_base64(path) or self._is_url(path):
                return True
                
            file_path = Path(path)
            return (file_path.exists() and 
                    file_path.is_file() and 
                    file_path.suffix.lower() in self.SUPPORTED_FORMATS)
        except:
            return False
