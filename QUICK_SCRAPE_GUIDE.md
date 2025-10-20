# 🌐 Quick Scrape Feature - TUI Guide

## Overview

The Scraper screen now has **two modes** accessible via tabs:

1. **📋 From Config** - Use existing configuration files
2. **🌐 Quick Scrape** - Scrape directly from a URL without creating a config first

## 🚀 Quick Scrape Tab

### What It Does

Quick Scrape allows you to start scraping documentation immediately by entering:
- Skill name
- Documentation URL
- Basic settings

**No config file needed!** Perfect for testing or one-off scrapes.

### How to Use

1. **Launch TUI:**
   ```bash
   ss gui
   ```

2. **Navigate to Scraper:**
   - Press `s` or click "🔍 Start Scrape" on dashboard

3. **Switch to Quick Scrape tab:**
   - Click "🌐 Quick Scrape" tab at the top

4. **Fill in the form:**

   | Field | Description | Example |
   |-------|-------------|---------|
   | **Skill Name** | Identifier for your skill | `react`, `vue`, `my-docs` |
   | **Documentation URL** | Starting URL | `https://react.dev/` |
   | **Description** | When to use this skill | `React framework for building UIs` |
   | **Max Pages** | Maximum pages to scrape | `100` (default) |
   | **Main Content Selector** | CSS selector for content | `article` (default) |

5. **Choose an action:**
   - **🚀 Scrape Now** - Start scraping immediately with these settings
   - **💾 Save as Config** - Save settings as a config file for reuse

### Form Fields Explained

#### Skill Name (Required)
- Must be unique
- Used for output directory name: `output/{name}/`
- Examples: `react`, `vue-docs`, `python-tutorial`

#### Documentation URL (Required)
- Starting point for scraping
- Must be a valid HTTP/HTTPS URL
- Examples:
  - `https://react.dev/`
  - `https://docs.python.org/3/`
  - `https://vuejs.org/guide/`

#### Description (Optional)
- Helps Claude understand when to use this skill
- Auto-generated if left empty: `"Documentation for {name}"`
- Examples:
  - `"React framework for building user interfaces"`
  - `"Python 3 official documentation"`

#### Max Pages (Optional)
- Limits how many pages to scrape
- Default: `100`
- Recommended values:
  - Testing: `10-20`
  - Small docs: `50-100`
  - Medium docs: `100-500`
  - Large docs: `500-2000`

#### Main Content Selector (Optional)
- CSS selector to find main content on pages
- Default: `article`
- Common selectors:
  - `article` - Most modern documentation
  - `main` - HTML5 main element
  - `div[role="main"]` - Accessibility-focused sites
  - `div.content` - Custom class names
  - `.documentation` - Class-based selector

**How to find the right selector:**
1. Open documentation site in browser
2. Right-click on main content area
3. Select "Inspect Element"
4. Look for the parent element containing all content
5. Use its tag name, class, or role attribute

### Buttons

#### 🚀 Scrape Now
- Creates temporary config from form values
- Starts scraping immediately
- Does **not** save config to `configs/` directory
- Perfect for one-time scrapes or testing

**What happens:**
1. Validates form inputs (name and URL required)
2. Creates temporary config in memory
3. Displays scraping plan in log
4. Starts scraping process (integration pending)
5. Outputs to `output/{name}/`

#### 💾 Save as Config
- Saves form values as a permanent config file
- Saves to `configs/{name}.json`
- Can be reused later from "📋 From Config" tab
- Perfect for documentation you'll scrape regularly

**What happens:**
1. Validates form inputs
2. Creates config file at `configs/{name}.json`
3. Shows success message
4. Refreshes config dropdown in other tab
5. **Does not start scraping** - use "From Config" tab after saving

## 📋 From Config Tab

### What It Does

Uses existing configuration files from `configs/` directory with full control over:
- URL patterns (include/exclude)
- Categories for organizing content
- Custom selectors
- Rate limiting

### How to Use

1. **Select a config** from dropdown
2. **Set options:**
   - ☐ Skip Scrape (use cache) - Rebuild from cached data
   - ☐ Resume from checkpoint - Continue interrupted scrape
   - ☐ Fresh start - Delete checkpoint and start over
3. **Override max pages** (optional)
4. **Click action:**
   - 🚀 Start Scrape - Begin scraping
   - 📊 Estimate Only - Check page count first

