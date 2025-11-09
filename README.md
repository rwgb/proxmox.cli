# Proxmox CLI

[![PyPI version](https://badge.fury.io/py/proxmox-cli.svg)](https://badge.fury.io/py/proxmox-cli)
[![Python versions](https://img.shields.io/pypi/pyversions/proxmox-cli.svg)](https://pypi.org/project/proxmox-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful command-line interface tool for managing Proxmox Virtual Environment with support for VMs, containers, users, groups, roles, and permissions.

## Features

### Infrastructure Management
- 🖥️ **Virtual Machines** - Create, start, stop, and manage VMs
- 📦 **LXC Containers** - Full container lifecycle management
- 🔧 **Nodes** - Monitor and manage cluster nodes
- 💾 **Storage** - Storage configuration and monitoring
- 🗂️ **Resource Pools** - Organize and manage resource pools

### Identity & Access Management (IAM)
- 👤 **Users** - Create, update, and manage users
- 👥 **Groups** - Organize users into groups
- 🔐 **Roles** - Define custom roles with specific privileges
- 🔑 **API Tokens** - Generate and manage API tokens
- 🛡️ **ACLs** - Granular permission management

### Output & Configuration
- 📊 **Multiple Output Formats** - JSON (default), Table, YAML, Plain text
- ⚙️ **Configuration File** - Store credentials and preferences
- 🔒 **SSL Control** - Flexible SSL verification options
- 🚀 **Fast & Efficient** - Optimized for automation and scripting

## Installation

### From PyPI (Recommended)

```bash
pip install proxmox-cli
```

### From Source

```bash
git clone https://github.com/rwgb/proxmox.cli.git
cd proxmox.cli
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```bash
# List all VMs (JSON output by default)
proxmox-cli vm list

# List containers in table format
proxmox-cli --output table container list

# List users
proxmox-cli user list

# Show help
proxmox-cli --help
```

### Configuration

Create a configuration file at `~/.config/proxmox-cli/config.yaml`:

```yaml
proxmox:
  host: proxmox.example.com
  user: root@pam
  password: your-password
  # Or use API token
  # token_name: mytoken
  # token_value: your-token-value
  verify_ssl: false

output:
  format: json  # or table, yaml, plain
```

## Usage Examples

### Virtual Machines

```bash
# List all VMs
proxmox-cli vm list

# List VMs on specific node
proxmox-cli vm list --node pve1

# Start a VM
proxmox-cli vm start 100 --node pve1

# Stop a VM
proxmox-cli vm stop 100 --node pve1

# Get VM status
proxmox-cli vm status 100 --node pve1
```

### Containers

```bash
# List all containers
proxmox-cli container list

# Start a container
proxmox-cli container start 108 --node pve1

# Stop a container
proxmox-cli container stop 108 --node pve1
```

### User Management

```bash
# List all users
proxmox-cli user list

# Create a new user
proxmox-cli user create developer@pve \
  --password "SecurePass123" \
  --email "dev@example.com" \
  --groups "developers"

# Update user
proxmox-cli user update developer@pve --email "newemail@example.com"

# Delete user
proxmox-cli user delete developer@pve
```

### Role & Permission Management

```bash
# List all roles
proxmox-cli role list

# Create custom role
proxmox-cli role create CustomRole \
  --privs "VM.Allocate,VM.Audit,VM.PowerMgmt"

# Grant permissions
proxmox-cli acl add \
  --path "/" \
  --roles "PVEAdmin" \
  --users "admin@pve"
```

### API Tokens

```bash
# List tokens for a user
proxmox-cli token list user@pve

# Create API token
proxmox-cli token create user@pve mytoken \
  --comment "Automation token" \
  --no-privsep

# Delete token
proxmox-cli token delete user@pve mytoken
```

### Resource Pool Management

```bash
# List all resource pools
proxmox-cli pool list

# Create a new resource pool
proxmox-cli pool create production \
  --comment "Production environment resources"

# Show pool details and members
proxmox-cli pool show production

# Add VMs to a pool
proxmox-cli pool add-member production \
  --vm 100 --vm 101 --vm 102

# Add storage to a pool
proxmox-cli pool add-member production \
  --storage local-lvm

# Remove members from a pool
proxmox-cli pool remove-member production \
  --vm 100

# Update pool information
proxmox-cli pool update production \
  --comment "Updated production pool"

# Delete a pool
proxmox-cli pool delete production
```

## Output Formats

The CLI supports multiple output formats:

```bash
# JSON (default) - Perfect for scripting
proxmox-cli vm list

# Table - Human-readable
proxmox-cli --output table vm list

# YAML - Configuration-friendly
proxmox-cli --output yaml user list

# Plain text - Minimal
proxmox-cli --output plain node list
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 src/
black src/
```

## Configuration

Create a configuration file at `~/.config/proxmox-cli/config.yaml`:

```yaml
proxmox:
  host: your-proxmox-host
  user: root@pam
  verify_ssl: false
```

## License

MIT
