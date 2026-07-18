#!/usr/bin/env python3
"""Allocate, import, and validate project meeting PNG assets."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from meeting_context import build_context


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
EXPECTED_RE = re.compile(r"^\.\./figures/(\d{4})_fig(\d+)\.png$")


def is_png(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE
    except OSError:
        return False


def next_path(repo: Path, requested_date: str | None) -> tuple[str, Path]:
    context = build_context(repo, requested_date, datetime.now(ZoneInfo("Asia/Seoul")))
    return context.target_mmdd, repo.resolve() / context.next_figure


def import_figure(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"source does not exist: {source}")
    if source.suffix.lower() != ".png" or not is_png(source):
        raise SystemExit(f"source is not a valid PNG: {source}")

    mmdd, automatic = next_path(repo, args.date)
    destination = (
        repo / "docs" / "figures" / f"{mmdd}_fig{args.number}.png"
        if args.number is not None
        else automatic
    )
    if destination.exists():
        raise SystemExit(f"refusing to overwrite: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    relative = destination.relative_to(repo)
    print(f"saved: {relative}")
    print(f"![{args.alt}](../figures/{destination.name})")
    return 0


def validate_meeting(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    meeting = args.meeting if args.meeting.is_absolute() else repo / args.meeting
    if not meeting.is_file():
        raise SystemExit(f"meeting file does not exist: {meeting}")
    name_match = re.fullmatch(r"(\d{4})_meeting\.md", meeting.name)
    if not name_match:
        raise SystemExit("meeting filename must be mmdd_meeting.md")
    mmdd = name_match.group(1)
    text = meeting.read_text(encoding="utf-8")
    errors: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("!") and not IMAGE_RE.search(stripped):
            errors.append(f"line {line_number}: malformed image syntax: {stripped}")

    seen: set[str] = set()
    for _, link in IMAGE_RE.findall(text):
        expected = EXPECTED_RE.fullmatch(link)
        if not expected:
            errors.append(f"unexpected image path: {link}")
            continue
        if expected.group(1) != mmdd:
            errors.append(f"image prefix does not match meeting date: {link}")
        if link in seen:
            errors.append(f"duplicate image link: {link}")
        seen.add(link)
        path = (meeting.parent / link).resolve()
        if not path.is_relative_to((repo / "docs" / "figures").resolve()):
            errors.append(f"image escapes docs/figures: {link}")
        elif not path.is_file():
            errors.append(f"missing image: {link}")
        elif not is_png(path):
            errors.append(f"not a valid PNG: {link}")

    if "!image.png" in text:
        errors.append("unresolved !image.png placeholder")
    if errors:
        print("validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"validation passed: {meeting.relative_to(repo)} ({len(seen)} figure links)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    next_parser = subparsers.add_parser("next", help="Print the next meeting figure path")
    next_parser.add_argument("--repo", type=Path, default=Path.cwd())
    next_parser.add_argument("--date", help="Meeting date: YYYY-MM-DD or MMDD")

    import_parser = subparsers.add_parser("import", help="Copy a PNG into docs/figures")
    import_parser.add_argument("--repo", type=Path, default=Path.cwd())
    import_parser.add_argument("--date", help="Meeting date: YYYY-MM-DD or MMDD")
    import_parser.add_argument("--source", type=Path, required=True)
    import_parser.add_argument("--number", type=int)
    import_parser.add_argument("--alt", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a meeting's PNG links")
    validate_parser.add_argument("--repo", type=Path, default=Path.cwd())
    validate_parser.add_argument("--meeting", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "next":
        _, path = next_path(args.repo, args.date)
        print(path.relative_to(args.repo.resolve()))
        return 0
    if args.command == "import":
        if args.number is not None and args.number < 1:
            raise SystemExit("--number must be positive")
        return import_figure(args)
    return validate_meeting(args)


if __name__ == "__main__":
    raise SystemExit(main())
