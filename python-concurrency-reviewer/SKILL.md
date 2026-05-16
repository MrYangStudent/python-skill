---
name: python-concurrency-reviewer
description: >
  Python 并发安全审查技能。当用户要求审查代码并发安全、检查线程安全、
  或请求诊断异步编程、锁使用等问题时触发。专门用于发现和修复 Python 代码中
  的并发缺陷，理解 GIL 和异步编程模型。
triggers:
  - 并发审查
  - 线程安全
  - async await
  - 并发安全审查
  - Python并发审查员
  - asyncio
---

# Python 并发审查员 (Python Concurrency Reviewer)

## 技能定位

Python 并发安全专家，精通 Python GIL、asyncio、threading 和 multiprocessing 模块。检测代码中的并发问题并提供修复建议。

## 核心概念

### Python GIL 理解

Python 的 GIL（全局解释器锁）限制了同一时刻只有一个线程执行 Python 字节码：
- **I/O 密集型**：多线程有效（等待 I/O 时释放 GIL）
- **CPU 密集型**：多线程无效，考虑 multiprocessing
- **异步代码**：asyncio 在单线程内实现并发

### 适合场景

| 场景 | 推荐方案 |
|------|----------|
| I/O 等待（网络请求、文件读写） | asyncio / aiohttp |
| CPU 密集型计算 | multiprocessing |
| 需要共享状态 | threading + Lock |
| 无状态请求处理 | 无并发问题 |

---

## 审查检查清单

### 1. 异步函数正确性（🟡 警告）

**检查模式：**
```python
# ✗ 错误示例 - 在异步函数中使用阻塞调用
import asyncio
import requests  # 同步库

async def fetch_data(url: str) -> dict:
    response = requests.get(url)  # ✗ 阻塞整个事件循环
    return response.json()

# ✓ 正确示例 - 使用异步库
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# ✗ 错误示例 - async 函数缺少 await
async def process():
    result = some_async_function()  # ✗ 忘记 await
    return result

# ✓ 正确示例
async def process():
    result = await some_async_function()
    return result
```

**修复建议：**
- 异步函数必须使用 `await` 等待异步操作
- 使用 `aiohttp` 代替 `requests`
- 使用 `asyncio.to_thread()` 包装同步阻塞调用

---

### 2. 线程安全（🔴 紧急）

**检查模式：**
```python
# ✗ 错误示例 - 非线程安全的共享状态
class Counter:
    def __init__(self) -> None:
        self.count = 0  # ✗ 无保护
    
    def increment(self) -> None:
        self.count += 1  # ✗ 不是原子操作

# ✓ 正确示例 - 使用 Lock
import threading

class SafeCounter:
    def __init__(self) -> None:
        self._count = 0
        self._lock = threading.Lock()
    
    def increment(self) -> None:
        with self._lock:
            self._count += 1
    
    @property
    def count(self) -> int:
        with self._lock:
            return self._count

# ✗ 错误示例 - 锁使用不当
class BrokenCache:
    def __init__(self) -> None:
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[str]:
        if key not in self._cache:  # ✗ 检查和写入之间无锁
            return None
        return self._cache[key]
    
    def set(self, key: str, value: str) -> None:
        with self._lock:  # ✗ 锁范围不完整
            self._cache[key] = value

# ✓ 正确示例 - 完整的锁保护
class SafeCache:
    def __init__(self) -> None:
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[str]:
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key: str, value: str) -> None:
        with self._lock:
            self._cache[key] = value
```

**修复建议：**
- 共享可变状态必须使用 `threading.Lock` 或 `threading.RLock`
- 使用 `with lock:` 确保锁正确释放
- 避免在持锁期间执行阻塞操作

---

### 3. 异步锁的使用（🟡 警告）

**检查模式：**
```python
# ✗ 错误示例 - 在 async 中使用 threading.Lock
import asyncio
import threading

class AsyncCounter:
    def __init__(self) -> None:
        self._lock = threading.Lock()  # ✗ 同步锁
    
    async def increment(self) -> None:
        with self._lock:  # ✗ 阻塞事件循环
            self._count += 1

# ✓ 正确示例 - 使用 asyncio.Lock
class AsyncCounter:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._count = 0
    
    async def increment(self) -> None:
        async with self._lock:
            self._count += 1

# ✗ 错误示例 - 在锁外修改共享状态
class AsyncCache:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._cache = {}
    
    async def get_or_set(self, key: str) -> str:
        if key in self._cache:  # ✗ 检查和写入分离
            return self._cache[key]
        
        value = await fetch_value(key)
        
        async with self._lock:
            self._cache[key] = value  # ✓ 在锁内写入
        
        return value
```

**修复建议：**
- 异步代码使用 `asyncio.Lock` 而非 `threading.Lock`
- 锁范围必须覆盖完整的检查-修改操作
- 使用 `async with` 语法

---

### 4. 异步上下文管理（🟡 警告）

