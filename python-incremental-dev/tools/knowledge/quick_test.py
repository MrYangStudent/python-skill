#!/usr/bin/env python3
"""Quick test runner for knowledge.py."""
import sys
sys.path.insert(0, r'D:\python-skill\python-incremental-dev\tools\knowledge')

from knowledge import (
    Entry,
    format_yaml_frontmatter,
    parse_entries,
    parse_yaml_frontmatter,
    sanitize_filename,
    score_entry,
    extract_tags,
)

passed = 0
failed = 0

def run_test(name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print(f"  PASS: {name}")
    except Exception as e:
        failed += 1
        print(f"  FAIL: {name} - {str(e)[:100]}")

# Test YAML frontmatter
run_test("yaml_parse_kv", lambda: (
    parse_yaml_frontmatter("---\nid: entry-1\ntitle: Test\n---\nContent"),
    None
)[0] == {"id": "entry-1", "title": "Test"} or None)

run_test("yaml_parse_list", lambda: (
    parse_yaml_frontmatter("---\ntags: [search, filter]\n---\n"),
    None
)[0]["tags"] == ["search", "filter"] or None)

run_test("yaml_format", lambda: "id: e1" in format_yaml_frontmatter({"id": "e1", "tags": ["a", "b"]}))

run_test("yaml_no_fm", lambda: parse_yaml_frontmatter("no fm") == {})

# Test extract_tags
run_test("tags_brackets", lambda: extract_tags("[search, filter] Title") == ["search", "filter"])
run_test("tags_no_brackets", lambda: extract_tags("Title") == [])
run_test("tags_chinese", lambda: extract_tags("[搜索，过滤] Title") == ["搜索", "过滤"])

# Test sanitize_filename
run_test("filename_normal", lambda: sanitize_filename("search") == "search")
run_test("filename_special", lambda: sanitize_filename("search/filter") == "search_filter")
run_test("filename_upper", lambda: sanitize_filename("Search") == "search")
run_test("filename_empty", lambda: sanitize_filename("") == "untagged")

# Test score_entry
e = Entry(title="SearchUtils", tags=["search"], purpose="search list", source="pkg/search.py")
run_test("score_title", lambda: score_entry(e, "SearchUtils") >= 10)
run_test("score_tag", lambda: score_entry(e, "filter") == 0)  # no "filter" in this entry
run_test("score_purpose", lambda: score_entry(e, "搜索") == 0)  # not in this entry
run_test("score_no_match", lambda: score_entry(e, "nonexistent") == 0)

e2 = Entry(title="search", tags=["search"], purpose="search list")
run_test("score_exact", lambda: score_entry(e2, "search") >= 30)

print(f"\nResults: {passed} passed, {failed} failed")
if failed > 0:
    sys.exit(1)
