"""Main CLI entry point for proxmox-cli."""
import click
from proxmox_cli import __version__
from proxmox_cli.commands import vm, container, node, storage, backup


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option("--host", "-h", help="Proxmox host")
@click.option("--user", "-u", help="Proxmox user")
@click.option("--password", "-p", help="Proxmox password")
@click.option("--verify-ssl/--no-verify-ssl", default=None, help="Verify SSL certificate")
@click.pass_context
def main(ctx, config, host, user, password, verify_ssl):
    """Proxmox CLI - Command-line interface for Proxmox Virtual Environment."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config
    ctx.obj["host"] = host
    ctx.obj["user"] = user
    ctx.obj["password"] = password
    ctx.obj["verify_ssl"] = verify_ssl


# Register command groups
main.add_command(vm.vm)
main.add_command(container.container)
main.add_command(node.node)
main.add_command(storage.storage)
main.add_command(backup.backup)


if __name__ == "__main__":
    main()
