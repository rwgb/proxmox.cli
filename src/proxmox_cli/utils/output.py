"""Output formatting utilities."""
from typing import List, Dict, Any
from enum import Enum
import json
from tabulate import tabulate
from rich.console import Console
from rich.table import Table


class OutputFormat(Enum):
    """Output format options."""

    TABLE = "table"
    JSON = "json"
    YAML = "yaml"
    PLAIN = "plain"


console = Console()


def format_output(data: Any, format: OutputFormat = OutputFormat.TABLE, headers: List[str] = None) -> str:
    """Format output data according to specified format.

    Args:
        data: Data to format
        format: Output format
        headers: Optional list of headers for table format

    Returns:
        Formatted string
    """
    if format == OutputFormat.JSON:
        return json.dumps(data, indent=2)
    
    elif format == OutputFormat.TABLE:
        if isinstance(data, list) and data:
            if headers is None:
                headers = list(data[0].keys()) if isinstance(data[0], dict) else []
            return tabulate(data, headers="keys" if not headers else headers, tablefmt="grid")
        return str(data)
    
    elif format == OutputFormat.YAML:
        import yaml
        return yaml.dump(data, default_flow_style=False)
    
    else:  # PLAIN
        return str(data)


def print_table(data: List[Dict[str, Any]], title: str = None) -> None:
    """Print data as a rich table.

    Args:
        data: List of dictionaries to display
        title: Optional table title
    """
    if not data:
        console.print("[yellow]No data to display[/yellow]")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    # Add columns
    for key in data[0].keys():
        table.add_column(str(key).upper())
    
    # Add rows
    for item in data:
        table.add_row(*[str(v) for v in item.values()])
    
    console.print(table)


def print_success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message to print
    """
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message.

    Args:
        message: Error message to print
    """
    console.print(f"[red]✗[/red] {message}", style="red")


def print_warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message to print
    """
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def print_info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to print
    """
    console.print(f"[blue]ℹ[/blue] {message}", style="blue")
