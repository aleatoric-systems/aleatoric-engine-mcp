#!/bin/bash
#
# Funding Batch Diagnostics - Screenshot Demo
#
# This script runs the demo and captures screenshots at each step.
# Screenshots can be used to create a slideshow, animated GIF, or video.
#
# Usage:
#   bash demo_with_screenshots.sh
#
# Requirements:
#   - macOS: screencapture (built-in)
#   - Linux: scrot or imagemagick
#

set -e

# Configuration
SCREENSHOT_DIR="outputs/demo_screenshots"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="$SCREENSHOT_DIR/$TIMESTAMP"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Screenshot Demo - Funding Batch Diagnostics"
echo "============================================="
echo ""
echo "Screenshots will be saved to: $OUTPUT_DIR"
echo ""

# Function to capture screenshot
capture_screenshot() {
    local filename="$1"
    local description="$2"

    echo "📸 Capturing: $description"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        screencapture -x "$OUTPUT_DIR/$filename.png"
    elif command -v scrot &> /dev/null; then
        # Linux with scrot
        scrot "$OUTPUT_DIR/$filename.png"
    elif command -v import &> /dev/null; then
        # Linux with ImageMagick
        import -window root "$OUTPUT_DIR/$filename.png"
    else
        echo "⚠️  Screenshot tool not found. Skipping."
        return
    fi

    sleep 1
}

# Function to capture terminal only (macOS)
capture_terminal() {
    local filename="$1"
    local description="$2"

    echo "📸 Capturing terminal: $description"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Get Terminal window ID
        local window_id=$(osascript -e 'tell application "Terminal" to id of front window')
        screencapture -l"$window_id" "$OUTPUT_DIR/$filename.png"
    else
        # Fallback to full screen
        capture_screenshot "$filename" "$description"
    fi

    sleep 1
}

# ============================================================================
# Demo Start
# ============================================================================

clear
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                       ║"
echo "║          FUNDING BATCH DIAGNOSTICS - SCREENSHOT DEMO                  ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
sleep 2

capture_screenshot "01_title" "Title screen"

# ============================================================================
# Step 1: Setup Check
# ============================================================================

clear
echo "Step 1: Setup Verification"
echo "==========================="
echo ""
python test_funding_setup.py
sleep 2

capture_terminal "02_setup_check" "Setup verification complete"

# ============================================================================
# Step 2: Integration Test
# ============================================================================

clear
echo "Step 2: MCP Integration Test"
echo "============================="
echo ""
echo "Testing API connectivity and building test dataset..."
echo ""
sleep 2

capture_terminal "03_integration_start" "Starting integration test"

python test_mcp_integration.py > "$OUTPUT_DIR/integration_test.log" 2>&1 || true

# Show last 20 lines of output
tail -20 "$OUTPUT_DIR/integration_test.log"
sleep 2

capture_terminal "04_integration_complete" "Integration test complete"

# ============================================================================
# Step 3: Main Analysis
# ============================================================================

clear
echo "Step 3: Running Main Analysis (5 days)"
echo "======================================="
echo ""
echo "This will generate:"
echo "  • 5 days of synthetic market data"
echo "  • Funding simulations across 3 exchanges"
echo "  • Diagnostic plots and analytics"
echo ""
sleep 3

capture_terminal "05_analysis_start" "Starting main analysis"

# Run the main example
python funding_batch_diagnostics.py \
    --output-dir outputs/demo_analysis \
    > "$OUTPUT_DIR/main_analysis.log" 2>&1

# Show progress
echo ""
echo "Analysis complete!"
sleep 2

capture_terminal "06_analysis_complete" "Main analysis complete"

# ============================================================================
# Step 4: View Results
# ============================================================================

clear
echo "Step 4: Generated Files"
echo "======================="
echo ""
ls -lh outputs/demo_analysis/
echo ""
sleep 3

capture_terminal "07_file_list" "Generated files"

# ============================================================================
# Step 5: Text Report
# ============================================================================

clear
echo "Step 5: Analytics Report"
echo "========================"
echo ""
cat outputs/demo_analysis/report_BTCUSDT.txt
echo ""
sleep 5

capture_terminal "08_text_report" "Analytics report"

# ============================================================================
# Step 6: JSON Preview
# ============================================================================

clear
echo "Step 6: JSON Analytics Preview"
echo "==============================="
echo ""
head -40 outputs/demo_analysis/analytics_BTCUSDT.json
echo ""
sleep 3

