---
name: python-doc-generator
description: >
  Python 技术文档生成技能。当用户要求为代码生成文档、编写 Docstring 注释、创建 README、
  或请求生成 AI 友好的使用示例时触发。专门用于生成对 AI 工具（如 Cline、Cursor）
  可学习的规范文档。
triggers:
  - 生成文档
  - 写注释
  - 文档生成员
  - 生成 README
  - AI 使用示例
  - docstring
---

# Python 文档生成器 (Python Doc Generator)

## 技能定位

专门为 Python 代码生成 AI 友好的技术文档，使文档不仅对人类可读，还能被 AI 工具学习引用。

## 核心任务

### 1. Docstring 风格注释

Python 支持多种 Docstring 风格，推荐使用 **Google 风格**或 **NumPy 风格**：

#### Google 风格

```python
def add(a: int, b: int) -> int:
    """对两个整数进行加法运算。

    Args:
        a: 第一个加数
        b: 第二个加数

    Returns:
        两数之和

    Raises:
        TypeError: 当参数类型不正确时

    Examples:
        >>> add(1, 2)
        3
        >>> add(-1, -2)
        -3
    """
    return a + b
```

#### NumPy 风格

```python
def add(a: int, b: int) -> int:
    """
    对两个整数进行加法运算。

    Parameters
    ----------
    a : int
        第一个加数
    b : int
        第二个加数

    Returns
    -------
    int
        两数之和

    Raises
    ------
    TypeError
        当参数类型不正确时

    Examples
    --------
    >>> add(1, 2)
    3
    """
    return a + b
```

### 2. README 章节

生成标准化的 README 章节：

```markdown
## 模块名称

### 目的
简要说明模块的核心功能和价值（1-2 句话）。

### 快速开始
```python
# 最简使用示例
```

### 示例
```python
# 完整使用示例，展示多种场景
```

### API 参考
| 函数 | 说明 | 示例 |
|------|------|------|
| function_name | 功能说明 | `function_name(args)` |
```

### 3. AI 使用示例块

生成包含在注释中的 AI 友好示例，专门供 Cline/Cursor 等工具学习：

```python
def process_data(user_id: str, data: list) -> dict:
    """处理用户数据。
    
    Args:
        user_id: 用户唯一标识符
        data: 待处理的数据列表
    
    Returns:
        包含处理结果的字典
    
    Raises:
        ValueError: 当 user_id 为空时
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    return {"user_id": user_id, "count": len(data)}


# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：调用 process_data 函数                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：处理指定用户的数据
# 输入：user_id="user-123", data=[1, 2, 3]
# 输出：{"user_id": "user-123", "count": 3}
#
# 常见调用模式：
#   result = process_data("user-1", [1, 2, 3])
#   result = process_data(user_id, get_data())
#
# 边界情况：
#   - 空数据：process_data("id", []) → {"user_id": "id", "count": 0}
#   - 空 user_id：抛出 ValueError
#
# AI-Usage-End
```

### 4. 类文档

```python
class DataProcessor:
    """数据处理器，用于处理和转换业务数据。

    该类提供统一的数据处理接口，支持多种数据格式的转换和验证。

    Attributes:
        name: 处理器名称
        config: 配置字典
        _data: 内部数据存储

    Example:
        >>> processor = DataProcessor("processor-1", {"timeout": 30})
        >>> result = processor.process([1, 2, 3])
        >>> print(result)
        {'name': 'processor-1', 'count': 3}
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """初始化数据处理器。

        Args:
            name: 处理器名称，不能为空
            config: 可选配置字典，默认值为空字典
        """
        if not name:
            raise ValueError("name cannot be empty")
        
        self.name = name
        self.config = config or {}
        self._data: List[Any] = []
    
    def process(self, data: List[Any]) -> Dict[str, Any]:
        """处理数据。

        Args:
            data: 待处理的数据列表

        Returns:
            包含处理结果的字典

        Raises:
            ValueError: 当数据为空时
        """
        if not data:
            raise ValueError("data cannot be empty")
        
        return {
            "name": self.name,
            "count": len(data),
            "data": data,
        }
```

## 工作流程

1. **分析代码结构**
   - 识别导出的函数、类、方法
   - 确定参数类型、返回值类型、异常类型
   - 分析函数依赖和副作用

2. **生成 Docstring 注释**
   - 编写类级别注释
   - 为每个公共方法添加注释
   - 说明参数、返回值、可能的错误

3. **生成 README 内容**
   - 编写目的说明
   - 提供快速开始代码
   - 添加完整使用示例

4. **生成 AI 使用示例**
   - 在函数注释中添加 AI-Usage 块
   - 包含场景描述、输入输出示例
   - 列举常见调用模式和边界情况

## Docstring 规范

### 必须包含的内容

| 元素 | 说明 |
|------|------|
| 简短描述 | 一句话说明函数/类的功能 |
| Args | 参数列表及说明 |
| Returns | 返回值说明 |
| Raises | 可能抛出的异常 |
| Examples | 使用示例（可选但推荐） |

### 类型注解

```python
from typing import Optional, List, Dict, Any, Union, Callable, TypeVar

T = TypeVar("T")

# 基本类型
def func(a: int, b: str) -> bool: ...

# 容器类型
def func(items: List[int]) -> Dict[str, Any]: ...

# Optional
def func(name: Optional[str] = None) -> str: ...

# Union
def func(value: Union[int, str]) -> str: ...

# Callable
def func(callback: Callable[[int], str]) -> None: ...

# 泛型
def func(items: List[T]) -> T: ...
```

## 质量标准

- **完整性**：覆盖所有公共 API
- **准确性**：参数/返回值描述与实际一致
- **可学习性**：AI 示例具体、可执行
- **格式统一**：遵循 Google/NumPy docstring 规范

## 触发词

- "生成文档"
- "写注释"
- "生成 README"
- "AI 使用示例"
