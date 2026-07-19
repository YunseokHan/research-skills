#!/usr/bin/env python3
"""Resolve non-secret Notion meeting destination metadata."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--parent", help="Explicit Notion parent page/database URL or ID")
    parser.add_argument("--project", help="Explicit project display name")
    parser.add_argument("--database-title", help="Explicit project meeting database title")
    args = parser.parse_args()

    repo = args.repo.resolve()
    parent = (
        args.parent
        or os.environ.get("MEETING_NOTION_PARENT_URL")
        or os.environ.get("NOTION_MEETING_PARENT_URL")
    )
    project = args.project or os.environ.get("MEETING_NOTION_PROJECT") or repo.name
    database_title = (
        args.database_title
        or os.environ.get("MEETING_NOTION_DATABASE_TITLE")
        or project
    )

    payload = {
        "parent": parent,
        "project": project,
        "database_title": database_title,
        "source": "explicit" if args.parent else "environment" if parent else "missing",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if parent else 2


if __name__ == "__main__":
    raise SystemExit(main())
