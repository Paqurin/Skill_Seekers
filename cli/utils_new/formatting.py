"""
Output Formatting Utilities
Rich console formatting helpers
"""

from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def create_step_panel(step_num, total_steps, title, content, status="running"):
    """Create a formatted panel for workflow steps"""
    status_styles = {
        "running": ("cyan", "⏳"),
        "success": ("green", "✅"),
        "error": ("red", "❌"),
        "warning": ("yellow", "⚠️"),
    }

    style, emoji = status_styles.get(status, ("white", "○"))

    return Panel(
        content,
        title=f"[{style}]{emoji} Step {step_num}/{total_steps}: {title}[/{style}]",
        border_style=style,
        padding=(1, 2)
    )


def create_progress_bar():
    """Create a rich progress bar for long operations"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )


def create_summary_table(title, data):
    """
    Create a summary table
    data = [(label, value, style), ...]
    """
    table = Table(title=title, show_header=False, box=None)
    table.add_column("Label", style="cyan")
    table.add_column("Value")

    for item in data:
        if len(item) == 3:
            label, value, style = item
            table.add_row(label, f"[{style}]{value}[/{style}]")
        else:
            label, value = item
            table.add_row(label, str(value))

    return table
