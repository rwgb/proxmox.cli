# v0.4.2 - Storage Directory Creation Feature

## Release Date
November 13, 2025

## Overview
This release adds comprehensive support for creating and configuring Proxmox storage directories with flexible content type management. The new storage creation feature enables users to programmatically set up storage for various purposes including backups, ISOs, templates, VM disks, and custom scripts.

## What's New

### Features
- 🎯 **Storage Directory Creation** - Complete support for managing storage directories
  - Create storage via CLI: `storage create <storage-id> --path <path>`
  - Create storage via Python API: `client.create_storage(...)`
  - Support for 6 content types: images, rootdir, vztmpl, backup, iso, snippets
  - Shared storage flag for cluster configurations
  - Backup retention policies (maxfiles, prune-backups)
  - Node-specific storage configuration

### Commands Added
- `proxmox-cli storage create` - Create a new storage directory with flexible options

### Options
- `STORAGE_ID` (argument) - Unique storage identifier
- `--path` / `-p` (required) - Filesystem path on Proxmox host
- `--type` / `-t` - Storage type (default: dir)
- `--content` / `-c` - Content types (comma-separated)
- `--nodes` / `-n` - Cluster nodes (comma-separated)
- `--shared` / `--no-shared` - Mark storage as shared for clusters
- `--maxfiles` - Maximum number of backup files per VM
- `--prune-backups` - Backup retention options (e.g., 'keep-last=3,keep-weekly=2')

### Content Types Supported
| Type | Description | Use Case |
|------|-------------|----------|
| `images` | VM disk images (qcow2, raw, vmdk) | VM storage |
| `rootdir` | Container file systems | LXC containers |
| `vztmpl` | Container templates | LXC template storage |
| `backup` | Backup files | VM and container backups |
| `iso` | ISO images | Installation media |
| `snippets` | Custom scripts and configs | Hooks, cloud-init configs |

## Usage Examples

### Basic Backup Storage
```bash
proxmox-cli storage create backup-storage \
  --path /mnt/backups \
  --content backup
```

### ISO and Template Storage
```bash
proxmox-cli storage create iso-storage \
  --path /mnt/isos \
  --content "iso,vztmpl"
```

### Shared VM Disk Storage
```bash
proxmox-cli storage create vm-storage \
  --path /mnt/vms \
  --content "images,rootdir" \
  --shared
```

### Snippets Storage
```bash
proxmox-cli storage create snippets-storage \
  --path /mnt/snippets \
  --content snippets
```

### With Backup Retention Policy
```bash
proxmox-cli storage create backup-storage \
  --path /mnt/backups \
  --content backup \
  --maxfiles 10 \
  --prune-backups "keep-last=3,keep-weekly=2,keep-monthly=1"
```

### Node-Specific Storage
```bash
proxmox-cli storage create local-backup \
  --path /mnt/local-backup \
  --content backup \
  --nodes "node1,node2"
```

### Python API Usage
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

## Improvements
- Added comprehensive documentation in `docs/STORAGE_CREATE.md`
- Added quick reference guide in `docs/STORAGE_QUICKREF.md`
- Updated README.md with Storage Management section and examples
- Added implementation summary in `docs/STORAGE_FEATURE_SUMMARY.md`
- Code formatted according to Black standards

## Bug Fixes
- None in this release

## API Changes
- Added `ProxmoxClient.create_storage()` method with flexible parameter support

## Documentation
- Complete guide: `docs/STORAGE_CREATE.md` - Comprehensive documentation with all features
- Quick reference: `docs/STORAGE_QUICKREF.md` - Quick lookup guide
- README section: Storage Management examples and patterns
- Implementation summary: `docs/STORAGE_FEATURE_SUMMARY.md` - Technical details

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
- JSON (default) - Perfect for scripting
- Table - Human-readable output
- YAML - Configuration-friendly format
- Plain text - Minimal output

Example:
```bash
# JSON output (default)
proxmox-cli storage create test --path /mnt/test --content backup

# Table format
proxmox-cli --output table storage list

# YAML format
proxmox-cli --output yaml storage list
```

## Compatibility
- Proxmox VE 6.x and 7.x
- Python 3.8+
- All existing functionality remains backward compatible

## Known Limitations
- Currently supports directory (`dir`) storage type
- Future versions may add explicit support for other storage types (NFS, CIFS, LVM, ZFSPool, RBD)

## Installation
```bash
pip install proxmox-cli
```

## Migration Notes
- No breaking changes from v0.4.1
- Existing commands and APIs remain unchanged
- New `storage create` command is additive

## Testing
- All CLI commands tested and verified
- Comprehensive test coverage for storage commands
- Code formatting verified with Black
- Import sorting verified with isort

## Files Modified
- `src/proxmox_cli/client.py` - Added `create_storage()` method
- `src/proxmox_cli/commands/storage.py` - Added `create` command
- `tests/test_cli.py` - Added test cases
- `README.md` - Added Storage Management section
- `docs/STORAGE_CREATE.md` - New comprehensive documentation
- `docs/STORAGE_QUICKREF.md` - New quick reference guide
- `docs/STORAGE_FEATURE_SUMMARY.md` - New implementation summary

## Best Practices
1. **Separate Storage by Purpose** - Create dedicated storage for different content types
2. **Use Retention Policies** - Always configure retention policies for backup storage
3. **Mark Shared Storage** - Use `--shared` flag for cluster setups with shared storage (NFS, CIFS)
4. **Use Descriptive Names** - Choose clear, descriptive storage identifiers
5. **Verify Permissions** - Ensure the storage path exists and has proper permissions

## Troubleshooting

### Path doesn't exist
Ensure the path exists on the Proxmox host:
```bash
ssh root@proxmox-host "mkdir -p /mnt/new-storage"
```

### Permission denied
Set proper permissions on the directory:
```bash
ssh root@proxmox-host "chmod 755 /mnt/storage"
```

### Storage already exists
Check existing storage:
```bash
proxmox-cli storage list
```

## Related Commands
- `proxmox-cli storage list` - List all storage
- `proxmox-cli container templates` - List LXC templates on storage
- `proxmox-cli pool add-member` - Add storage to resource pool

## Contributors
- Ralph Brynard (@rwgb)

## Support
For issues, questions, or feature requests, please visit:
- GitHub Issues: https://github.com/rwgb/proxmox.cli/issues
- GitHub Discussions: https://github.com/rwgb/proxmox.cli/discussions

## Changelog
- **v0.4.2** - Storage directory creation feature
- **v0.4.1** - Previous release
- **v0.4.0** - Previous release

## Full Diff
Compare v0.4.1 to v0.4.2:
https://github.com/rwgb/proxmox.cli/compare/v0.4.1...v0.4.2

## Thank You
Thank you to all users and contributors for their feedback and support!
