---
name: writing-update
description: Synchronize, rewrite, revise, and polish an active LaTeX research manuscript in `docs/writing/` against the latest verified method/specification, results, recipe, prior-art boundaries, and paper facts. Use in projects whose root contains `AGENTS.md`, `CLAUDE.md`, and `docs/` when asked to update the paper after research progress, rewrite manuscript sections or the full draft, resolve paper/documentation drift, add verified citations or figures, or prepare a clean compiled draft or submission build.
---

# Writing Update

Update the paper as an evidence-preserving transaction. Keep `FACTS.md`, the manuscript, tables, appendices, bibliography, and compiled PDF mutually consistent.

## 1. Find the project and establish scope

1. Starting at the current directory, walk upward and select the nearest directory containing `AGENTS.md`, `CLAUDE.md`, and `docs/`. Treat it as `<project-root>`. Stop if no such root exists.
2. Read `<project-root>/AGENTS.md` and `CLAUDE.md` completely. Project instructions override generic defaults in this skill.
3. Inspect `git status` and preserve unrelated user edits.
4. Run the structural inventory before editing:

   ```bash
   python <skill-dir>/scripts/writing_audit.py --repo <project-root>
   ```

5. Read current research state in the order prescribed by project policy. In the common layout this is the lesson/index documents, relevant topic lessons, `docs/METHOD.md`, `docs/ROADMAP.md`, and relevant surveys.
6. Then read `docs/writing/FACTS.md`, `STATUS.md`, the manuscript assembly file, and every source file affected by the requested update.

Treat chat, meeting notes, and running-job reports only as leads. A paper claim requires primary evidence from the living docs and underlying metrics/logs/artifacts. Do not promote active or incomplete work into manuscript results.

## 2. Build the synchronization ledger

For every proposed change, record privately:

- authoritative source and evidence path;
- old paper statement;
- new verified statement;
- affected sections, tables, appendices, figures, and citations;
- claim status: confirmed, diagnostic, pending, limitation, or future work;
- protocol compatibility and uncertainty.

Read [references/paper-sync-map.md](references/paper-sync-map.md) to identify downstream consumers. Resolve contradictions before writing. Defer to the project's policy for which living document owns current method, experiment verdicts, future work, and paper claim boundaries.

## 3. Update in dependency order

1. **Living docs first.** If a material result or decision is not yet routed according to project policy, synchronize those docs before the manuscript.
2. **`FACTS.md`.** Update verified thesis, contributions, method, results, pending items, prior-art boundaries, and notation. Never infer a missing number.
3. **`STATUS.md`.** Record current draft state and unresolved evidence without duplicating the full facts ledger.
4. **Core narrative.** Revisit title, abstract, contribution order, introduction, method, analysis, conclusion, and limitations wherever new evidence changes emphasis or claim strength.
5. **Results and tables.** Keep prose, table values, captions, metric direction, uncertainty, and protocol caveats aligned.
6. **Implementation appendix.** Synchronize the reproducibility fields required by project policy, including budgets, optimization, schedules, conditioning, evaluation, and pinned revisions where applicable.
7. **Figures and bibliography.** Add only evidence-bearing figures and verified references.

Do not mechanically preserve the current tone after the evidence changes, and do not assume planned work will improve the method. Recalibrate the paper to the strongest defensible current account.

## 4. Choose local editing or a full rewrite

Use local edits when the argument and structure remain sound. A whole-file or full-manuscript rewrite is explicitly allowed when accumulated drift, inconsistent terminology, weak organization, or machine-generated prose makes piecemeal editing inferior.

Before a full rewrite:

1. freeze the synchronization ledger and enumerate every fact, result, citation, label, and limitation that must survive;
2. inspect user-authored uncommitted changes and preserve their intent unless contradicted by verified evidence;
3. retain or deliberately remap labels, cross-references, citations, equations, tables, and figure provenance;
4. compare the rewritten manuscript against `FACTS.md` section by section;
5. use the final diff to catch lost caveats or silently strengthened claims.

Permission to rewrite prose does not authorize inventing a new research decision, changing experimental evidence, or discarding unresolved limitations.

## 5. Enforce claim and evidence boundaries

