# LXC Container Template Management

This guide explains how to manage LXC container templates with Proxmox CLI.

## Overview

LXC container templates are pre-configured system images that can be used to quickly create new containers. Proxmox supports downloading templates from official repositories and managing them on your storage.

## Commands

### List Templates on Storage

List all container templates currently stored on your Proxmox node:

```bash
# List all templates on all nodes
proxmox-cli container templates

# List templates on a specific node
proxmox-cli container templates --node pve1

# List templates from specific storage
proxmox-cli container templates --node pve1 --storage local
```

**Output includes:**
- Template name
- Storage location
- Node
- Size
- Volume ID (volid)

### List Available Templates for Download

View templates available for download from Proxmox repositories:

```bash
# List available templates
proxmox-cli container available-templates --node pve1
```

**Output includes:**
- Template name
- OS type
- Version
- Description
- Architecture
- Section/category

### Download a Template

Download a template from the repository to your storage:

```bash
# Download Ubuntu 22.04 template
proxmox-cli container download-template \
  ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --node pve1 \
  --storage local

# Download Debian 12 template
proxmox-cli container download-template \
  debian-12-standard_12.2-1_amd64.tar.zst \
  --node pve1 \
  --storage local
```

**Parameters:**
- `TEMPLATE` (required): Template name from available-templates list
- `--node, -n` (required): Node where to download the template
- `--storage, -s` (default: local): Storage where to save the template

**Note:** Template downloads run as background tasks. The command returns a task ID that can be monitored in the Proxmox web interface.

### Create Container from Template

Create a new LXC container using a downloaded template:

```bash
# Basic container creation
proxmox-cli container create 200 \
  local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --node pve1 \
  --hostname my-container \
  --password "MySecurePassword123"

# Advanced container with networking
proxmox-cli container create 201 \
  local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
  --node pve1 \
  --hostname web-server \
  --password "SecurePass123" \
  --storage local-lvm \
  --memory 2048 \
  --cores 4 \
  --rootfs-size 20 \
  --nameserver 8.8.8.8 \
  --searchdomain example.com \
  --net0 "name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1"
```

**Parameters:**
- `VMID` (required): Unique container ID (e.g., 100-999)
- `OSTEMPLATE` (required): Template volume ID (format: `storage:vztmpl/template-name.tar.zst`)
- `--node, -n` (required): Node where to create the container
- `--hostname`: Container hostname
- `--password`: Root password
- `--storage, -s` (default: local-lvm): Storage for container root filesystem
- `--memory, -m` (default: 512): Memory in MB
- `--cores, -c` (default: 1): Number of CPU cores
- `--rootfs-size` (default: 8): Root filesystem size in GB
- `--nameserver`: DNS nameserver IP
- `--searchdomain`: DNS search domain
- `--net0`: Network configuration (format: `name=eth0,bridge=vmbr0,ip=dhcp` or static IP)

## Template Naming Convention

Templates follow this naming pattern:
```
<os>-<version>-<type>_<release>-<build>_<arch>.tar.zst
```

Examples:
- `ubuntu-22.04-standard_22.04-1_amd64.tar.zst`
- `debian-12-standard_12.2-1_amd64.tar.zst`
- `alpine-3.18-default_20230607_amd64.tar.xz`
- `centos-9-stream-default_20230607_amd64.tar.xz`

## Volume ID Format

When creating containers, you need to specify the template using a volume ID:
```
<storage>:vztmpl/<template-filename>
```

Examples:
- `local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst`
- `nfs-storage:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst`

## Network Configuration

The `--net0` parameter accepts various network configurations:

### DHCP (automatic IP)
```bash
--net0 "name=eth0,bridge=vmbr0,ip=dhcp"
```

### Static IP
```bash
--net0 "name=eth0,bridge=vmbr0,ip=192.168.1.100/24,gw=192.168.1.1"
```

### IPv6
```bash
--net0 "name=eth0,bridge=vmbr0,ip=192.168.1.100/24,ip6=2001:db8::100/64,gw6=2001:db8::1"
```

## Complete Workflow Example

Here's a complete workflow for creating a container from scratch:

```bash
# 1. Check available templates for download
proxmox-cli container available-templates --node pve1 | grep ubuntu

# 2. Download Ubuntu 22.04 template
proxmox-cli container download-template \
  ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --node pve1 \
  --storage local

# Wait for download to complete (check in web UI or wait a few minutes)

# 3. Verify template is downloaded
proxmox-cli container templates --node pve1 --storage local

# 4. Create container from template
proxmox-cli container create 200 \
  local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --node pve1 \
  --hostname ubuntu-web \
  --password "MyPassword123" \
  --memory 1024 \
  --cores 2 \
  --rootfs-size 10 \
  --net0 "name=eth0,bridge=vmbr0,ip=dhcp"

# 5. Start the container
proxmox-cli container start 200 --node pve1

# 6. Verify container is running
proxmox-cli container list --node pve1
```

## Storage Types

Container templates can be stored on various storage types:
- **dir** - Directory-based storage
- **nfs** - NFS network storage
- **cifs** - CIFS/SMB network storage
- **glusterfs** - GlusterFS storage
- **zfspool** - ZFS pool

Most commonly, templates are stored on `local` storage (typically `/var/lib/vz/template/cache/` on the Proxmox host).

## Output Formats

All commands support multiple output formats:

```bash
# JSON output (default)
proxmox-cli container templates --node pve1

# Table format
proxmox-cli --output table container templates --node pve1

# YAML format
proxmox-cli --output yaml container templates --node pve1

# Plain text format
proxmox-cli --output plain container templates --node pve1
```

## Troubleshooting

### Template not found after download
Wait a few minutes for the download task to complete. Large templates can take several minutes. You can check task status in the Proxmox web interface under Tasks.

### "Permission denied" errors
Ensure your user has appropriate permissions:
- `VM.Allocate` - To create containers
- `Datastore.AllocateTemplate` - To download templates
- `Datastore.Audit` - To list templates

### Network configuration not working
Ensure:
1. The bridge (e.g., `vmbr0`) exists on the node
2. IP address is in correct CIDR notation (e.g., `192.168.1.100/24`)
3. Gateway is specified for static IPs

### Container fails to start after creation
Check:
1. Template was fully downloaded
2. Storage has enough space
3. Container configuration is valid
4. No conflicting VMID or hostname

## See Also

- [Proxmox VE Documentation - LXC](https://pve.proxmox.com/wiki/Linux_Container)
- [Container Management](../README.md#containers)
- [API Documentation](API.md)
