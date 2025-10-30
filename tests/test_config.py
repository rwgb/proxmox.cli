"""Tests for configuration management."""
import pytest
from pathlib import Path
from proxmox_cli.config import Config


def test_default_config():
    """Test default configuration creation."""
    config = Config()
    assert config.get("proxmox.user") == "root@pam"
    assert config.get("proxmox.verify_ssl") is False
    assert config.get("output.format") == "table"


def test_config_get_set():
    """Test configuration get and set operations."""
    config = Config()
    config.set("test.key", "value")
    assert config.get("test.key") == "value"
    assert config.get("nonexistent.key", "default") == "default"


def test_config_nested_keys():
    """Test nested configuration keys."""
    config = Config()
    config.set("level1.level2.level3", "nested_value")
    assert config.get("level1.level2.level3") == "nested_value"
