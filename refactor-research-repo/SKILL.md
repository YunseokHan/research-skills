---
name: refactor-research-repo
description: Audit and refactor an existing research repository into a sustainable layout that separates active package code, living research documentation, execution/orchestration scripts, tests/configuration, generated artifacts, and archived work. Use when migrating a research codebase into a CTSA-style structure, reorganizing `docs/` around METHOD/ROADMAP/LESSON/meetings/surveys, standardizing `scripts/`, adding repository governance, or organizing existing paper artifacts under a conference-neutral `docs/writing/` layout.
---

# Refactor Research Repository

Turn an existing research repository into a maintainable research system without changing scientific behavior or
discarding provenance. Transfer the ownership rules and evidence discipline, not CTSA-specific names or methods.

## 1. Establish the migration boundary

1. Resolve `<repo>` from the user-provided path or current directory.
2. Read every applicable repository instruction file completely (`AGENTS.md`, `CLAUDE.md`, and equivalents).
3. Inspect Git status and treat every existing change as user-owned. Do not mix unrelated cleanup into the migration.
4. Ask only when the package identity, paper ownership, or destructive migration boundary cannot be inferred safely.
5. Never launch experiments, move external datasets, rewrite results, or alter remote state merely to reorganize the
   repository.

The migration must preserve current imports, commands, configs, checkpoints, artifact provenance, and user edits unless
the user explicitly authorizes a breaking change.

## 2. Inventory before designing

Run the bundled audit before editing:

```bash
python <skill-dir>/scripts/repo_audit.py --repo <repo>
```

Use `--json` when a machine-readable ledger is useful. Inspect at least:

- active source roots, entry points, tests, configs, notebooks, and native extensions;
- training, inference, evaluation, data-build, reporting, monitoring, and orchestration commands;
- current-state docs, run logs, decision records, meeting notes, surveys, and paper artifacts;
- generated outputs, caches, datasets, credentials, large files, and ignored paths;
- archived or apparently dead code, without assuming that unimported means disposable;
- CI, packaging, environment files, and external path assumptions.

Read [references/target-layout.md](references/target-layout.md) after inventory. Read
[references/migration-playbook.md](references/migration-playbook.md) before proposing file moves. If manuscript or
submission artifacts exist, also read [references/writing-layout.md](references/writing-layout.md).
When the reference repository has mature `AGENTS.md`/`CLAUDE.md` policies, read
[references/governance-transfer.md](references/governance-transfer.md) before
drafting target instructions.

## 3. Produce a source-to-target map

Before moving code, build a migration ledger with these columns:

| Current path | Target path | Role | Action | Import/command consumers | Evidence/docs owner | Risk |
|---|---|---|---|---|---|---|

Classify every material path as active, generated, external, archived, ambiguous, or user-owned. Resolve ambiguity from
imports, command references, recent Git history, configs, logs, and documented workflows. Do not infer current method
state from filename age alone.

Use the project’s own package name. Never rename a target package to `ctsa` unless that is the real project name.

## 4. Scaffold only missing governance

Preview the non-destructive scaffold:

```bash
python <skill-dir>/scripts/scaffold_layout.py \
  --repo <repo> --project-name "<name>" --package-name "<package>" --dry-run
```

Remove `--dry-run` only after the mapping is coherent. Add `--with-writing` only when real manuscript or submission
artifacts exist. The scaffold never overwrites existing files; merge templates into existing policies manually.

Templates use `{{PROJECT_NAME}}` and `{{PACKAGE_NAME}}` placeholders. Treat them as starting points, not claims about
the target repository.

## 5. Refactor in dependency order

### 5.1 Active code

1. Establish one active package root (`src/<package>/` or `<package>/`, following existing packaging convention).
2. Keep only stable public entry modules at the package root; group implementation by responsibility such as
   `models/`, `data/`, `eval/`, `training/`, and package-local utilities.
