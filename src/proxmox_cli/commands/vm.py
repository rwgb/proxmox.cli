"""Virtual Machine management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def vm():
    """Manage virtual machines."""
    pass


@vm.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.option("--templates-only", is_flag=True, help="Show only VM templates")
@click.pass_context
def list_vms(ctx, node, templates_only):
    """List all virtual machines."""
    try:
        client = get_proxmox_client(ctx)

        vms = client.get_vms(node=node)

        if vms:
            # Filter templates if requested
            if templates_only:
                vms = [v for v in vms if v.get("template", 0) == 1]

            # Filter to show only relevant columns
            filtered_vms = []
            for v in vms:
                vm_info = {
                    "vmid": v.get("vmid"),
                    "name": v.get("name"),
                    "status": v.get("status"),
                    "cpu": f"{v.get('cpu', 0)*100:.2f}%",
                    "memory": f"{v.get('mem', 0) / (1024**3):.2f}GB / {v.get('maxmem', 0) / (1024**3):.2f}GB",
                    "uptime": f"{v.get('uptime', 0) // 86400}d {(v.get('uptime', 0) % 86400) // 3600}h",
                }
                # Add template indicator if it's a template
                if v.get("template", 0) == 1:
                    vm_info["template"] = "yes"
                filtered_vms.append(vm_info)

            # Check output format from context
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(filtered_vms)
            else:
                # Convert keys to uppercase for table display
                table_data = []
                for item in filtered_vms:
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="Virtual Machines")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                message = "No templates found" if templates_only else "No virtual machines found"
                print_error(message)

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list VMs: {str(e)}")


@vm.command("templates")
@click.option("--node", "-n", help="Filter by node name")
@click.pass_context
def list_templates(ctx, node):
    """List all VM templates."""
    try:
        client = get_proxmox_client(ctx)

        vms = client.get_vms(node=node)

        # Filter only templates
        templates = [v for v in vms if v.get("template", 0) == 1]

        if templates:
            # Format template information
            filtered_templates = []
            for t in templates:
                filtered_templates.append(
                    {
                        "vmid": t.get("vmid"),
                        "name": t.get("name"),
                        "node": t.get("node", "unknown"),
                        "disk": f"{t.get('maxdisk', 0) / (1024**3):.2f}GB",
                        "memory": f"{t.get('maxmem', 0) / (1024**3):.2f}GB",
                        "cpu": f"{t.get('cpus', 0)} cores",
                    }
                )

            # Check output format from context
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(filtered_templates)
            else:
                # Convert keys to uppercase for table display
                table_data = []
                for item in filtered_templates:
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="VM Templates")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No templates found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list templates: {str(e)}")


@vm.command("start")
@click.argument("vmid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def start_vm(ctx, vmid, node):
    """Start a virtual machine."""
    try:
        client = get_proxmox_client(ctx)

        client.api.nodes(node).qemu(vmid).status.start.post()
        print_success(f"VM {vmid} started successfully")

    except Exception as e:
        print_error(f"Failed to start VM: {str(e)}")


@vm.command("stop")
@click.argument("vmid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def stop_vm(ctx, vmid, node):
    """Stop a virtual machine."""
    try:
        client = get_proxmox_client(ctx)

        client.api.nodes(node).qemu(vmid).status.stop.post()
        print_success(f"VM {vmid} stopped successfully")

    except Exception as e:
        print_error(f"Failed to stop VM: {str(e)}")


@vm.command("status")
@click.argument("vmid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def vm_status(ctx, vmid, node):
    """Get virtual machine status."""
    try:
        client = get_proxmox_client(ctx)

        status = client.api.nodes(node).qemu(vmid).status.current.get()
        print_table([status], title=f"VM {vmid} Status")

    except Exception as e:
        print_error(f"Failed to get VM status: {str(e)}")


@vm.command("create")
@click.option("--node", "-n", required=True, help="Node name where VM will be created")
@click.option("--vmid", required=True, type=int, help="VM ID (must be unique)")
@click.option("--name", required=True, help="VM name")
@click.option("--memory", "-m", default=2048, type=int, help="Memory in MB (default: 2048)")
@click.option("--cores", "-c", default=2, type=int, help="Number of CPU cores (default: 2)")
@click.option("--sockets", "-s", default=1, type=int, help="Number of CPU sockets (default: 1)")
@click.option("--disk-size", "-d", default="32G", help="Disk size (e.g., 32G, 64G)")
@click.option("--storage", default="local-lvm", help="Storage for disk (default: local-lvm)")
@click.option("--iso", help="ISO image name (e.g., debian-12.0.0-amd64-netinst.iso)")
@click.option("--ostype", default="l26", help="OS type (l26=Linux 2.6+, win10=Windows 10)")
@click.option("--network-bridge", default="vmbr0", help="Network bridge (default: vmbr0)")
@click.option("--network-model", default="virtio", help="Network card model (default: virtio)")
@click.option("--start", is_flag=True, help="Start VM after creation")
@click.pass_context
def create_vm(
    ctx,
    node,
    vmid,
    name,
    memory,
    cores,
    sockets,
    disk_size,
    storage,
    iso,
    ostype,
    network_bridge,
    network_model,
    start,
):
    """Create a new virtual machine."""
    try:
        client = get_proxmox_client(ctx)

        # Build VM configuration
        vm_config = {
            "vmid": vmid,
            "name": name,
            "memory": memory,
            "cores": cores,
            "sockets": sockets,
            "ostype": ostype,
            "net0": f"{network_model},bridge={network_bridge}",
        }

        # Add disk configuration
        vm_config["scsi0"] = f"{storage}:{disk_size}"
        vm_config["scsihw"] = "virtio-scsi-pci"

        # Add ISO if provided
        if iso:
            vm_config["ide2"] = f"{storage}:iso/{iso},media=cdrom"

        # Create the VM
        client.api.nodes(node).qemu.post(**vm_config)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "vmid": vmid, "name": name, "node": node})
        else:
            print_success(f"VM {vmid} ({name}) created successfully on node {node}")

        # Start VM if requested
        if start:
            client.api.nodes(node).qemu(vmid).status.start.post()
            if ctx.obj.get("output_format", "json") == "json":
                print_json({"success": True, "vmid": vmid, "status": "started"})
            else:
                print_success(f"VM {vmid} started successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create VM: {str(e)}")


@vm.command("clone")
@click.option("--node", "-n", required=True, help="Node name where VM/template exists")
@click.option("--source-vmid", required=True, type=int, help="Source VM/template ID to clone from")
@click.option("--new-vmid", required=True, type=int, help="New VM ID (must be unique)")
@click.option("--name", required=True, help="Name for the cloned VM")
@click.option("--target-node", help="Target node (defaults to same as source)")
@click.option("--storage", help="Target storage (defaults to same as source)")
@click.option("--full", is_flag=True, help="Create a full clone (default: linked clone)")
@click.option("--description", help="Description for the cloned VM")
@click.option("--pool", help="Add VM to resource pool")
@click.option("--start", is_flag=True, help="Start VM after cloning")
@click.pass_context
def clone_vm(
    ctx, node, source_vmid, new_vmid, name, target_node, storage, full, description, pool, start
):
    """Clone a VM or template to create a new VM."""
    try:
        client = get_proxmox_client(ctx)

        # Build clone configuration
        clone_config = {
            "newid": new_vmid,
            "name": name,
        }

        # Add optional parameters
        if target_node:
            clone_config["target"] = target_node
        if storage:
            clone_config["storage"] = storage
        if full:
            clone_config["full"] = 1
        if description:
            clone_config["description"] = description
        if pool:
            clone_config["pool"] = pool

        # Clone the VM
        task_id = client.api.nodes(node).qemu(source_vmid).clone.post(**clone_config)

        if ctx.obj.get("output_format", "json") == "json":
            print_json(
                {
                    "success": True,
                    "source_vmid": source_vmid,
                    "new_vmid": new_vmid,
                    "name": name,
                    "task": task_id,
                    "clone_type": "full" if full else "linked",
                }
            )
        else:
            clone_type = "full clone" if full else "linked clone"
            print_success(f"VM {source_vmid} cloned to {new_vmid} ({name}) as {clone_type}")
            print_success(f"Task ID: {task_id}")

        # Start VM if requested
        if start:
            # Wait a moment for clone to complete
            import time

            time.sleep(2)
            target = target_node if target_node else node
            client.api.nodes(target).qemu(new_vmid).status.start.post()
            if ctx.obj.get("output_format", "json") == "json":
                print_json({"success": True, "vmid": new_vmid, "status": "started"})
            else:
                print_success(f"VM {new_vmid} started successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to clone VM: {str(e)}")
