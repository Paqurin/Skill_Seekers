# 🖥️ Skill Seeker TUI Guide

## Terminal User Interface with Mouse Support

Skill Seeker now includes a beautiful, interactive Terminal User Interface (TUI) built with the Textual framework. The TUI provides a modern, mouse-enabled interface for all Skill Seeker operations.

## 🚀 Quick Start

Launch the TUI with:

```bash
ss gui
# or
skillseeker gui
```

**Mouse support:** Click anywhere, select items, and press buttons with your mouse!

## 📱 Screens Overview

### 1. **Dashboard** (Main Screen)

The dashboard provides an at-a-glance view of your Skill Seeker project:

- **📊 Quick Stats:**
  - Number of configurations
  - Cached data sets
  - Built skills
  - Packaged .zip files

- **📈 Recent Activity:**
  - Recently built skills with timestamps
  - Quick status overview

- **⚡ Quick Actions:**
  - 🎯 New Config - Create a new configuration
  - 🔍 Start Scrape - Begin scraping documentation
  - ✨ Enhance Skill - Enhance with AI
  - 📤 Upload Skill - Upload to Claude

**Keyboard Shortcuts:**
- `c` - Go to Configs screen
- `s` - Go to Scrape screen
- `k` - Go to Skills screen
- `q` - Quit application
- `d` - Return to Dashboard

### 2. **Configuration Manager** (Press `c`)

Browse, create, and manage your configuration files:

- **Features:**
  - Interactive table of all configs
  - Live preview of selected config
  - Create new configs with form wizard
  - Validate configurations
  - Split large configs

- **Actions:**
  - Click any config row to see details
  - 📝 New - Create new configuration
  - ✓ Validate - Check config validity
  - ✂️ Split - Split large documentation configs

**Keyboard Shortcuts:**
- `n` - New config
- `v` - Validate selected config
- `Escape` - Go back to Dashboard

### 3. **Documentation Scraper** (Press `s`)

Start scraping with a visual interface:

- **Features:**
  - Dropdown to select configuration
  - Options checkboxes:
    - ☐ Skip Scrape (use cached data)
    - ☐ Resume from checkpoint
    - ☐ Fresh start
  - Max pages override
  - Live progress bar
  - Scrolling log output

- **Actions:**
  - 🚀 Start Scrape - Begin scraping process
  - 📊 Estimate Only - Quick page count estimation

**Keyboard Shortcuts:**
- `Escape` - Go back to Dashboard

### 4. **Skill Manager** (Press `k`)

Manage built skills - enhance, package, upload:

- **Features:**
  - Table of all built skills with:
    - Skill name
    - File size
    - Last modified date
    - Status icons (✨ enhanced, 📦 packaged)
  - Skill preview panel
  - Action buttons

- **Actions:**
  - ✨ Enhance (Local) - Use Claude Code Max
  - ✨ Enhance (API) - Use Anthropic API
  - 📦 Package - Create .zip file
  - 📤 Upload to Claude - Auto-upload
  - 🗑️ Delete - Remove skill

**Keyboard Shortcuts:**
- `Escape` - Go back to Dashboard

### 5. **Upload Manager**

Upload packaged skills to Claude:

- **Features:**
  - Dropdown to select .zip file
  - API key status indicator
  - Upload log output

- **Actions:**
  - 📤 Upload - Single file upload
  - 📋 Batch Upload - Upload multiple files

**Keyboard Shortcuts:**
- `Escape` - Go back to Dashboard

### 6. **New Config Wizard**

Interactive form to create new configurations:

- **Fields:**
  - Skill Name (required)
  - Documentation URL (required)
  - Description
  - Max Pages (default: 100)

- **Actions:**
  - ✓ Create - Save new config
  - ✗ Cancel - Discard and return

**Keyboard Shortcuts:**
- `Escape` - Cancel and go back

## 🎨 UI Features

### Mouse Support

The TUI is **fully mouse-enabled**:
- ✅ Click buttons to trigger actions
- ✅ Click table rows to select items
- ✅ Click input fields to type
- ✅ Scroll with mouse wheel
- ✅ Click dropdowns to select options

### Keyboard Navigation

