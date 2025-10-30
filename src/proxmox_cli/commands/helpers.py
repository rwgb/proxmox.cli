"""Helper functions for commands."""

from proxmox_cli.client import ProxmoxClient
from proxmox_cli.config import Config


def get_proxmox_client(ctx):
    """Get configured Proxmox client from context.

    Args:
        ctx: Click context object

    Returns:
        ProxmoxClient instance
    """
    config = Config(ctx.obj.get("config_path"))

    # Get verify_ssl with proper fallback handling
    verify_ssl = ctx.obj.get("verify_ssl")
    if verify_ssl is None:
        verify_ssl = config.get("proxmox.verify_ssl", True)

    return ProxmoxClient(
        host=ctx.obj.get("host") or config.get("proxmox.host"),
        user=ctx.obj.get("user") or config.get("proxmox.user"),
        password=ctx.obj.get("password") or config.get("proxmox.password"),
        token_name=config.get("proxmox.token_name"),
        token_value=config.get("proxmox.token_value"),
        verify_ssl=verify_ssl,
    )
