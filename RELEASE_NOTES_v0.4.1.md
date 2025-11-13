# v0.4.1 - LXC Container Template Management

## What's New

### Features
- 🎯 **LXC Container Template Management** - Complete support for managing LXC container templates
  - List templates on storage: `container templates`
  - List downloadable templates: `container available-templates`
  - Download templates: `container download-template`
  - Create containers from templates: `container create`

### Improvements
- Added comprehensive documentation in `docs/CONTAINER_TEMPLATES.md`
- Updated README with template management examples
- Added AI Copilot instructions for better development experience

### Bug Fixes
- Fixed CI/CD pipeline dependency installation issues
- Resolved merge conflicts in version files

### Documentation
- Complete guide for LXC container template workflows
- Network configuration examples (DHCP and static IP)
- Troubleshooting section

## Installation

```bash
pip install proxmox-cli
```

## Example Usage

```bash
# List available templates for download
proxmox-cli container available-templates --node pve1

# Download a template
proxmox-cli container download-template ubuntu-22.04-standard_22.04-1_amd64.tar.zst --node pve1

# Create container from template
proxmox-cli container create 200 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst --node pve1 --hostname web-server
```

**Full Changelog**: https://github.com/rwgb/proxmox.cli/compare/v0.3.0...v0.4.1