3. Keep importable logic in the package. Keep shell policy, experiment composition, fleet operations, and user-facing
   command wrappers in `scripts/`.
4. Move verified superseded code to an explicit archive excluded from the active import closure. Do not delete it.
5. Update imports, module entry points, configs, tests, and documentation atomically with each move.

Do not force a Python layout onto a non-Python repository. Preserve the same separation of active library,
entrypoints, scripts, tests, configuration, generated state, and archive using the language’s native conventions.

### 5.2 Living documentation

Make `docs/` the durable research memory rather than a dump of chronological notes:

- `METHOD.md`: current method/specification, current recipe, and evaluation contract only;
- `ROADMAP.md`: future work only, with hypothesis, reason, dependency/trigger, budget, and decision rule;
- `LESSON.md`: pointer-only index into topic lessons;
- `lessons/<topic>.md`: resolved decisions, negative results, key evidence, risks, and reopen conditions;
- `CODE_STRUCTURE.md`: active layout, ownership boundaries, entry points, and archive rules;
- `meetings/`: dated research updates that compare against the previous meeting;
- `surveys/`: externally verified prior-art reviews and novelty boundaries;
- `figures/`: stable documentation figures with relative links;
- `writing/`: optional and created only for real paper artifacts.

Route every migrated statement to one owner. Do not keep the same method truth in README, ROADMAP, meeting notes, and
paper without declaring which copy is authoritative.

### 5.3 Execution scripts

1. Provide one discoverable dispatcher such as `scripts/run.sh`, `scripts/run.py`, `make`, or task-runner equivalent.
2. Separate stable entry wrappers from experiment orchestrators, evaluators/report builders, monitors/watchers, and
   data-build tools.
3. Make launch scripts fail closed: validate environment, inputs, output provenance, and resource ownership before
   mutation.
4. Give long jobs explicit DONE/FAILED semantics and external monitoring; a process exit alone is not a complete
   research result.
5. Move completed one-off scripts to `scripts/archive/` with enough context to identify their campaign.

### 5.4 Configuration, tests, and artifacts

- Put versioned experiment/configuration inputs in `configs/` or the project-native equivalent.
- Keep fast correctness tests in `tests/`; add import and command smoke tests for moved entry points.
- Keep `.env.example` versioned and secrets in ignored local environment files.
- Keep datasets, caches, checkpoints, logs, and generated outputs outside the active source tree and ignored by default.
- Record artifact schemas, naming, provenance, and reproduction commands without committing large generated state.

## 6. Install sustainability rules

Build a policy-transfer ledger before editing target instructions:

| Source rule | Portable invariant | Target parameter/evidence | Target owner | Literal excluded |
|---|---|---|---|---|

Review every normative section of the source `AGENTS.md` and `CLAUDE.md`; do not
transfer only directory layout. Preserve generally applicable research and
operational discipline while parameterizing package names, commands, resources,
datasets, metrics, venues, paths, session identifiers, and tool availability.
Use the extraction and rejection tests in
[references/governance-transfer.md](references/governance-transfer.md).

Merge the policy templates into repository-local instructions. Require:

- living docs updated in the same change as material code, method, result, recipe, or plan changes;
- plans removed from ROADMAP when resolved and distilled into topic lessons;
- evidence labels that separate verified results, reported claims, inference, and unknowns;
- matched protocols, seeds/repetitions, budgets, uncertainty, and qualitative inspection for empirical verdicts;
- preservation of negative results and superseded designs without keeping them in the active import closure;
- no hardcoded secrets, machine-specific paths, or undocumented entry points;
- no paper claim promoted from a running job or incomplete result bundle.
- lessons and primary prior art checked before new ideas or novelty claims;
- current method, future plans, resolved evidence, meeting chronology, and paper
  claims assigned to distinct authoritative owners;
- environment-selected interpreters and machine-local values rather than hardcoded
  paths, plus a safe versioned environment schema;
