# Makefile

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PRE_COMMIT := $(VENV)/bin/pre-commit

.PHONY: install precommit clean help

help:
	@echo "Available commands:"
	@echo "  make all        - It runs install and then precommit"
	@echo "  make install    - Set up the virtual environment and install all requirements"
	@echo "  make precommit  - Install pre-commit hooks"
	@echo "  make clean      - Remove the virtual environment"
	@echo "  make help       - Show this help message"

all: install precommit
	@echo "All resources are in place"

install: $(VENV) requirements.txt requirements-dev.txt
	@echo "Upgrading pip..."
	$(PIP) install --upgrade pip
	@echo "Installing requirements..."
	$(PIP) install -r requirements.txt
	@echo "Installing development requirements..."
	$(PIP) install -r requirements-dev.txt
	@$(MAKE) precommit

$(VENV):
	@echo "Creating virtual environment in $(VENV)..."
	python -m venv $(VENV)

precommit:
	@echo "Installing pre-commit hooks..."
	$(PRE_COMMIT) install

clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
