# Proxmox CLI API Documentation

## Overview

The Proxmox CLI provides a Python API that can be used programmatically in addition to the command-line interface.

## Core Components

### ProxmoxClient

The main client for interacting with Proxmox API.

```python
from proxmox_cli.client import ProxmoxClient

client = ProxmoxClient(
    host="proxmox.example.com",
    user="root@pam",
    password="your-password",
    verify_ssl=False
)

# Get cluster nodes
nodes = client.get_nodes()

# Get virtual machines
vms = client.get_vms()

# Get containers
containers = client.get_containers()
```

### Configuration

Manage configuration programmatically:

```python
from proxmox_cli.config import Config

config = Config()
config.set("proxmox.host", "proxmox.example.com")
config.set("proxmox.user", "root@pam")
config.save()

# Read values
host = config.get("proxmox.host")
```

### Output Formatting

Format output data:

```python
from proxmox_cli.utils.output import print_table, print_success, format_output
from proxmox_cli.utils.output import OutputFormat

# Print as table
print_table(data, title="My Data")

# Print success message
print_success("Operation completed")

# Format data
json_output = format_output(data, OutputFormat.JSON)
```

### Utilities

Helper functions:

```python
from proxmox_cli.utils.helpers import (
    validate_vmid,
    validate_ip,
    format_size,
    format_uptime
)

# Validate VM ID
is_valid = validate_vmid("100")

# Format size
size_str = format_size(1073741824)  # "1.00 GB"

# Format uptime
uptime_str = format_uptime(86400)  # "1d"
```

## Examples

### List All VMs Across Cluster

```python
from proxmox_cli.client import ProxmoxClient

client = ProxmoxClient(
    host="proxmox.example.com",
    user="root@pam",
    password="password"
)

vms = client.get_vms()
for vm in vms:
    print(f"VM {vm['vmid']}: {vm['name']} - Status: {vm['status']}")
```

### Start a VM

```python
client.api.nodes("node1").qemu("100").status.start.post()
```

### Get Node Status

```python
status = client.api.nodes("node1").status.get()
print(f"CPU: {status['cpu']}, Memory: {status['memory']}")
```
