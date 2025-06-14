#!/bin/bash

echo "===================================="
echo "Ollama Vision MCP Setup (Unix/Linux)"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Upgrading pip..."
pip install --upgrade pip

echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[5/5] Installing package in development mode..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to install in development mode"
    echo "Continuing with basic installation..."
fi

echo
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo
echo "Virtual environment created at: $(pwd)/venv"
echo
echo "To use this server:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Pull a vision model: ollama pull llava-phi3"
echo "3. Configure your MCP client with:"
echo "   Command: $(pwd)/venv/bin/python"
echo "   Args: -m src.server"
echo "   CWD: $(pwd)"
echo
echo "To activate the virtual environment manually:"
echo "   source venv/bin/activate"
echo
