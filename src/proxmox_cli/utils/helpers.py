"""Helper utility functions."""
import re
from typing import Optional


def validate_vmid(vmid: str) -> bool:
    """Validate VM/Container ID format.

    Args:
        vmid: VM or Container ID

    Returns:
        True if valid, False otherwise
    """
    return bool(re.match(r"^\d+$", str(vmid)))


def validate_ip(ip: str) -> bool:
    """Validate IP address format.

    Args:
        ip: IP address string

    Returns:
        True if valid, False otherwise
    """
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return bool(re.match(pattern, ip))


def parse_size(size_str: str) -> Optional[int]:
    """Parse size string (e.g., '10G', '512M') to bytes.

    Args:
        size_str: Size string with unit

    Returns:
        Size in bytes or None if invalid
    """
    units = {
        "K": 1024,
        "M": 1024**2,
        "G": 1024**3,
        "T": 1024**4,
    }
    
    match = re.match(r"^(\d+)([KMGT])?$", size_str.upper())
    if not match:
        return None
    
    value, unit = match.groups()
    multiplier = units.get(unit, 1) if unit else 1
    return int(value) * multiplier


def format_size(bytes: int) -> str:
    """Format bytes to human-readable size.

    Args:
        bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def format_uptime(seconds: int) -> str:
    """Format uptime in seconds to human-readable format.

    Args:
        seconds: Uptime in seconds

    Returns:
        Formatted uptime string
    """
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)
