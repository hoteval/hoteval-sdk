"""Shared utilities for release scripts."""

import os
import subprocess


def run_command(*args: str, cwd: str | None = None) -> str:
    """Run a shell command and return the output."""
    result = subprocess.run(
        args,
        capture_output=True,
        check=True,
        encoding='utf-8',
        cwd=cwd
    )
    return result.stdout.strip()


# Configuration
REPO = 'hoteval/hoteval-sdk'
CHANGELOG_FILE = '../../CHANGELOG.md'  # Relative to python/scripts/release/
PYTHON_PYPROJECT = 'pyproject.toml'    # Relative to python/
PYTHON_INIT = 'hoteval/__init__.py'    # Relative to python/

# Get GitHub token
try:
    GITHUB_TOKEN = run_command('gh', 'auth', 'token')
except (subprocess.CalledProcessError, FileNotFoundError):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    if not GITHUB_TOKEN:
        print("Warning: No GitHub token found. Install 'gh' CLI or set GITHUB_TOKEN env var.")
