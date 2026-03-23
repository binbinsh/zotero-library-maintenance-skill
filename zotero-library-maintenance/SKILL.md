---
name: zotero-library-maintenance
description: Use when auditing, organizing, de-duplicating, repairing, or metadata-cleaning a local Zotero library via the Zotero local API and Zotero's internal Run JavaScript tool. Covers endpoint discovery, unfiled top-level items, collection assignment, standalone attachment re-parenting, conservative year filling, and broken PDF diagnosis/repair.
---

# Zotero Library Maintenance

## Overview

Use this skill for high-leverage maintenance on a local Zotero library when the user wants structural cleanup, metadata cleanup, or attachment repair. It is optimized for the Zotero local API plus in-app mutation through Zotero's `Run JavaScript` window.

This skill assumes:
- Reads come from the local API after discovery of the local base URL
- Reads should prefer the local-user alias after verifying the local API
- Writes happen through Zotero internal JS, not the local API
- The safest default is to prefer existing parent items, existing collections, and reversible edits

## Workflow

1. Audit first.
2. Separate top-level problems from child-item problems.
3. Prefer reuse over creation.
4. Mutate in Zotero internal JS, then re-audit from the local API.
5. Treat broken-PDF repair as a separate pass from metadata cleanup.

Read [playbook.md](./references/playbook.md) for the detailed phase-by-phase workflow.

## Decision Tree

If the user is cleaning `Unfiled Items`:
- Start with top-level non-attachment items
- Then handle top-level attachments
- Ignore child notes/annotations unless the user explicitly wants them normalized

If the user reports missing years:
- Only patch high-confidence years
- Prefer `YYYY` over invented full dates
- Use URL/arXiv/ACL/OpenAlex style evidence before fuzzy web matches

If the user reports PDF open failures:
- Check whether the attachment path resolves inside Zotero
- Check whether the parent's best attachment points at a missing child
- Repair in this order:
  - trash missing duplicate PDF children when a good sibling exists
  - re-download missing `imported_url` PDFs from attachment URL
  - derive replacement PDF URLs from parent metadata when safe
  - for remaining standalone/odd cases, create or repair parent structure conservatively

## Key Rules

- Discover the local API base URL before assuming a port.
- Prefer the local-user alias for local API reads after discovery succeeds.
- Treat `top-level` and `child` items as different maintenance problems.
- Keep each paper in exactly one collection unless the user asks otherwise.
- Minimize new collections; prefer existing semantic buckets.
- For top-level attachments, first try to attach them to an existing parent item before creating a new parent.
- When creating placeholder parents, make the smallest truthful record you can: title, optional year, optional authors, item type.
- Do not trust Zotero's "best attachment" to imply file existence; verify the actual file path.
- Do not delete missing attachments if they have child notes/annotations; isolate those for manual review.

## Reading Order

- For library triage and repair workflow: read [playbook.md](./references/playbook.md)
- For maintenance heuristics and failure patterns: read [maintenance-patterns.md](./references/maintenance-patterns.md)
- For deterministic local audits: use [local_api_audit.py](./scripts/local_api_audit.py)
- For re-downloading missing `imported_url` PDFs from stored attachment URLs: use [redownload_missing_imported_url_pdfs.py](./scripts/redownload_missing_imported_url_pdfs.py)

## Typical Outputs

- A counts-based audit of unfiled parents, standalone attachments, missing dates, and broken PDFs
- A batch JS script to run inside Zotero
- A conservative mutation log
- A short residual-risk list for the items that still need manual handling