- correctness tests before expensive runs and fail-closed launch preflights;
- held-out, matched, uncertainty-aware evaluation appropriate to the target domain;
- resource ownership checks, watcher coverage, explicit DONE/FAILED contracts,
  queued continuation, and idle-resource reclamation for shared compute;
- exact-versus-hypothesis language, adversarial review of material decisions, and
  refusal to follow a logically flawed instruction without surfacing the issue;
- paper synchronization and compilation checks when a method, recipe, or best
  result changes and a manuscript exists.

When both Codex and Claude Code participate, also install an explicit supervisory
contract rather than treating them as interchangeable agents:

- Codex owns independent supervision: reconstruct the preceding user–Claude
  conversation, check the latest overriding instruction, and verify Claude's
  claims against repository state, logs, processes, metrics, and artifacts.
- Claude owns bounded implementation and compute operation under the shared
  repository policy. Its requests to Codex must identify the active objective,
  exact write or job/config, resource preflight, expected artifacts and markers,
  watcher, and reclamation/next-queue behavior.
- Give Codex standing authority to execute valid in-scope writes, corrections,
  launches, evaluations, transitions, retries, documentation sync, and compute
  reclamation without relaying each routine action to the user. Require Codex to
  hold destructive, credential/access, external-publication, third-party-resource,
  ambiguous research-direction, or provenance-bypassing requests.
- Require every Claude report to be audited in conversational context. A plausible
  status that answers the wrong task, forgets a correction, confuses neighboring
  experiments, or omits promised evidence is a supervisory failure.
- Configure repository-local, read-only pointers to the active Claude transcript
  and any Codex operator-report task through ignored environment variables when
  those facilities exist. Never hardcode a user's home path or copy transcripts
  into the repository.
- When the user asks for status, require a connected prose report covering the
  preceding decision context, per-job state, verified versus reported evidence,
  bottlenecks, risks, ETAs, transitions, and next autonomous actions.

Adapt this contract to the target project's actual compute and operator surfaces.
Do not copy CTSA node names, GPU topology, session paths, or commands.

These governance rules are a more important transfer than any exact directory name.

## 7. Organize writing only when applicable

When paper artifacts exist, follow [references/writing-layout.md](references/writing-layout.md). Keep the layout
conference-neutral: isolate venue-provided style files and submission wrappers from manuscript-owned sections, facts,
tables, figures, bibliography, and compilation scripts. Preserve the original venue template and licenses; do not
rewrite style files.

Do not create a fake manuscript merely to satisfy the layout.

## 8. Validate the migration

Run:

```bash
python <skill-dir>/scripts/repo_audit.py --repo <repo> --validate
```

Then validate in proportion to the move:

1. import/package smoke tests and the project test suite;
2. help/dry-run for every stable command and orchestrator changed;
3. config and environment loading from a clean shell;
4. relative documentation links and living-doc ownership;
5. no tracked caches, credentials, generated binaries, or accidental large files;
6. paper compilation and citation/reference checks when writing exists;
7. final Git diff, including rename coverage and unrelated user edits.
8. policy checks proving that the generated `AGENTS.md` and `CLAUDE.md` agree on
   the Codex-supervisor/Claude-operator boundary, autonomous-action validity gate,
   conversational-context audit, and status-report contract.

Do not report success if the new tree exists but old commands, imports, links, or documentation still point to the
previous layout.

## 9. Hand off

Report:

- the final tree and source-to-target mapping;
- behavior-preserving compatibility shims, if any, and their removal plan;
- commands/tests/audits executed and exact failures remaining;
- documents created or synchronized and their ownership contract;
- archived versus deleted material (deletion should normally be none);
- generated/external paths intentionally left outside the repository;
- follow-up migrations that were intentionally deferred.

For a copy-ready user instruction, use [assets/refactor-instruction.md](assets/refactor-instruction.md).
