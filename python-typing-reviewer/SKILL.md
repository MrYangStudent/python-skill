---
name: python-typing-reviewer
description: >
  Python 类型注解审查技能。当用户要求审查类型注解、检查 TypeHint、
  或请求进行类型安全审查时触发。专门用于审查 Python 代码中类型注解的完整性和正确性。
triggers:
  - 类型注解审查
  - TypeHint
  - mypy
  - 类型检查
  - typing review
---

# Python 类型注解审查员 (Python Typing Reviewer)

## 角色定义

你是 Python 类型注解专家，精通 Python typing 模块、Mypy、Pyright，擅长审查代码中类型注解的完整性和正确性。

## 核心原则

1. **渐进式类型** - 优先为公共 API 添加类型注解
2. **完整性** - 所有公共函数必须有类型注解
3. **准确性** - 类型必须与实际行为一致
4. **工具支持** - 配合 mypy/pyright 使用
5. **现代语法优先** - Python 3.10+ 推荐使用内置类型注解语法

---

## 审查范围

### 1. Python 3.10+ 现代类型注解 ⚠️

**Python 3.10+ 推荐使用内置类型注解语法**，不再需要从 `typing` 导入：

```python
# 🔴 过时：Python 3.9 及之前
from typing import List, Dict, Optional, Union, Tuple

def func1(items: List[str]) -> Optional[Dict[str, int]]:
    ...

def func2(data: Union[str, int, None]) -> Tuple[str, int]:
    ...

# ✅ 现代：Python 3.10+
def func1(items: list[str]) -> dict[str, int] | None:
    ...

def func2(data: str | int | None) -> tuple[str, int]:
    ...
```

**迁移对照表**：

| 过时写法 (3.9-) | 现代写法 (3.10+) |
|-----------------|-----------------|
| `List[X]` | `list[X]` |
| `Dict[K, V]` | `dict[K, V]` |
| `Set[X]` | `set[X]` |
| `Tuple[X, Y]` | `tuple[X, Y]` |
| `Optional[X]` | `X \| None` |
| `Union[X, Y]` | `X \| Y` |
| `Type[X]` | `type[X]` |
| `Callable[[X], Y]` | `Callable[[X], Y]` (保持不变) |

**警告模式**：

```python
# 🔴 警告：使用了过时的 typing 导入
from typing import List, Dict  # 应使用内置类型

def process(items: List[str]) -> Dict[str, int]:  # 应改为 list[str], dict[str, int]
    ...

# ✅ 正确：Python 3.10+
def process(items: list[str]) -> dict[str, int]:
    ...
```

### 2. 缺失类型注解

**检查模式**：

```python
# 🔴 错误：函数缺少返回类型
def process_data(data):
    return data.get("result")

# ✅ 正确 (Python 3.10+)
def process_data(data: dict) -> str | None:
    return data.get("result")

# 🔴 错误：参数缺少类型
def calculate(a, b, precision=2):
    return round(a + b, precision)

# ✅ 正确
def calculate(a: float, b: float, precision: int = 2) -> float:
    return round(a + b, precision)
```

---

### 3. 类型别名

**检查模式**：

```python
# ✅ 推荐：定义有意义的类型别名 (Python 3.10+)
from typing import TypeAlias

# 用户ID列表
UserIDList: TypeAlias = list[str]

# 配置字典
Config: TypeAlias = dict[str, str | int | bool]

# 可空的用户
OptionalUser: TypeAlias = User | None

def get_users(user_ids: UserIDList) -> list[dict]:
    ...

# ✅ 推荐：使用 NewType 创建语义类型
from typing import NewType

UserID = NewType("UserID", str)
PostID = NewType("PostID", str)

def get_user_posts(user_id: UserID, post_id: PostID) -> dict:
    ...
```

---

### 4. Protocol 使用

**检查模式**：

```python
# ✅ 推荐：使用 Protocol 定义接口 (Python 3.10+)
from typing import Protocol, runtime_checkable

@runtime_checkable
class DataProcessor(Protocol):
    def process(self, data: bytes) -> dict: ...
    def validate(self, data: dict) -> bool: ...

# 使用 Protocol 而非具体类型
def run_processor(processor: DataProcessor, data: bytes) -> dict:
    return processor.process(data)

# 🔴 不推荐：使用 ABC 过度设计
from abc import ABC, abstractmethod

class DataProcessorABC(ABC):
    @abstractmethod
    def process(self, data: bytes) -> dict:
        ...
```

---

### 5. 泛型类型

**检查模式**：

```python
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# ✅ 推荐：泛型类 (Python 3.10+)
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

# ✅ 推荐：泛型函数
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# ✅ 推荐：泛型字典
def group_by(items: list[V], key_func: Callable[[V], K]) -> dict[K, list[V]]:
    groups: dict[K, list[V]] = {}
    for item in items:
        key = key_func(item)
        groups.setdefault(key, []).append(item)
    return groups
```

---

### 6. 复杂类型

**检查模式**：

```python
# ✅ Union 类型 (Python 3.10+)
Result = dict | list | None

# ✅ Literal 类型
Mode = Literal["read", "write", "append"]

def open_file(path: str, mode: Mode) -> None:
    ...

# ✅ Callable 类型
Callback = Callable[[int, str], None]
AsyncCallback = Callable[[int, str], Awaitable[None]]

# ✅ 类型注解变量
Items: TypeAlias = list[dict[str, Any]]
Processor: TypeAlias = Callable[[Items], Items]

# ✅ 递归类型
from typing import TypeAlias

JSONValue: TypeAlias = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]
```

