"""Backup management commands."""

import click

from proxmox_cli.client import ProxmoxClient
from proxmox_cli.config import Config
from proxmox_cli.utils.output import print_error, print_success, print_table


@click.group()
def backup():
    """Manage backups."""
    pass


@backup.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.option("--storage", "-s", help="Filter by storage")
@click.pass_context
def list_backups(ctx, node, storage):
    """List all backups."""
    try:
        config = Config(ctx.obj.get("config_path"))
        client = ProxmoxClient(
            host=ctx.obj.get("host") or config.get("proxmox.host"),
            user=ctx.obj.get("user") or config.get("proxmox.user"),
            password=ctx.obj.get("password"),
            verify_ssl=ctx.obj.get("verify_ssl", config.get("proxmox.verify_ssl", True)),
        )

        # Implementation depends on Proxmox backup structure
        print_error("Backup listing not yet implemented")

    except Exception as e:
        print_error(f"Failed to list backups: {str(e)}")
