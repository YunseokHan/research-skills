#!/usr/bin/env python3
"""Audit the structural integrity and draft state of docs/writing."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}")
FIGURE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.MULTILINE)
ANNOTATION_RE = re.compile(r"\\(codex|claude|han)\s*\{")
PENDING_RE = re.compile(r"\b(?:PENDING|PEND|TODO|TBD|FIXME)\b", re.IGNORECASE)


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        lines.append(line[: match.start()] if match else line)
    return "\n".join(lines)


def tex_path(writing: Path, raw: str) -> Path:
    path = writing / raw
    if path.suffix == "":
        path = path.with_suffix(".tex")
    return path.resolve()


def source_closure(writing: Path) -> tuple[list[Path], list[str]]:
    root = (writing / "main.tex").resolve()
    queue = [root]
    seen: set[Path] = set()
    missing: list[str] = []
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        if not path.is_file():
            missing.append(str(path))
            continue
        text = strip_comments(path.read_text(encoding="utf-8"))
        for raw in INPUT_RE.findall(text):
            child = tex_path(writing, raw)
            if child not in seen:
                queue.append(child)
    return sorted(path for path in seen if path.is_file()), sorted(missing)


def resolve_figure(writing: Path, raw: str) -> Path | None:
    base = (writing / raw).resolve()
    candidates = [base] if base.suffix else [base.with_suffix(ext) for ext in (".pdf", ".png", ".jpg", ".jpeg", ".eps")]
    return next((path for path in candidates if path.is_file()), None)


def line_markers(path: Path, text: str) -> list[dict[str, object]]:
    markers: list[dict[str, object]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if PENDING_RE.search(line):
            markers.append({"file": str(path), "line": number, "text": line.strip()[:240]})
    return markers


def audit(repo: Path, submission: bool, require_fresh_pdf: bool) -> tuple[dict[str, object], list[str]]:
    repo = repo.resolve()
    writing = repo / "docs" / "writing"
    errors: list[str] = []
    for required in (writing / "main.tex", writing / "FACTS.md", writing / "STATUS.md", writing / "reference.bib"):
        if not required.is_file():
            errors.append(f"missing required file: {required.relative_to(repo)}")

    sources, missing_inputs = source_closure(writing) if (writing / "main.tex").is_file() else ([], [])
    errors.extend(f"missing input: {path}" for path in missing_inputs)

    combined = "\n".join(strip_comments(path.read_text(encoding="utf-8")) for path in sources)
    citations = sorted({key.strip() for group in CITE_RE.findall(combined) for key in group.split(",") if key.strip()})
    bib_text = (writing / "reference.bib").read_text(encoding="utf-8") if (writing / "reference.bib").is_file() else ""
    bib_keys = set(BIB_RE.findall(bib_text))
    missing_citations = sorted(set(citations) - bib_keys)
    errors.extend(f"missing bibliography entry: {key}" for key in missing_citations)

    labels = [label for label in LABEL_RE.findall(combined) if "#" not in label]
    label_counts = Counter(labels)
    duplicate_labels = sorted(label for label, count in label_counts.items() if count > 1)
    refs = sorted({label for label in REF_RE.findall(combined) if "#" not in label})
    missing_refs = sorted(set(refs) - set(labels))
    errors.extend(f"duplicate label: {label}" for label in duplicate_labels)
    errors.extend(f"undefined static reference: {label}" for label in missing_refs)

    figure_paths = sorted(set(FIGURE_RE.findall(combined)))
    missing_figures = sorted(raw for raw in figure_paths if resolve_figure(writing, raw) is None)
    errors.extend(f"missing figure: {path}" for path in missing_figures)

    annotations = Counter(ANNOTATION_RE.findall(combined))
    pending: list[dict[str, object]] = []
    for path in sources:
        relative = path.relative_to(repo)
        text = strip_comments(path.read_text(encoding="utf-8"))
        pending.extend(line_markers(relative, text))

    pdf = writing / "main.pdf"
    freshness_sources = sources + ([writing / "reference.bib"] if (writing / "reference.bib").is_file() else [])
    latest_source_ns = max((path.stat().st_mtime_ns for path in freshness_sources), default=0)
    pdf_stale = not pdf.is_file() or pdf.stat().st_mtime_ns < latest_source_ns
    if require_fresh_pdf and pdf_stale:
        errors.append("main.pdf is missing or older than a compiled source")

    if submission:
        for name, count in sorted(annotations.items()):
            if count:
                errors.append(f"submission contains {count} \\{name} annotation(s)")
        if pending:
            errors.append(f"submission contains {len(pending)} pending marker line(s)")

    payload: dict[str, object] = {
        "writing_root": str(writing.relative_to(repo)),
        "source_count": len(sources),
        "source_files": [str(path.relative_to(repo)) for path in sources],
        "citation_count": len(citations),
        "missing_citations": missing_citations,
        "label_count": len(set(labels)),
        "duplicate_labels": duplicate_labels,
        "missing_references": missing_refs,
        "figure_count": len(figure_paths),
        "missing_figures": missing_figures,
        "annotations": dict(sorted(annotations.items())),
        "pending_markers": pending,
        "pdf_exists": pdf.is_file(),
        "pdf_stale": pdf_stale,
        "submission_mode": submission,
        "errors": errors,
    }
    return payload, errors


def print_human(payload: dict[str, object]) -> None:
    print(f"writing root: {payload['writing_root']}")
    print(
        f"sources={payload['source_count']} citations={payload['citation_count']} "
        f"labels={payload['label_count']} figures={payload['figure_count']}"
    )
    annotations = payload["annotations"]
    annotation_summary = ", ".join(f"{name}={count}" for name, count in annotations.items()) or "none"
    print(f"draft annotations: {annotation_summary} | pending lines={len(payload['pending_markers'])}")
    print(f"pdf exists={payload['pdf_exists']} stale={payload['pdf_stale']}")
    if payload["pending_markers"]:
        print("pending markers:")
        for marker in payload["pending_markers"]:
            print(f"- {marker['file']}:{marker['line']}: {marker['text']}")
    if payload["errors"]:
        print("errors:")
        for error in payload["errors"]:
            print(f"- {error}")
    else:
        print("structural audit passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--submission", action="store_true", help="Reject draft annotations and pending markers")
    parser.add_argument("--require-fresh-pdf", action="store_true", help="Reject a missing or stale main.pdf")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload, errors = audit(args.repo, args.submission, args.require_fresh_pdf)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human(payload)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