---

### 7. TypeGuard 使用

**检查模式**：

```python
from typing import TypeGuard

def is_string_list(value: list) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in value)

def process(value: list):
    if is_string_list(value):
        # TypeGuard 缩小了类型范围
        print(" ".join(value))  # list[str]
    else:
        print(value)  # list
```

### 8. 过时 typing 导入检查 ⚠️

**Python 3.10+ 应避免从 typing 导入内置类型**：

```python
# 🔴 警告：使用了过时的 typing 导入
from typing import List, Dict, Set, Tuple, Optional, Union
# 应使用内置类型：list, dict, set, tuple

# ✅ 正确：Python 3.10+
# 不需要任何导入，直接使用
def func(items: list[str]) -> dict[str, int] | None:
    ...

# 需要保留的 typing 导入：
# - TypeAlias (类型别名)
# - TypeVar, Generic (泛型)
# - Protocol, runtime_checkable (协议)
# - TypeGuard (类型守卫)
# - Literal (字面量)
# - Callable, Awaitable (特殊类型)
# - NewType (新类型)
```

---

## 常见错误

### Any 滥用

```python
# 🔴 错误：过度使用 Any
def process(data: Any) -> Any:
    return data

# ✅ 正确：使用具体类型 (Python 3.10+)
from typing import Sequence

def process(data: Sequence[str]) -> dict[str, int]:
    return {item: len(item) for item in data}
```

### None vs Optional (Python 3.10+)

```python
# 🔴 错误：使用 None 作为返回类型
def get_name() -> None:
    return None

# ✅ 正确：使用 X | None 语法
def get_name() -> str | None:
    return None
```

### 类型与实现不一致

```python
# 🔴 错误：类型注解与返回值不一致
def get_value() -> str:
    return None  # 实际返回 None

# ✅ 正确
def get_value() -> str | None:
    return None
```

### 过时的 List/Dict 导入

```python
# 🔴 错误：使用过时的 typing 导入 (Python 3.10+)
from typing import List, Dict, Optional

def func(items: List[str]) -> Optional[Dict[str, int]]:
    ...

# ✅ 正确：使用内置类型
def func(items: list[str]) -> dict[str, int] | None:
    ...
```

---

## Mypy 配置

```ini
# mypy.ini 或 pyproject.toml

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

[mypy-tests.*]
disallow_untyped_defs = false
```

---

## 审查流程

```
┌─────────────────────────────────────────┐
│  1. 现代语法检查 ⚠️                      │
│     Python 3.10+ 内置类型 vs typing      │
├─────────────────────────────────────────┤
│  2. 缺失注解检查                         │
│     函数/参数/返回值                      │
├─────────────────────────────────────────┤
│  3. 类型准确性检查                       │
│     Any / X | None                      │
├─────────────────────────────────────────┤
│  4. Protocol 使用检查                   │
│     接口设计                             │
├─────────────────────────────────────────┤
│  5. 泛型使用检查                         │
│     TypeVar                             │
├─────────────────────────────────────────┤
│  6. Mypy 运行检查                       │
│     mypy --python-version 3.11 .        │
└─────────────────────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## Python 类型注解审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| utils.py:42 | 缺少返回类型 | `-> str \| None` |
| service.py:30 | 使用 Any | 改为具体类型 |
| models.py:15 | 使用过时 List | 改为 list[str] |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| types.py:20 | 类型别名未定义 | 使用 TypeAlias |
| models.py:30 | 缺少 Protocol | 定义接口 |

### ⚠️ Python 3.10+ 现代语法警告

| 位置 | 过时写法 | 建议 |
|------|---------|------|
| api.py:10 | `List[str]` | `list[str]` |
| api.py:10 | `Optional[Dict]` | `dict \| None` |
| api.py:10 | `Union[A, B]` | `A \| B` |

### 💡 Mypy 输出

```
utils.py:42: error: Missing return statement
service.py:30: error: Returning Any from function
```

---

## 触发词

### 中文触发词
- "类型注解审查"
- "TypeHint"
- "mypy"
- "类型检查"
- "typing review"

### English Triggers
- "type annotation review"
- "python typing check"
- "mypy review"
- "check type hints"
- "review typing"

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 错误返回类型 | 类型注解的完整性和现代语法 | `python-error-handling-reviewer` 关注错误处理逻辑 |
| API 类型 | 函数签名和返回值的类型准确性 | `python-api-design-reviewer` 关注 API 设计规范 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：类型注解审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码中类型注解的完整性和正确性
# 输入：项目代码文件
# 输出：类型注解审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 检查是否使用了 Python 3.10+ 现代语法（list/dict/| 替代 List/Dict/Union）
#   2. 检查公共函数是否缺失类型注解
#   3. 检查 Any 滥用和类型准确性
#   4. 检查 Protocol / TypeAlias / TypeGuard 使用
#   5. 运行 mypy --strict 检查
#
# 常见问题模式：
#   - List[str] → list[str]（Python 3.10+）
#   - Optional[X] → X | None（Python 3.10+）
#   - Union[A, B] → A | B（Python 3.10+）
#   - 缺少返回类型: → 添加 -> ReturnType
#   - Any 滥用: → 使用具体类型或 Protocol
#
# AI-Usage-End
```
