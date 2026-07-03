# 增量开发策略

## 策略优先级（P0-P3）

本技能在执行增量开发时，遵循以下优先级选择策略：

| 优先级 | 策略 | 适用场景 | 对应传统策略 |
|--------|------|----------|-------------|
| **P0 — 首选** | **内联扩展** — 在现有文件中新增函数/方法 | 功能与现有模块逻辑紧密相关 | 无（直接扩展） |
| **P1** | **组合复用** — 组合多个现有模块实现新功能 | 功能横跨多个现有模块 | 依赖注入解耦 |
| **P2** | **适配器模式** — 写适配器对接新旧代码 | 新旧代码接口不一致 | 适配器模式 |
| **P3 — 末选** | **新模块独立目录** | 功能完全独立，与现有代码无强关联 | 扩展优于修改 + Feature Flag |

> **胶水编程原则**: 始终优先从 P0 开始尝试，只有当低优先级策略不可行时才升级到更高优先级。

---

## 新旧代码隔离策略

### 核心原则

以下策略用于需要隔离新旧代码的场景（通常对应 P2-P3）：

1. **扩展优于修改** — 通过 Protocol/ABC 扩展新功能
2. **依赖注入解耦** — 面向 Protocol 编程
3. **适配器模式** — 隔离新旧代码交互
4. **Feature Flag** — 配置控制功能开关

---

## 1. 扩展优于修改

```python
# ✗ 错误：直接修改旧函数
class OldService:
    def process(self) -> None:
        # 修改原有逻辑...
        pass

# ✓ 正确：创建新实现，通过 Protocol 扩展
from typing import Protocol


class Processor(Protocol):
    def process(self) -> None: ...


class NewProcessor:
    """新处理器实现。"""

    def process(self) -> None:
        # 新逻辑...
        pass
```

---

## 2. 依赖注入解耦

```python
# ✓ 正确：通过 Protocol 依赖
from typing import Protocol


class StorageProtocol(Protocol):
    def get(self, key: str) -> bytes: ...
    def set(self, key: str, value: bytes) -> None: ...
    def delete(self, key: str) -> None: ...


class Service:
    """通过构造函数注入依赖。"""

    def __init__(self, storage: StorageProtocol) -> None:
        self._storage = storage


# 旧实现保持兼容
class LegacyStorage:
    def get(self, key: str) -> bytes:
        # 旧实现...
        pass

    def set(self, key: str, value: bytes) -> None:
        # 旧实现...
        pass

    def delete(self, key: str) -> None:
        # 旧实现...
        pass


# 新实现独立开发
class NewStorage:
    def get(self, key: str) -> bytes:
        # 新实现...
        pass

    def set(self, key: str, value: bytes) -> None:
        # 新实现...
        pass

    def delete(self, key: str) -> None:
        # 新实现...
        pass
```

---

## 3. 适配器模式对接旧代码

```python
# 适配器：包装旧服务供新代码使用
class LegacyAdapter:
    """将旧服务适配为新接口。"""

    def __init__(self, old_service: OldService) -> None:
        self._old_service = old_service

    def call(self) -> None:
        self._old_service.old_method()


# 适配器：包装新服务供旧代码使用
class NewAdapter:
    """将新服务适配为旧接口。"""

    def __init__(self, new_service: NewService) -> None:
        self._new_service = new_service

    def legacy_method(self) -> None:
        self._new_service.new_method()
```

---

## 4. Feature Flag 控制

```python
from dataclasses import dataclass


@dataclass
class FeatureFlags:
    """功能开关配置。"""
    new_processor: bool = False
    cache_enabled: bool = True


class Service:
    """通过 Feature Flag 控制功能切换。"""

    def __init__(self, flags: FeatureFlags) -> None:
        self._flags = flags

    def process(self) -> None:
        if self._flags.new_processor:
            return self._new_processor.process()
        return self._old_processor.process()
```

---

## 目录结构示例

```
project/
├── src/
│   ├── legacy/           # 旧代码（不修改）
│   │   ├── __init__.py
│   │   ├── service.py
│   │   └── test_service.py
│   └── features/         # 新功能目录
│       ├── myfeature/    # 新功能模块
│       │   ├── __init__.py
│       │   ├── myfeature.py
│       │   ├── test_myfeature.py
│       │   └── adapter.py      # 适配器（如需要）
│       └── another/       # 另一个新功能
│           ├── __init__.py
│           ├── another.py
│           └── test_another.py
├── pkg/                  # 公共包
│   └── http_client/
│       └── __init__.py
└── pyproject.toml
```

