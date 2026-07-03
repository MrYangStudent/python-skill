# 工具函数参考

## 核心原则

1. **标准库优先** - 优先使用 Python 标准库（`itertools`、`collections`、`functools` 等）
2. **类型注解** - 所有公开函数必须有完整类型注解
3. **Docstring** - 每个导出函数必须有 docstring
4. **YAGNI 门槛** - 重复 ≥3 次才封装，≤2 款内联即可

---

## 封装决策树

```
是否重复 ≥3 次？
  → 否：不封装，内联使用
  → 是：逻辑是否稳定？
    → 否：用 lambda/回调，不抽象
    → 是：能否用标准库替代？
      → 能：直接用标准库（itertools/collections/functools）
      → 不能：是否涉及泛型/多类型？
        → 是：使用 TypeVar/Generic
        → 否：简单封装为独立函数
```

---

## 标准库替代清单（优先使用）

| 需求 | Go 需封装 | Python 标准库直接可用 |
|------|-----------|----------------------|
| 列表映射 | `slicex.Map` | `map()` 或 `[f(x) for x in lst]` |
| 列表过滤 | `slicex.Filter` | `filter()` 或 `[x for x in lst if cond]` |
| 去重 | `slicex.Unique` | `list(set(lst))` 或 `dict.fromkeys(lst)` |
| 分组 | `slicex.GroupBy` | `itertools.groupby`（需先排序）或手动循环 |
| 分块 | `slicex.Chunk` | 循环 `lst[i:i+n]` |
| 排序 | `slicex.Sort` | `sorted()` 或 `list.sort()` |
| 展平 | `slicex.Flatten` | `itertools.chain.from_iterable` |
| Map 键 | `mapx.Keys` | `dict.keys()` |
| Map 值 | `mapx.Values` | `dict.values()` |
| Map 合并 | `mapx.Merge` | `{**a, **b}` 或 `a | b`（3.9+） |
| 反转 Map | `mapx.Invert` | `{v: k for k, v in d.items()}` |
| 分页 | `pagex` | 自定义分页函数 |
| 重试 | `retryx` | 自定义或 `tenacity`（需评估引入） |
| 缓存 | `cachex` | `functools.lru_cache` / `cachetools`（需评估） |
| 日期格式 | `timex` | `datetime.strftime/strptime` |
| 类型转换 | `convx` | `int()`/`str()`/`bool()` + 自定义校验 |
| 去重过滤 | `slicex.Contains` | `x in set` 或 `x in lst` |
| 查找 | `slicex.Find` | `next((x for x in lst if cond), None)` |
| 计数器 | `Counter` | `collections.Counter` |
| 双端队列 | `deque` | `collections.deque` |
| 合并字典 | `ChainMap` | `collections.ChainMap` |
| 命名元组 | `NamedTuple` | `typing.NamedTuple` 或 `dataclasses.dataclass` |
| 减少聚合 | `Reduce` | `functools.reduce` |

---

## 需要自定义封装的场景

以下场景 Python 标准库无法直接覆盖，需要自定义封装：

### HTTP 客户端封装

```python
"""HTTP 客户端封装，支持超时、重试、统一异常处理."""

import httpx
from typing import Any, TypeVar

T = TypeVar("T")


class HttpClient:
    """统一 HTTP 客户端，支持超时和 JSON 序列化。"""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """发送 GET 请求并解析 JSON 响应。"""
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, *, body: Any) -> dict[str, Any]:
        """发送 POST 请求并解析 JSON 响应。"""
        response = self._client.post(path, json=body)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """关闭客户端连接。"""
        self._client.close()
```

### 重试机制

