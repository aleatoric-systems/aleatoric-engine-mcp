# Video Demo Creation Guide

Complete guide for creating a professional video demonstration of the Funding Batch Diagnostics example.

## Quick Start

```bash
# 1. Set your API key
export ALEATORIC_API_KEY="your-key-here"

# 2. Start recording (see options below)

# 3. Run the demo script
bash demo_script.sh

# 4. Stop recording
```

## Recording Options

### Option 1: Terminal Recording (Recommended for CLI demos)

#### Using asciinema (Best for terminal-only)

**Install:**
```bash
# macOS
brew install asciinema

# Ubuntu/Debian
sudo apt-get install asciinema

# Python (any OS)
pip install asciinema
```

**Record:**
```bash
# Start recording
asciinema rec funding_demo.cast

# Run the demo
bash demo_script.sh

# Stop recording (Ctrl+D or exit)
exit

# Play back
asciinema play funding_demo.cast

# Upload to asciinema.org (shareable link)
asciinema upload funding_demo.cast

# Convert to GIF (requires agg)
# Install: cargo install --git https://github.com/asciinema/agg
agg funding_demo.cast funding_demo.gif
```

**Pros:**
- Perfect for terminal-based demos
- Small file size
- Easy to share (asciinema.org links)
- Can convert to GIF or SVG

