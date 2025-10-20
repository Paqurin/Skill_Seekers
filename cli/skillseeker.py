#!/usr/bin/env python3
"""
Skill Seeker - Unified CLI
Comprehensive command-line interface for converting documentation to Claude AI skills

Usage:
    skillseeker <command> [options]
    ss <command> [options]  # Short alias
"""

import sys
from pathlib import Path

try:
    import click
    from rich.console import Console
    from rich.table import Table
except ImportError:
    print("❌ Error: Required packages not installed")
    print("Install with: pip install click rich")
    sys.exit(1)

# Initialize console for rich output
console = Console()

# Version
__version__ = "2.0.0"


@click.group()
@click.version_option(__version__, prog_name="skillseeker")
@click.pass_context
def cli(ctx):
    """
    🚀 Skill Seeker - Convert documentation websites to Claude AI skills

    A comprehensive tool to automatically scrape, organize, enhance, and package
    any documentation website into a production-ready Claude skill.

    \b
    Quick Start:
        ss init                          # Interactive setup
        ss scrape run configs/react.json # Scrape documentation
        ss enhance local react           # Enhance with AI
        ss package single react          # Package skill
        ss workflow full react.json      # Complete workflow

    \b
    For detailed help on any command:
        ss <command> --help
    """
    ctx.ensure_object(dict)
    ctx.obj['CONSOLE'] = console


# ============================================================================
# CONFIG COMMANDS
# ============================================================================

@cli.group(name='config')
def config_group():
    """📋 Configuration management commands"""
    pass


@config_group.command(name='list')
@click.option('--format', type=click.Choice(['table', 'json', 'simple']), default='table',
              help='Output format')
@click.pass_context
def config_list(ctx, format):
    """List all available preset configurations"""
    from cli.commands.config_cmd import list_configs
    list_configs(console, format)


@config_group.command(name='create')
@click.option('--name', prompt='Skill name', help='Skill identifier')
@click.option('--url', prompt='Documentation URL', help='Base URL of documentation')
@click.option('--description', prompt='Description', help='When to use this skill')
@click.option('--max-pages', default=100, help='Maximum pages to scrape')
@click.option('--output', help='Output config file path')
@click.pass_context
def config_create(ctx, name, url, description, max_pages, output):
    """Create a new configuration file interactively"""
    from cli.commands.config_cmd import create_config
    create_config(console, name, url, description, max_pages, output)


@config_group.command(name='validate')
@click.argument('config_path', type=click.Path(exists=True))
@click.pass_context
def config_validate(ctx, config_path):
    """Validate a configuration file"""
    from cli.commands.config_cmd import validate_config
    validate_config(console, config_path)


@config_group.command(name='split')
@click.argument('config_path', type=click.Path(exists=True))
@click.option('--strategy', type=click.Choice(['auto', 'none', 'category', 'router', 'size']),
              default='auto', help='Splitting strategy')
@click.option('--target-pages', default=5000, help='Target pages per skill')
@click.option('--dry-run', is_flag=True, help='Preview without saving')
@click.pass_context
def config_split(ctx, config_path, strategy, target_pages, dry_run):
    """Split large documentation config into multiple focused skills"""
    from cli.commands.config_cmd import split_config
    split_config(console, config_path, strategy, target_pages, dry_run)


# ============================================================================
# SCRAPE COMMANDS
# ============================================================================

@cli.group(name='scrape')
def scrape_group():
    """🔍 Documentation scraping commands"""
    pass


@scrape_group.command(name='run')
@click.argument('config', type=str)
@click.option('--skip-scrape', is_flag=True, help='Use cached data')
@click.option('--resume', is_flag=True, help='Resume from checkpoint')
@click.option('--fresh', is_flag=True, help='Clear checkpoint and start fresh')
@click.option('--max-pages', type=int, help='Override max_pages from config')
@click.pass_context
def scrape_run(ctx, config, skip_scrape, resume, fresh, max_pages):
    """Scrape documentation and build skill"""
    from cli.commands.scrape_cmd import run_scrape
    run_scrape(console, config, skip_scrape, resume, fresh, max_pages)


