#!/bin/bash
# Build and publish script for Proxmox CLI
# Usage: ./scripts/publish.sh [test|prod]

set -e

TARGET=${1:-test}

if [[ ! "$TARGET" =~ ^(test|prod)$ ]]; then
    echo "Error: Target must be 'test' or 'prod'"
    echo "Usage: $0 [test|prod]"
    exit 1
fi

echo "📦 Building Proxmox CLI for $TARGET..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Install build dependencies
echo "📥 Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "🔨 Building package..."
python -m build

# Check the distribution
echo "🔍 Checking package..."
twine check dist/*

# Check for PyPI API token
if [[ -z "$PY_PI_API_TOKEN" ]]; then
    echo "⚠️  Warning: PY_PI_API_TOKEN environment variable not set"
    echo "Twine will prompt for credentials or use ~/.pypirc"
fi

if [[ "$TARGET" == "test" ]]; then
    echo "📤 Uploading to Test PyPI..."
    echo "Repository: https://test.pypi.org/project/proxmox-cli/"
    if [[ -n "$PY_PI_API_TOKEN" ]]; then
        twine upload --repository testpypi --username __token__ --password "$PY_PI_API_TOKEN" dist/*
    else
        twine upload --repository testpypi dist/*
    fi
    
    echo ""
    echo "✅ Published to Test PyPI!"
    echo ""
    echo "To install from Test PyPI:"
    echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ proxmox-cli"
else
    echo "📤 Uploading to Production PyPI..."
    echo "⚠️  This will publish to the official PyPI repository!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [[ "$confirm" != "yes" ]]; then
        echo "❌ Aborted."
        exit 1
    fi
    
    if [[ -n "$PY_PI_API_TOKEN" ]]; then
        twine upload --username __token__ --password "$PY_PI_API_TOKEN" dist/*
    else
        twine upload dist/*
    fi
    
    echo ""
    echo "✅ Published to PyPI!"
    echo ""
    echo "To install:"
    echo "  pip install proxmox-cli"
fi

echo ""
echo "Package contents:"
ls -lh dist/
