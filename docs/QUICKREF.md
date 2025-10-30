# Quick Reference Guide - Version Management & Publishing

## Version Bumping

### Using Scripts (Recommended)
```bash
# Patch version (0.1.0 → 0.1.1)
./scripts/bump_version.sh patch
# or
make bump-patch

# Minor version (0.1.0 → 0.2.0)
./scripts/bump_version.sh minor
# or
make bump-minor

# Major version (0.1.0 → 1.0.0)
./scripts/bump_version.sh major
# or
make bump-major
```

### Using bump-my-version Directly
```bash
bump-my-version bump patch
bump-my-version bump minor
bump-my-version bump major

# Show current version
bump-my-version show current_version

# Dry run (see what will change)
bump-my-version bump --dry-run patch
```

## Publishing

### Test PyPI (Always test first!)
```bash
./scripts/publish.sh test
# or
make publish-test
```

### Production PyPI
```bash
./scripts/publish.sh prod
# or
make publish-prod
```

## Complete Release Workflow

```bash
# Automated release (recommended)
./scripts/release.sh patch  # or minor/major
# or
make release-patch  # or release-minor/release-major

# This will:
# 1. Bump version
# 2. Run tests
# 3. Build package
# 4. Upload to Test PyPI
# 5. Provide next steps
```

## Manual Steps

### 1. Build Package
```bash
python -m build
# or
make build
```

### 2. Check Package
```bash
twine check dist/*
```

### 3. Upload to Test PyPI
```bash
twine upload --repository testpypi dist/*
```

### 4. Test Installation
```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            proxmox-cli
```

### 5. Upload to PyPI
```bash
twine upload dist/*
```

## Configuration Files

### PyPI Credentials (~/.pypirc)
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-production-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token
```

### Version Configuration (pyproject.toml)
```toml
[tool.bumpversion]
current_version = "0.1.0"
commit = true
tag = true
tag_name = "v{new_version}"
message = "chore: bump version from {current_version} to {new_version}"
```

## Git Operations

### Push Changes
```bash
# Push branch
git push origin release/0.1.0

# Push tags
git push --tags

# Push all
git push origin release/0.1.0 --tags
```

### Using Git Flow
```bash
# Start release
git flow release start 0.1.0

# Finish release (merges to main and dev, creates tag)
git flow release finish 0.1.0
```

## GitHub Actions

The repository includes automated workflows:

- **publish.yml** - Automatically publishes to PyPI when a GitHub release is created
- **tests.yml** - Runs tests on push/PR to main/dev branches

### Trigger Automated Publishing
1. Create a GitHub release with tag (e.g., `v0.1.0`)
2. GitHub Actions will automatically build and publish to PyPI

## Makefile Targets

```bash
make help              # Show all available targets
make install           # Install package
make install-dev       # Install with dev dependencies
make test              # Run tests
make lint              # Run linting
make format            # Format code
make clean             # Clean build artifacts
make build             # Build distribution
make bump-patch        # Bump patch version
make bump-minor        # Bump minor version
make bump-major        # Bump major version
make publish-test      # Publish to Test PyPI
make publish-prod      # Publish to PyPI
make release-patch     # Complete patch release
make release-minor     # Complete minor release
make release-major     # Complete major release
```

## Troubleshooting

### Clear Build Artifacts
```bash
rm -rf dist/ build/ *.egg-info src/*.egg-info
make clean
```

### Reinstall Package
```bash
pip uninstall proxmox-cli
pip install -e ".[dev]"
```

### Check Version
```bash
proxmox-cli --version
python -c "import proxmox_cli; print(proxmox_cli.__version__)"
bump-my-version show current_version
```

### View Package Files
```bash
tar -tzf dist/proxmox-cli-0.1.0.tar.gz
```

## Common Workflows

### Bug Fix Release
```bash
# 1. Fix the bug
# 2. Commit changes
git add .
git commit -m "fix: description of fix"

# 3. Bump patch version
make bump-patch

# 4. Release
make release-patch
```

### Feature Release
```bash
# 1. Develop feature
# 2. Commit changes
git add .
git commit -m "feat: new feature"

# 3. Bump minor version
make bump-minor

# 4. Release
make release-minor
```

### Breaking Change Release
```bash
# 1. Implement breaking change
# 2. Commit changes
git add .
git commit -m "feat!: breaking change"

# 3. Bump major version
make bump-major

# 4. Release
make release-major
```

## Links

- **PyPI**: https://pypi.org/project/proxmox-cli/
- **Test PyPI**: https://test.pypi.org/project/proxmox-cli/
- **GitHub**: https://github.com/rwgb/proxmox.cli
- **Documentation**: See docs/RELEASE.md for detailed instructions
