# Changelog

All notable changes to Skill Seeker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Homebrew formula for macOS/Linux distribution
- npm package wrapper for Node.js ecosystem
- Standalone binary releases (PyInstaller/Nuitka)
- Shell completion scripts (bash, zsh, fish)
- Global configuration file (~/.skillseeker/config.yaml)

## [2.0.0] - 2025-01-19

### Added - CLI 2.0

**Major CLI Overhaul:**
- 🚀 New unified CLI interface (`skillseeker` or `ss` command)
- 📋 12 command groups with 30+ commands
- ⚡ High-level workflow commands (quick, full, rebuild)
- 🎨 Rich terminal output with colors, tables, and progress indicators
- 📊 Status dashboard showing project overview
- 🧙 Interactive setup wizard (`ss init`)
- 🔍 Auto-discovery of configs and skills
- 🧹 Clean command for cache management
- 🧪 Integrated test runner

**Command Groups:**
- `config` - Configuration management (list, create, validate, split)
- `scrape` - Scraping operations (run, estimate, dry-run)
- `build` - Build from cached data
- `enhance` - AI enhancement (local, api)
- `package` - Packaging (single, multi, all)
- `upload` - Upload to Claude (skill, batch)
- `router` - Router/hub skill generation
- `workflow` - Complete workflows (quick, full, rebuild)
- `status` - Project status dashboard
- `clean` - Cleanup operations
- `init` - Interactive wizard
- `test` - Run tests

**Documentation:**
- README_CLI.md - Complete command reference (2,500+ lines)
- INSTALL_CLI.md - Installation guide
- CLI_SUMMARY.md - Technical architecture
- CLI_IMPLEMENTATION.md - Implementation details
- CLI_VISUAL_GUIDE.md - Visual command tree

**Infrastructure:**
- Modern `pyproject.toml` configuration
- Package structure for distribution
- Entry points for global commands
- Utility modules (validation, formatting)
- Comprehensive test coverage

### Added - Distribution

**PyPI Publishing:**
- PyPI package ready for distribution
- Modern `pyproject.toml` setup
- GitHub Actions workflow for automated publishing
- Trusted Publisher configuration (secure, no tokens)
- MANIFEST.in for complete package bundling

**Installation Methods:**
- pipx (recommended): `pipx install skillseeker`
- pip: `pip install skillseeker`
- Source: `pip install -e .`

**Documentation:**
- PUBLISHING.md - Complete publishing guide for maintainers
- INSTALL_DISTRIBUTION.md - Multi-method installation guide
- Automated build and publish workflow
- TestPyPI support for testing releases

### Changed

**Improved User Experience:**
- Single entry point replaces 11+ separate scripts
- Consistent command structure across all operations
- Beautiful, color-coded output
- Helpful error messages with solutions
- Smart suggestions based on project state

**Backwards Compatibility:**
- All original CLI scripts still work
- No breaking changes to existing workflows
- Gradual migration path for users

### Technical

**Dependencies:**
- click>=8.0.0 - CLI framework
- rich>=10.0.0 - Terminal UI
- pyyaml>=5.4.0 - Configuration
- requests>=2.25.0 - HTTP client
- beautifulsoup4>=4.9.0 - HTML parsing

**Package Details:**
- Python 3.7+ required
- Cross-platform (Windows, macOS, Linux)
- Isolated installation via pipx
- Global `ss` and `skillseeker` commands

## [1.0.0] - 2024-12-XX

### Added - Original Features

**Core Functionality:**
- Documentation scraping with BFS traversal
- Smart categorization by topic
- Code language detection
- Pattern extraction from docs
- Enhanced SKILL.md generation
- AI-powered enhancement (local + API)
- ZIP packaging for Claude upload
- Automatic upload via API

**MCP Integration:**
- 9 MCP tools for Claude Code
- Natural language interface
- Auto-upload feature with API key detection
- Large documentation support (split configs)
- Router/hub skill generation
- Checkpoint/resume for long scrapes

**Preset Configurations:**
- Godot Engine
- React
- Vue.js
- Django
- FastAPI
- Kubernetes
- Tailwind CSS
- And more

**Documentation:**
- README.md - Main project documentation
- QUICKSTART.md - Get started in 3 steps
- docs/LARGE_DOCUMENTATION.md - Handle 10K-40K+ pages
- docs/ENHANCEMENT.md - AI enhancement guide
- docs/UPLOAD_GUIDE.md - Upload instructions
- docs/MCP_SETUP.md - MCP integration setup

**CLI Tools:**
- doc_scraper.py - Main scraping engine
- estimate_pages.py - Page count estimation
- enhance_skill.py - API-based enhancement
- enhance_skill_local.py - Local enhancement (Claude Code)
- package_skill.py - ZIP packaging with auto-upload
- upload_skill.py - Direct upload to Claude
- split_config.py - Config splitting for large docs
- generate_router.py - Router/hub skill generation
- run_tests.py - Test runner (96 tests passing)

## Version History

- **2.0.0** - CLI 2.0 + PyPI Distribution
- **1.0.0** - Original release with MCP integration

---

## Migration Guide

### From 1.x to 2.0

**Good news:** No breaking changes! Both old and new methods work.

**Old Way (still works):**
```bash
python3 cli/doc_scraper.py --config configs/react.json
python3 cli/enhance_skill_local.py output/react/
python3 cli/package_skill.py output/react/
```

**New Way (recommended):**
```bash
ss workflow full react.json
```

**Or step by step:**
```bash
ss scrape run react
ss enhance local react
ss package single react --upload
```

### Installing 2.0

**Recommended:**
```bash
pipx install skillseeker
ss init
```

**From source (development):**
```bash
git pull
pip install -e .
ss --version
```

---

## Semantic Versioning

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New features, backwards compatible
- **PATCH** version (0.0.X): Bug fixes, backwards compatible

---

[Unreleased]: https://github.com/yourusername/Skill_Seekers/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/yourusername/Skill_Seekers/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yourusername/Skill_Seekers/releases/tag/v1.0.0
