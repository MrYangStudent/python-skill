---
name: python-async-lifecycle-reviewer
description: >
  Python 异步生命周期审查技能，检查 asyncio 任务的生命周期管理、取消信号处理、
  超时设置和资源清理。当用户要求审查 async 代码、检查 asyncio 使用、
  或请求诊断异步超时/取消问题时触发。
triggers:
  - async审查
  - asyncio检查
  - async review
  - 异步生命周期
  - 任务取消
  - 超时检查
  - asyncio审查
  - 异步代码审查
  - async生命周期
  - 协程审查
---

# Python 异步生命周期审查员

## 角色定义

你是 Python asyncio 专家，精通异步任务生命周期管理、取消信号传播、超时控制和资源清理，擅长确保异步代码的正确使用。

## 核心原则

1. **生命周期完整** — 异步任务必须从创建到完成有明确的生命周期
2. **取消传播正确** — 正确处理 asyncio.CancelledError，确保资源释放
3. **超时合理设置** — 所有外部调用必须设置超时
4. **资源确保清理** — 异步上下文管理器必须正确使用

---

## 审查范围

### 1. 任务生命周期管理

**正确模式**：

```python
# asyncio 任务：明确创建和等待
import asyncio

async def main() -> None:
    # 方式 1：直接 await（最推荐）
    result = await do_business(param)

    # 方式 2：create_task + await（需要并发时）
    task = asyncio.create_task(do_business(param))
    try:
        result = await task
    except asyncio.CancelledError:
        task.cancel()
        await task  # 确保任务完成清理

    # 方式 3：TaskGroup（Python 3.11+，结构化并发）
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data(url1))
        t2 = tg.create_task(fetch_data(url2))
    # tg 结束时所有任务已完成或异常已收集

async def query_db(pool: asyncpg.Pool, query: str) -> list:
    async with pool.acquire() as conn:
        return await conn.fetch(query)
```

**危险模式**：

```python
# 🔴 危险：fire-and-forget（任务无人管理）
async def handler(request: Request) -> Response:
    asyncio.create_task(process_in_background(data))  # 无人等待！
    return Response()

# 🔴 危险：gather 不处理取消
results = await asyncio.gather(*tasks)  # 一个失败，其他继续跑

# 🔴 危险：裸 asyncio.sleep 无取消处理
await asyncio.sleep(3600)  # 1小时，期间无法取消
```

### 2. 取消信号处理

**正确模式**：

```python
# ✅ 正确处理 CancelledError + 资源释放
async def long_running() -> None:
    try:
        while True:
            await do_step()
    except asyncio.CancelledError:
        # 清理资源
        await cleanup()
        raise  # 重新抛出，让调用者知道任务被取消

# ✅ 使用 asyncio.shield 保护不可取消的操作
async def fetch_with_cleanup() -> dict:
    try:
        # shield 保护 cancel 不传播到内部操作
        result = await asyncio.shield(fetch_data())
    except asyncio.CancelledError:
        # fetch_data 继续运行，但当前协程被取消
        raise
    return result

# ✅ TaskGroup 结构化取消（Python 3.11+）
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(task1())
    t2 = tg.create_task(task2())
# 任一任务异常 → 其他任务自动取消 → 异常收集
```

**危险模式**：

```python
# 🔴 危险：吞掉 CancelledError
async def process() -> None:
    try:
        await do_work()
    except asyncio.CancelledError:
        return  # 吞掉！上层不知道任务被取消

# 🔴 危险：未在 finally 中清理资源
async def download(url: str) -> bytes:
    resp = await session.get(url)
    data = await resp.read()
    # 如果中途取消，resp 不会被关闭！
    return data

# ✅ 正确：使用 async with 确保清理
async def download(url: str) -> bytes:
    async with session.get(url) as resp:
        return await resp.read()
```

### 3. 超时设置

**检查清单**：

