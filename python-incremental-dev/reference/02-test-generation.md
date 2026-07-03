# 测试生成规范

## 测试覆盖要求

1. **正常路径测试** - 基本功能验证、多种输入组合、预期输出准确性
2. **边界情况测试** - None、空字符串、空列表、零值、极端值
3. **错误路径测试** - 无效输入、异常条件、异常传播验证
4. **并发安全测试** - asyncio 竞态、多线程读写场景

---

## 测试模板

### 基础函数测试

```python
import pytest


class TestAdd:
    """Add 函数的测试套件。"""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),           # 正数相加
        (-1, -2, -3),        # 负数相加
        (0, 5, 5),           # 零值
        (1000000, 2000000, 3000000),  # 大数
    ])
    def test_normal(self, a, b, expected):
        """正常路径测试。"""
        assert add(a, b) == expected
```

### 带 Exception 的函数测试

```python
import pytest


class TestUserStoreGetByID:
    """UserStore.get_by_id 的测试套件。"""

    def test_user_exists(self):
        """用户存在时正常返回。"""
        store = UserStore()
        store.users["user-1"] = User(id="user-1", name="Alice")
        user = store.get_by_id("user-1")
        assert user.name == "Alice"

    def test_user_not_found(self):
        """用户不存在时抛出 NotFoundError。"""
        store = UserStore()
        with pytest.raises(NotFoundError):
            store.get_by_id("not-exist")

    def test_invalid_id(self):
        """无效 ID 时抛出 ValueError。"""
        store = UserStore()
        with pytest.raises(ValueError):
            store.get_by_id("")
```

### 异步函数测试

```python
import pytest
import asyncio


class TestAsyncFetcher:
    """AsyncFetcher 的测试套件。"""

    @pytest.mark.asyncio
    async def test_fetch_data(self):
        """正常异步数据获取。"""
        fetcher = AsyncFetcher()
        result = await fetcher.fetch("https://api.example.com/data")
        assert result.status == "ok"

    @pytest.mark.asyncio
    async def test_fetch_timeout(self):
        """超时时抛出 TimeoutError。"""
        fetcher = AsyncFetcher(timeout=0.001)
        with pytest.raises(TimeoutError):
            await fetcher.fetch("https://slow.example.com/data")
```

### 并发安全测试

```python
import pytest
import threading


class TestCounterConcurrent:
    """Counter 的并发安全测试。"""

    def test_concurrent_increment(self):
        """多线程并发递增。"""
        counter = ThreadSafeCounter()
        num_threads = 100
        increments_per_thread = 1000

        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=lambda: [
                counter.increment() for _ in range(increments_per_thread)
            ])
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        expected = num_threads * increments_per_thread
        assert counter.value() == expected
```

### 边界情况测试

```python
import pytest
from strings import strings


class TestValidateNameEdgeCases:
    """validate_name 的边界情况测试。"""

    @pytest.mark.parametrize("input,should_raise", [
        ("", True),                    # 空字符串
        ("A", False),                  # 单字符
        ("Alice", False),              # 正常长度
        ("a" * 100, False),            # 最大长度
        ("a" * 101, True),             # 超过最大长度
        ("Alice Wang", False),         # 包含空格
        ("User123", False),            # 包含数字
        ("12345", True),               # 纯数字
        ("user@#$", True),             # 特殊字符
    ])
    def test_edge_cases(self, input, should_raise):
        """边界情况：各种特殊输入。"""
        if should_raise:
            with pytest.raises(ValueError):
                validate_name(input)
        else:
            validate_name(input)  # 不应抛异常
```

---

## 测试命名规范

| 格式 | 用途 |
|------|------|
| `Test_<Unit>_<Scenario>` | 正常/错误路径 |
| `Test_<Unit>_EdgeCases` | 边界情况 |
| `Test_<Unit>_Concurrent` | 并发测试 |

---

## Mock 编写模板

```python
from unittest.mock import MagicMock, AsyncMock


class MockStorage:
    """模拟存储服务。"""

    def __init__(self):
        self.data: dict[str, bytes] = {}
        self.get_error: Exception | None = None
        self.set_error: Exception | None = None
        self.on_get: MagicMock | None = None
        self.on_set: MagicMock | None = None

    def get(self, key: str) -> bytes:
        if self.on_get:
            self.on_get(key)
        if self.get_error:
            raise self.get_error
        return self.data.get(key, b"")

    def set(self, key: str, value: bytes) -> None:
        if self.on_set:
            self.on_set(key, value)
        if self.set_error:
            raise self.set_error
        self.data[key] = value

    def delete(self, key: str) -> None:
        self.data.pop(key, None)


class MockAsyncStorage:
    """模拟异步存储服务。"""

    def __init__(self):
        self.data: dict[str, bytes] = {}
        self.get_error: Exception | None = None
        self.on_get: AsyncMock | None = None

    async def get(self, key: str) -> bytes:
        if self.on_get:
            await self.on_get(key)
        if self.get_error:
            raise self.get_error
        return self.data.get(key, b"")

    async def set(self, key: str, value: bytes) -> None:
        self.data[key] = value
```

---

## pytest 配置参考

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests", "features"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "integration: marks tests as integration tests",
    "slow: marks tests as slow",
]
addopts = "--cov --cov-report=term-missing -v"
```
