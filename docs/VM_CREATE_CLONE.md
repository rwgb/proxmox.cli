# VM Creation and Cloning Feature

This document describes the VM creation, cloning, and template management functionality in proxmox-cli.

## Features

### 1. List Templates (`vm templates`)

List all VM templates available in your Proxmox cluster.

### 2. Create VM (`vm create`)

Create a new virtual machine from scratch with customizable specifications.

### 3. Clone VM (`vm clone`)

Clone an existing VM or template to create a new VM (supports both full and linked clones).

## Usage Examples

### Listing Templates

```bash
# List all templates
proxmox-cli vm templates

# List templates on a specific node
proxmox-cli vm templates --node skullcanyon

# List only templates (alternative using list command)
proxmox-cli vm list --templates-only --node skullcanyon
```

**Example Output:**

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

### Creating a New VM

#### Basic VM Creation

```bash
# Create a basic Linux VM
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 200 \
  --name "ubuntu-server" \
  --memory 4096 \
  --cores 4

# Create a Windows VM with ISO
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 201 \
  --name "windows-server-2019" \
  --memory 8192 \
  --cores 4 \
  --disk-size 100G \
  --iso "windows-server-2019.iso" \
  --ostype win10 \
  --start
```

#### Advanced VM Creation

```bash
# Create VM with custom network and storage
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 202 \
  --name "database-server" \
  --memory 16384 \
  --cores 8 \
  --sockets 2 \
  --disk-size 500G \
  --storage local-lvm \
  --network-bridge vmbr0 \
  --network-model virtio \
  --ostype l26
```

### Cloning VMs

#### Clone from Template (Linked Clone)

```bash
# Create a linked clone from template (fast, uses less space)
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 210 \
  --name "web-server-01"

# Clone and start immediately
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 211 \
  --name "web-server-02" \
  --start
```

#### Full Clone

```bash
# Create a full clone (independent copy)
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 100 \
  --new-vmid 220 \
  --name "backup-server" \
  --full

# Clone to different node and storage
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 100 \
  --new-vmid 221 \
  --name "remote-server" \
  --target-node hades \
  --storage remote-storage \
  --full
```

#### Clone with Additional Options

```bash
# Clone with description and pool assignment
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 230 \
  --name "production-app-01" \
  --description "Production application server" \
  --pool production-pool \
  --full \
  --start
```

## Command Reference

### `vm templates`

List all VM templates in the Proxmox cluster.

**Optional Options:**
- `--node`, `-n`: Filter by node name

**Examples:**

```bash
# List all templates across all nodes
proxmox-cli vm templates

# List templates on a specific node
proxmox-cli vm templates --node skullcanyon
```

**Output:** Returns template information including VMID, name, node, disk size, memory, and CPU cores.

### `vm list`

List all virtual machines (with optional template filtering).

**Optional Options:**
- `--node`, `-n`: Filter by node name
- `--templates-only`: Show only VM templates

**Examples:**

```bash
# List all VMs
proxmox-cli vm list

# List VMs on specific node
proxmox-cli vm list --node skullcanyon

# List only templates
proxmox-cli vm list --templates-only
```

**Note:** Regular VMs and templates are shown in the list. Templates are indicated with a `"template": "yes"` field.

### `vm create`

Create a new virtual machine.

**Required Options:**
- `--node`, `-n`: Node name where VM will be created
- `--vmid`: VM ID (must be unique across the cluster)
- `--name`: VM name

**Optional Options:**
- `--memory`, `-m`: Memory in MB (default: 2048)
- `--cores`, `-c`: Number of CPU cores (default: 2)
- `--sockets`, `-s`: Number of CPU sockets (default: 1)
- `--disk-size`, `-d`: Disk size with unit (default: "32G")
- `--storage`: Storage for disk (default: "local-lvm")
- `--iso`: ISO image name for installation
- `--ostype`: OS type (default: "l26" for Linux 2.6+)
  - `l26`: Linux 2.6+ Kernel
  - `l24`: Linux 2.4 Kernel
  - `win10`: Windows 10/2016/2019
  - `win8`: Windows 8/2012
  - `win7`: Windows 7/2008
  - `wxp`: Windows XP/2003
  - `other`: Other OS
- `--network-bridge`: Network bridge (default: "vmbr0")
- `--network-model`: Network card model (default: "virtio")
  - `virtio`: VirtIO (paravirtualized)
  - `e1000`: Intel E1000
  - `rtl8139`: Realtek RTL8139
- `--start`: Start VM after creation

**Examples:**

```bash
# Minimal VM
proxmox-cli vm create --node skullcanyon --vmid 100 --name test-vm

# Production-ready VM
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 101 \
  --name prod-web-01 \
  --memory 8192 \
  --cores 4 \
  --disk-size 100G \
  --storage ssd-pool \
  --start

# VM with ISO for installation
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 102 \
  --name ubuntu-2404 \
  --memory 4096 \
  --cores 2 \
  --disk-size 50G \
  --iso ubuntu-24.04-server-amd64.iso \
  --ostype l26
```

### `vm clone`

Clone an existing VM or template.

