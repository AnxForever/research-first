#!/usr/bin/env python3
"""A tiny, offline reading shelf used as a forward-evaluation fixture."""

import argparse
import json
from pathlib import Path
from urllib.parse import quote

DEFAULT_DATA = Path(__file__).with_name("shelf.json")


def load_items(path):
    """Load the shelf's JSON array without changing its source file."""
    with path.open("r", encoding="utf-8-sig") as handle:
        items = json.load(handle)
    if not isinstance(items, list):
        raise ValueError("shelf data must be a JSON array")
    return items


def render_markdown_link(title, url):
    """Render one Markdown link; used by the existing Markdown list view."""
    safe_title = str(title).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
    safe_url = quote(str(url), safe=":/?#@!$&'*+,;=%-._~")
    return "[{}]({})".format(safe_title, safe_url)


def render_list(items, output_format):
    """Print every shelf row in stored order."""
    for index, item in enumerate(items, start=1):
        marker = "x" if item.get("selected") else " "
        title = str(item.get("title", ""))
        url = str(item.get("url", ""))
        note = " ".join(str(item.get("note", "")).splitlines())
        if output_format == "markdown":
            label = render_markdown_link(title, url)
            suffix = " — {}".format(note) if note else ""
            print("- [{}] {}{}".format(marker, label, suffix))
        else:
            print("{}. [{}] {} — {}".format(index, marker, title, url))
            if note:
                print("   note: {}".format(note))


def build_parser():
    parser = argparse.ArgumentParser(description="Offline reading shelf")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="path to shelf JSON")
    commands = parser.add_subparsers(dest="command", required=True)
    list_parser = commands.add_parser("list", help="list saved reading items")
    list_parser.add_argument(
        "--format", choices=("text", "markdown"), default="text", help="list output format"
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    items = load_items(args.data)
    if args.command == "list":
        render_list(items, args.format)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