@scrape_group.command(name='estimate')
@click.argument('config', type=str)
@click.option('--max-discovery', default=1000, help='Max pages to discover')
@click.pass_context
def scrape_estimate(ctx, config, max_discovery):
    """Estimate page count before scraping"""
    from cli.commands.scrape_cmd import estimate_pages
    estimate_pages(console, config, max_discovery)


@scrape_group.command(name='dry-run')
@click.argument('config', type=str)
@click.pass_context
def scrape_dry_run(ctx, config):
    """Preview what will be scraped without downloading"""
    from cli.commands.scrape_cmd import dry_run
    dry_run(console, config)


# ============================================================================
# BUILD COMMAND
# ============================================================================

@cli.command(name='build')
@click.argument('skill_name', type=str)
@click.pass_context
def build(ctx, skill_name):
    """🏗️  Build skill from cached scraped data"""
    from cli.commands.build_cmd import build_skill
    build_skill(console, skill_name)


# ============================================================================
# ENHANCE COMMANDS
# ============================================================================

@cli.group(name='enhance')
def enhance_group():
    """✨ AI enhancement commands"""
    pass


@enhance_group.command(name='local')
@click.argument('skill_name', type=str)
@click.option('--auto-approve', is_flag=True, help='Skip confirmation')
@click.pass_context
def enhance_local(ctx, skill_name, auto_approve):
    """Enhance SKILL.md using Claude Code (no API key needed)"""
    from cli.commands.enhance_cmd import enhance_local
    enhance_local(console, skill_name, auto_approve)


@enhance_group.command(name='api')
@click.argument('skill_name', type=str)
@click.option('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY)')
@click.pass_context
def enhance_api(ctx, skill_name, api_key):
    """Enhance SKILL.md using Claude API (requires API key)"""
    from cli.commands.enhance_cmd import enhance_api
    enhance_api(console, skill_name, api_key)


# ============================================================================
# PACKAGE COMMANDS
# ============================================================================

@cli.group(name='package')
def package_group():
    """📦 Skill packaging commands"""
    pass


@package_group.command(name='single')
@click.argument('skill_name', type=str)
@click.option('--upload', is_flag=True, help='Auto-upload if API key available')
@click.option('--no-open', is_flag=True, help='Do not open folder after packaging')
@click.pass_context
def package_single(ctx, skill_name, upload, no_open):
    """Package a single skill into .zip file"""
    from cli.commands.package_cmd import package_single
    package_single(console, skill_name, upload, not no_open)


@package_group.command(name='multi')
@click.argument('pattern', type=str)
@click.option('--upload', is_flag=True, help='Auto-upload all if API key available')
@click.pass_context
def package_multi(ctx, pattern, upload):
    """Package multiple skills matching pattern"""
    from cli.commands.package_cmd import package_multi
    package_multi(console, pattern, upload)


@package_group.command(name='all')
@click.option('--upload', is_flag=True, help='Auto-upload all if API key available')
@click.pass_context
def package_all(ctx, upload):
    """Package all skills in output/ directory"""
    from cli.commands.package_cmd import package_all
    package_all(console, upload)


# ============================================================================
# UPLOAD COMMANDS
# ============================================================================

@cli.group(name='upload')
def upload_group():
    """📤 Claude upload commands"""
    pass


@upload_group.command(name='skill')
@click.argument('zip_file', type=click.Path(exists=True))
@click.pass_context
def upload_skill(ctx, zip_file):
    """Upload a skill .zip file to Claude"""
    from cli.commands.upload_cmd import upload_skill
    upload_skill(console, zip_file)


@upload_group.command(name='batch')
@click.argument('pattern', type=str)
@click.pass_context
def upload_batch(ctx, pattern):
    """Upload multiple .zip files matching pattern"""
    from cli.commands.upload_cmd import upload_batch
    upload_batch(console, pattern)


# ============================================================================
# ROUTER COMMAND
# ============================================================================

@cli.group(name='router')
def router_group():
    """🔀 Router skill commands"""
    pass


