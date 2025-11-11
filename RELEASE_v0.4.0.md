## 🎉 Release v0.4.0 - Resource Pool Management

This release adds comprehensive resource pool management capabilities to proxmox-cli, enabling better organization and grouping of Proxmox resources.

### ✨ New Features

**Resource Pool Management Commands**
- `pool list` - List all resource pools in your Proxmox environment
- `pool create` - Create new resource pools with optional descriptions
- `pool delete` - Remove resource pools
- `pool update` - Update pool information and metadata
- `pool show` - Display detailed pool information including all members
- `pool add-member` - Add VMs and storage to resource pools (supports multiple resources)
- `pool remove-member` - Remove VMs and storage from resource pools

### 🚀 Enhancements

- **API Client Methods**: Added 7 new methods to `ProxmoxClient` for pool operations
- **Batch Operations**: Support for adding/removing multiple VMs and storage in a single command
- **Consistent Integration**: Full integration with existing CLI patterns and output formats (JSON, table, YAML, plain)
- **Comprehensive Documentation**: Updated README with usage examples and command references

### 📚 Usage Examples

```bash
# List all resource pools
proxmox-cli pool list

# Create a production pool
proxmox-cli pool create production --comment "Production environment resources"

# Add multiple VMs to a pool
proxmox-cli pool add-member production --vm 100 --vm 101 --vm 102

# Add storage to a pool
proxmox-cli pool add-member production --storage local-lvm

# View pool details and members
proxmox-cli pool show production

# Remove a VM from the pool
proxmox-cli pool remove-member production --vm 100
```

### 📦 Installation

```bash
pip install --upgrade proxmox-cli
```

### 🔗 Links

- [Full Changelog](https://github.com/rwgb/proxmox.cli/compare/v0.3.0...v0.4.0)
- [Documentation](https://github.com/rwgb/proxmox.cli#resource-pool-management)

### 💡 Why Resource Pools?

Resource pools allow you to organize and manage related VMs, containers, and storage together, making it easier to:
- Group resources by project, environment, or team
- Apply permissions at the pool level
- Manage resources as logical units
- Improve organization in large Proxmox deployments
