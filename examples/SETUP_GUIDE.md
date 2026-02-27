# Setup Guide - Aleatoric MCP Examples

Complete guide to setting up your environment for running the Aleatoric MCP examples.

## Quick Setup (2 minutes)

```bash
# 1. Run the automated setup script
bash setup.sh

# 2. Edit .env and add your API key
nano .env  # or use your preferred editor

# 3. Activate the environment
source activate.sh

# 4. Run validation
python test_funding_setup.py

# Done! You're ready to run examples
```

---

## Detailed Setup Instructions

### Prerequisites

**Required:**
- Python 3.9 or higher
- pip (usually comes with Python)
- Internet connection

**Optional:**
- Git (for cloning the repository)
- Virtual environment support (venv or virtualenv)

### Step 1: Get an API Key

1. Visit https://aleatoric.systems
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key (you'll need it in Step 4)

### Step 2: Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/aleatoric/aleatoric-engine-mcp.git
cd aleatoric-engine-mcp/examples
```

**Option B: Download ZIP**
1. Download the repository as ZIP
2. Extract to your desired location
3. Navigate to the `examples` directory

### Step 3: Run the Setup Script

The automated setup script will:
- Check your Python version
- Create a virtual environment
- Install all dependencies
- Create configuration files
- Verify the installation

**Run the setup:**
```bash
bash setup.sh
```

**What it does:**
```
✓ Checks for Python 3.9+
✓ Creates virtual environment in ./venv
✓ Upgrades pip to latest version
✓ Installs httpx, matplotlib, pandas, numpy
✓ Creates .env file from template
✓ Verifies all packages import correctly
✓ Creates helper scripts (activate.sh, run_example.sh)
```

### Step 4: Configure Environment Variables

Edit the `.env` file and add your API key:

```bash
nano .env
```

Replace the placeholder with your actual key:
```bash
ALEATORIC_API_KEY=your-actual-api-key-here
```

**Important:** Never commit `.env` to version control!

### Step 5: Activate the Virtual Environment

**Unix/macOS/Linux:**
```bash
source activate.sh
# or manually:
source venv/bin/activate
```

**Windows:**
```batch
activate.bat
# or manually:
venv\Scripts\activate.bat
```

**You should see:**
```
✓ Virtual environment activated
✓ Environment variables loaded from .env
```

### Step 6: Verify Installation

Run the validation test:
```bash
python test_funding_setup.py
```

**Expected output:**
```
Checking Python version...
  ✓ Python 3.11.x (compatible)

Checking dependencies...
  ✓ httpx          - HTTP client for API calls
  ✓ matplotlib     - Plotting and visualization
  ✓ pandas         - Data manipulation
  ✓ numpy          - Numerical operations

Checking API key...
  ✓ ALEATORIC_API_KEY is set

Checking output directory...
  ✓ Output directory is writable

✅ All checks passed! You're ready to run the example.
```

### Step 7: Test API Integration

Run the integration test (makes real API calls):
```bash
python test_mcp_integration.py
```

This will:
- Check MCP service health
- List available presets
- Generate 60 seconds of test data
- Simulate funding rates
- Test multi-exchange functionality

**If successful, you're all set!**

---

## Manual Setup (Alternative)

If the automated script doesn't work, you can set up manually:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Unix/macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```batch
venv\Scripts\activate.bat
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create .env File

```bash
cp .env.example .env
```

Edit `.env` and add your API key.

### 6. Verify

```bash
python test_funding_setup.py
```

---

## Platform-Specific Instructions

### macOS

**Install Python (if needed):**
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

**Run setup:**
```bash
cd aleatoric-engine-mcp/examples
bash setup.sh
```

### Ubuntu/Debian Linux

**Install Python (if needed):**
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip
```

**Run setup:**
```bash
cd aleatoric-engine-mcp/examples
bash setup.sh
```

### Windows

**Install Python (if needed):**
1. Download from https://www.python.org/downloads/
2. Run installer
3. Check "Add Python to PATH"
4. Complete installation

**Run setup:**
```batch
cd aleatoric-engine-mcp\examples
bash setup.sh
```

Note: You may need Git Bash or WSL to run the setup script.

**Alternative for Windows (using PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env
copy .env.example .env

# Edit .env with your API key
notepad .env
```

### Windows Subsystem for Linux (WSL)

Follow the Ubuntu/Debian instructions above.

---

## Helper Scripts

After running `setup.sh`, you'll have these helper scripts:

### activate.sh (Unix/macOS/Linux)

Quick activation with environment loading:
```bash
source activate.sh
```

### activate.bat (Windows)

Quick activation for Windows:
```batch
activate.bat
```

### run_example.sh

Run examples with automatic activation and environment loading:
```bash
./run_example.sh funding_batch_diagnostics.py
./run_example.sh test_mcp_integration.py
./run_example.sh  # defaults to funding_batch_diagnostics.py
```

---

## Environment Variables

Configure these in `.env`:

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `ALEATORIC_API_KEY` | Your MCP API key | `ak_1234567890abcdef` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_BASE_URL` | API endpoint URL | `https://mcp.aleatoric.systems` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `DEMO_SPEED` | Demo playback speed | `1.0` |
| `OUTPUT_DIR` | Output directory | `./outputs` |
| `HTTP_TIMEOUT` | Request timeout (seconds) | `300` |
| `MAX_CONCURRENCY` | Parallel requests limit | `5` |

---

## Dependency Overview

The examples require these Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| `httpx` | ≥0.25.0 | Async HTTP client for MCP API |
| `matplotlib` | ≥3.8.0 | Plotting and visualization |
| `pandas` | ≥2.0.0 | Data manipulation and analysis |
| `numpy` | ≥1.24.0 | Numerical computing |
| `python-dotenv` | ≥1.0.0 | Load .env files (optional) |

**Total install size:** ~200 MB

---

## Troubleshooting

### "Python 3.9+ not found"

**Solution:**
```bash
# Check your Python version
python3 --version

# If too old, install newer version:
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11
```

### "Permission denied: ./setup.sh"

**Solution:**
```bash
chmod +x setup.sh
bash setup.sh
```

### "pip install failed"

**Solutions:**

1. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

3. **Install packages individually:**
   ```bash
   pip install httpx
   pip install matplotlib
   pip install pandas
   pip install numpy
   ```

### "ModuleNotFoundError" when running examples

**Solution:**
Make sure virtual environment is activated:
```bash
source activate.sh
```

### "ALEATORIC_API_KEY not set"

**Solutions:**

1. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

2. **Edit .env:**
   ```bash
   nano .env
   # Add: ALEATORIC_API_KEY=your-actual-key
   ```

3. **Manual export (temporary):**
   ```bash
   export ALEATORIC_API_KEY="your-key-here"
   ```

### "HTTPError 401 Unauthorized"

**Causes:**
- Invalid API key
- Expired API key
- API key not set

**Solution:**
1. Verify your API key is correct in `.env`
2. Check key hasn't expired at https://aleatoric.systems
3. Generate a new key if needed

### "HTTPError 429 Too Many Requests"

**Cause:** Rate limit exceeded

**Solution:** Wait a few minutes before retrying

### matplotlib plots don't display

**macOS:**
```bash
# Install backend
pip install PyQt5
```

**Linux:**
```bash
# Install Tkinter
sudo apt-get install python3-tk
```

**Or use non-interactive backend:**
```python
import matplotlib
matplotlib.use('Agg')  # PNG backend
```

### Virtual environment activation doesn't work

**Unix/Linux/macOS:**
```bash
# Ensure you're using 'source'
source venv/bin/activate

# Not just:
# venv/bin/activate  # This won't work!
```

**Windows PowerShell:**
```powershell
# You may need to enable scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

---

## Uninstalling / Cleaning Up

To remove the environment:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv/

# Remove environment file (careful!)
rm .env

# Remove generated outputs
rm -rf outputs/

# Remove Python cache
rm -rf __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## Advanced Setup Options

### Using conda Instead of venv

```bash
# Create conda environment
conda create -n aleatoric-mcp python=3.11

# Activate
conda activate aleatoric-mcp

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env
```

### Using pipenv

```bash
# Install pipenv
pip install pipenv

# Create environment and install dependencies
pipenv install httpx matplotlib pandas numpy python-dotenv

# Activate
pipenv shell

# Configure
cp .env.example .env
nano .env
```

### Using poetry

```bash
# Initialize poetry project
poetry init

# Add dependencies
poetry add httpx matplotlib pandas numpy python-dotenv

# Install
poetry install

# Activate
poetry shell

# Configure
cp .env.example .env
nano .env
```

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "funding_batch_diagnostics.py"]
```

```bash
# Build
docker build -t aleatoric-mcp-examples .

# Run (pass API key)
docker run -e ALEATORIC_API_KEY=your-key aleatoric-mcp-examples
```

---

## Development Setup

For contributing or development:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
flake8 .
black .
mypy .
```

---

## CI/CD Setup

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test Examples

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd examples
          bash setup.sh
          python test_funding_setup.py
      env:
        ALEATORIC_API_KEY: ${{ secrets.ALEATORIC_API_KEY }}
```

---

## Getting Help

### Issues?

1. **Check this guide** - Most issues are covered above
2. **Run diagnostics:**
   ```bash
   python test_funding_setup.py
   ```
3. **Check logs:**
   ```bash
   tail -f outputs/*/logs/*.log
   ```
4. **Open GitHub issue** with:
   - Operating system
   - Python version
   - Error message
   - Steps to reproduce

### Resources

- **Documentation:** See all .md files in examples/
- **Quick Start:** QUICKSTART_FUNDING.md
- **Architecture:** ARCHITECTURE.md
- **Video Demo:** VIDEO_DEMO_GUIDE.md

---

## Next Steps

After successful setup:

1. **Run validation:**
   ```bash
   python test_funding_setup.py
   python test_mcp_integration.py
   ```

2. **Try the main example:**
   ```bash
   python funding_batch_diagnostics.py
   ```

3. **Create a demo:**
   ```bash
   bash demo_script.sh
   ```

4. **Read the documentation:**
   ```bash
   cat QUICKSTART_FUNDING.md
   ```

Happy analyzing! 🚀
