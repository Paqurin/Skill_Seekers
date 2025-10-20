"""
Build Command
Build skills from cached scraped data
"""

import sys
import subprocess
from pathlib import Path
from ..utils_new.validation import find_skill_directory


def build_skill(console, skill_name):
    """Build skill from cached data"""

    # Check if data exists
    data_dir = Path(f'output/{skill_name}_data')

    if not data_dir.exists():
        console.print(f"❌ No cached data found for: [red]{skill_name}[/red]", style="red")
        console.print(f"\n💡 Available options:")
        console.print(f"  1. Scrape first: [cyan]ss scrape run {skill_name}[/cyan]")
        console.print(f"  2. Check existing data: [cyan]ss status[/cyan]")
        sys.exit(1)

    # Check if there's a config file
    config_path = Path(f'configs/{skill_name}.json')

    if not config_path.exists():
        console.print(f"❌ Config not found: [red]{skill_name}.json[/red]", style="red")
        sys.exit(1)

    # Run doc_scraper with --skip-scrape
    console.print(f"\n🏗️  Building skill from cached data: [cyan]{skill_name}[/cyan]\n")

    cmd = ['python3', 'cli/doc_scraper.py', '--config', str(config_path), '--skip-scrape']

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Skill built successfully![/green]")
        console.print(f"\n💡 Next steps:")
        console.print(f"  1. Enhance: [cyan]ss enhance local {skill_name}[/cyan]")
        console.print(f"  2. Package: [cyan]ss package single {skill_name}[/cyan]")
    except subprocess.CalledProcessError:
        console.print(f"\n❌ Build failed", style="red")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n⚠️  Interrupted by user", style="yellow")
        sys.exit(130)
