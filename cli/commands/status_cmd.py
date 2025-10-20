"""
Status Command
Shows project overview, cached data, built skills, suggestions
"""

import json
from pathlib import Path
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns


def show_status(console, detailed=False):
    """Show comprehensive project status"""

    console.print("\n[bold cyan]╔══════════════════════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║        📊 Skill Seeker Project Status                   ║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════════════════════╝[/bold cyan]\n")

    # 1. Configurations
    _show_configs_status(console, detailed)

    # 2. Cached Data
    _show_cached_data_status(console, detailed)

    # 3. Built Skills
    _show_built_skills_status(console, detailed)

    # 4. Packaged Skills
    _show_packaged_skills_status(console, detailed)

    # 5. API Key Status
    _show_api_key_status(console)

    # 6. Suggestions
    _show_suggestions(console)


def _show_configs_status(console, detailed):
    """Show available configurations"""
    configs_dir = Path('configs')
    if not configs_dir.exists():
        return

    config_files = list(configs_dir.glob('*.json'))

    if config_files:
        console.print(f"[bold]📋 Configurations:[/bold] {len(config_files)} presets")

        if detailed:
            table = Table(show_header=True, header_style="bold cyan", box=None)
            table.add_column("Name", style="green")
            table.add_column("Max Pages", justify="right")

            for config_file in sorted(config_files)[:10]:
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    table.add_row(
                        config.get('name', config_file.stem),
                        str(config.get('max_pages', '?'))
                    )
                except:
                    pass

            console.print(table)
        else:
            # Show first few
            names = [f.stem for f in sorted(config_files)[:5]]
            more = len(config_files) - 5
            display = ", ".join(names)
            if more > 0:
                display += f", +{more} more"
            console.print(f"   └─ {display}")

        console.print()


def _show_cached_data_status(console, detailed):
    """Show cached scraped data"""
    output_dir = Path('output')
    if not output_dir.exists():
        return

    data_dirs = list(output_dir.glob('*_data'))

    if data_dirs:
        console.print(f"[bold]💾 Cached Data:[/bold] {len(data_dirs)} skills")

        for data_dir in sorted(data_dirs):
            # Get summary
            summary_file = data_dir / "summary.json"
            if summary_file.exists():
                try:
                    with open(summary_file, 'r') as f:
                        summary = json.load(f)

                    pages = summary.get('total_pages', 0)
                    name = summary.get('name', data_dir.stem.replace('_data', ''))

                    # Calculate size
                    size = sum(f.stat().st_size for f in data_dir.rglob('*') if f.is_file())
                    size_str = _format_size(size)

                    console.print(f"   ├─ [green]{name}[/green] ({pages} pages, {size_str})")

                except:
                    console.print(f"   ├─ {data_dir.stem}")
            else:
                console.print(f"   ├─ {data_dir.stem}")

        console.print()


def _show_built_skills_status(console, detailed):
    """Show built skills (with SKILL.md)"""
    output_dir = Path('output')
    if not output_dir.exists():
        return

    # Find directories with SKILL.md
    skill_dirs = []
    for item in output_dir.iterdir():
        if item.is_dir() and not item.name.endswith('_data'):
            if (item / "SKILL.md").exists():
                skill_dirs.append(item)

    if skill_dirs:
        console.print(f"[bold]🏗️  Built Skills:[/bold] {len(skill_dirs)} skills")

        for skill_dir in sorted(skill_dirs):
            # Count reference files
            refs_dir = skill_dir / "references"
            ref_count = len(list(refs_dir.glob('*.md'))) if refs_dir.exists() else 0

            # Check if enhanced
            has_backup = (skill_dir / "SKILL.md.backup").exists()
            enhanced = " (enhanced)" if has_backup else ""

            console.print(f"   ├─ [green]{skill_dir.name}[/green] (SKILL.md + {ref_count} references{enhanced})")

        console.print()


def _show_packaged_skills_status(console, detailed):
    """Show packaged .zip files"""
    output_dir = Path('output')
    if not output_dir.exists():
        return

    zip_files = list(output_dir.glob('*.zip'))

    if zip_files:
        console.print(f"[bold]📦 Packaged:[/bold] {len(zip_files)} skills")

        for zip_file in sorted(zip_files):
            size = zip_file.stat().st_size
            size_str = _format_size(size)
            console.print(f"   └─ [green]{zip_file.name}[/green] ({size_str})")

        console.print()


def _show_api_key_status(console):
    """Show API key configuration status"""
    import os

    api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()

    if api_key:
        console.print("[bold]🔑 API Key:[/bold] [green]✓ Configured[/green]")
        console.print("   └─ Auto-upload enabled\n")
    else:
        console.print("[bold]🔑 API Key:[/bold] [yellow]○ Not configured[/yellow]")
        console.print("   └─ Manual upload only\n")


def _show_suggestions(console):
    """Show smart suggestions based on current state"""
    suggestions = []

    output_dir = Path('output')
    if output_dir.exists():
        # Find cached data without built skills
        for data_dir in output_dir.glob('*_data'):
            skill_name = data_dir.stem.replace('_data', '')
            skill_dir = output_dir / skill_name

            if not skill_dir.exists() or not (skill_dir / "SKILL.md").exists():
                suggestions.append(f"Build '{skill_name}' from cached data: [cyan]ss build {skill_name}[/cyan]")

        # Find built skills without packages
        for skill_dir in output_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.endswith('_data'):
                if (skill_dir / "SKILL.md").exists():
                    zip_file = output_dir / f"{skill_dir.name}.zip"
                    if not zip_file.exists():
                        suggestions.append(f"Package '{skill_dir.name}' skill: [cyan]ss package single {skill_dir.name}[/cyan]")

    if suggestions:
        console.print("[bold]💡 Suggestions:[/bold]")
        for suggestion in suggestions[:5]:  # Show max 5
            console.print(f"   • {suggestion}")
        console.print()


def _format_size(size_bytes):
    """Format bytes to human-readable size"""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
