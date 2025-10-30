#!/bin/bash
# Complete release workflow for Proxmox CLI
# Usage: ./scripts/release.sh [major|minor|patch]

set -e

VERSION_PART=${1:-patch}

if [[ ! "$VERSION_PART" =~ ^(major|minor|patch)$ ]]; then
    echo "Error: Version part must be 'major', 'minor', or 'patch'"
    echo "Usage: $0 [major|minor|patch]"
    exit 1
fi

echo "🚀 Starting release workflow for $VERSION_PART version..."
echo ""

# Step 1: Bump version
echo "Step 1: Bumping version..."
./scripts/bump_version.sh $VERSION_PART

# Step 2: Run tests
echo ""
echo "Step 2: Running tests..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v || {
        echo "❌ Tests failed. Please fix the issues before releasing."
        exit 1
    }
else
    echo "⚠️  pytest not found, skipping tests"
fi

# Step 3: Build package
echo ""
echo "Step 3: Building package..."
./scripts/publish.sh test

# Get the new version
NEW_VERSION=$(grep "^current_version" .bumpversion.cfg | cut -d'=' -f2 | tr -d ' ')

echo ""
echo "✅ Release $NEW_VERSION complete!"
echo ""
echo "📝 Next steps:"
echo "1. Test the package from Test PyPI:"
echo "   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ proxmox-cli"
echo ""
echo "2. If everything works, publish to production PyPI:"
echo "   ./scripts/publish.sh prod"
echo ""
echo "3. Push the version tag to GitHub:"
echo "   git push origin v$NEW_VERSION"
echo ""
echo "4. Create a GitHub release with the changelog"
