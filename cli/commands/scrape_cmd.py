"""
Scrape Commands
Documentation scraping operations
"""

import sys
import subprocess
from pathlib import Path
from ..utils_new.validation import find_config
from ..utils_new.formatting import create_step_panel


def run_scrape(console, config, skip_scrape, resume, fresh, max_pages):
    """Run documentation scraping"""
    # Find config file
    config_path = find_config(config)

    if not config_path:
        console.print(f"❌ Config not found: {config}", style="red")
        console.print("\n💡 Try: [cyan]ss config list[/cyan] to see available configs")
        sys.exit(1)

    # Build command
    cmd = ['python3', 'cli/doc_scraper.py', '--config', str(config_path)]

    if skip_scrape:
        cmd.append('--skip-scrape')
    if resume:
        cmd.append('--resume')
    if fresh:
        cmd.append('--fresh')
    if max_pages:
        cmd.extend(['--max-pages', str(max_pages)])

    # Show what we're doing
    console.print(create_step_panel(
        1, 1,
        "Scraping Documentation",
        f"Config: [cyan]{config_path}[/cyan]\n"
        f"Skip scrape: {skip_scrape}\n"
        f"Resume: {resume}",
        status="running"
    ))

    # Run scraper
    try:
        result = subprocess.run(cmd, check=True)
        console.print("\n✅ Scraping complete!", style="green bold")
    except subprocess.CalledProcessError:
        console.print("\n❌ Scraping failed", style="red bold")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n\n⚠️  Interrupted by user", style="yellow")
        sys.exit(130)


def estimate_pages(console, config, max_discovery):
    """Estimate page count before scraping"""
    config_path = find_config(config)

    if not config_path:
        console.print(f"❌ Config not found: {config}", style="red")
        sys.exit(1)

    # Run estimator
    cmd = ['python3', 'cli/estimate_pages.py', str(config_path), '--max-discovery', str(max_discovery)]

    try:
        console.print(f"🔍 Estimating pages for: [cyan]{config_path}[/cyan]\n")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        console.print("\n❌ Estimation failed", style="red")
        sys.exit(1)


def dry_run(console, config):
    """Preview what will be scraped"""
    config_path = find_config(config)

    if not config_path:
        console.print(f"❌ Config not found: {config}", style="red")
        sys.exit(1)

    cmd = ['python3', 'cli/doc_scraper.py', '--config', str(config_path), '--dry-run']

    try:
        console.print(f"👁️  Dry run for: [cyan]{config_path}[/cyan]\n")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        console.print("\n❌ Dry run failed", style="red")
        sys.exit(1)
