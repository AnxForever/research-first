#!/usr/bin/env python3
"""Build a self-contained WorkBuddy ZIP from the canonical skill sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import tempfile
from urllib.parse import urlsplit
import zipfile

import yaml

from validate_package import _frontmatter
from validate_workbuddy import validate_workbuddy


DOCS_URL = "https://open.workbuddy.cn/docs/skill"
PUBLIC_REPOSITORY = "https://github.com/AnxForever/research-first"
_LINK = re.compile(r"\[([^\]\n]+)\]\(([^\s)]+)\)")
_RUNTIME_NOTE = (
    "Resolve @references/ and @templates/ paths relative to this installed skill's "
    "directory. Read them only when the stated condition applies. Respond in the "
    "user's language. The core workflow needs no Python packages or API key.\n"
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def _rewrite_links(text: str, source: str, destinations: dict[str, str], ref: str) -> str:
    def replace(match: re.Match) -> str:
        label, target = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)
        source_target = posixpath.normpath(posixpath.join(posixpath.dirname(source), parsed.path))
        if source_target in destinations:
            destination = destinations[source_target]
            if destination.startswith(("references/", "templates/")):
                return f"{label} (@{destination})"
            output_source = destinations[source]
            relative = posixpath.relpath(destination, posixpath.dirname(output_source) or ".")
            return f"[{label}]({relative})"
        if source_target.startswith("evals/"):
            return f"[{label}]({PUBLIC_REPOSITORY}/blob/{ref}/{source_target})"
        return match.group(0)

    return _LINK.sub(replace, text)


def build_workbuddy(root: Path, output_dir: Path, metadata_path: Path | None = None) -> tuple[Path, Path]:
    root = root.resolve()
    metadata_path = metadata_path or root / "packaging" / "workbuddy.yaml"
    metadata = yaml.safe_load(_text(metadata_path))
    if not isinstance(metadata, dict):
        raise ValueError("WorkBuddy metadata must be a YAML mapping")
    name, version = metadata.get("name"), metadata.get("version")
    # These values become directory and archive names. Reject before any writes.
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("name must be lowercase alphanumeric groups separated by hyphens")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("version must use major.minor.patch for this release builder")

    source_metadata, error, body = _frontmatter(_text(root / "SKILL.md"))
    if error or not source_metadata or source_metadata.get("name") != name:
        raise ValueError(f"canonical skill identity does not match metadata: {error or name}")

    destinations = {"SKILL.md": "SKILL.md", "LICENSE": "LICENSE"}
    for path in sorted((root / "references").glob("*.md")):
        destinations[path.relative_to(root).as_posix()] = path.relative_to(root).as_posix()
    for path in sorted((root / "assets").glob("*.md")):
        destinations[path.relative_to(root).as_posix()] = f"templates/{path.name}"
    for source in ("scripts/jev_check.py", "scripts/requirements-jev.txt"):
        destinations[source] = source
    destinations["evals/jev-cases.json"] = "references/jev-cases.json"

    commit = _git(root, "rev-parse", "HEAD")
    public_ref = commit or "main"
    files: dict[str, bytes] = {}
    inputs: dict[str, str] = {}
    for source, destination in destinations.items():
        path = root / source
        inputs[source] = _sha256(path.read_bytes())
        text = _text(path)
        if source == "SKILL.md":
            text = "---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=100) + "---\n" + body
            text = text.replace("# Research First\n", "# Research First\n\n" + _RUNTIME_NOTE, 1)
        if path.suffix == ".md":
            text = _rewrite_links(text, source, destinations, public_ref)
        if source == "references/jev-checkpoints.md":
            text = text.replace(
                "## Use the Optional Adapter\n",
                "## Use the Optional Adapter\n\n"
                "Run the commands below from this skill's installed directory, resolved "
                "from the loaded SKILL.md. Pass an absolute path to the evidence card; "
                "do not assume the user's project contains these scripts.\n",
                1,
            )
        files[destination] = text.rstrip("\n").encode("utf-8") + b"\n"
    inputs[metadata_path.relative_to(root).as_posix() if metadata_path.is_relative_to(root) else "build-metadata"] = _sha256(metadata_path.read_bytes())
    inputs["scripts/build_workbuddy.py"] = _sha256(Path(__file__).read_bytes())
    inputs["scripts/validate_workbuddy.py"] = _sha256((Path(__file__).parent / "validate_workbuddy.py").read_bytes())
    inputs["scripts/validate_package.py"] = _sha256((Path(__file__).parent / "validate_package.py").read_bytes())

    # Validate a real on-disk package, then validate the bytes read back from its ZIP.
    with tempfile.TemporaryDirectory(prefix="research-first-workbuddy-") as temporary:
        stage = Path(temporary) / name
        for destination, data in files.items():
            target = stage / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        errors = validate_workbuddy(stage)
        if errors:
            raise ValueError("WorkBuddy package validation failed:\n" + "\n".join(errors))
        archive_stage = Path(temporary) / "package.zip"
        with zipfile.ZipFile(archive_stage, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for destination, data in sorted(files.items()):
                info = zipfile.ZipInfo(str(PurePosixPath(name, destination)), date_time=(2026, 1, 1, 0, 0, 0))
                info.create_system = 3  # Keep ZIP headers independent of the host OS.
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        unpacked = Path(temporary) / "unpacked"
        with zipfile.ZipFile(archive_stage) as archive:
            archive.extractall(unpacked)  # Entries are generated above from our fixed sources.
        errors = validate_workbuddy(unpacked / name)
        if errors:
            raise ValueError("ZIP round-trip validation failed:\n" + "\n".join(errors))
        archive_data = archive_stage.read_bytes()

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{name}-workbuddy-{version}.zip"
    manifest_path = archive_path.with_suffix(".manifest.json")
    worktree_status = _git(root, "status", "--porcelain")
    manifest = {
        "platform": "WorkBuddy",
        "version": version,
        "specification": DOCS_URL,
        "source_commit": commit,
        "source_worktree_dirty": None if worktree_status is None else bool(worktree_status),
        "archive": archive_path.name,
        "archive_sha256": _sha256(archive_data),
        "file_count": len(files),
        "checks": {"package_structure": "passed", "zip_round_trip": "passed", "workbuddy_runtime": "unverified"},
        "source_inputs_sha256": inputs,
        "files_sha256": {path: _sha256(data) for path, data in sorted(files.items())},
    }
    archive_path.write_bytes(archive_data)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return archive_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--output-dir", type=Path, default=root / "dist" / "workbuddy")
    args = parser.parse_args()
    try:
        archive, manifest = build_workbuddy(root, args.output_dir.resolve())
    except (OSError, ValueError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")
    print(f"WorkBuddy ZIP: {archive}")
    print(f"Manifest: {manifest}")
    print("Local structure and ZIP checks passed; WorkBuddy runtime acceptance is unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
