---
name: meeting-report
description: Create or update compact, evidence-backed weekly research meeting briefs with local follow-up explanations, organize meeting figures, and optionally mirror the validated report into a project-specific Notion database using callouts and section-anchored explanation comments. Use in projects whose root contains `AGENTS.md`, `CLAUDE.md`, and `docs/`, especially when asked to prepare or refresh `docs/meetings/mmdd_meeting.md`, report progress since the last meeting, organize `docs/figures/mmdd_fig#.png`, create a reusable Notion meeting archive, or explicitly publish meeting material to Notion.
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

Use the compact briefing contract below unless the user explicitly requests another format:

1. Make the first non-empty line `# 1. <short noun phrase>`. Do not add a document title, draft timestamp, reporting disclaimer, or introductory preface.
2. Use `# 1. Summary` as a blockquoted numbered agenda. List only the topics to be discussed; do not place findings or narrative in the summary.
3. Number every section and subsection. Use short noun-phrase headings such as `Baseline`, `Adapter reuse`, or `Flow encoding`; never use a question or sentence as a heading.
4. Prefer bullets and tables over paragraphs. In Korean, end bullets with nouns or compact fragments rather than `~이다`, `~한다`, or lab-notebook narration. Reserve prose for a caveat that cannot remain precise as a fragment.
5. Follow a table with only the few bullets needed to state the result and trade-off. Do not restate every cell in prose.
6. Rewrite repository-local run tags, aliases, and shorthand into reader-facing technical names. For example, prefer `16-frame self-routed video baseline` over an internal checkpoint tag, `frame-chunk autoregressive schedule` over a schedule nickname, and `gamma-companded flow encoding` over a bare encoding acronym. Retain an internal alias once in parentheses only when required for artifact provenance.
7. Keep protocol, sample count, uncertainty, status, and decision boundaries explicit even when compressing the wording.
8. End every content-bearing numbered section or subsection with one local prose paragraph beginning `**의미.**`. Explain what the preceding evidence establishes, how it changes the research interpretation, and which follow-up question it enables. Exempt `Summary`, `TODO`, `References`, and container headings with no direct body. Keep this paragraph in the repository Markdown even when the Notion mirror moves it into a comment.

Infer language, heading depth, equation density, table style, and status vocabulary from recent accepted meeting files without weakening this contract. Preserve useful conventions while correcting malformed links, typos, stale scientific claims, and unexplained internal terminology.

Lead with what changed since the previous meeting. Preserve uncertainty and avoid inflated claims, diary narration, generic AI transitions, and repeated background already covered previously.

## 7. Validate and hand off

1. Write or update only `docs/meetings/mmdd_meeting.md` and required `docs/figures/mmdd_fig#.png` files, except for documentation synchronization required by the project policies.
2. Validate figure links and PNG files:

   ```bash
   python <skill-dir>/scripts/meeting_assets.py validate \
     --repo <project-root> --meeting docs/meetings/mmdd_meeting.md
   ```

   Validation also requires one final `**의미.**` paragraph for every content-bearing numbered unit.
3. Preview the exact Notion comment mapping when publication is requested:

   ```bash
   python <skill-dir>/scripts/meeting_assets.py comments \
     --repo <project-root> --meeting docs/meetings/mmdd_meeting.md
   ```

   Treat the emitted heading, selection anchor, and explanation as a stable mapping. Do not paraphrase the explanation during publication.
   Generate the publication body and comment mappings together before writing:

   ```bash
   python <skill-dir>/scripts/meeting_assets.py notion \
     --repo <project-root> --meeting docs/meetings/mmdd_meeting.md
   ```

   Use the emitted `body` and `comments` rather than manually reformatting the local document.
4. Search for unresolved placeholders, stale statuses, unsupported superlatives, metric-direction mistakes, sentence-like headings, and unexplained repository-local aliases. Apply the noun-ending rule to bullets; allow natural declarative prose inside `**의미.**` paragraphs.
5. Inspect `git diff` without altering unrelated user changes.
6. Report the meeting path, comparison baseline, figure paths, evidence still missing, and any living-doc synchronization performed.

## 8. Optionally publish to Notion

Keep the validated local meeting Markdown and imported PNGs as the canonical research record. Publish to Notion only when the user explicitly requests it; preparing a meeting report alone does not authorize an external write.

When Notion publication is requested, read [references/notion-publishing.md](references/notion-publishing.md) completely and follow it after local validation. Resolve the parent with `scripts/notion_destination.py` from an explicit request, repository environment, or interactive clarification. Under a parent page, reuse or create one list database whose title is the project name, then upsert one `mmdd_meeting` page per local report. Match an existing project title case-insensitively before creating anything. Convert every local blockquote group—including the Summary agenda—to a native Notion callout, omit each local `**의미.**` paragraph from the Notion page body, and attach its exact prose as a comment on the corresponding numbered heading. Use the available Notion connector rather than direct HTTP or stored credentials, preserve content and comments outside the skill-owned page, and read both the page and its discussions back before reporting success.

If the Notion connector is unavailable, authentication is incomplete, the destination is ambiguous, or required figures cannot be transferred or linked durably, finish the local report and describe Notion publication as blocked or partial. Never silently omit evidence or claim that publication completed.
