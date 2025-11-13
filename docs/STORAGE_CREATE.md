# Storage Creation Feature

## Overview

The Proxmox CLI now supports creating directory-based storage with flexible content type configurations. This feature allows you to programmatically set up storage for various purposes including backups, ISOs, templates, VM disks, and custom scripts.

## Features

- Create directory storage with custom paths
- Support for multiple content types
- Configure shared storage for clusters
- Set backup retention policies
- Node-specific or cluster-wide storage

## Content Types

Proxmox storage supports different content types:

| Content Type | Description | Use Case |
|--------------|-------------|----------|
| `images` | VM disk images (qcow2, raw, vmdk) | VM storage |
| `rootdir` | Container file systems | LXC containers |
| `vztmpl` | Container templates | LXC template storage |
| `backup` | Backup files | VM and container backups |
| `iso` | ISO images | Installation media |
| `snippets` | Custom scripts and configs | Hooks, cloud-init configs |

## Usage Examples

### Basic Backup Storage

Create a simple directory storage for backups:

```bash
proxmox-cli storage create backup-storage \
  --path /mnt/backups \
  --content backup
```

### ISO and Template Storage

Store ISOs and LXC templates together:

```bash
proxmox-cli storage create iso-storage \
  --path /mnt/isos \
  --content "iso,vztmpl"
```

### VM Disk Storage (Shared)

Create shared storage for VM disks in a cluster:

```bash
proxmox-cli storage create vm-storage \
  --path /mnt/vms \
  --content "images,rootdir" \
  --shared
```

### Snippets Storage

Storage for custom scripts and cloud-init configurations:

```bash
proxmox-cli storage create snippets-storage \
  --path /mnt/snippets \
  --content snippets
```

### Backup Storage with Retention

Configure backup storage with automatic retention policies:

```bash
proxmox-cli storage create backup-storage \
  --path /mnt/backups \
  --content backup \
  --maxfiles 10 \
  --prune-backups "keep-last=3,keep-weekly=2,keep-monthly=1"
```

### Node-Specific Storage

Create storage on specific nodes only:

```bash
proxmox-cli storage create local-backup \
  --path /mnt/local-backup \
  --content backup \
  --nodes "node1,node2"
```

### Multi-Purpose Storage

Combine multiple content types:

```bash
proxmox-cli storage create general-storage \
  --path /mnt/general \
  --content "backup,iso,vztmpl,snippets"
```

## Command Options

### Required Options

- `STORAGE_ID` - Unique identifier for the storage (argument)
- `--path` / `-p` - Path on the filesystem where storage is located

### Optional Options

- `--type` / `-t` - Storage type (default: `dir`)
- `--content` / `-c` - Content types (comma-separated)
- `--nodes` / `-n` - Comma-separated list of cluster nodes
- `--shared` - Mark storage as shared (for clusters)
- `--maxfiles` - Maximum number of backup files per VM
- `--prune-backups` - Backup retention options

## Backup Retention Options

The `--prune-backups` option supports various retention policies:

- `keep-last=N` - Keep last N backups
- `keep-hourly=N` - Keep N hourly backups
- `keep-daily=N` - Keep N daily backups
- `keep-weekly=N` - Keep N weekly backups
- `keep-monthly=N` - Keep N monthly backups
- `keep-yearly=N` - Keep N yearly backups

Example:
```bash
--prune-backups "keep-last=5,keep-weekly=4,keep-monthly=6"
```

## Output Formats

All commands support multiple output formats:

### JSON (Default)

```bash
proxmox-cli storage create my-storage --path /mnt/storage --content backup
```

Output:
```json
{
  "success": true,
  "storage": "my-storage",
  "path": "/mnt/storage"
}
```

### Table Format

```bash
proxmox-cli --output table storage list
```

### YAML Format

```bash
proxmox-cli --output yaml storage list
```

## Storage Types

While the CLI currently focuses on directory (`dir`) storage, the underlying API supports:

- `dir` - Directory on local filesystem
- `nfs` - NFS network storage
- `cifs` - CIFS/SMB network storage
- `lvm` - LVM volume group
- `zfspool` - ZFS pool
- `rbd` - Ceph RBD storage

Future versions may add explicit support for these types.

## Best Practices

### 1. Separate Storage by Purpose

Create dedicated storage for different purposes:

```bash
# Backup storage
proxmox-cli storage create backups --path /mnt/backups --content backup

# ISO storage
proxmox-cli storage create isos --path /mnt/isos --content iso

# Template storage
proxmox-cli storage create templates --path /mnt/templates --content vztmpl
```

### 2. Use Retention Policies for Backups

Always configure retention policies for backup storage:

```bash
proxmox-cli storage create backups \
  --path /mnt/backups \
  --content backup \
  --prune-backups "keep-last=7,keep-weekly=4,keep-monthly=6"
```

### 3. Mark Shared Storage Appropriately

For cluster setups with shared storage (NFS, CIFS):

```bash
proxmox-cli storage create shared-storage \
  --path /mnt/nfs/shared \
  --content "images,rootdir" \
  --shared
```

### 4. Use Descriptive Names

Choose clear, descriptive storage identifiers:

```bash
# Good
proxmox-cli storage create prod-vm-backups --path /mnt/prod-backups --content backup

# Avoid
proxmox-cli storage create storage1 --path /mnt/data --content backup
```

## Programmatic Usage

Use the Python API for scripting:

```python
from proxmox_cli.client import ProxmoxClient

client = ProxmoxClient(
    host="proxmox.example.com",
    user="root@pam",
    password="password",
    verify_ssl=False
)

# Create backup storage
client.create_storage(
    storage_id="backup-storage",
    storage_type="dir",
    path="/mnt/backups",
    content="backup",
    maxfiles=10
)

# Create shared VM storage
client.create_storage(
    storage_id="vm-storage",
    storage_type="dir",
    path="/mnt/vms",
    content="images,rootdir",
    shared=1
)
```

## Troubleshooting

### Permission Errors

Ensure the path exists and has proper permissions:

```bash
# On the Proxmox host
sudo mkdir -p /mnt/backups
sudo chmod 755 /mnt/backups
```

### Storage Already Exists

If you get an error that storage already exists, list current storage:

```bash
proxmox-cli storage list
```

### Path Not Found

The path must exist on the Proxmox host before creating storage:

```bash
# Create directory on host first
ssh root@proxmox-host "mkdir -p /mnt/new-storage"

# Then create storage in Proxmox
proxmox-cli storage create new-storage --path /mnt/new-storage --content backup
```

## Related Commands

- `proxmox-cli storage list` - List all storage
- `proxmox-cli container templates` - List LXC templates on storage
- `proxmox-cli pool add-member --storage` - Add storage to resource pool

## API Reference

The storage create functionality uses the Proxmox VE API endpoint:

```
POST /api2/json/storage
```

Parameters:
- `storage` - Storage identifier
- `type` - Storage type
- `path` - Storage path
- `content` - Content types
- `nodes` - Node list
- `shared` - Shared flag (0 or 1)
- `maxfiles` - Maximum backup files
- `prune-backups` - Retention options

For more information, see the [Proxmox VE API documentation](https://pve.proxmox.com/pve-docs/api-viewer/).
