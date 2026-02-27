#!/bin/bash
#
# Create Animated GIF from Screenshots
#
# This script creates an animated GIF or video from demo screenshots.
#
# Requirements:
#   - ImageMagick (for GIF): brew install imagemagick
#   - ffmpeg (for video): brew install ffmpeg
#
# Usage:
#   bash create_demo_gif.sh [screenshot_directory]
#

set -e

# Configuration
SCREENSHOT_DIR="${1:-outputs/demo_screenshots}"
OUTPUT_GIF="funding_batch_demo.gif"
OUTPUT_MP4="funding_batch_demo.mp4"
DELAY=200  # Delay between frames in 1/100th of a second (200 = 2 seconds)

echo "Creating Demo Animation"
echo "======================="
echo ""

# Find the most recent screenshot directory
if [ -d "$SCREENSHOT_DIR" ]; then
    # Get the most recent timestamped subdirectory
    LATEST_DIR=$(ls -dt "$SCREENSHOT_DIR"/*/ 2>/dev/null | head -1)

    if [ -z "$LATEST_DIR" ]; then
        echo "No screenshot directories found in $SCREENSHOT_DIR"
        echo "Run demo_with_screenshots.sh first to capture screenshots."
        exit 1
    fi

    SCREENSHOT_DIR="$LATEST_DIR"
    echo "Using screenshots from: $SCREENSHOT_DIR"
else
    echo "Screenshot directory not found: $SCREENSHOT_DIR"
    echo "Run demo_with_screenshots.sh first to capture screenshots."
    exit 1
fi

cd "$SCREENSHOT_DIR"

# Count screenshots
NUM_SCREENSHOTS=$(ls -1 *.png 2>/dev/null | wc -l)
echo "Found $NUM_SCREENSHOTS screenshots"
echo ""

if [ "$NUM_SCREENSHOTS" -eq 0 ]; then
    echo "No PNG files found in $SCREENSHOT_DIR"
    exit 1
fi

# ============================================================================
# Option 1: Create Animated GIF with ImageMagick
# ============================================================================

if command -v convert &> /dev/null; then
    echo "Creating animated GIF with ImageMagick..."

    convert -delay $DELAY -loop 0 \
            -resize 1920x1080 \
            -background black \
            -gravity center \
            -extent 1920x1080 \
            [0-9]*.png \
            "$OUTPUT_GIF"

    GIF_SIZE=$(du -h "$OUTPUT_GIF" | cut -f1)
    echo "✓ Created: $OUTPUT_GIF ($GIF_SIZE)"
    echo ""

    # Optimize GIF
    if command -v gifsicle &> /dev/null; then
        echo "Optimizing GIF with gifsicle..."
        gifsicle -O3 --colors 256 "$OUTPUT_GIF" -o "${OUTPUT_GIF%.gif}_optimized.gif"
        OPTIMIZED_SIZE=$(du -h "${OUTPUT_GIF%.gif}_optimized.gif" | cut -f1)
        echo "✓ Optimized: ${OUTPUT_GIF%.gif}_optimized.gif ($OPTIMIZED_SIZE)"
        echo ""
    else
        echo "Tip: Install gifsicle to optimize GIF size:"
        echo "  brew install gifsicle"
        echo ""
    fi
else
    echo "⚠️  ImageMagick not found. Skipping GIF creation."
    echo "Install with: brew install imagemagick"
    echo ""
fi

# ============================================================================
# Option 2: Create MP4 Video with ffmpeg
# ============================================================================

if command -v ffmpeg &> /dev/null; then
    echo "Creating MP4 video with ffmpeg..."

    # Create a temporary file list
    ls -1 [0-9]*.png | sort -n > filelist.txt

    # Create video with 1 fps (1 second per image)
    ffmpeg -y -loglevel error \
           -framerate 0.5 \
           -pattern_type glob -i '[0-9]*.png' \
           -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
           -c:v libx264 \
           -pix_fmt yuv420p \
           -preset slow \
           -crf 18 \
           "$OUTPUT_MP4"

    MP4_SIZE=$(du -h "$OUTPUT_MP4" | cut -f1)
    echo "✓ Created: $OUTPUT_MP4 ($MP4_SIZE)"
    echo ""

    # Clean up
    rm -f filelist.txt
else
    echo "⚠️  ffmpeg not found. Skipping video creation."
    echo "Install with: brew install ffmpeg"
    echo ""
fi

# ============================================================================
# Option 3: Create WebM (web-optimized)
# ============================================================================

if command -v ffmpeg &> /dev/null; then
    echo "Creating WebM video for web..."

    ffmpeg -y -loglevel error \
           -framerate 0.5 \
           -pattern_type glob -i '[0-9]*.png' \
           -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
           -c:v libvpx-vp9 \
           -b:v 2M \
           "${OUTPUT_MP4%.mp4}.webm"

    WEBM_SIZE=$(du -h "${OUTPUT_MP4%.mp4}.webm" | cut -f1)
    echo "✓ Created: ${OUTPUT_MP4%.mp4}.webm ($WEBM_SIZE)"
    echo ""
fi

# ============================================================================
# Summary
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO ANIMATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Output files in: $SCREENSHOT_DIR"
echo ""

ls -lh *.gif *.mp4 *.webm 2>/dev/null || true

echo ""
echo "Next steps:"
echo ""

if [ -f "$OUTPUT_GIF" ]; then
    echo "  • View GIF:"
    echo "    open $OUTPUT_GIF"
    echo ""
fi

if [ -f "$OUTPUT_MP4" ]; then
    echo "  • View video:"
    echo "    open $OUTPUT_MP4"
    echo ""
fi

echo "  • Upload to YouTube/Vimeo"
echo "  • Embed in README.md"
echo "  • Share on social media"
echo ""

# Create a README for the animations
cat > ANIMATIONS_README.md << 'EOF'
# Demo Animations

This directory contains animated versions of the Funding Batch Diagnostics demo.

## Files

- `funding_batch_demo.gif` - Animated GIF (best for README)
- `funding_batch_demo_optimized.gif` - Optimized GIF (smaller size)
- `funding_batch_demo.mp4` - MP4 video (best quality)
- `funding_batch_demo.webm` - WebM video (web-optimized)

## Usage

### In Markdown/README
```markdown
![Funding Batch Demo](funding_batch_demo.gif)
```

### In HTML
```html
<video controls>
  <source src="funding_batch_demo.mp4" type="video/mp4">
  <source src="funding_batch_demo.webm" type="video/webm">
  Your browser does not support video.
</video>
```

### On YouTube
Upload the MP4 file directly.

### On Twitter/X
GIFs work best (under 15MB limit).

### On LinkedIn
MP4 works well for native video posts.

## Customization

To create your own animations:

1. Adjust frame delay:
   ```bash
   DELAY=300 bash create_demo_gif.sh  # 3 seconds per frame
   ```

2. Change resolution:
   Edit the script to use different scale values.

3. Add fade transitions:
   Modify ffmpeg command to include fade filters.

## Tools Used

- **ImageMagick**: GIF creation and optimization
- **ffmpeg**: Video encoding
- **gifsicle**: GIF optimization
EOF

echo "Created ANIMATIONS_README.md with usage instructions"
echo ""
