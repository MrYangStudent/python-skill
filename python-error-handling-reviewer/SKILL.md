---
name: python-error-handling-reviewer
description: >
  Python 错误处理审查技能。当用户要求审查代码错误处理、检查异常使用、
  或请求诊断类型错误等问题时触发。专门用于发现和修复 Python 代码中
  的错误处理缺陷，遵循 Python 异常最佳实践。
triggers:
  - 错误处理审查
  - 检查异常
  - 审查代码
  - 错误处理审查员
  - 检查 try-except
---

# Python 错误处理审查员 (Error Handling Reviewer)

## 技能定位

Python 错误处理专家，遵循 Python 异常哲学。检测代码中的错误处理问题并提供修复建议。

## 审查检查项

### 1. 裸 except 子句

**检查模式：**
```python
# ✗ 错误示例 - 裸 except
try:
    result = risky_function()
except:
    pass

# ✗ 错误示例 - 捕获所有异常
try:
    result = risky_function()
except Exception:
    pass

# ✓ 正确示例 - 捕获具体异常
try:
    result = risky_function()
except ValueError as e:
    raise ValueError(f"invalid value: {e}") from e
except TimeoutError as e:
    raise TimeoutError(f"operation timed out: {e}") from e
```

**修复建议：**
- 始终捕获具体异常类型
- 使用 `except Exception` 时需添加注释说明原因
- 在 except 块中记录日志或重新抛出

### 2. 异常被静默忽略

**检查模式：**
```python
# ✗ 错误示例
try:
    send_notification(user)
except NotificationError:
    pass  # 静默忽略

# ✓ 正确示例
try:
    send_notification(user)
except NotificationError as e:
    logger.warning(f"notification failed for user {user}: {e}")
    # 或重新抛出
    raise
```

**修复建议：**
- 至少记录日志
- 如果确实不需要处理，使用注释说明原因
- 考虑是否需要传播给调用方

### 3. 异常信息不完整

**检查模式：**
```python
# ✗ 缺少上下文
raise ValueError("error")

# ✓ 提供足够上下文
raise ValueError(f"validate_user: user_id '{user_id}' is invalid: {reason}")

# ✗ 裸 raise
try:
    do_something()
except SomeError:
    raise  # 丢失原始 traceback 上下文

# ✓ 使用 raise from
try:
    do_something()
except SomeError as e:
    raise ValueError("operation failed") from e
```

**修复建议：**
- 异常消息应能回答：哪里、什么、为什么
- 使用 `raise ... from e` 保留原始异常链
- 使用结构化日志记录异常

### 4. 类型注解缺失

> **注意**：类型注解的详细审查请使用 `python-typing-reviewer` 技能，本节仅检查与错误处理直接相关的类型问题。

**检查模式：**
```python
# ✗ 缺少类型注解
def process_data(data):
    return data.get("result")

# ✓ 完整类型注解（Python 3.10+）
def process_data(data: dict[str, object]) -> str | None:
    return data.get("result")

# ✗ 不一致的类型注解
def function(a: str) -> int:  # 实际返回 None
    return None

# ✓ 标注可空返回
def function(a: str) -> str | None:
    return None
```

**修复建议：**
- 所有公共函数必须有类型注解
- 使用 `X | None` 明确可能返回 None 的情况（Python 3.10+）
- 定期运行 mypy 检查

### 5. 参数校验

**检查模式：**
```python
# ✗ 未校验参数
def find_user(user_id: str) -> dict:
    user = db.find(user_id)  # user_id 为空时会怎样？
    return user

# ✓ 参数校验
def find_user(user_id: str) -> dict:
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    user = db.find(user_id)
    if user is None:
        raise KeyError(f"user not found: {user_id}")
    return user
```

**修复建议：**
- 在函数入口处进行参数校验
- 使用自定义异常类表达业务错误
- 遵循 "fail fast" 原则

### 6. 资源泄漏

**检查模式：**
```python
# ✗ 错误示例 - 文件未关闭
def read_file(path: str) -> str:
    f = open(path, "r")
    data = f.read()
    # f 未关闭
    return data

# ✓ 正确示例 - 使用 context manager
def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

# ✗ 错误示例 - 连接未关闭
def query_database():
    conn = create_connection()
    result = conn.execute(query)
    # conn 未关闭
    return result

# ✓ 正确示例
def query_database():
    with create_connection() as conn:
        return conn.execute(query)
```

