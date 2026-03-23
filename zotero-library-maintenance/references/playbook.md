# Playbook

## Scope

This playbook is for local Zotero library maintenance using:
- local read API discovered from the running Zotero instance
- in-app write path: Zotero `Run JavaScript`

The local API is fast and complete enough for inventory, but writes are not supported. Do not plan around `PATCH` or local API mutation.

## Endpoint Discovery

Do not assume the port is fixed, even though `23119` is the common default.

Use one of these discovery paths:

1. Preferred, from inside Zotero `Run JavaScript`:
   - `Zotero.Prefs.get('connector.url')`
   - this typically returns a loopback URL with the active port
2. Outside Zotero, probe candidate bases and accept the first one whose `/api/` root responds with headers like:
   - `X-Zotero-Version`
   - `Zotero-API-Version`
3. Treat the common default ports as fallback candidates, not guarantees.

## User Library Discovery

For the local API, prefer the built-in local-user alias after discovery.

Why:
- Zotero's local API explicitly accepts `userID 0` as the alias for the logged-in local user
- the actual numeric user id may differ by machine/account

If you need the real numeric user id:
- inspect the returned item payload under `library.id`
- or inspect the `alternate` links in API responses

Use the real numeric id only when required by the task. Otherwise the local-user alias is the least fragile choice.

## Phase 1: Audit

Use the local API to compute:
- top-level non-attachment items without collections
- top-level attachments without parents
- top-level non-attachment items without `date`
- PDF attachments whose resolved storage path does not exist
- parent items whose best/oldest PDF child is missing while another PDF child exists

Prefer counting first, then sampling titles, then deciding whether a fix is safe enough to batch.

## Phase 2: Unfiled Top-Level Records

Order of operations:
1. Classify top-level non-attachment items into existing collections
2. Re-check `top_level_no_collection`
3. Handle top-level attachments only after top-level bibliographic items are clean

Collection rules:
- Reuse existing collections aggressively
- Keep each paper in exactly one collection
- Only suggest new collections if a whole thematic cluster does not fit existing buckets

## Phase 3: Standalone Attachments

Process standalone attachments in this order:

1. Exact-title match to existing parent items
2. High-similarity title match where the parent is clearly the same work
3. Zotero PDF recognition for files that are genuinely standalone and recognizable
4. Placeholder parent creation when recognition fails but the library still benefits from parent-child structure

Placeholder parent guidelines:
- Use `document` by default
- Upgrade to `book` when the title obviously denotes a book/manual/edition
- Copy collection membership from the attachment
- Use `pdfinfo` title/author/year if it is cleaner than the raw filename

## Phase 4: Missing Dates

Use a conservative policy.

Strong signals:
- arXiv URL or PDF path with paper ID -> infer year from YYMM
- ACL/ISCA/PMLR/OpenReview/official proceedings URL with explicit year
- exact OpenAlex or other primary-source metadata title match
- obvious edition/year in authoritative title

Do not fill dates when:
- the best external match is fuzzy
- multiple years compete with similar confidence
- the record is a generic webpage or ambiguous manual

Prefer `YYYY` unless the exact publication date is clearly supported.

## Phase 5: Broken PDF Opening

There are two dominant failure modes.

### Mode A: Broken duplicate child PDF blocks a good sibling

Symptoms:
- parent has multiple PDF children
- one or more are missing on disk
- at least one sibling PDF exists
- Zotero chooses the oldest PDF child, not necessarily the existing one

Safe fix:
- trash missing duplicate PDF children only when they have no child notes/annotations
- then re-check the parent's best attachment

### Mode B: Missing PDF child with recoverable source URL

Symptoms:
- attachment path is missing
- `linkMode` is `imported_url`
- attachment retains a direct PDF `url`

Safe fix:
- re-download to the exact storage path recorded by Zotero
- verify it is a PDF before replacing

Fallback:
- if the attachment URL is dead but the parent item has a trustworthy source URL, derive the PDF URL from the parent
- common patterns:
  - arXiv `/abs/` -> `/pdf/...pdf`
  - ISCA archive `.html` -> `.pdf`

### Residual cases

If a missing PDF attachment is:
- `imported_file` with no surviving copy elsewhere
- or a `linked_url` ResearchGate-style attachment

then do not pretend it is fixed automatically. These need manual source recovery or conversion into a plain webpage-style attachment.

## Phase 6: Mutation Method

Use Zotero internal JS from `Run JavaScript`.

Reliable write patterns:
- `item.setCollections([...])`
- `item.parentID = parent.id`
- `item.setField('date', '2024')`
- `item.deleted = true`
- `await item.saveTx({ skipDateModifiedUpdate: true })`

When batching:
- write logs to a temp JSON file for each batch
- re-audit after every meaningful batch
- keep each batch logically narrow so failures are easy to isolate
