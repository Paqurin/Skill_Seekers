"""
Init Command
Interactive setup wizard for first-time users
"""

import sys
import json
from pathlib import Path


def init_wizard(console, preset=None):
    """Interactive setup wizard"""

    console.print("\n[bold cyan]🚀 Skill Seeker Setup Wizard[/bold cyan]")
    console.print("[dim]This wizard will help you create your first Claude skill[/dim]\n")

    # Step 1: Choose preset or custom
    if preset:
        config_path = Path(f'configs/{preset}.json')
        if not config_path.exists():
            console.print(f"❌ Preset not found: {preset}", style="red")
            sys.exit(1)
    else:
        console.print("[bold]Step 1: Choose Configuration[/bold]")
        console.print("1. Use a preset (React, Vue, Godot, etc.)")
        console.print("2. Create custom configuration\n")

        choice = input("Choose option [1/2]: ").strip()

        if choice == '1':
            # Show presets
            from .config_cmd import list_configs
            list_configs(console, format='simple')

            preset_name = input("\nEnter preset name: ").strip()
            config_path = Path(f'configs/{preset_name}.json')

            if not config_path.exists():
                console.print(f"❌ Preset not found: {preset_name}", style="red")
                sys.exit(1)
        else:
            # Custom config
            console.print("\n[bold]Create Custom Configuration[/bold]")
            name = input("Skill name: ").strip()
            url = input("Documentation URL: ").strip()
            description = input("Description: ").strip()

            # Create config
            from .config_cmd import create_config
            create_config(console, name, url, description, 100, None)

            config_path = Path(f'configs/{name}.json')

    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)

    skill_name = config.get('name', 'unknown')

    # Step 2: Estimate pages
    console.print(f"\n[bold]Step 2: Estimate Pages[/bold]")
    console.print(f"Config: [cyan]{config_path}[/cyan]")

    estimate = input("\nRun page estimation? [Y/n]: ").strip().lower()

    if estimate != 'n':
        from .scrape_cmd import estimate_pages
        estimate_pages(console, str(config_path), 1000)

    # Step 3: Confirm and start
    console.print(f"\n[bold]Step 3: Start Scraping[/bold]")
    console.print(f"Ready to scrape [cyan]{skill_name}[/cyan]")

    proceed = input("\nProceed with scraping? [Y/n]: ").strip().lower()

    if proceed == 'n':
        console.print("\n✋ Setup cancelled")
        console.print(f"\nTo run later: [cyan]ss workflow full {config_path}[/cyan]")
        return

    # Run full workflow
    console.print("\n🚀 Starting full workflow...\n")

    from .workflow_cmd import full_workflow
    full_workflow(console, str(config_path), enhance='local', upload=False)

    # Done!
    console.print("\n[bold green]✅ Setup complete![/bold green]")
    console.print(f"\nYour skill is ready: [cyan]output/{skill_name}.zip[/cyan]")
    console.print("\n💡 Next steps:")
    console.print("  1. Upload to Claude: https://claude.ai/skills")
    console.print(f"  2. Or auto-upload: [cyan]ss upload skill output/{skill_name}.zip[/cyan]")
