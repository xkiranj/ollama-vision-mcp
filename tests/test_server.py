#!/usr/bin/env python3
"""
Test script for Ollama Vision MCP Server
Verifies that all components are working correctly
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.ollama_client import OllamaClient
from src.image_handler import ImageHandler

async def test_ollama_connection():
    """Test connection to Ollama"""
    print("Testing Ollama connection...")
    config = Config()
    client = OllamaClient(config)
    
    connected = await client.check_connection()
    if connected:
        print("✅ Successfully connected to Ollama")
        
        # List available models
        models = await client.list_models()
        if models:
            print(f"✅ Found {len(models)} vision models:")
            for model in models:
                print(f"   - {model}")
        else:
            print("❌ No vision models found. Please run: ollama pull llava-phi3")
            return False
    else:
        print("❌ Failed to connect to Ollama")
        print("   Make sure Ollama is running: ollama serve")
        return False
    
    return True

async def test_image_handler():
    """Test image handling capabilities"""
    print("\nTesting image handler...")
    handler = ImageHandler()
    
    # Create a test image
    test_image_path = Path(__file__).parent / "test_image.png"
    
    if not test_image_path.exists():
        print("ℹ️  Creating test image...")
        from PIL import Image, ImageDraw
        
        # Create a simple test image
        img = Image.new('RGB', (200, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), "Test Image", fill='black')
        img.save(test_image_path)
        print(f"✅ Created test image at: {test_image_path}")
    
    # Test loading the image
    try:
        encoded = await handler.process_image(str(test_image_path))
        print(f"✅ Successfully processed image (encoded length: {len(encoded)})")
        return True
    except Exception as e:
        print(f"❌ Failed to process image: {e}")
        return False

async def test_vision_analysis():
    """Test actual vision analysis"""
    print("\nTesting vision analysis...")
    
    config = Config()
    client = OllamaClient(config)
    handler = ImageHandler()
    
    # Use test image
    test_image_path = Path(__file__).parent / "test_image.png"
    
    try:
        # Process image
        image_data = await handler.process_image(str(test_image_path))
        
        # Analyze with Ollama
        print(f"Analyzing image with {config.default_model}...")
        result = await client.analyze_image(
            image_data,
            "Describe what you see in this image",
            config.default_model
        )
        
        print("✅ Analysis successful!")
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔍 Ollama Vision MCP Server Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: Ollama connection
    if not await test_ollama_connection():
        all_passed = False
        print("\n⚠️  Cannot proceed without Ollama connection")
        return
    
    # Test 2: Image handler
    if not await test_image_handler():
        all_passed = False
    
    # Test 3: Vision analysis
    if not await test_vision_analysis():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! The server is ready to use.")
        print("\nNext steps:")
        print("1. Add the server to your MCP client configuration")
        print("2. Restart your MCP client")
        print("3. Start analyzing images!")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
