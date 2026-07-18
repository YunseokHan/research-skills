# Sustainable Research Repository Target Layout

## Contents

1. Core tree
2. Code ownership
3. Documentation ownership
4. Script ownership
5. State and artifact boundaries
6. Optional components

## 1. Core tree

Adapt names and language conventions; do not copy `ctsa` as a literal package name.

```text
<repo>/
├── AGENTS.md                 # repository policy and agent authority
├── CLAUDE.md                 # optional Claude-specific adapter to shared policy
├── README.md                 # user-facing overview and quick start, not method truth
├── pyproject.toml            # or language-native package/build manifest
├── .env.example              # variable names and safe examples only
├── .gitignore
├── <package>/                # or src/<package>/; active import closure
│   ├── train.*               # stable public entrypoint when applicable
│   ├── infer.*
│   ├── config.*
│   ├── models/
│   ├── data/
│   │   └── build/            # versioned data preparation code
│   ├── eval/
│   └── archive/              # inactive, documented, not imported
├── configs/                  # versioned inputs, no secrets or machine paths
├── tests/
├── scripts/
│   ├── run.sh                # or equivalent common dispatcher
│   └── archive/              # completed one-off orchestration
├── docs/
│   ├── METHOD.md
│   ├── ROADMAP.md
│   ├── LESSON.md
│   ├── CODE_STRUCTURE.md
│   ├── lessons/
│   │   ├── history/          # frozen/raw provenance only when needed
│   │   └── legacy/           # verbatim stale documents
│   ├── meetings/
│   ├── surveys/
│   ├── figures/
│   └── writing/              # optional; only for actual paper artifacts
├── skills/                   # optional repository-local reusable agent workflows
├── cache/                    # ignored/generated
├── logs/                     # ignored/generated
└── outputs/                  # ignored/generated checkpoints/results
```

Repositories may use `artifacts/`, `runs/`, `checkpoints/`, or object storage instead of the last three directories.
The invariant is that generated state is not intermingled with active source or living documentation.

## 2. Code ownership

- The package is the active import closure. A file under `archive/` must not be imported by active code.
- Package modules own reusable logic. `scripts/` owns command composition and operations, not core algorithms.
- Data preparation belongs under a discoverable data/build boundary rather than loose root scripts.
- Evaluation owns metric implementations, protocol definitions, collation, and report generation.
- Public entrypoints are few and stable. Internal file names may change without changing the user command surface.
- Helpers stay close to their owning subsystem; avoid one global `utils.py` that silently couples the repository.

## 3. Documentation ownership

| File | Owns | Must not become |
|---|---|---|
| `METHOD.md` | Current method, recipe, inference, evaluation contract | Historical diary or future wish list |
| `ROADMAP.md` | Unresolved hypotheses, triggers, budgets, decision rules | Append-only run log |
| `LESSON.md` | One-line topic pointers and status | Full lesson content |
| `lessons/<topic>.md` | Verdict, evidence, negative results, risk, reopen rule | Unfiltered logs |
| `CODE_STRUCTURE.md` | Active layout, entrypoints, placement/archive rules | File dump without ownership |
| `meetings/` | Time-bounded delta reports | Canonical method specification |
| `surveys/` | Verified external prior art and novelty boundary | Memory-based bibliography |
| `writing/FACTS.md` | Paper claim/evidence ledger | Replacement for METHOD |

Every material statement should have one authoritative owner and downstream consumers. Meeting notes and papers may
summarize the owner but must not silently diverge from it.

## 4. Script ownership

Recommended categories, whether represented as folders, prefixes, or a registry:

- stable command dispatcher;
- train/infer/eval wrappers;
- experiment orchestration;
- data build and migration;
- report/figure rendering;
- health checks and external watchers;
- archive of completed one-offs.

Each long-running workflow should define inputs, provenance manifest, output root, failure marker, success contract,
watcher, and idempotent resume/retry policy.

## 5. State and artifact boundaries

- `configs/`: versioned intent.
- `outputs/` or artifact store: generated results and checkpoints.
- `logs/`: execution evidence, not scientific summary.
- `cache/`: reproducible or externally sourced acceleration state.
- `docs/`: distilled, reviewable research memory.
- `.env`: local secrets and machine paths; `.env.example`: safe schema.

Never cite a checkpoint merely by a mutable nickname. Record config, code revision, data manifest, seed, budget, and
evaluation protocol in its manifest or report bundle.

## 6. Optional components

- `notebooks/`: exploration only; promote reusable logic into the package and record conclusions in lessons.
- `workflows/` or CI configuration: useful for tests, docs links, paper compilation, and packaging.
- `third_party/`: retain license and upstream revision; do not mix with project-owned source.
- `docs/writing/`: include only when a real draft, submission template, or paper evidence ledger exists.
- `skills/`: track repository-specific workflows that should generalize across sessions or sibling projects.
