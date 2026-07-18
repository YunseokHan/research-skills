# CLAUDE.md — {{PROJECT_NAME}}

Follow `AGENTS.md` and this repository's living documents. Project-specific details below override generic defaults.

## Project identity

- Purpose: [replace with verified project purpose]
- Active package: `{{PACKAGE_NAME}}/`
- Stable commands: [list verified commands]
- Environment: load machine-specific values from `.env`; keep only the safe schema in `.env.example`.

## Required read order

1. `docs/LESSON.md` and task-relevant lessons, to avoid repeating rejected work;
2. `docs/METHOD.md`, the current method/recipe/evaluation contract;
3. `docs/ROADMAP.md`, unresolved future work only;
4. `docs/CODE_STRUCTURE.md`, before adding or moving code.

## Maintenance routing

- Method/recipe/protocol changes → `docs/METHOD.md`.
- Experiment outcomes and resolved decisions → topic lesson + `docs/LESSON.md` pointer.
- Plans and open questions → `docs/ROADMAP.md`.
- Code layout and entrypoints → `docs/CODE_STRUCTURE.md`.
- Prior-art work → `docs/surveys/` with verified primary sources.
- Paper claims → `docs/writing/FACTS.md` and affected manuscript files when writing exists.

Keep METHOD current, ROADMAP future-only, LESSON pointer-only, and meetings chronological but non-authoritative.

## Execution discipline

Use the common command dispatcher documented in `docs/CODE_STRUCTURE.md`. Validate environment, data/config inputs,
resource ownership, output provenance, and watcher coverage before long-running work. Define explicit success/failure
contracts and do not infer scientific success from a process exit.

## Research discipline

Match comparisons by the budget unit appropriate to this project. Record dataset/split, sample count, seeds,
uncertainty, metric implementation, checkpoint/config revision, and qualitative inspection. Verify external novelty
claims from primary sources. Preserve negative results and state risks/reopen conditions.
