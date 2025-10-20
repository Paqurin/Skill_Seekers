"""
Package Commands
Package skills into .zip files for Claude upload
"""

import sys
import subprocess
from pathlib import Path
from ..utils_new.validation import find_skill_directory


def package_single(console, skill_name, upload, open_folder):
    """Package a single skill"""

    # Find skill directory
    skill_dir = find_skill_directory(skill_name)

    if not skill_dir:
        console.print(f"❌ Skill not found: [red]{skill_name}[/red]", style="red")
        console.print(f"\n💡 Build the skill first: [cyan]ss build {skill_name}[/cyan]")
        sys.exit(1)

    console.print(f"\n📦 Packaging skill: [cyan]{skill_name}[/cyan]\n")

    # Build command
    cmd = ['python3', 'cli/package_skill.py', str(skill_dir)]

    if not open_folder:
        cmd.append('--no-open')

    if upload:
        cmd.append('--upload')

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Packaging complete![/green]")

        zip_path = Path(f'output/{skill_name}.zip')
        if zip_path.exists():
            size = zip_path.stat().st_size / (1024 * 1024)
            console.print(f"   Package: [cyan]{zip_path}[/cyan] ({size:.1f} MB)")

        if not upload:
            console.print(f"\n💡 To upload: [cyan]ss upload skill output/{skill_name}.zip[/cyan]")

    except subprocess.CalledProcessError:
        console.print(f"\n❌ Packaging failed", style="red")
        sys.exit(1)


def package_multi(console, pattern, upload):
    """Package multiple skills matching pattern"""

    # Find matching skill directories
    output_dir = Path('output')
    matches = []

    for item in output_dir.glob(pattern):
        if item.is_dir() and (item / "SKILL.md").exists():
            matches.append(item)

    if not matches:
        console.print(f"❌ No skills found matching: [red]{pattern}[/red]", style="red")
        sys.exit(1)

    console.print(f"\n📦 Packaging [cyan]{len(matches)}[/cyan] skills...\n")

    success = 0
    failed = 0

    for skill_dir in matches:
        console.print(f"  Packaging: {skill_dir.name}...", end=" ")

        cmd = ['python3', 'cli/package_skill.py', str(skill_dir), '--no-open']
        if upload:
            cmd.append('--upload')

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            console.print("[green]✓[/green]")
            success += 1
        except subprocess.CalledProcessError:
            console.print("[red]✗[/red]")
            failed += 1

    console.print(f"\n✅ Packaged [green]{success}[/green] skills")
    if failed > 0:
        console.print(f"❌ Failed: [red]{failed}[/red]", style="yellow")


def package_all(console, upload):
    """Package all skills in output/ directory"""

    output_dir = Path('output')
    if not output_dir.exists():
        console.print("❌ No output directory found", style="red")
        sys.exit(1)

    # Find all skill directories (with SKILL.md, not ending in _data)
    skill_dirs = []
    for item in output_dir.iterdir():
        if item.is_dir() and not item.name.endswith('_data'):
            if (item / "SKILL.md").exists():
                skill_dirs.append(item)

    if not skill_dirs:
        console.print("❌ No skills found to package", style="red")
        sys.exit(1)

    console.print(f"\n📦 Packaging [cyan]all {len(skill_dirs)}[/cyan] skills...\n")

    success = 0
    failed = 0

    for skill_dir in skill_dirs:
        console.print(f"  {skill_dir.name}...", end=" ")

        cmd = ['python3', 'cli/package_skill.py', str(skill_dir), '--no-open']
        if upload:
            cmd.append('--upload')

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            console.print("[green]✓[/green]")
            success += 1
        except subprocess.CalledProcessError:
            console.print("[red]✗[/red]")
            failed += 1

    console.print(f"\n✅ Packaged [green]{success}[/green] skills")
    if failed > 0:
        console.print(f"⚠️  Failed: [yellow]{failed}[/yellow]")
