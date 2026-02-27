# Video Demo - Complete Guide

This directory contains everything needed to create professional video demonstrations of the Funding Batch Diagnostics example.

## Quick Start

### Option 1: Automated Screen Recording (Recommended)

```bash
# 1. Set API key
export ALEATORIC_API_KEY="your-key-here"

# 2. Start your screen recorder (QuickTime, OBS, etc.)

# 3. Run the demo script
bash demo_script.sh

# 4. Stop recording
```

**Duration**: ~6-7 minutes
**Output**: Full walkthrough with all features

---

### Option 2: Screenshot-Based Demo

```bash
# 1. Set API key
export ALEATORIC_API_KEY="your-key-here"

# 2. Capture screenshots automatically
bash demo_with_screenshots.sh

# 3. Create animated GIF or video
bash create_demo_gif.sh
```

**Duration**: ~3-4 minutes
**Output**: Animated GIF or MP4 video

---

### Option 3: Terminal Recording (asciinema)

```bash
# 1. Install asciinema
brew install asciinema  # macOS
# or: pip install asciinema

# 2. Start recording
asciinema rec funding_demo.cast

# 3. Run demo
bash demo_script.sh

# 4. Stop (Ctrl+D)

# 5. Upload or convert
asciinema upload funding_demo.cast
# or: agg funding_demo.cast funding_demo.gif
```

**Duration**: ~6-7 minutes
**Output**: Terminal recording or GIF

---

## Files Overview

| File | Purpose | Size |
|------|---------|------|
| `demo_script.sh` | Main automated demo with 11 parts | ~15 KB |
| `demo_with_screenshots.sh` | Captures screenshots at each step | ~12 KB |
| `create_demo_gif.sh` | Creates GIF/video from screenshots | ~6 KB |
| `VIDEO_DEMO_GUIDE.md` | Comprehensive recording guide | ~18 KB |
| `VIDEO_DEMO_README.md` | This file - quick reference | ~8 KB |

---

## Demo Script Features

### 11-Part Structure

1. **Setup Verification** (30s)
   - Validates environment
   - Checks dependencies

2. **MCP Integration Test** (30s)
   - Tests API connectivity
   - Builds 60s test dataset

3. **Directory Preparation** (10s)
   - Creates clean output directory

4. **Main Analysis** (90s)
   - Generates 5 days of market data
   - Simulates funding across exchanges
   - Creates diagnostics

5. **Results Overview** (20s)
   - Lists generated files

6. **Text Report** (30s)
   - Shows analytics summary

7. **JSON Analytics** (20s)
   - Displays machine-readable data

8. **Parquet Inspection** (40s)
   - Examines market data structure

9. **Visualization** (30s)
   - Opens diagnostic plot

10. **Customization Demo** (60s)
    - Quick 1-day example

11. **Summary** (30s)
    - Recap and next steps

**Total**: ~6-7 minutes

---

## Recording Tools Comparison

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **asciinema** | Terminal demos | Small files, shareable | Terminal only |
| **QuickTime** | macOS, simple | Built-in, easy | Basic features |
| **OBS Studio** | Professional | Free, powerful | Complex setup |
| **Loom** | Quick sharing | Easy, cloud-hosted | Quality limits |
| **Screenshot script** | Slides/GIFs | Flexible editing | Manual assembly |

---

## Output Formats

### For Different Platforms

**YouTube/Vimeo:**
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Frame rate: 30 fps
- Run: `demo_script.sh` with screen recording

**Twitter/X:**
- Format: GIF or MP4
- Max size: 512 MB (video), 15 MB (GIF)
- Duration: < 2:20
- Run: `demo_with_screenshots.sh` then `create_demo_gif.sh`

**LinkedIn:**
- Format: MP4
- Resolution: 1920x1080
- Duration: < 10 minutes
- Run: `demo_script.sh` with screen recording

**GitHub README:**
- Format: GIF
- Max size: ~10 MB (for fast loading)
- Run: `create_demo_gif.sh` with optimization

**Documentation:**
- Format: Screenshots (PNG)
- Run: `demo_with_screenshots.sh`

---

## Customization

### Adjust Demo Speed

```bash
# Faster (half the pauses)
DEMO_SPEED=0.5 bash demo_script.sh

# Slower (double the pauses)
DEMO_SPEED=2 bash demo_script.sh
```

### Change Parameters

Edit `demo_script.sh` to modify:
- Symbol (default: BTCUSDT)
- Duration (default: 5 days)
- Exchanges (default: binance, hyperliquid, okx)
- Position size (default: 1.0)

### Custom Narration

Record voiceover separately and sync in post-production:
1. Run demo with screen recording (no audio)
2. Record narration following the script
3. Combine in video editor (iMovie, Premiere, etc.)

See suggested narration in `VIDEO_DEMO_GUIDE.md`

---

## Post-Production Tips

### Editing Checklist

- [ ] Trim dead space at start/end
- [ ] Add title screen (0-10s)
- [ ] Add section headers (match 11 parts)
- [ ] Highlight key outputs (arrows, boxes)
- [ ] Add closing call-to-action
- [ ] Include social media handles
- [ ] Add background music (optional, subtle)
- [ ] Color correct if needed
- [ ] Add subtitles/captions (accessibility)

### Recommended Edits

**Essential:**
- Title screen with logo
- Section transitions
- End screen with links

**Nice to have:**
- Voiceover narration
- Text annotations
- Background music
- Zoom effects on key data

