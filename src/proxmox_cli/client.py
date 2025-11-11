"""Proxmox API client wrapper."""

from typing import Any, Dict, Optional

import urllib3
from proxmoxer import ProxmoxAPI


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

    def get_pools(self) -> list:
        """Get list of resource pools.

        Returns:
            List of resource pool information dictionaries
        """
        return self.api.pools.get()

    def get_pool(self, poolid: str) -> Dict[str, Any]:
        """Get resource pool details.

        Args:
            poolid: Pool identifier

        Returns:
            Pool information dictionary including members
        """
        return self.api.pools(poolid).get()

    def create_pool(self, poolid: str, comment: Optional[str] = None) -> None:
        """Create a new resource pool.

        Args:
            poolid: Pool identifier
            comment: Optional comment/description
        """
        pool_data = {"poolid": poolid}
        if comment:
            pool_data["comment"] = comment
        self.api.pools.post(**pool_data)

    def update_pool(self, poolid: str, comment: Optional[str] = None) -> None:
        """Update resource pool information.

        Args:
            poolid: Pool identifier
            comment: Optional comment/description
        """
        if comment:
            self.api.pools(poolid).put(comment=comment)

    def delete_pool(self, poolid: str) -> None:
        """Delete a resource pool.

        Args:
            poolid: Pool identifier
        """
        self.api.pools(poolid).delete()

    def add_pool_members(
        self, poolid: str, vms: Optional[list] = None, storages: Optional[list] = None
    ) -> None:
        """Add members to a resource pool.

        Args:
            poolid: Pool identifier
            vms: Optional list of VM IDs
            storages: Optional list of storage IDs
        """
        update_data = {}
        if vms:
            update_data["vms"] = ",".join(str(vm) for vm in vms)
        if storages:
            update_data["storage"] = ",".join(storages)
        if update_data:
            self.api.pools(poolid).put(**update_data)

    def remove_pool_members(
        self, poolid: str, vms: Optional[list] = None, storages: Optional[list] = None
    ) -> None:
        """Remove members from a resource pool.

        Args:
            poolid: Pool identifier
            vms: Optional list of VM IDs
            storages: Optional list of storage IDs
        """
        delete_data = {"delete": 1}
        if vms:
            delete_data["vms"] = ",".join(str(vm) for vm in vms)
        if storages:
            delete_data["storage"] = ",".join(storages)
        if len(delete_data) > 1:  # More than just 'delete' key
            self.api.pools(poolid).put(**delete_data)

    def get_storage_content(
        self, node: str, storage: str, content_type: Optional[str] = None
    ) -> list:
        """Get storage content list.

        Args:
            node: Node name
            storage: Storage identifier
            content_type: Optional content type filter (vztmpl, iso, backup, etc.)

        Returns:
            List of storage content items
        """
        params = {}
        if content_type:
            params["content"] = content_type
        return self.api.nodes(node).storage(storage).content.get(**params)

    def get_container_templates(
        self, node: Optional[str] = None, storage: Optional[str] = None
    ) -> list:
        """Get available LXC container templates.

        Args:
            node: Optional node name to filter templates
            storage: Optional storage name to filter templates

        Returns:
            List of template information dictionaries
        """
        templates = []

        # Get nodes to check
        nodes_to_check = [node] if node else [n["node"] for n in self.get_nodes()]

        for node_name in nodes_to_check:
            try:
                # Get storage list for this node
                storages = self.api.nodes(node_name).storage.get()

                for storage_info in storages:
                    storage_name = storage_info["storage"]

                    # Skip if specific storage requested and doesn't match
                    if storage and storage != storage_name:
                        continue

                    # Check if storage type supports container templates
                    storage_type = storage_info.get("type", "")
                    if storage_type not in ["dir", "nfs", "cifs", "glusterfs", "zfspool"]:
                        continue

                    try:
                        # Get templates from this storage
                        content = (
                            self.api.nodes(node_name)
                            .storage(storage_name)
                            .content.get(content="vztmpl")
                        )

                        for item in content:
                            template_info = {
                                "volid": item.get("volid"),
                                "storage": storage_name,
                                "node": node_name,
                                "size": item.get("size", 0),
                                "format": item.get("format", ""),
                            }
                            templates.append(template_info)
                    except Exception:
                        # Skip storages that don't have template content or are inaccessible
                        continue
            except Exception:
                # Skip nodes that are unreachable
                continue

        return templates

    def download_container_template(self, node: str, storage: str, template: str) -> Dict[str, Any]:
        """Download a container template from a repository.

        Args:
            node: Node name where to download the template
            storage: Storage identifier where to store the template
            template: Template name (e.g., 'ubuntu-22.04-standard_22.04-1_amd64.tar.zst')

        Returns:
            Task information dictionary
        """
        result = self.api.nodes(node).aplinfo.post(storage=storage, template=template)
        return result

    def get_available_templates(self, node: str) -> list:
        """Get list of available templates that can be downloaded.

        Args:
            node: Node name

        Returns:
            List of available template information
        """
        return self.api.nodes(node).aplinfo.get()

    def create_container(
        self,
        node: str,
        vmid: int,
        ostemplate: str,
        hostname: Optional[str] = None,
        password: Optional[str] = None,
        storage: str = "local-lvm",
        memory: int = 512,
        cores: int = 1,
        rootfs_size: int = 8,
        **kwargs,
    ) -> str:
        """Create a new LXC container.

        Args:
            node: Node name where to create the container
            vmid: Container ID
            ostemplate: Template volume ID (e.g., 'local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst')
            hostname: Container hostname
            password: Root password
            storage: Storage for container root filesystem
            memory: Memory in MB
            cores: Number of CPU cores
            rootfs_size: Root filesystem size in GB
            **kwargs: Additional parameters

        Returns:
            Task ID (UPID)
        """
        container_data = {
            "vmid": vmid,
            "ostemplate": ostemplate,
            "storage": storage,
            "memory": memory,
            "cores": cores,
            "rootfs": f"{storage}:{rootfs_size}",
        }

        if hostname:
            container_data["hostname"] = hostname
        if password:
            container_data["password"] = password

        # Add any additional parameters
        container_data.update(kwargs)

        return self.api.nodes(node).lxc.post(**container_data)
