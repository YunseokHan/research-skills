# Research paper synchronization map

Use this map after identifying a verified research delta. Inspect all listed consumers and adapt filenames to the current manuscript structure.

| Research delta | Typical authoritative source | Paper consumers |
| --- | --- | --- |
| Central thesis or novelty boundary | current method/spec, relevant lesson and survey | facts ledger, title, abstract, introduction, related work, contribution list, conclusion, limitations |
| Architecture, algorithm, or mathematical operator | current method/spec, implementation, relevant lesson | facts ledger, method, theoretical appendix, setup appendix, diagrams, notation |
| Current training or execution recipe | current method/spec and run manifest | facts ledger, method recipe paragraph, reproducibility appendix, affected captions/tables |
| New headline result | current evaluation state and source artifact | facts/status ledgers, results prose, main table, abstract/introduction/conclusion when headline-relevant, limitations |
| Diagnostic or ablation | matching lesson/decision record and registered artifact | facts ledger with diagnostic scope, analysis/results, ablation table or additional-results appendix |
| Evaluation-protocol change | current evaluation specification and lesson | facts ledger, results setup, table captions, metric appendix, setup appendix, limitations |
| Adopted or rejected alternative | decision record and method/roadmap transition | facts ledger, current method if adopted, analysis or limitations if scientifically material; never raw run chronology |
| New prior-art boundary | verified primary sources, survey, novelty record | facts ledger, related work, contribution wording, bibliography, relevant limitations |
| Figure or qualitative verdict | source artifacts and visual inspection | facts ledger if claim-bearing, manuscript figure directory, relevant section/caption, appendix examples |

## Common section responsibilities

- Facts ledger: single paper claim boundary; no guessed results.
- Status ledger: short snapshot of manuscript maturity and missing evidence.
- Main assembly file: packages, macros, title, draft notice, and section assembly. Ensure `\codex` exists before using Codex comments.
- Abstract: problem, method, strongest supported result, bounded conclusion; no promised future gain.
- Introduction: motivation, gap, contributions, and headline evidence.
- Related work: fair nearest-neighbor positioning supported by verified citations.
- Method: current adopted method only; experimental branches appear only when clearly labeled and necessary.
- Results and tables: protocol-compatible evidence, uncertainty, baselines, and caveats.
- Analysis: valid diagnostics, controlled ablations, and claim-boundary analysis.
- Conclusion: supported takeaway and limitations, not a progress report.
- Reproducibility appendix: implementation details and budgets required by policy.
- Metrics appendix: definitions, directions, protocols, and known traps.
- Theory appendix: exact statements with assumptions matching the implementation.
- Additional-results appendix: secondary matched results and visual evidence.
- Limitations/future appendix: present limitations and non-guaranteed future directions.
- Bibliography: verified metadata only.

## Consistency checks

- A headline number should appear identically in the facts ledger, results prose, its table, and every headline mention.
- A recipe should use the same units and values in the current method/spec, facts ledger, method, and setup appendix.
- A pending experiment should remain pending everywhere; it must not appear as evidence in the abstract or conclusion.
- A superseded method should leave the current method rather than survive as a second active recipe in the paper.
- A diagnostic should retain its scope and must not be rephrased as whole-system superiority.
- After a full rewrite, every pre-rewrite claim, citation, label, figure, and limitation must be either preserved or deliberately retired in the synchronization ledger.

