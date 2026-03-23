# zotero-library-maintenance-skill

Public repo for the `zotero-library-maintenance` Codex skill plus a minimal `CLAUDE.md` adaptation.

Skill folder:
- [`zotero-library-maintenance/`](./zotero-library-maintenance/)

Notes:
- The skill assumes a local Zotero desktop app with the local API enabled.
- It does not hardcode a single endpoint; scripts discover the active local API base URL and use the local-user alias by default.

What this skill does not do:
- It is not a general-purpose Zotero plugin or GUI extension.
- It does not promise perfect metadata reconstruction for every damaged attachment.
- It does not fetch paywalled PDFs or defeat source-site access controls.
- It does not replace manual review for ambiguous duplicates, scanned books, or low-confidence metadata merges.
