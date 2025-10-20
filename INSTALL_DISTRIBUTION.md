# Skill Seeker Installation Guide

Multiple ways to install Skill Seeker CLI - choose the method that works best for you!

---

## 🌟 Recommended: pipx (Modern Python Standard)

**Best for:** Most users, especially Python developers

### Why pipx?

- ✅ Isolated environments (no dependency conflicts)
- ✅ Automatic PATH management
- ✅ Easy updates
- ✅ Industry standard for CLI tools
- ✅ Recommended by Python Packaging Authority

### Installation

```bash
# 1. Install pipx (one-time setup)
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 2. Restart your terminal, then install Skill Seeker
pipx install skillseeker

# 3. Verify installation
ss --version
ss --help
```

### Usage

```bash
# Use anywhere
ss init
ss status
ss workflow full react.json

# Update to latest version
pipx upgrade skillseeker

# Uninstall
pipx uninstall skillseeker
```

---

## 🐍 Option 2: pip (Traditional Python)

**Best for:** Quick installation, existing virtual environments

### Global Installation (Not Recommended)

```bash
pip install skillseeker
```

⚠️ **Warning:** May cause dependency conflicts with other packages.

### Virtual Environment (Better)

```bash
# Create virtual environment
python3 -m venv ~/skillseeker-env

# Activate it
source ~/skillseeker-env/bin/activate  # macOS/Linux
# or
~/skillseeker-env\Scripts\activate  # Windows

# Install
pip install skillseeker

# Use
ss --help
```

### User Installation (Compromise)

```bash
pip install --user skillseeker
```

---

## 💻 Option 3: From Source (Development)

**Best for:** Contributors, developers, testing latest features

### Clone and Install

```bash
# Clone repository
git clone https://github.com/yourusername/Skill_Seekers.git
cd Skill_Seekers

# Install in editable mode
pip install -e .

# Or with all optional dependencies
pip install -e ".[dev,api,mcp]"

# Verify
ss --version
```

### Benefits

- ✅ Latest unreleased features
- ✅ Easy to modify code
- ✅ Changes reflect immediately
- ✅ Can contribute back

---

## 🍺 Option 4: Homebrew (macOS/Linux)

**Status:** Coming soon!

**Best for:** macOS/Linux users who prefer Homebrew

```bash
# Will be available as:
brew install skillseeker

# Update
brew upgrade skillseeker
```

*Currently in development. Use pipx for now.*

---

## 📦 Option 5: npm (Node.js Ecosystem)

**Status:** Coming soon!

**Best for:** Teams already using Node.js/npm

```bash
# Will be available as:
npm install -g skillseeker

# Update
npm update -g skillseeker
```

*Currently in development. Use pipx for now.*

---

## 💾 Option 6: Standalone Binary (Zero Dependencies)

**Status:** Coming soon!

**Best for:** Non-technical users, no Python needed

Download from [GitHub Releases](https://github.com/yourusername/Skill_Seekers/releases):

- `skillseeker-windows.exe` - Windows
- `skillseeker-macos` - macOS
- `skillseeker-linux` - Linux

```bash
# Download and run (example for Linux)
chmod +x skillseeker-linux
./skillseeker-linux --help
```

*Currently in development. Use pipx for now.*

---

## Platform-Specific Instructions

### macOS

```bash
# Install pipx via Homebrew
brew install pipx
pipx ensurepath

# Install Skill Seeker
pipx install skillseeker

# Done!
ss --version
```

### Linux (Debian/Ubuntu)

```bash
# Install pipx
sudo apt update
sudo apt install pipx
pipx ensurepath

# Install Skill Seeker
pipx install skillseeker

# Done!
ss --version
```

### Linux (Fedora/RHEL)

```bash
# Install pipx
sudo dnf install pipx
pipx ensurepath

# Install Skill Seeker
pipx install skillseeker

# Done!
ss --version
```

### Linux (Arch)

```bash
# Install pipx
sudo pacman -S python-pipx
pipx ensurepath

# Install Skill Seeker
pipx install skillseeker

# Done!
ss --version
```

### Windows

```powershell
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Restart terminal, then:
pipx install skillseeker

# Done!
ss --version
```

---

## Verification

After installation, verify it works:

```bash
# Check version
ss --version

# Show help
ss --help

# Check status
ss status

# List presets
ss config list

# Run interactive wizard
ss init
```

**Expected output:**
```
skillseeker, version 2.0.0
```

---

## Troubleshooting

### "Command not found: ss"

**Solution 1:** Ensure PATH is configured

```bash
# For pipx
pipx ensurepath

# Then restart terminal
```

**Solution 2:** Use full command

```bash
python3 -m cli.skillseeker --help
```

**Solution 3:** Check installation location

```bash
pipx list  # Shows installed packages and their paths
which ss   # Shows command location
```

### "No module named 'click'"

You're missing dependencies. Reinstall:

```bash
pipx uninstall skillseeker
pipx install skillseeker
```

### "Permission denied"

Don't use `sudo` with pipx or pip --user. If you must:

```bash
# NOT recommended
sudo pip install skillseeker

# Recommended instead
pipx install skillseeker
```

### pipx not found

Install pipx first:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Then restart your terminal.

---

## Updating

### pipx

```bash
pipx upgrade skillseeker
```

### pip

```bash
pip install --upgrade skillseeker
```

### From source

```bash
cd Skill_Seekers
git pull
pip install -e .
```

---

## Uninstalling

### pipx

```bash
pipx uninstall skillseeker
```

### pip

```bash
pip uninstall skillseeker
```

### From source

```bash
pip uninstall skillseeker
```

---

## Which Method Should I Choose?

### Quick Decision Tree

```
Are you a Python developer?
├─ Yes → Use pipx (recommended)
└─ No
   ├─ Do you have Python installed?
   │  ├─ Yes → Use pipx
   │  └─ No → Wait for standalone binary (coming soon)
   └─ Are you a Node.js developer?
      └─ Yes → Wait for npm package (coming soon)
```

### Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **pipx** | Isolated, clean, recommended | Requires Python | Most users ⭐ |
| **pip** | Simple, familiar | May cause conflicts | Quick tests |
| **Source** | Latest features, editable | More setup | Contributors |
| **Homebrew** | Easy on Mac/Linux | Not available yet | Mac users |
| **npm** | Familiar to JS devs | Not available yet | Node.js teams |
| **Binary** | No dependencies | Large download | Non-technical |

---

## Next Steps

After installation:

1. **Read the CLI Guide:** [README_CLI.md](README_CLI.md)
2. **Run the wizard:** `ss init`
3. **Check the status:** `ss status`
4. **Explore commands:** `ss --help`

---

## Getting Help

### Documentation

- **CLI Reference:** [README_CLI.md](README_CLI.md)
- **Installation:** [INSTALL_CLI.md](INSTALL_CLI.md)
- **Publishing:** [PUBLISHING.md](PUBLISHING.md)
- **Project README:** [README.md](README.md)

### Support

- **Issues:** https://github.com/yourusername/Skill_Seekers/issues
- **Discussions:** https://github.com/yourusername/Skill_Seekers/discussions

---

**Ready to build skills?** 🚀

Start with: `pipx install skillseeker && ss init`
