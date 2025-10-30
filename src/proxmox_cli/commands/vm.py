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
@click.pass_context
def list_vms(ctx, node):
    """List all virtual machines."""
    try:
        client = get_proxmox_client(ctx)

        vms = client.get_vms(node=node)

        if vms:
            # Filter to show only relevant columns
            filtered_vms = []
            for v in vms:
                filtered_vms.append(
                    {
                        "vmid": v.get("vmid"),
                        "name": v.get("name"),
                        "status": v.get("status"),
                        "cpu": f"{v.get('cpu', 0)*100:.2f}%",
                        "memory": f"{v.get('mem', 0) / (1024**3):.2f}GB / {v.get('maxmem', 0) / (1024**3):.2f}GB",
                        "uptime": f"{v.get('uptime', 0) // 86400}d {(v.get('uptime', 0) % 86400) // 3600}h",
                    }
                )

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
                print_error("No virtual machines found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list VMs: {str(e)}")


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
