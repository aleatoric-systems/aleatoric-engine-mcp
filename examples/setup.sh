#!/bin/bash
#
# Environment Setup Script for Aleatoric MCP Examples
#
# This script creates a Python virtual environment and installs all
# dependencies needed to run the examples.
#
# Usage:
#   bash setup.sh
#   # or
#   ./setup.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
VENV_DIR="venv"
PYTHON_MIN_VERSION="3.9"

echo -e "${BOLD}${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              ALEATORIC MCP EXAMPLES - ENVIRONMENT SETUP                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Function to print section headers
print_header() {
    echo -e "${BOLD}${CYAN}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print warnings
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to check Python version
check_python_version() {
    local python_cmd=$1

    if ! command -v "$python_cmd" &> /dev/null; then
        return 1
    fi

    local version=$($python_cmd --version 2>&1 | awk '{print $2}')
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)

    if [ "$major" -eq 3 ] && [ "$minor" -ge 9 ]; then
        echo "$python_cmd"
        return 0
    fi

    return 1
}

# ============================================================================
# Step 1: Check Python Installation
# ============================================================================

print_header "Step 1: Checking Python Installation"

PYTHON_CMD=""

# Try different Python commands
for cmd in python3.12 python3.11 python3.10 python3.9 python3 python; do
    if check_python_version "$cmd" > /dev/null 2>&1; then
        PYTHON_CMD=$(check_python_version "$cmd")
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    print_error "Python 3.9+ not found"
    echo ""
    echo "Please install Python 3.9 or higher:"
    echo ""
    echo "  macOS:   brew install python@3.11"
    echo "  Ubuntu:  sudo apt-get install python3.11"
    echo "  Windows: Download from python.org"
    echo ""
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_success "Found $PYTHON_CMD (version $PYTHON_VERSION)"
echo ""

# ============================================================================
# Step 2: Create Virtual Environment
# ============================================================================

print_header "Step 2: Creating Virtual Environment"

if [ -d "$VENV_DIR" ]; then
    print_warning "Virtual environment already exists at ./$VENV_DIR"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        print_warning "Using existing virtual environment"
        source "$VENV_DIR/bin/activate" 2>/dev/null || . "$VENV_DIR/Scripts/activate" 2>/dev/null
        echo ""
        # Skip to dependency installation
        SKIP_VENV_CREATION=true
    fi
fi

if [ "$SKIP_VENV_CREATION" != "true" ]; then
    echo "Creating virtual environment in ./$VENV_DIR..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    print_success "Virtual environment created"
    echo ""

    # Activate virtual environment
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate" 2>/dev/null || . "$VENV_DIR/Scripts/activate" 2>/dev/null

    if [ -n "$VIRTUAL_ENV" ]; then
        print_success "Virtual environment activated"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
    echo ""
fi

# ============================================================================
# Step 3: Upgrade pip
# ============================================================================

print_header "Step 3: Upgrading pip"

echo "Upgrading pip to latest version..."
python -m pip install --upgrade pip --quiet
PIP_VERSION=$(pip --version | awk '{print $2}')
print_success "pip upgraded to version $PIP_VERSION"
echo ""

# ============================================================================
# Step 4: Install Dependencies
# ============================================================================

print_header "Step 4: Installing Dependencies"

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found"
    exit 1
fi

echo "Installing packages from requirements.txt..."
echo ""

# Install with progress
pip install -r requirements.txt

echo ""
print_success "All dependencies installed"
echo ""

# Show installed packages
echo "Installed packages:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pip list --format=columns | grep -E "httpx|matplotlib|pandas|numpy|python-dotenv" || true
echo ""

# ============================================================================
# Step 5: Environment Configuration
# ============================================================================

print_header "Step 5: Environment Configuration"

ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "../$ENV_EXAMPLE" ]; then
        echo "Creating .env file from template..."
        cp "../$ENV_EXAMPLE" "$ENV_FILE"
        print_success "Created .env file"
        echo ""
        print_warning "IMPORTANT: Edit .env and add your ALEATORIC_API_KEY"
        echo ""
        echo "  1. Open .env in your editor"
        echo "  2. Replace 'your-api-key-here' with your actual API key"
        echo "  3. Save the file"
        echo ""
    else
        echo "Creating new .env file..."
        cat > "$ENV_FILE" << 'ENVEOF'
