#!/bin/bash
#
# Funding Batch Diagnostics - Video Demo Script
#
# This script provides a narrated, step-by-step demonstration of the
# funding batch diagnostics example for video recording.
#
# Usage:
#   1. Ensure ALEATORIC_API_KEY is set
#   2. Start screen recording (QuickTime, OBS, asciinema, etc.)
#   3. Run: bash demo_script.sh
#   4. Stop recording when complete
#

set -e  # Exit on error

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Demo configuration
DEMO_SPEED=${DEMO_SPEED:-1}  # Set to 0.5 for slower demo, 2 for faster
PAUSE_SHORT=2
PAUSE_MEDIUM=4
PAUSE_LONG=6

# Function to print section headers
print_header() {
    echo -e "\n${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}$1${NC}"
    echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Function to print step descriptions
print_step() {
    echo -e "${BOLD}${GREEN}▶${NC} ${BOLD}$1${NC}"
    sleep $(echo "$PAUSE_SHORT * $DEMO_SPEED" | bc)
}

# Function to print commands before executing
print_command() {
    echo -e "${YELLOW}$ $1${NC}"
    sleep 1
}

# Function to pause with message
pause_with_message() {
    echo -e "\n${CYAN}$1${NC}"
    sleep $(echo "$2 * $DEMO_SPEED" | bc)
}

# Clear screen and start demo
clear

# Title screen
echo -e "${BOLD}${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              FUNDING BATCH DIAGNOSTICS - LIVE DEMONSTRATION               ║
║                                                                           ║
║                    Aleatoric MCP Protocol Example                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

pause_with_message "Starting demo in 3 seconds..." 3

# ============================================================================
# PART 1: Setup Verification
# ============================================================================

print_header "PART 1: Setup Verification"

print_step "First, let's verify our environment is ready"
print_command "python test_funding_setup.py"
python test_funding_setup.py || {
    echo -e "\n${RED}Setup validation failed. Please fix issues and try again.${NC}"
    exit 1
}

pause_with_message "✓ Environment is ready!" $PAUSE_MEDIUM

# ============================================================================
# PART 2: MCP Integration Test
# ============================================================================

print_header "PART 2: MCP API Integration Test"

print_step "Now let's test the MCP API by generating a small dataset"
pause_with_message "This will make real API calls to build 60 seconds of test data" $PAUSE_SHORT

print_command "python test_mcp_integration.py"
python test_mcp_integration.py || {
    echo -e "\n${RED}MCP integration test failed. Check your API key.${NC}"
    exit 1
}

pause_with_message "✓ MCP API integration verified!" $PAUSE_MEDIUM

# ============================================================================
# PART 3: Directory Setup
# ============================================================================

print_header "PART 3: Prepare Output Directory"

print_step "Let's create a clean output directory for our demo"
print_command "rm -rf outputs/funding_analysis_demo"
rm -rf outputs/funding_analysis_demo

print_command "mkdir -p outputs/funding_analysis_demo"
mkdir -p outputs/funding_analysis_demo

pause_with_message "✓ Output directory ready" $PAUSE_SHORT

# ============================================================================
# PART 4: Run the Main Example
# ============================================================================

print_header "PART 4: Generate 5 Days of Funding Analysis"

print_step "Now for the main event: 5-day funding batch analysis"
echo -e "\nThis will:"
echo -e "  ${GREEN}•${NC} Generate 5 days (432,000 seconds) of synthetic market data"
echo -e "  ${GREEN}•${NC} Simulate funding rates across 3 exchanges (Binance, Hyperliquid, OKX)"
echo -e "  ${GREEN}•${NC} Calculate comprehensive statistics and analytics"
echo -e "  ${GREEN}•${NC} Create professional diagnostic visualizations"
echo -e "  ${GREEN}•${NC} Export results in multiple formats (Parquet, JSON, TXT, PNG)"

pause_with_message "\nStarting in 3 seconds..." 3

print_command "python funding_batch_diagnostics.py --output-dir outputs/funding_analysis_demo"
python funding_batch_diagnostics.py --output-dir outputs/funding_analysis_demo

pause_with_message "✓ Analysis complete!" $PAUSE_MEDIUM

# ============================================================================
# PART 5: Explore the Results
# ============================================================================

print_header "PART 5: Explore the Generated Outputs"

print_step "Let's see what was created"
print_command "ls -lh outputs/funding_analysis_demo/"
ls -lh outputs/funding_analysis_demo/

pause_with_message "\nNotice the 4 output files:" $PAUSE_SHORT

echo -e "  ${CYAN}1.${NC} ${BOLD}market_data_BTCUSDT_5d.parquet${NC}  - Raw market data (Parquet format)"
echo -e "  ${CYAN}2.${NC} ${BOLD}analytics_BTCUSDT.json${NC}         - Machine-readable analytics"
echo -e "  ${CYAN}3.${NC} ${BOLD}report_BTCUSDT.txt${NC}             - Human-readable report"
echo -e "  ${CYAN}4.${NC} ${BOLD}funding_diagnostics_BTCUSDT.png${NC} - Diagnostic visualizations"

pause_with_message "" $PAUSE_MEDIUM

# ============================================================================
# PART 6: View the Text Report
# ============================================================================

print_header "PART 6: View the Analytics Report"

print_step "Let's look at the human-readable report"
print_command "cat outputs/funding_analysis_demo/report_BTCUSDT.txt"
cat outputs/funding_analysis_demo/report_BTCUSDT.txt

pause_with_message "\n✓ Comprehensive statistics for each exchange!" $PAUSE_LONG

# ============================================================================
# PART 7: View JSON Analytics
# ============================================================================

print_header "PART 7: View JSON Analytics (First 30 Lines)"

print_step "The JSON file contains machine-readable analytics"
print_command "head -30 outputs/funding_analysis_demo/analytics_BTCUSDT.json"
head -30 outputs/funding_analysis_demo/analytics_BTCUSDT.json

pause_with_message "\n✓ Perfect for programmatic access!" $PAUSE_MEDIUM

# ============================================================================
# PART 8: Inspect Market Data
# ============================================================================

print_header "PART 8: Inspect the Market Data (Parquet)"

print_step "Let's peek at the raw market data using Python"
print_command "python -c \"import pandas as pd; df = pd.read_parquet('outputs/funding_analysis_demo/market_data_BTCUSDT_5d.parquet'); print(df.info()); print('\\n'); print(df.head())\""

python << 'PYEOF'
import pandas as pd

print("\n📊 Loading Parquet data...\n")
df = pd.read_parquet('outputs/funding_analysis_demo/market_data_BTCUSDT_5d.parquet')

print("Dataset Information:")
print("=" * 60)
df.info()

print("\n\nFirst 10 rows:")
print("=" * 60)
print(df.head(10))

print(f"\n\nDataset contains {len(df):,} events over 5 days")
print("=" * 60)
PYEOF

pause_with_message "\n✓ Rich market microstructure data!" $PAUSE_LONG

# ============================================================================
# PART 9: View the Diagnostic Plot
# ============================================================================

print_header "PART 9: View the Diagnostic Visualization"

print_step "Opening the diagnostic plot..."
pause_with_message "This 5-panel visualization shows:" $PAUSE_SHORT

echo -e "  ${CYAN}Panel 1:${NC} Funding rates over time (all exchanges)"
echo -e "  ${CYAN}Panel 2:${NC} Cumulative PnL comparison"
echo -e "  ${CYAN}Panel 3:${NC} Funding rate distribution (box plots)"
echo -e "  ${CYAN}Panel 4:${NC} Average funding rates (bar chart)"
echo -e "  ${CYAN}Panel 5:${NC} Total PnL by exchange (bar chart)"

pause_with_message "" $PAUSE_SHORT

# Open the plot based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_command "open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png"
    open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_command "xdg-open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png"
    xdg-open outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png
else
    echo -e "${YELLOW}Plot saved to: outputs/funding_analysis_demo/funding_diagnostics_BTCUSDT.png${NC}"
fi

pause_with_message "✓ Professional, publication-ready visualization!" $PAUSE_LONG

# ============================================================================
# PART 10: Customization Demo
# ============================================================================

print_header "PART 10: Customization Example"

print_step "The example is highly customizable. Let's run a quick 1-day analysis:"

print_command "python funding_batch_diagnostics.py --days 1 --symbol ETHUSDT --exchanges binance hyperliquid --output-dir outputs/eth_demo"

pause_with_message "Running customized analysis..." $PAUSE_SHORT

python funding_batch_diagnostics.py \
    --days 1 \
    --symbol ETHUSDT \
    --exchanges binance hyperliquid \
    --output-dir outputs/eth_demo

pause_with_message "\n✓ Easy to customize for different symbols, durations, and exchanges!" $PAUSE_MEDIUM

# ============================================================================
# PART 11: Summary
# ============================================================================

print_header "PART 11: Summary"

echo -e "${BOLD}What We Demonstrated:${NC}\n"
echo -e "  ${GREEN}✓${NC} Environment setup and validation"
echo -e "  ${GREEN}✓${NC} MCP API integration testing"
echo -e "  ${GREEN}✓${NC} 5-day batch market data generation"
echo -e "  ${GREEN}✓${NC} Multi-exchange funding simulation"
echo -e "  ${GREEN}✓${NC} Comprehensive analytics calculation"
echo -e "  ${GREEN}✓${NC} Professional diagnostic visualizations"
echo -e "  ${GREEN}✓${NC} Multiple output formats (Parquet, JSON, TXT, PNG)"
echo -e "  ${GREEN}✓${NC} Easy customization options"

echo -e "\n${BOLD}Key Features:${NC}\n"
echo -e "  ${CYAN}•${NC} ${BOLD}Production-ready code:${NC} Async, error handling, type hints"
echo -e "  ${CYAN}•${NC} ${BOLD}Reproducible results:${NC} Deterministic seeding"
echo -e "  ${CYAN}•${NC} ${BOLD}Institutional-grade:${NC} Realistic market microstructure"
echo -e "  ${CYAN}•${NC} ${BOLD}Exchange-specific:${NC} Venue-accurate funding models"
echo -e "  ${CYAN}•${NC} ${BOLD}Comprehensive docs:${NC} Quickstart, full docs, architecture"

echo -e "\n${BOLD}Use Cases:${NC}\n"
echo -e "  ${YELLOW}▸${NC} Quantitative strategy development and backtesting"
echo -e "  ${YELLOW}▸${NC} Exchange funding rate analysis and comparison"
echo -e "  ${YELLOW}▸${NC} Risk management and PnL modeling"
echo -e "  ${YELLOW}▸${NC} Market making and arbitrage research"
echo -e "  ${YELLOW}▸${NC} Educational demonstrations of MCP protocol"

echo -e "\n${BOLD}Next Steps:${NC}\n"
echo -e "  ${BLUE}1.${NC} Explore the generated files in outputs/"
echo -e "  ${BLUE}2.${NC} Read the documentation (funding_batch_diagnostics.md)"
echo -e "  ${BLUE}3.${NC} Customize for your specific use case"
echo -e "  ${BLUE}4.${NC} Integrate with your trading/research infrastructure"

# ============================================================================
# Finale
# ============================================================================

echo -e "\n${BOLD}${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                      DEMONSTRATION COMPLETE! 🎉                           ║
║                                                                           ║
║              Thank you for watching the Funding Batch                     ║
║              Diagnostics example for Aleatoric MCP.                       ║
║                                                                           ║
║          For more info: https://github.com/aleatoric/mcp                  ║
║                                                                           ║
╔═══════════════════════════════════════════════════════════════════════════╗
EOF
echo -e "${NC}\n"

echo -e "${GREEN}Demo completed successfully!${NC}"
echo -e "Recording can now be stopped.\n"
