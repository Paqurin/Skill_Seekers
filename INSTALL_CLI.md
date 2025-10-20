# Skill Seeker CLI Installation Guide

## Quick Install

### Option 1: Install as Package (Recommended)

```bash
# Navigate to project directory
cd Skill_Seekers

# Install with pip (creates `skillseeker` and `ss` commands)
pip install -e .

# Verify installation
ss --version
ss --help
```

**Benefits:**
- ✅ Global `ss` and `skillseeker` commands
- ✅ Works from any directory
- ✅ Auto-completion support
- ✅ Clean, professional UX

### Option 2: Use Directly (No Installation)

```bash
# Navigate to project directory
cd Skill_Seekers

# Run directly
python3 cli/skillseeker.py --help

# Create alias for convenience
alias ss="python3 $(pwd)/cli/skillseeker.py"
```

**Benefits:**
- ✅ No installation needed
- ✅ Works immediately
- ⚠️  Alias only works in current shell

---

## Requirements

### Python Version

- Python 3.7 or higher

### Dependencies

#### Core (Required)

```bash
pip install requests beautifulsoup4 click rich pyyaml
```

#### Optional (For Specific Features)

```bash
# For API-based enhancement
pip install anthropic

# For development
pip install pytest pytest-cov
```

#### Install All at Once

```bash
# Core dependencies
pip install -r requirements.txt

# All dependencies (including optional)
pip install -e ".[dev,api,mcp]"
```

---

## Verification

After installation, verify everything works:

```bash
# Check version
ss --version

# See all commands
ss --help

# Check status
ss status

# List configs
ss config list
```

**Expected output:**
```
╔══════════════════════════════════════════════════════════╗
║        📊 Skill Seeker Project Status                   ║
╚══════════════════════════════════════════════════════════╝

📋 Configurations: 12 presets
   └─ react, vue, godot, django, fastapi, +7 more
...
```

---

## Shell Completion (Optional)

### Bash

Add to `~/.bashrc`:

```bash
eval "$(_SS_COMPLETE=bash_source ss)"
```

Then reload:

```bash
source ~/.bashrc
```

### Zsh

Add to `~/.zshrc`:

```bash
eval "$(_SS_COMPLETE=zsh_source ss)"
```

Then reload:

```bash
source ~/.zshrc
```

### Fish

Add to `~/.config/fish/config.fish`:

```fish
eval (env _SS_COMPLETE=fish_source ss)
```

Then reload:

```fish
source ~/.config/fish/config.fish
```

---

## First Run

After installation, run the interactive wizard:

```bash
ss init
```

This will:
1. Help you choose or create a config
2. Estimate page count
3. Scrape documentation
4. Build and enhance the skill
5. Package for upload

---

## Troubleshooting

### "Command not found: ss"

**Solution 1:** Reinstall

```bash
pip uninstall skillseeker
pip install -e .
```

**Solution 2:** Use full path

```bash
python3 cli/skillseeker.py --help
```

**Solution 3:** Create alias

```bash
alias ss="python3 /path/to/Skill_Seekers/cli/skillseeker.py"
```

### "ImportError: No module named 'click'"

**Solution:** Install dependencies

```bash
pip install click rich pyyaml requests beautifulsoup4
```

### "Permission denied"

**Solution:** Make executable

```bash
chmod +x cli/skillseeker.py
```

### "Cannot find config"

**Solution:** Check working directory

```bash
# The CLI expects to run from project root
cd /path/to/Skill_Seekers
ss config list
```

---

## Uninstall

```bash
# Uninstall package
pip uninstall skillseeker

# Remove config (optional)
rm -rf ~/.skillseeker
```

---

## Next Steps

After installation:

1. **Read the CLI Guide:** [README_CLI.md](README_CLI.md)
2. **Run the wizard:** `ss init`
3. **Check the status:** `ss status`
4. **Explore commands:** `ss --help`

---

## Quick Reference

```bash
# Installation
pip install -e .

# Verification
ss --version
ss status

# First time use
ss init

# Common commands
ss config list
ss scrape run react
ss enhance local react
ss package single react
ss workflow full react.json
```

---

**Ready to build skills?** 🚀

Start with: `ss init`
