"""LXC Container management commands."""

import click

from proxmox_cli.commands.helpers import get_proxmox_client
from proxmox_cli.utils.output import print_error, print_json, print_success, print_table


@click.group()
def container():
    """Manage LXC containers."""
    pass


@container.command("list")
@click.option("--node", "-n", help="Filter by node name")
@click.pass_context
def list_containers(ctx, node):
    """List all LXC containers."""
    try:
        client = get_proxmox_client(ctx)

        containers = client.get_containers(node=node)

        if containers:
            # Filter to show only relevant columns
            filtered_containers = []
            for c in containers:
                filtered_containers.append(
                    {
                        "vmid": c.get("vmid"),
                        "name": c.get("name"),
                        "status": c.get("status"),
                        "cpu": f"{c.get('cpu', 0)*100:.2f}%",
                        "memory": f"{c.get('mem', 0) / (1024**3):.2f}GB / {c.get('maxmem', 0) / (1024**3):.2f}GB",
                        "uptime": f"{c.get('uptime', 0) // 86400}d {(c.get('uptime', 0) % 86400) // 3600}h",
                    }
                )

            # Check output format from context
            output_format = ctx.obj.get("output_format", "json")
            if output_format == "json":
                print_json(filtered_containers)
            else:
                # Convert keys to uppercase for table display
                table_data = []
                for item in filtered_containers:
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="LXC Containers")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No containers found")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list containers: {str(e)}")


@container.command("start")
@click.argument("ctid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def start_container(ctx, ctid, node):
    """Start an LXC container."""
    try:
        client = get_proxmox_client(ctx)

        client.api.nodes(node).lxc(ctid).status.start.post()
        print_success(f"Container {ctid} started successfully")

    except Exception as e:
        print_error(f"Failed to start container: {str(e)}")


@container.command("stop")
@click.argument("ctid")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def stop_container(ctx, ctid, node):
    """Stop an LXC container."""
    try:
        client = get_proxmox_client(ctx)

        client.api.nodes(node).lxc(ctid).status.stop.post()
        print_success(f"Container {ctid} stopped successfully")

    except Exception as e:
        print_error(f"Failed to stop container: {str(e)}")


@container.command("templates")
@click.option("--node", "-n", help="Filter by node name")
@click.option("--storage", "-s", help="Filter by storage name")
@click.pass_context
def list_templates(ctx, node, storage):
    """List available LXC container templates on storage."""
    try:
        client = get_proxmox_client(ctx)

        templates = client.get_container_templates(node=node, storage=storage)

        if templates:
            # Format template information
            filtered_templates = []
            for t in templates:
                # Extract template name from volid (e.g., 'local:vztmpl/ubuntu-22.04.tar.zst')
                volid = t.get("volid", "")
                template_name = volid.split("/")[-1] if "/" in volid else volid

                filtered_templates.append(
                    {
                        "template": template_name,
                        "storage": t.get("storage"),
                        "node": t.get("node"),
                        "size": f"{t.get('size', 0) / (1024**2):.2f}MB",
                        "volid": volid,
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
                print_table(table_data, title="LXC Container Templates")
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


@container.command("available-templates")
@click.option("--node", "-n", required=True, help="Node name")
@click.pass_context
def list_available_templates(ctx, node):
    """List templates available for download from repositories."""
    try:
        client = get_proxmox_client(ctx)

        templates = client.get_available_templates(node=node)

        if templates:
            # Format template information
            filtered_templates = []
            for t in templates:
                filtered_templates.append(
                    {
                        "template": t.get("template", ""),
                        "os": t.get("os", ""),
                        "version": t.get("version", ""),
                        "description": t.get("headline", ""),
                        "architecture": t.get("architecture", ""),
                        "section": t.get("section", ""),
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
                    # Limit description length for table view
                    if "DESCRIPTION" in {k.upper(): v for k, v in item.items()}:
                        desc = item.get("description", "")
                        if len(desc) > 50:
                            item["description"] = desc[:47] + "..."
                    table_data.append({k.upper(): v for k, v in item.items()})
                print_table(table_data, title="Available Templates for Download")
        else:
            if ctx.obj.get("output_format", "json") == "json":
                print_json([])
            else:
                print_error("No templates available")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to list available templates: {str(e)}")


@container.command("download-template")
@click.argument("template")
@click.option("--node", "-n", required=True, help="Node name")
@click.option("--storage", "-s", default="local", help="Storage name (default: local)")
@click.pass_context
def download_template(ctx, template, node, storage):
    """Download a container template from repository.

    TEMPLATE: Template name (e.g., 'ubuntu-22.04-standard_22.04-1_amd64.tar.zst')
    """
    try:
        client = get_proxmox_client(ctx)

        result = client.download_container_template(
            node=node, storage=storage, template=template
        )

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json(result)
        else:
            print_success(f"Template download started: {template}")
            if isinstance(result, dict) and "UPID" in result.values():
                print_success(f"Task ID: {result}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to download template: {str(e)}")


@container.command("create")
@click.argument("vmid", type=int)
@click.argument("ostemplate")
@click.option("--node", "-n", required=True, help="Node name")
@click.option("--hostname", help="Container hostname")
@click.option("--password", help="Root password")
@click.option("--storage", "-s", default="local-lvm", help="Storage for rootfs (default: local-lvm)")
@click.option("--memory", "-m", default=512, type=int, help="Memory in MB (default: 512)")
@click.option("--cores", "-c", default=1, type=int, help="Number of CPU cores (default: 1)")
@click.option("--rootfs-size", default=8, type=int, help="Root filesystem size in GB (default: 8)")
@click.option("--nameserver", help="DNS nameserver")
@click.option("--searchdomain", help="DNS search domain")
@click.option("--net0", help="Network configuration (e.g., 'name=eth0,bridge=vmbr0,ip=dhcp')")
@click.pass_context
def create_container(
    ctx, vmid, ostemplate, node, hostname, password, storage, memory, cores, rootfs_size, nameserver, searchdomain, net0
):
    """Create a new LXC container from a template.

    VMID: Container ID (must be unique)
    OSTEMPLATE: Template volume ID (e.g., 'local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst')
    """
    try:
        client = get_proxmox_client(ctx)

        # Build additional parameters
        kwargs = {}
        if nameserver:
            kwargs["nameserver"] = nameserver
        if searchdomain:
            kwargs["searchdomain"] = searchdomain
        if net0:
            kwargs["net0"] = net0

        result = client.create_container(
            node=node,
            vmid=vmid,
            ostemplate=ostemplate,
            hostname=hostname,
            password=password,
            storage=storage,
            memory=memory,
            cores=cores,
            rootfs_size=rootfs_size,
            **kwargs,
        )

        output_format = ctx.obj.get("output_format", "json")
        if output_format == "json":
            print_json({"vmid": vmid, "task": result})
        else:
            print_success(f"Container {vmid} created successfully")
            print_success(f"Task ID: {result}")

    except Exception as e:
        if ctx.obj.get("output_format", "json") == "json":
            print_json({"error": str(e)})
        else:
            print_error(f"Failed to create container: {str(e)}")

