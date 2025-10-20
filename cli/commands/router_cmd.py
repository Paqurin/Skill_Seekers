"""
Router Command
Generate router/hub skills for large documentation
"""

import sys
import subprocess
from pathlib import Path


def generate_router(console, configs, name, output_dir):
    """Generate router skill from multiple configs"""

    # Validate config files
    valid_configs = []
    for config in configs:
        config_path = Path(config)
        if not config_path.exists():
            console.print(f"⚠️  Config not found: [yellow]{config}[/yellow]", style="yellow")
        else:
            valid_configs.append(str(config_path))

    if not valid_configs:
        console.print("❌ No valid configs provided", style="red")
        sys.exit(1)

    console.print(f"\n🔀 Generating router skill from [cyan]{len(valid_configs)}[/cyan] configs...\n")

    # Build command
    cmd = ['python3', 'cli/generate_router.py'] + valid_configs

    if name:
        cmd.extend(['--name', name])
    if output_dir:
        cmd.extend(['--output-dir', output_dir])

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Router skill generated![/green]")
    except subprocess.CalledProcessError:
        console.print(f"\n❌ Router generation failed", style="red")
        sys.exit(1)
