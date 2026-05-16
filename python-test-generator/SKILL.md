---
name: python-test-generator
description: >
  Python 测试生成技能。当用户要求为代码生成测试、编写单元测试、创建 test 文件、
  或请求生成 pytest 测试用例时触发。专门用于生成完整的、可运行的测试套件，
  包含正常路径、边界情况和错误路径测试。
triggers:
  - 生成测试
  - 写单元测试
  - 测试生成员
  - pytest 测试
  - 单元测试
---

# Python 测试生成专员 (Test Generator)

## 技能定位

Python 测试专家，精通 pytest 框架，擅长生成高质量、可维护的测试套件。遵循 Python 测试最佳实践。

## 测试覆盖要求

### 1. 正常路径测试
- 基本功能验证
- 多种输入组合
- 预期输出准确性

### 2. 边界情况测试
- None 值
- 空值（空字符串、0、空列表、空字典）
- 极端值（最大值、最小值）

### 3. 错误路径测试
- 无效输入
- 异常条件
- 异常传播验证

### 4. 异步测试
- async/await 函数测试
- 异步上下文管理

## 测试模板

### 基础函数测试

```python
import pytest


def add(a: int, b: int) -> int:
    """加法运算。
    
    Args:
        a: 第一个加数
        b: 第二个加数
    
    Returns:
        两数之和
    """
    return a + b


class TestAdd:
    """加法函数测试类。"""
    
    def test_normal_cases(self) -> None:
        """测试正常路径。"""
        test_cases = [
            (1, 2, 3),      # 正数相加
            (-1, -2, -3),   # 负数相加
            (0, 5, 5),      # 零值
            (1000000, 2000000, 3000000),  # 大数相加
        ]
        
        for a, b, expected in test_cases:
            assert add(a, b) == expected
    
    def test_edge_cases(self) -> None:
        """测试边界情况。"""
        assert add(0, 0) == 0
        assert add(0, -1) == -1


# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：调用 add 函数进行加法运算               ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：计算两个数的和
# 输入：a=10, b=20
# 输出：result=30
#
# 常见调用模式：
#   result = add(10, 20)
#   total = add(x, y) + add(z, w)
#
# 边界情况：
#   - 正数相加：add(1, 2) → 3
#   - 负数相加：add(-1, -2) → -3
#   - 零值：add(0, 5) → 5
#
# AI-Usage-End
```

### 带 Exception 的函数测试

```python
import pytest


class ValidationError(Exception):
    """验证异常。"""
    pass


class UserStore:
    """用户存储。"""
    
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}
    
    def get_by_id(self, user_id: str) -> dict:
        """根据 ID 获取用户。
        
        Args:
            user_id: 用户 ID
        
        Returns:
            用户字典
        
        Raises:
            ValidationError: 当 user_id 为空或用户不存在时
        """
        if not user_id:
            raise ValidationError("user_id cannot be empty")
        
        if user_id not in self._users:
            raise ValidationError(f"user not found: {user_id}")
        
        return self._users[user_id]
    
    def add(self, user_id: str, name: str) -> None:
        """添加用户。"""
        if not user_id:
            raise ValidationError("user_id cannot be empty")
        self._users[user_id] = {"id": user_id, "name": name}


class TestUserStoreGetById:
    """UserStore.get_by_id 测试类。"""
    
    def test_user_exists(self) -> None:
        """测试用户存在的情况。"""
        store = UserStore()
        store.add("user-1", "Alice")
        
        user = store.get_by_id("user-1")
        
        assert user["name"] == "Alice"
    
    def test_user_not_found(self) -> None:
        """测试用户不存在。"""
        store = UserStore()
        
        with pytest.raises(ValidationError) as exc_info:
            store.get_by_id("not-exist")
        
        assert "not found" in str(exc_info.value)
    
    def test_empty_id(self) -> None:
        """测试空 ID。"""
        store = UserStore()
        
        with pytest.raises(ValidationError) as exc_info:
            store.get_by_id("")
        
        assert "cannot be empty" in str(exc_info.value)
```

### Mock 测试

```python
import pytest
from unittest.mock import Mock, MagicMock, patch


class ExternalService:
    """外部服务（需要 Mock）。"""
    
    def fetch_data(self, endpoint: str) -> dict:
        """获取数据。"""
        # 实际会调用外部 API
        ...


class DataProcessor:
    """数据处理器。"""
    
    def __init__(self, service: ExternalService) -> None:
        self._service = service
    
    def process(self, endpoint: str) -> str:
        """处理数据。"""
        data = self._service.fetch_data(endpoint)
        return data.get("result", "default")


class TestDataProcessor:
    """DataProcessor 测试类。"""
    
    def test_process_success(self) -> None:
        """测试处理成功。"""
        mock_service = Mock(spec=ExternalService)
        mock_service.fetch_data.return_value = {"result": "processed"}
        
        processor = DataProcessor(mock_service)
        result = processor.process("/api/data")
        
        assert result == "processed"
        mock_service.fetch_data.assert_called_once_with("/api/data")
    
    def test_process_with_default(self) -> None:
        """测试使用默认值。"""
        mock_service = Mock(spec=ExternalService)
        mock_service.fetch_data.return_value = {}  # 无 result
        
        processor = DataProcessor(mock_service)
        result = processor.process("/api/empty")
        
        assert result == "default"
```