**Required Options:**
- `--node`, `-n`: Node name where source VM/template exists
- `--source-vmid`: Source VM/template ID to clone from
- `--new-vmid`: New VM ID (must be unique)
- `--name`: Name for the cloned VM

**Optional Options:**
- `--target-node`: Target node for clone (defaults to source node)
- `--storage`: Target storage (defaults to source storage)
- `--full`: Create a full clone instead of linked clone
- `--description`: Description for the cloned VM
- `--pool`: Add VM to specified resource pool
- `--start`: Start VM after cloning

**Clone Types:**

1. **Linked Clone (default)**:
   - Fast creation
   - Uses less disk space
   - Depends on source template/VM
   - Best for: Templates, development environments

2. **Full Clone (`--full`)**:
   - Complete independent copy
   - Takes longer to create
   - Uses more disk space
   - Independent of source
   - Best for: Production VMs, backups

**Examples:**

```bash
# Basic linked clone
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 100 \
  --name cloned-vm

# Full clone for production
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 101 \
  --name prod-vm-01 \
  --full \
  --description "Production server" \
  --pool production

# Clone to different node
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 100 \
  --new-vmid 200 \
  --name remote-vm \
  --target-node hades \
  --storage remote-lvm \
  --full
```

## JSON Output

Both commands support JSON output when using `--output json`:

### Create VM JSON Response

```json
{
  "success": true,
  "vmid": 200,
  "name": "ubuntu-server",
  "node": "skullcanyon"
}
```

### Clone VM JSON Response

```json
{
  "success": true,
  "source_vmid": 9000,
  "new_vmid": 210,
  "name": "web-server-01",
  "task": "UPID:skullcanyon:00001234:0000ABCD:00000000:qmclone:210:root@pam:",
  "clone_type": "linked"
}
```

## Common Workflows

### 1. Template-Based VM Provisioning

```bash
# Step 1: Create template (one time)
proxmox-cli vm create \
  --node skullcanyon \
  --vmid 9000 \
  --name ubuntu-template \
  --memory 2048 \
  --cores 2 \
  --disk-size 32G \
  --iso ubuntu-24.04-server-amd64.iso

# (Install OS, configure, then convert to template via UI or API)

# Step 2: Clone from template (multiple times)
for i in {1..5}; do
  proxmox-cli vm clone \
    --node skullcanyon \
    --source-vmid 9000 \
    --new-vmid $((200 + i)) \
    --name "web-server-0$i" \
    --start
done
```

### 2. Development Environment Setup

```bash
# Create dev VM from template
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9001 \
  --new-vmid 300 \
  --name "dev-environment" \
  --description "Development environment for testing" \
  --start

# (Linked clone is fine for dev - saves space and time)
```

### 3. Production Deployment

```bash
# Full clone for production (independent of template)
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 9000 \
  --new-vmid 400 \
  --name "prod-app-server" \
  --full \
  --storage ssd-pool \
  --pool production \
  --description "Production application server" \
  --start
```

### 4. VM Migration/Backup

```bash
# Clone to different node (backup/DR)
proxmox-cli vm clone \
  --node skullcanyon \
  --source-vmid 100 \
  --new-vmid 500 \
  --name "backup-vm" \
  --target-node hades \
  --storage backup-storage \
  --full \
  --description "Backup copy of VM 100"
```

## Best Practices

### VM Creation

1. **Choose appropriate VMID ranges**:
   - 100-199: Test/Development VMs
   - 200-299: Staging VMs
   - 300-999: Production VMs
   - 9000-9999: Templates

2. **Memory allocation**:
   - Start conservative, scale up as needed
   - Leave some memory for host OS
   - Monitor actual usage before adding more

3. **Storage selection**:
   - SSD/NVMe for databases and high-I/O workloads
   - HDD for bulk storage, backups
   - Local storage for templates (faster cloning)

4. **Network configuration**:
   - Use `virtio` for best performance (Linux)
   - Use `e1000` for compatibility (older OS)

### VM Cloning

1. **Use linked clones for**:
   - Development/testing environments
   - Temporary VMs
   - When disk space is limited
   - Quick provisioning needed

2. **Use full clones for**:
   - Production environments
   - VMs that need to be independent
   - Long-term deployments
   - When you might delete the template

3. **Template management**:
   - Keep templates up-to-date with patches
   - Use cloud-init for customization
   - Document template configurations
   - Use naming conventions (e.g., `ubuntu-2404-template`)

## Error Handling

Common errors and solutions:

### "VMID already exists"
```bash
# Check existing VMs
proxmox-cli vm list

# Use a different VMID
proxmox-cli vm create --vmid 999 ...
```

### "Insufficient resources"
```bash
# Check node resources first
proxmox-cli node status skullcanyon

# Reduce VM specs or use different node
```

### "Storage not found"
```bash
# List available storage
proxmox-cli storage list

# Use correct storage name
```

### "Template not found"
```bash
# Verify source VMID exists
proxmox-cli vm list

# Check source VMID is correct
```

## See Also

- `proxmox-cli vm list` - List all VMs
- `proxmox-cli vm start` - Start a VM
- `proxmox-cli vm stop` - Stop a VM
- `proxmox-cli vm status` - Get VM status
- `proxmox-cli node list` - List cluster nodes
- `proxmox-cli storage list` - List available storage
