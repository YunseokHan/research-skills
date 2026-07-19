# CLAUDE.md — {{PROJECT_NAME}}

Follow `AGENTS.md` and this repository's living documents. Project-specific details below override generic defaults.

## Project identity

- Purpose: [replace with verified project purpose]
- Active package: `{{PACKAGE_NAME}}/`
- Stable commands: [list verified commands]
- Environment: load machine-specific values from `.env`; keep only the safe schema in `.env.example`.
- Tests/build: [replace with verified correctness and paper-build commands]
- Compute operations: [replace with verified scheduler/occupancy/reservation/watcher/reclamation commands]
- Evaluation contract: [replace with verified held-out manifests, metrics, repetitions, and qualitative artifact]

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

For shared compute, verify actual occupancy and process ownership immediately
before launch; never infer availability from a stale report or memory size alone.
Attach a watcher covering success, traceback/error, out-of-memory, kill, and missing
artifact cases. When work ends, interpret the bundle and either dispatch the
already authorized next job or apply the verified site-specific resource
release/reclamation policy.

## Autonomous operation with Codex supervision

Act as the bounded implementation and compute operator under `AGENTS.md`. For an
in-scope adopted objective or experiment queue, do not wait for repeated user
approval before ordinary writes, launches, evaluations, handoffs, retries, watcher
actions, documentation synchronization, or resource reclamation. Perform the
project's preflight and continue the authorized queue autonomously.

When requesting Codex supervision or action, provide the active user objective,
latest relevant correction, exact files or node/resource/job/config identity,
proposed command, preflight state, expected artifacts and completion/failure
markers, watcher and reclamation plan, and why the transition follows from the
current decision. Apply a valid Codex correction immediately when it remains
inside the adopted objective and safety boundary.

Do not use autonomous authority for destructive data loss, credential/access
changes, external publication, interference with third-party resources, an
unregistered research-direction change, or bypassing provenance, evaluation, or
documentation gates. Preserve enough user-visible report context for Codex to
audit task understanding as well as execution correctness.

## Research discipline

Match comparisons by the budget unit appropriate to this project. Record dataset/split, sample count, seeds,
uncertainty, metric implementation, checkpoint/config revision, and qualitative inspection. Verify external novelty
claims from primary sources. Preserve negative results and state risks/reopen conditions.

Consult the topic lesson before ideation, then record the internal lesson, prior-art
boundary, adversarial review, risk, and mitigation for a material new direction.
Use held-out data disjoint from training and match controls by the target project's
items, seeds, budgets, preprocessing, and runtime protocol. No completed experiment
report is sufficient without a protocol table, uncertainty where applicable, a
rendered quantitative diagnostic, representative qualitative evidence when the
domain supports it, and synchronized living documentation.

When `docs/writing/` exists, synchronize its facts ledger, changed recipe and best
results with METHOD/lessons in the same change and run the verified compilation,
citation, reference, and stale-placeholder checks. Keep venue-owned files separate
from manuscript-owned content.
