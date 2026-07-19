# Governance Transfer

## Contents

1. Transfer objective
2. Rule classification
3. Portable policy families
4. Parameterization
5. Rejection tests
6. Validation

## 1. Transfer objective

Treat mature repository instructions as an operational research system, not as
project prose. Inspect every normative section in source `AGENTS.md`, `CLAUDE.md`,
and equivalent files. Transfer the rule's invariant and evidence contract while
replacing source-specific literals with verified target values or explicit
placeholders.

## 2. Rule classification

For each source rule, record:

| Class | Action |
|---|---|
| Portable invariant | Install in target instructions |
| Portable but parameterized | Install with target-derived values or placeholders |
| Source-only fact | Do not copy; record as excluded literal |
| Tool/site capability | Install conditionally after verifying availability |
| Conflicting target policy | Preserve target policy and document the conflict |
| Ambiguous | Ask before changing authority or research intent |

Separate policy from examples. A named GPU node is source-only; “verify resource
ownership before launch” is portable. A specific metric is source-only; “use a
matched held-out protocol with uncertainty and qualitative inspection” is portable.

## 3. Portable policy families

Audit and transfer all applicable families:

1. **Authority and roles** — Codex supervision, Claude operation, autonomous valid
   actions, safety exclusions, conversational-context audit, privacy boundaries.
2. **Read order and truth ownership** — lessons before ideation, current method
   before roadmap, code structure before placement, primary artifacts over chat.
3. **Documentation state machine** — METHOD current-only, ROADMAP future-only,
   LESSON pointer-only, topic lessons for resolved evidence, meetings chronological,
   writing downstream of verified facts.
4. **Ideation and novelty** — internal negative-result check, primary-source prior
   art, adversarial second opinion, explicit novelty/risk/reopen verdict.
5. **Code and archive ownership** — one active import closure, stable entrypoints,
   package/script/config/test separation, archive rather than silent deletion.
6. **Environment and secrets** — environment-selected interpreter, ignored local
   values, safe `.env.example`, no machine paths or credentials in versioned files.
7. **Execution contracts** — tests and preflight before long jobs, immutable config
   and source/data provenance, success/failure markers, idempotent retry/transition.
8. **Shared compute** — actual occupancy/process ownership checks, no co-location on
   foreign work, watcher for success and failure, queued continuation, teardown or
   idle-resource reclamation. Parameterize the site's scheduler/reservation method.
9. **Evaluation** — held-out disjointness, matched prompts/seeds/budgets/sampler,
   multi-run uncertainty, baseline, target-appropriate metrics, qualitative arbiter.
10. **Completion reporting** — table with protocol and uncertainty, saved rendered
    quantitative visualization, representative qualitative evidence, provenance,
    living-doc update; training completion alone is not a result.
11. **Writing** — facts ledger when present, synchronized recipe/best results,
    venue-neutral manuscript ownership, compile/citation/reference checks, honest
    claim calibration and project-defined prose style.
12. **Research conduct** — evidence labels, honesty about failures/skips, challenge
    flawed instructions, scale experiments to the claim when compute policy permits.

## 4. Parameterization

Derive target values from code, configs, scheduler/site docs, environment schema,
tests, and existing instructions. Parameterize at least:

- project/package identity and active source root;
- stable commands, interpreter variable, and test/compile commands;
- compute backend, ownership query, reservation/reclamation mechanism, and watcher;
- dataset manifests and held-out split contract;
- domain metrics, required sample/repetition count, and qualitative artifact;
- paper facts/build paths and venue-owned files;
- transcript/report reader commands and ignored environment variable names.

If a value is unknown, use an explicit `[PROJECT: ...]` placeholder and report the
policy as incomplete. Never silently copy the reference repository's value.

## 5. Rejection tests

Reject a proposed transfer when it:

- copies project names, methods, nodes, GPU topology, datasets, metrics, run tags,
  paths, session IDs, venue names, or timestamps without target evidence;
- grants broader mutation/external authority than the source rule;
- assumes a scheduler, MCP connector, transcript reader, or monitoring facility that
  is not available in the target environment;
- weakens a target safety rule or overwrites a stricter existing instruction;
- converts a research preference into a universal fact without preserving its
  project-policy qualification.

## 6. Validation

Before handoff:

1. account for every normative source heading in the policy-transfer ledger;
2. search generated instructions for excluded source literals;
3. verify `AGENTS.md` and `CLAUDE.md` agree on roles, authority, docs, execution,
   evaluation, and completion;
4. resolve or expose every placeholder;
5. dry-run/scaffold the templates and inspect the rendered files;
6. report intentionally omitted rules and the evidence for omission.
