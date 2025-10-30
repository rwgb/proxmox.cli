"""Role management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def role():
    """Manage Proxmox roles."""
    pass


@role.command("list")
@click.pass_context
def list_roles(ctx):
    """List all roles."""
    try:
        client = get_proxmox_client(ctx)

        roles = client.api.access.roles.get()

        if roles:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(roles)
            else:
                print_table(roles, title="Roles")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No roles found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list roles: {str(e)}")


@role.command("create")
@click.argument("roleid")
@click.option("--privs", help="Comma-separated list of privileges")
@click.pass_context
def create_role(ctx, roleid, privs):
    """Create a new role."""
    try:
        client = get_proxmox_client(ctx)

        role_data = {"roleid": roleid}
        if privs:
            role_data["privs"] = privs

        client.api.access.roles.post(**role_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "roleid": roleid})
        else:
            print_success(f"Role '{roleid}' created successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create role: {str(e)}")


@role.command("delete")
@click.argument("roleid")
@click.pass_context
def delete_role(ctx, roleid):
    """Delete a role."""
    try:
        client = get_proxmox_client(ctx)

        client.api.access.roles(roleid).delete()

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "roleid": roleid})
        else:
            print_success(f"Role '{roleid}' deleted successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to delete role: {str(e)}")


@role.command("update")
@click.argument("roleid")
@click.option("--privs", required=True, help="Comma-separated list of privileges")
@click.option("--append/--no-append", default=False, help="Append privileges instead of replacing")
@click.pass_context
def update_role(ctx, roleid, privs, append):
    """Update role privileges."""
    try:
        client = get_proxmox_client(ctx)

        role_data = {"privs": privs}
        if append:
            role_data["append"] = 1

        client.api.access.roles(roleid).put(**role_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "roleid": roleid})
        else:
            print_success(f"Role '{roleid}' updated successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to update role: {str(e)}")


@role.command("show")
@click.argument("roleid")
@click.pass_context
def show_role(ctx, roleid):
    """Show role details."""
    try:
        client = get_proxmox_client(ctx)

        role_info = client.api.access.roles(roleid).get()

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(role_info)
        else:
            print_table([role_info], title=f"Role: {roleid}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get role info: {str(e)}")