# Aleatoric MCP API Configuration
ALEATORIC_API_KEY=your-api-key-here

# Optional: Override MCP base URL (default: https://mcp.aleatoric.systems)
# MCP_BASE_URL=https://mcp.aleatoric.systems

# Optional: Logging level
# LOG_LEVEL=INFO
ENVEOF
        print_success "Created .env file"
        echo ""
        print_warning "IMPORTANT: Edit .env and add your ALEATORIC_API_KEY"
        echo ""
    fi
else
    print_success ".env file already exists"
    echo ""
fi

# ============================================================================
# Step 6: Verify Installation
# ============================================================================

print_header "Step 6: Verifying Installation"

echo "Running verification tests..."
echo ""

# Quick import test
python << 'PYTEST'
import sys

packages = {
    'httpx': 'HTTP client',
    'matplotlib': 'Plotting',
    'pandas': 'Data analysis',
    'numpy': 'Numerical computing',
}

print("Checking package imports:")
print("=" * 60)

all_good = True
for package, description in packages.items():
    try:
        __import__(package)
        print(f"✓ {package:15s} - {description}")
    except ImportError as e:
        print(f"✗ {package:15s} - FAILED: {e}")
        all_good = False

print("=" * 60)

if all_good:
    print("\n✓ All packages imported successfully!")
    sys.exit(0)
else:
    print("\n✗ Some packages failed to import")
    sys.exit(1)
PYTEST

if [ $? -eq 0 ]; then
    print_success "Package verification passed"
else
    print_error "Package verification failed"
    exit 1
fi

echo ""

# ============================================================================
# Step 7: Create Activation Helper Scripts
# ============================================================================

print_header "Step 7: Creating Helper Scripts"

# Create activation script for Unix
cat > activate.sh << 'ACTIVATEOF'
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
ACTIVATEOF

chmod +x activate.sh
print_success "Created activate.sh"

# Create activation script for Windows
cat > activate.bat << 'ACTIVATEBAT'
@echo off
REM Quick activation script for Windows

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
    echo To deactivate, run: deactivate
    echo.
    echo You can now run examples:
    echo   python funding_batch_diagnostics.py
    echo   python test_mcp_integration.py
    echo.
) else (
    echo Virtual environment not found. Run setup.sh first.
    exit /b 1
)
ACTIVATEBAT

print_success "Created activate.bat (Windows)"

# Create a simple run script
cat > run_example.sh << 'RUNEOF'
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
RUNEOF

chmod +x run_example.sh
print_success "Created run_example.sh"

echo ""

# ============================================================================
# Final Summary
# ============================================================================

echo -e "${BOLD}${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                          SETUP COMPLETE! 🎉                               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${BOLD}Environment Details:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Python:           $PYTHON_VERSION"
echo "  Virtual Env:      ./$VENV_DIR"
echo "  Configuration:    ./.env"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BOLD}Next Steps:${NC}"
echo ""
echo "  1. ${CYAN}Set your API key:${NC}"
echo "     Edit .env and replace 'your-api-key-here' with your actual key"
echo ""
echo "  2. ${CYAN}Activate the environment:${NC}"
echo "     source activate.sh              # Unix/macOS/Linux"
echo "     activate.bat                    # Windows"
echo ""
echo "  3. ${CYAN}Run validation tests:${NC}"
echo "     python test_funding_setup.py"
echo "     python test_mcp_integration.py"
echo ""
echo "  4. ${CYAN}Try the examples:${NC}"
echo "     python funding_batch_diagnostics.py"
echo "     bash demo_script.sh"
echo ""

echo -e "${BOLD}Helper Scripts Created:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  activate.sh       - Quick activation (Unix/macOS/Linux)"
echo "  activate.bat      - Quick activation (Windows)"
echo "  run_example.sh    - Run examples with auto-activation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${BOLD}Quick Start:${NC}"
echo ""
echo "  # Edit your API key"
echo "  nano .env  # or vim .env, or code .env"
echo ""
echo "  # Run an example"
echo "  ./run_example.sh funding_batch_diagnostics.py"
echo ""

echo -e "${YELLOW}⚠  Remember to set your ALEATORIC_API_KEY in .env before running examples!${NC}"
echo ""
