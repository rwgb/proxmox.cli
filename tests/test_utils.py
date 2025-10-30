"""Tests for utility functions."""

import pytest

from proxmox_cli.utils.helpers import (
    format_size,
    format_uptime,
    parse_size,
    validate_ip,
    validate_vmid,
)


def test_validate_vmid():
    """Test VMID validation."""
    assert validate_vmid("100") is True
    assert validate_vmid("999") is True
    assert validate_vmid("abc") is False
    assert validate_vmid("10a") is False


def test_validate_ip():
    """Test IP address validation."""
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("10.0.0.1") is True
    assert validate_ip("256.1.1.1") is False
    assert validate_ip("192.168.1") is False
    assert validate_ip("not.an.ip.address") is False


def test_parse_size():
    """Test size parsing."""
    assert parse_size("1024") == 1024
    assert parse_size("1K") == 1024
    assert parse_size("1M") == 1024 * 1024
    assert parse_size("1G") == 1024 * 1024 * 1024
    assert parse_size("invalid") is None


def test_format_size():
    """Test size formatting."""
    assert "1.00 KB" in format_size(1024)
    assert "1.00 MB" in format_size(1024 * 1024)
    assert "1.00 GB" in format_size(1024 * 1024 * 1024)


def test_format_uptime():
    """Test uptime formatting."""
    assert format_uptime(90) == "1m 30s"
    assert format_uptime(3661) == "1h 1m 1s"
    assert format_uptime(86400) == "1d"
