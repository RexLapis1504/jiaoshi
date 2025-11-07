#!/bin/bash

# AI Paper Checker - Setup Script

echo "========================================"
echo "AI Paper Checker - Setup"
echo "========================================"
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✅ Python version OK"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run validation
echo "[5/5] Validating installation..."
python validate_structure.py
echo ""

# Check for API key
echo "========================================"
echo "Configuration"
echo "========================================"
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   For AI-powered grading, set the environment variable:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "   Without it, the system will use rule-based grading."
else
    echo "✅ OPENAI_API_KEY is set"
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:7860"
echo ""
echo "To run tests:"
echo "  python test_system.py"
echo ""
