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
