# Image (VM Template) Management

The `image` command group provides management for VM templates (also known as images) in your Proxmox cluster.

## Overview

VM templates are pre-configured virtual machines that serve as blueprints for creating new VMs quickly. In Proxmox, templates are created by converting existing VMs into read-only templates that can be cloned.

## Commands

### `image list`

List all VM templates available in the Proxmox cluster.

**Usage:**

```bash
proxmox-cli image list [OPTIONS]
```

**Options:**

- `--node`, `-n`: Filter templates by node name

**Examples:**

```bash
# List all templates across all nodes
proxmox-cli image list

# List templates on a specific node
proxmox-cli image list --node skullcanyon

# List templates with table output
proxmox-cli --output table image list
```

**Output Format:**

```json
[
  {
    "vmid": 107,
    "name": "debian12base",
    "node": "skullcanyon",
    "disk": "5.00GB",
    "memory": "1.00GB",
    "cpu": "1 cores"
  },
  {
    "vmid": 9000,
    "name": "ubuntu-22.04-template",
    "node": "skullcanyon",
    "disk": "32.00GB",
    "memory": "2.00GB",
    "cpu": "2 cores"
  }
]
```

**Fields:**

- `vmid`: Virtual Machine ID of the template
- `name`: Template name
- `node`: Proxmox node where the template is located
- `disk`: Total disk size allocated to the template
- `memory`: Memory allocated to the template
- `cpu`: Number of CPU cores assigned to the template

### `image info`

Show detailed information about a specific VM template.

**Usage:**

```bash
proxmox-cli image info VMID [OPTIONS]
```

**Arguments:**

- `VMID`: The VM template ID to get information about (required)

**Options:**

- `--node`, `-n`: Node name where template is located (optional, will auto-discover if not specified)

**Examples:**

```bash
# Get detailed info about template 107 (auto-discover node)
proxmox-cli image info 107

# Get detailed info with node specified
proxmox-cli image info 107 --node skullcanyon

# Get info with table output
proxmox-cli --output table image info 107
```

**Output Format:**

```json
{
  "vmid": 107,
  "name": "debian12base",
  "node": "skullcanyon",
  "template": true,
  "description": "Packer ephemeral build VM",
  "ostype": "other",
  "cpu": {
    "cores": 1,
    "sockets": 1,
    "total": 1
  },
  "memory": "1.00GB",
  "memory_mb": 1024,
  "networks": [
    {
      "interface": "net0",
      "config": "e1000=5A:F0:9F:B4:45:12,bridge=vmbr0",
      "e1000": "5A:F0:9F:B4:45:12",
      "bridge": "vmbr0"
    }
  ],
  "disks": [
    {
      "interface": "scsi0",
      "config": "local-lvm:base-107-disk-0,cache=none,replicate=0,size=5G",
      "storage": "local-lvm",
      "size": "5G"
    }
  ],
  "total_disk_size": "5.00GB",
  "boot_order": "order=scsi0;net0",
  "qemu_agent": "1"
}
```

**Fields:**

- `vmid`: Virtual Machine ID
- `name`: Template name
- `node`: Proxmox node location
- `template`: Always true for templates
- `description`: Template description
- `ostype`: Operating system type (l26, win10, etc.)
- `cpu`: CPU configuration (cores, sockets, total)
- `memory`: Memory allocation in GB
- `memory_mb`: Memory in MB
- `networks`: Network interface configurations
- `disks`: Disk configurations with storage and size
- `total_disk_size`: Total disk space allocated
- `boot_order`: Boot device order
- `qemu_agent`: QEMU guest agent status
- `bios`: BIOS type (if configured)
- `machine`: Machine type (if configured)

**Error Cases:**

```bash
# Non-existent template
$ proxmox-cli image info 9999
{"error": "Template with VMID 9999 not found"}

# VM is not a template
$ proxmox-cli image info 101 --node skullcanyon
{"error": "VM 101 is not a template"}
```

## Common Workflows

### 1. Finding and Inspecting Templates Before Cloning

```bash
# Step 1: List available templates
proxmox-cli image list

# Step 2: Get detailed information about a specific template
proxmox-cli image info 107

# Step 3: Clone from the template
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 107 \
  --new-vmid 200 \
  --name "my-new-server"
```

### 2. Checking Template Resources

```bash
# View template specifications before cloning
proxmox-cli image info 107

# This helps you understand:
# - How much disk space the cloned VM will need
# - Memory requirements
# - CPU allocation
# - Network configuration
# - Installed software (from description)
```

