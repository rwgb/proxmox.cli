"""Group management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def group():
    """Manage Proxmox groups."""
    pass


@group.command("list")
@click.pass_context
def list_groups(ctx):
    """List all groups."""
    try:
        client = get_proxmox_client(ctx)

        groups = client.api.access.groups.get()

        if groups:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(groups)
            else:
                print_table(groups, title="Groups")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No groups found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list groups: {str(e)}")


@group.command("create")
@click.argument("groupid")
@click.option("--comment", help="Group comment/description")
@click.pass_context
def create_group(ctx, groupid, comment):
    """Create a new group."""
    try:
        client = get_proxmox_client(ctx)

        group_data = {"groupid": groupid}
        if comment:
            group_data["comment"] = comment

        client.api.access.groups.post(**group_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "groupid": groupid})
        else:
            print_success(f"Group '{groupid}' created successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create group: {str(e)}")


@group.command("delete")
@click.argument("groupid")
@click.pass_context
def delete_group(ctx, groupid):
    """Delete a group."""
    try:
        client = get_proxmox_client(ctx)

        client.api.access.groups(groupid).delete()

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "groupid": groupid})
        else:
            print_success(f"Group '{groupid}' deleted successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to delete group: {str(e)}")


@group.command("update")
@click.argument("groupid")
@click.option("--comment", help="Group comment/description")
@click.pass_context
def update_group(ctx, groupid, comment):
    """Update group information."""
    try:
        client = get_proxmox_client(ctx)

        if not comment:
            raise ValueError("No update parameters provided")

        client.api.access.groups(groupid).put(comment=comment)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "groupid": groupid})
        else:
            print_success(f"Group '{groupid}' updated successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to update group: {str(e)}")


@group.command("show")
@click.argument("groupid")
@click.pass_context
def show_group(ctx, groupid):
    """Show group details."""
    try:
        client = get_proxmox_client(ctx)

        group_info = client.api.access.groups(groupid).get()

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(group_info)
        else:
            print_table([group_info], title=f"Group: {groupid}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get group info: {str(e)}")
