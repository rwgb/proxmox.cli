# Release and Publishing Guide

This guide explains how to manage versions, create releases, and publish the Proxmox CLI to PyPI.

## Table of Contents

- [Version Management](#version-management)
- [Release Workflow](#release-workflow)
- [Publishing to PyPI](#publishing-to-pypi)
- [PyPI Configuration](#pypi-configuration)
- [GitHub Releases](#github-releases)

## Version Management

This project uses [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Automated Version Bumping

We use `bump-my-version` to automatically update version numbers across all files.

#### Install Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- `bump-my-version` - Version bumping tool
- `build` - Package builder
- `twine` - PyPI uploader

#### Bump Version Manually

```bash
# Bump patch version (0.1.0 → 0.1.1)
bump-my-version bump patch

# Bump minor version (0.1.0 → 0.2.0)
bump-my-version bump minor

# Bump major version (0.1.0 → 1.0.0)
bump-my-version bump major
```

The version is automatically updated in:
- `pyproject.toml`
- `setup.py`
- `src/proxmox_cli/__init__.py`
- Git commit and tag created automatically

#### Using Scripts

```bash
# Bump patch version
./scripts/bump_version.sh patch

# Bump minor version
./scripts/bump_version.sh minor

# Bump major version
./scripts/bump_version.sh major
```

## Release Workflow

### Quick Release (Recommended)

Use the automated release script:

```bash
# Create a patch release
./scripts/release.sh patch

# Create a minor release
./scripts/release.sh minor

# Create a major release
./scripts/release.sh major
```

This script will:
1. ✅ Bump the version
2. ✅ Run tests
3. ✅ Build the package
4. ✅ Upload to Test PyPI
5. ✅ Provide next steps

### Manual Release Process

#### 1. Prepare for Release

Ensure your working directory is clean:

```bash
git status
```

Commit any pending changes:

```bash
git add .
git commit -m "chore: prepare for release"
```

#### 2. Bump Version

```bash
./scripts/bump_version.sh patch  # or minor/major
```

#### 3. Run Tests

```bash
pytest tests/ -v
```

#### 4. Build Package

```bash
./scripts/publish.sh test
```

#### 5. Test from Test PyPI

```bash
# Create a test environment
python -m venv test-env
source test-env/bin/activate  # On Windows: test-env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            proxmox-cli

# Test the installation
proxmox-cli --version
proxmox-cli --help

# Clean up
deactivate
rm -rf test-env
```

#### 6. Publish to Production PyPI

```bash
./scripts/publish.sh prod
```

#### 7. Push Tags to GitHub

```bash
git push origin release/0.1.0
git push --tags
```

## Publishing to PyPI

### First-Time Setup

#### 1. Create PyPI Accounts

- **Test PyPI**: https://test.pypi.org/account/register/
- **Production PyPI**: https://pypi.org/account/register/

#### 2. Generate API Tokens

**Test PyPI:**
1. Go to https://test.pypi.org/manage/account/token/
2. Create new token with name "proxmox-cli"
3. Save the token securely

**Production PyPI:**
1. Go to https://pypi.org/manage/account/token/
2. Create new token with name "proxmox-cli"
3. Save the token securely

#### 3. Configure Credentials

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-production-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

Set proper permissions:

```bash
chmod 600 ~/.pypirc
```

### Publishing Commands

#### Test PyPI (Recommended First)

```bash
# Build
python -m build

# Upload to Test PyPI
twine upload --repository testpypi dist/*
```

#### Production PyPI

```bash
# Build
python -m build

# Upload to PyPI
twine upload dist/*
```

### Verify Publication

**Test PyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            proxmox-cli
```

**Production PyPI:**
```bash
pip install proxmox-cli
```

## GitHub Releases

### Create GitHub Release

After publishing to PyPI, create a GitHub release:

1. Go to https://github.com/rwgb/proxmox.cli/releases/new
2. Select the version tag (e.g., `v0.1.0`)
3. Set release title: `Release 0.1.0`
4. Add release notes (see template below)
5. Attach distribution files from `dist/` folder
6. Click "Publish release"

### Release Notes Template

```markdown
## What's New

### Features
- Add user management commands
- Add group management commands
- Add role management commands
- Add ACL/permissions management
- Add API token management

### Improvements
- Enhanced JSON output formatting
- Better error handling

### Bug Fixes
- Fixed SSL verification issues
- Fixed offline node handling

### Documentation
- Added IAM documentation
- Updated API examples

## Installation

```bash
pip install proxmox-cli==0.1.0
```

## Upgrade

```bash
pip install --upgrade proxmox-cli
```

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.
```

## Version Bump Examples

### Patch Release (Bug Fixes)

```bash
# Current: 0.1.0
./scripts/bump_version.sh patch
# New: 0.1.1
```

Use for:
- Bug fixes
- Documentation updates
- Minor improvements

### Minor Release (New Features)

```bash
# Current: 0.1.0
./scripts/bump_version.sh minor
# New: 0.2.0
```

Use for:
- New features
- Backward-compatible changes
- New commands or options

### Major Release (Breaking Changes)

```bash
# Current: 0.1.0
./scripts/bump_version.sh major
# New: 1.0.0
```

Use for:
- Breaking API changes
- Removed features
- Major refactoring

## Troubleshooting

### Clean Build Artifacts

```bash
rm -rf dist/ build/ *.egg-info src/*.egg-info
```

### Reinstall in Development Mode

```bash
pip install -e ".[dev]"
```

### Check Package

```bash
python -m build
twine check dist/*
```

### View Package Contents

```bash
tar -tzf dist/proxmox-cli-0.1.0.tar.gz
```

## Continuous Integration

For automated releases using GitHub Actions, see `.github/workflows/release.yml`.

## Best Practices

1. **Always test on Test PyPI first**
2. **Run tests before releasing**
3. **Update CHANGELOG.md**
4. **Create GitHub release with notes**
5. **Use semantic versioning**
6. **Tag releases in git**
7. **Keep credentials secure**
8. **Document breaking changes**

## Quick Reference

```bash
# Bump version and commit
./scripts/bump_version.sh patch

# Complete release to Test PyPI
./scripts/release.sh patch

# Publish to production
./scripts/publish.sh prod

# Manual bump
bump-my-version bump patch

# Build package
python -m build

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```
