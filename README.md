# Proxmox CLI

A command-line interface tool for managing Proxmox Virtual Environment.

## Features

- Manage virtual machines and containers
- Monitor cluster resources
- Perform backup and restore operations
- Manage storage and networking
- User and permission management

## Installation

```bash
pip install -e .
```

## Usage

```bash
proxmox-cli --help
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
