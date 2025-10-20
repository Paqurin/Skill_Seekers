"""
Enhance Commands
AI-powered SKILL.md enhancement
"""

import sys
import subprocess
from pathlib import Path
from ..utils_new.validation import find_skill_directory


def enhance_local(console, skill_name, auto_approve):
    """Enhance SKILL.md using Claude Code (local, no API key)"""

    # Find skill directory
    skill_dir = find_skill_directory(skill_name)

    if not skill_dir:
        console.print(f"❌ Skill not found: [red]{skill_name}[/red]", style="red")
        console.print(f"\n💡 Build the skill first: [cyan]ss build {skill_name}[/cyan]")
        sys.exit(1)

    # Confirm
    if not auto_approve:
        console.print(f"\n✨ Enhance SKILL.md for: [cyan]{skill_name}[/cyan]")
        console.print("This will:")
        console.print("  • Backup current SKILL.md")
        console.print("  • Open new terminal with Claude Code")
        console.print("  • Generate enhanced SKILL.md (30-60 seconds)")

        proceed = input("\nProceed? [Y/n]: ").strip().lower()
        if proceed == 'n':
            console.print("✋ Enhancement cancelled")
            return

    # Run enhancer
    console.print(f"\n🚀 Launching local enhancement...\n")

    cmd = ['python3', 'cli/enhance_skill_local.py', str(skill_dir)]

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Enhancement complete![/green]")
        console.print(f"\n💡 Next: [cyan]ss package single {skill_name}[/cyan]")
    except subprocess.CalledProcessError:
        console.print(f"\n⚠️  Enhancement may have failed", style="yellow")
        console.print(f"   Check: {skill_dir / 'SKILL.md'}")
    except KeyboardInterrupt:
        console.print("\n⚠️  Interrupted", style="yellow")


def enhance_api(console, skill_name, api_key):
    """Enhance SKILL.md using Claude API"""

    # Find skill directory
    skill_dir = find_skill_directory(skill_name)

    if not skill_dir:
        console.print(f"❌ Skill not found: [red]{skill_name}[/red]", style="red")
        sys.exit(1)

    # Check API key
    import os
    if not api_key:
        api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()

    if not api_key:
        console.print("❌ API key required", style="red")
        console.print("\nOptions:")
        console.print("  1. Set: [cyan]export ANTHROPIC_API_KEY=sk-ant-...[/cyan]")
        console.print("  2. Pass: [cyan]ss enhance api {skill_name} --api-key sk-ant-...[/cyan]")
        console.print("  3. Use local: [cyan]ss enhance local {skill_name}[/cyan] (no API key needed)")
        sys.exit(1)

    # Run API enhancer
    console.print(f"\n✨ Enhancing with Claude API: [cyan]{skill_name}[/cyan]\n")

    cmd = ['python3', 'cli/enhance_skill.py', str(skill_dir)]
    if api_key:
        cmd.extend(['--api-key', api_key])

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Enhancement complete![/green]")
        console.print(f"\n💡 Next: [cyan]ss package single {skill_name}[/cyan]")
    except subprocess.CalledProcessError:
        console.print(f"\n❌ Enhancement failed", style="red")
        sys.exit(1)
