"""Node management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_table


@click.group()
def node():
    """Manage Proxmox nodes."""
    pass


@node.command("list")
@click.pass_context
def list_nodes(ctx):
    """List all nodes in the cluster."""
    try:
        client = get_proxmox_client(ctx)

        nodes = client.get_nodes()

        if nodes:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(nodes)
            else:
                print_table(nodes, title="Cluster Nodes")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No nodes found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list nodes: {str(e)}")


@node.command("status")
@click.argument("node_name")
@click.pass_context
def node_status(ctx, node_name):
    """Get node status information."""
    try:
        client = get_proxmox_client(ctx)

        status = client.api.nodes(node_name).status.get()
        print_table([status], title=f"Node {node_name} Status")

    except Exception as e:
        print_error(f"Failed to get node status: {str(e)}")
