#!/usr/bin/env python3
"""Resolve project meeting dates and paths using Korea Standard Time."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")
MEETING_RE = re.compile(r"^(\d{2})(\d{2})_meeting\.md$")
FIGURE_RE = re.compile(r"^(\d{4})_fig(\d+)\.png$")


@dataclass(frozen=True)
class MeetingContext:
    as_of_kst: str
    target_date: str
    target_mmdd: str
    target_meeting: str
    target_exists: bool
    previous_date: str | None
    previous_meeting: str | None
    recent_meetings: list[str]
    next_figure: str


def parse_date(value: str | None, today: date) -> date:
    if value is None:
        monday = today - timedelta(days=today.weekday())
        return monday + timedelta(days=3)
    if re.fullmatch(r"\d{4}", value):
        return date(today.year, int(value[:2]), int(value[2:]))
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "date must be YYYY-MM-DD or MMDD"
        ) from exc


def infer_named_date(mmdd: str, target: date) -> date:
    month, day = int(mmdd[:2]), int(mmdd[2:])
    candidate = date(target.year, month, day)
    if candidate >= target:
        candidate = date(target.year - 1, month, day)
    return candidate


def build_context(repo: Path, requested_date: str | None, now: datetime) -> MeetingContext:
    repo = repo.resolve()
    target = parse_date(requested_date, now.date())
    mmdd = target.strftime("%m%d")
    meetings_dir = repo / "docs" / "meetings"
    figures_dir = repo / "docs" / "figures"
    target_path = meetings_dir / f"{mmdd}_meeting.md"

    dated_meetings: list[tuple[date, Path]] = []
    for path in meetings_dir.glob("*_meeting.md"):
        match = MEETING_RE.match(path.name)
        if match and path != target_path:
            named_mmdd = "".join(match.groups())
            dated_meetings.append((infer_named_date(named_mmdd, target), path))
    dated_meetings.sort(key=lambda item: item[0], reverse=True)

    previous_date, previous_path = (dated_meetings[0] if dated_meetings else (None, None))
    recent = [str(path.relative_to(repo)) for _, path in dated_meetings[:3]]

    numbers: list[int] = []
    for path in figures_dir.glob(f"{mmdd}_fig*.png"):
        match = FIGURE_RE.match(path.name)
        if match and match.group(1) == mmdd:
            numbers.append(int(match.group(2)))
    next_number = max(numbers, default=0) + 1

    return MeetingContext(
        as_of_kst=now.astimezone(KST).isoformat(timespec="seconds"),
        target_date=target.isoformat(),
        target_mmdd=mmdd,
        target_meeting=str(target_path.relative_to(repo)),
        target_exists=target_path.exists(),
        previous_date=previous_date.isoformat() if previous_date else None,
        previous_meeting=str(previous_path.relative_to(repo)) if previous_path else None,
        recent_meetings=recent,
        next_figure=str((figures_dir / f"{mmdd}_fig{next_number}.png").relative_to(repo)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--date", help="Explicit meeting date: YYYY-MM-DD or MMDD")
    parser.add_argument("--json", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    context = build_context(args.repo, args.date, datetime.now(KST))
    payload = asdict(context)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