- Preserve every distinction and prohibition defined by the current project's facts and evaluation policy.
- Distinguish diagnostic/internal evidence from protocol-matched headline results.
- State the protocol fields required by the project, including sample counts, repetitions/seeds, budgets, and uncertainty where applicable.
- Compare training or data budgets in the units required by project policy.
- Keep protocol mismatches, off-domain settings, small samples, and metric traps explicit.
- Require the project's result-completion bundle before treating an experiment as complete.
- Keep pending work pending; never replace placeholders or annotations with guessed values.
- Scope conclusions to the evaluated datasets, tasks, conditions, and protocols.

For a new novelty or related-work claim, verify primary papers/code online, update project-mandated surveys or lessons first, and then add verified BibTeX metadata. Never cite from memory or use a search snippet as evidence.

## 6. Write like a mature research paper

Read [references/paper-style.md](references/paper-style.md) before changing prose.

Frame design choices by anticipating the failure mode they address, not as lab chronology. Use direct, compact paragraphs with one argumentative job each. Remove generic transitions, repeated summaries, inflated adjectives, and formulaic claims unsupported by evidence.

Preserve established notation and LaTeX semantics. Local edits are not preferred categorically over full rewrites; choose the mode that yields the clearest coherent manuscript while satisfying the rewrite safeguards above.

## 7. Create and use the Codex comment command

Before inserting a Codex editorial comment, search the manuscript preamble for an existing `\codex` definition. Reuse it if present and never define it twice.

If `\codex` is absent:

1. ensure the color package used by the manuscript is loaded; add `\usepackage{xcolor}` when no compatible color package is present;
2. add the following definition in the preamble near other draft-annotation commands:

   ```tex
   \long\def\codex#1{{\color{blue}#1}}
   ```

3. compile immediately to confirm the definition and package order are valid.

Use `\codex{...}` only for a necessary Codex editorial comment or unresolved working-draft note. Do not write Codex comments with another agent's command. Comments must identify the missing evidence or required decision precisely; they are not a place to hide a paper claim. Remove all draft comments for a submission build.

## 8. Update figures, tables, and citations safely

- Store manuscript-owned figures under `docs/writing/figs/` with stable descriptive names unless project policy specifies another path.
- Trace every figure and table to a reproducible artifact and matched protocol.
- Inspect qualitative figures before describing them.
- Keep captions self-contained and state protocol caveats when they affect interpretation.
- Preserve or deliberately remap labels and update every textual reference after a rewrite.
- Check every citation key against the bibliography; verify author, title, venue, year, and stable identifier from a primary source.
- Do not edit conference style files, generated LaTeX auxiliaries, or template examples unless the user explicitly requests template maintenance.

## 9. Compile and validate

After editing:

1. Run the structural audit. A stale PDF is expected before compilation:

   ```bash
   python <skill-dir>/scripts/writing_audit.py --repo <project-root>
   ```

2. Run the compile command defined by project policy. In the common layout:

   ```bash
   bash scripts/compile_paper.sh
   ```

   Inspect output text, not only the exit code. Require zero undefined citations, zero undefined references, and zero missing bibliography entries.
3. Rerun:

   ```bash
   python <skill-dir>/scripts/writing_audit.py --repo <project-root> --require-fresh-pdf
   ```

4. Inspect the LaTeX log for new overfull boxes or material warnings.
5. Render and visually inspect affected PDF pages, especially after a full rewrite or changes to layout, tables, equations, or figures.
6. Cross-check every changed number and claim against `FACTS.md` and primary evidence, then inspect the final diff.

Use `--submission` only when the user explicitly requests submission-ready cleanup:

```bash
python <skill-dir>/scripts/writing_audit.py --repo <project-root> --submission --require-fresh-pdf
```

Submission mode forbids draft annotations and pending markers. A normal working draft may retain precise `\codex{[PENDING: ...]}` notes.

## 10. Hand off the update

Report:

- changed manuscript files and the research delta they encode;
- whether editing was local or a full rewrite, and how facts/labels/citations were preserved;
- facts/results/recipe synchronized;
- claims narrowed, strengthened, or left pending;
- citations and figures added or changed;
- compile/audit status and remaining warnings;
- unresolved evidence that prevented a complete update.

Do not describe the paper as synchronized if its facts ledger, prose, tables, appendices, or PDF still disagree.

