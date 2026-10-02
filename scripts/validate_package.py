#!/usr/bin/env python3
"""Check that a skill package is complete enough to distribute."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_REFERENCE_RE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)")
_LINK_START_RE = re.compile(r"!?\[(?:\\.|[^\]\\])*\]\(")
_SCAFFOLD_RE = re.compile(
    r"(?i)(?:\b(?:TODO|TBD|FIXME|WIP)\b\s*:|\b(?:INSERT|REPLACE|FILL\s+IN)\s+"
    r"(?:THIS|HERE|ME|VALUE|CONTENT)\b|\bYOUR\s+(?:SKILL\s+)?(?:NAME|DESCRIPTION)\b|"
    r"\[(?:TODO|TBD|FIXME|YOUR\s+(?:SKILL\s+)?(?:NAME|DESCRIPTION))[^\]]*\])"
)
_TEMPLATE_RE = re.compile(r"(?:\$\{[^}]+\}|\{\{.*?\}\}|\{[^{}]+\}|<[A-Za-z_][^<>]*>)")

def _frontmatter(text: str) -> tuple[dict | None, str | None, str]:
    """Return frontmatter mapping, parse error, and the remaining Markdown body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing YAML frontmatter", ""
    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        return None, "YAML frontmatter has no closing '---'", ""
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}", ""
    if not isinstance(data, dict):
        return None, "YAML frontmatter must be a mapping", ""
    return data, None, "\n".join(lines[end + 1 :])


def _valid_name(value: object) -> bool:
    return (isinstance(value, str) and 1 <= len(value) <= 64
            and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) is not None)


def _blank_fenced_and_inline_code(text: str) -> str:
    """Remove fenced and inline code while retaining line numbers and line layout."""
    lines = text.splitlines()
    fence_char = None
    fence_length = 0
    for index, line in enumerate(lines):
        match = _FENCE_RE.match(line)
        if fence_char is not None:
            if (
                match
                and match.group(1)[0] == fence_char
                and len(match.group(1)) >= fence_length
                and not match.group(2).strip()
            ):
                fence_char = None
                fence_length = 0
            lines[index] = ""
        elif match:
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
            lines[index] = ""

    inline_code = re.compile(r"(?<!`)(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)")
    return "\n".join(inline_code.sub("", line) for line in lines)


def _inline_destinations(line: str):
    """Yield inline-link destinations from one non-code Markdown line."""
    for match in _LINK_START_RE.finditer(line):
        index = match.end()
        while index < len(line) and line[index].isspace():
            index += 1
        if index >= len(line):
            continue
        if line[index] == "<":
            close = line.find(">", index + 1)
            if close < 0:
                continue
            yield line[index + 1 : close]
            continue

        start = index
        depth = 0
        escaped = False
        while index < len(line):
            char = line[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(" and depth == 0:
                depth += 1
            elif char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            elif char.isspace() and depth == 0:
                break
            index += 1
        destination = line[start:index].rstrip(")")
        if destination:
            yield destination


def _markdown_destinations(text: str):
    visible = _blank_fenced_and_inline_code(text)
    for line_number, line in enumerate(visible.splitlines(), start=1):
        definition = _REFERENCE_RE.match(line)
        if definition:
            target = definition.group(1)
            if target.startswith("<") and target.endswith(">"):  # Markdown's angle-wrapped destination.
                target = target[1:-1]
            yield line_number, target
        yield from ((line_number, target) for target in _inline_destinations(line))


def _is_template_target(target: str) -> bool:
    return bool(_TEMPLATE_RE.search(target))


def _local_target(root: Path, source: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or _is_template_target(target):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith("//"):
        return None
    if not parsed.path:  # Fragment-only links point back to the current document.
        return source
    local_path_text = unquote(parsed.path.replace("\\ ", " "))
    local_path = Path(local_path_text)
    if local_path_text.startswith(("/", "\\")):
        candidate = root / local_path_text.lstrip("/\\")
    else:
        candidate = source.parent / local_path
    try:
        resolved_root = root.resolve()
        resolved_candidate = candidate.resolve()
        if not resolved_candidate.is_relative_to(resolved_root):
            return candidate  # It will be reported as an invalid package-local target.
    except OSError:
        return candidate
    return candidate


def validate_package(root: Path | str) -> list[str]:
    """Return distribution defects for a package directory; an empty list means valid."""
    root = Path(root)
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    agent_path = root / "agents" / "openai.yaml"
    if not skill_path.is_file():
        return ["missing SKILL.md"]
    if not agent_path.is_file():
        errors.append("missing agents/openai.yaml")

    try:
        skill_text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"SKILL.md cannot be read as UTF-8: {exc}"]

    metadata, frontmatter_error, body = _frontmatter(skill_text)
    if frontmatter_error:
        errors.append(f"SKILL.md: {frontmatter_error}")
    elif metadata is not None:
        name = metadata.get("name")
        description = metadata.get("description")
        if not _valid_name(name):
            errors.append("SKILL.md: name must be 1-64 lowercase alphanumeric groups separated by single hyphens")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append("SKILL.md: description must be a non-empty string of at most 1024 characters")

    visible_skill = _blank_fenced_and_inline_code(skill_text)
    for line_number, line in enumerate(visible_skill.splitlines(), start=1):
        marker = _SCAFFOLD_RE.search(line)
        if marker:
            errors.append(f"SKILL.md:{line_number}: unfinished scaffold marker {marker.group(0)!r}")

    agent_text = ""
    if agent_path.is_file():
        try:
            agent_text = agent_path.read_text(encoding="utf-8")
            agent_data = yaml.safe_load(agent_text)
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"agents/openai.yaml: cannot read valid YAML: {exc}")
            agent_data = None
        interface = agent_data.get("interface") if isinstance(agent_data, dict) else None
        prompt = interface.get("default_prompt") if isinstance(interface, dict) else None
        for field in ("display_name", "short_description", "default_prompt"):
            value = interface.get(field) if isinstance(interface, dict) else None
            if not isinstance(value, str) or not value.strip():
                errors.append(f"agents/openai.yaml: interface.{field} must be a non-empty string")
        if isinstance(prompt, str) and metadata is not None:
            name = metadata.get("name")
            if isinstance(name, str) and f"${name}" not in prompt:
                errors.append(f"agents/openai.yaml: default_prompt must invoke ${name}")

    ignored_directories = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    import os

    for current, directories, files in os.walk(root):
        directories[:] = [name for name in directories if name not in ignored_directories]
        current_path = Path(current)
        for filename in files:
            if not filename.lower().endswith(".md"):
                continue
            source = current_path / filename
            try:
                markdown = source.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{source.relative_to(root).as_posix()}: cannot read Markdown as UTF-8: {exc}")
                continue
            for line_number, target in _markdown_destinations(markdown):
                candidate = _local_target(root, source, target)
                if candidate is None:
                    continue
                try:
                    exists = candidate.resolve().is_relative_to(root.resolve()) and candidate.exists()
                except OSError:
                    exists = False
                if not exists:
                    relative = source.relative_to(root).as_posix()
                    errors.append(f"{relative}:{line_number}: missing local Markdown target {target!r}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1],
                        help="package directory (default: repository root)")
    args = parser.parse_args(argv)
    errors = validate_package(args.root)
    if errors:
        print("Package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Package validation passed: {args.root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
