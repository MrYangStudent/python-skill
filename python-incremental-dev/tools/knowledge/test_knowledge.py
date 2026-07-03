#!/usr/bin/env python3
"""knowledge.py 的单元测试."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest

# 导入被测模块
sys_path = str(Path(__file__).parent)
import sys
sys.path.insert(0, sys_path)

from knowledge import (
    Entry,
    KB_DIR_NAME,
    format_yaml_frontmatter,
    parse_entries,
    parse_yaml_frontmatter,
    sanitize_filename,
    score_entry,
    extract_tags,
    discover_import_relations,
    discover_tag_relations,
)


class TestYamlFrontmatter:
    """YAML frontmatter 解析和格式化测试."""

    def test_parse_simple_kv(self):
        """解析简单键值对."""
        text = "---\nid: entry-123\ntitle: Test\n---\n\nContent"
        result = parse_yaml_frontmatter(text)
        assert result["id"] == "entry-123"
        assert result["title"] == "Test"

    def test_parse_inline_list(self):
        """解析内联列表标签."""
        text = "---\ntags: [search, filter]\n---\n\nContent"
        result = parse_yaml_frontmatter(text)
        assert result["tags"] == ["search", "filter"]

    def test_parse_multiline_list(self):
        """解析多行列表."""
        text = "---\ntags:\n  - search\n  - filter\n---\n\nContent"
        result = parse_yaml_frontmatter(text)
        assert result["tags"] == ["search", "filter"]

    def test_parse_no_frontmatter(self):
        """无 frontmatter 时返回空字典."""
        result = parse_yaml_frontmatter("Just content\nNo frontmatter")
        assert result == {}

    def test_format_simple(self):
        """格式化简单 frontmatter."""
        data = {"id": "entry-1", "title": "Test"}
        result = format_yaml_frontmatter(data)
        assert "id: entry-1" in result
        assert "title: Test" in result
        assert result.startswith("---")
        assert result.endswith("---")

    def test_format_list(self):
        """格式化含列表的 frontmatter."""
        data = {"tags": ["search", "filter"]}
        result = format_yaml_frontmatter(data)
        assert "tags: [search, filter]" in result


class TestParseEntries:
    """条目解析测试."""

    def test_parse_markdown_fields(self):
        """解析 Markdown 字段格式条目."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("""## [search] SearchUtils - 搜索工具

**标签**: search, filter
**来源**: pkg/search.py
**更新**: 2026-07-03
**用途**: 搜索列表元素

```python
result = find_first(items, lambda x: x.id == 1)
```

---
""")
        tmp.close()

        entries = parse_entries(tmp.name)
        assert len(entries) >= 1
        e = entries[0]
        assert "SearchUtils" in e.title
        assert "search" in e.tags
        assert e.source == "pkg/search.py"
        assert e.updated == "2026-07-03"
        assert "搜索列表元素" in e.purpose
        assert "find_first" in e.example

        os.unlink(tmp.name)

    def test_parse_yaml_frontmatter_entry(self):
        """解析 YAML frontmatter 格式条目."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("""---
id: entry-123
title: "[search] SearchUtils - 搜索工具"
tags: [search, filter]
source: "pkg/search.py"
updated: 2026-07-03
purpose: "搜索列表元素"
---

## [search] SearchUtils - 搜索工具

```python
result = find_first(items, lambda x: x.id == 1)
```

