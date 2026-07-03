---
title: "Knowledge Base Schema"
type: reference
---

# Knowledge Base Schema

This is the reference copy of the schema that defines conventions and workflows for the LLM-maintained knowledge base.

## Directory Structure

```
knowledge-base-root/
├── schema.md              # Conventions and workflows (this file)
├── raw/                   # Immutable source documents (human-curated)
│   └── *.md               # Source documents (articles, papers, notes)
└── wiki/                  # LLM-generated and maintained pages
    ├── index.md           # Content-oriented catalog of all pages
    ├── log.md             # Chronological append-only activity log
    ├── overview.md        # Top-level synthesis and navigation hub
    ├── entities/          # Entity pages — people, organizations, tools, books
    ├── concepts/          # Concept pages — ideas, principles, frameworks
    ├── comparisons/       # Comparison pages — side-by-side analyses
    └── questions/         # Answers filed as pages
```

## Workflows Reference

### Ingest Workflow

1. Read the source from `raw/`
2. Discuss key takeaways with the user
3. Create a **source summary page** at `wiki/concepts/` or `wiki/entities/`
4. Create/update relevant **entity pages**
5. Create/update relevant **concept pages**
6. Check for contradictions with existing wiki content — flag them
7. Update `wiki/overview.md` if the knowledge domain expands
8. Update `wiki/index.md` — add/update entries for all new and modified pages
9. Append entry to `wiki/log.md`

### Query Workflow

1. Read `wiki/index.md` to find relevant pages
2. Read those pages for context
3. Synthesize answer with citations to wiki pages and source documents
4. If the answer is valuable, offer to file it as a new wiki page
5. If accepted, create page under `wiki/questions/` and update index + log

### Lint Workflow

1. Scan for contradictions — same topic, conflicting claims
2. Identify stale claims — superceded by newer sources
3. Find orphan pages — no inbound links
4. Spot missing pages — important concepts mentioned but lacking dedicated page
5. Report findings with specific page references
6. Log the lint pass to `wiki/log.md`

## Output Formats

- **Markdown page** — default, stored in `wiki/`
- **Comparison table** — stored in `wiki/comparisons/`
- **Marp slides** — if user needs a presentation
- **Diagram** — Mermaid embedded in markdown
