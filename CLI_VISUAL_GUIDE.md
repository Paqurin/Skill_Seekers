# Skill Seeker CLI 2.0 - Visual Guide

## Command Tree

```
ss (skillseeker)
│
├─ init                          🚀 Interactive setup wizard
│
├─ config                        📋 Configuration management
│  ├─ list                           List all presets
│  ├─ create                         Create new config
│  ├─ validate                       Validate config file
│  └─ split                          Split large configs
│
├─ scrape                        🔍 Documentation scraping
│  ├─ run                            Main scraping
│  ├─ estimate                       Estimate page count
│  └─ dry-run                        Preview scraping
│
├─ build                         🏗️  Build from cached data
│
├─ enhance                       ✨ AI enhancement
│  ├─ local                          Claude Code (no API key)
│  └─ api                            API-based (requires key)
│
├─ package                       📦 Skill packaging
│  ├─ single                         Package one skill
│  ├─ multi                          Package matching pattern
│  └─ all                            Package all skills
│
├─ upload                        📤 Claude upload
│  ├─ skill                          Upload single .zip
│  └─ batch                          Upload multiple .zips
│
├─ router                        🔀 Router generation
│  └─ generate                       Create router/hub skill
│
├─ workflow                      ⚡ Complete workflows
│  ├─ quick                          Scrape → Package
│  ├─ full                           Scrape → Enhance → Package → Upload
│  └─ rebuild                        Build → Enhance → Package (from cache)
│
├─ status                        📊 Project dashboard
│
├─ clean                         🧹 Clean operations
│
├─ test                          🧪 Run tests
│
└─ --version                     📌 Show version
```

## Workflow Visualization

### Quick Workflow (`ss workflow quick`)

```
┌─────────────┐
│  Start      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Scrape             │  (~25 min)
│  Documentation      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Package            │  (~10 sec)
│  skill.zip          │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Done! ✅   │
└─────────────┘
```

### Full Workflow (`ss workflow full`)

```
┌─────────────┐
│  Start      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Scrape             │  (~25 min)
│  Documentation      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Build Skill        │  (~1 min)
│  SKILL.md + refs    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Enhance            │  (~60 sec)
│  AI-powered         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Package            │  (~10 sec)
│  skill.zip          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Upload to Claude   │  (~10 sec, optional)
│  (if --upload)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Done! ✅   │
└─────────────┘
```

### Rebuild Workflow (`ss workflow rebuild`)

```
┌─────────────┐
│  Start      │
│  (has cache)│
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Build from Cache   │  (~1 min)
│  (no scraping!)     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Enhance            │  (~60 sec)
│  AI-powered         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Package            │  (~10 sec)
│  skill.zip          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Upload (optional)  │  (~10 sec)
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Done! ✅   │
└─────────────┘

Total: 2-4 minutes! ⚡
```

## Status Dashboard Example

```
╔══════════════════════════════════════════════════════════╗
║        📊 Skill Seeker Project Status                   ║
╚══════════════════════════════════════════════════════════╝

📋 Configurations: 12 presets
   └─ react, vue, godot, django, fastapi, +7 more

💾 Cached Data: 3 skills
   ├─ react (245 pages, 15.2 MB)
   ├─ vue (180 pages, 12.1 MB)
   └─ godot (450 pages, 28.5 MB)

🏗️  Built Skills: 2 skills
   ├─ react (SKILL.md + 8 references) (enhanced)
   └─ vue (SKILL.md + 6 references)

📦 Packaged: 1 skill
   └─ react.zip (2.1 MB)

🔑 API Key: ✓ Configured

💡 Suggestions:
   • Build 'godot' from cached data: ss build godot
   • Package 'vue' skill: ss package single vue
```

## File Organization

