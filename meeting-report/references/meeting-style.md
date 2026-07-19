# Research meeting writing style

## Contents

- Document opening and headings
- Voice and local meaning explanations
- Terminology and technical presentation
- Results, figures, and status language
- Final style check

Use the following compact briefing style by default. Override it only when the user explicitly selects a different format.

## Document opening

- First non-empty line: `# 1. Summary` or another short numbered noun phrase.
- No document-level title above section 1.
- No draft date, reporting-window disclaimer, comparison explanation, or boilerplate preface.
- Summary content: blockquoted numbered agenda only.

```markdown
# 1. Summary

> 1. Adapter reuse
> 2. Occlusion handling
> 3. Encoding, schedule, temporal operator
```

- Summary as a table of contents, not an executive summary of findings.
- Keep this as a blockquote in the local Markdown. The Notion publisher converts it, and any other local blockquote group, to a native callout.

## Headings

- Numbered hierarchy: `# 1.`, `## 1.1.`, `### 1.1.1.`.
- Short noun phrases: `Baseline`, `Results`, `Flow encoding`, `Active experiments`, `Research plan`.
- No questions, full sentences, or conversational headings such as `무엇이 바뀌었나` or `왜 실패했나`.
- No redundant heading such as the meeting date plus a second explanatory title.

## Voice

- Bullets and tables as the default unit of composition.
- Korean noun-ending fragments instead of repeated `~이다`, `~한다`, `~되었다` prose.
- One claim, observation, protocol element, or decision per bullet.
- Nested bullets for evidence decomposition, conditions, and decision branches.
- Paragraph prose only for a causal caveat that would become misleading when fragmented.
- Evidence before interpretation; verified result separated from hypothesis and pending work.
- No generic openings, lab-notebook narration, marketing adjectives, or repeated summary paragraphs.

Preferred:

```markdown
- ours의 spatial quality 부족 (FVD, CLIPSim)
- Gamma-companded encoding의 severe motion collapse
- 가장 유력한 원인: flow-interface calibration mismatch
```

Avoid:

```markdown
현재 결과를 살펴보면 ours의 spatial quality가 부족하다는 것을 확인할 수 있다.
우리는 gamma-companded encoding을 시도했지만 severe motion collapse가 발생했다.
```

## Local meaning explanations

- End every content-bearing numbered section or subsection with one prose paragraph in this exact form:

```markdown
**의미.** 이 비교는 단순히 지표의 우열을 보여주는 것이 아니라, 현재 병목이 motion 부족이 아닌 spatial appearance 보존에 있음을 구분하기 위한 근거다. 따라서 후속 실험은 motion dial보다 temporal operator가 frozen image prior를 얼마나 침범하는지에 초점을 둔다.
```

- Explain three things in one compact paragraph: what the preceding material establishes, how it changes the research interpretation, and what follow-up question or decision it supports.
- Write natural connected prose so the repository reader can ask a follow-up without reconstructing the table or bullets alone.
- Keep the explanation as the final direct paragraph under its heading and on one logical Markdown line; do not place bullets, figures, or another paragraph after it.
- Exempt `Summary`, `TODO`, `References`, and container headings that contain only child headings.
- Do not use the `**의미.**` paragraph as a second result summary or introduce unsupported evidence.
- Keep the paragraph in local Markdown. During Notion publication, remove it from the page body and post its exact text as a comment anchored to the corresponding numbered heading.

## Terminology

- Write for a collaborator who understands the research area but not repository-local aliases.
- Expand run tags and code nicknames into technical descriptions.
- Keep an internal alias only once in parentheses when needed to connect the document to an artifact.
- Prefer:
  - `16-frame self-routed video baseline` over an internal checkpoint tag
  - `frame-chunk autoregressive schedule` over a schedule nickname
  - `shared-timestep linear flow encoding` over an encoding/config alias
  - `gamma-companded flow encoding` over a bare encoding acronym
- Expand metric or control shorthand when its meaning is not obvious from the table header.

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
- Follow each table with one to four compact bullets covering the primary outcome and relevant trade-offs.
- Do not repeat the table row-by-row in prose.
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

## Final style check

- First line matching `# 1.`.
- Blockquoted numbered agenda in section 1.
- No preface or draft metadata.
- Short noun-phrase headings.
- Bullet-first body with minimal paragraph prose.
- One final `**의미.**` prose paragraph for every content-bearing numbered unit.
- No repeated Korean declarative `다.` endings outside the required meaning paragraphs.
- No unexplained run tags or code aliases.
- Table, figure, montage, protocol, and uncertainty retained despite compression.
