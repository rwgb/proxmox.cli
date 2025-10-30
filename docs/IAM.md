# IAM (Identity and Access Management) Commands

This document describes the IAM commands available in the Proxmox CLI for managing users, groups, roles, permissions (ACLs), and API tokens.

## User Management

Manage Proxmox users with the `user` command group.

### List Users
```bash
proxmox-cli user list
```

### Create User
```bash
proxmox-cli user create user@pve \
  --password "SecurePassword123" \
  --email "user@example.com" \
  --firstname "John" \
  --lastname "Doe" \
  --groups "developers,users" \
  --comment "Developer account"
```

Options:
- `--password, -p`: User password
- `--email, -e`: Email address
- `--firstname`: First name
- `--lastname`: Last name
- `--groups`: Comma-separated list of groups
- `--enable/--disable`: Enable or disable the user (default: enabled)
- `--expire`: Account expiration date (Unix epoch)
- `--comment`: User comment/description

### Update User
```bash
proxmox-cli user update user@pve \
  --email "newemail@example.com" \
  --groups "developers" \
  --enable
```

### Delete User
```bash
proxmox-cli user delete user@pve
```

### Show User Details
```bash
proxmox-cli user show user@pve
```

### Change Password
```bash
proxmox-cli user set-password user@pve --password "NewPassword123"
```

## Group Management

Manage Proxmox groups with the `group` command group.

### List Groups
```bash
proxmox-cli group list
```

### Create Group
```bash
proxmox-cli group create developers --comment "Development team"
```

### Update Group
```bash
proxmox-cli group update developers --comment "Updated description"
```

### Delete Group
```bash
proxmox-cli group delete developers
```

### Show Group Details
```bash
proxmox-cli group show developers
```

## Role Management

Manage Proxmox roles with the `role` command group.

### List Roles
```bash
proxmox-cli role list
```

### Create Role
```bash
proxmox-cli role create CustomRole \
  --privs "VM.Allocate,VM.Audit,VM.PowerMgmt"
```

Common privileges:
- `VM.Allocate`: Create/remove VMs
- `VM.Audit`: View VM status
- `VM.PowerMgmt`: Power management (start/stop)
- `VM.Console`: Access VM console
- `VM.Config.*`: Configure VM settings
- `Datastore.Allocate`: Create/remove datastores
- `Datastore.AllocateSpace`: Allocate space on datastores
- `Sys.Audit`: View system status
- `Sys.Modify`: Modify system settings
- `User.Modify`: Modify users
- `Permissions.Modify`: Modify permissions

### Update Role
```bash
# Replace privileges
proxmox-cli role update CustomRole \
  --privs "VM.Allocate,VM.Audit,VM.PowerMgmt,VM.Console"

# Append privileges
proxmox-cli role update CustomRole \
  --privs "VM.Backup" \
  --append
```

### Delete Role
```bash
proxmox-cli role delete CustomRole
```

### Show Role Details
```bash
proxmox-cli role show CustomRole
```

## ACL (Permissions) Management

Manage access control lists (permissions) with the `acl` command group.

### List ACLs
```bash
proxmox-cli acl list
```

### Add ACL Entry (Grant Permissions)
```bash
# Grant permissions to a user
proxmox-cli acl add \
  --path "/" \
  --roles "PVEAdmin" \
  --users "user@pve"

# Grant permissions to a group
proxmox-cli acl add \
  --path "/vms" \
  --roles "PVEVMUser" \
  --groups "developers"

# Grant permissions to an API token
proxmox-cli acl add \
  --path "/storage" \
  --roles "PVEDatastoreUser" \
  --tokens "user@pve!tokenid"

# Multiple users/groups
proxmox-cli acl add \
  --path "/vms/100" \
  --roles "PVEVMUser" \
  --users "user1@pve,user2@pve" \
  --groups "developers" \
  --no-propagate
```

Common paths:
- `/`: Root (entire cluster)
- `/vms`: All VMs
- `/vms/100`: Specific VM (VMID 100)
- `/storage`: All storage
- `/storage/local`: Specific storage
- `/nodes`: All nodes
- `/nodes/pve1`: Specific node
- `/pool/mypool`: Specific resource pool