**修复建议：**
- 始终使用 context manager（with 语句）
- 确保所有资源在异常情况下也能正确关闭
- 使用 `finally` 块处理清理逻辑

## 工作流程

1. **扫描代码**
   - 搜索 `except:` 和 `except Exception:`
   - 搜索 `raise` 语句
   - 搜索 `open(` 调用
   - 搜索缺少类型注解的函数

2. **分析每个问题**
   - 确定问题类型
   - 评估严重程度（Error/Warning/Suggestion）
   - 检查是否有误报

3. **生成报告**
   ```
   ## Python 错误处理审查报告
   
   ### 🔴 Error（必须修复）
   - 文件: xxx.py:123
     问题: 使用裸 except
     代码: `except:`
     建议: 改为 `except SpecificException:`
   
   ### 🟡 Warning（建议修复）
   - 文件: xxx.py:456
     问题: 异常信息不完整
     代码: `raise ValueError("error")`
     建议: `raise ValueError(f"context: {detail}")`
   
   ### 💡 Suggestion（可选改进）
   - 文件: xxx.py:789
     问题: 缺少类型注解
     代码: `def function(data)`
     建议: `def function(data: dict) -> str:`
   ```

## 严重程度定义

| 级别 | 描述 | 示例 |
|------|------|------|
| 🔴 Error | 必须修复 | 裸 except、资源泄漏 |
| 🟡 Warning | 建议修复 | 异常信息不完整、缺少类型注解 |
| 💡 Suggestion | 可选改进 | 代码可优化 |

## 常见模式库

### 正确示例

```python
# 1. 标准异常处理
try:
    result = risky_operation()
except ValueError as e:
    raise ValueError(f"operation failed: {e}") from e

# 2. 使用 context manager
with open(path, "r") as f:
    data = f.read()

# 3. 自定义异常
class ValidationError(Exception):
    """验证异常。"""
    pass

# 4. 可选类型标注（Python 3.10+）
def get_value() -> str | None:
    return None

# 5. 结构化日志
logger.error(
    "operation failed",
    extra={
        "operation": "db.query",
        "error": str(e),
        "duration": elapsed,
    }
)
```

### 错误示例

```python
# 1. 裸 except
try:
    do_something()
except:  # ✗
    pass

# 2. 静默忽略
try:
    send_notification()
except NotificationError:  # ✗
    pass

# 3. 空异常消息
raise ValueError("")  # ✗

# 4. 资源泄漏
f = open(path, "r")  # ✗
data = f.read()
# 未关闭

# 5. 缺少类型注解
def function(data):  # ✗
    return data.get("key")
```

---

## AI 使用示例

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 类型注解 | 与错误处理直接相关的类型（如返回值可空） | `python-typing-reviewer` 负责完整的类型审查 |
| 资源关闭 | 未使用 context manager 导致的资源泄漏 | `python-database-reviewer` 负责数据库连接关闭 |
| 异常日志 | 异常处理中的日志记录规范 | `python-logging-reviewer` 负责完整的日志规范 |
| 安全漏洞 | 错误信息泄露（如堆栈暴露） | `python-security-reviewer` 负责完整的安全审查 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：错误处理审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码中的错误处理质量
# 输入：项目代码文件
# 输出：错误处理审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 扫描所有 try-except 块，检查裸 except
#   2. 检查异常是否被静默忽略（pass）
#   3. 检查异常消息是否包含足够上下文
#   4. 检查 raise from 链是否正确
#   5. 检查资源是否使用 context manager
#
# 常见问题模式：
#   - 裸 except: → 改为 except SpecificException
#   - 静默忽略: → 至少记录 logger.warning
#   - 缺少上下文: → raise ValueError(f"context: {detail}")
#   - 资源泄漏: → 使用 with 语句
#   - 缺少 raise from: → raise ... from e
#
# AI-Usage-End
```

---

## 触发词

- "错误处理审查"
- "检查异常"
- "审查代码"
- "错误处理审查员"
