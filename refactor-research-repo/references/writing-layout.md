# Conference-Neutral Writing Layout

Use this reference only when the target repository already contains a manuscript, submission template, bibliography,
paper tables/figures, or a concrete request to start a paper.

## Target organization

```text
docs/writing/
├── FACTS.md                 # claim/evidence/protocol ledger; paper source of truth
├── STATUS.md                # draft state, target venue/deadline, blockers
├── main.tex                 # manuscript-owned assembly file
├── math_commands.tex
├── references.bib
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related_work.tex
│   ├── method.tex
│   ├── experiments.tex
│   ├── conclusion.tex
│   └── appendices/
├── tables/                  # manuscript-owned table sources
├── figs/                    # stable paper figures, not transient run outputs
├── venue/                   # unmodified conference/journal template and style files
│   └── <venue-year>/
└── builds/                  # ignored generated PDFs/auxiliaries, or use a repo-level build dir
```

Adapt section names to the field and venue. Do not create empty sections merely to match this example.

## Venue independence

- Keep manuscript content in project-owned section/table/figure files.
- Isolate official style, class, bibliography style, and submission wrapper files under `venue/<venue-year>/` or an
  equally explicit boundary.
- Keep a single canonical `main.tex`; when venues require incompatible wrappers, make thin venue entry files that
  import the canonical content rather than forking the paper.
- Preserve official templates and licenses verbatim. Never “clean up” a `.sty`, `.cls`, or example file unless the
  user explicitly maintains the template.
- Store venue, track, anonymity mode, page limit, deadline, and compilation command in `STATUS.md`, not throughout
  the manuscript.

## Evidence synchronization

`FACTS.md` should record the thesis, contribution candidates, current method, verified headline results, protocol,
limitations, prior-art boundaries, and pending evidence. Every quantitative claim in TeX must trace to a stable result
artifact and compatible protocol. Update METHOD/lessons first, FACTS second, manuscript/tables third, and compile last.

Do not promote a running experiment, internal diagnostic, unmatched budget, or uninspected qualitative result into a
paper claim. Draft annotations must identify the exact missing evidence and be removable for submission.

## Build hygiene

- Provide one `scripts/compile_paper.sh` or equivalent command.
- Ignore auxiliary files and generated builds while keeping source figures and required venue files tracked.
- Require zero undefined citations/references and inspect affected PDF pages after layout changes.
- Keep submission archives reproducible from tracked source plus explicitly documented external assets.
