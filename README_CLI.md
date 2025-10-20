# Skill Seeker CLI 2.0

**Modern, unified command-line interface for building Claude AI skills**

## What's New in 2.0?

✨ **Single Entry Point:** `skillseeker` or `ss` command for everything
✨ **Smart Workflows:** High-level commands for common tasks
✨ **Rich Output:** Beautiful progress bars, tables, and colored output
✨ **Auto-Discovery:** Finds configs and skills automatically
✨ **Status Dashboard:** See everything at a glance
✨ **Interactive Wizard:** `ss init` for first-time users

---

## Quick Start

### Installation

```bash
# Install package (creates `skillseeker` and `ss` commands)
pip install -e .

# Or use directly without installation
python3 cli/skillseeker.py --help
```

### First Time User

```bash
# Interactive setup wizard
ss init

# That's it! The wizard will:
# 1. Help you choose or create a config
# 2. Estimate page count
# 3. Scrape documentation
# 4. Build and enhance the skill
# 5. Package for upload
```

### Quick Commands

```bash
# See what you have
ss status

# List presets
ss config list

# Scrape a preset
ss scrape run react

# Full workflow (one command!)
ss workflow full react.json

# Package and upload
ss package single react --upload
```

---

## Command Reference

### Global Options

```bash
ss --help              # Show all commands
ss --version           # Show version
ss <command> --help    # Command-specific help
```

### 1. Init (Interactive Wizard)

```bash
ss init                      # Full interactive setup
ss init --preset react       # Use preset, skip selection
```

**What it does:**
- Guides you through creating/selecting a config
- Runs page estimation
- Executes full scraping workflow
- Perfect for first-time users

---

### 2. Config Commands

#### List Configurations

```bash
ss config list               # Table view (default)
ss config list --format json # JSON output
ss config list --format simple # Simple list
```

#### Create Configuration

```bash
ss config create \
  --name myframework \
  --url https://docs.example.com/ \
  --description "My framework docs" \
  --max-pages 500
```

**Interactive mode:**
```bash
ss config create
# Will prompt for all values
```

#### Validate Configuration

```bash
ss config validate configs/react.json
ss config validate myconfig.json
```

Shows errors and warnings before scraping.

#### Split Configuration (Large Docs)

```bash
ss config split godot.json                    # Auto-detect strategy
ss config split godot.json --strategy router  # Create router + sub-skills
ss config split godot.json --strategy category # Split by categories
ss config split godot.json --dry-run          # Preview without saving
```

**Strategies:**
- `auto` - Automatically choose best approach
- `router` - Create hub + specialized sub-skills (recommended for 10K+ pages)
- `category` - Split by documentation categories
- `size` - Split by page count
- `none` - Don't split

---

### 3. Scrape Commands

#### Run Scraping

```bash
ss scrape run react.json                  # Scrape from config
ss scrape run react                       # Auto-find config
ss scrape run react --skip-scrape         # Use cached data
ss scrape run react --resume              # Resume from checkpoint
ss scrape run react --fresh               # Clear checkpoint, start fresh
ss scrape run react --max-pages 100       # Override max_pages
```

#### Estimate Pages

```bash
ss scrape estimate react.json             # Estimate page count (fast!)
ss scrape estimate react --max-discovery 500
```

**Why estimate first?**
- Validates config patterns work
- Shows estimated total pages
- Recommends optimal `max_pages` value
- Takes 1-2 minutes vs 20-40 for full scrape

#### Dry Run

```bash
ss scrape dry-run react.json              # Preview what will be scraped
```

---

### 4. Build Command

```bash
ss build react                            # Build from cached data
```

Fast rebuild without re-scraping. Uses cached data from `output/react_data/`.

---

### 5. Enhance Commands

#### Local Enhancement (Recommended - No API Key)

```bash
ss enhance local react                    # Opens Claude Code terminal
ss enhance local react --auto-approve     # Skip confirmation
```

Uses your Claude Code Max plan. Takes 30-60 seconds.

#### API Enhancement (Requires API Key)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
ss enhance api react
ss enhance api react --api-key sk-ant-... # Or pass directly
```

---

### 6. Package Commands

#### Package Single Skill

```bash
ss package single react                   # Package one skill
ss package single react --upload          # Auto-upload if API key set
ss package single react --no-open         # Don't open folder
```

#### Package Multiple Skills

```bash
ss package multi "godot-*"                # Package all godot-* skills
ss package multi "godot-*" --upload       # Upload all
```

#### Package All Skills

```bash
ss package all                            # Package everything in output/
ss package all --upload                   # Upload everything
```

---

### 7. Upload Commands

#### Upload Single Skill

```bash
export ANTHROPIC_API_KEY=sk-ant-...
ss upload skill output/react.zip
```

#### Batch Upload

```bash
ss upload batch "*.zip"                   # Upload all .zip files
```

---

### 8. Router Commands

#### Generate Router Skill

```bash
ss router generate configs/godot-*.json   # Create from multiple configs
ss router generate godot-2d.json godot-3d.json godot-scripting.json
ss router generate godot-*.json --name godot-hub
```

Creates an intelligent router that directs queries to specialized sub-skills.

---

### 9. Workflow Commands (High-Level)

#### Quick Workflow

```bash
ss workflow quick react.json              # Scrape → Build → Package
ss workflow quick react.json --upload     # + Upload
```

**Steps:**
1. Scrape documentation
2. Package skill
3. (Optional) Upload

**Time:** ~25 minutes

#### Full Workflow

```bash
ss workflow full react.json               # Complete workflow
ss workflow full react.json --enhance api # Use API enhancement
ss workflow full react.json --enhance none # Skip enhancement
ss workflow full react.json --upload      # + Upload
```

**Steps:**
1. Scrape documentation
2. Build skill
3. Enhance SKILL.md (local by default)
4. Package skill
5. (Optional) Upload

**Time:** ~26 minutes (with local enhancement)

#### Rebuild Workflow

```bash
ss workflow rebuild react                 # Fast rebuild from cache
ss workflow rebuild react --enhance api   # Use API enhancement
ss workflow rebuild react --upload        # + Upload
```

**Steps:**
1. Build from cached data
2. Enhance SKILL.md
3. Package skill
4. (Optional) Upload

**Time:** ~2-4 minutes (using cache!)

---

### 10. Status Command

```bash
ss status                                 # Show project overview
ss status --detailed                      # Show detailed information
```

**Shows:**
- Available configurations (12 presets)
- Cached data (3 skills with sizes)
- Built skills (2 skills with ref counts)
- Packaged skills (1 .zip file)
- API key status
- Smart suggestions for next steps

**Example Output:**
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

---

### 11. Clean Command

```bash
ss clean all                              # Clean everything
ss clean cache                            # Clean cached data only
ss clean checkpoints                      # Clean checkpoint files
ss clean backups                          # Clean .backup files
ss clean cache --skill react              # Clean specific skill
ss clean all --force                      # Skip confirmation
```

---

### 12. Test Command

```bash
ss test                                   # Run all tests
ss test --verbose                         # Verbose output
ss test --pattern test_scraper*           # Run specific tests
```

---

## Common Workflows

### Workflow 1: First Time (With Scraping)

```bash
# Option A: Interactive
ss init

