# PowerShell Setup Script for Aleatoric MCP Examples
#
# This script creates a Python virtual environment and installs all
# dependencies needed to run the examples on Windows.
#
# Usage:
#   .\setup.ps1
#

# Ensure script stops on errors
$ErrorActionPreference = "Stop"

# Configuration
$VenvDir = "venv"
$PythonMinVersion = [version]"3.9.0"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║                                                                           ║" -ForegroundColor Blue
Write-Host "║              ALEATORIC MCP EXAMPLES - ENVIRONMENT SETUP                   ║" -ForegroundColor Blue
Write-Host "║                          (Windows)                                        ║" -ForegroundColor Blue
Write-Host "║                                                                           ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Function to print section headers
function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host $Text -ForegroundColor Cyan
    Write-Host ("━" * 75) -ForegroundColor Blue
}

# Function to print success messages
function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor Green
}

# Function to print error messages
function Write-ErrorMsg {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor Red
}

# Function to print warnings
function Write-Warning {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor Yellow
}

# ============================================================================
# Step 1: Check Python Installation
# ============================================================================

Write-Header "Step 1: Checking Python Installation"

$PythonCmd = $null

# Try to find Python
$PythonCommands = @("python", "python3", "py")

foreach ($cmd in $PythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python (\d+\.\d+\.\d+)") {
            $versionNumber = [version]$Matches[1]
            if ($versionNumber -ge $PythonMinVersion) {
                $PythonCmd = $cmd
                Write-Success "Found $cmd (version $($Matches[1]))"
                break
            }
        }
    }
    catch {
        continue
    }
}

if (-not $PythonCmd) {
    Write-ErrorMsg "Python 3.9+ not found"
    Write-Host ""
    Write-Host "Please install Python 3.9 or higher:"
    Write-Host "  Download from: https://www.python.org/downloads/"
    Write-Host "  Make sure to check 'Add Python to PATH' during installation"
    Write-Host ""
    exit 1
}

Write-Host ""

# ============================================================================
# Step 2: Create Virtual Environment
# ============================================================================

Write-Header "Step 2: Creating Virtual Environment"

if (Test-Path $VenvDir) {
    Write-Warning "Virtual environment already exists at .\$VenvDir"
    $response = Read-Host "Do you want to recreate it? (y/N)"

    if ($response -eq "y" -or $response -eq "Y") {
        Write-Warning "Removing existing virtual environment..."
        Remove-Item -Recurse -Force $VenvDir
    }
    else {
        Write-Warning "Using existing virtual environment"
        & "$VenvDir\Scripts\Activate.ps1"
        $SkipVenvCreation = $true
    }
}

if (-not $SkipVenvCreation) {
    Write-Host "Creating virtual environment in .\$VenvDir..."
    & $PythonCmd -m venv $VenvDir
    Write-Success "Virtual environment created"
    Write-Host ""

    Write-Host "Activating virtual environment..."
    & "$VenvDir\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
    Write-Host ""
}

# ============================================================================
# Step 3: Upgrade pip
# ============================================================================

Write-Header "Step 3: Upgrading pip"

Write-Host "Upgrading pip to latest version..."
& python -m pip install --upgrade pip --quiet
$pipVersion = & pip --version
Write-Success "pip upgraded: $pipVersion"
Write-Host ""

# ============================================================================
# Step 4: Install Dependencies
# ============================================================================

Write-Header "Step 4: Installing Dependencies"

if (-not (Test-Path "requirements.txt")) {
    Write-ErrorMsg "requirements.txt not found"
    exit 1
}

Write-Host "Installing packages from requirements.txt..."
Write-Host ""

& pip install -r requirements.txt

Write-Host ""
Write-Success "All dependencies installed"
Write-Host ""

Write-Host "Installed packages:"
Write-Host ("━" * 75)
& pip list | Select-String "httpx|matplotlib|pandas|numpy|python-dotenv"
Write-Host ""

# ============================================================================
# Step 5: Environment Configuration
# ============================================================================

Write-Header "Step 5: Environment Configuration"

$EnvFile = ".env"
$EnvExample = ".env.example"