```python
# HTTP 客户端：设置请求超时
import httpx

async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
    resp = await client.get(url)

# 数据库操作：设置查询超时
async with pool.acquire() as conn:
    result = await conn.fetch(query, timeout=30.0)

# 外部 API：设置总超时
try:
    result = await asyncio.wait_for(call_api(), timeout=5.0)
except asyncio.TimeoutError:
    raise AppError(ERR_INTERNAL, cause=TimeoutError("API 超时"))

# 合理超时参考
# - 数据库查询: 5-30s
# - 外部 API: 3-10s
# - 缓存操作: 100ms-1s
# - 简单计算: 无需超时
```

**超时传播**：

```python
# 🔴 危险：硬编码超时，无法被外部控制
async def fetch_data() -> dict:
    return await asyncio.wait_for(internal_call(), timeout=30.0)

# ✅ 推荐：从配置继承超时
async def fetch_data(timeout: float = 10.0) -> dict:
    return await asyncio.wait_for(internal_call(), timeout=timeout)
```

### 4. 资源清理

**正确模式**：

```python
# ✅ async with 管理资源
async with db_pool.acquire() as conn:
    await conn.execute(query)

async with httpx.AsyncClient() as client:
    resp = await client.get(url)

# ✅ finally 确保清理
async def with_cleanup() -> None:
    resource = await acquire_resource()
    try:
        await process(resource)
    finally:
        await release_resource(resource)

# ✅ 自定义异步上下文管理器
class AsyncDBConnection:
    async def __aenter__(self) -> "AsyncDBConnection":
        self.conn = await create_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.conn.close()
```

**危险模式**：

```python
# 🔴 危险：未关闭连接
conn = await pool.acquire()
result = await conn.fetch(query)
# 如果异常，conn 不会被释放回 pool！

# 🔴 危险：Session 未关闭
session = httpx.AsyncClient()
resp = await session.get(url)
# session 永远不关闭！

# ✅ 正确
async with pool.acquire() as conn:
    result = await conn.fetch(query)

async with httpx.AsyncClient() as session:
    resp = await session.get(url)
```

### 5. 并发控制

```python
# ✅ Semaphore 控制并发数
async def batch_fetch(urls: list[str], max_concurrent: int = 10) -> list:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)

    return await asyncio.gather(*[fetch_one(u) for u in urls])

# ✅ 使用 asyncio.wait 灵活等待
done, pending = await asyncio.wait(
    tasks, timeout=10.0,
    return_when=asyncio.FIRST_COMPLETED,
)
for task in pending:
    task.cancel()
await asyncio.gather(*pending, return_exceptions=True)  # 确保取消完成
```

### 6. 异步上下文变量传递

Python 3.7+ 的 `contextvars` 是 asyncio 的上下文传递机制，替代 Go 的 `context.Context`：

```python
import contextvars

# 定义上下文变量
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")
user_id_var: contextvars.ContextVar[int] = contextvars.ContextVar("user_id")

# 中间件注入
async def middleware(request: Request) -> Response:
    token1 = request_id_var.set(request.headers.get("X-Request-ID", ""))
    token2 = user_id_var.set(request.user_id)
    try:
        return await handler(request)
    finally:
        request_id_var.reset(token1)
        user_id_var.reset(token2)

# 业务代码取值
async def process_order(order_id: str) -> dict:
    req_id = request_id_var.get("")  # 自动传播到子任务
    uid = user_id_var.get(0)
    logger.info(f"request_id={req_id} user_id={uid} processing order {order_id}")
```

---

## 审查流程

