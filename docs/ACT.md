# Running GitHub Actions Locally with Act

This document explains how to run GitHub Actions workflows locally using `nektos/act`.

## What is Act?

[Act](https://github.com/nektos/act) is a tool that allows you to run your GitHub Actions locally. It reads your workflow files and executes them using Docker containers, simulating the GitHub Actions environment.

## Prerequisites

- **Docker**: Act uses Docker to run workflows. Make sure Docker is installed and running.
- **act**: The act CLI tool (already installed via install script)

## Installation

Act has been installed to `./bin/act`. You may want to move it to your PATH:

```bash
sudo mv ./bin/act /usr/local/bin/act
```

Or add `./bin` to your PATH:

```bash
export PATH="$PWD/bin:$PATH"
```

## Quick Start

### List Available Workflows

```bash
# List all workflows and their jobs
act -l

# List jobs in a specific workflow
./scripts/run-actions.sh tests --list
```

### Run the Tests Workflow

```bash
# Run all test jobs (will run all OS/Python combinations)
./scripts/run-actions.sh tests

# Run tests with specific Python version
./scripts/run-actions.sh tests --python 3.11

# Run tests on specific platform
./scripts/run-actions.sh tests --platform ubuntu-latest

# Run specific job
./scripts/run-actions.sh tests --job test

# Combine filters (Python 3.11 on Ubuntu only)
./scripts/run-actions.sh tests --platform ubuntu-latest --python 3.11
```

### Dry Run

See what would be executed without running:

```bash
./scripts/run-actions.sh tests --dry-run
```

### Verbose Output

Get detailed information about what's happening:

```bash
./scripts/run-actions.sh tests --verbose
```

## Direct Act Commands

You can also use act directly:

```bash
# List all workflows
act -l

# Run a specific workflow
act -W .github/workflows/tests.yml

# Run a specific job
act -W .github/workflows/tests.yml -j test

# Run with specific event
act push -W .github/workflows/tests.yml

# Run with matrix variables
act -W .github/workflows/tests.yml --matrix python-version:3.11 --matrix os:ubuntu-latest

# Pull latest images before running
act -W .github/workflows/tests.yml --pull
```

## Configuration

### .actrc File

The `.actrc` file configures default behavior for act:

```bash
# Use specific Docker images
-P ubuntu-latest=catthehacker/ubuntu:act-latest

# Reuse containers for faster runs
--reuse

# Verbose output
--verbose
```

### .env.act File

Store environment variables and secrets in `.env.act`:

```bash
GITHUB_TOKEN=your_token_here
PYPI_API_TOKEN=your_test_pypi_token
```

**Note**: This file is gitignored. Never commit secrets to version control.

## Workflow-Specific Usage

### Tests Workflow

The tests workflow runs on multiple OS and Python versions. When running locally, you'll likely want to limit the matrix:

```bash
# Run only Python 3.11 on Ubuntu (fastest)
./scripts/run-actions.sh tests --platform ubuntu-latest --python 3.11

# Run all Python versions on Ubuntu
./scripts/run-actions.sh tests --platform ubuntu-latest

# Run specific Python version on all platforms
./scripts/run-actions.sh tests --python 3.11
```

**Individual Steps:**

To run individual linting/testing steps locally without act:

```bash
# Format check
black --check src/proxmox_cli tests/

# Lint
flake8 src/proxmox_cli tests/

# Sort imports
isort --check-only src/proxmox_cli tests/

# Type check
mypy src/proxmox_cli

# Tests
pytest tests/ -v --cov=src/proxmox_cli
```

### Publish Workflow

The publish workflow requires a GitHub release event:

```bash
# Simulate a release event (dry run recommended)
./scripts/run-actions.sh publish --event release --dry-run

# Actually run it (ensure you have PYPI_API_TOKEN in .env.act)
./scripts/run-actions.sh publish --event release
```

## Troubleshooting

### Docker Issues

If you get Docker-related errors:

```bash
# Check if Docker is running
docker ps

# Pull the latest act images
docker pull catthehacker/ubuntu:act-latest
```

### Container Permission Issues

If you encounter permission issues:

```bash
# Run with --privileged
act --privileged
```

### Secrets Not Working

Make sure secrets are in `.env.act` and the file is being read:

```bash
# Verify env file location
cat .env.act

# Check if act is reading it
act --env-file .env.act --list
```

### Workflow Not Found

Make sure you're in the project root directory:

```bash
cd /Users/ralph.brynard/rwgb.github.projects/proxmox.cli
./scripts/run-actions.sh tests
```

## Performance Tips

1. **Use --reuse**: Reuses containers between runs (configured in `.actrc`)
2. **Limit matrix**: Run specific OS/Python combinations instead of all
3. **Run individual steps**: For quick checks, run commands directly instead of full workflow
4. **Use medium images**: We use `catthehacker/ubuntu:act-latest` for better compatibility

## Common Use Cases

### Before Pushing Code

```bash
# Quick validation (Python 3.11 on Ubuntu only)
./scripts/run-actions.sh tests --platform ubuntu-latest --python 3.11

# Or run individual checks
black --check src/proxmox_cli tests/
flake8 src/proxmox_cli tests/
pytest tests/
```

### Testing Workflow Changes

```bash
# Test modified workflow
act -W .github/workflows/tests.yml --dry-run

# Run it
act -W .github/workflows/tests.yml
```

### Debugging Failed CI

```bash
# Run with verbose output
./scripts/run-actions.sh tests --verbose --python 3.11

# Run specific failing job
./scripts/run-actions.sh tests --job test --platform ubuntu-latest
```

## Limitations

1. **No macOS/Windows containers**: Act runs everything in Linux containers (even for macos-latest/windows-latest)
2. **Some GitHub-specific features unavailable**: Like GitHub API interactions, GITHUB_TOKEN permissions
3. **Different environment**: May have subtle differences from actual GitHub Actions runners
4. **Docker required**: All workflows run in Docker containers

## Additional Resources

- [Act Documentation](https://nektosact.com/)
- [Act GitHub Repository](https://github.com/nektos/act)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Images for Act](https://github.com/catthehacker/docker_images)

## Examples

### Complete Testing Before Push

```bash
# 1. Format code
black src/proxmox_cli tests/

# 2. Run local validation
./scripts/run-actions.sh tests --platform ubuntu-latest --python 3.11

# 3. If all passes, commit and push
git add -A
git commit -m "feat: add new feature"
git push
```

### Testing Multiple Python Versions

```bash
# Test with all Python versions on Ubuntu
for version in 3.8 3.9 3.10 3.11 3.12; do
    echo "Testing Python $version..."
    ./scripts/run-actions.sh tests --platform ubuntu-latest --python $version
done
```

### Quick Lint Check

```bash
# Just run the linting steps
act -W .github/workflows/tests.yml -j test --matrix python-version:3.11 \
    --env ACT=true \
    -s GITHUB_TOKEN="" \
    --no-skip-checkout
```
