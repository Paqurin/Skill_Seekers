# Publishing Skill Seeker to PyPI

Complete guide for maintainers on how to publish new versions to PyPI.

## Prerequisites

### 1. Install Build Tools

```bash
pip install build twine
```

### 2. Set Up PyPI Account

1. Create account at https://pypi.org/account/register/
2. Verify email
3. Enable 2FA (required for publishing)

### 3. Configure Trusted Publishing (Recommended)

**Trusted Publishing** is the modern, secure way to publish to PyPI without API tokens.

#### On PyPI:

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new pending publisher:
   - **PyPI Project Name:** `skillseeker`
   - **Owner:** `yourusername` (your GitHub username)
   - **Repository name:** `Skill_Seekers`
   - **Workflow name:** `publish-pypi.yml`
   - **Environment name:** `pypi`
3. Save

#### On Test PyPI (for testing):

1. Go to https://test.pypi.org/manage/account/publishing/
2. Add the same configuration with environment name: `testpypi`

---

## Publishing Process

### Option 1: Automatic Publishing (Recommended)

Publish automatically when creating a GitHub release.

#### Steps:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "2.1.0"  # Increment version
   ```

2. **Commit changes**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 2.1.0"
   git push
   ```

3. **Create Git tag**:
   ```bash
   git tag v2.1.0
   git push origin v2.1.0
   ```

4. **Create GitHub Release**:
   - Go to https://github.com/yourusername/Skill_Seekers/releases/new
   - Select tag: `v2.1.0`
   - Release title: `v2.1.0`
   - Describe changes
   - Click "Publish release"

5. **GitHub Actions automatically**:
   - Builds the package
   - Publishes to TestPyPI
   - Publishes to PyPI (production)

6. **Verify**:
   - Check https://pypi.org/project/skillseeker/
   - Test installation: `pipx install skillseeker`

---

### Option 2: Manual Publishing

For testing or when automatic publishing isn't available.

#### Step 1: Build the Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build new distribution
python -m build
```

This creates:
- `dist/skillseeker-2.0.0.tar.gz` (source distribution)
- `dist/skillseeker-2.0.0-py3-none-any.whl` (wheel distribution)

#### Step 2: Check the Build

```bash
twine check dist/*
```

Should output: `Checking dist/... PASSED`

#### Step 3: Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pipx install --index-url https://test.pypi.org/simple/ skillseeker
```

If it works, uninstall:
```bash
pipx uninstall skillseeker
```

#### Step 4: Upload to PyPI

```bash
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

Or use Trusted Publishing (no credentials needed).

#### Step 5: Verify

```bash
# Install from PyPI
pipx install skillseeker

# Test it works
ss --version
ss --help
```

---

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (2.0.0 → 2.1.0): New features, backwards compatible
- **Patch** (2.1.0 → 2.1.1): Bug fixes, backwards compatible

### Pre-releases:

- Alpha: `2.1.0a1`
- Beta: `2.1.0b1`
- Release Candidate: `2.1.0rc1`

---

## Checklist Before Publishing

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run tests: `pytest`
- [ ] Test CLI locally: `pip install -e .` then `ss --help`
- [ ] Build package: `python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] Test on TestPyPI (optional)
- [ ] Create git tag
- [ ] Push tag to GitHub
- [ ] Create GitHub Release (triggers auto-publish)
- [ ] Verify on PyPI
- [ ] Test installation: `pipx install skillseeker`

---

## Troubleshooting

### "Package already exists"

You can't overwrite a version on PyPI. Increment the version number.

### "Invalid distribution"

Run `twine check dist/*` to see what's wrong. Common issues:
- Missing `README.md`
- Invalid `pyproject.toml` syntax
- Missing required metadata

### "Authentication failed"

For manual upload:
1. Create API token at https://pypi.org/manage/account/token/
2. Use `__token__` as username
3. Use token value as password

For Trusted Publishing:
1. Verify configuration on PyPI
2. Check GitHub Actions workflow
3. Ensure repository/workflow names match exactly

### Build fails

```bash
# Update build tools
pip install --upgrade build setuptools wheel

# Clean and rebuild
rm -rf dist/ build/ *.egg-info
python -m build
```

---

## Post-Publishing

### 1. Announce Release

- Update README.md with new version
- Post in discussions/community
- Update documentation

### 2. Monitor

- Check PyPI download stats
- Monitor GitHub issues for bug reports
- Watch for user feedback

### 3. Next Steps

Start planning next version:
- Create milestone for next release
- Label issues for next version
- Update project board

---

## Publishing Workflow Summary

```
┌─────────────────────┐
│  Update version in  │
│   pyproject.toml    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Update CHANGELOG   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Run tests         │
│   pytest            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Commit & push      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Create git tag     │
│  git tag v2.1.0     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Push tag           │
│  git push --tags    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Create GitHub      │
│  Release            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  GitHub Actions     │
│  auto-publishes     │
│  to PyPI ✅         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Verify on PyPI     │
│  Test install       │
└─────────────────────┘
```

---

## Resources

- **PyPI**: https://pypi.org/project/skillseeker/
- **Test PyPI**: https://test.pypi.org/project/skillseeker/
- **Python Packaging Guide**: https://packaging.python.org/
- **Trusted Publishing Guide**: https://docs.pypi.org/trusted-publishers/
- **Semantic Versioning**: https://semver.org/

---

## Quick Reference

```bash
# Local development
pip install -e .

# Run tests
pytest

# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Or just create GitHub Release and it auto-publishes!
```

---

**Questions?** Open an issue or check the Python Packaging documentation.
