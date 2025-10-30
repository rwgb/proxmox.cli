.PHONY: help install install-dev test lint format clean build publish bump-patch bump-minor bump-major release act-test act-publish act-list

help:
	@echo "Available targets:"
	@echo "  install       - Install package"
	@echo "  install-dev   - Install package with development dependencies"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linting"
	@echo "  format        - Format code"
	@echo "  clean         - Clean build artifacts"
	@echo "  build         - Build distribution packages"
	@echo "  bump-patch    - Bump patch version (0.1.0 -> 0.1.1)"
	@echo "  bump-minor    - Bump minor version (0.1.0 -> 0.2.0)"
	@echo "  bump-major    - Bump major version (0.1.0 -> 1.0.0)"
	@echo "  publish-test  - Publish to Test PyPI"
	@echo "  publish-prod  - Publish to PyPI"
	@echo "  release-patch - Complete patch release workflow"
	@echo "  release-minor - Complete minor release workflow"
	@echo "  release-major - Complete major release workflow"
	@echo "  act-test      - Run tests workflow locally with act (Python 3.11/Ubuntu)"
	@echo "  act-publish   - Run publish workflow locally with act"
	@echo "  act-list      - List all available workflows and jobs"

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

bump-patch:
	./scripts/bump_version.sh patch

bump-minor:
	./scripts/bump_version.sh minor

bump-major:
	./scripts/bump_version.sh major

publish-test:
	./scripts/publish.sh test

publish-prod:
	./scripts/publish.sh prod

release-patch:
	./scripts/release.sh patch

release-minor:
	./scripts/release.sh minor

release-major:
	./scripts/release.sh major

# Act (local GitHub Actions) targets
act-test:
	./scripts/run-actions.sh tests --platform ubuntu-latest --python 3.11

act-publish:
	./scripts/run-actions.sh publish --event release --dry-run

act-list:
	./scripts/run-actions.sh all
