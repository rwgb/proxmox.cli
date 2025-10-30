#!/usr/bin/env python3
"""Example usage of Proxmox CLI API."""

from proxmox_cli.client import ProxmoxClient
from proxmox_cli.config import Config
from proxmox_cli.utils.output import print_table, print_success, print_error


def main():
    """Example usage of Proxmox CLI programmatically."""
    
    # Load configuration
    config = Config()
    
    # Create client
    try:
        client = ProxmoxClient(
            host=config.get("proxmox.host", "proxmox.example.com"),
            user=config.get("proxmox.user", "root@pam"),
            password="your-password",  # In production, use secure password management
            verify_ssl=config.get("proxmox.verify_ssl", False),
        )
    except Exception as e:
        print_error(f"Failed to connect: {e}")
        return
    
    # Get cluster version
    try:
        version = client.get_version()
        print_success(f"Connected to Proxmox {version.get('version', 'unknown')}")
    except Exception as e:
        print_error(f"Failed to get version: {e}")
    
    # List all nodes
    try:
        nodes = client.get_nodes()
        print_table(nodes, title="Cluster Nodes")
    except Exception as e:
        print_error(f"Failed to list nodes: {e}")
    
    # List all VMs
    try:
        vms = client.get_vms()
        print_table(vms, title="Virtual Machines")
    except Exception as e:
        print_error(f"Failed to list VMs: {e}")
    
    # List all containers
    try:
        containers = client.get_containers()
        print_table(containers, title="LXC Containers")
    except Exception as e:
        print_error(f"Failed to list containers: {e}")


if __name__ == "__main__":
    main()
