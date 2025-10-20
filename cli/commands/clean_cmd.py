"""
Clean Command
Clean cached data, checkpoints, backups
"""

import sys
import shutil
from pathlib import Path


def clean_data(console, target, skill, force):
    """Clean cached data, checkpoints, or backups"""

    if target == 'all':
        targets = ['cache', 'checkpoints', 'backups']
    else:
        targets = [target]

    # Collect items to delete
    items_to_delete = []

    for target_type in targets:
        if target_type == 'cache':
            # Delete *_data directories
            output_dir = Path('output')
            if output_dir.exists():
                for data_dir in output_dir.glob('*_data'):
                    if not skill or data_dir.stem == f'{skill}_data':
                        items_to_delete.append((data_dir, 'cached data'))

        elif target_type == 'checkpoints':
            # Delete checkpoint.json files
            output_dir = Path('output')
            if output_dir.exists():
                for checkpoint in output_dir.glob('*/checkpoint.json'):
                    if not skill or checkpoint.parent.stem == f'{skill}_data':
                        items_to_delete.append((checkpoint, 'checkpoint'))

        elif target_type == 'backups':
            # Delete .backup files
            output_dir = Path('output')
            if output_dir.exists():
                for backup in output_dir.glob('*/*.backup'):
                    if not skill or skill in str(backup):
                        items_to_delete.append((backup, 'backup'))

    if not items_to_delete:
        console.print("✨ Nothing to clean", style="green")
        return

    # Show what will be deleted
    console.print(f"\n🧹 Found [yellow]{len(items_to_delete)}[/yellow] items to clean:")
    for item, item_type in items_to_delete:
        console.print(f"  • {item} ({item_type})")

    # Confirm
    if not force:
        confirm = input("\nProceed with deletion? [y/N]: ").strip().lower()
        if confirm != 'y':
            console.print("✋ Cancelled")
            return

    # Delete
    deleted = 0
    failed = 0

    for item, item_type in items_to_delete:
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            deleted += 1
        except Exception as e:
            console.print(f"  ⚠️  Failed to delete {item}: {e}", style="yellow")
            failed += 1

    console.print(f"\n✅ Deleted [green]{deleted}[/green] items")
    if failed > 0:
        console.print(f"⚠️  Failed: [yellow]{failed}[/yellow]")
