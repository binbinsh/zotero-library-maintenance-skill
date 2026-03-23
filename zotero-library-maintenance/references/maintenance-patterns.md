# Maintenance Patterns

This reference captures practical patterns for Zotero library maintenance:
- collection assignment for unfiled top-level papers
- top-level attachment re-parenting
- conservative year completion
- broken PDF diagnosis and repair

## Patterns That Worked

### 1. Treat top-level attachments as a separate maintenance layer

Standalone attachments often represent:
- an already-cataloged paper duplicated as a top-level PDF
- an uncataloged paper that should be recognized
- a manual/book/document that needs a placeholder parent

Trying to solve them together with normal bibliographic items makes the workflow messy.

### 2. Prefer attaching to an existing parent over creating a new one

Exact or near-exact title matches resolved a large fraction of standalone PDF clutter with low risk.

### 3. Conservative year filling is worth it

The safe wins came from:
- arXiv IDs
- proceedings URLs with explicit years
- exact metadata matches

Fuzzy semantic web search caused too much noise.

### 4. Broken open behavior usually came from attachment selection, not the surviving file

Important finding:
- Zotero's best-attachment choice can still point at a missing PDF child
- the parent then appears "broken" even if a sibling PDF exists

Removing missing duplicates restored normal open behavior at scale.

### 5. Missing `imported_url` PDFs are high-value repair targets

If the attachment still remembers its source URL, bulk re-download is usually much faster than re-finding metadata manually.

## Patterns To Avoid

- Do not mutate through the local API; it is read-oriented.
- Do not assume a `linked_url` PDF behaves like a local stored PDF.
- Do not delete missing attachments blindly if they may carry notes/annotations.
- Do not assume `bestAttachment` implies file existence.
