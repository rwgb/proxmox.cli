"""User management commands."""

import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_success, print_error, print_json


@click.group()
def user():
    """Manage Proxmox users."""
    pass


@user.command("list")
@click.pass_context
def list_users(ctx):
    """List all users."""
    try:
        client = get_proxmox_client(ctx)

        users = client.api.access.users.get()

        if users:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(users)
            else:
                print_table(users, title="Users")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No users found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list users: {str(e)}")


@user.command("create")
@click.argument("userid")
@click.option("--password", "-p", help="User password")
@click.option("--email", "-e", help="User email address")
@click.option("--firstname", help="First name")
@click.option("--lastname", help="Last name")
@click.option("--groups", help="Comma-separated list of groups")
@click.option("--enable/--disable", default=True, help="Enable or disable user")
@click.option("--expire", type=int, help="Account expiration date (Unix epoch)")
@click.option("--comment", help="User comment")
@click.pass_context
def create_user(ctx, userid, password, email, firstname, lastname, groups, enable, expire, comment):
    """Create a new user."""
    try:
        client = get_proxmox_client(ctx)

        user_data = {
            "userid": userid,
        }

        if password:
            user_data["password"] = password
        if email:
            user_data["email"] = email
        if firstname:
            user_data["firstname"] = firstname
        if lastname:
            user_data["lastname"] = lastname
        if groups:
            user_data["groups"] = groups
        if not enable:
            user_data["enable"] = 0
        if expire:
            user_data["expire"] = expire
        if comment:
            user_data["comment"] = comment

        client.api.access.users.post(**user_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid})
        else:
            print_success(f"User '{userid}' created successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create user: {str(e)}")


@user.command("delete")
@click.argument("userid")
@click.pass_context
def delete_user(ctx, userid):
    """Delete a user."""
    try:
        client = get_proxmox_client(ctx)

        client.api.access.users(userid).delete()

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid})
        else:
            print_success(f"User '{userid}' deleted successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to delete user: {str(e)}")


@user.command("update")
@click.argument("userid")
@click.option("--email", "-e", help="User email address")
@click.option("--firstname", help="First name")
@click.option("--lastname", help="Last name")
@click.option("--groups", help="Comma-separated list of groups")
@click.option("--enable/--disable", default=None, help="Enable or disable user")
@click.option("--expire", type=int, help="Account expiration date (Unix epoch)")
@click.option("--comment", help="User comment")
@click.pass_context
def update_user(ctx, userid, email, firstname, lastname, groups, enable, expire, comment):
    """Update user information."""
    try:
        client = get_proxmox_client(ctx)

        user_data = {}

        if email:
            user_data["email"] = email
        if firstname:
            user_data["firstname"] = firstname
        if lastname:
            user_data["lastname"] = lastname
        if groups:
            user_data["groups"] = groups
        if enable is not None:
            user_data["enable"] = 1 if enable else 0
        if expire:
            user_data["expire"] = expire
        if comment:
            user_data["comment"] = comment

        if not user_data:
            raise ValueError("No update parameters provided")

        client.api.access.users(userid).put(**user_data)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid})
        else:
            print_success(f"User '{userid}' updated successfully")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to update user: {str(e)}")


@user.command("show")
@click.argument("userid")
@click.pass_context
def show_user(ctx, userid):
    """Show user details."""
    try:
        client = get_proxmox_client(ctx)

        user_info = client.api.access.users(userid).get()

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(user_info)
        else:
            print_table([user_info], title=f"User: {userid}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get user info: {str(e)}")


@user.command("set-password")
@click.argument("userid")
@click.option("--password", "-p", required=True, help="New password")
@click.pass_context
def set_password(ctx, userid, password):
    """Change user password."""
    try:
        client = get_proxmox_client(ctx)

        client.api.access.password.put(userid=userid, password=password)

        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid})
        else:
            print_success(f"Password changed for user '{userid}'")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to change password: {str(e)}")
