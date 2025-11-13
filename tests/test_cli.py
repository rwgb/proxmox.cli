"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner

from proxmox_cli.cli import main


def test_cli_version():
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Proxmox CLI" in result.output


def test_vm_command_group():
    """Test VM command group."""
    runner = CliRunner()
    result = runner.invoke(main, ["vm", "--help"])
    assert result.exit_code == 0
    assert "virtual machines" in result.output.lower()


def test_container_command_group():
    """Test container command group."""
    runner = CliRunner()
    result = runner.invoke(main, ["container", "--help"])
    assert result.exit_code == 0
    assert "container" in result.output.lower()


def test_container_templates_command():
    """Test container templates command."""
    runner = CliRunner()
    result = runner.invoke(main, ["container", "templates", "--help"])
    assert result.exit_code == 0
    assert "templates" in result.output.lower()


def test_container_available_templates_command():
    """Test container available-templates command."""
    runner = CliRunner()
    result = runner.invoke(main, ["container", "available-templates", "--help"])
    assert result.exit_code == 0
    assert "available" in result.output.lower() or "download" in result.output.lower()


def test_container_download_template_command():
    """Test container download-template command."""
    runner = CliRunner()
    result = runner.invoke(main, ["container", "download-template", "--help"])
    assert result.exit_code == 0
    assert "download" in result.output.lower()


def test_container_create_command():
    """Test container create command."""
    runner = CliRunner()
    result = runner.invoke(main, ["container", "create", "--help"])
    assert result.exit_code == 0
    assert "create" in result.output.lower()


def test_storage_command_group():
    """Test storage command group."""
    runner = CliRunner()
    result = runner.invoke(main, ["storage", "--help"])
    assert result.exit_code == 0
    assert "storage" in result.output.lower()


def test_storage_list_command():
    """Test storage list command."""
    runner = CliRunner()
    result = runner.invoke(main, ["storage", "list", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output.lower()


def test_storage_create_command():
    """Test storage create command."""
    runner = CliRunner()
    result = runner.invoke(main, ["storage", "create", "--help"])
    assert result.exit_code == 0
    assert "create" in result.output.lower()
    assert "storage" in result.output.lower()