```
┌─────────────────────────────┐
│  1. 任务生命周期检查         │
│     create_task / gather     │
│     fire-and-forget 检测     │
├─────────────────────────────┤
│  2. 取消信号处理检查         │
│     CancelledError 处理      │
│     资源释放                 │
├─────────────────────────────┤
│  3. 超时设置检查             │
│     wait_for / timeout 参数  │
├─────────────────────────────┤
│  4. 资源清理检查             │
│     async with / finally     │
├─────────────────────────────┤
│  5. 并发控制检查             │
│     Semaphore / TaskGroup    │
├─────────────────────────────┤
│  6. 上下文变量检查           │
│     contextvars 传播         │
└─────────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## Python 异步生命周期审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| handler/api.py:42 | fire-and-forget 任务 | 使用 TaskGroup 或 await |
| service/batch.py:55 | 吞掉 CancelledError | 重新 raise |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| dao/user.py:20 | 无超时设置 | 添加 asyncio.wait_for 5s |
| client/http.py:30 | Session 未关闭 | 使用 async with

### 💡 可选改进

| 建议 |
|------|
| 使用 TaskGroup（Python 3.11+）替代 gather |
| 添加 request_id 到日志（contextvars） |
| 考虑 Semaphore 控制并发数 |
| 使用 asyncio.shield 保护关键操作 |
```

---

## 典型反模式速查

### 反模式 1: fire-and-forget
```python
# 🔴 危险
asyncio.create_task(background_work())

# ✅ 正确
async with asyncio.TaskGroup() as tg:
    tg.create_task(background_work())
```

### 反模式 2: 吞掉 CancelledError
```python
# 🔴 危险
try:
    await work()
except asyncio.CancelledError:
    pass  # 吞掉

# ✅ 正确
try:
    await work()
except asyncio.CancelledError:
    await cleanup()
    raise
```

### 反模式 3: 未管理资源
```python
# 🔴 危险
conn = await pool.acquire()

# ✅ 正确
async with pool.acquire() as conn:
    ...
```

### 反模式 4: 无超时外部调用
```python
# 🔴 危险
result = await external_api_call()

# ✅ 正确
result = await asyncio.wait_for(external_api_call(), timeout=10.0)
```

### 反模式 5: gather 不处理异常
```python
# 🔴 危险
results = await asyncio.gather(*tasks)

# ✅ 正确
results = await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 最佳实践

### 1. 结构化并发（Python 3.11+）

```python
async def fetch_all(urls: list[str]) -> list[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_one(url)) for url in urls]
    return [t.result() for t in tasks]
```

### 2. 超时保护所有外部调用

```python
async def safe_call(fn: Callable, timeout: float = 10.0) -> Any:
    try:
        return await asyncio.wait_for(fn(), timeout=timeout)
    except asyncio.TimeoutError:
        raise AppError(ERR_INTERNAL, cause=TimeoutError(f"超时 {timeout}s"))
```

### 3. 上下文变量传递追踪信息

```python
request_id_var = contextvars.ContextVar("request_id")

async def middleware(request):
    token = request_id_var.set(request.id)
    try:
        return await handler(request)
    finally:
        request_id_var.reset(token)
```

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 并发安全 | asyncio 任务生命周期和取消 | `python-concurrency-reviewer` 关注线程/锁安全 |
| 错误处理 | CancelledError 的正确处理 | `python-error-handling-reviewer` 关注通用异常处理 |
| 资源管理 | 异步资源释放 | `python-refactor-reviewer` 关注代码结构 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：异步生命周期审查                            ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python asyncio 代码的生命周期管理
# 输入：项目代码文件
# 输出：异步生命周期审查报告（按风险等级分级）
#
# 审查步骤：
#   1. 检查 fire-and-forget 任务（create_task 无 await）
#   2. 检查 CancelledError 处理（是否吞掉或未清理）
#   3. 检查超时设置（外部调用是否有 timeout）
#   4. 检查资源管理（async with / finally）
#   5. 检查并发控制（Semaphore / TaskGroup）
#   6. 检查 contextvars 传播
#
# 常见问题模式：
#   - fire-and-forget: → TaskGroup 或显式 await
#   - 吞掉 CancelledError: → cleanup + raise
#   - 无超时: → asyncio.wait_for
#   - 未管理资源: → async with
#   - gather 不处理异常: → return_exceptions=True
#
# AI-Usage-End
```

---

## 触发词

- "async审查"
- "asyncio检查"
- "async review"
- "异步生命周期"
- "任务取消"
- "超时检查"
- "asyncio审查"
- "协程审查"