capture_terminal "09_json_preview" "JSON analytics preview"

# ============================================================================
# Step 7: Parquet Inspection
# ============================================================================

clear
echo "Step 7: Market Data Inspection"
echo "==============================="
echo ""

python << 'PYEOF'
import pandas as pd
df = pd.read_parquet('outputs/demo_analysis/market_data_BTCUSDT_5d.parquet')
print("Dataset Info:")
print("=" * 60)
df.info()
print("\nFirst 10 rows:")
print("=" * 60)
print(df.head(10))
print(f"\nTotal events: {len(df):,}")
PYEOF

sleep 5

capture_terminal "10_parquet_inspection" "Parquet data inspection"

# ============================================================================
# Step 8: Open Visualization
# ============================================================================

clear
echo "Step 8: Diagnostic Visualization"
echo "================================="
echo ""
echo "Opening the diagnostic plot..."
echo ""
sleep 2

capture_terminal "11_before_plot" "Before opening plot"

# Open the plot
if [[ "$OSTYPE" == "darwin"* ]]; then
    open outputs/demo_analysis/funding_diagnostics_BTCUSDT.png
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open outputs/demo_analysis/funding_diagnostics_BTCUSDT.png &
fi

echo "Plot opened! Take a moment to review the 5-panel visualization."
echo ""
sleep 5

capture_screenshot "12_plot_displayed" "Diagnostic plot displayed"

# Copy the plot to screenshots directory
cp outputs/demo_analysis/funding_diagnostics_BTCUSDT.png \
   "$OUTPUT_DIR/13_diagnostic_plot.png"

# ============================================================================
# Step 9: Summary
# ============================================================================

clear
cat << 'EOF'
Step 9: Demo Complete!
======================

What we demonstrated:
  ✓ Environment validation
  ✓ MCP API integration
  ✓ 5-day market data generation
  ✓ Multi-exchange funding simulation
  ✓ Comprehensive analytics
  ✓ Professional visualizations

Output files:
  • market_data_BTCUSDT_5d.parquet  - Raw market data
  • analytics_BTCUSDT.json          - Machine-readable analytics
  • report_BTCUSDT.txt              - Human-readable report
  • funding_diagnostics_BTCUSDT.png - Diagnostic visualization

Key features:
  • Production-ready async code
  • Deterministic reproducibility
  • Exchange-specific funding models
  • Multiple export formats
  • Comprehensive documentation

Use cases:
  • Quantitative strategy development
  • Exchange funding analysis
  • Risk management
  • Market making research
  • Educational demonstrations

Next steps:
  1. Customize for your symbols/exchanges
  2. Integrate with your infrastructure
  3. Explore the comprehensive documentation
  4. Build on this example for your needs

Thank you for watching! 🚀
EOF

sleep 5

capture_terminal "14_summary" "Demo summary"

# ============================================================================
# Create Index
# ============================================================================

cat > "$OUTPUT_DIR/README.md" << EOF
# Funding Batch Diagnostics - Screenshot Demo

Demo captured on: $(date)

## Screenshots

