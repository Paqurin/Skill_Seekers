"""
Workflow Commands
High-level workflow automation (scrape → build → enhance → package → upload)
"""

import sys
import subprocess
import time
from pathlib import Path
from ..utils_new.validation import find_config
from ..utils_new.formatting import create_step_panel


def quick_workflow(console, config, upload):
    """Quick workflow: scrape → build → package"""
    console.print("\n[bold cyan]⚡ Quick Workflow[/bold cyan]")
    console.print("[dim]Steps: Scrape → Build → Package[/dim]\n")

    # Find config
    config_path = find_config(config)
    if not config_path:
        console.print(f"❌ Config not found: {config}", style="red")
        sys.exit(1)

    # Load config to get skill name
    import json
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    skill_name = config_data.get('name', 'unknown')

    steps = [
        ("Scrape documentation", ['python3', 'cli/doc_scraper.py', '--config', str(config_path)]),
        ("Package skill", ['python3', 'cli/package_skill.py', f'output/{skill_name}/']),
    ]

    if upload:
        steps.append(("Upload to Claude", ['python3', 'cli/upload_skill.py', f'output/{skill_name}.zip']))

    # Run steps
    for i, (step_name, cmd) in enumerate(steps, 1):
        console.print(create_step_panel(
            i, len(steps), step_name,
            f"Running: [dim]{' '.join(cmd)}[/dim]",
            status="running"
        ))

        try:
            result = subprocess.run(cmd, check=True)
            console.print(f"[green]✅ {step_name} complete![/green]\n")
        except subprocess.CalledProcessError:
            console.print(f"[red]❌ {step_name} failed[/red]", style="red")
            sys.exit(1)
        except KeyboardInterrupt:
            console.print("\n⚠️  Interrupted by user", style="yellow")
            sys.exit(130)

    console.print("\n[bold green]🎉 Quick workflow complete![/bold green]")


def full_workflow(console, config, enhance, upload):
    """Full workflow: scrape → build → enhance → package → upload"""
    console.print("\n[bold cyan]⚡ Full Workflow[/bold cyan]")
    console.print("[dim]Steps: Scrape → Build → Enhance → Package → Upload[/dim]\n")

    # Find config
    config_path = find_config(config)
    if not config_path:
        console.print(f"❌ Config not found: {config}", style="red")
        sys.exit(1)

    # Load config to get skill name
    import json
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    skill_name = config_data.get('name', 'unknown')

    # Build step list
    steps = [
        ("Scrape documentation", ['python3', 'cli/doc_scraper.py', '--config', str(config_path)]),
    ]

    if enhance == 'local':
        steps.append(("Enhance (local)", ['python3', 'cli/enhance_skill_local.py', f'output/{skill_name}/']))
    elif enhance == 'api':
        steps.append(("Enhance (API)", ['python3', 'cli/enhance_skill.py', f'output/{skill_name}/']))

    steps.append(("Package skill", ['python3', 'cli/package_skill.py', f'output/{skill_name}/']))

    if upload:
        steps.append(("Upload to Claude", ['python3', 'cli/upload_skill.py', f'output/{skill_name}.zip']))

    # Run steps
    start_time = time.time()

    for i, (step_name, cmd) in enumerate(steps, 1):
        step_start = time.time()

        console.print(create_step_panel(
            i, len(steps), step_name,
            f"Running: [dim]{' '.join(cmd)}[/dim]",
            status="running"
        ))

        try:
            result = subprocess.run(cmd, check=True)
            elapsed = time.time() - step_start
            console.print(f"[green]✅ {step_name} complete! ({elapsed:.1f}s)[/green]\n")
        except subprocess.CalledProcessError:
            console.print(f"[red]❌ {step_name} failed[/red]")
            sys.exit(1)
        except KeyboardInterrupt:
            console.print("\n⚠️  Interrupted by user", style="yellow")
            sys.exit(130)

    total_time = time.time() - start_time
    console.print(f"\n[bold green]🎉 Full workflow complete! ({total_time/60:.1f} minutes)[/bold green]")


def rebuild_workflow(console, skill_name, enhance, upload):
    """Fast rebuild: build → enhance → package (uses cached data)"""
    console.print("\n[bold cyan]⚡ Rebuild Workflow[/bold cyan]")
    console.print("[dim]Steps: Build (from cache) → Enhance → Package[/dim]\n")

    # Check if cached data exists
    data_dir = Path(f'output/{skill_name}_data')
    if not data_dir.exists():
        console.print(f"❌ No cached data found for: {skill_name}", style="red")
        console.print(f"\n💡 Run scraping first: [cyan]ss scrape run {skill_name}[/cyan]")
        sys.exit(1)

    # Build steps
    steps = [
        ("Build from cache", ['python3', 'cli/doc_scraper.py', '--name', skill_name, '--skip-scrape']),
    ]

    if enhance == 'local':
        steps.append(("Enhance (local)", ['python3', 'cli/enhance_skill_local.py', f'output/{skill_name}/']))
    elif enhance == 'api':
        steps.append(("Enhance (API)", ['python3', 'cli/enhance_skill.py', f'output/{skill_name}/']))

    steps.append(("Package skill", ['python3', 'cli/package_skill.py', f'output/{skill_name}/']))

    if upload:
        steps.append(("Upload to Claude", ['python3', 'cli/upload_skill.py', f'output/{skill_name}.zip']))

    # Run steps
    for i, (step_name, cmd) in enumerate(steps, 1):
        console.print(create_step_panel(
            i, len(steps), step_name,
            f"Running: [dim]{' '.join(cmd)}[/dim]",
            status="running"
        ))

        try:
            result = subprocess.run(cmd, check=True)
            console.print(f"[green]✅ {step_name} complete![/green]\n")
        except subprocess.CalledProcessError:
            console.print(f"[red]❌ {step_name} failed[/red]")
            sys.exit(1)

    console.print("\n[bold green]🎉 Rebuild workflow complete![/bold green]")