```python
"""重试工具，支持指数退避."""

import asyncio
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_sync(
    fn: Callable[[], T],
    max_attempts: int = 3,
    initial_wait: float = 0.1,
    multiplier: float = 2.0,
    max_wait: float = 10.0,
) -> T:
    """同步重试函数，指数退避。"""
    wait = initial_wait
    last_exception: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if attempt == max_attempts:
                break
            time.sleep(wait)
            wait = min(wait * multiplier, max_wait)

    raise RuntimeError(f"重试 {max_attempts} 次后失败: {last_exception}") from last_exception


async def retry_async(
    fn: Callable[[], T],
    max_attempts: int = 3,
    initial_wait: float = 0.1,
    multiplier: float = 2.0,
    max_wait: float = 10.0,
) -> T:
    """异步重试函数，指数退避。"""
    wait = initial_wait
    last_exception: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await fn()
        except Exception as e:
            last_exception = e
            if attempt == max_attempts:
                break
            await asyncio.sleep(wait)
            wait = min(wait * multiplier, max_wait)

    raise RuntimeError(f"重试 {max_attempts} 次后失败: {last_exception}") from last_exception
```

### 分页工具

```python
"""分页参数和结果封装."""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PageParams:
    """分页请求参数。"""
    page: int = 1
    page_size: int = 20

    def offset(self) -> int:
        """计算 SQL OFFSET。"""
        if self.page <= 0:
            return 0
        return (self.page - 1) * self.limit()

    def limit(self) -> int:
        """计算 SQL LIMIT，限制最大值。"""
        if self.page_size <= 0:
            return 20
        if self.page_size > 100:
            return 100
        return self.page_size


@dataclass
class PageResult(Generic[T]):
    """分页响应结果。"""
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


def new_page_result(items: list[T], total: int, params: PageParams) -> PageResult[T]:
    """创建分页结果。"""
    limit = params.limit()
    pages = total // limit + (1 if total % limit > 0 else 0)
    return PageResult(items=items, total=total, page=params.page, page_size=limit, pages=pages)
```

### 参数验证器

```python
"""链式参数验证器."""

from typing import Any


class Validator:
    """链式参数验证器。"""

    def __init__(self, value: Any, field_name: str = "value") -> None:
        self._value = value
        self._field_name = field_name
        self._errors: list[str] = []

    def not_blank(self) -> "Validator":
        """验证非空。"""
        if not self._value or (isinstance(self._value, str) and not self._value.strip()):
            self._errors.append(f"{self._field_name} 不能为空")
        return self

    def min_len(self, length: int) -> "Validator":
        """验证最小长度。"""
        if isinstance(self._value, (str, list)) and len(self._value) < length:
            self._errors.append(f"{self._field_name} 长度不能小于 {length}")
        return self

    def max_len(self, length: int) -> "Validator":
        """验证最大长度。"""
        if isinstance(self._value, (str, list)) and len(self._value) > length:
            self._errors.append(f"{self._field_name} 长度不能大于 {length}")
        return self

    def email(self) -> "Validator":
        """验证邮箱格式。"""
        import re
        if isinstance(self._value, str) and not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", self._value):
            self._errors.append(f"{self._field_name} 邮箱格式无效")
        return self

    def mobile(self) -> "Validator":
        """验证手机号格式（中国大陆）。"""
        import re
        if isinstance(self._value, str) and not re.match(r"^1[3-9]\d{9}$", self._value):
            self._errors.append(f"{self._field_name} 手机号格式无效")
        return self

    def validate(self) -> None:
        """执行验证，有错误时抛出 ValueError。"""
        if self._errors:
            raise ValueError("; ".join(self._errors))
```

---

## 禁止封装的场景

| 场景 | 原因 | 正确做法 |
|------|------|----------|
| `str.lower()` | 标准库已完美覆盖 | 直接调用 `s.lower()` |
| `len(lst)` | 标准库已完美覆盖 | 直接调用 `len(lst)` |
| `json.loads/dumps` | 标准库已完美覆盖 | 直接调用 |
| `datetime.now()` | 标准库已完美覆盖 | 直接调用 |
| 简单类型转换 `int(x)` | 标准库已完美覆盖 | 直接调用 |
| 列表推导 `[f(x) for x in lst]` | Python 原生语法比封装更清晰 | 直接使用列表推导 |
