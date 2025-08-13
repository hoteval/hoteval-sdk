#!/usr/bin/env python3
"""Create PR and release draft for the HotEval Python SDK."""

import re
import sys

import requests
from shared import CHANGELOG_FILE, GITHUB_TOKEN, REPO, run_command


def get_latest_version_from_changelog() -> str:
    """Get the most recently listed version from the changelog."""
    with open(CHANGELOG_FILE) as f:
        for line in f:
            match = re.match(r'^## \[v(\d+\.\d+\.\d+)\]', line)
            if match:
                return match.group(1)
    raise ValueError('Latest version not found in changelog')


def get_latest_release_notes_from_changelog() -> str:
    """Get the release notes for the latest version from the changelog."""
    with open(CHANGELOG_FILE) as f:
        content = f.read()

    # Find the first version section
    match = re.search(r'^## \[v(\d+\.\d+\.\d+)\] \([^)]+\)\n\n(.*?)(?=\n## \[v|\nZ)', content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(2).strip()

    raise ValueError('Latest release notes not found in changelog')


def commit_and_push_changes(version: str) -> None:
    """Commit and push changes to a new branch."""
    branch_name = f'release/v{version}'

    # Create and switch to new branch
    run_command('git', 'checkout', '-b', branch_name)

    # Add all changes
    run_command('git', 'add', '.')

    # Commit changes
    run_command('git', 'commit', '-m', f'Release v{version}')

    # Push to origin
    run_command('git', 'push', 'origin', branch_name)

    print(f"✅ Pushed changes to branch: {branch_name}")


def create_pull_request(version: str) -> str:
    """Create a pull request on GitHub."""
    if not GITHUB_TOKEN:
        print("❌ No GitHub token available. Cannot create PR.")
        return ""

    url = f'https://api.github.com/repos/{REPO}/pulls'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
    }

    data = {
        'title': f'Release v{version}',
        'head': f'release/v{version}',
        'base': 'main',
        'body': f'''Release v{version}

This PR contains:
- Version bump to v{version}
- Updated CHANGELOG.md with release notes

After merging this PR, publish the release draft to complete the release process.
''',
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        pr_url = response.json()['html_url']
        print(f"✅ Created PR: {pr_url}")
        return pr_url
    except Exception as e:
        print(f"❌ Failed to create PR: {e}")
        return ""


def create_github_release_draft(version: str, release_notes: str) -> str:
    """Create a GitHub release draft."""
    if not GITHUB_TOKEN:
        print("❌ No GitHub token available. Cannot create release draft.")
        return ""

    url = f'https://api.github.com/repos/{REPO}/releases'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
    }

    data = {
        'tag_name': f'v{version}',
        'name': f'v{version}',
        'body': release_notes,
        'draft': True,
        'prerelease': False,
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        release_data = response.json()

        # Return the edit URL for easier publishing
        release_url = release_data['html_url']
        edit_url = release_url.replace('/releases/tag/', '/releases/edit/')
        print(f"✅ Created release draft: {edit_url}")
        return edit_url
    except Exception as e:
        print(f"❌ Failed to create release draft: {e}")
        return ""


def check_git_status() -> None:
    """Check if there are any uncommitted changes."""
    try:
        status = run_command('git', 'status', '--porcelain')
        if not status.strip():
            print("❌ No changes to commit. Run 'python scripts/release/prepare.py VERSION' first.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to check git status: {e}")
        sys.exit(1)


def check_on_main_branch() -> None:
    """Check if we're on the main branch."""
    try:
        current_branch = run_command('git', 'branch', '--show-current')
        if current_branch != 'main':
            print(f"❌ Must be on 'main' branch, currently on '{current_branch}'")
            print("Run 'git checkout main' first")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to check current branch: {e}")
        sys.exit(1)


if __name__ == '__main__':
    """Automate the release PR and draft creation process."""

    print("🚀 Creating release PR and draft...")

    # Pre-flight checks
    check_on_main_branch()
    check_git_status()

    try:
        version = get_latest_version_from_changelog()
        release_notes = get_latest_release_notes_from_changelog()
    except ValueError as e:
        print(f"❌ {e}")
        print("Make sure you've run 'python scripts/release/prepare.py VERSION' first")
        sys.exit(1)

    print(f"📋 Preparing release v{version}")

    # Create branch and push changes
    commit_and_push_changes(version)

    # Create PR
    pr_url = create_pull_request(version)

    # Create release draft
    draft_url = create_github_release_draft(version, release_notes)

    print(f"\n✅ Release process completed for v{version}")

    if pr_url:
        print(f"📋 Review and merge PR: {pr_url}")

    if draft_url:
        print(f"🚀 Publish release when ready: {draft_url}")

    print("\nNext steps:")
    print("1. Review and merge the PR")
    print("2. Publish the release draft on GitHub")
    print("3. The GitHub Action will automatically publish to PyPI")