"""
Upload Commands
Upload skills to Claude via API
"""

import sys
import subprocess
from pathlib import Path


def upload_skill(console, zip_file):
    """Upload a single skill .zip file"""

    zip_path = Path(zip_file)

    if not zip_path.exists():
        console.print(f"❌ File not found: [red]{zip_file}[/red]", style="red")
        sys.exit(1)

    if not zip_path.suffix == '.zip':
        console.print(f"❌ Not a .zip file: [red]{zip_file}[/red]", style="red")
        sys.exit(1)

    console.print(f"\n📤 Uploading: [cyan]{zip_path.name}[/cyan]\n")

    cmd = ['python3', 'cli/upload_skill.py', str(zip_path)]

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Upload complete![/green]")
    except subprocess.CalledProcessError:
        console.print(f"\n⚠️  Upload failed - try manual upload", style="yellow")
        console.print(f"\nManual upload:")
        console.print("  1. Go to https://claude.ai/skills")
        console.print("  2. Click \"Upload Skill\"")
        console.print(f"  3. Select: {zip_path}")


def upload_batch(console, pattern):
    """Upload multiple .zip files"""

    output_dir = Path('output')
    matches = list(output_dir.glob(pattern))

    # Filter to only .zip files
    zip_files = [f for f in matches if f.suffix == '.zip']

    if not zip_files:
        console.print(f"❌ No .zip files found matching: [red]{pattern}[/red]", style="red")
        sys.exit(1)

    console.print(f"\n📤 Uploading [cyan]{len(zip_files)}[/cyan] skills...\n")

    success = 0
    failed = 0

    for zip_file in zip_files:
        console.print(f"  {zip_file.name}...", end=" ")

        cmd = ['python3', 'cli/upload_skill.py', str(zip_file)]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            console.print("[green]✓[/green]")
            success += 1
        except subprocess.CalledProcessError:
            console.print("[red]✗[/red]")
            failed += 1

    console.print(f"\n✅ Uploaded [green]{success}[/green] skills")
    if failed > 0:
        console.print(f"⚠️  Failed: [yellow]{failed}[/yellow] (try manual upload)")
