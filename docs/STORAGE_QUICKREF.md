# Storage Create - Quick Reference

## Command Syntax

```bash
proxmox-cli storage create <STORAGE_ID> --path <PATH> [OPTIONS]
```

## Required Arguments

- `STORAGE_ID` - Unique storage identifier

## Required Options

- `--path` / `-p` - Filesystem path on Proxmox host

## Common Options

| Option | Short | Description |
|--------|-------|-------------|
| `--type` | `-t` | Storage type (default: dir) |
| `--content` | `-c` | Content types (comma-separated) |
| `--nodes` | `-n` | Cluster nodes (comma-separated) |
| `--shared` | | Mark as shared storage |
| `--maxfiles` | | Max backup files per VM |
| `--prune-backups` | | Backup retention rules |

## Content Types

| Type | Usage |
|------|-------|
| `backup` | VM/container backups |
| `iso` | Installation ISO images |
| `vztmpl` | LXC container templates |
| `images` | VM disk images |
| `rootdir` | Container filesystems |
| `snippets` | Custom scripts/configs |

## Quick Examples

### Backup Storage
```bash
proxmox-cli storage create backups --path /mnt/backups --content backup
```

### ISO Storage
```bash
proxmox-cli storage create isos --path /mnt/isos --content iso
```

### Template Storage
```bash
proxmox-cli storage create templates --path /mnt/templates --content vztmpl
```

### VM Storage (Shared)
```bash
proxmox-cli storage create vms --path /mnt/vms --content "images,rootdir" --shared
```

### With Retention
```bash
proxmox-cli storage create backups \
  --path /mnt/backups \
  --content backup \
  --prune-backups "keep-last=7,keep-weekly=4"
```

## Output Format

```bash
# JSON (default)
proxmox-cli storage create test --path /mnt/test --content backup

# Table
proxmox-cli --output table storage list

# YAML
proxmox-cli --output yaml storage list
```

## Common Patterns

### Development Environment
```bash
proxmox-cli storage create dev-backups --path /mnt/dev/backups --content backup
proxmox-cli storage create dev-isos --path /mnt/dev/isos --content "iso,vztmpl"
```

### Production Cluster
```bash
proxmox-cli storage create prod-vms \
  --path /mnt/nfs/vms \
  --content "images,rootdir" \
  --shared

proxmox-cli storage create prod-backups \
  --path /mnt/nfs/backups \
  --content backup \
  --shared \
  --prune-backups "keep-last=3,keep-weekly=4,keep-monthly=12"
```

### Node-Specific
```bash
proxmox-cli storage create node1-local \
  --path /mnt/local \
  --content backup \
  --nodes "node1"
```

## Troubleshooting

### Path doesn't exist
```bash
# Create on Proxmox host first
ssh root@proxmox-host "mkdir -p /mnt/new-storage"
```

### Permission denied
```bash
# Set proper permissions on host
ssh root@proxmox-host "chmod 755 /mnt/storage"
```

### Storage already exists
```bash
# Check existing storage
proxmox-cli storage list
```

## Related Commands

```bash
# List all storage
proxmox-cli storage list

# List templates on storage
proxmox-cli container templates --storage <storage-id>

# Add storage to pool
proxmox-cli pool add-member <pool> --storage <storage-id>
```

## Documentation

- Full guide: `docs/STORAGE_CREATE.md`
- README examples: Storage Management section
- API docs: `docs/API.md`