**Cons:**
- Terminal only (won't capture the plot opening)

---

#### Using termtosvg (Terminal to SVG animation)

**Install:**
```bash
pip install termtosvg
```

**Record:**
```bash
# Record and generate SVG
termtosvg funding_demo.svg

# Run the demo
bash demo_script.sh

# Stop recording (Ctrl+D)
exit
```

**Pros:**
- Creates embeddable SVG animation
- Works in web browsers
- Scalable vector graphics

**Cons:**
- Terminal only
- Limited editing options

---

### Option 2: Screen Recording (Best for full demo with plot)

#### macOS - QuickTime Player

**Record:**
1. Open QuickTime Player
2. File → New Screen Recording
3. Click record button
4. Select area (full screen or window)
5. Run demo: `bash demo_script.sh`
6. Stop recording: Click stop button in menu bar
7. File → Export → 1080p

**Settings:**
- Resolution: 1920x1080 or higher
- Frame rate: 30 fps
- Audio: Enable microphone if narrating

---

#### macOS - Screenshot.app (Built-in)

**Record:**
```bash
# Open Screenshot tool
cmd + shift + 5

# Or record via command line
screencapture -v funding_demo.mov

# Run demo in terminal
bash demo_script.sh
```

---

#### Windows - Xbox Game Bar

**Record:**
1. Press `Win + G` to open Game Bar
2. Click record button (or `Win + Alt + R`)
3. Run demo: `bash demo_script.sh` (in Git Bash or WSL)
4. Stop recording: `Win + Alt + R`
5. Videos saved to: `C:\Users\[Username]\Videos\Captures`

---

#### Linux - SimpleScreenRecorder

**Install:**
```bash
sudo apt-get install simplescreenrecorder
```

**Record:**
1. Open SimpleScreenRecorder
2. Select "Record a fixed rectangle" or "Entire screen"
3. Set frame rate to 30 fps
4. Click "Continue" → "Start Recording"
5. Run demo: `bash demo_script.sh`
6. Click "Stop Recording"

---

#### Cross-Platform - OBS Studio (Professional)

**Install:**
- Download from: https://obsproject.com/

**Setup:**
1. Open OBS Studio
2. Add Source → Window Capture (select terminal window)
3. Settings → Output → Recording Quality: "High Quality"
4. Settings → Video → Base Resolution: 1920x1080

**Record:**
1. Click "Start Recording"
2. Switch to terminal and run: `bash demo_script.sh`
3. Switch back to OBS and click "Stop Recording"
4. File saved to default output folder

**Advanced OBS Setup:**
```
Scene Setup:
├─ Terminal Window (fullscreen or windowed)
├─ Webcam (optional, corner overlay)
└─ Audio Input (microphone for narration)

Output Settings:
├─ Format: MP4
├─ Encoder: x264
├─ Rate Control: CBR
├─ Bitrate: 2500 Kbps
└─ Preset: Quality
```

---

### Option 3: Automated Demo with Screenshots

```bash
# Create a script that captures screenshots at each step
bash demo_with_screenshots.sh
```

See `demo_with_screenshots.sh` (created below) for automated screenshot capture.

---

## Demo Script Features

The `demo_script.sh` includes:

### 11 Parts:
1. **Setup Verification** - Validates environment
2. **MCP Integration Test** - Tests API with real data
3. **Directory Preparation** - Creates clean output
4. **Main Analysis** - 5-day funding batch
5. **Results Overview** - Lists generated files
6. **Text Report** - Shows analytics report
7. **JSON Analytics** - Displays machine-readable data
8. **Parquet Inspection** - Examines market data
9. **Visualization** - Opens diagnostic plot
10. **Customization Demo** - Quick 1-day example
11. **Summary** - Recap and next steps

### Visual Features:
- Color-coded output (headers, steps, commands)
- Progress indicators
- Timed pauses for readability
- ASCII art title screens
- Structured sections

### Customization:
```bash
# Speed up the demo (2x faster)
DEMO_SPEED=0.5 bash demo_script.sh

# Slow down the demo (2x slower)
DEMO_SPEED=2 bash demo_script.sh
```

---

## Recording Best Practices

### Terminal Setup

**Font & Size:**
```bash
# Recommended terminal settings:
Font: Monaco, Menlo, or JetBrains Mono
Size: 14-16pt (readable in video)
Theme: Dark background with high contrast
```

**Window Size:**
```bash
# Set terminal to standard HD size
# macOS Terminal: Preferences → Profiles → Window
Columns: 120
Rows: 30

# Or use resize command
resize -s 30 120
```

**Clean Terminal:**
```bash
# Clear history and prompt before recording
clear
export PS1="\[\033[01;32m\]\u@demo\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "
```

---

### Video Settings

**Resolution:**
- Minimum: 1280x720 (720p)
- Recommended: 1920x1080 (1080p)
- Professional: 2560x1440 (1440p)

**Frame Rate:**
- Standard: 30 fps
- Smooth: 60 fps (for scrolling/animations)

**Bitrate:**
- Good: 2500 Kbps
- Better: 5000 Kbps
- Best: 10000 Kbps

**Format:**
- MP4 (H.264) - Best compatibility
- WebM - Web-optimized
- MOV - macOS native

---

## Post-Production

### Editing Tools

**Free:**
- **iMovie** (macOS) - Simple, built-in
- **DaVinci Resolve** (All platforms) - Professional
- **Shotcut** (All platforms) - Open source
- **OpenShot** (All platforms) - Easy to use

**Paid:**
- **Final Cut Pro** (macOS) - Professional
- **Adobe Premiere** (All platforms) - Industry standard
- **Camtasia** (All platforms) - Screencast-focused

### Editing Steps:

1. **Trim**: Remove setup/cleanup portions
2. **Add Titles**:
   - Opening title: "Funding Batch Diagnostics Demo"
   - Section headers: Match the 11 parts
   - Closing: Call to action

3. **Add Annotations**:
   - Highlight important output
   - Arrow pointers to key metrics
   - Text overlays for explanations

4. **Add Music** (optional):
   - Subtle background music
   - Lower volume during narration
   - Fade in/out

5. **Add Voiceover** (optional):
   - Narrate each section
   - Explain what's happening
   - Point out key insights

### Example Timeline:
```
0:00 - 0:10   Opening title + logo
0:10 - 0:30   Part 1: Setup verification
0:30 - 1:00   Part 2: MCP integration test
1:00 - 1:10   Part 3: Directory prep
1:10 - 3:00   Part 4: Main analysis (key section)
3:00 - 3:30   Part 5: Results overview
3:30 - 4:00   Part 6: Text report
4:00 - 4:20   Part 7: JSON analytics
4:20 - 5:00   Part 8: Parquet inspection
5:00 - 5:30   Part 9: Visualization reveal
5:30 - 6:00   Part 10: Customization demo
6:00 - 6:30   Part 11: Summary
6:30 - 6:40   Closing + CTA
```

---

## Narration Script (Optional)

### Opening (0:00-0:10)
"Welcome to the Funding Batch Diagnostics demonstration for the Aleatoric MCP protocol. This example shows how to generate institutional-grade synthetic market data and analyze funding rates across multiple exchanges."

### Part 4 - Main Analysis (1:10-3:00)
"Here's where the magic happens. We're generating 5 full days of synthetic market data—that's 432,000 seconds of realistic orderbook updates and trades.

The MCP API creates this data with proper market microstructure, realistic spreads, and exchange-specific characteristics.

Next, we simulate funding rates across three major exchanges: Binance, Hyperliquid, and OKX. Each exchange has its own funding mechanism, and our tool accurately models those differences.

Finally, we calculate comprehensive statistics and create professional visualizations—all in about 60 seconds."

### Part 9 - Visualization (5:00-5:30)
"The diagnostic plot gives us a complete picture. The top panel shows funding rates over time for all exchanges. Notice how they differ based on each venue's specific mechanism.

Below that, we see cumulative PnL—this tells us how funding costs accumulate over the 5-day period.

The box plots show the distribution of rates, and the bar charts compare average rates and total PnL across exchanges.

This visualization is publication-ready at 150 DPI."

### Closing (6:30-6:40)
"That's the Funding Batch Diagnostics example. All code and documentation are available in the repository. Give it a try with your own parameters, and see what insights you can uncover!"

---

## Distribution

### Where to Upload:

**Video Platforms:**
- **YouTube** - Best for general audience
- **Vimeo** - Professional, higher quality
- **Loom** - Quick sharing, no editing needed

**Developer Platforms:**
- **GitHub** - Add to repository README
- **asciinema.org** - For terminal recordings

**Social Media:**
- **Twitter/X** - Short clips (< 2 min)
- **LinkedIn** - Professional audience
- **Reddit** - r/algotrading, r/python

### YouTube Upload Settings:

```
Title: "Funding Batch Diagnostics - Aleatoric MCP Demo"

Description:
Demonstration of the Funding Batch Diagnostics example for the
Aleatoric MCP protocol. This example shows:
• 5-day synthetic market data generation
• Multi-exchange funding rate simulation
• Comprehensive analytics and visualizations
• Production-ready code and documentation

Repository: [link]
Documentation: [link]
Try it yourself: [quick start link]

Timestamps:
0:00 Introduction
0:10 Setup verification
0:30 MCP integration test
1:10 Main analysis
3:00 Results overview
5:00 Visualization
6:00 Summary

Tags: quantitative finance, trading, market data, python,
      synthetic data, funding rates, cryptocurrency, mcp

Category: Science & Technology
```

---

## Quick Demo (30 seconds)

For a shorter version:

```bash
# Create abbreviated demo
cat > quick_demo.sh << 'EOF'
#!/bin/bash
clear
echo "Funding Batch Diagnostics - Quick Demo"
echo "========================================"
echo ""
echo "Generating 5 days of market data..."
python funding_batch_diagnostics.py --output-dir outputs/quick_demo
echo ""
echo "Results:"
ls -lh outputs/quick_demo/
echo ""
echo "Opening visualization..."
open outputs/quick_demo/funding_diagnostics_BTCUSDT.png
EOF

chmod +x quick_demo.sh
bash quick_demo.sh
```

---

## Troubleshooting

### "bc: command not found"
```bash
# Install bc for demo script math
# macOS
brew install bc

# Ubuntu/Debian
sudo apt-get install bc
```

### Plot doesn't open automatically
```bash
# Manually open after demo
open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png

# Or view in browser
python -m http.server 8000
# Then visit: http://localhost:8000/outputs/funding_analysis_demo/
```

### Demo runs too fast/slow
```bash
# Adjust speed
DEMO_SPEED=2 bash demo_script.sh  # Slower (2x pauses)
DEMO_SPEED=0.5 bash demo_script.sh  # Faster (0.5x pauses)
```

---

## Additional Resources

**Created Files:**
- `demo_script.sh` - Main demo automation
- `demo_with_screenshots.sh` - Screenshot capture version
- `quick_demo.sh` - 30-second abbreviated version

**Documentation:**
- `QUICKSTART_FUNDING.md` - Getting started
- `funding_batch_diagnostics.md` - Full documentation
- `ARCHITECTURE.md` - Technical details

**Examples:**
- See `examples/` directory for more sample code
- Check repository for video demos (if uploaded)

---

## Contact & Support

- **Issues**: GitHub Issues
- **Questions**: GitHub Discussions
- **Updates**: Star the repository for notifications

Happy recording! 🎥
