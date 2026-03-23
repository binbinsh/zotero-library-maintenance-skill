# Zotero Library Maintenance

Use the workflow in [`zotero-library-maintenance/SKILL.md`](./zotero-library-maintenance/SKILL.md) when working on a local Zotero library through `http://localhost:23119/api/`.

Preferred operating mode:
- audit first via the local API
- mutate through Zotero `Run JavaScript`
- verify every batch after writes

Main repair classes:
- unfiled top-level records
- standalone attachment re-parenting
- conservative year filling
- broken PDF diagnostics and recovery

Detailed references:
- [`playbook.md`](./zotero-library-maintenance/references/playbook.md)
- [`session-derived-patterns.md`](./zotero-library-maintenance/references/session-derived-patterns.md)
