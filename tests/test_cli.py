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