Navigate efficiently with keyboard:
- `Tab` - Move to next element
- `Shift+Tab` - Move to previous element
- `Enter` - Activate button/selection
- `Arrow Keys` - Navigate tables and menus
- `Escape` - Go back one screen
- `q` - Quit application
- `d` - Return to dashboard

### Color Coding

- **🟦 Blue borders** - Primary panels
- **🟩 Green borders** - Activity/success
- **🟨 Yellow borders** - Actions/warnings
- **🟥 Red text** - Errors
- **🟦 Cyan text** - Highlighted values

## 🔧 Integration with CLI Commands

The TUI integrates with all existing CLI tools:

| TUI Screen | Equivalent CLI Command |
|------------|------------------------|
| Dashboard Stats | `ss status` |
| Config List | `ss config list` |
| New Config | `ss config create` / `ss init` |
| Config Validate | `ss config validate <config>` |
| Start Scrape | `ss scrape run <config>` |
| Estimate Pages | `ss scrape estimate <config>` |
| Enhance Local | `ss enhance local <skill>` |
| Enhance API | `ss enhance api <skill>` |
| Package Skill | `ss package single <skill>` |
| Upload Skill | `ss upload skill <file>` |

## 🎯 Typical Workflow in TUI

### First-Time User:

1. **Launch TUI:** `ss gui`
2. **Press `c`** to go to Configuration Manager
3. **Click "📝 New"** to create a config
4. **Fill out form** with your documentation details
5. **Click "✓ Create"**
6. **Press `Escape`** to return to dashboard
7. **Press `s`** to go to Scraper
8. **Select your config** from dropdown
9. **Click "📊 Estimate Only"** to see page count first
10. **Click "🚀 Start Scrape"** when ready
11. **Wait for scraping** to complete (progress bar shows status)
12. **Press `k`** to go to Skill Manager
13. **Select your skill** from table
14. **Click "✨ Enhance (Local)"** to improve quality
15. **Click "📦 Package"** to create .zip file
16. **Click "📤 Upload to Claude"** to upload

### Power User (Cached Data):

1. `ss gui`
2. Press `k` → Select skill → "✨ Enhance" → "📦 Package" → "📤 Upload"
3. Done in 30 seconds!

## 🐛 Troubleshooting

### TUI won't launch

**Error:** `textual package not installed`

**Solution:**
```bash
pip install textual
# or
pipx install skillseeker
pipx inject skillseeker textual
```

### Mouse not working

Make sure your terminal supports mouse:
- ✅ Modern terminals (iTerm2, Windows Terminal, Alacritty, Kitty)
- ✅ tmux with mouse mode enabled
- ⚠️ Old terminals may have limited support

### Colors look wrong

Set your terminal to 256-color mode or true color support.

### TUI is slow

- Reduce the number of items in tables
- Clear old cached data with `ss clean all`

## 💡 Tips & Tricks

1. **Keyboard shortcuts are faster:** Learn `c`, `s`, `k`, `d`, `q` for quick navigation

2. **Preview before action:** Always select items in tables to see previews before taking action

3. **Check dashboard first:** The dashboard shows you what needs attention (uncached data, unpackaged skills, etc.)

4. **Use Quick Actions:** The dashboard Quick Actions are one-click shortcuts to common tasks

5. **Multi-screen workflow:** You can navigate between screens without losing your place

6. **Status indicators:** Look for ✨ (enhanced) and 📦 (packaged) icons in skill table

7. **Form validation:** New Config form validates inputs before saving

8. **Log outputs:** Scrape and Upload screens show live logs for monitoring

## 🎓 Advanced Features (Coming Soon)

The TUI framework supports future enhancements:

- [ ] Real-time scraping progress (page count, current URL)
- [ ] Inline config editing
- [ ] Diff viewer for enhanced skills
- [ ] Batch operations (select multiple skills)
- [ ] Skill comparison tool
- [ ] Custom themes and color schemes
- [ ] Plugin system for custom screens
- [ ] Export dashboard as report

## 📚 Additional Resources

- **Textual Documentation:** https://textual.textualize.io/
- **CLI Reference:** `ss --help`
- **Project Docs:** See README.md and docs/

## 🤝 Feedback

Found a bug or have a feature request for the TUI?
- Use the CLI: `ss --help` for contact info
- Or check the main README.md

---

**Enjoy the interactive experience! 🎉**
