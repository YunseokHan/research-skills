#!/usr/bin/env python3
"""Create missing sustainable-research-repository scaffolding without overwriting files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CORE_DIRS = (
    "configs",
    "tests",
    "scripts/archive",
    "docs/lessons/history",
    "docs/lessons/legacy",
    "docs/meetings",
    "docs/surveys",
    "docs/figures",
)
CORE_TEMPLATES = {
    ".env.example": ".env.example",
    ".gitignore": ".gitignore",
    "AGENTS.md": "AGENTS.md",
    "CLAUDE.md": "CLAUDE.md",
    "docs/METHOD.md": "docs/METHOD.md",
    "docs/ROADMAP.md": "docs/ROADMAP.md",
    "docs/LESSON.md": "docs/LESSON.md",
    "docs/CODE_STRUCTURE.md": "docs/CODE_STRUCTURE.md",
}
WRITING_TEMPLATES = {
    "docs/writing/FACTS.md": "docs/writing/FACTS.md",
    "docs/writing/STATUS.md": "docs/writing/STATUS.md",
}


def valid_package(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise argparse.ArgumentTypeError("package name must be a valid import identifier")
    return value


def render(text: str, project_name: str, package_name: str) -> str:
    return text.replace("{{PROJECT_NAME}}", project_name).replace("{{PACKAGE_NAME}}", package_name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--package-name", required=True, type=valid_package)
    parser.add_argument("--with-writing", action="store_true", help="Create optional writing facts/status structure")
    parser.add_argument("--with-runner", action="store_true", help="Install the Python-oriented scripts/run.sh template")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    if not repo.is_dir():
        parser.error(f"repository path is not a directory: {repo}")
    skill_dir = Path(__file__).resolve().parent.parent
    templates = skill_dir / "assets" / "templates"
    if not templates.is_dir():
        parser.error(f"template directory is missing: {templates}")

    dirs = list(CORE_DIRS)
    mapping = dict(CORE_TEMPLATES)
    if args.with_writing:
        dirs.extend(("docs/writing/sections", "docs/writing/tables", "docs/writing/figs", "docs/writing/venue"))
        mapping.update(WRITING_TEMPLATES)
    if args.with_runner:
        mapping["scripts/run.sh"] = "scripts/run.sh"

    created = 0
    skipped = 0
    for rel in dirs:
        target = repo / rel
        if target.is_dir():
            continue
        print(f"CREATE DIR  {rel}")
        if not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)
        created += 1

    for target_rel, template_rel in mapping.items():
        target = repo / target_rel
        source = templates / template_rel
        if target.exists():
            print(f"SKIP FILE   {target_rel} (exists)")
            skipped += 1
            continue
        if not source.is_file():
            print(f"ERROR       missing template {template_rel}", file=sys.stderr)
            return 2
        print(f"CREATE FILE {target_rel}")
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(source.read_text(), args.project_name, args.package_name))
            if target_rel == "scripts/run.sh":
                target.chmod(0o755)
        created += 1

    mode = "DRY RUN" if args.dry_run else "DONE"
    print(f"{mode}: {created} creation(s), {skipped} existing file(s) preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
