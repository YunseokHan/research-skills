# {{PROJECT_NAME}} — code structure

## Active tree

```text
{{PACKAGE_NAME}}/
  [document actual active package layout]
scripts/
configs/
tests/
```

## Placement and ownership rules

- [Where model/data/evaluation/training logic belongs]
- [What may live at the package root]
- [Where package-local helpers and shared metrics belong]
- [How archived code is excluded from the active import closure]

## Stable entrypoints

| Task | Module/command | Config | Output contract |
|---|---|---|---|
| [task] | [command] | [config] | [artifacts] |

## Execution and monitoring

[Common dispatcher, orchestrators, watchers, manifests, DONE/FAILED contract, retry policy.]

## Archive and compatibility shims

[Archived paths, why inactive, any temporary forwarding commands, and removal conditions.]
