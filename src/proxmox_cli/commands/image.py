"""Image (VM Template) management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_table


@click.group()
def image():
    """Manage VM templates (images)."""
    pass


@image.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.pass_context
def list_images(ctx, node):
    """List all VM templates."""
    try:
        client = get_proxmox_client(ctx)

        vms = client.get_vms(node=node)

        # Filter only templates
        templates = [v for v in vms if v.get("template", 0) == 1]

        if templates:
            # Format template information
            filtered_templates = []
            for t in templates:
                filtered_templates.append(
                    {
                        "vmid": t.get("vmid"),
                        "name": t.get("name"),
                        "node": t.get("node", "unknown"),
                        "disk": f"{t.get('maxdisk', 0) / (1024**3):.2f}GB",
                        "memory": f"{t.get('maxmem', 0) / (1024**3):.2f}GB",
                        "cpu": f"{t.get('cpus', 0)} cores",
                    }
                )

            # Check output format from context
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(filtered_templates)
            else:
                # Convert keys to uppercase for table display
                table_data = []
                for item in filtered_templates:
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="VM Templates")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No templates found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list templates: {str(e)}")
