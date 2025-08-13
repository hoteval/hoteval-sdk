# HotEval SDK Release Process

Modern, semi-automated release process for the HotEval Python SDK.

## Prerequisites

### Required Tools
- **GitHub CLI**: `gh` command for API access
  ```bash
  # Install on macOS
  brew install gh

  # Install on Linux
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt update
  sudo apt install gh
  ```

- **Authentication**: GitHub token for API access
  ```bash
  gh auth login
  ```

### Python Dependencies
```bash
# From repo root
pip install requests
```

## Release Workflow

### 1. Prepare Release
```bash
# From repo root
python scripts/release/prepare.py 0.1.0
```

**What this does:**
- ✅ Updates version in `python/pyproject.toml`
- ✅ Updates version in `python/hoteval/__init__.py`
- ✅ Runs code quality checks (black, ruff)
- ✅ Runs tests to ensure everything works
- ✅ Generates release notes from GitHub API
- ✅ Updates `CHANGELOG.md` with new release
- ✅ Adds comparison links to changelog

### 2. Review Changes
Review the generated `CHANGELOG.md`:
- Check that release notes are accurate
- Add any missing important changes
- Fix any formatting issues
- Mark breaking changes with **Breaking Change:**

### 3. Create PR and Release Draft
```bash
# From repo root
python scripts/release/push.py
```

**What this does:**
- ✅ Creates a new branch `release/v{VERSION}`
- ✅ Commits all changes
- ✅ Pushes branch to GitHub
- ✅ Creates a Pull Request
- ✅ Creates a draft GitHub release

### 4. Complete Release
1. **Review and merge the PR** - This updates the main branch
2. **Publish the release** - This triggers CI to publish to PyPI
3. **Celebrate** 🎉

## Manual Release (Alternative)

For releases from non-main branches or when automation fails:

### 1. Update Versions Manually
```bash
# Update python/pyproject.toml
version = "0.1.0"

# Update python/hoteval/__init__.py
__version__ = "0.1.0"
```

### 2. Update Changelog
Add a new section to `CHANGELOG.md`:
```markdown
## [v0.1.0] (2024-01-15)

### Added
- Initial release of HotEval Python SDK
- Runtime evaluation for agentic AI systems
- Simple data collection API

### Changed
- Moved from beta to stable release

[v0.1.0]: https://github.com/hoteval/hoteval-sdk/compare/v0.0.1...v0.1.0
```

### 3. Test and Build
```bash
cd python/
python -m pytest tests/ -v
python -m black --check hoteval/
python -m ruff check hoteval/
python -m build
```

### 4. Create Release
1. Create PR with changes
2. Merge PR
3. Create GitHub release with tag `v0.1.0`
4. CI will automatically publish to PyPI

## Troubleshooting

### "No GitHub token found"
```bash
# Install and authenticate with GitHub CLI
gh auth login

# Or set environment variable
export GITHUB_TOKEN="your_token_here"
```

### "Tests failed"
```bash
# Fix code issues
cd python/
python -m black hoteval/
python -m ruff check --fix hoteval/

# Run tests to see what's failing
python -m pytest tests/ -v
```

### "Version already exists in changelog"
- Check if you've already prepared this version
- Use a different version number
- Or manually edit the changelog

### "Must be on main branch"
```bash
git checkout main
git pull origin main
```

### "No changes to commit"
- Make sure you ran `prepare.py` first
- Check if there are any pending changes: `git status`

## GitHub Actions Integration

The release process integrates with GitHub Actions:

1. **On Release Published**: Automatically builds and publishes to PyPI
2. **On PR Creation**: Runs tests and quality checks
3. **On Push to main**: Runs full test suite

## Security

- **GitHub token**: Only needs public repo access for release notes generation
- **PyPI publishing**: Handled securely through GitHub Actions with OIDC
- **No secrets in scripts**: All authentication through GitHub CLI or environment variables

## Benefits Over Manual Process

### ✅ **Automated**
- Version updates in multiple files
- Changelog generation from commits
- Release notes from GitHub API
- PR and release draft creation

### ✅ **Safe**
- Pre-flight checks (tests, linting)
- Review process via PR
- Draft releases prevent accidental publishing
- Rollback possible before publishing

### ✅ **Consistent**
- Standardized changelog format
- Consistent version numbering
- Automatic comparison links
- Professional release notes

### ✅ **Traceable**
- Full git history of release changes
- GitHub release with detailed notes
- PR discussion for review
- Automatic tagging