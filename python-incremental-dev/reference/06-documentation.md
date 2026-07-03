# 文档生成规范

## 文档生成员

专门为代码生成 AI 友好的技术文档。

---

## Docstring 风格

### 模块级文档

```python
"""mathutil — 提供常用的数学运算工具函数。

目的：
  - 简化日常数学运算
  - 提供类型安全的数学函数

示例：

    >>> result = mathutil.add(1, 2)
    >>> result
    3
"""
```

### 函数文档

```python
def add(a: int, b: int) -> int:
    """对两个整数进行加法运算。

    Args:
        a: 第一个加数。
        b: 第二个加数。

    Returns:
        两数之和。

    Raises:
        TypeError: 如果参数不是整数。
    """
    return a + b
```

### 类文档

```python
class Cache(Generic[K, V]):
    """并发安全的内存缓存。

    支持设置 TTL 过期时间，零值可用（无需初始化即可安全使用）。

    Args:
        default_ttl: 默认过期时间（秒），None 表示永不过期。

    Example:

        >>> cache = Cache[str, int]()
        >>> cache.set("key", 42, ttl=60)
        >>> cache.get("key")
        (42, True)
    """

    def __init__(self, default_ttl: float | None = None) -> None:
        ...
```

### 异常文档

```python
# 定义异常类（按惯例以 Error 结尾）
class NotFoundError(Exception):
    """请求的资源不存在。"""

class InvalidInputError(ValueError):
    """输入参数无效。"""

class TimeoutError(Exception):
    """操作超时。"""
```

---

## AI 使用示例块

```python
def add(a: int, b: int) -> int:
    """对两个整数进行加法运算。

    AI-Usage-Begin
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  AI 使用示例：调用 add 函数进行加法运算               ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    场景：计算两个数的和
    输入：a=10, b=20
    输出：result=30

    常见调用模式：
      result = add(10, 20)
      total = add(x, y) + add(z, w)

    边界情况：
      - 正数相加：add(1, 2) → 3
      - 负数相加：add(-1, -2) → -3
      - 零值：add(0, 5) → 5

    AI-Usage-End
    """
    return a + b
```

---

## README 模板

```markdown
# 模块名称

简短描述模块的功能和用途。

## 功能特性

- 特性 1
- 特性 2
- 特性 3

## 安装

```bash
pip install your-package
```

## 快速开始

```python
from your_package import Feature

feature = Feature()
result = feature.do_something()
```

## API 参考

### Feature

创建一个新的 Feature 实例。

```python
feature = Feature(timeout=5.0, retry=3)
```

**参数**：
- `timeout`: 超时时间（秒）
- `retry`: 重试次数

### Feature.do_something

执行主要操作。

```python
result = feature.do_something(request)
```

**参数**：
- `request`: 请求参数

**返回**：
- `Response`: 响应对象

## 错误处理

| 异常 | 说明 |
|------|------|
| `NotFoundError` | 资源不存在 |
| `TimeoutError` | 操作超时 |
| `InvalidInputError` | 输入无效 |

## 示例

更多示例请参考 [examples](./examples/) 目录。
```

---

## CHANGELOG 条目模板

```markdown
## [Unreleased]

### Added
- 新功能描述

### Changed
- 功能变更描述

### Deprecated
- 废弃功能说明

### Fixed
- Bug 修复

### Security
- 安全相关更新
```

---

## 设计决策记录 (ADR)

```markdown
# ADR-001: 使用依赖注入解耦

## 状态
已接受

## 背景
原代码直接依赖具体实现，导致测试困难和模块耦合。

## 决策
使用构造函数注入依赖 Protocol。

## 后果
- 正面：便于单元测试，支持 Mock
- 负面：增加代码复杂度
```

---

## 类型注解文档

```python
from typing import Protocol, TypeVar, Generic

T = TypeVar("T")


class StorageProtocol(Protocol):
    """存储服务接口。"""

    def get(self, key: str) -> bytes: ...
    def set(self, key: str, value: bytes) -> None: ...
    def delete(self, key: str) -> None: ...


class Cache(Generic[T]):
    """泛型缓存，支持任意类型的值。"""

    def get(self, key: str) -> tuple[T, bool]:
        """获取缓存值。

        Returns:
            (value, exists) — value 为缓存值，exists 表示是否存在且未过期。
        """
        ...
```
