# Zotero Library Maintenance

Use the workflow in [`zotero-library-maintenance/SKILL.md`](./zotero-library-maintenance/SKILL.md) when working on a local Zotero library through the local Zotero API after endpoint discovery.

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
- [`maintenance-patterns.md`](./zotero-library-maintenance/references/maintenance-patterns.md)