Options:
- `--path, -p`: Access control path (required)
- `--roles, -r`: Role to assign (required)
- `--users, -u`: Comma-separated list of users
- `--groups, -g`: Comma-separated list of groups
- `--tokens, -t`: Comma-separated list of API tokens
- `--propagate/--no-propagate`: Propagate to child paths (default: propagate)

### Remove ACL Entry (Revoke Permissions)
```bash
proxmox-cli acl remove \
  --path "/" \
  --roles "PVEAdmin" \
  --users "user@pve"
```

## API Token Management

Manage API tokens with the `token` command group.

### List Tokens
```bash
proxmox-cli token list user@pve
```

### Create Token
```bash
proxmox-cli token create user@pve mytoken \
  --comment "Automation token" \
  --privsep
```

**Important:** The token value is only displayed once during creation. Save it securely!

Options:
- `--privsep/--no-privsep`: Enable privilege separation (default: enabled)
  - With privsep: Token has same permissions as user
  - Without privsep: Token needs separate ACL permissions
- `--expire`: Token expiration date (Unix epoch)
- `--comment`: Token description

### Update Token
```bash
proxmox-cli token update user@pve mytoken \
  --comment "Updated description" \
  --no-privsep
```

### Delete Token
```bash
proxmox-cli token delete user@pve mytoken
```

### Show Token Details
```bash
proxmox-cli token show user@pve mytoken
```

## Common Workflows

### Create a Read-Only User
```bash
# 1. Create the user
proxmox-cli user create readonly@pve \
  --password "SecurePass123" \
  --email "readonly@example.com"

# 2. Grant read-only permissions
proxmox-cli acl add \
  --path "/" \
  --roles "PVEAuditor" \
  --users "readonly@pve"
```

### Create an Automation User with API Token
```bash
# 1. Create the user
proxmox-cli user create automation@pve \
  --comment "Automation account"

# 2. Create API token (without privilege separation for better control)
proxmox-cli token create automation@pve apitoken \
  --comment "CI/CD automation" \
  --no-privsep

# 3. Grant specific permissions to the token
proxmox-cli acl add \
  --path "/" \
  --roles "PVEVMUser" \
  --tokens "automation@pve!apitoken"
```

### Create a Developer Group with VM Management Permissions
```bash
# 1. Create the group
proxmox-cli group create developers \
  --comment "Development team"

# 2. Grant permissions to the group
proxmox-cli acl add \
  --path "/vms" \
  --roles "PVEVMAdmin" \
  --groups "developers"

# 3. Add users to the group
proxmox-cli user update dev1@pve --groups "developers"
proxmox-cli user update dev2@pve --groups "developers"
```

### Create a Custom Role for Terraform
```bash
# 1. Create the role with specific privileges
proxmox-cli role create TerraformRole \
  --privs "VM.Allocate,VM.Audit,VM.Config.CPU,VM.Config.Memory,VM.Config.Disk,VM.Config.Network,VM.Config.Options,VM.PowerMgmt,Datastore.AllocateSpace,Datastore.Audit,Pool.Allocate"

# 2. Create a user for Terraform
proxmox-cli user create terraform@pve

# 3. Create API token
proxmox-cli token create terraform@pve tftoken --no-privsep

# 4. Grant permissions
proxmox-cli acl add \
  --path "/" \
  --roles "TerraformRole" \
  --tokens "terraform@pve!tftoken"
```

## Output Formats

All IAM commands support multiple output formats:

```bash
# JSON (default)
proxmox-cli user list

# Table format
proxmox-cli --output table user list

# YAML format
proxmox-cli --output yaml role list

# Plain text
proxmox-cli --output plain group list
```

## Examples with Table Output

```bash
# List users in table format
proxmox-cli --output table user list

# List roles with readable table
proxmox-cli --output table role list

# Show specific user details
proxmox-cli --output table user show user@pve
```
