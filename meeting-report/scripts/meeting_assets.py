#!/usr/bin/env python3
"""Allocate, import, and validate project meeting PNG assets."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from meeting_context import build_context


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
EXPECTED_RE = re.compile(r"^\.\./figures/(\d{4})_fig(\d+)\.png$")
HEADING_RE = re.compile(r"^(#{1,3})\s+(\d+(?:\.\d+)*\.)\s+(.+?)\s*$")
MEANING_RE = re.compile(r"^\*\*의미\.\*\*\s+(\S.*)$")
MEANING_EXEMPT_HEADINGS = {
    "Summary",
    "요약",
    "TODO",
    "To do",
    "References",
    "참고문헌",
}


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


def _selection_with_ellipsis(heading: str) -> str:
    """Build a stable Notion selection anchor for a numbered heading block."""
    if len(heading) <= 28:
        return heading
    return f"{heading[:14]}...{heading[-14:]}"


def parse_meaning_annotations(text: str) -> tuple[list[dict[str, object]], list[str]]:
    """Extract local meaning paragraphs and validate one per content-bearing unit."""
    headings: list[dict[str, object]] = []
    stack: list[int] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = HEADING_RE.fullmatch(line.strip())
        if match:
            level = len(match.group(1))
            while stack and int(headings[stack[-1]]["level"]) >= level:
                stack.pop()
            headings.append(
                {
                    "raw": line.strip(),
                    "level": level,
                    "title": match.group(3).strip(),
                    "line": line_number,
                    "direct_lines": [],
                }
            )
            stack.append(len(headings) - 1)
            continue
        if stack:
            direct_lines = headings[stack[-1]]["direct_lines"]
            assert isinstance(direct_lines, list)
            direct_lines.append((line_number, line))

    annotations: list[dict[str, object]] = []
    errors: list[str] = []
    for heading in headings:
        title = str(heading["title"])
        direct_lines = list(heading["direct_lines"])
        meaningful_lines = [
            (line_number, line)
            for line_number, line in direct_lines
            if line.strip()
            and line.strip() not in {"---", "***", "___"}
            and not line.strip().startswith("<!--")
        ]
        content_lines = [
            (line_number, line)
            for line_number, line in meaningful_lines
            if not MEANING_RE.fullmatch(line.strip())
        ]
        if title in MEANING_EXEMPT_HEADINGS or not content_lines:
            continue

        meaning_lines = [
            (line_number, line, MEANING_RE.fullmatch(line.strip()))
            for line_number, line in meaningful_lines
            if MEANING_RE.fullmatch(line.strip())
        ]
        raw_heading = str(heading["raw"])
        if not meaning_lines:
            errors.append(
                f"line {heading['line']}: missing final '**의미.**' paragraph for {raw_heading}"
            )
            continue
        if len(meaning_lines) > 1:
            errors.append(
                f"line {heading['line']}: multiple '**의미.**' paragraphs for {raw_heading}"
            )
            continue

        line_number, _, match = meaning_lines[0]
        assert match is not None
        if meaningful_lines[-1][0] != line_number:
            errors.append(
                f"line {line_number}: '**의미.**' must be the final direct paragraph for {raw_heading}"
            )
        annotations.append(
            {
                "heading": raw_heading,
                "selection_with_ellipsis": _selection_with_ellipsis(raw_heading),
                "comment": match.group(1).strip(),
                "line": line_number,
            }
        )
    return annotations, errors


def build_notion_payload(text: str) -> tuple[dict[str, object], list[str]]:
    """Remove local explanations and convert blockquotes to Notion callouts."""
    annotations, errors = parse_meaning_annotations(text)
    if errors:
        return {}, errors
    meaning_lines = {int(annotation["line"]) for annotation in annotations}
    source_lines = text.splitlines()
    notion_lines: list[str] = []
    callout_count = 0
    index = 0
    while index < len(source_lines):
        line_number = index + 1
        line = source_lines[index]
        if line_number in meaning_lines:
            index += 1
            continue
        if line.lstrip().startswith(">"):
            callout_lines: list[str] = []
            while index < len(source_lines) and source_lines[index].lstrip().startswith(">"):
                stripped = source_lines[index].lstrip()[1:]
                callout_lines.append(stripped[1:] if stripped.startswith(" ") else stripped)
                index += 1
            notion_lines.append('<callout icon="📌" color="gray_background">')
            notion_lines.extend(callout_lines)
            notion_lines.append("</callout>")
            callout_count += 1
            continue
        notion_lines.append(line)
        index += 1
    return {
        "body": "\n".join(notion_lines).rstrip() + "\n",
        "comments": annotations,
        "callout_count": callout_count,
    }, []


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
    annotations, meaning_errors = parse_meaning_annotations(text)
    errors.extend(meaning_errors)
    if errors:
        print("validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"validation passed: {meeting.relative_to(repo)} "
        f"({len(seen)} figure links, {len(annotations)} meaning comments)"
    )
    return 0


def emit_comments(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    meeting = args.meeting if args.meeting.is_absolute() else repo / args.meeting
    if not meeting.is_file():
        raise SystemExit(f"meeting file does not exist: {meeting}")
    annotations, errors = parse_meaning_annotations(meeting.read_text(encoding="utf-8"))
    if errors:
        print("comment extraction failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(json.dumps(annotations, ensure_ascii=False, indent=2))
    return 0


def emit_notion_payload(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    meeting = args.meeting if args.meeting.is_absolute() else repo / args.meeting
    if not meeting.is_file():
        raise SystemExit(f"meeting file does not exist: {meeting}")
    payload, errors = build_notion_payload(meeting.read_text(encoding="utf-8"))
    if errors:
        print("Notion payload generation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
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

    comments_parser = subparsers.add_parser(
        "comments", help="Emit Notion comment mappings from local meaning paragraphs"
    )
    comments_parser.add_argument("--repo", type=Path, default=Path.cwd())
    comments_parser.add_argument("--meeting", type=Path, required=True)

    notion_parser = subparsers.add_parser(
        "notion", help="Emit a callout body and heading-comment mappings for Notion"
    )
    notion_parser.add_argument("--repo", type=Path, default=Path.cwd())
    notion_parser.add_argument("--meeting", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "next":
        _, path = next_path(args.repo, args.date)
        print(path.relative_to(args.repo.resolve()))
        return 0
    if args.command == "import":
        if args.number is not None and args.number < 1:
            raise SystemExit("--number must be positive")
        return import_figure(args)
    if args.command == "comments":
        return emit_comments(args)
    if args.command == "notion":
        return emit_notion_payload(args)
    return validate_meeting(args)


if __name__ == "__main__":
    raise SystemExit(main())
