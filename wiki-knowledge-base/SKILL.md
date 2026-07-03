---
name: wiki-knowledge-base
description: >
  This skill maintains a local LLM-driven personal knowledge base using the LLM Wiki methodology.
  It supports two modes: INGEST ("存入wiki知识库") to extract knowledge from source documents into
  structured wiki pages, and QUERY ("检索wiki") to search the wiki and answer questions with citations.
  On first use, it asks for the knowledge base directory, auto-creates the structure if needed, and
  persists the location for future sessions. Always reports the KB location after each task.
  This skill should be used when the user says keywords like "存入wiki知识库", "存入wiki", "检索wiki",
  "搜索wiki", "wiki查询", or when the user wants to add knowledge to or search a local wiki knowledge base.
---

# Wiki Knowledge Base

Maintain a local, LLM-driven personal knowledge base using the LLM Wiki methodology.  
Support two core operations: **Ingest** (extract knowledge from sources) and **Query** (search wiki to answer).

## Trigger Keywords

Trigger this skill on keywords in any language:

| Trigger | Mode | Examples |
|---------|------|----------|
| `存入wiki知识库` / `存入wiki` | **Ingest** | Inject the given content into wiki |
| `检索wiki` / `搜索wiki` / `wiki查询` | **Query** | Search wiki to answer this question |

When the trigger Keyword is not present, do NOT use this skill.

## Step 0: KB Location Resolution (MUST RUN FIRST)

Before executing ANY mode (Ingest or Query), resolve the knowledge base location.

### 0.1 Load Saved Location

Read `references/kb-location.txt` from this skill directory. This file contains a single line: the absolute path to the knowledge base root (e.g., `d:\knowledge`).

### 0.2 If Location Is Not Saved

Ask the user with exact text:

> "请指定知识库的根目录路径（如 `d:\knowledge`）："

Receive the user's path. Normalize it to an absolute path.

### 0.3 Verify or Create KB Structure

Check if the KB root directory exists and contains `schema.md`:

- **Exists and has `schema.md`** → KB is initialized, proceed to Mode 1 or Mode 2.
- **Directory exists but no `schema.md`** → KB directory exists but is empty. Inform user and create full structure as described in Step 0.4.
- **Directory does not exist** → Auto-create the full KB structure including all directories and files (Step 0.4).

### 0.4 Create Full KB Structure (First-Time Setup)

When the KB needs to be initialized, create this structure:

```
{KB_ROOT}/
├── schema.md
├── raw/                    (empty dir)
└── wiki/
    ├── index.md
    ├── log.md
    ├── overview.md
    ├── concepts/            (empty dir)
    ├── entities/            (empty dir)
    ├── comparisons/         (empty dir)
    └── questions/           (empty dir)
```

Create ALL directories with `mkdir` commands, then create the three required files:

**`{KB_ROOT}/schema.md`** — Create a new schema file. Read `references/wiki-schema.md` from this skill and use it as the template, adjusting paths as needed.

**`{KB_ROOT}/wiki/index.md`** — Create an empty index with category tables (Overview, Concepts, Entities, Comparisons, Questions, Source Summaries), total pages: 0.

**`{KB_ROOT}/wiki/log.md`** — Create with a single initialization entry:
```
# Activity Log
## [today-date] init | Knowledge base initialized
- Location: {KB_ROOT}
- Created directory structure
- Created schema.md, wiki/index.md, wiki/log.md
```

### 0.5 Save Location

After resolution (whether loaded, user-provided, or created), write the absolute path to `references/kb-location.txt` in this skill directory. Use `write_to_file` — overwrite on each run to ensure it reflects the latest active KB.

Store only the path, no extra whitespace or comments. Example content:
```
d:\knowledge
```

## Architecture

The knowledge base follows a three-layer architecture:

```
KB_ROOT/
├── schema.md              # Conventions and workflow config
├── raw/                   # Immutable source documents (human-curated)
│   └── *.md
└── wiki/                  # LLM-generated and maintained pages
    ├── index.md           # Content catalog of all pages with summaries
    ├── log.md             # Chronological append-only activity log
    ├── overview.md        # Top-level synthesis hub
    ├── concepts/          # Concept/idea/framework pages
    ├── entities/          # People, orgs, tools, books pages
    ├── comparisons/       # Side-by-side comparison pages
    └── questions/         # Answers filed as pages
```

