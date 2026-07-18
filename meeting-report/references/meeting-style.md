# Research meeting writing style

Use the recent files in `docs/meetings/` as the live stylistic reference. This guide captures common research-meeting conventions while excluding broken placeholders and stale claims.

## Structure

- Start directly with the first substantive numbered topic when neighboring documents do so; avoid boilerplate executive-summary headings.
- Match the local heading hierarchy, commonly `# 1.`, `## 1.1.`, and `### 1.1.1.`.
- Separate major sections with `---` only when it improves scanning.
- Let the content determine section names. A useful progression is current thesis → changed method → results → bottleneck → next steps.
- End with the TODO/Future Works/Next Steps form used by neighboring documents.

## Voice

- Match the language of recent meetings. Retain domain-specific English terms when the project already uses them.
- Prefer short declarative sentences and compact bullets.
- State evidence first and place interpretation immediately afterward.
- Use the project's established conclusion marker, such as `⇒`, only for evidence-supported consequences.
- Be confident about verified facts and explicit about incomplete evidence.
- Avoid generic openings, marketing adjectives, and repeated summary paragraphs.
- Do not imitate typos, malformed HTML/editor exports, or stale notation from old meetings.

## Technical presentation

- Introduce a symbol immediately before its equation.
- Use display math for a core objective or transformation, not decorative derivations.
- Use fenced monospace diagrams only when structure or execution order is clearer visually.
- Put units, budget, sample count, repetitions/seeds, and protocol near the result table.
- Bold decisive values or phrases sparingly.
- Derive metric direction (`↑` or `↓`) from the current evaluation specification.

## Results

- Compare against the previous meeting's accepted control or current canonical baseline.
- Keep protocol-matched arms in one table and separate incompatible protocols.
- Report uncertainty where available; use `—` rather than inventing a missing value.
- Follow each table with a compact interpretation covering the primary outcome and relevant trade-offs.
- Do not call an experiment complete without the evidence bundle required by the project policies.

## Figures

- Store meeting-owned PNGs as `docs/figures/mmdd_fig#.png`.
- Link from a meeting as `![specific description](../figures/mmdd_fig#.png)`.
- Put each figure close to the paragraph or table it supports.
- Alt text should identify the compared conditions and view.
- Never use an image from another protocol merely because it looks representative.

## Status language

Use the vocabulary established by neighboring meetings. If the project writes in Korean, useful precise states include:

- `완료`: the required evidence bundle is present.
- `진행 중`: work is live; provide progress/ETA but no outcome claim.
- `발표 자료 대기`: computation may be finished, but required presentation evidence is incomplete.
- `기각`: the registered decision rule is met and the evidence bundle is complete.
- `계획`: no result exists yet.