---

## Protocol/ABC 设计模板

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class FeatureProtocol(Protocol):
    """新功能接口定义。"""

    def do_something(self, request: Request) -> Response: ...
    def close(self) -> None: ...


class FeatureImpl:
    """新功能实现。"""

    def __init__(self, client: HttpClient, cache: dict[str, bytes]) -> None:
        self._client = client
        self._cache = cache

    def do_something(self, request: Request) -> Response:
        """实现具体逻辑。"""
        if request is None:
            raise ValueError("request cannot be None")
        # 实现...

    def close(self) -> None:
        """清理资源。"""


# 确认实现接口
def _check_protocol() -> None:
    assert isinstance(FeatureImpl(), FeatureProtocol)
```

---

## 依赖注入示例

```python
from dataclasses import dataclass
from typing import Protocol


class StorageProtocol(Protocol):
    def get(self, key: str) -> bytes: ...
    def set(self, key: str, value: bytes) -> None: ...


class CacheProtocol(Protocol):
    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str, ttl: float | None = None) -> None: ...


class LoggerProtocol(Protocol):
    def info(self, msg: str, **kwargs: Any) -> None: ...
    def error(self, msg: str, **kwargs: Any) -> None: ...


@dataclass
class ServiceDependencies:
    """服务依赖配置。"""
    storage: StorageProtocol
    cache: CacheProtocol
    logger: LoggerProtocol


class Service:
    """通过依赖注入解耦。"""

    def __init__(self, deps: ServiceDependencies) -> None:
        self._storage = deps.storage
        self._cache = deps.cache
        self._logger = deps.logger


# Mock 依赖（用于测试）
class MockStorage:
    def __init__(self) -> None:
        self.data: dict[str, bytes] = {}

    def get(self, key: str) -> bytes:
        return self.data.get(key, b"")

    def set(self, key: str, value: bytes) -> None:
        self.data[key] = value
```

---

## 数据迁移策略

### 1. 向后兼容的数据结构

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    """用户数据，新增字段使用 Optional 兼容旧数据。"""
    id: str
    name: str
    email: str
    # 新增字段使用 Optional，兼容旧数据
    phone: Optional[str] = field(default=None)
    created_at: Optional[str] = field(default=None)
```

### 2. 数据库迁移脚本

```sql
-- V1: 添加新字段（可空）
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD COLUMN created_at TIMESTAMP;

-- V2: 设置默认值
UPDATE users SET phone = '' WHERE phone IS NULL;

-- V3: 添加约束
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

---

## 配置管理

### 配置文件结构

```yaml
# config.yaml
app:
  name: "myapp"
  env: "production"

server:
  host: "0.0.0.0"
  port: 8000
  timeout: 30

database:
  host: "localhost"
  port: 5432
  name: "myapp"
  max_connections: 25

# Feature Flags
features:
  new_processor: false  # 默认关闭
  cache_enabled: true
```

### 配置加载

```python
from dataclasses import dataclass


@dataclass
class AppConfig:
    name: str
    env: str


@dataclass
class FeatureFlags:
    new_processor: bool = False
    cache_enabled: bool = True


@dataclass
class Config:
    app: AppConfig
    server: dict[str, Any]
    database: dict[str, Any]
    features: FeatureFlags


def load_config(path: str) -> Config:
    """加载 YAML 配置文件。"""
    import yaml

    data = Path(path).read_text(encoding="utf-8")
    raw = yaml.safe_load(data)

    return Config(
        app=AppConfig(**raw["app"]),
        server=raw["server"],
        database=raw["database"],
        features=FeatureFlags(**raw["features"]),
    )
```

---

## 渐进式发布策略

### 1. 金丝雀发布

```python
import random


class CanaryRouter:
    """金丝雀路由：按比例分流到新旧服务。"""

    def __init__(self, primary: Service, canary: NewService, ratio: float = 0.1) -> None:
        self._primary = primary
        self._canary = canary
        self._ratio = ratio

    def process(self, request: Request) -> Response:
        if random.random() < self._ratio:
            return self._canary.process(request)
        return self._primary.process(request)
```

### 2. A/B 测试

```python
class ABTestRouter:
    """A/B 测试路由：按请求头分流。"""

    def __init__(self, variant_a: Service, variant_b: Service) -> None:
        self._variant_a = variant_a
        self._variant_b = variant_b

    def process(self, request: Request) -> Response:
        variant = request.headers.get("X-AB-Variant")
        if variant == "B":
            return self._variant_b.process(request)
        return self._variant_a.process(request)
```
