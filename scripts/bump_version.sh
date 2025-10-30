#!/bin/bash
# Version bumping script for Proxmox CLI
# Usage: ./scripts/bump_version.sh [major|minor|patch]

set -e

VERSION_PART=${1:-patch}

if [[ ! "$VERSION_PART" =~ ^(major|minor|patch)$ ]]; then
    echo "Error: Version part must be 'major', 'minor', or 'patch'"
    echo "Usage: $0 [major|minor|patch]"
    exit 1
fi

echo "📦 Bumping $VERSION_PART version..."

# Ensure we're on a clean working directory
if [[ -n $(git status -s) ]]; then
    echo "⚠️  Warning: You have uncommitted changes."
    echo "Please commit or stash your changes before bumping the version."
    exit 1
fi

# Install bump-my-version if not already installed
if ! command -v bump-my-version &> /dev/null; then
    echo "📥 Installing bump-my-version..."
    pip install bump-my-version
fi

# Get current version
CURRENT_VERSION=$(grep "^current_version" .bumpversion.cfg | cut -d'=' -f2 | tr -d ' ')
echo "Current version: $CURRENT_VERSION"

# Bump version
echo "🔄 Bumping version..."
bump-my-version bump $VERSION_PART

# Get new version
NEW_VERSION=$(grep "^current_version" .bumpversion.cfg | cut -d'=' -f2 | tr -d ' ')
echo "✅ Version bumped to: $NEW_VERSION"

# Show the changes
echo ""
echo "📝 Changes made:"
git show --stat

echo ""
echo "✅ Version bump complete!"
echo "   Old version: $CURRENT_VERSION"
echo "   New version: $NEW_VERSION"
echo ""
echo "Next steps:"
echo "1. Review the changes: git show"
echo "2. Push the changes: git push && git push --tags"
echo "3. Build the package: python -m build"
echo "4. Publish to PyPI: twine upload dist/*"
