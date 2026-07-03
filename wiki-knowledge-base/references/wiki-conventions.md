# Wiki Page Conventions

Every wiki page in the knowledge base MUST follow these formatting rules.

## YAML Frontmatter

Every page opens with:

```yaml
---
title: "Page Title"
type: concept | entity | comparison | question | source-summary | overview | index | log
tags: [tag1, tag2, tag3]
sources: [raw/source-file.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Required fields

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Page title in Title Case | `"Go Coding Standards"` |
| `type` | Page category (see types below) | `concept` |
| `tags` | Lowercase, hyphenated keywords | `[go, coding-standards]` |
| `created` | ISO date of first creation | `2026-07-01` |
| `updated` | ISO date of last modification | `2026-07-01` |

### Optional fields

| Field | Description | Example |
|-------|-------------|---------|
| `sources` | Raw source files this page draws from | `[raw/llm-wiki.md]` |

### Page types

| type | Directory | Purpose |
|------|-----------|---------|
| `concept` | `wiki/concepts/` | Ideas, principles, frameworks, methodologies |
| `entity` | `wiki/entities/` | People, organizations, tools, books, products |
| `comparison` | `wiki/comparisons/` | Side-by-side analysis of 2+ concepts |
| `question` | `wiki/questions/` | Answers to specific questions filed as pages |
| `source-summary` | `wiki/concepts/` or root | Summary of an ingested source document |
| `overview` | `wiki/` | Navigation hub page |
| `index` | `wiki/` | Content catalog |
| `log` | `wiki/` | Activity log |

## Page Structure

After frontmatter:

1. **H1 title** — matches frontmatter `title`, one `#` header
2. **One-line summary** — immediately after title, explains what this page covers
3. **Body sections** — `##` and `###` headers, organized logically
4. **Cross-references** — see below

## Wikilinks

Use Obsidian-compatible wikilinks for internal references:

```markdown
[[path/to/page.md|Display Text]]
```

- Use **relative paths from the wiki root** (e.g., `concepts/rag.md` not `../../../somewhere`)
- Always provide **display text** for readability
- Content pages should link to at least **2 other wiki pages**
- The `overview.md` and `index.md` are hubs — link generously

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Page filenames | lowercase, hyphens | `llm-wiki.md`, `go-coding-standards.md` |
| Page titles (frontmatter) | Title Case, descriptive | `"LLM Wiki"`, `"Go Coding Standards"` |
| Tags | lowercase, single-word or hyphenated | `go`, `knowledge-management` |
| Directory names | lowercase, plural nouns | `concepts/`, `entities/`, `comparisons/` |

## Content Principles

1. **Synthesize, don't copy** — Wiki pages should extract and structure knowledge, not reproduce source text
2. **One topic per page** — If a page covers two distinct topics, split it
3. **Link over duplicate** — If information exists elsewhere, link don't repeat
4. **Explain why, not just what** — Context and rationale matter more than raw facts
5. **Use tables for structured data** — Rules, checklists, comparisons belong in tables
6. **Keep summaries concise** — The index.md one-line summary should tell whether to open the page

## File Structure of the Knowledge Base

```
root/
├── schema.md                 # Conventions + LLM workflow config
├── raw/                      # Immutable sources
│   └── source-name.md
└── wiki/                     # LLM-generated content
    ├── overview.md           # Top-level navigation hub
    ├── index.md              # Full-page catalog with summaries
    ├── log.md                # Chronological activity log
    ├── concepts/             # Idea/framework pages
    ├── entities/             # Person/tool/org pages
    ├── comparisons/          # Comparison pages
    └── questions/            # Filed answers
```

## index.md Format

Table-based catalog, grouped by category:

```markdown
## 🧠 Concepts
| Page | Summary |
|------|---------|
| [[concepts/topic.md\|Topic]] | One-line summary |
```

## log.md Format

Append-only chronological entries:

```markdown
## [YYYY-MM-DD] operation | Short Title
- Created: page1, page2
- Updated: page3
- Contradictions found: none | list
- Key takeaways: bullet points
```
