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

## Common Workflows

### 1. Finding Templates for Cloning

```bash
# List available templates
proxmox-cli image list

# Clone from a template
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 107 \
  --new-vmid 200 \
  --name "my-new-server"
```

### 2. Checking Template Resources

```bash
# View template specifications before cloning
proxmox-cli image list --node skullcanyon

# This helps you understand:
# - How much disk space the cloned VM will need
# - Memory requirements
# - CPU allocation
```

### 3. Multi-Node Template Discovery

```bash
# Find all templates across the cluster
proxmox-cli image list

# Find templates on specific node
proxmox-cli image list --node node1
proxmox-cli image list --node node2
```

## Integration with VM Commands

The `image` command is designed to work seamlessly with `vm` commands:

```bash
# 1. List available templates
proxmox-cli image list

# 2. Get template details (VMID 107)
proxmox-cli vm status 107 --node skullcanyon

# 3. Clone the template
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 107 \
  --new-vmid 200 \
  --name "web-server-01" \
  --start
```

## Best Practices

### Template Organization

1. **Use meaningful names**: Name templates descriptively (e.g., `ubuntu-22.04-docker`, `debian12-base`, `windows-server-2019`)

2. **VMID ranges**: Reserve VMID ranges for templates
   - Templates: 9000-9999
   - VMs: 100-8999

3. **Keep templates minimal**: Templates should contain only necessary software to reduce disk usage

4. **Document templates**: Use descriptions to note what's installed (see future `image info` command)

### Template Discovery

- Use `proxmox-cli image list` to find available templates before creating VMs
- Check template resources to ensure they meet your requirements
- Filter by node to find templates on specific storage

### Performance

- Templates stored on fast storage (SSD/NVMe) enable faster cloning
- Linked clones are faster and use less space but depend on the template
- Full clones are slower but create independent VMs

## Future Commands (Planned)

The following commands are planned for future releases:

- `image info <vmid>` - Show detailed template information
- `image create <vmid>` - Convert a VM into a template
- `image delete <vmid>` - Delete a template
- `image clone <vmid>` - Quick template cloning (alias for `vm clone`)

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
