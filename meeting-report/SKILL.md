---
name: meeting-report
description: Create or update weekly research meeting notes by comparing the previous meeting with current verified repository, experiment, and artifact evidence. Use in projects whose root contains `AGENTS.md`, `CLAUDE.md`, and `docs/`, especially when asked to prepare or refresh `docs/meetings/mmdd_meeting.md`, report progress since the last meeting, or organize meeting figures under `docs/figures/mmdd_fig#.png`.
---

# Meeting Report

Create a concise research update in the style and language established by the current project's meeting documents. Treat the previous meeting as the comparison baseline and current artifacts—not chat claims—as evidence.

## 1. Find the project and reporting window

1. Starting at the current directory, walk upward and select the nearest directory containing `AGENTS.md`, `CLAUDE.md`, and `docs/`. Treat it as `<project-root>`. Stop if no such root exists.
2. Read `<project-root>/AGENTS.md` and `CLAUDE.md` completely. Project instructions override generic defaults in this skill.
3. Resolve this skill's directory from the loaded `SKILL.md`, then run:

   ```bash
   python <skill-dir>/scripts/meeting_context.py --repo <project-root>
   ```

   Pass `--date YYYY-MM-DD` only when the user specifies a meeting date. With no date, use Thursday of the current ISO week in `Asia/Seoul`, even when Thursday is earlier or later than today.
4. Use `target_meeting` as `docs/meetings/mmdd_meeting.md`. If it already exists, update it carefully; never replace user edits blindly.
5. Compare against `previous_meeting`, the latest meeting strictly before the target date. If none exists, state that this is a baseline report rather than inventing a comparison.

## 2. Build a verified delta ledger

Read sources in this order unless the project policies prescribe a stricter sequence:

1. the previous meeting, the target meeting if it exists, and up to two additional recent meeting files;
2. the project's current-state, lesson/history, method/specification, roadmap, and survey documents under `docs/`;
3. Git log/diff/status over the reporting window;
4. relevant commands, logs, checkpoints, metrics, figures, qualitative artifacts, and running-process state;
5. a project-provided bounded agent-session audit when external agent work is part of the interval.

Use chat and meeting prose only as leads. For each candidate update, record privately:

- previous state;
- current state: completed, active, blocked, rejected, or planned;
- exact evidence path and protocol;
- whether the claim is verified, reported-only, inferred, or unknown;
- the resulting meeting section.

Resolve contradictions against primary artifacts. Do not expose private transcript content, secrets, or hidden reasoning. Do not turn archived code or stale meeting text into current project state.

## 3. Select material progress

Prioritize deltas that change the research story:

- method, architecture, or specification changes;
- decision-grade experiment outcomes and rejected hypotheses;
- the current bottleneck and its evidence;
- active work status, with measured progress/ETA separated from results;
- next experiments, decision gates, and expected interpretation.

Reconcile every prior TODO as completed, superseded, active, or still planned. Omit routine refactors and minor operational noise unless they affect validity, reproducibility, resource use, or the next decision.

Never present partial work, a diagnostic gate, or a missing evaluation bundle as a completed method verdict. If a verified material outcome is absent from the project's living docs, follow the documentation routing in `AGENTS.md`/`CLAUDE.md` in the same change or report the documentation blocker.

## 4. Assemble result evidence

Follow the project's experiment-completion contract. Unless the project requires more, a completed empirical result should include:

1. a control/baseline comparison table;
2. exact protocol, sample count, seeds/repetitions, budget, and uncertainty where applicable;
3. paired deltas when the design permits them;
4. a rendered quantitative figure;
5. representative qualitative evidence or the closest applicable diagnostic visualization, inspected before interpretation.

Derive metric names and directions from the current project evaluation specification; never inherit an old meeting's arrow blindly. If a required table, plot, or qualitative artifact is missing, label the result as awaiting presentation and state exactly what is absent. Do not fabricate a figure or use an unrelated sample.

## 5. Import and link figures

Use only genuine result artifacts. Convert or render each selected source to PNG before import, then run:

```bash
python <skill-dir>/scripts/meeting_assets.py import \
  --repo <project-root> --date YYYY-MM-DD --source /path/to/source.png \
  --alt "concise, specific description"
```

The command copies without overwrite to the next available `docs/figures/mmdd_fig#.png` and prints the Markdown link. Number figures in order of first appearance and inspect every imported image before drawing a verdict.

Use a normal Markdown image link from `docs/meetings/`:

```markdown
![specific description](../figures/mmdd_fig1.png)
```

Never emit unresolved placeholders, absolute local paths, or links to transient output directories.

## 6. Match the local house style

Read [references/meeting-style.md](references/meeting-style.md) before drafting. Use [assets/meeting-template.md](assets/meeting-template.md) as a flexible scaffold, not mandatory fixed sections.

Infer language, heading depth, terminology, equation density, table style, and status vocabulary from the recent meeting files. Preserve useful conventions while correcting malformed links, typos, and stale scientific claims.

Lead with what changed since the previous meeting. Preserve uncertainty and avoid inflated claims, diary narration, generic AI transitions, and repeated background already covered previously.

## 7. Validate and hand off

1. Write or update only `docs/meetings/mmdd_meeting.md` and required `docs/figures/mmdd_fig#.png` files, except for documentation synchronization required by the project policies.
2. Validate figure links and PNG files:

   ```bash
   python <skill-dir>/scripts/meeting_assets.py validate \
     --repo <project-root> --meeting docs/meetings/mmdd_meeting.md
   ```

3. Search for unresolved placeholders, stale statuses, unsupported superlatives, and metric-direction mistakes.
4. Inspect `git diff` without altering unrelated user changes.
5. Report the meeting path, comparison baseline, figure paths, evidence still missing, and any living-doc synchronization performed.

