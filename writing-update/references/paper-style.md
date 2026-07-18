# Research paper style

## Argument

- Give each paragraph one job: establish a problem, define a method, present evidence, or delimit a claim.
- Put the closest prior work and exact distinction near the claim, not in a vague later disclaimer.
- Anticipate the naive design's failure mode, then introduce the chosen mechanism as the principled response.
- Keep method motivation prospective. Reserve retrospective language for localized negative results and limitations.
- Prefer a precise narrow contribution over a broad claim weakened by caveats several paragraphs later.

## Voice

- Use direct technical prose with varied sentence length and match the manuscript's established language.
- Prefer concrete subjects and verbs over passive filler.
- Avoid generic AI prose: “notably,” “importantly,” “comprehensive,” “robust,” “novel paradigm,” “this underscores,” and repeated “Furthermore/Moreover.”
- Avoid symmetrical lists created only for rhetorical polish. Contributions should reflect the actual evidence hierarchy.
- Do not repeat the same result in adjacent paragraphs unless its argumentative role changes.
- Use confident wording for verified facts and calibrated wording for diagnostics, incomplete comparisons, and hypotheses.

## Claims

- “Guarantee” and “prove” require a statement whose assumptions match the implementation.
- “Causal” requires a valid intervention and controlled comparison; otherwise name the diagnostic.
- “State of the art,” “superior,” and “general” require protocol-matched evidence at the claimed scope.
- An isolated component property does not automatically establish whole-system behavior.
- An intervention diagnostic establishes response within that diagnostic, not accuracy or end-to-end quality unless separately measured.
- A single aggregate metric is not a complete verdict when project policy requires multiple quantitative and qualitative checks.

## Results prose

- State protocol before values when protocol determines comparability.
- Pair an improvement with its cost when objectives trade off.
- Distinguish absolute values, paired deltas, confidence intervals, and diagnostic thresholds.
- Explain why a baseline is relevant and disclose off-domain or unmatched settings immediately.
- Do not turn “interval spans zero” into equivalence unless an equivalence test was designed.

## LaTeX

- Reuse notation from the facts ledger and existing definitions.
- Keep table captions self-contained but shorter than the analysis paragraph.
- Use nonbreaking references (`Section~\ref{...}`, `Table~\ref{...}`).
- Introduce every equation and interpret it in prose.
- Preserve or deliberately remap labels during rewrites and update all references.
- Use `\codex{[PENDING: exact missing evidence or action]}` for actionable draft notes only.

## Final polish checklist

- Remove lab-notebook chronology from the main text.
- Remove duplicated motivation and conclusion sentences.
- Check antecedents of “this,” “it,” and “these results.”
- Replace vague scope words with concrete datasets, tasks, conditions, and protocols.
- Ensure every superlative and novelty statement has evidence or a verified citation.
- Ensure limitations are candid without presenting planned gains as inevitable.

