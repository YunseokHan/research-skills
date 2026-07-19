# Notion publishing

## Contents

- Destination and authority
- Project meeting database and stable identity
- Faithful body conversion and local meaning comments
- Figure transfer and safe upsert
- Read-back verification

Use this workflow only after the local meeting document and its PNG assets pass the skill's validation. The repository copy remains canonical; Notion is a presentation mirror.

## 1. Resolve configuration and authority

1. Treat an explicit request such as “publish this meeting to Notion” as authority to write only the named meeting to the named destination.
2. Use the installed Notion connector/MCP tools. Never request, print, store, or embed a Notion token in the repository or skill.
3. Resolve the destination in this precedence order: an explicit URL/ID in the current request; `MEETING_NOTION_PARENT_URL`; `NOTION_MEETING_PARENT_URL`; otherwise ask for a parent page URL. Resolve the project name from an explicit value, `MEETING_NOTION_PROJECT`, or the repository directory name. Environment variables are locators, not credentials; never store OAuth tokens there.
4. Run `python <skill-dir>/scripts/notion_destination.py --repo <project-root>` to normalize the available values. Pass `--parent` or `--project` when the current request supplies them explicitly. The script prints only non-secret destination metadata.
5. Fetch `self` and the resolved parent through the connector before any write. Confirm the connected workspace and that the parent is accessible. If the parent belongs to another workspace, stop and reconnect.
6. Inspect the destination before writing. Never overwrite the parent body or an unrelated entry.

## 2. Create or reuse the project meeting database

For a parent page destination, use exactly one inline/list database titled `<project>` unless the user names another title.

1. Search or fetch the parent's children for a case-insensitive exact project-title match.
2. Reuse a single match and preserve its existing schema. If multiple matches exist, stop and ask.
3. If absent, create the database under the parent with only these portable properties:
   - title property `Name`;
   - date property `Meeting date`;
   - rich-text property `Source`;
   - select property `Sync status` with `Synced` and `Partial` options.
4. Create a list view when the connector supports view creation; otherwise retain the default view and treat the schema and entries as authoritative.
5. If the supplied destination is already a database/data source, inspect its schema and map only compatible existing properties. Never create or rename its properties without separate authorization.

## 3. Choose a stable identity

Use the tuple `(project name, ISO meeting date, local source path)` as the logical identity. Use the page title:

```text
mmdd_meeting
```

Before creating anything, search/query within the selected project database for the exact title and meeting date, then inspect matches. Update the single matching skill-owned page. If there are multiple matches or an existing page appears manually curated and its ownership is unclear, stop and ask rather than guessing.

Place a compact provenance block near the top:

- project/repository name;
- meeting date;
- canonical local path such as `docs/meetings/mmdd_meeting.md`;
- source Git commit when available, plus an explicit `dirty worktree` label when applicable;
- publication timestamp;
- `Managed meeting mirror; local repository is canonical.`

Do not expose filesystem prefixes, tokens, private logs, hidden transcript content, or secrets. Use repository-relative paths only.

## 4. Convert the report faithfully

Preserve headings, paragraphs, bullets, numbered lists, equations, tables, captions, and status labels as closely as the connector supports. Do not rewrite scientific claims during publication.

Use this order:

1. title and provenance;
2. the complete validated meeting body;
3. figures next to their original captions/sections;
4. a short publication note only when a Notion limitation required a documented fallback.

Apply two presentation transformations without changing scientific content:

1. Convert every local Markdown blockquote group into a native Notion callout using the connector's enhanced-Markdown callout syntax. The Summary agenda is the required minimum, for example:

   ```markdown
   <callout icon="📌" color="gray_background">
   1. Adapter reuse
   2. Occlusion handling
   3. Encoding, schedule, temporal operator
   </callout>
   ```

   Do not leave any presentation block as a `/quote` block in Notion. Preserve the original block text and use one callout per contiguous local blockquote group.
2. Generate the transformed Notion body and local explanation mappings with:

   ```bash
   python <skill-dir>/scripts/meeting_assets.py notion \
     --repo <project-root> --meeting docs/meetings/mmdd_meeting.md
   ```

   Use the emitted `body` directly; it has already converted blockquotes to callouts and removed local `**의미.**` paragraphs. After the page content exists, use the Notion comment tool once per emitted `comments` mapping, set `selection_with_ellipsis` to the emitted heading anchor, and post the emitted `comment` text verbatim. Anchor each explanation to its own numbered heading rather than adding page-level comments or a separate explanation section.

For the skill-created database, set `Name=mmdd_meeting`, `Meeting date=YYYY-MM-DD`, `Source=docs/meetings/mmdd_meeting.md`, and `Sync status=Synced` or `Partial`. For a pre-existing project database, map only its verified compatible properties; the title alone is sufficient when no date/source properties exist.

| Meaning | Candidate property |
| --- | --- |
| page title | `Name` or title property |
| meeting date | `Date` |
| project | `Project` |
| publication state | `Status` = `Prepared` or the nearest existing option |
| repository source | `Source` |

Never create or rename database properties without a separate user request.

## 5. Handle figures without losing evidence

Attempt to upload each imported `docs/figures/mmdd_fig#.png` through the connector when local-file upload is supported. Otherwise use a stable, access-controlled URL already supplied by the project or user.

Do not use `file://` URLs, absolute filesystem paths, transient `outputs/` paths, or fabricated public links. If a required figure cannot be uploaded or linked durably:

1. publish the text only if the user authorized a partial publication or the connector write is safely reversible;
2. add a clearly labeled `Figures pending transfer` block listing the repository-relative asset names and captions;
3. report the page as partial, not complete.

If the project's completion contract requires visible figures, Notion synchronization is incomplete until those figures are present.

## 6. Upsert safely

- Prefer creating or updating the date-specific database entry under the selected project database.
- Update only a page previously created by this workflow or explicitly designated by the user.
- Preserve comments, discussions, manually added follow-ups, and unrelated blocks. If the connector cannot replace only the managed content safely, create a new revision page or ask the user instead of clearing the page.
- Do not create duplicate pages to recover from a failed update. Re-read the destination first because the write may have succeeded despite a timeout.
- Do not alter sharing, permissions, workspace settings, database schema, or page ownership.
- Before commenting, fetch the page with discussions and retrieve all block comments. Skip an exact existing explanation comment. If a skill-owned explanation comment exists but its text changed, do not create a contradictory duplicate: create a new revision page or ask the user, because the connector cannot safely edit or delete comments.
- If a heading comment cannot be anchored precisely, leave the local report complete, mark the Notion sync partial, and report the failed heading. Do not fall back to placing the explanation in the page body unless the user requests that fallback.

## 7. Verify after writing

Read the resulting page back through the connector and verify:

1. destination ID/URL and title;
2. meeting date and provenance block;
3. presence and order of every top-level section;
4. table headers and row counts for decision-critical tables;
5. figure count, captions, and durable accessibility;
6. absence of unresolved placeholders and local absolute paths.
7. every local blockquote group rendered as a callout rather than a quote;
8. one anchored explanation discussion per local `**의미.**` paragraph, with exact text and no duplicates.

If verification fails, make one bounded correction when the intended fix is unambiguous, then read back again. Otherwise stop and report the exact mismatch. Report success only with the verified Notion URL/reference, whether the action created or updated the page, and any fidelity limitations.
