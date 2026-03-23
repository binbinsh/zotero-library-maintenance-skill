# Zotero Library Maintenance Skill

`zotero-library-maintenance` is a Codex/Claude-oriented maintenance skill for local Zotero libraries.

It is designed for high-leverage cleanup work on a running Zotero desktop app, especially when a library has accumulated:
- unfiled top-level items
- standalone PDF attachments
- broken parent/attachment structure
- missing years on otherwise useful records
- PDF attachments that no longer open because the stored file is missing or Zotero selects a broken duplicate

This repo contains:
- a Codex skill in [`zotero-library-maintenance/`](./zotero-library-maintenance/)
- a lightweight Claude adaptation in [`CLAUDE.md`](./CLAUDE.md)
- a small set of local audit and repair scripts

## What This Skill Is For

Use this skill when you have a local Zotero library and want to:
- audit structural problems before editing anything
- assign top-level records to collections conservatively
- attach standalone PDFs to existing parent items when possible
- create minimal placeholder parents when recognition fails but hierarchy still matters
- fill years only when the evidence is strong
- diagnose and repair broken PDF opening behavior

The skill assumes a local Zotero desktop app with the local API enabled.

## What This Skill Is Not

- It is not a general-purpose Zotero plugin or GUI extension.
- It does not write through the Zotero local API; mutations happen through Zotero internal JavaScript.
- It does not guarantee perfect bibliographic metadata recovery for every attachment, scan, or manual.
- It does not bypass paywalls, private hosting, expired signed URLs, or access-controlled PDF sources.
- It does not replace manual review for ambiguous duplicates, low-confidence metadata merges, or attachments that carry notes or annotations.

## How It Works

The skill uses two channels:

1. Read path:
   - Zotero local API
   - endpoint discovery instead of assuming a fixed host/port
   - local-user alias by default

2. Write path:
   - Zotero internal `Run JavaScript`
   - batch-safe edits with explicit logging and re-audit after each phase

The workflow is intentionally conservative:
- audit first
- separate top-level and child-item problems
- prefer reuse over creation
- only batch-delete broken duplicates when a good sibling exists

## Quick Start

### 1. Discover the local API endpoint

```bash
python3 zotero-library-maintenance/scripts/discover_local_api.py
```

Expected output is a JSON object with:
- `base_url`
- `user_alias`
- `resolved_user_id`

### 2. Run a read-only audit

```bash
python3 zotero-library-maintenance/scripts/local_api_audit.py
```

This reports counts for:
- top-level unfiled records
- top-level attachments
- top-level records missing dates
- PDF attachments whose stored file is missing

### 3. Repair recoverable `imported_url` PDF attachments

```bash
python3 zotero-library-maintenance/scripts/redownload_missing_imported_url_pdfs.py
```

This only targets:
- PDF attachments
- with `linkMode=imported_url`
- whose local storage file is missing
- and whose original attachment URL is still available

## Repository Layout

```text
zotero-library-maintenance-skill/
├── README.md
├── CLAUDE.md
├── LICENSE
└── zotero-library-maintenance/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── playbook.md
    │   └── maintenance-patterns.md
    └── scripts/
        ├── discover_local_api.py
        ├── zotero_discovery.py
        ├── local_api_audit.py
        └── redownload_missing_imported_url_pdfs.py
```

## Key Documents

- [`SKILL.md`](./zotero-library-maintenance/SKILL.md)
  Core trigger rules and condensed workflow.

- [`playbook.md`](./zotero-library-maintenance/references/playbook.md)
  Detailed operational workflow for collection cleanup, attachment re-parenting, year filling, and broken PDF repair.

- [`maintenance-patterns.md`](./zotero-library-maintenance/references/maintenance-patterns.md)
  Practical heuristics and failure patterns distilled into reusable rules.

## Script Notes

### `discover_local_api.py`

Discovers the active local Zotero API endpoint and the preferred local-user alias.

### `local_api_audit.py`

Performs a read-only audit of the local library. By default it discovers the endpoint first.

### `redownload_missing_imported_url_pdfs.py`

Attempts to restore missing local PDF files for attachments that still retain their original source URL.

### Script Configuration

All scripts support explicit overrides when needed:

```bash
python3 ... --base-url http://127.0.0.1:23119 --user-id 0
```

They also respect:
- `ZOTERO_BASE_URL`
- `ZOTERO_USER_ID`

If not provided, they discover the local endpoint first.

## Typical Maintenance Tasks Covered

- Clean up `Unfiled Items`
- Re-parent top-level PDFs under existing items
- Build minimal parent items for otherwise orphaned attachments
- Fill missing years conservatively
- Diagnose why double-clicking a parent item fails to open a PDF
- Remove missing duplicate PDF children when a good sibling already exists
- Re-download missing stored PDFs from recoverable source URLs

## Portability

This repo intentionally avoids machine-specific assumptions in public-facing docs:
- no hardcoded absolute local filesystem paths
- no fixed public user id assumption
- no requirement that the Zotero API always runs on one fixed port

The discovery helper keeps the workflow portable across machines where Zotero is configured differently.

## Validation

The skill structure is validated with Codex's skill validator and the repository is intended to remain lightweight and procedural rather than framework-heavy.

## Using It With Codex or Claude

- Codex: use the skill folder directly as a Codex skill
- Claude: use [`CLAUDE.md`](./CLAUDE.md) as the project-level instruction entry point

The repository is intentionally small enough to be read end-to-end before use.
