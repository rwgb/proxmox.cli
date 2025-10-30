"""API Token management commands."""
import click
from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_table, print_success, print_error, print_json


@click.group()
def token():
    """Manage Proxmox API tokens."""
    pass


@token.command("list")
@click.argument("userid")
@click.pass_context
def list_tokens(ctx, userid):
    """List all API tokens for a user."""
    try:
        client = get_proxmox_client(ctx)
        
        tokens = client.api.access.users(userid).token.get()
        
        if tokens:
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(tokens)
            else:
                print_table(tokens, title=f"API Tokens for {userid}")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error(f"No tokens found for user '{userid}'")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list tokens: {str(e)}")


@token.command("create")
@click.argument("userid")
@click.argument("tokenid")
@click.option("--privsep/--no-privsep", default=True, help="Enable privilege separation")
@click.option("--expire", type=int, help="Token expiration date (Unix epoch)")
@click.option("--comment", help="Token comment/description")
@click.pass_context
def create_token(ctx, userid, tokenid, privsep, expire, comment):
    """Create a new API token for a user."""
    try:
        client = get_proxmox_client(ctx)
        
        token_data = {
            "privsep": 1 if privsep else 0,
        }
        
        if expire:
            token_data["expire"] = expire
        if comment:
            token_data["comment"] = comment
        
        result = client.api.access.users(userid).token(tokenid).post(**token_data)
        
        if ctx.obj.get("output_format", "json") == "json":
            # Include the token value in the response (only shown once!)
            result["success"] = True
            result["userid"] = userid
            result["tokenid"] = tokenid
            print_json(result)
        else:
            print_success(f"Token '{tokenid}' created for user '{userid}'")
            if 'value' in result:
                print_success(f"Token value (save this, it won't be shown again): {result['value']}")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to create token: {str(e)}")


@token.command("delete")
@click.argument("userid")
@click.argument("tokenid")
@click.pass_context
def delete_token(ctx, userid, tokenid):
    """Delete an API token."""
    try:
        client = get_proxmox_client(ctx)
        
        client.api.access.users(userid).token(tokenid).delete()
        
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid, "tokenid": tokenid})
        else:
            print_success(f"Token '{tokenid}' deleted for user '{userid}'")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to delete token: {str(e)}")


@token.command("update")
@click.argument("userid")
@click.argument("tokenid")
@click.option("--privsep/--no-privsep", default=None, help="Enable privilege separation")
@click.option("--expire", type=int, help="Token expiration date (Unix epoch)")
@click.option("--comment", help="Token comment/description")
@click.pass_context
def update_token(ctx, userid, tokenid, privsep, expire, comment):
    """Update API token information."""
    try:
        client = get_proxmox_client(ctx)
        
        token_data = {}
        
        if privsep is not None:
            token_data["privsep"] = 1 if privsep else 0
        if expire:
            token_data["expire"] = expire
        if comment:
            token_data["comment"] = comment
        
        if not token_data:
            raise ValueError("No update parameters provided")
        
        client.api.access.users(userid).token(tokenid).put(**token_data)
        
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"success": True, "userid": userid, "tokenid": tokenid})
        else:
            print_success(f"Token '{tokenid}' updated for user '{userid}'")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e), "success": False})
        else:
            print_error(f"Failed to update token: {str(e)}")


@token.command("show")
@click.argument("userid")
@click.argument("tokenid")
@click.pass_context
def show_token(ctx, userid, tokenid):
    """Show API token details."""
    try:
        client = get_proxmox_client(ctx)
        
        token_info = client.api.access.users(userid).token(tokenid).get()
        
        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(token_info)
        else:
            print_table([token_info], title=f"Token: {userid}!{tokenid}")
    
    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to get token info: {str(e)}")