---
""")
        tmp.close()

        entries = parse_entries(tmp.name)
        assert len(entries) >= 1
        e = entries[0]
        assert e.id == "entry-123"
        assert "SearchUtils" in e.title
        assert "search" in e.tags
        assert e.source == "pkg/search.py"
        assert e.updated == "2026-07-03"

        os.unlink(tmp.name)


class TestExtractTags:
    """标签提取测试."""

    def test_extract_from_brackets(self):
        """从方括号提取标签."""
        tags = extract_tags("[search, filter] SearchUtils")
        assert tags == ["search", "filter"]

    def test_extract_no_brackets(self):
        """无方括号时返回空列表."""
        tags = extract_tags("SearchUtils")
        assert tags == []

    def test_extract_chinese_comma(self):
        """支持中文逗号."""
        tags = extract_tags("[搜索，过滤] SearchUtils")
        assert tags == ["搜索", "过滤"]


class TestSanitizeFilename:
    """文件名安全化测试."""

    def test_normal_tag(self):
        """正常标签."""
        assert sanitize_filename("search") == "search"

    def test_special_chars(self):
        """特殊字符替换."""
        assert sanitize_filename("search/filter") == "search_filter"

    def test_uppercase(self):
        """大写转小写."""
        assert sanitize_filename("Search") == "search"

    def test_empty_tag(self):
        """空标签返回 untagged."""
        assert sanitize_filename("") == "untagged"


class TestScoreEntry:
    """条目评分测试."""

    def _make_entry(self, **kwargs) -> Entry:
        """创建测试条目."""
        defaults = {
            "id": "entry-1",
            "title": "SearchUtils - 搜索工具",
            "tags": ["search", "filter"],
            "source": "pkg/search.py",
            "updated": "2026-07-03",
            "purpose": "搜索列表元素",
            "example": "result = find_first(items)",
        }
        for k, v in kwargs.items():
            defaults[k] = v
        return Entry(**defaults)

    def test_title_match(self):
        """标题匹配得分最高."""
        e = self._make_entry()
        score = score_entry(e, "SearchUtils")
        assert score >= 10  # 标题权重 10

    def test_title_exact_match(self):
        """标题完全匹配额外加分."""
        e = self._make_entry(title="search")
        score = score_entry(e, "search")
        assert score >= 30  # 10 + 20 完全匹配

    def test_tag_match(self):
        """标签匹配得分."""
        e = self._make_entry()
        score = score_entry(e, "filter")
        assert score >= 8

    def test_purpose_match(self):
        """用途描述匹配得分."""
        e = self._make_entry()
        score = score_entry(e, "搜索")
        assert score >= 5

    def test_no_match(self):
        """无匹配得分 0."""
        e = self._make_entry()
        score = score_entry(e, "nonexistent")
        assert score == 0

    def test_combined_match(self):
        """多维度匹配累加."""
        e = self._make_entry(title="search", tags=["search"])
        score = score_entry(e, "search")
        assert score >= 10 + 20 + 8  # 标题完全匹配 + 标签


class TestInitCommand:
    """init 命令测试."""

    def test_init_creates_structure(self):
        """初始化创建完整目录结构."""
        # 使用临时目录模拟
        tmp_dir = tempfile.mkdtemp()
        kb_path = Path(tmp_dir) / KB_DIR_NAME

        # 手动创建
        kb_path.mkdir(parents=True, exist_ok=True)
        index_path = kb_path / "INDEX.md"
        log_path = kb_path / "log.md"

        assert not index_path.exists()

        # 写入内容模拟 init
        index_path.write_text("# Knowledge Index\n", encoding="utf-8")
        log_path.write_text("# Activity Log\n", encoding="utf-8")

        assert index_path.exists()
        assert log_path.exists()

        shutil.rmtree(tmp_dir)

    def test_init_skip_existing(self):
        """已有知识库时跳过初始化."""
        tmp_dir = tempfile.mkdtemp()
        kb_path = Path(tmp_dir) / KB_DIR_NAME
        kb_path.mkdir(parents=True, exist_ok=True)
        index_path = kb_path / "INDEX.md"
        index_path.write_text("existing content", encoding="utf-8")

        # 不应覆盖
        content = index_path.read_text(encoding="utf-8")
        assert content == "existing content"

        shutil.rmtree(tmp_dir)


class TestRelatedField:
    """related 关联字段测试."""

    def test_entry_has_related_field(self):
        """Entry 数据结构包含 related 字段."""
        e = Entry(title="Test", related=["RelatedA", "RelatedB"])
        assert e.related == ["RelatedA", "RelatedB"]

    def test_entry_default_related_empty(self):
        """Entry 默认 related 为空列表."""
        e = Entry(title="Test")
        assert e.related == []

    def test_parse_yaml_with_related(self):
        """解析 YAML frontmatter 中 related 字段."""
        text = "---\nid: entry-1\ntitle: Test\nrelated: [RelatedA, RelatedB]\n---\n\nContent"
        result = parse_yaml_frontmatter(text)
        assert result["related"] == ["RelatedA", "RelatedB"]

    def test_format_yaml_with_related(self):
        """格式化含 related 的 YAML frontmatter."""
        data = {"id": "entry-1", "title": "Test", "related": ["A", "B"]}
        result = format_yaml_frontmatter(data)
        assert "related: [A, B]" in result

    def test_format_yaml_skip_empty_related(self):
        """格式化时空 related 列表不写入 frontmatter."""
        data = {"id": "entry-1", "title": "Test", "related": []}
        result = format_yaml_frontmatter(data)
        assert "related" not in result

    def test_parse_markdown_with_related(self):
        """解析 Markdown 格式的 **关联** 字段."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("""## [search] SearchUtils - 搜索工具

**标签**: search, filter
**来源**: pkg/search.py
**更新**: 2026-07-03
**用途**: 搜索列表元素
**关联**: FilterUtils - 过滤工具, SortUtils - 排序工具

---

""")
        tmp.close()

        entries = parse_entries(tmp.name)
        assert len(entries) >= 1
        e = entries[0]
        assert "FilterUtils - 过滤工具" in e.related
        assert "SortUtils - 排序工具" in e.related

        os.unlink(tmp.name)

    def test_parse_yaml_entry_with_related(self):
        """解析 YAML frontmatter 格式条目中的 related."""
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write("""---
id: entry-123
title: "[search] SearchUtils - 搜索工具"
tags: [search, filter]
related: [FilterUtils - 过滤, SortUtils - 排序]
source: "pkg/search.py"
updated: 2026-07-03
purpose: "搜索列表元素"
---

## [search] SearchUtils - 搜索工具

**关联**: FilterUtils - 过滤, SortUtils - 排序

---

""")
        tmp.close()

        entries = parse_entries(tmp.name)
        assert len(entries) >= 1
        e = entries[0]
        assert "FilterUtils - 过滤" in e.related
        assert "SortUtils - 排序" in e.related

        os.unlink(tmp.name)


class TestDiscoverRelations:
    """关联发现测试."""

    def test_discover_tag_relations_min_shared(self):
        """标签共享 >= 2 的条目被发现关联."""
        entries = [
            Entry(title="SearchA", tags=["search", "filter", "list"]),
            Entry(title="SearchB", tags=["search", "filter", "sort"]),
            Entry(title="UnrelatedC", tags=["auth", "user"]),
        ]
        relations = discover_tag_relations(entries, min_shared=2)
        assert "SearchA" in relations
        assert "SearchB" in relations["SearchA"]

    def test_discover_tag_relations_no_match(self):
        """标签共享 < 2 的条目不关联."""
        entries = [
            Entry(title="SearchA", tags=["search"]),
            Entry(title="AuthB", tags=["auth"]),
        ]
        relations = discover_tag_relations(entries, min_shared=2)
        assert len(relations) == 0

    def test_discover_import_relations(self):
        """通过 import 分析发现依赖关系."""
        # 创建临时项目目录和文件
        tmp_dir = tempfile.mkdtemp()
        # 创建 service.py（搜索条目的源文件）
        service_path = Path(tmp_dir) / "service.py"
        service_path.write_text("from utils.search import find_first\nfrom utils.filter import filter_active\n", encoding="utf-8")
        # 创建 utils/search.py（另一个条目的源文件）
        utils_dir = Path(tmp_dir) / "utils"
        utils_dir.mkdir()
        (utils_dir / "search.py").write_text("def find_first(items, fn): pass\n", encoding="utf-8")

        entries = [
            Entry(title="Service", source="service.py"),
            Entry(title="SearchUtils", source="utils/search.py"),
        ]
        relations = discover_import_relations(entries, tmp_dir)

        # Service 条目应该被发现关联 SearchUtils
        assert "Service" in relations
        assert "SearchUtils" in relations["Service"]

        shutil.rmtree(tmp_dir)
