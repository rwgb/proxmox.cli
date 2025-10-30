# Act Quick Start Guide

Run GitHub Actions workflows locally before pushing to GitHub!

## Installation Complete ✓

Act is installed at: `./bin/act`

## Quick Commands

### List All Workflows
```bash
make act-list
# or
./bin/act -l
```

### Run Tests Locally
```bash
# Quick test (Python 3.11 on Ubuntu)
make act-test

# Or use the helper script with more options
./scripts/run-actions.sh tests --python 3.11
```

### Test Before Pushing
```bash
# 1. Format your code
make format

# 2. Run local tests
make act-test

# 3. If passes, commit and push
git add -A
git commit -m "your message"
git push
```

## Common Use Cases

### Test Specific Python Version
```bash
./scripts/run-actions.sh tests --python 3.11
./scripts/run-actions.sh tests --python 3.12
```

### Test All Python Versions (Ubuntu only)
```bash
./scripts/run-actions.sh tests --platform ubuntu-latest
```

### See What Will Run (Dry Run)
```bash
./scripts/run-actions.sh tests --dry-run
```

### Verbose Output for Debugging
```bash
./scripts/run-actions.sh tests --verbose --python 3.11
```

## Important Notes

⚠️ **Docker Required**: Act uses Docker containers. Make sure Docker is running:
```bash
docker ps
```

⚠️ **First Run is Slow**: Act downloads Docker images on first run. Subsequent runs are much faster.

⚠️ **Linux Only**: Act runs everything in Linux containers, even for macos-latest/windows-latest.

## Full Documentation

See [docs/ACT.md](./docs/ACT.md) for complete documentation.

## Troubleshooting

### "Cannot connect to Docker"
```bash
# Start Docker Desktop or Docker daemon
open -a Docker  # macOS
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x ./scripts/run-actions.sh
```

### "act: command not found"
```bash
# Use the local installation
./bin/act -l

# Or move to PATH
sudo mv ./bin/act /usr/local/bin/act
```

## Getting Help

```bash
# Script help
./scripts/run-actions.sh --help

# Act help
./bin/act --help

# List available workflows
make act-list
```

## Examples from Your Project

### Before Pushing a Fix
```bash
# 1. Make your changes
vim src/proxmox_cli/commands/vm.py

# 2. Format
black src/proxmox_cli/

# 3. Test locally
make act-test

# 4. If successful, push
git commit -am "fix: update VM command"
git push
```

### Testing a Workflow Change
```bash
# Modify workflow
vim .github/workflows/tests.yml

# Test it locally
./bin/act push -W .github/workflows/tests.yml --matrix python-version:3.11

# If works, commit
git add .github/workflows/tests.yml
git commit -m "ci: update tests workflow"
```

### Quick Lint Check
```bash
# Run just the linting steps (faster than full workflow)
black --check src/proxmox_cli tests/
flake8 src/proxmox_cli tests/
isort --check-only src/proxmox_cli tests/
```