### 异步测试

```python
import pytest
import asyncio


async def fetch_data(endpoint: str, timeout: int | None = None) -> dict:
    """异步获取数据。"""
    await asyncio.sleep(0.1)  # 模拟异步操作
    return {"endpoint": endpoint, "data": [1, 2, 3]}


class TestAsyncFunctions:
    """异步函数测试类。"""
    
    @pytest.mark.asyncio
    async def test_fetch_data_success(self) -> None:
        """测试成功获取数据。"""
        result = await fetch_data("/api/users")
        
        assert result["endpoint"] == "/api/users"
        assert result["data"] == [1, 2, 3]
    
    @pytest.mark.asyncio
    async def test_fetch_data_with_context(self) -> None:
        """测试带超时的异步操作。"""
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                fetch_data("/api/slow"),
                timeout=0.001  # 极短超时
            )


# Fixture 示例
@pytest.fixture
def sample_data() -> dict:
    """样例数据 Fixture。"""
    return {"id": 1, "name": "Test", "items": [1, 2, 3]}


class TestWithFixtures:
    """使用 Fixture 的测试类。"""
    
    def test_with_sample_data(self, sample_data: dict) -> None:
        """使用 sample_data fixture。"""
        assert sample_data["id"] == 1
        assert len(sample_data["items"]) == 3
```

### 参数化测试

```python
import pytest


def filter_items(items: list[int], predicate: Callable[[int], bool]) -> list[int]:
    """过滤列表项。"""
    return [item for item in items if predicate(item)]


class TestFilterItems:
    """filter_items 参数化测试。"""
    
    @pytest.mark.parametrize(
        "items,predicate,expected",
        [
            ([1, 2, 3, 4, 5], lambda x: x > 2, [3, 4, 5]),
            ([1, 2, 3], lambda x: x > 10, []),
            ([], lambda x: x > 0, []),
            ([1, 2, 3], lambda x: x > 0, [1, 2, 3]),
        ],
    )
    def test_filter(
        self, 
        items: list[int], 
        predicate: Callable[[int], bool], 
        expected: list[int]
    ) -> None:
        """参数化测试用例。"""
        result = filter_items(items, predicate)
        assert result == expected
```

## 测试命名规范

| 格式 | 用途 |
|------|------|
| `test_<unit>_<scenario>` | 正常/错误路径 |
| `test_<unit>_edge_cases` | 边界情况 |
| `test_<unit>_async` | 异步测试 |
| `Test<Class>_<method>` | 类方法测试 |

## 最佳实践

### 1. 使用 pytest

```bash
# 运行所有测试
python -m pytest -v

# 带覆盖率
python -m pytest --cov=. --cov-report=term-missing

# 只运行失败的测试
python -m pytest --lf

# 停止于第一个失败
python -m pytest -x
```

### 2. Fixture 复用

```python
@pytest.fixture
def db_connection():
    """数据库连接 Fixture。"""
    conn = create_test_connection()
    yield conn
    conn.close()
```

### 3. Mock 对象

```python
from unittest.mock import Mock, patch

# 使用 patch 作为装饰器
@patch('module.ClassName')
def test_with_mock(mock_class):
    mock_class.return_value.method.return_value = "mocked"
    ...
```

## 完整测试文件模板

```python
"""模块测试文件。

AI-Usage-Begin
测试模块：提供加法、乘法等数学运算功能
主要函数：
  - add(a: int, b: int) -> int
  - multiply(a: int, b: int) -> int
AI-Usage-End
"""

import pytest


# 测试目标模块
import sys
sys.path.insert(0, '..')
from your_module import add, multiply, ValidationError


class TestAdd:
    """加法函数测试类。"""
    
    def test_normal_cases(self) -> None:
        """测试正常路径。"""
        test_cases = [
            (1, 2, 3),
            (-1, -2, -3),
            (0, 0, 0),
        ]
        
        for a, b, expected in test_cases:
            assert add(a, b) == expected
    
    def test_edge_cases(self) -> None:
        """测试边界情况。"""
        assert add(0, 0) == 0
        assert add(0, -1) == -1


class TestMultiply:
    """乘法函数测试类。"""
    
    def test_normal_cases(self) -> None:
        """测试正常路径。"""
        assert multiply(2, 3) == 6
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0


# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：调用 add 和 multiply 函数             ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：执行数学运算
# 输入：add(2, 3), multiply(4, 5)
# 输出：5, 20
#
# 常见调用模式：
#   result = add(x, y)
#   product = multiply(a, b)
#   combined = add(x, multiply(y, z))
#
# AI-Usage-End
```
