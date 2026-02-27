# Makefile for Aleatoric MCP Examples
#
# Quick commands for common tasks
#
# Usage:
#   make setup     - Create environment and install dependencies
#   make test      - Run validation tests
#   make demo      - Run the demo script
#   make example   - Run the main example
#   make clean     - Remove generated files
#   make help      - Show this help message

.PHONY: help setup install activate test test-setup test-api example demo clean distclean

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# Configuration
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ACTIVATE := . $(VENV)/bin/activate

help:
	@echo "$(BLUE)Aleatoric MCP Examples - Makefile$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@echo ""
	@echo "  $(YELLOW)make setup$(NC)        - Complete environment setup (recommended)"
	@echo "  $(YELLOW)make install$(NC)      - Install dependencies only (assumes venv exists)"
	@echo "  $(YELLOW)make test$(NC)         - Run all validation tests"
	@echo "  $(YELLOW)make test-setup$(NC)   - Run environment validation (no API calls)"
	@echo "  $(YELLOW)make test-api$(NC)     - Run API integration tests (requires API key)"
	@echo "  $(YELLOW)make example$(NC)      - Run the main funding example"
	@echo "  $(YELLOW)make demo$(NC)         - Run the automated demo script"
	@echo "  $(YELLOW)make clean$(NC)        - Remove outputs and cache"
	@echo "  $(YELLOW)make distclean$(NC)    - Remove everything (including venv)"
	@echo "  $(YELLOW)make help$(NC)         - Show this help message"
	@echo ""
	@echo "$(GREEN)First time setup:$(NC)"
	@echo "  1. make setup"
	@echo "  2. Edit .env and add your API key"
	@echo "  3. make test"
	@echo "  4. make example"
	@echo ""

setup:
	@echo "$(BLUE)Running automated setup...$(NC)"
	@bash setup.sh

$(VENV)/bin/activate:
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	@python3 -m venv $(VENV)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"

install: $(VENV)/bin/activate
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip --quiet
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"
	@echo ""
	@echo "$(YELLOW)Don't forget to:$(NC)"
	@echo "  1. Copy .env.example to .env"
	@echo "  2. Add your ALEATORIC_API_KEY to .env"
	@echo ""

test: test-setup test-api

test-setup: $(VENV)/bin/activate
	@echo "$(BLUE)Running environment validation...$(NC)"
	@$(ACTIVATE) && $(PYTHON) test_funding_setup.py

test-api: $(VENV)/bin/activate
	@echo "$(BLUE)Running API integration tests...$(NC)"
	@if [ -z "$$ALEATORIC_API_KEY" ] && [ ! -f .env ]; then \
		echo "$(YELLOW)⚠  Warning: ALEATORIC_API_KEY not set$(NC)"; \
		echo "Set it in .env or export it as an environment variable"; \
		exit 1; \
	fi
	@$(ACTIVATE) && \
		if [ -f .env ]; then export $$(cat .env | grep -v '^#' | xargs); fi && \
		$(PYTHON) test_mcp_integration.py

example: $(VENV)/bin/activate
	@echo "$(BLUE)Running funding batch diagnostics example...$(NC)"
	@if [ -z "$$ALEATORIC_API_KEY" ] && [ ! -f .env ]; then \
		echo "$(YELLOW)⚠  Warning: ALEATORIC_API_KEY not set$(NC)"; \
		echo "Set it in .env or export it as an environment variable"; \
		exit 1; \
	fi
	@$(ACTIVATE) && \
		if [ -f .env ]; then export $$(cat .env | grep -v '^#' | xargs); fi && \
		$(PYTHON) funding_batch_diagnostics.py

demo: $(VENV)/bin/activate
	@echo "$(BLUE)Running automated demo script...$(NC)"
	@if [ -z "$$ALEATORIC_API_KEY" ] && [ ! -f .env ]; then \
		echo "$(YELLOW)⚠  Warning: ALEATORIC_API_KEY not set$(NC)"; \
		echo "Set it in .env or export it as an environment variable"; \
		exit 1; \
	fi
	@$(ACTIVATE) && \
		if [ -f .env ]; then export $$(cat .env | grep -v '^#' | xargs); fi && \
		bash demo_script.sh

clean:
	@echo "$(BLUE)Cleaning generated files...$(NC)"
	@rm -rf outputs/
	@rm -rf __pycache__/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.log" -delete
	@rm -f *.cast *.gif *.mp4 *.webm
	@echo "$(GREEN)✓ Cleaned$(NC)"

distclean: clean
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	@rm -rf $(VENV)/
	@rm -f .env
	@echo "$(GREEN)✓ Complete cleanup done$(NC)"
	@echo ""
	@echo "$(YELLOW)Run 'make setup' to start fresh$(NC)"

# Convenience aliases
run: example
validate: test-setup
test-integration: test-api