**Advanced:**
- Picture-in-picture for plot
- Animated transitions
- Custom graphics/overlays

---

## Common Workflows

### Workflow 1: Quick Demo (30 min total)

```bash
# 1. Record (5 min)
asciinema rec demo.cast
bash demo_script.sh
exit

# 2. Convert to GIF (2 min)
agg demo.cast demo.gif

# 3. Upload to GitHub README (3 min)
```

**Use case**: Quick documentation, internal sharing

---

### Workflow 2: Professional Video (2-3 hours)

```bash
# 1. Record raw footage (10 min)
# Use OBS Studio

# 2. Record voiceover (15 min)

# 3. Edit in DaVinci Resolve (60-90 min)
#    - Trim, add titles, sync audio

# 4. Export and upload (20 min)
#    - YouTube, social media
```

**Use case**: Marketing, presentations, tutorials

---

### Workflow 3: Screenshot Slideshow (1 hour)

```bash
# 1. Capture screenshots (5 min)
bash demo_with_screenshots.sh

# 2. Import to Keynote/PowerPoint (20 min)

# 3. Add animations and notes (30 min)

# 4. Export to PDF or video (5 min)
```

**Use case**: Conference presentations, documentation

---

## Troubleshooting

### Demo Runs Too Fast
```bash
DEMO_SPEED=2 bash demo_script.sh
```

### API Timeouts
- Check internet connection
- Verify API key is valid
- Try shorter duration first (1 day)

### Screenshots Not Captured
- Verify screencapture/scrot is installed
- Grant screen recording permissions (macOS)
- Run manually: `screencapture test.png`

### Plot Doesn't Open
- Check if file was created:
  ```bash
  ls -lh outputs/*/funding_diagnostics_*.png
  ```
- Open manually:
  ```bash
  open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png
  ```

### GIF Too Large
```bash
# Install gifsicle
brew install gifsicle

# Optimize
gifsicle -O3 --colors 128 input.gif -o output.gif

# Or reduce frame rate
DELAY=400 bash create_demo_gif.sh  # 4s per frame instead of 2s
```

---

## Example Video Descriptions

### YouTube

**Title:**
"Funding Batch Diagnostics - Aleatoric MCP Protocol Demo"

**Description:**
```
Complete walkthrough of the Funding Batch Diagnostics example for the
Aleatoric MCP protocol.

This example demonstrates:
• 5-day synthetic market data generation
• Multi-exchange funding rate simulation (Binance, Hyperliquid, OKX)
• Comprehensive analytics and statistics
• Professional diagnostic visualizations
• Production-ready Python code

⏱️ Timestamps:
0:00 Introduction
0:10 Setup verification
0:40 MCP integration test
1:10 Main analysis (5-day generation)
3:00 Results overview
3:30 Analytics report
4:00 JSON data format
4:30 Market data inspection
5:00 Diagnostic visualization
5:40 Customization example
6:10 Summary & next steps

🔗 Links:
Repository: [URL]
Documentation: [URL]
Quick Start: [URL]
API Docs: [URL]

#quantfinance #trading #python #marketdata #mcp #aleatoric
```

---

### Twitter/X

**Post:**
```
🚀 New: Funding Batch Diagnostics for Aleatoric MCP

Generate 5 days of institutional-grade synthetic market data
→ Simulate funding across multiple exchanges
→ Get comprehensive analytics & visualizations
→ All in ~60 seconds

[GIF/Video]

Try it: [repo link]
```

---

### LinkedIn

**Post:**
```
Excited to share our new Funding Batch Diagnostics example for the
Aleatoric MCP protocol!

This production-ready tool demonstrates:
✓ Synthetic market data generation (5 days in ~60s)
✓ Multi-exchange funding simulation
✓ Comprehensive analytics with professional visualizations
✓ Export to Parquet, JSON, and publication-ready plots

Perfect for:
• Quantitative strategy development
• Exchange analysis & comparison
• Risk management & PnL modeling
• Market making research

Built with async Python, type hints, and comprehensive documentation.
Full example + test suite included.

Check it out: [link]

#QuantitativeFinance #Trading #Python #FinTech #MarketData
```

---

## Next Steps

After creating your video:

1. **Upload & Share**
   - YouTube (main repository)
   - Vimeo (high quality backup)
   - Twitter (short clips)
   - LinkedIn (professional audience)

2. **Embed in Documentation**
   - Add to README.md
   - Include in QUICKSTART
   - Link from docs site

3. **Create Variations**
   - 30-second teaser
   - 2-minute highlights
   - Full 7-minute walkthrough

4. **Gather Feedback**
   - Share with team
   - Post in communities
   - Iterate based on feedback

---

## Resources

**Tools:**
- asciinema: https://asciinema.org/
- OBS Studio: https://obsproject.com/
- DaVinci Resolve: https://www.blackmagicdesign.com/products/davinciresolve
- ImageMagick: https://imagemagick.org/
- ffmpeg: https://ffmpeg.org/

**Learning:**
- OBS tutorials: YouTube → "OBS Studio tutorial"
- Video editing: YouTube → "DaVinci Resolve beginner"
- Screen recording tips: YouTube → "Screen recording best practices"

**Assets:**
- Free music: YouTube Audio Library, Incompetech
- Icons: Font Awesome, Material Icons
- Stock footage: Pexels, Unsplash

---

## Support

Questions or issues:
- GitHub Issues: [repo link]
- Documentation: `VIDEO_DEMO_GUIDE.md`
- Examples: Check other demo scripts in this directory

Happy recording! 🎬
