# Act Setup Complete! 🎉

You can now run GitHub Actions workflows locally using **nektos/act**.

## What Was Installed

✅ **act binary** - Installed to `./bin/act` (version 0.2.82)
✅ **Configuration** - `.actrc` with sensible defaults
✅ **Helper script** - `./scripts/run-actions.sh` for easy workflow execution
✅ **Makefile targets** - Quick commands for common tasks
✅ **Documentation** - Complete guides in `docs/ACT.md` and `docs/ACT_QUICKSTART.md`

## ⚠️ Next Step Required: Install Docker

Act requires Docker to run workflows in containers. You need to install Docker Desktop:

### Install Docker Desktop for macOS

1. **Download**: https://www.docker.com/products/docker-desktop/
2. **Install**: Open the downloaded `.dmg` file and drag Docker to Applications
3. **Start**: Open Docker Desktop from Applications
4. **Verify**: Run `docker ps` to confirm it's running

Alternatively, using Homebrew (if available):
```bash
brew install --cask docker
```

## Quick Start (After Installing Docker)

### 1. List Available Workflows
```bash
make act-list
```
Output:
```
Stage  Job ID             Job name           Workflow name    Workflow file    Events
0      build-and-publish  build-and-publish  Publish to PyPI  publish.yml      release
0      test               test               Tests            tests.yml        push,pull_request
```

### 2. Run Tests Locally
```bash
# Quick test with Python 3.11 on Ubuntu (fastest)
make act-test
```

This will:
- Pull the Docker image (first time only, ~2-3 minutes)
- Run the tests workflow with Python 3.11 on Ubuntu
- Show you results just like GitHub Actions

### 3. Test Before Pushing Code
```bash
# 1. Make your changes
vim src/proxmox_cli/cli.py

# 2. Format code
make format

# 3. Test locally (catches issues before pushing!)
make act-test

# 4. If passes, commit and push
git add -A
git commit -m "feat: add new feature"
git push
```

## Available Commands

### Makefile Shortcuts
```bash
make act-test      # Run tests (Python 3.11, Ubuntu)
make act-publish   # Test publish workflow (dry-run)
make act-list      # List all workflows
```

### Helper Script (More Options)
```bash
# Test specific Python version
./scripts/run-actions.sh tests --python 3.11
./scripts/run-actions.sh tests --python 3.12

# Test all Python versions (Ubuntu only)
./scripts/run-actions.sh tests --platform ubuntu-latest

# Dry run (see what would execute)
./scripts/run-actions.sh tests --dry-run

# Verbose output for debugging
./scripts/run-actions.sh tests --verbose --python 3.11

# Get help
./scripts/run-actions.sh --help
```

### Direct act Commands
```bash
# List workflows
./bin/act -l

# Run specific workflow
./bin/act push -W .github/workflows/tests.yml

# Run with matrix filtering
./bin/act -W .github/workflows/tests.yml \
  --matrix python-version:3.11 \
  --matrix os:ubuntu-latest
```

## Why Use Act?

### Before Act (Slow Feedback Loop)
1. Write code
2. Commit and push
3. Wait for GitHub Actions to run (3-5 minutes)
4. See it failed on a linting error 😞
5. Fix locally
6. Push again
7. Wait again...

### With Act (Fast Feedback Loop)
1. Write code
2. Run `make act-test` (30 seconds - 1 minute)
3. See it fails immediately
4. Fix locally
5. Run `make act-test` again
6. Passes! Now push with confidence ✅

**Time saved**: 90% faster iteration!

## Common Use Cases

### Before Committing
```bash
# Quick validation
make format      # Format code
make act-test    # Test locally
git commit -am "fix: update feature"
git push
```

### Testing Workflow Changes
```bash
# Edit workflow
vim .github/workflows/tests.yml

# Test it
./bin/act push -W .github/workflows/tests.yml --matrix python-version:3.11

# If works, commit
git add .github/workflows/tests.yml
git commit -m "ci: improve tests workflow"
```

### Debugging CI Failures
```bash
# Run with verbose output
./scripts/run-actions.sh tests --verbose --python 3.11

# Or run individual steps manually
black --check src/proxmox_cli tests/
flake8 src/proxmox_cli tests/
pytest tests/ -v
```

## Important Notes

⚠️ **Docker is Required** - Act won't work without Docker running
⚠️ **First Run is Slow** - Downloads Docker images (~500MB), but cached after
⚠️ **Linux Containers Only** - Even macos-latest/windows-latest run in Linux
⚠️ **Some Limitations** - GitHub-specific features may not work (GITHUB_TOKEN, etc.)

## Documentation

- **Quick Start**: `docs/ACT_QUICKSTART.md` - Quick reference
- **Complete Guide**: `docs/ACT.md` - Full documentation with examples
- **Helper Script**: `./scripts/run-actions.sh --help` - Script usage
- **Official Docs**: https://nektosact.com/ - Act documentation

## Testing Your Setup

Once Docker is installed, test the setup:

```bash
# 1. Verify Docker is running
docker ps

# 2. List workflows
make act-list

# 3. Run a quick test (dry run)
./scripts/run-actions.sh tests --dry-run

# 4. Run actual test (will download Docker image first time)
make act-test
```

## Troubleshooting

### Docker not found
Install Docker Desktop from https://www.docker.com/products/docker-desktop/

### Cannot connect to Docker daemon
```bash
# Start Docker Desktop
open -a Docker
```

### Permission denied on scripts
```bash
chmod +x ./scripts/run-actions.sh
```

### act command not found
```bash
# Use local binary
./bin/act -l

# Or move to PATH
sudo mv ./bin/act /usr/local/bin/act
```

## Next Steps

1. **Install Docker Desktop** (required)
2. **Test the setup**: `make act-list`
3. **Run your first local workflow**: `make act-test`
4. **Read the docs**: `cat docs/ACT_QUICKSTART.md`

## Benefits You'll See

✅ **Catch errors early** - Find issues before pushing
✅ **Faster iteration** - 90% faster than waiting for GitHub Actions
✅ **Confidence** - Know your PR will pass CI before pushing
✅ **Learn workflows** - Understand how GitHub Actions work
✅ **Save time** - No more "fix lint error" commits

Happy local testing! 🚀