```
Skill_Seekers/
│
├─ cli/
│  ├─ skillseeker.py              Main entry point
│  │
│  ├─ commands/                   Command modules
│  │  ├─ config_cmd.py               📋 Config operations
│  │  ├─ scrape_cmd.py               🔍 Scraping
│  │  ├─ build_cmd.py                🏗️  Building
│  │  ├─ enhance_cmd.py              ✨ Enhancement
│  │  ├─ package_cmd.py              📦 Packaging
│  │  ├─ upload_cmd.py               📤 Uploading
│  │  ├─ router_cmd.py               🔀 Router gen
│  │  ├─ workflow_cmd.py             ⚡ Workflows
│  │  ├─ status_cmd.py               📊 Status
│  │  ├─ clean_cmd.py                🧹 Cleaning
│  │  ├─ init_cmd.py                 🚀 Wizard
│  │  └─ test_cmd.py                 🧪 Testing
│  │
│  ├─ utils_new/                  Utilities
│  │  ├─ validation.py               Input validation
│  │  └─ formatting.py               Output formatting
│  │
│  └─ [existing tools]            Legacy scripts (still work!)
│
├─ configs/                       Preset configurations
│  ├─ react.json
│  ├─ vue.json
│  ├─ godot.json
│  └─ ...
│
├─ output/                        Generated output
│  ├─ react_data/                    Cached scrape data
│  ├─ react/                         Built skill
│  └─ react.zip                      Packaged skill
│
├─ setup.py                       Package installer
├─ requirements-cli.txt           CLI dependencies
│
└─ docs/
   ├─ README_CLI.md               Complete command reference
   ├─ INSTALL_CLI.md              Installation guide
   ├─ CLI_SUMMARY.md              Technical summary
   └─ CLI_IMPLEMENTATION.md       Implementation details
```

## Usage Patterns

### Pattern 1: First-Time User

```
┌─────────────┐
│   ss init   │  Interactive wizard
└─────────────┘
       │
       ▼
Everything automated!
       │
       ▼
┌─────────────┐
│ skill.zip ✅│
└─────────────┘
```

### Pattern 2: Experienced User

```
ss config list           ← See options
ss scrape estimate       ← Check size
ss workflow full         ← Execute
```

### Pattern 3: Power User

```
ss scrape run react
ss enhance local react
ss package single react --upload
ss status
```

### Pattern 4: Large Documentation

```
ss config split godot.json --strategy router
ss scrape run godot-*.json  (parallel)
ss router generate godot-*.json
ss package multi "godot-*" --upload
```

## Quick Reference Card

```
╔════════════════════════════════════════════════════╗
║  Skill Seeker CLI - Quick Reference               ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  🚀 Getting Started                                ║
║     ss init              Interactive wizard        ║
║     ss --help            Show all commands         ║
║     ss status            Project dashboard         ║
║                                                    ║
║  📋 Common Operations                              ║
║     ss config list       List presets              ║
║     ss scrape run X      Scrape config X           ║
║     ss enhance local X   Enhance skill X           ║
║     ss package single X  Package skill X           ║
║                                                    ║
║  ⚡ Workflows                                      ║
║     ss workflow quick X  Fast workflow             ║
║     ss workflow full X   Complete workflow         ║
║     ss workflow rebuild  Fast rebuild (2-4 min)    ║
║                                                    ║
║  💡 Tips                                           ║
║     • Always estimate before scraping              ║
║     • Use cache for fast rebuilds                  ║
║     • Check status to see suggestions              ║
║     • Add --upload to auto-upload                  ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

## Installation Flow

```
┌─────────────────────┐
│  Install deps       │
│  pip install -r ... │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Install package    │
│  pip install -e .   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Verify install     │
│  ss --version       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Run wizard         │
│  ss init            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Building skills! ✅│
└─────────────────────┘
```

## Command Cheat Sheet

| Task | Command |
|------|---------|
| **Setup** | |
| First time | `ss init` |
| Install | `pip install -e .` |
| **Info** | |
| Version | `ss --version` |
| Help | `ss --help` |
| Status | `ss status` |
| **Config** | |
| List configs | `ss config list` |
| Create config | `ss config create` |
| Validate | `ss config validate X` |
| **Scrape** | |
| Estimate | `ss scrape estimate X` |
| Scrape | `ss scrape run X` |
| Resume | `ss scrape run X --resume` |
| **Build** | |
| Build | `ss build X` |
| From cache | `ss build X` (automatic) |
| **Enhance** | |
| Local (free) | `ss enhance local X` |
| API (paid) | `ss enhance api X` |
| **Package** | |
| One skill | `ss package single X` |
| Many skills | `ss package multi "Y*"` |
| All skills | `ss package all` |
| **Upload** | |
| One .zip | `ss upload skill X.zip` |
| Many .zips | `ss upload batch "*.zip"` |
| **Workflows** | |
| Quick | `ss workflow quick X` |
| Full | `ss workflow full X` |
| Rebuild | `ss workflow rebuild X` |
| **Cleanup** | |
| Clean cache | `ss clean cache` |
| Clean all | `ss clean all` |

---

**Made with ❤️ for Skill Seekers**
