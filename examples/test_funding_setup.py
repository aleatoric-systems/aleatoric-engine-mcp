#!/usr/bin/env python3
"""
Test script to validate your setup for funding_batch_diagnostics.py

This script checks that all required dependencies are installed and provides
helpful feedback without making any API calls.

Usage:
    python test_funding_setup.py
"""

import sys
from pathlib import Path


def check_python_version():
    """Check Python version compatibility."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (3.9+ required)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")

    dependencies = {
        'httpx': 'HTTP client for API calls',
        'matplotlib': 'Plotting and visualization',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical operations',
    }

    all_installed = True

    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"  ✓ {package:15s} - {description}")
        except ImportError:
            print(f"  ✗ {package:15s} - {description} (MISSING)")
            all_installed = False

    return all_installed


def check_api_key():
    """Check if API key is set."""
    import os
    print("\nChecking API key...")

    api_key = os.getenv('ALEATORIC_API_KEY')
    if api_key:
        masked_key = api_key[:8] + '...' + api_key[-4:] if len(api_key) > 12 else '***'
        print(f"  ✓ ALEATORIC_API_KEY is set ({masked_key})")
        return True
    else:
        print("  ✗ ALEATORIC_API_KEY not set")
        print("    Set it with: export ALEATORIC_API_KEY='your-key-here'")
        return False


def check_output_directory():
    """Check if output directory is writable."""
    print("\nChecking output directory...")

    test_dir = Path(__file__).parent / "outputs" / "test"
    try:
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / "test_write.txt"
        test_file.write_text("test")
        test_file.unlink()
        test_dir.rmdir()
        print(f"  ✓ Output directory is writable")
        return True
    except Exception as e:
        print(f"  ✗ Cannot write to output directory: {e}")
        return False


def simulate_example_data():
    """Create a minimal example to show expected data structure."""
    print("\nSimulating example data structure...")

    try:
        import pandas as pd
        import numpy as np

        # Create sample funding data
        periods = 15  # 5 days × 3 periods/day
        exchanges = ['binance', 'hyperliquid', 'okx']

        sample_data = {
            'Exchange': [],
            'Period': [],
            'Funding_Rate_bps': [],
            'Cumulative_PnL': []
        }

        for exchange in exchanges:
            cumulative = 0
            for period in range(periods):
                # Simulate some funding rates
                rate = np.random.normal(1.0, 0.5)  # 1 bps ± 0.5 bps
                pnl = -rate * 0.01  # Simplified PnL calculation
                cumulative += pnl

                sample_data['Exchange'].append(exchange.upper())
                sample_data['Period'].append(period)
                sample_data['Funding_Rate_bps'].append(rate)
                sample_data['Cumulative_PnL'].append(cumulative)

        df = pd.DataFrame(sample_data)

        print("\n  Sample Output Preview:")
        print("  " + "=" * 60)
        print("  This is what your data will look like:")
        print("  " + "=" * 60)

        # Show summary statistics
        summary = df.groupby('Exchange').agg({
            'Funding_Rate_bps': ['mean', 'std', 'min', 'max'],
            'Cumulative_PnL': 'last'
        }).round(2)

        print("\n  Summary by Exchange:")
        for line in summary.to_string().split('\n'):
            print(f"  {line}")

        print("\n  ✓ Sample data structure validated")
        return True

    except Exception as e:
        print(f"  ✗ Error creating sample data: {e}")
        return False


def test_plotting():
    """Test if matplotlib can create plots."""
    print("\nTesting plotting capability...")

    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt

        # Create a simple test plot
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title('Test Plot')

        # Save to temp location
        test_file = Path(__file__).parent / "outputs" / "test_plot.png"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(test_file, dpi=100)
        plt.close()

        # Clean up
        test_file.unlink()

        print("  ✓ Matplotlib plotting works")
        return True

    except Exception as e:
        print(f"  ✗ Plotting test failed: {e}")
        return False


def print_next_steps(all_checks_passed, api_key_set):
    """Print recommendations based on test results."""
    print("\n" + "=" * 70)
    print("SETUP VALIDATION SUMMARY")
    print("=" * 70)

    if all_checks_passed and api_key_set:
        print("\n✅ All checks passed! You're ready to run the example.")
        print("\nNext steps:")
        print("  1. Run the example:")
        print("     python funding_batch_diagnostics.py")
        print("\n  2. View the results in:")
        print("     outputs/funding_analysis/")
        print("\n  3. Check the generated reports:")
        print("     cat outputs/funding_analysis/report_BTCUSDT.txt")

    elif all_checks_passed and not api_key_set:
        print("\n⚠️  Almost ready! Just need to set your API key.")
        print("\nNext steps:")
        print("  1. Get an API key from: https://aleatoric.systems")
        print("  2. Set the environment variable:")
        print("     export ALEATORIC_API_KEY='your-key-here'")
        print("  3. Run this test again to verify")
        print("  4. Then run the example:")
        print("     python funding_batch_diagnostics.py")

    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nIf you continue to have issues:")
        print("  • Check Python version (3.9+ required)")
        print("  • Ensure pip is up to date: pip install --upgrade pip")
        print("  • Try in a virtual environment:")
        print("    python -m venv venv")
        print("    source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
        print("    pip install -r requirements.txt")

    print("\n" + "=" * 70)


def main():
    """Run all validation checks."""
    print("=" * 70)
    print("FUNDING BATCH DIAGNOSTICS - SETUP VALIDATION")
    print("=" * 70)
    print()
    print("This script will check if your environment is ready to run")
    print("the funding_batch_diagnostics.py example.")
    print()

    checks = []

    # Run all checks
    checks.append(('Python version', check_python_version()))
    checks.append(('Dependencies', check_dependencies()))
    api_key_set = check_api_key()
    checks.append(('API key', api_key_set))
    checks.append(('Output directory', check_output_directory()))
    checks.append(('Sample data', simulate_example_data()))
    checks.append(('Plotting', test_plotting()))

    # Determine overall status
    all_checks_passed = all(result for _, result in checks)

    # Print summary
    print_next_steps(all_checks_passed, api_key_set)

    # Return appropriate exit code
    return 0 if all_checks_passed else 1


if __name__ == "__main__":
    sys.exit(main())
