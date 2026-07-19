# Research Skills for Codex

Reusable Codex skills for maintaining research repositories as durable research
systems: code, living documentation, experiment execution, evidence, meetings,
and manuscripts stay synchronized instead of drifting across chats and ad-hoc
scripts.

These skills are project-agnostic. They transfer workflow and research discipline,
not CTSA-specific methods, servers, datasets, metrics, or conference templates.

## Included skills

| Skill | Use it when you need to… | Main output |
|---|---|---|
| [`refactor-research-repo`](refactor-research-repo/) | audit and migrate an existing research repository into a sustainable code/docs/scripts layout | a behavior-preserving repository refactor, living-document ownership, and Codex–Claude governance |
| [`meeting-report`](meeting-report/) | prepare a compact weekly research update from verified repository evidence | `docs/meetings/mmdd_meeting.md`, organized figures, and optional Notion publication |
| [`writing-update`](writing-update/) | synchronize or rewrite an active LaTeX paper after the method, results, recipe, or claim boundary changes | updated paper facts, sections, tables, references, figures, and compiled draft |

Each skill is a self-contained directory with a required `SKILL.md` and optional
scripts, references, templates, and UI metadata.

## Install with Codex

The easiest option is to ask Codex to use its built-in skill installer:

```text
Install the following Codex skills from YunseokHan/research-skills:
- refactor-research-repo
- meeting-report
- writing-update

Use the skill-installer workflow, verify every SKILL.md after installation, and
tell me when the skills will become available.
```

To install only one skill, name only that directory. For example:

```text
Install the refactor-research-repo skill from
https://github.com/YunseokHan/research-skills/tree/main/refactor-research-repo
```

Codex's installer normally makes an installed skill available on the next turn.
Start a new turn or restart the Codex surface if it does not appear immediately.

## Manual installation

Codex supports global skills for one user and repository-local skills for one
project. The current official locations are documented in the
[Codex customization guide](https://developers.openai.com/codex/concepts/customization#skills).

### Global installation

Clone once and symlink the skills you want into `~/.agents/skills`:

```bash
git clone https://github.com/YunseokHan/research-skills.git ~/.local/share/research-skills
mkdir -p ~/.agents/skills
ln -s ~/.local/share/research-skills/refactor-research-repo ~/.agents/skills/refactor-research-repo
ln -s ~/.local/share/research-skills/meeting-report ~/.agents/skills/meeting-report
ln -s ~/.local/share/research-skills/writing-update ~/.agents/skills/writing-update
```

Install only the directories you plan to use. If your Codex distribution uses
`$CODEX_HOME/skills` (commonly `~/.codex/skills`) as its installer-managed skill
root, use that location instead or let the built-in installer choose it.

### Repository-local installation

Use a submodule when a team wants to pin the exact skill revision:

```bash
git submodule add https://github.com/YunseokHan/research-skills.git .research-skills
mkdir -p .agents/skills
ln -s ../../.research-skills/refactor-research-repo .agents/skills/refactor-research-repo
ln -s ../../.research-skills/meeting-report .agents/skills/meeting-report
ln -s ../../.research-skills/writing-update .agents/skills/writing-update
git add .gitmodules .research-skills .agents/skills
```

Repository-local installation is preferable when the workflow is part of the
project's reproducibility contract. Global installation is preferable when the
same researcher uses the workflow across many repositories.

## Verify the installation

At minimum, confirm that each installed directory contains its manifest:

```bash
test -f ~/.agents/skills/refactor-research-repo/SKILL.md
test -f ~/.agents/skills/meeting-report/SKILL.md
test -f ~/.agents/skills/writing-update/SKILL.md
```

Then ask Codex:

```text
List the installed research skills and summarize when each one should trigger.
```

If a skill is not discovered, check the installation root, the symlink target,
and the YAML frontmatter at the top of its `SKILL.md`, then begin a new Codex turn.

## How to use the skills

Invoke a skill explicitly with `$skill-name`. Codex may also select it implicitly
when your request matches the description in `SKILL.md`, but explicit invocation
is preferable for consequential repository work.

### Refactor a research repository

```text
$refactor-research-repo

Audit this repository and refactor it into a sustainable research layout. Preserve
scientific behavior and history. First show me the source-to-target map and the
policy-transfer ledger; do not copy server- or project-specific literals from the
reference repository.
```

This skill installs distinct owners for current method, future plans, resolved
lessons, code structure, meetings, surveys, and optional paper artifacts. It also
transfers generally applicable execution, evaluation, provenance, shared-compute,
and Codex–Claude supervision rules while parameterizing target-specific details.

### Prepare a meeting report

```text
$meeting-report

Prepare this week's research meeting brief by comparing against the previous
meeting. Use verified results, include quantitative and qualitative evidence, and
save the canonical report under docs/meetings/.
```

To publish the validated report to Notion, request it explicitly:

```text
$meeting-report

Prepare this week's meeting brief and publish the validated version to the
project's configured Notion meeting database.
```

Notion publication requires an available and authorized Notion connector plus a
configured destination. Local Markdown remains canonical.

### Synchronize a paper

```text
$writing-update

Synchronize docs/writing with the latest verified method, experiment decisions,
recipe, and claim boundaries. Update FACTS.md first, preserve venue-owned files,
and compile and audit the resulting PDF.
```

The skill does not promote running experiments or unsupported expected gains into
paper claims.

## Expected project structure

The skills are most effective in repositories with durable project instructions
and living documents, for example:

```text
AGENTS.md
CLAUDE.md
docs/
  METHOD.md
  ROADMAP.md
  LESSON.md
  CODE_STRUCTURE.md
  lessons/
  meetings/
  surveys/
  figures/
  writing/        # optional; only when a real manuscript exists
scripts/
tests/
```

`refactor-research-repo` can create and populate the missing structure without
overwriting existing policy files. The meeting and writing skills expect the
repository's instructions to identify authoritative evidence and project-specific
commands.

## Updating

For a clone-and-symlink installation:

```bash
git -C ~/.local/share/research-skills pull --ff-only
```

For a pinned submodule installation:

```bash
git submodule update --remote --merge .research-skills
git add .research-skills
```

For an installer-managed copy, ask Codex to inspect the installed version and
perform a safe update. The installer may refuse to overwrite an existing skill;
do not delete a locally modified skill without reviewing its diff first.

## Safety and trust

- Read a skill's `SKILL.md` and inspect its scripts before first use.
- Repository `AGENTS.md` and user instructions take precedence over generic skill
  defaults.
- Preserve dirty-worktree changes and review generated Git diffs.
- Keep credentials, machine-local paths, private transcripts, datasets, and large
  generated artifacts out of this repository.
- Treat chat reports as leads; verify consequential claims against primary
  artifacts and project state.

## Development and validation

Each skill can be validated with Codex's bundled skill validator:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py refactor-research-repo
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py meeting-report
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py writing-update
```

Also run the skill-specific scripts or dry runs documented in each `SKILL.md`.
Changes should remain project-agnostic and must not introduce reference-project
paths, credentials, datasets, compute topology, or venue assumptions.