## Mode 1: Ingest（存入wiki知识库）

When the user says "存入wiki知识库" or similar, follow this workflow.

### Step 1.1: Identify Source Content

Determine the source of the knowledge to ingest:
- **User-provided text directly in chat** → Copy to `raw/source-YYYY-MM-DD.md`, name based on topic
- **Referenced file path** → Copy the file into `raw/`, rename to descriptive English filename
- **URL/Web content** → Fetch content, save to `raw/` as markdown

### Step 1.2: Read and Analyze Source

Read the source document from `raw/`. Extract:
1. **Key concepts** — core ideas, frameworks, principles
2. **Entities** — people, tools, organizations, books mentioned
3. **Relationships** — connections between concepts, contrasts, dependencies
4. **Actionable rules** — procedures, checklists, do's and don'ts

### Step 1.3: Create Wiki Pages

Based on extracted knowledge, create pages under `wiki/`:

- **Concept pages** (`wiki/concepts/`) — one per major idea. Include: summary, details, see-also links
- **Entity pages** (`wiki/entities/`) — one per significant tool/person/book. Include: what it is, role in the domain
- **Comparison pages** (`wiki/comparisons/`) — side-by-side with existing concepts where natural contrast exists

Every wiki page MUST follow conventions in `references/wiki-conventions.md`.

### Step 1.4: Update Infrastructure Pages

After creating new pages, touch these files:

- `wiki/overview.md` — add/update topic areas if the knowledge domain expands
- `wiki/index.md` — add entries for all new pages with one-line summaries in correct category tables
- `wiki/log.md` — append a log entry at the top:
  ```
  ## [YYYY-MM-DD] ingest | Source Title
  - Created: page1, page2, ...
  - Updated: page3, ...
  - Contradictions found: (list or "none")
  - Key takeaways: (2-3 bullet points)
  ```

### Step 1.5: Cross-Reference Check

- Ensure every new page links to at least 2 other wiki pages using `[[path/page.md|display text]]`
- Check for contradictions with existing wiki content — flag them explicitly in the log entry

### Ingest Anti-Patterns

- Do NOT copy source text verbatim into wiki pages — synthesize and structure
- Do NOT skip the index.md update — orphan pages degrade searchability
- Do NOT forget to copy sources to `raw/` before processing

## Mode 2: Query（检索wiki）

When the user says "检索wiki" or similar, follow this workflow.

### Step 2.1: Read Index

Start by reading `wiki/index.md` to identify relevant pages for the query topic.

### Step 2.2: Read Relevant Pages

Read the pages identified from the index that are most likely to answer the question. If the index does not contain a clear match, read `wiki/overview.md` for broader topic navigation.

### Step 2.3: Synthesize Answer

Combine information from all relevant pages into a coherent answer:
- Lead with the most important finding
- Include citations to specific wiki pages (use wikilinks or page references)
- Use comparison tables when contrasting two or more concepts
- Keep the answer concise — the wiki is for deep reading, this is the synthesis

### Step 2.4: Offer to File

If the answer would be valuable for future queries, ask the user: **"Should I file this answer as a new wiki page?"**

If yes, create a page under `wiki/questions/` and update index + log.

### Query Anti-Patterns

- Do NOT answer from general knowledge if the wiki has relevant pages — use the wiki first
- Do NOT read every wiki page sequentially — use index.md to triage

## Step Final: Report Knowledge Base Location

After completing any mode (Ingest or Query), ALWAYS report the knowledge base location to the user. Use exactly this format:

> 📂 知识库位置：`{KB_ROOT}`

This confirms which KB was used and helps the user navigate to it. Include it at the end of every response, after the task summary.

## References

- `references/wiki-conventions.md` — Page formatting rules, YAML frontmatter, naming conventions
- `references/wiki-schema.md` — Complete schema document (mirror of the knowledge base's `schema.md`)