@router_group.command(name='generate')
@click.argument('configs', nargs=-1, type=str, required=True)
@click.option('--name', help='Router skill name (default: auto-inferred)')
@click.option('--output-dir', help='Output directory for router config')
@click.pass_context
def router_generate(ctx, configs, name, output_dir):
    """Generate router/hub skill from multiple configs"""
    from cli.commands.router_cmd import generate_router
    generate_router(console, list(configs), name, output_dir)


# ============================================================================
# WORKFLOW COMMANDS (High-level)
# ============================================================================

@cli.group(name='workflow')
def workflow_group():
    """⚡ Complete workflow commands"""
    pass


@workflow_group.command(name='quick')
@click.argument('config', type=str)
@click.option('--upload', is_flag=True, help='Upload after packaging')
@click.pass_context
def workflow_quick(ctx, config, upload):
    """Quick workflow: scrape → build → package"""
    from cli.commands.workflow_cmd import quick_workflow
    quick_workflow(console, config, upload)


@workflow_group.command(name='full')
@click.argument('config', type=str)
@click.option('--enhance', type=click.Choice(['local', 'api', 'none']), default='local',
              help='Enhancement type')
@click.option('--upload', is_flag=True, help='Upload after packaging')
@click.pass_context
def workflow_full(ctx, config, enhance, upload):
    """Full workflow: scrape → build → enhance → package → upload"""
    from cli.commands.workflow_cmd import full_workflow
    full_workflow(console, config, enhance, upload)


@workflow_group.command(name='rebuild')
@click.argument('skill_name', type=str)
@click.option('--enhance', type=click.Choice(['local', 'api', 'none']), default='local',
              help='Enhancement type')
@click.option('--upload', is_flag=True, help='Upload after packaging')
@click.pass_context
def workflow_rebuild(ctx, skill_name, enhance, upload):
    """Fast rebuild from cache: build → enhance → package"""
    from cli.commands.workflow_cmd import rebuild_workflow
    rebuild_workflow(console, skill_name, enhance, upload)


# ============================================================================
# STATUS COMMAND
# ============================================================================

@cli.command(name='status')
@click.option('--detailed', is_flag=True, help='Show detailed information')
@click.pass_context
def status(ctx, detailed):
    """📊 Show project status and suggestions"""
    from cli.commands.status_cmd import show_status
    show_status(console, detailed)


# ============================================================================
# CLEAN COMMAND
# ============================================================================

@cli.command(name='clean')
@click.argument('target', type=click.Choice(['all', 'cache', 'checkpoints', 'backups']), default='all')
@click.option('--skill', help='Clean specific skill only')
@click.option('--force', is_flag=True, help='Skip confirmation')
@click.pass_context
def clean(ctx, target, skill, force):
    """🧹 Clean cached data, checkpoints, or backups"""
    from cli.commands.clean_cmd import clean_data
    clean_data(console, target, skill, force)


# ============================================================================
# INIT COMMAND (Interactive Setup)
# ============================================================================

@cli.command(name='init')
@click.option('--preset', help='Use a preset config (e.g., react, vue, godot)')
@click.pass_context
def init(ctx, preset):
    """🚀 Interactive setup wizard (recommended for first-time users)"""
    from cli.commands.init_cmd import init_wizard
    init_wizard(console, preset)


# ============================================================================
# TEST COMMAND
# ============================================================================

@cli.command(name='test')
@click.option('--verbose', is_flag=True, help='Verbose output')
@click.option('--pattern', help='Test file pattern')
@click.pass_context
def test(ctx, verbose, pattern):
    """🧪 Run tests"""
    from cli.commands.test_cmd import run_tests
    run_tests(console, verbose, pattern)


# ============================================================================
# GUI COMMAND
# ============================================================================

@cli.command(name='gui')
@click.pass_context
def gui(ctx):
    """🖥️  Launch interactive TUI (Terminal User Interface) with mouse support"""
    try:
        from cli.tui import run_tui
        run_tui()
    except ImportError:
        console.print("❌ Error: textual package not installed", style="red")
        console.print("Install with: pip install textual", style="yellow")
        sys.exit(1)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n\n⚠️  Interrupted by user", style="yellow")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="red")
        import traceback
        if '--debug' in sys.argv:
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
