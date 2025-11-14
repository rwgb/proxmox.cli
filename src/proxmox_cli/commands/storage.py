"""Storage management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


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


@storage.command("create")
@click.argument("storage_id")
@click.option("--type", "-t", "storage_type", default="dir", help="Storage type (default: dir)")
@click.option("--path", "-p", required=True, help="Path on the filesystem")
@click.option(
    "--content",
    "-c",
    help="Content types (comma-separated: vztmpl,iso,backup,images,rootdir,snippets)",
)
@click.option("--nodes", "-n", help="Comma-separated list of cluster nodes (optional)")
@click.option(
    "--shared/--no-shared",
    default=False,
    help="Mark storage as shared (default: no)",
)
@click.option("--maxfiles", type=int, help="Maximum number of backup files per VM")
@click.option(
    "--prune-backups",
    help="Retention options (e.g., 'keep-last=3,keep-weekly=2')",
)
@click.pass_context
def create_storage(
    ctx, storage_id, storage_type, path, content, nodes, shared, maxfiles, prune_backups
):
    """Create a new storage directory.

    STORAGE_ID: Unique identifier for the storage

    Examples:

    \b
    # Basic directory storage for backups
    proxmox-cli storage create backup-storage --path /mnt/backups --content backup

    \b
    # ISO and template storage
    proxmox-cli storage create iso-storage --path /mnt/isos --content "iso,vztmpl"

    \b
    # VM disk storage with shared flag
    proxmox-cli storage create vm-storage --path /mnt/vms \\
      --content "images,rootdir" --shared

    \b
    # Snippets storage for custom scripts
    proxmox-cli storage create snippets-storage --path /mnt/snippets \\
      --content snippets
    """
    try:
        client = get_proxmox_client(ctx)

        # Build additional parameters
        kwargs = {}
        if shared:
            kwargs["shared"] = 1
        if maxfiles:
            kwargs["maxfiles"] = maxfiles
        if prune_backups:
            kwargs["prune-backups"] = prune_backups

        client.create_storage(
            storage_id=storage_id,
            storage_type=storage_type,
            path=path,
            content=content,
            nodes=nodes,
            **kwargs,
        )

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "storage": storage_id, "path": path})
        else:
            print_success(f"Storage '{storage_id}' created successfully at {path}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create storage: {str(e)}")