# Option B: Command-line
ss workflow full react.json --enhance local
```

**Time:** ~25 minutes
**Result:** `output/react.zip` ready for upload

### Workflow 2: Fast Rebuild (Using Cache)

```bash
ss workflow rebuild react --enhance local
```

**Time:** ~2-4 minutes
**Result:** Updated skill with enhancements

### Workflow 3: Large Documentation (10K+ pages)

```bash
# 1. Split config
ss config split godot.json --strategy router

# 2. Scrape all in parallel (in separate terminals)
ss scrape run godot-2d.json &
ss scrape run godot-3d.json &
ss scrape run godot-scripting.json &
wait

# 3. Generate router
ss router generate configs/godot-*.json

# 4. Package all
ss package multi "godot-*" --upload
```

### Workflow 4: Create Custom Skill

```bash
# 1. Create config
ss config create

# 2. Validate
ss config validate myframework.json

# 3. Estimate
ss scrape estimate myframework.json

# 4. Run full workflow
ss workflow full myframework.json
```

---

## Tips & Tricks

### Short Aliases

```bash
# Create shell aliases for even shorter commands
alias ssi="ss init"
alias sss="ss status"
alias ssr="ss scrape run"
alias sse="ss enhance local"
alias ssp="ss package single"
```

### Auto-Complete

```bash
# Bash
eval "$(_SS_COMPLETE=bash_source ss)"

# Zsh
eval "$(_SS_COMPLETE=zsh_source ss)"

# Fish
eval (env _SS_COMPLETE=fish_source ss)
```

### Check Before Scraping

```bash
# Always estimate first for unknown documentation
ss scrape estimate newframework.json

# Adjust max_pages based on estimate
# Then scrape
ss scrape run newframework.json
```

### Use Cache Effectively

```bash
# Scrape once
ss scrape run react.json

# Then rebuild quickly anytime
ss build react
ss enhance local react
ss package single react
```

### Monitor Long Scrapes

```bash
# Use checkpoint feature for long scrapes
# Edit config: "checkpoint": {"enabled": true, "interval": 1000}

# If interrupted, resume
ss scrape run godot.json --resume
```

---

## Comparison: Old vs New CLI

### Old Way (Multiple Scripts)

```bash
# Multiple commands, hard to remember
python3 cli/doc_scraper.py --config configs/react.json
python3 cli/enhance_skill_local.py output/react/
python3 cli/package_skill.py output/react/ --upload
```

### New Way (Unified CLI)

```bash
# One command, clear and simple
ss workflow full react.json --upload

# Or step by step
ss scrape run react
ss enhance local react
ss package single react --upload
```

### New Way (Even Simpler)

```bash
# Interactive wizard does everything
ss init
```

---

## Backwards Compatibility

All original CLI scripts still work:

```bash
python3 cli/doc_scraper.py --config configs/react.json
python3 cli/estimate_pages.py configs/react.json
python3 cli/enhance_skill_local.py output/react/
python3 cli/package_skill.py output/react/
```

But the new unified CLI is recommended for better UX.

---

## Troubleshooting

### Command Not Found

```bash
# If `ss` or `skillseeker` not found after install:
pip install -e .

# Or use directly:
python3 cli/skillseeker.py status
```

### Config Not Found

```bash
# Check available configs
ss config list

# Validate your config
ss config validate myconfig.json
```

### No Cached Data

```bash
# Check status
ss status

# If data missing, scrape first
ss scrape run react
```

### Enhancement Failed

```bash
# Try API enhancement instead
export ANTHROPIC_API_KEY=sk-ant-...
ss enhance api react

# Or skip enhancement
ss package single react
```

---

## What's Next?

After mastering the CLI, explore:

- **MCP Integration:** Use from Claude Code with natural language
- **Large Documentation:** Split configs for 10K+ page docs
- **Router Skills:** Create intelligent hub skills
- **Batch Operations:** Package and upload multiple skills at once

See the main [README.md](README.md) for complete documentation.

---

## Feedback & Issues

Found a bug or have a suggestion?

1. Check existing issues: `gh issue list`
2. Create new issue: `gh issue create`
3. Or open an issue on GitHub

---

**Happy skill building with the new CLI!** 🚀
