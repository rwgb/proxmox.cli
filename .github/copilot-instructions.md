# Proxmox CLI - AI Coding Agent Instructions

## Project Overview

A Python CLI tool for managing Proxmox Virtual Environment (VE) using the Proxmox API. Built with Click framework for command structure, supporting VMs, LXC containers, IAM (users/groups/roles/ACLs), nodes, storage, backups, and resource pools.

**Core Components:**
- `src/proxmox_cli/cli.py` - Main Click entry point, registers all command groups
- `src/proxmox_cli/client.py` - ProxmoxClient wrapper around proxmoxer library
- `src/proxmox_cli/config.py` - YAML config handler (`~/.config/proxmox-cli/config.yaml`)
- `src/proxmox_cli/commands/` - Command modules (vm, container, user, group, role, acl, etc.)
- `src/proxmox_cli/utils/output.py` - Output formatting (JSON, table, YAML, plain)

## Architecture Patterns

### Command Structure
All commands follow this pattern (see `src/proxmox_cli/commands/vm.py` as reference):

```python
@click.group()
def resource():
    """Manage [resource type]."""
    pass

@resource.command("action")
@click.option("--node", "-n", help="Node name")
@click.pass_context
def action_resource(ctx, node):
    client = get_proxmox_client(ctx)  # Always use this helper
    # Execute API calls through client.api
    # Handle output format from ctx.obj.get("output_format", "json")
```

**Critical:** Use `get_proxmox_client(ctx)` from `commands/helpers.py` to initialize the client - it handles config file loading, CLI option overrides, and SSL verification.

### Output Format Handling
Commands must support multiple output formats. Pattern from existing commands:
```python
output_format = ctx.obj.get("output_format", "json")
if output_format == "json":
    print_json(data)
else:
    # For table output, convert keys to uppercase
    table_data = [{k.upper(): v for k, v in item.items()} for item in data]
    print_table(table_data, title="Resource Name")
```

### Client API Access
ProxmoxClient wraps proxmoxer's ProxmoxAPI. Access endpoints using chained calls:
- VMs: `client.api.nodes(node).qemu(vmid).status.start.post()`
- Containers: `client.api.nodes(node).lxc(ctid).status.stop.post()`
- Users: `client.api.access.users.post(userid=userid, password=password)`

## Development Workflow

### Setup
```bash
make install-dev  # Install with dev dependencies
```

### Testing & Quality
```bash
make test         # pytest with coverage (requires 80%+ coverage)
make lint         # flake8 + mypy checks
make format       # black + isort auto-formatting
```

**Pre-commit checklist:**
1. Format code: `make format`
2. Run tests: `make test`
3. Check lint: `make lint`

### Release Process
**Version is synchronized across 3 files:** `pyproject.toml`, `setup.py`, `src/proxmox_cli/__init__.py`

```bash
# Automated release (recommended)
./scripts/release.sh patch|minor|major  # Bumps version, tests, builds, uploads to Test PyPI

# Manual steps
./scripts/bump_version.sh patch  # Uses bump-my-version
make test
./scripts/publish.sh test        # Test PyPI
./scripts/publish.sh prod        # Production PyPI
```

Never manually edit version numbers - always use `bump-my-version` or the scripts.

### Local CI Testing
```bash
make act-test     # Run tests workflow locally with act (Python 3.11/Ubuntu)
make act-publish  # Test publish workflow
make act-list     # List available workflows
```

## Code Conventions

### Import Organization (isort)
Order: stdlib → third-party → local. Example:
```python
import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success
```

### Error Handling
Always wrap API calls in try-except and respect output format:
```python
try:
    client = get_proxmox_client(ctx)
    result = client.api.nodes(node).qemu(vmid).status.get()
    print_success(f"Action completed")
except Exception as e:
    if ctx.obj.get("output_format", "json") == "json":
        print_json({"error": str(e)})
    else:
        print_error(f"Failed: {str(e)}")
```

### Configuration Precedence
1. CLI flags (`--host`, `--user`, etc.)
2. Config file (`~/.config/proxmox-cli/config.yaml`)
3. Defaults in `Config._default_config()`

SSL verification defaults to False for self-signed certs (common in Proxmox).

## Current Branch Context

Branch: `feature/lxcCtrTmpltManagement`
- Focus: LXC container template management (COMPLETED)
- Key features added:
  - List templates on storage: `container templates`
  - List downloadable templates: `container available-templates`
  - Download templates: `container download-template`
  - Create containers from templates: `container create`
- Modified files: 
  - `src/proxmox_cli/client.py` - Added template management methods
  - `src/proxmox_cli/commands/container.py` - Added template commands
  - Documentation: `docs/CONTAINER_TEMPLATES.md`, README.md updated

## Adding New Commands

1. Create command module in `src/proxmox_cli/commands/[resource].py`
2. Follow existing patterns (see `vm.py` or `container.py`)
3. Register in `src/proxmox_cli/cli.py`: `main.add_command(resource.resource)`
4. Add tests in `tests/test_cli.py`
5. Update README.md with usage examples

## Key Dependencies

- `click>=8.0.0` - CLI framework
- `proxmoxer>=2.0.0` - Proxmox API wrapper
- `rich>=13.0.0` - Terminal formatting (tables, colors)
- `pyyaml>=6.0` - Config file parsing
- `tabulate>=0.9.0` - Table formatting fallback

## Testing Notes

Tests use Click's `CliRunner` for CLI invocation. Most tests are integration-style:
```python
runner = CliRunner()
result = runner.invoke(main, ["vm", "--help"])
assert result.exit_code == 0
```

Real Proxmox API calls are not mocked in current test suite - tests verify CLI structure, not API behavior.
