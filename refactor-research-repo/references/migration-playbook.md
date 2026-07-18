# Migration Playbook

## Contents

1. Preserve before improving
2. Code migration
3. Documentation distillation
4. Execution migration
5. Governance transfer
6. Compatibility and rollout
7. Common failure modes

## 1. Preserve before improving

Create the inventory and source-to-target ledger before touching paths. Record the current test command, stable user
commands, import roots, package manifest, environment schema, data roots, output conventions, current paper build, and
dirty worktree. When a file appears unused, verify imports, shell references, configs, documentation, recent history,
and external launch commands before calling it dead.

Prefer staged migration:

1. introduce target directories and governance;
2. move one subsystem and update all consumers;
3. validate behavior;
4. add a temporary compatibility shim only when unavoidable;
5. move the next subsystem;
6. archive verified superseded material;
7. remove shims only in an explicitly approved breaking change.

## 2. Code migration

Group by responsibility, not by campaign date or model nickname. Typical mapping:

| Existing material | Target owner |
|---|---|
| model definitions and frozen-backbone loaders | `<package>/models/` |
| datasets, transforms, extraction, manifest builders | `<package>/data/` and `data/build/` |
| metrics, evaluation protocols, report collation | `<package>/eval/` |
| stable training/inference APIs | package root or dedicated `training/`/`inference/` |
| shell composition, cluster launch, sweep definitions | `scripts/` |
| constants meant to vary by run | `configs/` |
| CPU/GPU correctness and regression checks | `tests/` |
| verified inactive implementation | package or scripts `archive/` |

Do not combine architecture redesign with path migration unless the user requests both. A structural refactor should
have behavior-preserving acceptance tests.

## 3. Documentation distillation

Classify each existing document paragraph:

- current method/recipe/protocol → `METHOD.md`;
- unresolved future experiment → `ROADMAP.md`;
- resolved result or rejected idea → `lessons/<topic>.md`;
- code ownership/entrypoint → `CODE_STRUCTURE.md`;
- chronological delta → `meetings/`;
- verified external comparison → `surveys/`;
- paper claim or submission artifact → `writing/`;
- raw historical source worth preserving → `lessons/history/` or `legacy/`.

Do not copy the same chronological document into every category. Distill it, keep a provenance pointer, and preserve a
verbatim source only when its loss would matter.

Topic lessons should include:

1. status;
2. question and scope;
3. verified evidence and exact protocol;
4. verdict and rejected interpretations;
5. consequence for the current method;
6. risk and reopen condition;
7. provenance paths.

Roadmap items should include what, why, dependency/trigger, budget, comparison/control, success/kill rule, and artifact
bundle. Remove resolved items instead of marking the roadmap as an execution diary.

## 4. Execution migration

Build a stable command surface first. A common dispatcher prevents every meeting or operator from inventing a new
command. It should use an environment-selected interpreter and forward arguments without hiding them.

For each long job, distinguish:

- launcher: validates inputs/resources, writes manifest, starts work;
- worker: performs one bounded task;
- watcher: observes progress, crashes, artifact consistency, and teardown;
- report builder: turns raw metrics into a table, plot, and qualitative artifact;
- dispatcher: performs an already authorized dependency transition idempotently.

Avoid scripts that declare success solely because a process exited or a checkpoint exists. Define the full completion
contract and do not let monitors invent scientific decisions.

## 5. Governance transfer

The most important style transfer from CTSA is the research state machine:

```text
hypothesis in ROADMAP
  -> versioned config + executable script
  -> run manifest + raw artifacts
  -> matched evaluation + uncertainty + qualitative check
  -> topic lesson verdict
  -> METHOD update if adopted
  -> paper FACTS/manuscript update if claim-relevant
```

Install these rules in repository instructions:

- code and matching documentation land together;
- plans, current method, and history have different owners;
- chat and agent reports are leads, not primary evidence;
- no result is complete without protocol and an inspectable result bundle;
- negative results remain discoverable;
- external prior-art claims require primary-source verification;
- shared compute operations require ownership, preflight, watcher, and reclamation policies appropriate to the site;
- agents do not expand authority from read-only review into launches or external mutation.

## 6. Compatibility and rollout

Preserve stable commands when possible by forwarding old entrypoints to new modules with a deprecation note. Record
every shim in `CODE_STRUCTURE.md` with owner and removal condition. Avoid indefinite duplicate implementations.

For large migrations, land independently testable slices:

1. docs ownership and policy;
2. package boundary and imports;
3. stable command dispatcher;
4. evaluation/reporting boundary;
5. archive and generated-state cleanup;
6. optional writing organization.

## 7. Common failure modes

- Copying CTSA-specific package names, servers, metrics, or conference files into an unrelated project.
- Creating empty documentation that claims facts not recovered from evidence.
- Turning ROADMAP into a task checklist with completed run logs.
- Moving code without updating shell scripts, configs, module invocations, tests, and docs.
- Treating `archive/` as a second active source tree.
- Committing checkpoints, caches, private data, credentials, LaTeX auxiliaries, or machine paths.
- Reformatting the whole repository so the structural diff becomes unauditable.
- Deleting negative results because they are not part of the current method.
- Creating `docs/writing/` when no paper exists, or binding manuscript structure to one venue.
- Reporting “refactor complete” when compatibility shims, stale imports, broken links, or missing commands remain.
