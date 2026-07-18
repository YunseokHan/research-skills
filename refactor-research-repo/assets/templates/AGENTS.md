# {{PROJECT_NAME}} repository policy

## Read order

Before acting, read this file, `CLAUDE.md` when present, `docs/LESSON.md`, `docs/METHOD.md`, and the task-relevant
lesson/roadmap/code-structure documents. Current code and primary artifacts outrank chat summaries.

## Documentation completion gate

A material change is incomplete until its living documentation is updated in the same change:

- current method, recipe, or evaluation contract → `docs/METHOD.md`;
- resolved result or decision → matching `docs/lessons/<topic>.md` and pointer/status in `docs/LESSON.md`;
- remaining plan, hypothesis, dependency, budget, or decision gate → `docs/ROADMAP.md`;
- code layout or command ownership → `docs/CODE_STRUCTURE.md`;
- paper-relevant claim → synchronize `docs/writing/` when it exists.

Remove resolved work from ROADMAP rather than appending a run diary. Preserve superseded designs in lessons/archive.

## Safety and authority

Preserve unrelated user changes. Inspection does not authorize launches, external messages, remote mutation, data
migration, or destructive cleanup. Never expose or commit secrets, private data, machine-local paths, or transcripts.

## Evidence and experiment completion

Separate verified evidence, reported claims, inference, and unknowns. Do not treat training completion as an empirical
verdict. A completed experiment requires the exact protocol, matched control, budget, seeds/repetitions, uncertainty,
machine-readable metrics, an appropriate quantitative visualization, and representative qualitative evidence when the
domain has visual outputs. Record provenance and update the owning lesson/METHOD before declaring completion.

## Repository boundaries

Active importable code lives under `{{PACKAGE_NAME}}/` or the configured source root. Execution/orchestration lives
under `scripts/`; configuration under `configs/`; tests under `tests/`; generated cache/logs/outputs stay ignored.
Verified inactive work moves to an archive outside the active import closure and is not silently deleted.
