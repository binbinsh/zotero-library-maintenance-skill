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

What this skill does not do:
- It does not guarantee authoritative bibliographic metadata for every attachment or scanned book.
- It does not bypass publisher paywalls, private file hosting restrictions, or expired signed URLs.
- It does not mutate Zotero through the local API; writes must go through Zotero internal JS.
- It does not automatically delete ambiguous missing attachments that may carry notes or annotations.

Detailed references:
- [`playbook.md`](./zotero-library-maintenance/references/playbook.md)
- [`maintenance-patterns.md`](./zotero-library-maintenance/references/maintenance-patterns.md)
