# Installation - Quick Reference

Choose your installation method:

## 🚀 Automated Setup (Recommended)

### Unix/macOS/Linux
```bash
bash setup.sh
```

### Windows
```powershell
.\setup.ps1
```

### Using Make
```bash
make setup
```

**That's it!** The script will:
- ✓ Check Python version (3.9+ required)
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Create configuration files
- ✓ Verify installation

---

## ⚡ Quick Start (3 Steps)

```bash
# 1. Setup
bash setup.sh

# 2. Configure (add your API key)
nano .env

# 3. Test
source activate.sh
python test_funding_setup.py
```

---

## 📋 Requirements

- **Python:** 3.9 or higher
- **pip:** Latest version (auto-upgraded during setup)
- **Internet:** Required for API access
- **API Key:** Get yours at https://aleatoric.systems

---

## 📦 What Gets Installed

| Package | Size | Purpose |
|---------|------|---------|
| httpx | ~5 MB | HTTP client for MCP API |
| matplotlib | ~50 MB | Plotting and visualization |
| pandas | ~100 MB | Data manipulation |
| numpy | ~30 MB | Numerical computing |
| python-dotenv | ~50 KB | Environment variables |

**Total:** ~200 MB

---

## 🔧 Manual Installation

If automated setup doesn't work:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Create config
cp .env.example .env
nano .env  # Add your API key
```

---

## ✅ Verify Installation

```bash
# Activate environment
source activate.sh

# Run validation (no API calls)
python test_funding_setup.py

# Run API integration test (requires API key)
python test_mcp_integration.py
```

**Expected output:**
```
✅ All checks passed! You're ready to run the example.
```

---

## 🎯 Next Steps

After successful installation:

**1. Run the main example:**
```bash
python funding_batch_diagnostics.py
```

**2. Create a video demo:**
```bash
bash demo_script.sh
```

**3. Read the docs:**
- **Quick Start:** `QUICKSTART_FUNDING.md`
- **Full Setup Guide:** `SETUP_GUIDE.md`
- **Architecture:** `ARCHITECTURE.md`

---

## 🆘 Troubleshooting

### Python version too old
```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt install python3.11

# Windows
# Download from python.org
```

### Permission denied
```bash
chmod +x setup.sh activate.sh
bash setup.sh
```

### Pip install fails
```bash
python -m pip install --upgrade pip
pip cache purge
pip install -r requirements.txt
```

### API key issues
```bash
# Check .env exists
cat .env

# Edit and add key
nano .env

# Or export directly
export ALEATORIC_API_KEY="your-key-here"
```

### More help
See detailed troubleshooting in `SETUP_GUIDE.md`

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `INSTALL.md` | This file - quick installation reference |
| `SETUP_GUIDE.md` | Comprehensive setup guide with troubleshooting |
| `QUICKSTART_FUNDING.md` | 5-minute guide to first example |
| `README.md` | Overview and example listing |

---

## 🎓 Learning Path

```
1. INSTALL.md (you are here)
   └─ Get environment set up

2. QUICKSTART_FUNDING.md
   └─ Run your first example (5 min)

3. funding_batch_diagnostics.md
   └─ Understand the main example

4. ARCHITECTURE.md
   └─ Deep dive into technical details

5. VIDEO_DEMO_GUIDE.md
   └─ Create professional demos
```

---

## 💡 Tips

**Use Make for convenience:**
```bash
make setup      # One-command setup
make test       # Run all tests
make example    # Run main example
make clean      # Clean up outputs
make help       # Show all commands
```

**Activate quickly:**
```bash
source activate.sh  # Auto-loads .env
```

**Run examples easily:**
```bash
./run_example.sh funding_batch_diagnostics.py
```

---

## 🔗 Resources

- **Get API Key:** https://aleatoric.systems
- **Full Documentation:** All .md files in this directory
- **GitHub Issues:** Report problems or get help
- **Examples:** See all Python files in this directory

---

## ✨ Installation Complete?

Run this to verify:
```bash
make test
# or
python test_funding_setup.py
python test_mcp_integration.py
```

If all tests pass, you're ready! 🎉

Start with:
```bash
python funding_batch_diagnostics.py
```
