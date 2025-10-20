"""
Input Validation Utilities
"""

import re
from pathlib import Path


def validate_config_name(name):
    """Validate config/skill name format"""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))


def validate_url(url):
    """Validate URL format"""
    return url.startswith(('http://', 'https://'))


def validate_skill_directory(skill_path):
    """Validate that a directory is a valid skill directory"""
    skill_path = Path(skill_path)

    if not skill_path.exists():
        return False, f"Directory not found: {skill_path}"

    if not skill_path.is_dir():
        return False, f"Not a directory: {skill_path}"

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"SKILL.md not found in {skill_path}"

    return True, None


def find_config(config_name):
    """
    Find config file by name
    Searches: configs/<name>.json, configs/<name>, <name>
    """
    # If it's already a path and exists, use it
    if Path(config_name).exists():
        return Path(config_name)

    # Try configs directory
    config_path = Path(f'configs/{config_name}')
    if config_path.exists():
        return config_path

    # Try with .json extension
    config_path = Path(f'configs/{config_name}.json')
    if config_path.exists():
        return config_path

    # Try without configs directory
    config_path = Path(f'{config_name}.json')
    if config_path.exists():
        return config_path

    return None


def find_skill_directory(skill_name):
    """
    Find skill directory by name
    Searches: output/<name>/, output/<name>_data/, <name>/
    """
    # Try output directory
    skill_path = Path(f'output/{skill_name}')
    if skill_path.exists() and skill_path.is_dir():
        if (skill_path / "SKILL.md").exists():
            return skill_path

    # Try without output prefix
    skill_path = Path(skill_name)
    if skill_path.exists() and skill_path.is_dir():
        if (skill_path / "SKILL.md").exists():
            return skill_path

    return None