## 🎯 Workflow Examples

### Example 1: Quick Test Scrape

**Goal:** Test scraping React docs with 20 pages

1. `ss gui` → Press `s`
2. Click "🌐 Quick Scrape" tab
3. Fill in:
   - Name: `react-test`
   - URL: `https://react.dev/`
   - Max Pages: `20`
   - Selector: `article`
4. Click "🚀 Scrape Now"
5. Wait for completion (5-10 minutes)
6. Check `output/react-test/`

### Example 2: Save Config for Later

**Goal:** Create reusable config for Vue.js docs

1. `ss gui` → Press `s`
2. Click "🌐 Quick Scrape" tab
3. Fill in:
   - Name: `vue`
   - URL: `https://vuejs.org/guide/`
   - Description: `Vue.js framework documentation`
   - Max Pages: `100`
   - Selector: `main`
4. Click "💾 Save as Config"
5. See success: `✓ Saved to vue.json`
6. Switch to "📋 From Config" tab
7. Select `vue` from dropdown
8. Click "🚀 Start Scrape"

### Example 3: Find the Right Selector

**Goal:** Scrape custom documentation with unknown selector

1. Open docs site in browser
2. Right-click main content → Inspect
3. Find parent element: `<div class="docs-content">`
4. `ss gui` → Press `s` → "🌐 Quick Scrape"
5. Fill in:
   - Name: `my-docs`
   - URL: `https://my-docs.example.com/`
   - Selector: `div.docs-content`
6. Click "🚀 Scrape Now"

## 🔧 Advanced Tips

### 1. Testing Selectors
Always test with **small max_pages** (10-20) first to verify:
- Selector is correct
- Content is being extracted
- No errors occur

### 2. Save Often-Used Configs
If you'll scrape documentation multiple times (updates, different sections), use **"💾 Save as Config"** instead of quick scrape.

### 3. Use Estimate First
For config-based scraping, use **"📊 Estimate Only"** to check page count before full scrape.

### 4. Common Selectors by Platform

| Platform | Typical Selector |
|----------|-----------------|
| Read the Docs | `div[role="main"]` |
| MkDocs | `article` |
| Docusaurus | `article` |
| GitBook | `main` |
| Sphinx | `div.document` |
| Jekyll | `article.content` |
| Hugo | `article` or `main` |

### 5. URL Patterns
Quick scrape uses default patterns:
- **Excludes:** `/search`, `/_static/`
- **Includes:** Everything else

For custom patterns, save as config and edit the JSON file.

## 📊 Output

Both modes output to the same location:

```
output/
└── {skill-name}/
    ├── SKILL.md              # Main skill file
    ├── references/           # Categorized docs
    │   ├── index.md
    │   └── ...
    ├── scripts/              # Empty (user scripts)
    └── assets/               # Empty (user assets)

output/
└── {skill-name}_data/        # Cached scraped data
    ├── pages/
    │   └── *.json
    └── summary.json
```

## 🐛 Troubleshooting

### "Name and URL are required"
- Make sure both fields are filled in
- Skill name cannot be empty
- URL must start with `http://` or `https://`

### "No content extracted"
- Wrong selector - try different ones: `article`, `main`, `div.content`
- Use browser inspector to find correct selector
- Some sites may block scraping (check robots.txt)

### Config already exists
- If saving config and name already exists, it will overwrite
- Use different name or edit existing config file

### Slow scraping
- Documentation sites may have rate limiting
- Default rate limit: 0.5 seconds between requests
- Large docs (500+ pages) can take 30-60 minutes

## 🔗 Related Features

### CLI Equivalent

```bash
# Quick scrape via CLI
ss scrape run --name react --url https://react.dev/ --description "React docs" --max-pages 100

# Or use interactive mode
ss init
```

### After Scraping

Once scraping is complete:
1. Press `k` to go to Skill Manager
2. Select your skill
3. Click "✨ Enhance" to improve quality
4. Click "📦 Package" to create .zip
5. Click "📤 Upload" to send to Claude

## 📚 Further Reading

- [TUI_GUIDE.md](TUI_GUIDE.md) - Full TUI documentation
- [CLI_SUMMARY.md](CLI_SUMMARY.md) - CLI command reference
- [CLAUDE.md](CLAUDE.md) - Configuration details

---

**Happy scraping! 🚀**
