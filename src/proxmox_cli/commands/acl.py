"""ACL (Access Control List) and permissions management commands."""
import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_success, print_error, print_json


@click.group()
def acl():
    """Manage Proxmox ACLs and permissions."""
    pass


@acl.command("list")
@click.pass_context
def list_acls(ctx):
    """List all ACL entries."""
    try:
        client = get_proxmox_client(ctx)
        
        acls = client.api.access.acl.get()
        
        if acls:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(acls)
            else:
                print_table(acls, title="Access Control Lists")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No ACL entries found")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list ACLs: {str(e)}")


@acl.command("add")
@click.option("--path", "-p", required=True, help="Access control path (e.g., /, /vms/100)")
@click.option("--roles", "-r", required=True, help="Role to assign")
@click.option("--users", "-u", help="Comma-separated list of users")
@click.option("--groups", "-g", help="Comma-separated list of groups")
@click.option("--tokens", "-t", help="Comma-separated list of API tokens")
@click.option("--propagate/--no-propagate", default=True, help="Propagate to child paths")
@click.pass_context
def add_acl(ctx, path, roles, users, groups, tokens, propagate):
    """Add ACL entry (grant permissions)."""
    try:
        client = get_proxmox_client(ctx)
        
        acl_data = {
            "path": path,
            "roles": roles,
            "propagate": 1 if propagate else 0,
        }
        
        if users:
            acl_data["users"] = users
        if groups:
            acl_data["groups"] = groups
        if tokens:
            acl_data["tokens"] = tokens
        
        if not (users or groups or tokens):
            raise ValueError("At least one of --users, --groups, or --tokens must be specified")
        
        client.api.access.acl.put(**acl_data)
        
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "path": path, "roles": roles})
        else:
            print_success(f"ACL entry added for path '{path}'")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to add ACL: {str(e)}")


@acl.command("remove")
@click.option("--path", "-p", required=True, help="Access control path")
@click.option("--roles", "-r", required=True, help="Role to remove")
@click.option("--users", "-u", help="Comma-separated list of users")
@click.option("--groups", "-g", help="Comma-separated list of groups")
@click.option("--tokens", "-t", help="Comma-separated list of API tokens")
@click.pass_context
def remove_acl(ctx, path, roles, users, groups, tokens):
    """Remove ACL entry (revoke permissions)."""
    try:
        client = get_proxmox_client(ctx)
        
        acl_data = {
            "path": path,
            "roles": roles,
            "delete": 1,
        }
        
        if users:
            acl_data["users"] = users
        if groups:
            acl_data["groups"] = groups
        if tokens:
            acl_data["tokens"] = tokens
        
        if not (users or groups or tokens):
            raise ValueError("At least one of --users, --groups, or --tokens must be specified")
        
        client.api.access.acl.put(**acl_data)
        
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "path": path, "roles": roles})
        else:
            print_success(f"ACL entry removed for path '{path}'")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to remove ACL: {str(e)}")
