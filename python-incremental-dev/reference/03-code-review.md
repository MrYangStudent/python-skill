# 代码审查规范

## 审查清单概览

| 审查类型 | 关注点 |
|----------|--------|
| 异常处理 | 被吞异常、异常类型、异常链 |
| 类型安全 | 类型注解完整性、运行时类型检查 |
| 安全漏洞 | 注入、敏感信息、路径遍历 |
| 性能 | 超时、内存、资源释放 |
| 日志 | 级别、脱敏、结构化 |
| API 设计 | RESTful、状态码、响应结构 |
| 并发安全 | asyncio 竞态、线程安全 |

---

## 1. 异常处理审查

### 1.1 被吞的异常

```python
# ✗ 错误示例
try:
    result = risky_function()
except Exception:
    pass  # 吞掉所有异常

# ✓ 正确示例
try:
    result = risky_function()
except ValueError as e:
    logger.warning(f"处理值异常: {e}")
    result = default_value
```

### 1.2 裸 except

```python
# ✗ 错误示例
try:
    do_something()
except:  # 捕获所有异常包括 KeyboardInterrupt
    handle_error()

# ✓ 正确示例
try:
    do_something()
except (ValueError, IOError) as e:
    handle_error(e)
```

### 1.3 异常链保留

```python
# ✗ 错误示例
raise ValueError("operation failed")

# ✓ 正确示例
raise ValueError("process data failed") from e
```

### 1.4 参数校验

```python
# ✓ 参数校验
def find_user(id: str) -> User:
    if not id:
        raise ValueError("id cannot be empty")
    # ...
```

---

## 2. 类型安全审查

### 2.1 类型注解缺失

```python
# ✗ 错误示例
def process(data):
    result = transform(data)
    return result

# ✓ 正确示例
def process(data: list[Item]) -> Result:
    result = transform(data)
    return result
```

### 2.2 Any 类型滥用

```python
# ✗ 错误示例
def handle(value: Any) -> Any:
    pass

# ✓ 正确示例
def handle(value: str | int) -> str:
    pass
```

---

## 3. 并发安全审查

### 3.1 asyncio 竞态

```python
# ✗ 错误示例：共享状态无保护
cache: dict[str, str] = {}

async def update_cache(key: str, value: str) -> None:
    cache[key] = value  # 多协程可能竞态

# ✓ 正确示例：使用 asyncio.Lock
import asyncio

_cache: dict[str, str] = {}
_cache_lock = asyncio.Lock()

async def update_cache(key: str, value: str) -> None:
    async with _cache_lock:
        _cache[key] = value
```

### 3.2 线程安全

```python
# ✓ 正确示例 - 使用 threading.Lock
import threading

class SafeCache:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._data: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        with self._lock:
            return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        with self._lock:
            self._data[key] = value
```

### 3.3 线程/协程退出机制

```python
# ✓ 正确示例 - asyncio.TaskGroup
async def fetch_all(urls: list[str]) -> list[str]:
    results: list[str] = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_one(url, results))
    return results

# ✓ 正确示例 - threading.Event
stop_event = threading.Event()

def worker() -> None:
    while not stop_event.is_set():
        process_item()

def stop_workers() -> None:
    stop_event.set()
```

---

## 4. 安全审查

### 4.1 敏感信息泄露

```python
# 🔴 危险：敏感信息硬编码
API_KEY = "sk-xxxx-xxxx-xxxx"

# ✅ 推荐：环境变量或配置
import os
api_key = os.environ["API_KEY"]
```

### 4.2 SQL 注入

```python
# 🔴 危险：字符串拼接
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ 安全：参数化查询
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (name,))
```

### 4.3 命令注入

```python
# 🔴 危险：shell 注入
os.system(f"ls {user_input}")

# ✅ 安全：参数化执行
import subprocess
subprocess.run(["ls", user_input], check=True)
```

### 4.4 路径遍历

```python
# 🔴 危险：用户输入拼接到路径
path = f"./uploads/{filename}"

# ✅ 安全：路径校验
import os
safe_path = os.path.normpath(os.path.join("./uploads", filename))
if not safe_path.startswith(os.path.normpath("./uploads/")):
    raise ValueError("invalid path")
```

---

## 5. 性能审查

### 5.1 超时与连接

```python
# 🔴 危险：无限等待
response = requests.get(url)

# ✅ 安全：设置超时
response = requests.get(url, timeout=5.0)
```

### 5.2 资源释放

```python
# ✅ 安全：上下文管理器
with open(path) as f:
    data = f.read()
```

### 5.3 列表预分配

```python
# ✅ 推荐：列表推导优于循环 append
results = [transform(item) for item in items]
```

### 5.4 同步手段

```python
# 🔴 禁止：time.sleep 作为同步
import time
time.sleep(1)  # 等待另一个线程

# ✅ 推荐：Event 或 Condition
event = threading.Event()
event.wait()
```

---

## 6. 日志规范审查

### 6.1 日志级别使用

| 级别 | 使用场景 | 示例 |
|------|----------|------|
| DEBUG | 开发调试 | "进入函数 X" |
| INFO | 正常流程 | "用户登录成功" |
| WARNING | 异常但可处理 | "重试第 N 次" |
| ERROR | 错误需要关注 | "数据库连接失败" |

### 6.2 敏感信息脱敏

```python
# 🔴 危险：日志输出敏感信息
logger.info(f"用户登录: password={password}")

# ✅ 安全：脱敏处理
def mask_sensitive(key: str, value: str) -> str:
    if key in ("password", "secret", "token"):
        return "***"
    if key in ("authorization",) and len(value) > 8:
        return value[:4] + "****"
    return value
```

### 6.3 结构化日志

```python
# ✅ 推荐：使用 structlog 或 json 格式
logger.info("purchase_success", user_id=user_id, product=product, price=price)
```

---

## 7. API 设计审查

### 7.1 RESTful 规范

| 规则 | 正确示例 | 错误示例 |
|------|----------|----------|
| 使用名词 | GET /users | GET /getUsers |
| 使用复数 | GET /users | GET /user |
| 层级结构 | GET /users/{id}/orders | GET /userOrders?user_id={id} |

### 7.2 HTTP 状态码

| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | OK | 成功响应 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未认证 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器错误 |

### 7.3 响应结构

```python
# ✅ 推荐：统一响应结构
from pydantic import BaseModel

class Response(BaseModel):
    code: int
    message: str
    data: Any = None

class PageResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
```
