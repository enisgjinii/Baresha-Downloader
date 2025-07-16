#!/usr/bin/env python3
"""
Test script for the automatic release system.
This script helps you understand how conventional commits work.
"""

import re
import sys
from typing import Dict, List, Tuple


def parse_commit_message(message: str) -> Dict:
    """
    Parse a conventional commit message and return its components.

    Args:
        message: The commit message to parse

    Returns:
        Dictionary with parsed components
    """
    # Conventional commit pattern
    pattern = r"^(?P<type>feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s+(?P<description>.+)$"

    match = re.match(pattern, message)
    if not match:
        return {"valid": False, "error": "Does not follow conventional commit format"}

    groups = match.groupdict()

    # Check for breaking change in body
    breaking_change = "BREAKING CHANGE:" in message

    # Determine version bump type
    bump_type = "none"
    if groups["type"] == "feat" and not groups["breaking"] and not breaking_change:
        bump_type = "minor"
    elif groups["type"] == "fix" and not groups["breaking"] and not breaking_change:
        bump_type = "patch"
    elif groups["breaking"] or breaking_change:
        bump_type = "major"
    elif groups["type"] in ["docs", "style", "refactor", "test", "chore", "ci", "build", "perf"]:
        bump_type = "none"

    return {
        "valid": True,
        "type": groups["type"],
        "scope": groups["scope"],
        "description": groups["description"],
        "breaking": bool(groups["breaking"] or breaking_change),
        "bump_type": bump_type,
        "message": message,
    }


def get_version_bump_example(current_version: str, bump_type: str) -> str:
    """
    Get an example of how the version would change.

    Args:
        current_version: Current version (e.g., "1.0.0")
        bump_type: Type of bump ("major", "minor", "patch", "none")

    Returns:
        Example version change
    """
    if bump_type == "none":
        return f"{current_version} (no change)"

    parts = current_version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"

    return current_version


def test_commit_messages() -> List[Dict]:
    """
    Test various commit message examples.

    Returns:
        List of test results
    """
    test_messages = [
        "feat: add playlist download support",
        "fix: resolve memory leak in batch downloads",
        "docs: update installation instructions",
        "style: format code according to style guide",
        "refactor: improve error handling in download engine",
        "test: add unit tests for video info extraction",
        "chore: update dependencies",
        "ci: add automated testing workflow",
        "build: update build configuration",
        "perf: optimize video processing algorithm",
        "revert: revert to previous download method",
        "feat(ui): add dark mode toggle",
        "fix(download): resolve resume issue for large files",
        "feat!: completely redesign application architecture",
        "feat: add new download format\n\nBREAKING CHANGE: API has changed significantly",
        "just some random commit message",
        "updated stuff",
        "fixed bug",
        "new feature",
    ]

    results = []
    for message in test_messages:
        result = parse_commit_message(message)
        results.append(result)

    return results


def print_results(results: List[Dict], current_version: str = "1.0.0"):
    """
    Print formatted results of commit message analysis.

    Args:
        results: List of parsed commit messages
        current_version: Current version to use in examples
    """
    print("🚀 Conventional Commit Message Tester")
    print("=" * 50)
    print()

    print("📋 Test Results:")
    print("-" * 50)

    for i, result in enumerate(results, 1):
        print(f"\n{i:2d}. {result['message']}")

        if result["valid"]:
            bump_type = result["bump_type"]
            new_version = get_version_bump_example(current_version, bump_type)

            status = "✅ VALID"
            if bump_type == "major":
                status += " (MAJOR RELEASE)"
            elif bump_type == "minor":
                status += " (MINOR RELEASE)"
            elif bump_type == "patch":
                status += " (PATCH RELEASE)"
            else:
                status += " (NO RELEASE)"

            print(f"    {status}")
            print(f"    Type: {result['type']}")
            if result["scope"]:
                print(f"    Scope: {result['scope']}")
            print(f"    Description: {result['description']}")
            print(f"    Breaking Change: {'Yes' if result['breaking'] else 'No'}")
            print(f"    Version: {current_version} → {new_version}")
        else:
            print(f"    ❌ INVALID: {result['error']}")
            print(f"    Version: {current_version} (no change)")


def print_usage_guide():
    """
    Print usage guide for conventional commits.
    """
    print("\n📚 Conventional Commit Guide:")
    print("=" * 50)

    print("\n🎯 Format:")
    print("   <type>(<scope>): <description>")
    print()
    print("   [optional body]")
    print()
    print("   [optional footer(s)]")

    print("\n📝 Types that trigger releases:")
    print("   feat:     New feature (minor version bump)")
    print("   fix:      Bug fix (patch version bump)")
    print("   BREAKING CHANGE: Breaking change (major version bump)")
    print("   revert:   Revert previous commit (patch version bump)")

    print("\n📝 Types that don't trigger releases:")
    print("   docs:     Documentation changes")
    print("   style:    Code style changes")
    print("   refactor: Code refactoring")
    print("   test:     Adding or updating tests")
    print("   chore:    Maintenance tasks")
    print("   ci:       CI/CD changes")
    print("   build:    Build system changes")
    print("   perf:     Performance improvements")

    print("\n💡 Examples:")
    print("   feat: add playlist download support")
    print("   fix: resolve download resume issue")
    print("   feat(ui): add dark mode toggle")
    print("   fix(download): resolve memory leak")
    print("   feat!: completely redesign UI")
    print("   feat: add new API\n\nBREAKING CHANGE: API has changed")

    print("\n🚀 How to use:")
    print("   1. Write your commit message in conventional format")
    print("   2. Push to main/master branch")
    print("   3. GitHub Actions will automatically create a release")
    print("   4. Or manually create a tag: git tag -a v1.1.0 -m 'Release v1.1.0'")


def main():
    """
    Main function to run the test script.
    """
    if len(sys.argv) > 1:
        # Test a specific commit message
        message = " ".join(sys.argv[1:])
        result = parse_commit_message(message)
        current_version = "1.0.0"

        print("🚀 Conventional Commit Message Tester")
        print("=" * 50)
        print()
        print(f"Testing: {message}")
        print("-" * 50)

        if result["valid"]:
            bump_type = result["bump_type"]
            new_version = get_version_bump_example(current_version, bump_type)

            status = "✅ VALID"
            if bump_type == "major":
                status += " (MAJOR RELEASE)"
            elif bump_type == "minor":
                status += " (MINOR RELEASE)"
            elif bump_type == "patch":
                status += " (PATCH RELEASE)"
            else:
                status += " (NO RELEASE)"

            print(f"Status: {status}")
            print(f"Type: {result['type']}")
            if result["scope"]:
                print(f"Scope: {result['scope']}")
            print(f"Description: {result['description']}")
            print(f"Breaking Change: {'Yes' if result['breaking'] else 'No'}")
            print(f"Version: {current_version} → {new_version}")
        else:
            print(f"Status: ❌ INVALID")
            print(f"Error: {result['error']}")
            print(f"Version: {current_version} (no change)")

        print_usage_guide()
    else:
        # Run all test cases
        results = test_commit_messages()
        print_results(results)
        print_usage_guide()


if __name__ == "__main__":
    main()
