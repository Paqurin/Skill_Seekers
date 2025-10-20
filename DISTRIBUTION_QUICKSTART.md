# Distribution Quick Start

Get Skill Seeker up and running in under 2 minutes!

---

## For Users (Installation)

### Option 1: pipx (Recommended ⭐)

```bash
# Install pipx (one-time)
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Close and reopen terminal, then:
pipx install skillseeker

# Done!
ss --version
ss init
```

### Option 2: pip

```bash
pip install skillseeker
ss --version
```

### Option 3: From Source

```bash
git clone https://github.com/yourusername/Skill_Seekers.git
cd Skill_Seekers
pip install -e .
ss --version
```

---

## For Maintainers (Publishing)

### First Time Setup

1. **Install tools:**
   ```bash
   pip install build twine
   ```

2. **Configure PyPI Trusted Publishing:**
   - Go to https://pypi.org/manage/account/publishing/
   - Add pending publisher:
     - Project: `skillseeker`
     - Owner: `yourusername`
     - Repo: `Skill_Seekers`
     - Workflow: `publish-pypi.yml`
     - Environment: `pypi`

3. **Do same for TestPyPI:**
   - Go to https://test.pypi.org/manage/account/publishing/
   - Environment: `testpypi`

### Publishing a Release

```bash
# 1. Update version in pyproject.toml
version = "2.1.0"

# 2. Update CHANGELOG.md with changes

# 3. Commit
git add pyproject.toml CHANGELOG.md
git commit -m "Release v2.1.0"

# 4. Tag
git tag v2.1.0

# 5. Push
git push && git push --tags

# 6. Create GitHub Release
# Go to: https://github.com/yourusername/Skill_Seekers/releases/new
# Select tag: v2.1.0
# Click "Publish release"

# 7. GitHub Actions auto-publishes to PyPI! ✅
```

### Manual Testing (Optional)

```bash
# Build locally
python -m build

# Check
twine check dist/*

# Test on TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI
pipx install --index-url https://test.pypi.org/simple/ skillseeker

# Test it
ss --version

# Clean up
pipx uninstall skillseeker
```

---

## Verification

After publishing:

```bash
# Install from PyPI
pipx install skillseeker

# Verify
ss --version         # Should show: 2.1.0
ss --help            # Should display help
ss config list       # Should list configs
ss status            # Should show status

# Check PyPI
# Visit: https://pypi.org/project/skillseeker/
```

---

## Troubleshooting

### "Package not found"

Wait 2-3 minutes after publishing, then:
```bash
pipx install --force skillseeker
```

### "Already exists" error when publishing

You can't overwrite a version. Increment version number in `pyproject.toml`.

### Build fails

```bash
# Update tools
pip install --upgrade build setuptools wheel

# Clean and rebuild
rm -rf dist/ build/ *.egg-info
python -m build
```

---

## Resources

- **Installation:** [INSTALL_DISTRIBUTION.md](INSTALL_DISTRIBUTION.md)
- **Publishing:** [PUBLISHING.md](PUBLISHING.md)
- **CLI Guide:** [README_CLI.md](README_CLI.md)
- **Summary:** [DISTRIBUTION_SUMMARY.md](DISTRIBUTION_SUMMARY.md)

---

**Ready to go!** 🚀

**Users:** `pipx install skillseeker`
**Maintainers:** See [PUBLISHING.md](PUBLISHING.md)
