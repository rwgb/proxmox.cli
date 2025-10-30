"""Proxmox API client wrapper."""

from typing import Optional, Dict, Any
from proxmoxer import ProxmoxAPI
import urllib3


class ProxmoxClient:
    """Wrapper for Proxmox API client."""

    def __init__(
        self,
        host: str,
        user: str,
        password: Optional[str] = None,
        token_name: Optional[str] = None,
        token_value: Optional[str] = None,
        verify_ssl: bool = True,
    ):
        """Initialize Proxmox client.

        Args:
            host: Proxmox host address
            user: Username for authentication
            password: Password for authentication (optional if using token)
            token_name: API token name (optional)
            token_value: API token value (optional)
            verify_ssl: Whether to verify SSL certificate
        """
        self.host = host
        self.user = user
        self.verify_ssl = verify_ssl

        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Authenticate with password or token
        if token_name and token_value:
            self.api = ProxmoxAPI(
                host,
                user=user,
                token_name=token_name,
                token_value=token_value,
                verify_ssl=verify_ssl,
                timeout=30,
            )
        elif password:
            self.api = ProxmoxAPI(
                host,
                user=user,
                password=password,
                verify_ssl=verify_ssl,
                timeout=30,
            )
        else:
            raise ValueError("Either password or token credentials must be provided")

    def get_version(self) -> Dict[str, Any]:
        """Get Proxmox version information.

        Returns:
            Version information dictionary
        """
        return self.api.version.get()

    def get_cluster_status(self) -> list:
        """Get cluster status.

        Returns:
            List of cluster status information
        """
        return self.api.cluster.status.get()

    def get_nodes(self) -> list:
        """Get list of nodes in the cluster.

        Returns:
            List of node information dictionaries
        """
        return self.api.nodes.get()

    def get_vms(self, node: Optional[str] = None) -> list:
        """Get list of virtual machines.

        Args:
            node: Optional node name to filter VMs

        Returns:
            List of VM information dictionaries
        """
        if node:
            return self.api.nodes(node).qemu.get()

        # Get VMs from all nodes, skipping unreachable nodes
        vms = []
        for node_info in self.get_nodes():
            node_name = node_info["node"]
            try:
                node_vms = self.api.nodes(node_name).qemu.get()
                vms.extend(node_vms)
            except Exception:
                # Skip nodes that fail to respond (offline, network issues, etc.)
                continue
        return vms

    def get_containers(self, node: Optional[str] = None) -> list:
        """Get list of LXC containers.

        Args:
            node: Optional node name to filter containers

        Returns:
            List of container information dictionaries
        """
        if node:
            return self.api.nodes(node).lxc.get()

        # Get containers from all nodes, skipping unreachable nodes
        containers = []
        for node_info in self.get_nodes():
            node_name = node_info["node"]
            try:
                node_containers = self.api.nodes(node_name).lxc.get()
                containers.extend(node_containers)
            except Exception:
                # Skip nodes that fail to respond (offline, network issues, etc.)
                continue
        return containers
