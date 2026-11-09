#!/usr/bin/env python3
"""Validate a WorkBuddy skill package before upload."""

from __future__ import annotations

import argparse
import os
from pathlib import Path, PureWindowsPath
import re
import sys
from urllib.parse import unquote, urlsplit

try:  # Direct script execution and tests add scripts/ to sys.path.
    from validate_package import (
        _blank_fenced_and_inline_code,
        _frontmatter,
        _local_target,
        _markdown_destinations,
        _valid_name,
    )
except ImportError:  # Also support ``python -m scripts.validate_workbuddy``.
    from .validate_package import (
        _blank_fenced_and_inline_code,
        _frontmatter,
        _local_target,
        _markdown_destinations,
        _valid_name,
    )


_RESOURCE_RE = re.compile(
    r"(?<![\w/@])@(?P<kind>references|templates)/"
    r"(?P<path>[^\s<>()\[\]{}\"'`]+)"
)
_TRAILING_PUNCTUATION = ".,;:!?"
_REQUIRED_FIELDS = ("description", "description_zh", "description_en", "version", "author")
_IGNORED_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def _is_within(path: Path, directory: Path) -> bool:
    try:
        return path.resolve().is_relative_to(directory.resolve())
    except (OSError, RuntimeError, ValueError):
        return False


def _resource_target(root: Path, kind: str, raw_path: str) -> tuple[Path | None, str | None]:
    """Resolve a WorkBuddy resource path, rejecting traversal and external targets."""
    path = unquote(raw_path.rstrip(_TRAILING_PUNCTUATION).replace("\\", "/"))
    parsed = urlsplit(path)
    suffix = parsed.path
    windows_path = PureWindowsPath(suffix)
    if not suffix or suffix.startswith("/") or windows_path.is_absolute() or windows_path.drive:
        return None, f"@{kind}/{raw_path}: resource path must stay under {kind}/"

    base = root / kind
    candidate = base / suffix
    try:
        resolved = candidate.resolve()
        if not resolved.is_relative_to(base.resolve()):
            return None, f"@{kind}/{raw_path}: resource path escapes {kind}/"
        if not resolved.is_relative_to(root.resolve()):
            return None, f"@{kind}/{raw_path}: resource path escapes the package"
    except (OSError, RuntimeError, ValueError):
        return None, f"@{kind}/{raw_path}: resource path cannot be resolved"
    if not resolved.is_file():
        return None, f"@{kind}/{raw_path}: missing package resource"
    return resolved, None


def _markdown_resource_link(root: Path, source: Path, target: str) -> str | None:
    """Return references/templates namespace for a Markdown link into that tree."""
    candidate = _local_target(root, source, target)
    if candidate is None:
        return None
    for kind in ("references", "templates"):
        if _is_within(candidate, root / kind):
            return kind
    return None


def validate_workbuddy(root: Path | str) -> list[str]:
    """Return WorkBuddy package defects; an empty list means the package is valid.

    In addition to WorkBuddy's documented frontmatter and resource references,
    this checker treats a present ``name`` matching the package directory and
    normalizing template references to ``@templates/`` as local build invariants.
    WorkBuddy itself allows ``name`` to be omitted; its guide specifies the
    ``templates/`` directory without prescribing a template-reference syntax.
    """
    root = Path(root).resolve()
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return ["missing SKILL.md"]

    try:
        skill_text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"SKILL.md cannot be read as UTF-8: {exc}"]

    metadata, frontmatter_error, _body = _frontmatter(skill_text)
    if frontmatter_error:
        errors.append(f"SKILL.md: {frontmatter_error}")
    elif metadata is not None:
        for field in _REQUIRED_FIELDS:
            value = metadata.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"SKILL.md: {field} must be a non-empty string")

        name = metadata.get("name")
        if "name" in metadata:
            if not _valid_name(name):
                errors.append("SKILL.md: name must be 1-64 lowercase alphanumeric groups separated by single hyphens")
            elif name != root.name:
                errors.append(f"SKILL.md: name {name!r} must match package directory {root.name!r}")

    # Check every shipped Markdown file for readable text, resource directives,
    # and intact local links. Directives in code examples are not active refs.
    for current, directories, files in os.walk(root):
        directories[:] = [name for name in directories if name not in _IGNORED_DIRECTORIES]
        current_path = Path(current)
        for filename in files:
            if not filename.lower().endswith(".md"):
                continue
            source = current_path / filename
            try:
                markdown = source.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                relative = source.relative_to(root).as_posix()
                errors.append(f"{relative}: cannot be read as UTF-8: {exc}")
                continue

            visible = _blank_fenced_and_inline_code(markdown)
            relative = source.relative_to(root).as_posix()
            for line_number, line in enumerate(visible.splitlines(), start=1):
                for match in _RESOURCE_RE.finditer(line):
                    kind = match.group("kind")
                    _resource, error = _resource_target(root, kind, match.group("path"))
                    if error:
                        errors.append(f"{relative}:{line_number}: {error}")

            for line_number, target in _markdown_destinations(markdown):
                kind = _markdown_resource_link(root, source, target)
                if kind:
                    errors.append(
                        f"{relative}:{line_number}: use @{kind}/... instead of a Markdown link to {kind}/"
                    )
                candidate = _local_target(root, source, target)
                if candidate is None:
                    continue
                try:
                    exists = candidate.resolve().is_relative_to(root) and candidate.exists()
                except (OSError, RuntimeError, ValueError):
                    exists = False
                if not exists:
                    errors.append(f"{relative}:{line_number}: missing or out-of-package Markdown target {target!r}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="WorkBuddy package directory containing SKILL.md")
    args = parser.parse_args(argv)
    errors = validate_workbuddy(args.root)
    if errors:
        print("WorkBuddy package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"WorkBuddy package validation passed: {Path(args.root).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
