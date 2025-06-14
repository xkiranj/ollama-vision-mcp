#!/usr/bin/env python3
"""
Setup script for Ollama Vision MCP Server
This provides backward compatibility for older pip versions
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ollama-vision-mcp",
    version="1.0.0",
    author="Ollama Vision MCP Contributors",
    description="A Model Context Protocol server providing computer vision capabilities using Ollama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ollama-vision-mcp/ollama-vision-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.9.1",
        "aiohttp>=3.8.0",
        "aiofiles>=23.0.0",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ollama-vision-mcp=src.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
