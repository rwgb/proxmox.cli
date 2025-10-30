"""Storage management commands."""
import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_error


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
            print_table(storage_list, title="Storage")
        else:
            print_error("No storage found")
    
    except Exception as e:
        print_error(f"Failed to list storage: {str(e)}")
