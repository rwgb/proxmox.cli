.PHONY: help install install-dev test lint format clean build

help:
	@echo "Available targets:"
	@echo "  install      - Install package"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build distribution packages"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src/proxmox_cli --cov-report=term-missing

lint:
	flake8 src/proxmox_cli tests/
	mypy src/proxmox_cli

format:
	black src/proxmox_cli tests/
	isort src/proxmox_cli tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/

build: clean
	python -m build
