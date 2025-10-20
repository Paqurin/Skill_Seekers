"""
Configuration Management Commands
Handles listing, creating, validating, and splitting configs
"""

import json
import sys
from pathlib import Path
from rich.table import Table
from rich.panel import Panel


def list_configs(console, format='table'):
    """List all available preset configurations"""
    configs_dir = Path('configs')

    if not configs_dir.exists():
        console.print("❌ No configs directory found", style="red")
        return

    config_files = sorted(configs_dir.glob('*.json'))

    if not config_files:
        console.print("❌ No configuration files found", style="red")
        return

    if format == 'table':
        table = Table(title="📋 Available Configurations", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Description", style="white")
        table.add_column("Max Pages", justify="right", style="yellow")
        table.add_column("Status", style="blue")

        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)

                name = config.get('name', config_file.stem)
                description = config.get('description', 'No description')[:50]
                max_pages = config.get('max_pages', '?')

                # Check if data exists
                data_dir = Path(f'output/{name}_data')
                status = "✓ cached" if data_dir.exists() else "—"

                table.add_row(name, description, str(max_pages), status)

            except Exception as e:
                console.print(f"⚠️  Error loading {config_file.name}: {e}", style="yellow")

        console.print(table)
        console.print(f"\n💡 Use: [cyan]ss scrape run <config-name>[/cyan] to scrape")

    elif format == 'json':
        configs = []
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                configs.append({
                    'file': str(config_file),
                    'name': config.get('name', config_file.stem),
                    'description': config.get('description', ''),
                    'max_pages': config.get('max_pages', 0)
                })
            except:
                pass

        console.print_json(data=configs)

    else:  # simple
        for config_file in config_files:
            console.print(f"  {config_file.stem}")


def create_config(console, name, url, description, max_pages, output):
    """Create a new configuration file"""
    from ..utils_new.validation import validate_config_name, validate_url

    # Validate inputs
    if not validate_config_name(name):
        console.print("❌ Invalid name (use only letters, numbers, hyphens, underscores)", style="red")
        return

    if not validate_url(url):
        console.print("❌ Invalid URL (must start with http:// or https://)", style="red")
        return

    # Create config dictionary
    config = {
        "name": name,
        "description": description,
        "base_url": url if url.endswith('/') else url + '/',
        "selectors": {
            "main_content": "div[role='main']",
            "title": "title",
            "code_blocks": "pre code"
        },
        "url_patterns": {
            "include": [],
            "exclude": []
        },
        "categories": {},
        "rate_limit": 0.5,
        "max_pages": max_pages
    }

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = Path(f'configs/{name}.json')

    # Ensure configs directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save config
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)

    console.print(f"\n✅ Config created: [green]{output_path}[/green]")
    console.print(f"\n💡 Next steps:")
    console.print(f"  1. Edit selectors if needed: [cyan]{output_path}[/cyan]")
    console.print(f"  2. Run: [cyan]ss scrape estimate {name}[/cyan]")
    console.print(f"  3. Run: [cyan]ss scrape run {name}[/cyan]")


def validate_config(console, config_path):
    """Validate a configuration file"""
    # Import validation from doc_scraper
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from doc_scraper import validate_config as validate, load_config

    try:
        config = load_config(config_path)
        errors, warnings = validate(config)

        if not errors and not warnings:
            console.print(f"✅ Config is valid: [green]{config_path}[/green]")
            console.print(Panel.fit(
                f"[green]Name:[/green] {config.get('name')}\n"
                f"[green]URL:[/green] {config.get('base_url')}\n"
                f"[green]Max Pages:[/green] {config.get('max_pages', '?')}",
                title="Configuration Details",
                border_style="green"
            ))
            return

        if warnings:
            console.print(f"\n⚠️  [yellow]Warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  • {warning}", style="yellow")

        if errors:
            console.print(f"\n❌ [red]Errors:[/red]")
            for error in errors:
                console.print(f"  • {error}", style="red")
            sys.exit(1)

    except Exception as e:
        console.print(f"❌ Failed to load config: {e}", style="red")
        sys.exit(1)


def split_config(console, config_path, strategy, target_pages, dry_run):
    """Split large configuration into multiple focused configs"""
    # Import from split_config.py
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from split_config import ConfigSplitter

    with console.status(f"[cyan]Analyzing config for splitting..."):
        splitter = ConfigSplitter(config_path, strategy, target_pages)
        configs = splitter.split()

    if dry_run:
        console.print("\n[yellow]DRY RUN - No files saved[/yellow]")

        table = Table(title="Split Preview", show_header=True, header_style="bold cyan")
        table.add_column("Config Name", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Categories", style="white")

        for cfg in configs:
            is_router = cfg.get('_router', False)
            config_type = "Router" if is_router else "Sub-skill"
            categories = ", ".join(cfg.get('categories', {}).keys())

            table.add_row(cfg['name'], config_type, categories)

        console.print(table)
        console.print(f"\n💡 Run without --dry-run to save {len(configs)} config files")

    else:
        saved_files = splitter.save_configs(configs)

        console.print(f"\n✅ Created {len(saved_files)} configuration files:")
        for filepath in saved_files:
            console.print(f"  [green]✓[/green] {filepath}")

        console.print(f"\n💡 Next steps:")
        console.print("  1. Review generated configs")
        console.print("  2. Scrape each config (can run in parallel):")
        for filepath in saved_files:
            console.print(f"     [cyan]ss scrape run {filepath}[/cyan]")

        if any(cfg.get('_router', False) for cfg in configs):
            console.print("  3. Router skill will intelligently direct queries to sub-skills")
