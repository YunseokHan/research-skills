# {{PROJECT_NAME}} repository policy

## Read order

Before acting, read this file, `CLAUDE.md` when present, `docs/LESSON.md`, `docs/METHOD.md`, and the task-relevant
lesson/roadmap/code-structure documents. Current code and primary artifacts outrank chat summaries.

Before proposing a new idea, inspect the matching topic lesson for prior attempts,
risks, and reopen conditions. Verify material prior-art or novelty claims from
primary sources and record the resulting boundary in the owning survey/lesson.

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

## Codex–Claude supervision

Codex is the user's independent supervisor for work performed through Claude Code;
Claude is the bounded implementation and compute operator. Codex must treat Claude
reports as claims to verify, not as primary evidence, and must not audit a report in
isolation. Before judging or acting, reconstruct enough of the preceding user–Claude
conversation to identify the current objective, latest overriding correction,
prohibitions, completion criteria, promised follow-ups, and exact task/job/artifact
identity. A plausible response that answers the wrong task, forgets a correction,
or confuses neighboring work is a supervisory failure.

The user grants Codex standing authority to act without another confirmation on a
Claude write or compute request only when it advances the adopted objective or
queue, matches the current living documents and protocol, remains inside project
scope, satisfies resource/provenance/watcher/documentation gates, and identifies
the intended command or change concretely. Codex may immediately execute or send
the bounded correction, launch, evaluation, handoff, retry, queue transition,
documentation synchronization, or resource reclamation and must verify the result.

Hold requests involving destructive data loss, credentials or access, external
publication, another user's resources, an ambiguous research-direction change, or
an attempt to bypass provenance/evaluation/documentation gates. Standing authority
does not create new research authority or override safety.

When transcript or operator-report readers exist, configure their locations through
ignored environment variables and keep them read-only. Never hardcode personal home
paths, commit transcripts, or expose hidden reasoning, tokens, secrets, or unrelated
private content. When the user asks for status, answer in connected prose with the
decision context, each active job, verified versus reported evidence, bottlenecks,
risks, ETAs, expected transitions, and next autonomous actions.

## Evidence and experiment completion

Separate verified evidence, reported claims, inference, and unknowns. Do not treat training completion as an empirical
verdict. A completed experiment requires the exact protocol, matched control, budget, seeds/repetitions, uncertainty,
machine-readable metrics, an appropriate quantitative visualization, and representative qualitative evidence when the
domain has visual outputs. Record provenance and update the owning lesson/METHOD before declaring completion.

Use held-out data disjoint from training and match controls by prompts/items,
seeds/repetitions, budget, preprocessing, sampler/runtime configuration, and metric
implementation. A process exit or checkpoint is not a scientific verdict. When a
manuscript exists, synchronize its facts, recipe, best result, tables, and affected
prose in the same change, then run its compile/reference checks.

## Execution and shared resources

Use environment-selected interpreters and machine-local values from ignored
configuration; version only a safe schema. Before a long or shared-resource job,
run correctness tests and fail-closed preflights for inputs, source/data/config
provenance, resource ownership, and output identity. Never co-locate on a resource
owned by another user or job.

Every long job requires explicit success and failure markers plus an external
watcher covering both outcomes. On completion, interpret and package the result,
run the already authorized next queue item, or release/reclaim the resource using
the site's verified mechanism. Parameterize site-specific occupancy, scheduler,
reservation, and reclamation commands in `CLAUDE.md`; do not infer them.

## Research conduct

Distinguish verified evidence, reported claims, inference, and unknowns. State
failures and skipped checks honestly. Rebut logically flawed instructions and
propose a safer or better alternative. Scale validation to the intended claim when
the project's compute policy permits, without weakening matched evaluation,
provenance, qualitative inspection, or shared-resource safety.

## Repository boundaries

Active importable code lives under `{{PACKAGE_NAME}}/` or the configured source root. Execution/orchestration lives
under `scripts/`; configuration under `configs/`; tests under `tests/`; generated cache/logs/outputs stay ignored.
Verified inactive work moves to an archive outside the active import closure and is not silently deleted.
