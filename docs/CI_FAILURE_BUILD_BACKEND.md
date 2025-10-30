# CI Workflow Failure Analysis - Build Backend Error

## Issue Summary

**Workflow**: Tests (Windows, Python 3.12)  
**Failed Step**: Install dependencies  
**Error**: `Getting requirements to build editable did not run successfully`  
**Root Cause**: Incomplete setuptools build backend configuration in `pyproject.toml`

## What Happened

The GitHub Actions workflow on Windows failed when trying to install the package in editable mode:

```bash
pip install -e ".[dev]"
```

### Error Message

```
Getting requirements to build editable did not run successfully.
exit code: 1

File "...\setuptools\build_meta.py", line 473, in get_requires_for_build_editable
    return self.get_requires_for_build_wheel(config_settings)
```

## Root Causes

### 1. setuptools_scm Not Configured

The `pyproject.toml` had `setuptools_scm` in build requirements but **no configuration**:

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]  # ❌ Not configured
```

`setuptools_scm` is for **automatic version management from git tags**. Since we're managing versions **manually** with `bump-my-version`, this dependency was unnecessary and causing conflicts.

### 2. Missing Package Discovery Configuration

Modern setuptools (PEP 660) requires explicit package discovery when using `src` layout:

**Before** (missing):
```toml
[project.scripts]
proxmox-cli = "proxmox_cli.cli:main"

[tool.black]  # Directly after scripts
```

**After** (fixed):
```toml
[project.scripts]
proxmox-cli = "proxmox_cli.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
```

### 3. Outdated setuptools Requirement

**Before**: `setuptools>=45` (from 2020)  
**After**: `setuptools>=61.0` (better PEP 660 editable install support)

## The Fix

### Changes to `pyproject.toml`

```diff
[build-system]
-requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
+requires = ["setuptools>=61.0", "wheel"]
 build-backend = "setuptools.build_meta"

 [project.scripts]
 proxmox-cli = "proxmox_cli.cli:main"

+[tool.setuptools]
+package-dir = {"" = "src"}
+
+[tool.setuptools.packages.find]
+where = ["src"]
+
 [tool.black]
```

### What This Does

1. **Removed `setuptools_scm`** - We don't use automatic versioning from git
2. **Upgraded setuptools** - Modern version with better PEP 660 support  
3. **Added package discovery** - Tells setuptools where to find packages (`src/`)
4. **Explicit package directory** - Maps root to `src` folder

## Verification

Test locally:

```bash
# Test package can be built
python3 -m pip install -e ".[dev]" --no-deps --dry-run

# Expected output:
# Would install proxmox-cli-0.1.0
```

## Why It Failed on Windows But Not macOS/Linux

This is a **setuptools version/configuration sensitivity issue**:

- **Windows runners**: Stricter setuptools validation, newer pip versions
- **macOS/Linux**: May have had older setuptools that were more permissive
- **All platforms**: Should now work consistently

## Related Files

- `pyproject.toml` - Modern Python project configuration (PEP 518/621)
- `setup.py` - Legacy setup file (kept for compatibility)

**Note**: We're using **both** files for maximum compatibility:
- `pyproject.toml` - Modern standard, used by pip/build tools
- `setup.py` - Legacy fallback, used by bump-my-version

## Prevention

### Test Editable Install Locally

Before pushing:

```bash
# Create fresh virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Test editable install
pip install -e ".[dev]"

# Should succeed without errors
```

### Use act to Test All Platforms

```bash
# Test on all OS platforms locally
./scripts/run-actions.sh tests --verbose
```

## Understanding Editable Installs

**Editable install** (`pip install -e .`):
- Installs package in "development mode"
- Changes to source code are immediately reflected
- No need to reinstall after code changes
- **Requires** proper package discovery configuration

**Regular install** (`pip install .`):
- Copies package to site-packages
- Changes require reinstall
- More forgiving of configuration issues

## Key Takeaways

1. ✅ **Remove unused dependencies** - Don't include `setuptools_scm` without configuration
2. ✅ **Use modern setuptools** - >=61.0 for better PEP 660 support
3. ✅ **Explicit is better** - Always configure package discovery for src layout
4. ✅ **Test editable installs** - They're stricter than regular installs
5. ✅ **Test on Windows** - Often catches configuration issues first

## Commit

**Commit**: `1992434` - "fix: resolve setuptools build backend configuration"

Changes:
- Removed `setuptools_scm[toml]>=6.2` from build requirements
- Updated `setuptools>=45` to `setuptools>=61.0`
- Added `[tool.setuptools]` section with `package-dir`
- Added `[tool.setuptools.packages.find]` with `where = ["src"]`

## Status

✅ **Fixed**: pyproject.toml now has proper setuptools configuration  
✅ **Committed**: Changes committed to `dev` branch  
✅ **Pushed**: Available on GitHub for CI to re-run  
✅ **Documented**: This analysis created for future reference

The Windows CI workflow should now pass! 🎉

## Additional Resources

- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml specification
- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml
- [PEP 660](https://peps.python.org/pep-0660/) - Editable installs
- [setuptools packaging guide](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)
- [setuptools src layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout)
