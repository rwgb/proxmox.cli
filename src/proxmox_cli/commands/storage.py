"""Storage management commands."""

import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_error, print_json


@click.group()
def storage():
    """Manage storage."""
    pass


@storage.command("list")
@click.pass_context
def list_storage(ctx):
    """List all storage."""
    try:
        client = get_proxmox_client(ctx)

        storage_list = client.api.storage.get()

        if storage_list:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(storage_list)
            else:
                print_table(storage_list, title="Storage")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No storage found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list storage: {str(e)}")
