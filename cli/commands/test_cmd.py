"""
Test Command
Run project tests
"""

import sys
import subprocess


def run_tests(console, verbose, pattern):
    """Run tests"""

    console.print("\n🧪 Running tests...\n")

    cmd = ['python3', 'cli/run_tests.py']

    if verbose:
        cmd.append('--verbose')
    if pattern:
        cmd.extend(['--pattern', pattern])

    try:
        result = subprocess.run(cmd, check=True)
        console.print(f"\n✅ [green]Tests passed![/green]")
    except subprocess.CalledProcessError:
        console.print(f"\n❌ Tests failed", style="red")
        sys.exit(1)
