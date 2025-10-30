"""LXC Container management commands."""
import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_success, print_error, print_json


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
                    'vmid': c.get('vmid'),
                    'name': c.get('name'),
                    'status': c.get('status'),
                    'cpu': f"{c.get('cpu', 0)*100:.2f}%",
                    'memory': f"{c.get('mem', 0) / (1024**3):.2f}GB / {c.get('maxmem', 0) / (1024**3):.2f}GB",
                    'uptime': f"{c.get('uptime', 0) // 86400}d {(c.get('uptime', 0) % 86400) // 3600}h",
                })
            
            # Check output format from context
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(filtered_containers)
            else:
                # Convert keys to uppercase for table display
                table_data = []
                for item in filtered_containers:
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="LXC Containers")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No containers found")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
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
