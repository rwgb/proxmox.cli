"""Resource pool management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def pool():
    """Manage Proxmox resource pools."""
    pass


@pool.command("list")
@click.pass_context
def list_pools(ctx):
    """List all resource pools."""
    try:
        client = get_proxmox_client(ctx)

        pools = client.api.pools.get()

        if pools:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(pools)
            else:
                print_table(pools, title="Resource Pools")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No resource pools found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list resource pools: {str(e)}")


@pool.command("create")
@click.argument("poolid")
@click.option("--comment", help="Pool comment/description")
@click.pass_context
def create_pool(ctx, poolid, comment):
    """Create a new resource pool."""
    try:
        client = get_proxmox_client(ctx)

        pool_data = {"poolid": poolid}
        if comment:
            pool_data["comment"] = comment

        client.api.pools.post(**pool_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "poolid": poolid})
        else:
            print_success(f"Resource pool '{poolid}' created successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create resource pool: {str(e)}")


@pool.command("delete")
@click.argument("poolid")
@click.pass_context
def delete_pool(ctx, poolid):
    """Delete a resource pool."""
    try:
        client = get_proxmox_client(ctx)

        client.api.pools(poolid).delete()

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "poolid": poolid})
        else:
            print_success(f"Resource pool '{poolid}' deleted successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to delete resource pool: {str(e)}")


@pool.command("update")
@click.argument("poolid")
@click.option("--comment", help="Pool comment/description")
@click.pass_context
def update_pool(ctx, poolid, comment):
    """Update resource pool information."""
    try:
        client = get_proxmox_client(ctx)

        if not comment:
            raise ValueError("No update parameters provided")

        client.api.pools(poolid).put(comment=comment)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "poolid": poolid})
        else:
            print_success(f"Resource pool '{poolid}' updated successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to update resource pool: {str(e)}")


@pool.command("show")
@click.argument("poolid")
@click.pass_context
def show_pool(ctx, poolid):
    """Show resource pool details including members."""
    try:
        client = get_proxmox_client(ctx)

        pool_info = client.api.pools(poolid).get()

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(pool_info)
        else:
            # Display pool information
            pool_details = {
                "poolid": poolid,
                "comment": pool_info.get("comment", ""),
            }
            print_table([pool_details], title=f"Pool: {poolid}")

            # Display members if any
            members = pool_info.get("members", [])
            if members:
                print("\nPool Members:")
                print_table(members, title="Members")
            else:
                print("\nNo members in this pool")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get pool info: {str(e)}")


@pool.command("add-member")
@click.argument("poolid")
@click.option("--vm", "vms", multiple=True, help="VM ID to add to pool (can specify multiple)")
@click.option(
    "--storage", "storages", multiple=True, help="Storage ID to add to pool (can specify multiple)"
)
@click.pass_context
def add_member(ctx, poolid, vms, storages):
    """Add VMs or storage to a resource pool."""
    try:
        client = get_proxmox_client(ctx)

        if not vms and not storages:
            raise ValueError("Must specify at least one VM or storage to add")

        # Prepare the update data
        update_data = {}
        if vms:
            update_data["vms"] = ",".join(vms)
        if storages:
            update_data["storage"] = ",".join(storages)

        client.api.pools(poolid).put(**update_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json(
                {
                    "success": True,
                    "poolid": poolid,
                    "vms_added": list(vms),
                    "storages_added": list(storages),
                }
            )
        else:
            if vms:
                print_success(f"Added VMs {', '.join(vms)} to pool '{poolid}'")
            if storages:
                print_success(f"Added storages {', '.join(storages)} to pool '{poolid}'")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to add members to pool: {str(e)}")


@pool.command("remove-member")
@click.argument("poolid")
@click.option("--vm", "vms", multiple=True, help="VM ID to remove from pool (can specify multiple)")
@click.option(
    "--storage",
    "storages",
    multiple=True,
    help="Storage ID to remove from pool (can specify multiple)",
)
@click.pass_context
def remove_member(ctx, poolid, vms, storages):
    """Remove VMs or storage from a resource pool."""
    try:
        client = get_proxmox_client(ctx)

        if not vms and not storages:
            raise ValueError("Must specify at least one VM or storage to remove")

        # Prepare the delete data
        delete_data = {}
        if vms:
            delete_data["vms"] = ",".join(vms)
        if storages:
            delete_data["storage"] = ",".join(storages)

        client.api.pools(poolid).put(delete=1, **delete_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json(
                {
                    "success": True,
                    "poolid": poolid,
                    "vms_removed": list(vms),
                    "storages_removed": list(storages),
                }
            )
        else:
            if vms:
                print_success(f"Removed VMs {', '.join(vms)} from pool '{poolid}'")
            if storages:
                print_success(f"Removed storages {', '.join(storages)} from pool '{poolid}'")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to remove members from pool: {str(e)}")
