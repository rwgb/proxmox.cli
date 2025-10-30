"""LXC Container management commands."""
import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_success, print_error


@click.group()
def container():
    """Manage LXC containers."""
    pass


@container.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.pass_context
def list_containers(ctx, node):
    """List all LXC containers."""
    try:
        client = get_proxmox_client(ctx)
        
        containers = client.get_containers(node=node)
        
        if containers:
            # Filter to show only relevant columns
            filtered_containers = []
            for c in containers:
                filtered_containers.append({
                    'VMID': c.get('vmid'),
                    'Name': c.get('name'),
                    'Status': c.get('status'),
                    'CPU': f"{c.get('cpu', 0)*100:.2f}%",
                    'Memory': f"{c.get('mem', 0) / (1024**3):.2f}GB / {c.get('maxmem', 0) / (1024**3):.2f}GB",
                    'Uptime': f"{c.get('uptime', 0) // 86400}d {(c.get('uptime', 0) % 86400) // 3600}h",
                })
            print_table(filtered_containers, title="LXC Containers")
        else:
            print_error("No containers found")
    
    except Exception as e:
        print_error(f"Failed to list containers: {str(e)}")


@container.command("start")
@click.argument("ctid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def start_container(ctx, ctid, node):
    """Start an LXC container."""
    try:
        client = get_proxmox_client(ctx)
        
        client.api.nodes(node).lxc(ctid).status.start.post()
        print_success(f"Container {ctid} started successfully")
    
    except Exception as e:
        print_error(f"Failed to start container: {str(e)}")


@container.command("stop")
@click.argument("ctid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def stop_container(ctx, ctid, node):
    """Stop an LXC container."""
    try:
        client = get_proxmox_client(ctx)
        
        client.api.nodes(node).lxc(ctid).status.stop.post()
        print_success(f"Container {ctid} stopped successfully")
    
    except Exception as e:
        print_error(f"Failed to stop container: {str(e)}")
