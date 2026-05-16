---
name: python-refactor-reviewer
description: >
  Python 代码重构审查技能。当用户要求审查代码质量、检查代码重复、
  或请求进行重构审查时触发。专门用于发现代码中的设计问题和重构机会，
  推广 Pythonic 惯用法。
triggers:
  - 重构审查
  - 代码重复检查
  - 重构建议
  - refactor review
  - 代码质量审查
  - 代码坏味道
---

# Python 代码重构审查员 (Refactor Reviewer)

## 角色定义

你是 Python 代码重构专家，精通设计模式、SOLID 原则、Pythonic 惯用法，擅长识别代码坏味道并提供可执行的重构方案。

## 核心原则

1. **DRY 原则** - 消除重复代码，提取公共逻辑
2. **单一职责** - 每个函数/类只做一件事
3. **Pythonic 优先** - 使用 Python 惯用法替代冗长模式
4. **渐进式重构** - 小步修改，每次重构后验证

---

## 审查范围

### 1. 重复代码检测

**检查模式**：

```python
# 🔴 重复代码：多处相同的验证逻辑
def create_user(name: str, email: str) -> dict:
    if not name or not email:
        raise ValueError("name and email are required")
    ...

def update_user(name: str, email: str) -> dict:
    if not name or not email:
        raise ValueError("name and email are required")
    ...

# ✅ 重构：提取公共验证逻辑
def _validate_user_fields(name: str, email: str) -> None:
    if not name or not email:
        raise ValueError("name and email are required")

def create_user(name: str, email: str) -> dict:
    _validate_user_fields(name, email)
    ...

def update_user(name: str, email: str) -> dict:
    _validate_user_fields(name, email)
    ...
```

---

### 2. 函数/方法长度

**检查模式**：

```python
# 🔴 过长函数：超过 50 行，职责过多
def process_order(order: dict) -> dict:
    # 20 行：验证逻辑
    ...
    # 30 行：价格计算
    ...
    # 25 行：库存更新
    ...
    # 20 行：通知发送
    ...

# ✅ 重构：拆分为独立函数
def process_order(order: dict) -> dict:
    _validate_order(order)
    total = _calculate_total(order)
    _update_inventory(order)
    _send_notification(order)
    return {"total": total, "status": "processed"}

def _validate_order(order: dict) -> None:
    ...

def _calculate_total(order: dict) -> float:
    ...

def _update_inventory(order: dict) -> None:
    ...

def _send_notification(order: dict) -> None:
    ...
```

**阈值建议**：
- 函数长度：建议 < 50 行，最多不超过 80 行
- 类方法数：建议 < 10 个公开方法
- 嵌套深度：建议 < 4 层

---

### 3. 圈复杂度

**检查模式**：

```python
# 🔴 高复杂度：多层嵌套 if-else
def get_discount(user: dict, order: dict) -> float:
    if user["level"] == "vip":
        if order["total"] > 1000:
            if user["years"] > 5:
                return 0.3
            else:
                return 0.2
        else:
            return 0.1
    elif user["level"] == "gold":
        if order["total"] > 500:
            return 0.15
        else:
            return 0.05
    return 0.0

# ✅ 重构：使用策略模式或查表法
DISCOUNT_TABLE: dict[str, dict[str, float]] = {
    "vip": {"high": 0.2, "low": 0.1, "loyal": 0.3},
    "gold": {"high": 0.15, "low": 0.05},
}

def get_discount(user: dict, order: dict) -> float:
    tier = user["level"]
    if tier == "vip" and user.get("years", 0) > 5:
        return DISCOUNT_TABLE[tier]["loyal"]
    threshold = 1000 if tier == "vip" else 500
    key = "high" if order["total"] > threshold else "low"
    return DISCOUNT_TABLE.get(tier, {}).get(key, 0.0)
```

**阈值建议**：圈复杂度 < 10

---

### 4. 过深嵌套

**检查模式**：

