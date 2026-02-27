#!/bin/bash
# Quick runner for examples

set -e

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "✗ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check API key
if [ -z "$ALEATORIC_API_KEY" ] || [ "$ALEATORIC_API_KEY" = "your-api-key-here" ]; then
    echo "✗ ALEATORIC_API_KEY not set or still has default value"
    echo "  Edit .env and set your API key"
    exit 1
fi

# Run the specified example or default
EXAMPLE="${1:-funding_batch_diagnostics.py}"

echo "Running: $EXAMPLE"
echo ""

python "$EXAMPLE"