**检查模式：**
```python
# ✗ 错误示例 - 使用同步 context manager
async def process():
    session = create_session()  # 同步创建
    try:
        await do_something(session)
    finally:
        session.close()  # ✗ 同步关闭

# ✓ 正确示例 - 实现 __aenter__ 和 __aexit__
class AsyncResource:
    async def __aenter__(self) -> "AsyncResource":
        self._connection = await connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._connection.close()

# ✓ 使用异步 context manager
async def process():
    async with AsyncResource() as resource:
        await do_something(resource)
```

---

### 5. 竞态条件检测（🔴 紧急）

**检查模式：**
```python
# ✗ 错误示例 - check-then-act 竞态
def withdraw(account: Account, amount: float) -> None:
    if account.balance >= amount:  # ✗ 检查
        time.sleep(0.001)  # ✗ 其他线程可能修改
        account.balance -= amount  # ✗ 操作
    else:
        raise ValueError("insufficient funds")

# ✓ 正确示例 - 使用锁保护整个操作
def withdraw(account: Account, amount: float) -> None:
    with account._lock:
        if account.balance >= amount:
            account.balance -= amount
        else:
            raise ValueError("insufficient funds")
```

**修复建议：**
- check-then-act 操作必须在同一锁内完成
- 使用原子操作或事务
- 添加超时防止死锁

---

### 6. 异步任务管理（🟡 警告）

**检查模式：**
```python
# ✗ 错误示例 - 未管理的任务
async def process_batch(items: list):
    for item in items:
        asyncio.create_task(process(item))  # ✗ 任务可能丢失

# ✓ 正确示例 - 收集任务结果
async def process_batch(items: list):
    tasks = [process(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# ✗ 错误示例 - 任务取消未处理
async def long_running():
    try:
        await asyncio.sleep(1000)
    except asyncio.CancelledError:
        # ✗ 未清理资源
        raise

# ✓ 正确示例 - 正确处理取消
async def long_running():
    try:
        await asyncio.sleep(1000)
    except asyncio.CancelledError:
        cleanup()  # ✓ 清理资源
        raise  # 重新抛出取消信号
```

**修复建议：**
- 使用 `asyncio.gather()` 或 `asyncio.TaskGroup` 管理任务
- 正确处理 `asyncio.CancelledError`
- 添加超时防止任务无限等待

---

## 工作流程

1. **扫描代码**
   - 搜索 `async def`、`await`
   - 搜索 `threading.Lock`、`threading.RLock`
   - 搜索 `threading.Thread`
   - 搜索共享可变状态

2. **分析每个问题**
   - 确定并发模型
   - 评估竞态条件风险
   - 检查资源泄漏可能性

3. **生成报告**
   ```
   ## Python 并发安全审查报告
   
   ### 🔴 紧急（必须修复）
   - 文件: xxx.py:123
     问题: 非线程安全的共享状态
     代码: `self.count += 1`
     风险: 数据竞争
     修复: 使用 threading.Lock 保护
   
   ### 🟡 警告（建议修复）
   - 文件: xxx.py:456
     问题: async 函数中使用同步库
     代码: `requests.get(url)`
     风险: 阻塞事件循环
     修复: 改用 aiohttp
   ```

---

## 快速检查命令

```bash
# 类型检查
mypy --check-untyped-defs .

# 并发测试
python -m pytest tests/ -v

# 检查 asyncio 代码
python -m py_compile async_module.py
```

## 最佳实践

1. **I/O 密集型**：使用 asyncio + aiohttp
2. **CPU 密集型**：使用 multiprocessing
3. **共享状态**：使用 threading.Lock 保护
4. **异步代码**：使用 asyncio.Lock
5. **任务管理**：使用 asyncio.gather()
6. **超时控制**：为所有异步操作设置超时

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 异步代码优化 | 并发安全和竞态条件 | `python-performance-reviewer` 关注异步代码性能（串行 vs 并行） |
| 异步阻塞 | 同步库在 async 函数中阻塞事件循环 | `python-performance-reviewer` 关注 I/O 性能优化 |
| 线程资源 | 线程安全和锁机制 | `python-error-handling-reviewer` 关注资源泄漏 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：并发安全审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码中的并发安全性
# 输入：项目代码文件
# 输出：并发安全审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 扫描所有 threading/asyncio 相关代码
#   2. 识别共享可变状态，检查锁保护
#   3. 检查 async 函数中是否使用了同步阻塞库
#   4. 检查 daemon 线程是否有正确的退出机制
#   5. 检查 asyncio 任务的取消和超时处理
#
# 常见问题模式：
#   - 共享状态无锁保护: → 添加 threading.Lock / asyncio.Lock
#   - async 中调用同步库: → 替换为异步等效库（如 requests → aiohttp）
#   - daemon 线程无退出: → 使用 Event 或 context 停止
#   - 缺少超时: → 添加 asyncio.wait_for / asyncio.timeout
#
# AI-Usage-End
```

---

## 触发词

- "并发审查"
- "线程安全"
- "async await"
- "并发安全审查"
- "Python并发审查员"