1. \`01_title.png\` - Title screen
2. \`02_setup_check.png\` - Setup verification
3. \`03_integration_start.png\` - Starting MCP integration test
4. \`04_integration_complete.png\` - Integration test complete
5. \`05_analysis_start.png\` - Starting main analysis
6. \`06_analysis_complete.png\` - Main analysis complete
7. \`07_file_list.png\` - Generated files
8. \`08_text_report.png\` - Analytics report
9. \`09_json_preview.png\` - JSON analytics preview
10. \`10_parquet_inspection.png\` - Parquet data inspection
11. \`11_before_plot.png\` - Before opening plot
12. \`12_plot_displayed.png\` - Diagnostic plot displayed
13. \`13_diagnostic_plot.png\` - High-res diagnostic plot
14. \`14_summary.png\` - Demo summary

## Creating Animated GIF

Using ImageMagick:
\`\`\`bash
convert -delay 200 -loop 0 *.png demo.gif
\`\`\`

Using ffmpeg:
\`\`\`bash
ffmpeg -framerate 0.5 -pattern_type glob -i '*.png' \\
       -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \\
       demo.mp4
\`\`\`

## Creating Video

\`\`\`bash
ffmpeg -framerate 1 -pattern_type glob -i '*.png' \\
       -c:v libx264 -pix_fmt yuv420p \\
       -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \\
       demo_video.mp4
\`\`\`

## Logs

- \`integration_test.log\` - Full MCP integration test output
- \`main_analysis.log\` - Full main analysis output
EOF

# ============================================================================
# Finale
# ============================================================================

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                       ║"
echo "║                     SCREENSHOT DEMO COMPLETE! 📸                      ║"
echo "║                                                                       ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Screenshots saved to: $OUTPUT_DIR"
echo ""
echo "You can now:"
echo "  • Create an animated GIF:"
echo "    cd $OUTPUT_DIR"
echo "    convert -delay 200 -loop 0 *.png demo.gif"
echo ""
echo "  • Create a video:"
echo "    ffmpeg -framerate 1 -i '%02d*.png' demo.mp4"
echo ""
echo "  • Create a slideshow in Keynote/PowerPoint"
echo ""
echo "  • Use as documentation images"
echo ""

# Create a simple HTML viewer
cat > "$OUTPUT_DIR/viewer.html" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>Funding Batch Diagnostics - Screenshot Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #1e1e1e;
            color: #fff;
        }
        h1 { color: #4a9eff; }
        .screenshot {
            margin: 20px 0;
            padding: 20px;
            background: #2d2d2d;
            border-radius: 8px;
        }
        img {
            max-width: 100%;
            border: 2px solid #444;
            border-radius: 4px;
        }
        .caption {
            margin-top: 10px;
            color: #aaa;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Funding Batch Diagnostics - Screenshot Demo</h1>

    <div class="screenshot">
        <h2>1. Title Screen</h2>
        <img src="01_title.png" alt="Title">
        <div class="caption">Demo introduction</div>
    </div>

    <div class="screenshot">
        <h2>2. Setup Verification</h2>
        <img src="02_setup_check.png" alt="Setup">
        <div class="caption">Validating environment and dependencies</div>
    </div>

    <div class="screenshot">
        <h2>3. MCP Integration Test - Start</h2>
        <img src="03_integration_start.png" alt="Integration Start">
        <div class="caption">Testing MCP API connectivity</div>
    </div>

    <div class="screenshot">
        <h2>4. MCP Integration Test - Complete</h2>
        <img src="04_integration_complete.png" alt="Integration Complete">
        <div class="caption">Successfully built test dataset via API</div>
    </div>

    <div class="screenshot">
        <h2>5. Main Analysis - Start</h2>
        <img src="05_analysis_start.png" alt="Analysis Start">
        <div class="caption">Beginning 5-day funding analysis</div>
    </div>

    <div class="screenshot">
        <h2>6. Main Analysis - Complete</h2>
        <img src="06_analysis_complete.png" alt="Analysis Complete">
        <div class="caption">Analysis finished successfully</div>
    </div>

    <div class="screenshot">
        <h2>7. Generated Files</h2>
        <img src="07_file_list.png" alt="File List">
        <div class="caption">Four output files created</div>
    </div>

    <div class="screenshot">
        <h2>8. Analytics Report</h2>
        <img src="08_text_report.png" alt="Text Report">
        <div class="caption">Human-readable summary with statistics</div>
    </div>

    <div class="screenshot">
        <h2>9. JSON Analytics</h2>
        <img src="09_json_preview.png" alt="JSON Preview">
        <div class="caption">Machine-readable analytics format</div>
    </div>

    <div class="screenshot">
        <h2>10. Market Data Inspection</h2>
        <img src="10_parquet_inspection.png" alt="Parquet Inspection">
        <div class="caption">Examining the generated market data</div>
    </div>

    <div class="screenshot">
        <h2>13. Diagnostic Visualization</h2>
        <img src="13_diagnostic_plot.png" alt="Diagnostic Plot">
        <div class="caption">5-panel comprehensive analysis visualization</div>
    </div>

    <div class="screenshot">
        <h2>14. Summary</h2>
        <img src="14_summary.png" alt="Summary">
        <div class="caption">Demo recap and next steps</div>
    </div>

    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #444; color: #666;">
        <p>Funding Batch Diagnostics for Aleatoric MCP Protocol</p>
    </footer>
</body>
</html>
HTMLEOF

echo "  • View screenshots in browser:"
echo "    open $OUTPUT_DIR/viewer.html"
echo ""