if (-not (Test-Path $EnvFile)) {
    if (Test-Path "..\$EnvExample") {
        Write-Host "Creating .env file from template..."
        Copy-Item "..\$EnvExample" $EnvFile
        Write-Success "Created .env file"
        Write-Host ""
        Write-Warning "IMPORTANT: Edit .env and add your ALEATORIC_API_KEY"
        Write-Host ""
        Write-Host "  1. Open .env in your editor"
        Write-Host "  2. Replace 'your-api-key-here' with your actual API key"
        Write-Host "  3. Save the file"
        Write-Host ""
    }
    elseif (Test-Path $EnvExample) {
        Write-Host "Creating .env file from template..."
        Copy-Item $EnvExample $EnvFile
        Write-Success "Created .env file"
        Write-Host ""
    }
    else {
        Write-Host "Creating new .env file..."
        @"
# Aleatoric MCP API Configuration
ALEATORIC_API_KEY=your-api-key-here

# Optional: Override MCP base URL (default: https://mcp.aleatoric.systems)
# MCP_BASE_URL=https://mcp.aleatoric.systems

# Optional: Logging level
# LOG_LEVEL=INFO
"@ | Out-File -FilePath $EnvFile -Encoding utf8
        Write-Success "Created .env file"
        Write-Host ""
        Write-Warning "IMPORTANT: Edit .env and add your ALEATORIC_API_KEY"
        Write-Host ""
    }
}
else {
    Write-Success ".env file already exists"
    Write-Host ""
}

# ============================================================================
# Step 6: Verify Installation
# ============================================================================

Write-Header "Step 6: Verifying Installation"

Write-Host "Running verification tests..."
Write-Host ""

$verifyScript = @"
import sys

packages = {
    'httpx': 'HTTP client',
    'matplotlib': 'Plotting',
    'pandas': 'Data analysis',
    'numpy': 'Numerical computing',
}

print('Checking package imports:')
print('=' * 60)

all_good = True
for package, description in packages.items():
    try:
        __import__(package)
        print(f'✓ {package:15s} - {description}')
    except ImportError as e:
        print(f'✗ {package:15s} - FAILED: {e}')
        all_good = False

print('=' * 60)

if all_good:
    print('\n✓ All packages imported successfully!')
    sys.exit(0)
else:
    print('\n✗ Some packages failed to import')
    sys.exit(1)
"@

$verifyScript | & python -

if ($LASTEXITCODE -eq 0) {
    Write-Success "Package verification passed"
}
else {
    Write-ErrorMsg "Package verification failed"
    exit 1
}

Write-Host ""

# ============================================================================
# Final Summary
# ============================================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                                           ║" -ForegroundColor Green
Write-Host "║                          SETUP COMPLETE! 🎉                               ║" -ForegroundColor Green
Write-Host "║                                                                           ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "Environment Details:" -ForegroundColor White
Write-Host ("━" * 75)
Write-Host "  Python:           $PythonCmd"
Write-Host "  Virtual Env:      .\$VenvDir"
Write-Host "  Configuration:    .\.env"
Write-Host ("━" * 75)
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor White
Write-Host ""
Write-Host "  1. " -NoNewline; Write-Host "Set your API key:" -ForegroundColor Cyan
Write-Host "     Edit .env and replace 'your-api-key-here' with your actual key"
Write-Host "     notepad .env"
Write-Host ""
Write-Host "  2. " -NoNewline; Write-Host "Activate the environment:" -ForegroundColor Cyan
Write-Host "     .\activate.bat"
Write-Host "     # or"
Write-Host "     .\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  3. " -NoNewline; Write-Host "Run validation tests:" -ForegroundColor Cyan
Write-Host "     python test_funding_setup.py"
Write-Host "     python test_mcp_integration.py"
Write-Host ""
Write-Host "  4. " -NoNewline; Write-Host "Try the examples:" -ForegroundColor Cyan
Write-Host "     python funding_batch_diagnostics.py"
Write-Host ""

Write-Host "⚠  Remember to set your ALEATORIC_API_KEY in .env before running examples!" -ForegroundColor Yellow
Write-Host ""
