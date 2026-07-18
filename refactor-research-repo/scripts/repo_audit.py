#!/usr/bin/env python3
"""Inventory and validate a sustainable research-repository layout."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".tox",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "cache",
    "logs",
    "outputs",
    "checkpoints",
}
SOURCE_SUFFIXES = {".py", ".rs", ".go", ".c", ".cc", ".cpp", ".cu", ".h", ".hpp", ".java", ".kt", ".jl"}
GENERATED_PREFIXES = ("cache/", "logs/", "outputs/", "checkpoints/", "wandb/", "build/", "dist/")
GENERATED_SUFFIXES = (".pt", ".pth", ".ckpt", ".safetensors", ".onnx", ".aux", ".log", ".bbl", ".blg")


def run(repo: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(args, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.strip()


def git_lines(repo: Path, *args: str) -> list[str]:
    code, out = run(repo, "git", *args)
    return out.splitlines() if code == 0 and out else []


def walk_files(repo: Path, max_depth: int | None = None):
    for root, dirs, files in os.walk(repo):
        root_path = Path(root)
        rel_root = root_path.relative_to(repo)
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".git")]
        if max_depth is not None and len(rel_root.parts) >= max_depth:
            dirs[:] = []
        for name in files:
            yield root_path / name


def package_candidates(repo: Path) -> list[str]:
    candidates: set[str] = set()
    for init in repo.glob("*/__init__.py"):
        if init.parent.name not in SKIP_DIRS:
            candidates.add(init.parent.relative_to(repo).as_posix())
    for init in repo.glob("src/*/__init__.py"):
        candidates.add(init.parent.relative_to(repo).as_posix())
    for manifest in ("Cargo.toml", "go.mod", "package.json", "Project.toml"):
        if (repo / manifest).is_file():
            candidates.add(f"<manifest:{manifest}>")
    return sorted(candidates)


def relative_files(path: Path, pattern: str) -> list[str]:
    if not path.is_dir():
        return []
    return sorted(p.relative_to(path).as_posix() for p in path.glob(pattern) if p.is_file())


def build_report(repo: Path, package: str | None) -> dict:
    files = list(walk_files(repo, max_depth=5))
    suffix_counts = Counter(p.suffix.lower() or "<none>" for p in files)
    tracked = git_lines(repo, "ls-files")
    status = git_lines(repo, "status", "--short")
    docs = repo / "docs"
    scripts = repo / "scripts"

    large_tracked = []
    for rel in tracked:
        path = repo / rel
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size >= 5 * 1024 * 1024:
            large_tracked.append({"path": rel, "bytes": size})

    generated_tracked = [
        rel
        for rel in tracked
        if rel.startswith(GENERATED_PREFIXES) or rel.lower().endswith(GENERATED_SUFFIXES)
    ]
    secret_risks = [
        rel
        for rel in tracked
        if Path(rel).name in {".env", "credentials.json", "secrets.json", "id_rsa"}
    ]

    root_sources = sorted(
        p.name for p in repo.iterdir() if p.is_file() and p.suffix.lower() in SOURCE_SUFFIXES
    )
    script_files = sorted(
        p.relative_to(repo).as_posix()
        for p in scripts.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    ) if scripts.is_dir() else []

    writing = docs / "writing"
    report = {
        "repo": str(repo),
        "git": {
            "is_repo": bool((repo / ".git").exists() or git_lines(repo, "rev-parse", "--show-toplevel")),
            "status": status,
            "tracked_files": len(tracked),
        },
        "top_level": sorted(p.name + ("/" if p.is_dir() else "") for p in repo.iterdir()),
        "code": {
            "requested_package": package,
            "package_candidates": package_candidates(repo),
            "root_source_files": root_sources,
            "source_suffix_counts": {k: suffix_counts[k] for k in sorted(suffix_counts) if k in SOURCE_SUFFIXES},
            "has_archive": (repo / "archive").is_dir()
            or bool(package and (repo / package / "archive").is_dir())
            or any((repo / candidate / "archive").is_dir() for candidate in package_candidates(repo) if not candidate.startswith("<")),
        },
        "docs": {
            "present": docs.is_dir(),
            "root_files": sorted(p.name for p in docs.glob("*") if p.is_file()) if docs.is_dir() else [],
            "method": (docs / "METHOD.md").is_file(),
            "roadmap": (docs / "ROADMAP.md").is_file(),
            "lesson_index": (docs / "LESSON.md").is_file(),
            "code_structure": (docs / "CODE_STRUCTURE.md").is_file(),
            "lesson_files": len(relative_files(docs / "lessons", "**/*.md")),
            "meeting_files": len(relative_files(docs / "meetings", "*.md")),
            "survey_files": len(relative_files(docs / "surveys", "*.md")),
            "writing_present": writing.is_dir(),
            "writing_facts": (writing / "FACTS.md").is_file(),
            "writing_status": (writing / "STATUS.md").is_file(),
        },
        "execution": {
            "scripts_present": scripts.is_dir(),
            "script_count": len(script_files),
            "common_runner": any((repo / p).is_file() for p in ("scripts/run.sh", "scripts/run.py", "Makefile", "justfile")),
            "tests_present": (repo / "tests").is_dir(),
            "configs_present": (repo / "configs").is_dir(),
            "env_example": (repo / ".env.example").is_file(),
        },
        "hygiene": {
            "generated_tracked": generated_tracked,
            "secret_risks": secret_risks,
            "large_tracked": large_tracked,
        },
    }
    return report


def validate(report: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs = report["docs"]
    execution = report["execution"]
    code = report["code"]

    if not code["package_candidates"] and not code["requested_package"]:
        errors.append("No active package/source manifest was detected; pass --package or document the native source root.")
    for key, label in (
        ("method", "docs/METHOD.md"),
        ("roadmap", "docs/ROADMAP.md"),
        ("lesson_index", "docs/LESSON.md"),
        ("code_structure", "docs/CODE_STRUCTURE.md"),
    ):
        if not docs[key]:
            errors.append(f"Missing living document: {label}")
    if not execution["scripts_present"]:
        errors.append("Missing scripts/ execution boundary.")
    if not execution["common_runner"]:
        warnings.append("No common command dispatcher detected (scripts/run.*, Makefile, or justfile).")
    if not execution["tests_present"]:
        warnings.append("No tests/ directory detected.")
    if not execution["configs_present"]:
        warnings.append("No configs/ directory detected; confirm configuration ownership is documented elsewhere.")
    if not execution["env_example"]:
        warnings.append("No .env.example detected.")
    if report["git"]["status"]:
        warnings.append("Worktree is dirty; preserve and attribute existing changes before migration.")
    if report["hygiene"]["generated_tracked"]:
        warnings.append("Generated/artifact-like files are tracked; audit before changing ignore rules.")
    if report["hygiene"]["secret_risks"]:
        errors.append("Potential secret files are tracked: " + ", ".join(report["hygiene"]["secret_risks"]))
    if docs["writing_present"] and (not docs["writing_facts"] or not docs["writing_status"]):
        warnings.append("docs/writing exists without both FACTS.md and STATUS.md.")
    return errors, warnings


def print_human(report: dict, do_validate: bool) -> int:
    print(f"Repository: {report['repo']}")
    print(f"Git tracked/status: {report['git']['tracked_files']} / {len(report['git']['status'])} changed entries")
    print("Package candidates: " + (", ".join(report["code"]["package_candidates"]) or "none detected"))
    print("Root source files: " + (", ".join(report["code"]["root_source_files"]) or "none"))
    docs = report["docs"]
    print(
        "Living docs: "
        f"METHOD={docs['method']} ROADMAP={docs['roadmap']} LESSON={docs['lesson_index']} "
        f"CODE_STRUCTURE={docs['code_structure']} lessons={docs['lesson_files']} "
        f"meetings={docs['meeting_files']} surveys={docs['survey_files']} writing={docs['writing_present']}"
    )
    execution = report["execution"]
    print(
        f"Execution: scripts={execution['script_count']} runner={execution['common_runner']} "
        f"tests={execution['tests_present']} configs={execution['configs_present']} env_example={execution['env_example']}"
    )
    hygiene = report["hygiene"]
    print(
        f"Hygiene: generated_tracked={len(hygiene['generated_tracked'])} "
        f"secret_risks={len(hygiene['secret_risks'])} large_tracked={len(hygiene['large_tracked'])}"
    )
    if not do_validate:
        return 0
    errors, warnings = validate(report)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    print(f"Validation: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--package", help="Expected active package/source root when auto-detection is ambiguous")
    parser.add_argument("--json", action="store_true", help="Emit the full inventory as JSON")
    parser.add_argument("--validate", action="store_true", help="Check the sustainable-layout contract")
    args = parser.parse_args()
    repo = args.repo.expanduser().resolve()
    if not repo.is_dir():
        parser.error(f"repository path is not a directory: {repo}")
    report = build_report(repo, args.package)
    if args.json:
        if args.validate:
            errors, warnings = validate(report)
            report["validation"] = {"errors": errors, "warnings": warnings}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if args.validate and report["validation"]["errors"] else 0
    return print_human(report, args.validate)


if __name__ == "__main__":
    sys.exit(main())
