"""Image (VM Template) management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def image():
    """Manage VM templates (images)."""
    pass


@image.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.pass_context
def list_images(ctx, node):
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


@image.command("info")
@click.argument("vmid", type=int)
@click.option("--node", "-n", help="Node name where template is located")
@click.pass_context
def template_info(ctx, vmid, node):
    """Show detailed information about a VM template.

    VMID: The VM template ID to get information about
    """
    try:
        client = get_proxmox_client(ctx)

        # If node not specified, find it by checking each node
        if not node:
            nodes = client.get_nodes()
            found_node = None

            for node_info in nodes:
                node_name = node_info.get("node")
                try:
                    # Try to get VMs from this node
                    vms = client.api.nodes(node_name).qemu.get()
                    for v in vms:
                        if v.get("vmid") == vmid and v.get("template", 0) == 1:
                            found_node = node_name
                            break
                    if found_node:
                        break
                except Exception:
                    # Skip nodes that are unreachable
                    continue

            if not found_node:
                if ctx.obj.get("output_format", "json") == "json":
                    print_json({"error": f"Template with VMID {vmid} not found"})
                else:
                    print_error(f"Template with VMID {vmid} not found")
                return

            node = found_node

        # Get detailed VM configuration
        try:
            config = client.api.nodes(node).qemu(vmid).config.get()
        except Exception as e:
            if ctx.obj.get("output_format", "json") == "json":
                print_json({"error": f"Template {vmid} not found on node {node}: {str(e)}"})
            else:
                print_error(f"Template {vmid} not found on node {node}: {str(e)}")
            return

        # Verify it's actually a template
        if not config.get("template", 0):
            if ctx.obj.get("output_format", "json") == "json":
                print_json({"error": f"VM {vmid} is not a template"})
            else:
                print_error(f"VM {vmid} is not a template")
            return

        # Format the detailed information
        memory_val = config.get("memory", 0)
        try:
            memory_mb = int(memory_val) if memory_val else 0
            memory_gb = f"{memory_mb / 1024:.2f}GB"
        except (ValueError, TypeError):
            memory_mb = 0
            memory_gb = "N/A"

        info = {
            "vmid": vmid,
            "name": config.get("name", "N/A"),
            "node": node,
            "template": True,
            "description": config.get("description", "No description"),
            "ostype": config.get("ostype", "other"),
            "cpu": {
                "cores": config.get("cores", 0),
                "sockets": config.get("sockets", 1),
                "total": config.get("cores", 0) * config.get("sockets", 1),
            },
            "memory": memory_gb,
            "memory_mb": memory_mb,
        }

        # Parse network interfaces
        networks = []
        for key, value in config.items():
            if key.startswith("net"):
                net_info = {"interface": key, "config": value}
                # Parse network config string
                if "=" in value:
                    parts = value.split(",")
                    for part in parts:
                        if "=" in part:
                            k, v = part.split("=", 1)
                            net_info[k.strip()] = v.strip()
                networks.append(net_info)
        if networks:
            info["networks"] = networks

        # Parse disk configuration
        disks = []
        total_disk_size = 0
        for key, value in config.items():
            if key.startswith(("scsi", "sata", "ide", "virtio")) and key[-1].isdigit():
                disk_info = {"interface": key, "config": value}
                # Parse disk config string
                if ":" in value:
                    parts = value.split(",")
                    storage_info = parts[0].split(":")
                    if len(storage_info) >= 2:
                        disk_info["storage"] = storage_info[0]
                        # Extract size if present
                        for part in parts:
                            if "size=" in part:
                                size_str = part.split("=")[1]
                                disk_info["size"] = size_str
                                # Convert to GB for total
                                try:
                                    if "G" in size_str:
                                        total_disk_size += float(size_str.replace("G", ""))
                                    elif "M" in size_str:
                                        total_disk_size += float(size_str.replace("M", "")) / 1024
                                except ValueError:
                                    pass
                disks.append(disk_info)
        if disks:
            info["disks"] = disks
            info["total_disk_size"] = f"{total_disk_size:.2f}GB"

        # Add boot order if present
        if "boot" in config:
            info["boot_order"] = config["boot"]

        # Add BIOS type
        if "bios" in config:
            info["bios"] = config["bios"]

        # Add machine type
        if "machine" in config:
            info["machine"] = config["machine"]

        # Add agent info
        if "agent" in config:
            info["qemu_agent"] = config["agent"]

        # Output format
        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(info)
        else:
            # For table output, create a formatted display
            display_info = {
                "VMID": info["vmid"],
                "NAME": info["name"],
                "NODE": info["node"],
                "TEMPLATE": "Yes",
                "OS TYPE": info["ostype"],
                "CPU CORES": info["cpu"]["cores"],
                "CPU SOCKETS": info["cpu"]["sockets"],
                "TOTAL CPUS": info["cpu"]["total"],
                "MEMORY": info["memory"],
                "TOTAL DISK": info.get("total_disk_size", "N/A"),
                "DESCRIPTION": (
                    info["description"][:50] + "..."
                    if len(info["description"]) > 50
                    else info["description"]
                ),
            }

            print_table([display_info], title=f"Template {vmid} Information")

            # Show disks
            if disks:
                print("\nDisks:")
                disk_table = []
                for disk in disks:
                    disk_table.append(
                        {
                            "INTERFACE": disk["interface"],
                            "STORAGE": disk.get("storage", "N/A"),
                            "SIZE": disk.get("size", "N/A"),
                        }
                    )
                print_table(disk_table, title="Disk Configuration")

            # Show networks
            if networks:
                print("\nNetworks:")
                net_table = []
                for net in networks:
                    net_table.append(
                        {
                            "INTERFACE": net["interface"],
                            "MODEL": net.get("model", "N/A"),
                            "BRIDGE": net.get("bridge", "N/A"),
                        }
                    )
                print_table(net_table, title="Network Configuration")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get template info: {str(e)}")
