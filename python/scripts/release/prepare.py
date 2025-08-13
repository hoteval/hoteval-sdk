#!/usr/bin/env python3
"""Prepare a new release for the HotEval Python SDK."""

import re
import sys
from datetime import date
from pathlib import Path

import requests
from shared import (
    CHANGELOG_FILE,
    GITHUB_TOKEN,
    PYTHON_INIT,
    PYTHON_PYPROJECT,
    REPO,
    run_command,
)


def update_version_pyproject(new_version: str) -> None:
    """Update the version in pyproject.toml."""
    # Work from python/ directory
    pyproject_path = Path("../..") / PYTHON_PYPROJECT
    with open(pyproject_path) as f:
        content = f.read()

    updated_content = re.sub(
        r'version\s*=\s*"[^\"]+"',
        f'version = "{new_version}"',
        content
    )

    with open(pyproject_path, 'w') as f:
        f.write(updated_content)

    print(f"Updated version in {PYTHON_PYPROJECT}")


def update_version_init(new_version: str) -> None:
    """Update the version in __init__.py."""
    # Work from python/ directory
    init_path = Path("../..") / PYTHON_INIT
    with open(init_path) as f:
        content = f.read()

    updated_content = re.sub(
        r'__version__\s*=\s*"[^\"]+"',
        f'__version__ = "{new_version}"',
        content
    )

    with open(init_path, 'w') as f:
        f.write(updated_content)

    print(f"Updated version in {PYTHON_INIT}")


def get_last_tag() -> str:
    """Get the latest tag from the Git repository."""
    try:
        return run_command('git', 'describe', '--tags', '--abbrev=0')
    except:  # noqa: E722
        return "v0.0.0"  # Default if no tags exist


def get_release_notes(new_version: str) -> str:
    """Generate release notes from GitHub's release notes generator."""
    if not GITHUB_TOKEN:
        return f"Release notes for v{new_version}\n\nPlease add release notes manually."

    last_tag = get_last_tag()

    data = {
        'target_committish': 'main',
        'previous_tag_name': last_tag,
        'tag_name': f'v{new_version}',
    }

    try:
        response = requests.post(
            f'https://api.github.com/repos/{REPO}/releases/generate-notes',
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {GITHUB_TOKEN}',
            },
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        body = response.json()['body']

        # Clean up the release notes
        body = re.sub(r'<!--.*?-->\n\n', '', body)
        body = re.sub(r'([^\n])(\n#+ .+?\n)', r'\1\n\2', body)  # Add blank line before headers
        body = re.sub(
            rf'https://github.com/{REPO}/pull/(\d+)',
            rf'[#\1](https://github.com/{REPO}/pull/\1)',
            body
        )
        body = re.sub(r'\*\*Full Changelog.*', '', body, flags=re.DOTALL)
        body = re.sub(r"## What's Changed\n", '', body)

        return body.strip()

    except Exception as e:
        print(f"Warning: Failed to generate release notes from GitHub: {e}")
        return f"Release notes for v{new_version}\n\nPlease add release notes manually."


def create_changelog_if_missing() -> None:
    """Create CHANGELOG.md if it doesn't exist."""
    changelog_path = Path(CHANGELOG_FILE)
    if not changelog_path.exists():
        changelog_content = """# Release Notes

## [Unreleased]

### Added
- Initial release of HotEval Python SDK

### Changed

### Fixed

"""
        changelog_path.write_text(changelog_content)
        print(f"Created {CHANGELOG_FILE}")


def update_changelog(new_version: str, notes: str) -> None:
    """Update CHANGELOG.md with the new release notes."""
    create_changelog_if_missing()

    changelog_path = Path(CHANGELOG_FILE)
    changelog_content = changelog_path.read_text()

    date_today = date.today().strftime('%Y-%m-%d')
    title = f'## [v{new_version}] ({date_today})'

    if title in changelog_content:
        print(f'WARNING: {title} already exists in CHANGELOG.md')
        return

    new_chunk = f'{title}\n\n{notes}\n\n'

    # Insert after the first header (# Release Notes)
    updated_content = re.sub(
        r'(# Release Notes\n\n)',
        rf'\1{new_chunk}',
        changelog_content
    )

    changelog_path.write_text(updated_content)

    # Add comparison link at the end
    last_tag = get_last_tag()
    compare_link = f'[v{new_version}]: https://github.com/{REPO}/compare/{last_tag}...v{new_version}\n'

    with open(changelog_path, 'a') as f:
        f.write(compare_link)

    print(f"Updated {CHANGELOG_FILE}")


def run_tests() -> None:
    """Run tests to ensure everything works."""
    print("🧪 Running tests...")
    try:
        run_command('uv', 'run', 'pytest', 'tests/', '-v', cwd='../..')
        print("✅ Tests passed")
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        sys.exit(1)


def check_code_quality() -> None:
    """Run code quality checks."""
    print("🔍 Checking code quality...")
    try:
        run_command('uv', 'run', 'ruff', 'check', 'hoteval/', cwd='../..')
        run_command('uv', 'run', 'ruff', 'format', '--check', '--diff', 'hoteval/', cwd='../..')
        print("✅ Code quality checks passed")
    except Exception as e:
        print(f"❌ Code quality checks failed: {e}")
        print("Run 'make format-python' to fix formatting issues")
        sys.exit(1)


if __name__ == '__main__':
    """Automate the version bump and changelog update process."""

    if len(sys.argv) != 2:
        print('Usage: python prepare.py {VERSION}')
        print('Example: python prepare.py 0.1.0')
        sys.exit(1)

    version = sys.argv[1]

    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print('Error: Version must be in format X.Y.Z (e.g., 0.1.0)')
        sys.exit(1)

    print(f"🚀 Preparing release v{version}")

    # Update version numbers
    update_version_pyproject(version)
    update_version_init(version)

    # Run quality checks
    check_code_quality()
    run_tests()

    # Update changelog
    run_command('git', 'fetch', '--tags')  # Ensure we have latest tags
    release_notes = get_release_notes(version)
    update_changelog(version, release_notes)

    print(f"\n✅ Successfully prepared release v{version}")
    print("\nNext steps:")
    print("1. Review the changes in CHANGELOG.md")
    print("2. Run 'python scripts/release/push.py' to create PR and release draft")
    print("3. Review and merge the PR")
    print("4. Publish the release on GitHub")