```python
# 🔴 过深嵌套：4+ 层缩进
def process(data: dict) -> str | None:
    if data:
        if "items" in data:
            for item in data["items"]:
                if item.get("active"):
                    if item.get("price") > 0:
                        return item["name"]
    return None

# ✅ 重构：提前返回（Guard Clauses）
def process(data: dict) -> str | None:
    if not data or "items" not in data:
        return None

    for item in data["items"]:
        if not item.get("active") or item.get("price", 0) <= 0:
            continue
        return item["name"]

    return None
```

---

### 5. Pythonic 惯用法

**检查模式**：

```python
# 🔴 非惯用写法
result = []
for item in items:
    if item.active:
        result.append(item.name)

# ✅ 列表推导式
result = [item.name for item in items if item.active]

# 🔴 非惯用写法
index = 0
for item in items:
    print(index, item)
    index += 1

# ✅ enumerate
for index, item in enumerate(items):
    print(index, item)

# 🔴 非惯用写法
d = {}
for item in items:
    if item.category not in d:
        d[item.category] = []
    d[item.category].append(item)

# ✅ defaultdict
from collections import defaultdict
d = defaultdict(list)
for item in items:
    d[item.category].append(item)

# 🔴 手动实现 dataclass
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

# ✅ 使用 dataclass
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

---

### 6. 设计模式建议

**常见场景**：

| 场景 | 推荐模式 | 说明 |
|------|---------|------|
| 多种算法可替换 | Strategy 策略模式 | 消除大量 if-else |
| 对象创建复杂 | Factory 工厂模式 | 解耦创建和使用 |
| 事件通知解耦 | Observer 观察者模式 | 避免直接依赖 |
| 接口多版本兼容 | Adapter 适配器模式 | 统一不同接口 |
| 流式处理 | Builder 构建者模式 | 分步构建复杂对象 |
| 有限状态机 | State 状态模式 | 替代状态判断逻辑 |

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 性能问题 | 代码结构导致的性能问题 | `python-performance-reviewer` 关注运行时性能优化 |
| 类型注解 | 重构后需要更新的类型签名 | `python-typing-reviewer` 负责类型注解审查 |
| 错误处理 | 重构过程中的错误处理改进 | `python-error-handling-reviewer` 关注异常处理逻辑 |
| 架构设计 | 类/模块级别的重构 | `python-architecture-reviewer` 关注系统级架构 |

---

## 审查流程

```
┌─────────────────────────┐
│  1. 重复代码扫描         │
│     相似代码段检测       │
├─────────────────────────┤
│  2. 函数复杂度检查       │
│     长度 / 圈复杂度      │
├─────────────────────────┤
│  3. 嵌套深度检查         │
│     提前返回 / 提取方法  │
├─────────────────────────┤
│  4. Pythonic 惯用法检查  │
│     推导式 / dataclass   │
├─────────────────────────┤
│  5. 设计模式建议         │
│     识别可优化结构       │
└─────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## Python 代码重构审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| utils.py:42-68 | 重复代码（27行） | 提取公共函数 |
| service.py:15-90 | 函数过长（76行） | 拆分为 4 个子函数 |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| api.py:30 | 圈复杂度 15 | 使用策略模式 |
| handler.py:45 | 嵌套 4 层 | 提前返回 |

### 💡 Pythonic 建议

| 位置 | 当前写法 | 建议 |
|------|---------|------|
| models.py:10 | 手写 __init__/__repr__ | 使用 @dataclass |
| utils.py:20 | for + append | 列表推导式 |
| data.py:35 | if key not in dict | collections.defaultdict |
```

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：代码重构审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码的设计质量和重构机会
# 输入：项目代码文件
# 输出：重构审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 检测重复代码段
#   2. 检查函数长度和圈复杂度
#   3. 检查嵌套深度
#   4. 检查是否使用了 Pythonic 惯用法
#   5. 识别可应用设计模式的场景
#
# 常见问题模式：
#   - 重复代码: → 提取公共函数/方法
#   - 函数过长: → 拆分为多个子函数
#   - 高圈复杂度: → 策略模式/查表法
#   - 过深嵌套: → 提前返回/提取方法
#   - 非惯用写法: → dataclass/comprehension/enumerate
#
# AI-Usage-End
```

---

## 触发词

- "重构审查"
- "代码重复检查"
- "重构建议"
- "refactor review"
- "代码质量审查"
- "代码坏味道"