### 3. Comparing Multiple Templates

```bash
# List all available templates
proxmox-cli image list

# Compare specific templates in detail
proxmox-cli image info 107  # Debian 12 template
proxmox-cli image info 9000  # Ubuntu 22.04 template

# Choose the best template for your needs
```

### 4. Multi-Node Template Discovery

```bash
# Find all templates across the cluster
proxmox-cli image list

# Get details about a template (auto-discovers node)
proxmox-cli image info 107

# Or specify node if known
proxmox-cli image info 107 --node skullcanyon
```

## Integration with VM Commands

The `image` command is designed to work seamlessly with `vm` commands:

```bash
# 1. List available templates
proxmox-cli image list

# 2. Get detailed template information
proxmox-cli image info 107

# 3. Clone the template
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 107 \
  --new-vmid 200 \
  --name "web-server-01" \
  --start

# 4. Check the new VM status
proxmox-cli vm status 200 --node skullcanyon
```

**Typical Workflow:**

```bash
# Discovery phase
proxmox-cli image list                    # Find all templates
proxmox-cli image info 107                # Inspect template details

# Provisioning phase  
proxmox-cli vm clone \                    # Clone template
  --source-vmid 107 \
  --new-vmid 200 \
  --name "prod-app-01" \
  --full \
  --start

# Management phase
proxmox-cli vm list                       # List all VMs
proxmox-cli vm status 200 --node skullcanyon  # Check VM status
```

## Best Practices

### Template Organization

1. **Use meaningful names**: Name templates descriptively (e.g., `ubuntu-22.04-docker`, `debian12-base`, `windows-server-2019`)

2. **VMID ranges**: Reserve VMID ranges for templates
   - Templates: 9000-9999
   - VMs: 100-8999

3. **Keep templates minimal**: Templates should contain only necessary software to reduce disk usage

4. **Document templates**: Use descriptions to note what's installed
   ```bash
   # View template description
   proxmox-cli image info 107 | jq '.description'
   ```

### Template Discovery

- Use `proxmox-cli image list` to find available templates before creating VMs
- Use `proxmox-cli image info <vmid>` to inspect template details and specifications
- Check template resources (disk, memory, CPU) to ensure they meet your requirements
- Review network and disk configurations before cloning
- Filter by node to find templates on specific storage

### Performance

- Templates stored on fast storage (SSD/NVMe) enable faster cloning
- Linked clones are faster and use less space but depend on the template
- Full clones are slower but create independent VMs

## Future Commands (Planned)

The following commands are planned for future releases:

- ~~`image info <vmid>`~~ - ✅ **Implemented** - Show detailed template information
- `image create <vmid>` - Convert a VM into a template
- `image delete <vmid>` - Delete a template
- `image clone <vmid>` - Quick template cloning (alias for `vm clone`)
- `image export <vmid>` - Export template as OVA/backup
- `image import <file>` - Import template from file

## Differences from VM Commands

### `image list` vs `vm list --templates-only`

Both commands show templates, but with different purposes:

- **`image list`**: Dedicated command for template management
  - Shows template-specific information (disk, memory, CPU specs)
  - Cleaner output focused on template discovery
  - Designed for finding templates to clone

- **`vm list --templates-only`**: VM-centric view
  - Shows runtime information (status, CPU usage, uptime)
  - Useful when managing templates as VMs
  - Shows current resource usage

**When to use which:**

- Use `image list` when **selecting a template to clone**
- Use `vm list --templates-only` when **managing template VMs** (start/stop/modify)

### Example Comparison

```bash
# Finding a template to clone
$ proxmox-cli image list
[
  {
    "vmid": 107,
    "name": "debian12base",
    "node": "skullcanyon",
    "disk": "5.00GB",    # What you'll get when you clone
    "memory": "1.00GB",  # Template specs
    "cpu": "1 cores"
  }
]

# Managing template VMs
$ proxmox-cli vm list --templates-only
[
  {
    "vmid": 107,
    "name": "debian12base",
    "status": "stopped",      # Current state
    "cpu": "0.00%",          # Current usage
    "memory": "0.00GB / 1.00GB",
    "uptime": "0d 0h",
    "template": "yes"
  }
]
```

## See Also

- [VM Create and Clone Documentation](VM_CREATE_CLONE.md)
- `proxmox-cli vm --help` - VM management commands
- `proxmox-cli vm clone --help` - Clone VMs from templates
- `proxmox-cli vm list --help` - List VMs and templates
