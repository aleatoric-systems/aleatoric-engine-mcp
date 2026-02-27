#!/bin/bash
# Quick activation script for the virtual environment

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
    echo ""
    echo "To deactivate, run: deactivate"
    echo ""

    # Load .env if it exists
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | xargs)
        echo "✓ Environment variables loaded from .env"
        echo ""
    fi

    echo "You can now run examples:"
    echo "  python funding_batch_diagnostics.py"
    echo "  python test_mcp_integration.py"
    echo "  bash demo_script.sh"
    echo ""
else
    echo "✗ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi
