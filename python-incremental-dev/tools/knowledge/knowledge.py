#!/usr/bin/env python3
"""Knowledge — 知识库管理工具.

用于增量开发场景下沉淀、检索和更新项目可复用知识.
零外部依赖，纯 Python 标准库实现.

用法:

    python knowledge.py init                    # 初始化知识库
    python knowledge.py add                     # 交互式新增条目
    python knowledge.py add -t "标题" -s "来源" -p "用途"  # 命令行新增
    python knowledge.py add -t "标题" -r "关联1" "关联2"   # 新增带关联
    python knowledge.py search <关键词>          # 搜索知识条目
    python knowledge.py list                    # 列出所有条目
    python knowledge.py list --stale <目录>      # 标记过时条目
    python knowledge.py check-stale <项目目录>   # 检查条目是否过期
    python knowledge.py reindex                  # 从内容文件重建 INDEX.md
    python knowledge.py scan [目录...]           # 扫描项目代码提取导出函数/类
    python knowledge.py lint                    # 知识库完整性检查
    python knowledge.py link [项目目录]           # 自动发现条目间的关联关系
"""

import argparse
import ast
import io
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


KB_DIR_NAME = "project-knowledge"
INDEX_FILE = "INDEX.md"
LOG_FILE = "log.md"


@dataclass
class Entry:
    """一条知识条目."""

    id: str = ""
    title: str = ""
    tags: list[str] = field(default_factory=list)
    source: str = ""
    updated: str = ""
    purpose: str = ""
    example: str = ""
    file_path: str = ""
    line_num: int = 0
    related: list[str] = field(default_factory=list)  # 关联条目 title 列表


# ---------- YAML frontmatter 解析 ----------

_YAML_BLOCK_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_YAML_KV_RE = re.compile(r"^(\w[\w-]*)\s*:\s*(.*)$")
_YAML_LIST_RE = re.compile(r"^\s+\-\s+(.+)$")


def parse_yaml_frontmatter(text: str) -> dict:
    """解析 YAML frontmatter 块，返回键值字典.

    支持简单键值对和列表值（如 tags: [a, b] 或 tags:\n  - a\n  - b）.
    """
    match = _YAML_BLOCK_RE.match(text)
    if not match:
        return {}

    yaml_text = match.group(1)
    result: dict = {}
    current_key: Optional[str] = None
    current_list: list[str] = []

    for line in yaml_text.split("\n"):
        # 列表项
        list_match = _YAML_LIST_RE.match(line)
        if list_match and current_key:
            current_list.append(list_match.group(1).strip().strip("'\""))
            continue

        # 保存上一个 key 的列表
        if current_key and current_list:
            result[current_key] = current_list
            current_list = []
            current_key = None

        # 键值对
        kv_match = _YAML_KV_RE.match(line)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip()
            # 内联列表 [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                items = [v.strip().strip("'\"") for v in value[1:-1].split(",")]
                result[key] = items
                current_key = None
            elif value == "":
                # 纯列表模式（key:\n  - a\n  - b），等待后续列表项
                current_key = key
                current_list = []
            else:
                result[key] = value.strip("'\"")
                current_key = None
                current_list = []

    # 保存最后的列表
    if current_key and current_list:
        result[current_key] = current_list
    elif current_key and not current_list:
        # 纯列表模式但没有列表项（如 tags: 后无列表），存为空列表
        result[current_key] = []

    return result


def format_yaml_frontmatter(data: dict) -> str:
    """将字典格式化为 YAML frontmatter 字符串.

    空列表字段不写入 frontmatter，减少冗余.
    """
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            if value:  # 非空列表才写入
                lines.append(f"{key}: [{', '.join(value)}]")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


# ---------- Markdown 条目解析 ----------

_TITLE_RE = re.compile(r"^##\s+(\[[^\]]+\]\s*)?(.+)$")
_FIELD_RE = re.compile(r"^\*\*([^*]+)\*\*\s*:\s*(.+)$")


def parse_entries(path: str) -> list[Entry]:
    """解析单个 .md 知识文件，提取所有结构化 Entry."""
    data = Path(path).read_text(encoding="utf-8")
    entries: list[Entry] = []
    current: Optional[Entry] = None
    in_code_block = False
    in_frontmatter = False

    lines = data.split("\n")

    # 先尝试解析 YAML frontmatter
    fm = parse_yaml_frontmatter(data)
    if fm:
        current = Entry(
            id=fm.get("id", ""),
            title=fm.get("title", ""),
            tags=fm.get("tags", []) if isinstance(fm.get("tags", []), list) else [fm.get("tags", "")],
            source=fm.get("source", ""),
            updated=fm.get("updated", ""),
            purpose=fm.get("purpose", ""),
            related=fm.get("related", []) if isinstance(fm.get("related", []), list) else [fm.get("related", "")] if fm.get("related") else [],
            file_path=path,
        )

    # 跳过 frontmatter 区域
    fm_end = 0
    if fm:
        match = _YAML_BLOCK_RE.match(data)
        if match:
            fm_end = match.end()

    content_lines = data[fm_end:].split("\n") if fm_end > 0 else lines

    in_code_block = False

    for i, line in enumerate(content_lines):
        trimmed = line.strip()

        # 代码块
        if trimmed.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            if current and not current.id:
                current.example += line + "\n"
            continue

        # 标题
        title_match = _TITLE_RE.match(trimmed)
        if title_match:
            if current and not current.id:
                entries.append(current)
            if not fm or not current:
                current = Entry(file_path=path, line_num=i + 1)
            if title_match.group(2):
                current.title = title_match.group(2)
            # 从标题提取标签
            if title_match.group(1):
                tag_content = title_match.group(1).strip().strip("[]")
                current.tags = [t.strip() for t in tag_content.split(",")]
            continue

        # 字段
        field_match = _FIELD_RE.match(trimmed)
        if field_match and current:
            field_name = field_match.group(1)
            field_value = field_match.group(2).strip()
            if field_name == "标签":
                current.tags = [t.strip() for t in field_value.replace("，", ",").split(",")]
            elif field_name == "来源":
                current.source = field_value
            elif field_name == "更新":
                current.updated = field_value
            elif field_name == "用途":
                current.purpose = field_value
            elif field_name == "关联":
                current.related = [t.strip() for t in field_value.replace("，", ",").split(",") if t.strip()]

    if current:
        entries.append(current)

    return entries


def load_all_entries(kb_dir: Optional[str] = None) -> list[Entry]:
    """遍历 project-knowledge/ 目录，解析所有 .md 文件并返回条目列表."""
    kb_path = Path(kb_dir or KB_DIR_NAME)
    if not kb_path.exists():
        print(f"❌ 知识库目录不存在 ({kb_path})，请先运行 `python knowledge.py init`")
        sys.exit(1)

    entries: list[Entry] = []
    for md_file in kb_path.glob("*.md"):
        if md_file.name in (INDEX_FILE, LOG_FILE):
            continue
        try:
            file_entries = parse_entries(str(md_file))
            entries.extend(file_entries)
        except Exception as e:
            print(f"⚠️  解析 {md_file} 失败: {e}")

    return entries


# ---------- init ----------

def run_init(args: argparse.Namespace) -> None:
    """初始化 project-knowledge/ 目录并创建 INDEX.md 和 log.md."""
    kb_dir = Path(KB_DIR_NAME)
    kb_dir.mkdir(parents=True, exist_ok=True)

    index_path = kb_dir / INDEX_FILE
    if index_path.exists():
        print("✅ 知识库已存在，跳过初始化。")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Knowledge Index

> 项目可复用知识条目索引。每次增量开发后更新。
> 最后更新: {date_str}

| 条目 | 标签 | 来源 | 更新日期 |
|------|------|------|----------|
"""
    index_path.write_text(content, encoding="utf-8")

    # 创建 log.md
    log_path = kb_dir / LOG_FILE
    log_content = f"""# Activity Log

## [{date_str}] init | Knowledge base initialized
- Location: {kb_dir}
- Created directory structure
- Created INDEX.md, log.md
"""
    log_path.write_text(log_content, encoding="utf-8")

    print(f"✅ 知识库已初始化: {kb_dir}")


# ---------- add ----------

def run_add(args: argparse.Namespace) -> None:
    """交互式或命令行方式添加知识条目到知识库."""
    title = args.title or ""
    source = args.source or ""
    purpose = args.purpose or ""
    example = args.example or ""

    # 交互模式
    if not title:
        title = input("📝 标题: ").strip()
        tags_input = input("🏷️  标签(逗号分隔): ").strip()
        source = input("📁 来源文件: ").strip()
        purpose = input("💡 用途: ").strip()
        print("🔧 示例代码(多行，输入 EOF 结束):")
        example_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "EOF":
                    break
                example_lines.append(line)
            except EOFError:
                break
        example = "\n".join(example_lines).strip()

        if tags_input:
            extra_tags = [t.strip() for t in tags_input.replace("，", ",").split(",")]
        else:
            extra_tags = []
    else:
        extra_tags = []

    if not title:
        print("❌ 标题不能为空")
        sys.exit(1)

    # 生成条目
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    entry_id = f"entry-{int(now.timestamp())}"

    # 确定标签
    tag_list = extra_tags or extract_tags(title)
    tag_line = ", ".join(tag_list) if tag_list else "general"
    if not tag_list:
        tag_list = ["general"]

    # 使用 YAML frontmatter 格式
    # 确定 related 列表
    related_list = args.related or []

    fm_data = {
        "id": entry_id,
        "title": title,
        "tags": tag_list,
        "source": source or "-",
        "updated": date_str,
        "purpose": purpose or "-",
    }
    if related_list:
        fm_data["related"] = related_list
    fm_str = format_yaml_frontmatter(fm_data)

    entry_text = f"\n{fm_str}\n\n## {title}\n\n"
    entry_text += f"**标签**: {tag_line}\n"
    entry_text += f"**来源**: {source or '-'}\n"
    entry_text += f"**更新**: {date_str}\n"
    entry_text += f"**用途**: {purpose or '-'}\n"
    if related_list:
        entry_text += f"**关联**: {', '.join(related_list)}\n"
    entry_text += "\n"
    if example:
        entry_text += "```python\n"
        entry_text += example + "\n"
        entry_text += "```\n"
    entry_text += "\n---\n"

    # 写入知识库文件
    kb_dir = Path(KB_DIR_NAME)
    kb_dir.mkdir(parents=True, exist_ok=True)

    # 根据第一个标签选择子文件
    file_name = "common-utils.md"
    for t in tag_list:
        if t and t != "general":
            file_name = sanitize_filename(t) + ".md"
            break

    file_path = kb_dir / file_name
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry_text)

    # 更新 INDEX.md
    update_index(str(kb_dir), title, tag_line, source or "-", date_str)

    # 更新 log.md
    append_log(str(kb_dir), "add", title, f"新增条目: {title}")

    print(f"✅ 已保存条目: {title} → {file_path}")


def extract_tags(title: str) -> list[str]:
    """从 "[tag1, tag2] Title" 格式的标题中提取标签列表."""
    match = re.search(r"\[([^\]]+)\]", title)
    if match:
        tag_content = match.group(1).strip()
        return [t.strip() for t in tag_content.replace("，", ",").split(",")]
    return []


def update_index(kb_dir: str, title: str, tags: str, source: str, date: str) -> None:
    """将新增条目的摘要信息追加到 INDEX.md 索引表中."""
    index_path = Path(kb_dir) / INDEX_FILE
    if not index_path.exists():
        return

    data = index_path.read_text(encoding="utf-8")
    line = f"| {title} | {tags} | {source} | {date} |"
    lines = data.split("\n")

    # 更新最后更新日期
    for i, l in enumerate(lines):
        if l.startswith("> 最后更新:"):
            lines[i] = f"> 最后更新: {date}"
            break

    # 找到表格区域
    table_start = -1
    table_end = -1
    for i, l in enumerate(lines):
        if l.startswith("|------"):
            table_start = i
        if table_start != -1 and l.strip().startswith("|"):
            table_end = i

    if table_start == -1 or table_end == -1:
        lines.append(line)
    else:
        lines.insert(table_end + 1, line)

    index_path.write_text("\n".join(lines), encoding="utf-8")


def append_log(kb_dir: str, operation: str, title: str, detail: str) -> None:
    """追加操作日志到 log.md."""
    log_path = Path(kb_dir) / LOG_FILE
    if not log_path.exists():
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{date_str}] {operation} | {title}\n- {detail}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def sanitize_filename(tag: str) -> str:
    """将标签转为安全的文件名."""
    safe = re.sub(r"[^\w\-]", "_", tag.lower())
    safe = safe.strip("_")
    return safe or "untagged"


# ---------- search ----------

def score_entry(entry: Entry, keyword: str) -> int:
    """对知识条目按关键词进行加权评分.

    标题(30) > 标签(8) > 用途(5) > 来源(3) > 示例(2).
    """
    kw = keyword.lower()
    score = 0

    # 标题匹配（最高权重）
    if kw in entry.title.lower():
        score += 10
        if entry.title.lower() == kw:
            score += 20  # 完全匹配

    # 标签匹配
    for tag in entry.tags:
        if kw in tag.lower():
            score += 8

    # 用途描述匹配
    if kw in entry.purpose.lower():
        score += 5

    # 来源文件匹配
    if kw in entry.source.lower():
        score += 3

    # 示例代码匹配
    if kw in entry.example.lower():
        score += 2

    return score


def run_search(args: argparse.Namespace) -> None:
    """全文搜索知识库，按相关性排序输出匹配条目."""
    keyword = " ".join(args.keywords)
    if not keyword:
        print("❌ 请指定搜索关键词")
        sys.exit(1)

    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空。")
        return

    results = []
    for e in entries:
        s = score_entry(e, keyword)
        if s > 0:
            results.append((e, s))

    if not results:
        print("❌ 未找到匹配条目。")
        return

    # 按分数排序
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"🔍 找到 {len(results)} 条匹配结果:\n")
    for i, (e, s) in enumerate(results):
        print(f"{i + 1}. {e.title}")
        print(f"   📁 {e.source}")
        print(f"   🏷️  {', '.join(e.tags)}")
        print(f"   💡 {e.purpose}")
        print(f"   📅 {e.updated}")
        if e.related:
            print(f"   🔗 关联: {', '.join(e.related)}")
        print()


# ---------- list ----------

def run_list(args: argparse.Namespace) -> None:
    """列出知识库中所有条目，支持 --stale 过滤过时条目."""
    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空。使用 `python knowledge.py add` 添加条目。")
        return

    project_dir = args.stale or ""

    print(f"📚 知识库共 {len(entries)} 条:\n")
    for i, e in enumerate(entries):
        print(f"{i + 1}. {e.title}")
        print(f"   📁 {e.source} | 🏷️  {', '.join(e.tags)} | 📅 {e.updated}")
        if project_dir:
            status = check_entry_freshness(e, project_dir)
            print(f"   {status}")
        print()


# ---------- check-stale ----------

def check_entry_freshness(entry: Entry, project_dir: str) -> str:
    """对比条目来源文件的修改时间与记录日期，返回时效状态字符串."""
    if not entry.source or entry.source == "-":
        return f"✅ {entry.title} 无来源文件，持保留"

    source_path = Path(project_dir) / entry.source
    if not source_path.exists():
        return f"⚠️  [{entry.title}] 来源文件不存在: {entry.source}"

    mod_time = source_path.stat().st_mtime
    mod_date = datetime.fromtimestamp(mod_time)

    try:
        entry_date = datetime.strptime(entry.updated, "%Y-%m-%d")
    except ValueError:
        return f"⚠️  [{entry.title}] 日期格式无法解析: {entry.updated}"

    if mod_date > entry_date + __import__("datetime").timedelta(hours=24):
        return (
            f"⚠️  [{entry.title}] 可能过期 — "
            f"文件 {entry.source} 最后修改 {mod_date.strftime('%Y-%m-%d')}，"
            f"条目记录 {entry.updated}"
        )

    return f"✅ [{entry.title}] 时效正常"


def run_check_stale(args: argparse.Namespace) -> None:
    """对比知识条目来源文件的修改时间，报告过期条目."""
    project_dir = args.project_dir
    if not project_dir:
        print("❌ 请指定项目代码目录路径")
        print("用法: python knowledge.py check-stale <项目目录>")
        sys.exit(1)

    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空，无需检查。")
        return

    stale_count = 0
    fresh_count = 0

    print("🔍 正在检查条目时效性...")
    for e in entries:
        status = check_entry_freshness(e, project_dir)
        if "过期" in status or "可能过期" in status:
            stale_count += 1
            print(f"⚠️  {status}")
            print(f"   📁 来源: {e.source} | 📅 记录: {e.updated}")
            print()
        else:
            fresh_count += 1

    print(f"📊 结果: {fresh_count} 条有效, {stale_count} 条过期/待更新")
    if stale_count > 0:
        print("💡 提示: 使用 `python knowledge.py add` 重新录入过期条目以更新信息。")


# ---------- reindex ----------

def run_reindex(args: argparse.Namespace) -> None:
    """从 project-knowledge/ 下的内容文件重建 INDEX.md."""
    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空，INDEX.md 无需更新。")
        return

    kb_dir = Path(KB_DIR_NAME)
    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Knowledge Index\n",
        "\n",
        "> 项目可复用知识条目索引。每次增量开发后更新。\n",
        f"> 最后更新: {date_str}\n",
        "\n",
        "| 条目 | 标签 | 来源 | 更新日期 |\n",
        "|------|------|------|----------|\n",
    ]
    for e in entries:
        tags_str = ", ".join(e.tags)
        lines.append(f"| {e.title} | {tags_str} | {e.source} | {e.updated} |\n")

    index_path = kb_dir / INDEX_FILE
    index_path.write_text("".join(lines), encoding="utf-8")

    print(f"✅ INDEX.md 已重建（共 {len(entries)} 条）: {index_path}")


# ---------- scan ----------

@dataclass
class ScanCandidate:
    """从代码中扫描出的候选知识条目."""

    name: str
    doc: str
    module: str
    file: str


def run_scan(args: argparse.Namespace) -> None:
    """扫描指定目录中的 Python 代码，提取导出函数/类作为候选知识条目."""
    dirs = args.directories or [".", "src", "pkg", "app"]

    candidates: list[ScanCandidate] = []
    for dir_path in dirs:
        scan_dir = Path(dir_path)
        if not scan_dir.exists() or not scan_dir.is_dir():
            continue

        for py_file in scan_dir.rglob("*.py"):
            # 排除测试文件和 __init__.py
            if py_file.name.startswith("test_") or py_file.name == "__init__.py" or py_file.name.startswith("conftest"):
                continue

            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue

            module_name = py_file.stem
            for node in ast.walk(tree):
                # 公开类
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                    doc = ast.get_docstring(node) or ""
                    candidates.append(ScanCandidate(
                        name=node.name,
                        doc=doc,
                        module=module_name,
                        file=str(py_file),
                    ))
                # 公开函数（排除方法和 main）
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    if node.name == "main":
                        continue
                    # 排除类方法（通过 col_offset 判断是否在类内部）
                    # 简化判断：函数定义在类内部时跳过
                    doc = ast.get_docstring(node) or ""
                    candidates.append(ScanCandidate(
                        name=node.name,
                        doc=doc,
                        module=module_name,
                        file=str(py_file),
                    ))

    if not candidates:
        print("🔍 未找到可导出的函数或类。")
        return

    # 加载已有条目，用于去重
    existing: set[str] = set()
    try:
        entries = load_all_entries()
        for e in entries:
            existing.add(e.title)
    except SystemExit:
        pass

    new_count = 0
    for c in candidates:
        short_desc = c.doc.split("\n")[0] if c.doc else ""
        title = f"[{c.module}] {c.name} - {short_desc}" if short_desc else c.name
        if title in existing or c.name in existing:
            continue
        new_count += 1
        print(f"  📦 建议添加:")
        print(f'     python knowledge.py add -t "{title}" -s "{c.file}" -p "{short_desc}"')
        print()

    if new_count == 0:
        print("✅ 所有导出函数/类已存在于知识库，无需新增。")
    else:
        print(f"📊 共发现 {new_count} 个新候选条目（共扫描 {len(candidates)} 个导出符号）。")
        print("💡 复制上方 python knowledge.py add 命令执行即可保存。")


# ---------- lint ----------

def run_lint(args: argparse.Namespace) -> None:
    """知识库完整性检查：矛盾、孤儿、过期."""
    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空，无需 lint。")
        return

    issues: list[str] = []

    # 1. 检查重复标题
    titles: dict[str, list[Entry]] = {}
    for e in entries:
        if e.title not in titles:
            titles[e.title] = []
        titles[e.title].append(e)

    for title, group in titles.items():
        if len(group) > 1:
            files = [e.file_path for e in group]
            issues.append(f"🔴 重复标题: '{title}' 出现 {len(group)} 次 → {files}")

    # 2. 检查孤儿条目（无标签或无来源）
    for e in entries:
        if not e.tags or e.tags == ["general"]:
            issues.append(f"🟡 弱标签: '{e.title}' 仅有 general 标签")
        if not e.source or e.source == "-":
            issues.append(f"🟡 无来源: '{e.title}' 缺少来源文件信息")

    # 3. 检查过期日期（与当前日期对比）
    today = datetime.now()
    for e in entries:
        if e.updated:
            try:
                entry_date = datetime.strptime(e.updated, "%Y-%m-%d")
                age_days = (today - entry_date).days
                if age_days > 90:
                    issues.append(f"🟡 过旧: '{e.title}' 已 {age_days} 天未更新（{e.updated}）")
            except ValueError:
                issues.append(f"🔴 日期格式错误: '{e.title}' → {e.updated}")

    # 4. 检查标签一致性（同概念不同标签名）
    tag_variants: dict[str, set[str]] = {}
    for e in entries:
        for tag in e.tags:
            normalized = tag.lower().replace("-", " ").replace("_", " ")
            if normalized not in tag_variants:
                tag_variants[normalized] = set()
            tag_variants[normalized].add(tag)

    for norm, variants in tag_variants.items():
        if len(variants) > 1:
            issues.append(f"🟡 标签不一致: 同一概念有多个变体 → {variants}")

    # 5. 检查 INDEX.md 与实际条目数的一致性
    kb_dir = Path(KB_DIR_NAME)
    index_path = kb_dir / INDEX_FILE
    if index_path.exists():
        index_data = index_path.read_text(encoding="utf-8")
        index_rows = len([l for l in index_data.split("\n") if l.strip().startswith("|") and not l.startswith("|------")])
        # 减去表头行
        index_rows -= 1
        actual_count = len(entries)
        if index_rows != actual_count:
            issues.append(f"🔴 索引不一致: INDEX.md 有 {index_rows} 行，实际 {actual_count} 条目")

    # 6. 检查关联引用是否存在
    all_titles = {e.title for e in entries}
    for e in entries:
        for ref in e.related:
            if ref not in all_titles:
                issues.append(f"🔴 关联引用不存在: '{e.title}' 引用了 '{ref}'，但该条目不存在")

    # 6. 检查关联引用是否存在
    all_titles = {e.title for e in entries}
    for e in entries:
        for ref in e.related:
            if ref not in all_titles:
                issues.append(f"🔴 关联引用不存在: '{e.title}' 引用了 '{ref}'，但该条目不存在")

    # 报告
    if not issues:
        print("✅ 知识库 lint 检查通过，无问题。")
    else:
        print(f"🔍 知识库 lint 发现 {len(issues)} 个问题:\n")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n📊 共 {len(issues)} 个问题")
        print("💡 提示: 使用 `python knowledge.py reindex` 修复索引问题")


# ---------- link ----------

def discover_import_relations(entries: list[Entry], project_dir: str) -> dict[str, list[str]]:
    """通过分析条目来源文件的 import 语句，发现条目间的依赖关系.

    返回字典: {entry_title: [依赖的条目title列表]}.
    仅分析 Python 源码的 import/from ... import 语句.
    """
    relations: dict[str, list[str]] = {}

    # 构建 source → entry 的映射
    source_to_entries: dict[str, list[Entry]] = {}
    for e in entries:
        if e.source and e.source != "-":
            # source 是相对路径，如 pkg/search.py
            source_to_entries[e.source] = source_to_entries.get(e.source, []) + [e]

    for e in entries:
        if not e.source or e.source == "-":
            continue

        source_path = Path(project_dir) / e.source
        if not source_path.exists() or not source_path.suffix == ".py":
            continue

        try:
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue

        # 提取 import 路径中的文件引用
        imported_files: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # import pkg.search → pkg/search.py
                    mod_path = alias.name.replace(".", "/") + ".py"
                    imported_files.add(mod_path)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # from pkg.search import find → pkg/search.py
                    mod_path = node.module.replace(".", "/") + ".py"
                    imported_files.add(mod_path)

        # 查找 import 路径与知识库条目 source 的匹配
        related_titles: list[str] = []
        for imp_file in imported_files:
            # 尝试多种匹配方式
            for src_key, src_entries in source_to_entries.items():
                # 精确匹配或路径后缀匹配
                if imp_file == src_key or src_key.endswith(imp_file.split("/")[-1]):
                    for se in src_entries:
                        if se.title != e.title:  # 不关联自己
                            related_titles.append(se.title)

        if related_titles:
            relations[e.title] = related_titles

    return relations


def discover_tag_relations(entries: list[Entry], min_shared: int = 2) -> dict[str, list[str]]:
    """通过标签相似度发现条目间的关联关系.

    当两个条目共享 >= min_shared 个标签时，认为它们关联.
    返回字典: {entry_title: [关联的条目title列表]}.
    """
    relations: dict[str, list[str]] = {}

    for i, e1 in enumerate(entries):
        e1_tags = set(e1.tags)
        for j, e2 in enumerate(entries):
            if i == j:
                continue
            e2_tags = set(e2.tags)
            shared = len(e1_tags & e2_tags)
            if shared >= min_shared:
                relations.setdefault(e1.title, []).append(e2.title)

    return relations


def run_link(args: argparse.Namespace) -> None:
    """自动发现条目间的关联关系并输出建议.

    两种发现方式：
    1. import 分析：条目 source 文件 import 了其他条目 source 的模块
    2. 标签相似度：共享 >= 2 个标签的条目互相关联
    """
    project_dir = args.project_dir or "."
    entries = load_all_entries()
    if not entries:
        print("📚 知识库为空，无法发现关联。")
        return

    # 1. import 分析
    import_relations = discover_import_relations(entries, project_dir)

    # 2. 标签相似度
    tag_relations = discover_tag_relations(entries)

    # 合并并去重（排除已存在的关联）
    existing_related: dict[str, set[str]] = {}
    for e in entries:
        existing_related[e.title] = set(e.related)

    # 输出建议
    total_suggestions = 0
    for e in entries:
        suggestions: list[str] = []

        # import 关联
        if e.title in import_relations:
            for ref in import_relations[e.title]:
                if ref not in existing_related.get(e.title, set()):
                    suggestions.append(ref)

        # 标签关联
        if e.title in tag_relations:
            for ref in tag_relations[e.title]:
                if ref not in existing_related.get(e.title, set()) and ref not in suggestions:
                    suggestions.append(ref)

        if not suggestions:
            continue

        total_suggestions += len(suggestions)
        print(f"🔗 {e.title}")
        print(f"   建议关联: {', '.join(suggestions)}")
        print(f"   添加命令: python knowledge.py add -t \"{e.title}\" -s \"{e.source}\" -p \"{e.purpose}\" -r \"{', '.join(suggestions)}\"")
        print()

    if total_suggestions == 0:
        print("✅ 未发现新的关联建议（所有 import 和标签关联已记录）。")
    else:
        print(f"📊 共发现 {total_suggestions} 个关联建议。")
        print("💡 复制上方 add 命令并添加 --related 参数即可更新条目关联。")


# ---------- CLI 入口 ----------

def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器."""
    parser = argparse.ArgumentParser(
        description="Knowledge — 知识库管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""用法:
  python knowledge.py init                   初始化知识库目录结构
  python knowledge.py add                   交互式添加知识条目
  python knowledge.py add -t "标题" -s "来源" -p "用途" [-e "示例"] [-r "关联1" "关联2"]  命令行添加
  python knowledge.py search <关键词>        搜索知识条目
  python knowledge.py list [--stale <目录>]  列出条目
  python knowledge.py check-stale <项目目录>  检查并报告过期条目
  python knowledge.py reindex                 从内容文件重建 INDEX.md
  python knowledge.py scan [目录...]           扫描项目代码提取导出函数/类
  python knowledge.py lint                    知识库完整性检查
  python knowledge.py link [项目目录]           自动发现条目间的关联关系""",
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    subparsers.add_parser("init", help="初始化知识库目录结构")

    # add
    add_parser = subparsers.add_parser("add", help="添加知识条目")
    add_parser.add_argument("-t", "--title", default="", help="条目标题")
    add_parser.add_argument("-s", "--source", default="", help="来源文件路径")
    add_parser.add_argument("-p", "--purpose", default="", help="用途描述")
    add_parser.add_argument("-e", "--example", default="", help="示例代码")
    add_parser.add_argument("-r", "--related", nargs="*", default=[], help="关联条目标题列表")

    # search
    search_parser = subparsers.add_parser("search", help="搜索知识条目")
    search_parser.add_argument("keywords", nargs="+", help="搜索关键词")

    # list
    list_parser = subparsers.add_parser("list", help="列出所有条目")
    list_parser.add_argument("--stale", default="", help="同时检查过期条目（指定项目目录）")

    # check-stale
    stale_parser = subparsers.add_parser("check-stale", help="检查过期条目")
    stale_parser.add_argument("project_dir", help="项目代码目录路径")

    # reindex
    subparsers.add_parser("reindex", help="从内容文件重建 INDEX.md")

    # scan
    scan_parser = subparsers.add_parser("scan", help="扫描项目代码提取导出函数/类")
    scan_parser.add_argument("directories", nargs="*", help="扫描目录列表")

    # lint
    subparsers.add_parser("lint", help="知识库完整性检查")

    # link
    link_parser = subparsers.add_parser("link", help="自动发现条目间的关联关系")
    link_parser.add_argument("project_dir", nargs="?", default=".", help="项目代码目录路径（默认当前目录）")

    return parser


def main() -> None:
    """CLI 入口函数."""
    # Windows 下设置 stdout 为 UTF-8，避免 emoji 输出编码错误
    # 仅在 CLI 直接运行时执行，不影响 pytest 导入
    if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    command_map = {
        "init": run_init,
        "add": run_add,
        "search": run_search,
        "list": run_list,
        "check-stale": run_check_stale,
        "reindex": run_reindex,
        "scan": run_scan,
        "lint": run_lint,
        "link": run_link,
    }

    cmd_func = command_map.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        print(f"未知命令: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
