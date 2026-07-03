---
name: python-utility-functions
description: >
  Python 通用工具函数封装技能。当用户要求封装常用函数、编写工具库、生成 HTTP 客户端封装、
  签名/加密工具、排序工具、时间格式化工具、泛型序列/dict 转换工具时触发。
  专门用于识别重复逻辑并封装为可复用的类型安全工具函数，遵循 Python 标准库优先原则。
  集成 Python Minimal Code 原则：封装前先问"真的需要封装吗？还是只是重复了两次？"
triggers:
  - 封装工具函数
  - 通用函数
  - 工具库
  - HTTP封装
  - 签名工具
  - 加密工具
  - 排序工具
  - 时间格式化
  - 泛型转换
  - 列表工具
  - 字典工具
  - 去重
  - 分页
  - retry重试
  - Python工具函数
  - utility functions
  - Python通用函数
  - python-minimal-code
  - 最小可行封装
---

# Python 通用工具函数封装 (Python Utility Functions)

## 技能定位

Python 工具函数封装专家，善于识别项目中的重复逻辑，将其抽象为类型安全、零外部依赖的可复用函数。遵循标准库优先、类型注解优先、接口最小化原则。

## 核心原则

1. **标准库优先** — 仅使用 Python 标准库，不引入第三方依赖
2. **类型注解优先** — 所有公开函数必须有完整的类型注解
3. **接口最小化** — 函数参数接受 `Iterable` / `Mapping` 等标准协议
4. **零值可用** — 函数默认参数即可安全使用
5. **Python Minimal Code YAGNI** — 封装前先问：重复次数是否真够？未来是否真的需要？

### Python Minimal Code 集成：封装决策树

在封装任何工具函数之前，严格执行以下判断：

```
发现重复代码
  ├── 出现 >= 2 次？
  │   ├── 否 → 不封装，保持内联（YAGNI）
  │   └── 是 → 逻辑是否稳定？
  │       ├── 否 → 等等看，下次重复时再封装
  │       └── 是 → 是否可用标准库替代？
  │           ├── 是 → 用标准库
  │           └── 否 → 封装为独立函数
  └── 涉及外部资源（HTTP、DB）？
      └── 是 → 封装为类，便于 Mock 测试
```

### 封装门槛

| 重复次数 | 建议 | 说明 |
|----------|------|------|
| 1 次 | ❌ 不封装 | 第一次做决定是好抽象 |
| 2 次 | ⚠️ 谨慎 | 可能是巧合，等等看第 3 次 |
| 3 次+ | ✅ 封装 | 模式已确立，值得抽象 |

**关键原则**：封装的收益必须大于维护成本。如果封装后工具函数比原始代码还长，或者需要复杂的文档才能使用，说明封装过早或过度。

## 封装检查清单

---

### 1. HTTP 客户端封装

**问题**: 每个 HTTP 调用都重复设置超时、Header、错误处理。

**封装方案**:

```python
"""HTTP 客户端封装，内置超时和通用 Header。"""

import json
from typing import Any, TypeVar, Generic
from dataclasses import dataclass, field
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import http.client

T = TypeVar("T")


@dataclass
class Response(Generic[T]):
    """HTTP 响应封装。"""
    status_code: int
    headers: dict[str, str]
    body: T


class Client:
    """封装 HTTP 客户端，内置超时和通用 Header。"""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}

    def set_header(self, key: str, value: str) -> "Client":
        """设置通用 Header，所有请求都会携带。"""
        self.headers[key] = value
        return self

    def get(self, path: str) -> Response[dict]:
        """发送 GET 请求并解码 JSON 响应。"""
        return self._request("GET", path)

    def post(self, path: str, body: Any = None) -> Response[dict]:
        """发送 POST 请求，body 会被编码为 JSON。"""
        return self._request("POST", path, body)

    def _request(
        self, method: str, path: str, body: Any = None
    ) -> Response[dict]:
        """执行请求并解码响应。"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        data = json.dumps(body).encode() if body is not None else None

        req = Request(url, data=data, method=method)
        for k, v in self.headers.items():
            req.add_header(k, v)
        if body is not None:
            req.add_header("Content-Type", "application/json")

        try:
            with urlopen(req, timeout=self.timeout) as resp:
                resp_headers = {k: v for k, v in resp.headers.items()}
                result = json.loads(resp.read().decode())
                return Response(
                    status_code=resp.status,
                    headers=resp_headers,
                    body=result,
                )
        except HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}") from e
        except URLError as e:
            raise RuntimeError(f"请求失败: {e.reason}") from e
```

**使用示例**:
```python
client = Client("https://api.example.com", timeout=10.0)
client.set_header("Authorization", f"Bearer {token}")

resp = client.get("/users/123")
print(resp.body["name"])
```

---

### 2. 签名工具封装

**问题**: API 签名逻辑散落各处，HMAC 签名参数拼接不统一。

**封装方案**:

```python
"""通用签名器，支持 HMAC-SHA256 和 MD5 签名。"""

import hashlib
import hmac
import enum
from typing import Protocol


class Method(enum.Enum):
    """签名算法。"""
    HMAC_SHA256 = "hmac_sha256"
    MD5 = "md5"


class Signer:
    """通用签名器。"""

    def __init__(self, secret_key: str, method: Method = Method.HMAC_SHA256) -> None:
        self._secret_key = secret_key.encode()
        self.method = method

    @classmethod
    def hmac_sha256(cls, secret_key: str) -> "Signer":
        """创建 HMAC-SHA256 签名器。"""
        return cls(secret_key, Method.HMAC_SHA256)

    @classmethod
    def md5(cls, secret_key: str) -> "Signer":
        """创建 MD5 签名器（仅用于兼容旧接口，新系统应使用 HMAC-SHA256）。"""
        return cls(secret_key, Method.MD5)

    def sign(self, params: dict[str, str]) -> str:
        """对参数按 key 字典序排序后拼接签名。

        拼接格式: key1=value1&key2=value2... + &key=secretKey
        """
        sorted_keys = sorted(params.keys())
        content = "&".join(f"{k}={params[k]}" for k in sorted_keys)

        if self.method == Method.HMAC_SHA256:
            return hmac.new(
                self._secret_key, content.encode(), hashlib.sha256
            ).hexdigest()
        elif self.method == Method.MD5:
            return hashlib.md5(
                (content + f"&key={self._secret_key.decode()}").encode()
            ).hexdigest()
        raise ValueError(f"unsupported sign method: {self.method}")

    def verify(self, params: dict[str, str], signature: str) -> bool:
        """验证签名是否匹配。"""
        expected = self.sign(params)
        return hmac.compare_digest(expected, signature)
```

**使用示例**:
```python
signer = Signer.hmac_sha256("my-secret-key")
sig = signer.sign({
    "amount": "100",
    "orderId": "12345",
    "timestamp": "1700000000",
})

ok = signer.verify(params, received_sig)
```

---

### 3. 加密/哈希工具封装

**问题**: AES 加密、SHA 哈希等操作步骤冗长且容易出错。

**封装方案**:

```python
"""加密和哈希工具封装。"""

import hashlib
import os
from cryptography.fernet import Fernet
import base64


def sha256(data: str) -> str:
    """计算字符串的 SHA-256 哈希值，返回十六进制编码。"""
    return hashlib.sha256(data.encode()).hexdigest()


def sha1(data: str) -> str:
    """计算字符串的 SHA-1 哈希值，返回十六进制编码。"""
    return hashlib.sha1(data.encode()).hexdigest()


def md5(data: str) -> str:
    """计算字符串的 MD5 哈希值，返回十六进制编码。仅用于兼容旧接口。"""
    return hashlib.md5(data.encode()).hexdigest()


def hmac_sha256(key: str, data: str) -> str:
    """计算 HMAC-SHA256 签名。"""
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()


def aes_key_from_password(password: str, salt: bytes | None = None) -> bytes:
    """从密码生成 AES 密钥（Fernet 兼容格式）。

    salt 为 None 时自动生成随机 salt。
    返回值可直接用于 Fernet 加解密。
    """
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return base64.urlsafe_b64encode(key)


def aes_encrypt(key: bytes, plaintext: str) -> bytes:
    """使用 AES（Fernet）加密明文。"""
    f = Fernet(key)
    return f.encrypt(plaintext.encode())


def aes_decrypt(key: bytes, ciphertext: bytes) -> str:
    """使用 AES（Fernet）解密密文。"""
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()
```

**使用示例**:
```python
# SHA-256 哈希
hash_value = sha256("hello world")

# AES 加解密
key = aes_key_from_password("my-password")
encrypted = aes_encrypt(key, "sensitive data")
decrypted = aes_decrypt(key, encrypted)
```

---

### 4. 序列操作工具封装

**问题**: Map/Filter/Unique/GroupBy 等函数式操作在业务代码中反复手写循环。

**封装方案**:

```python
"""序列操作工具，提供常用列表/迭代器转换函数。"""

from typing import Callable, Iterable, TypeVar, Hashable, overload

T = TypeVar("T")
R = TypeVar("R")
K = TypeVar("K", bound=Hashable)


def map_(items: Iterable[T], fn: Callable[[T], R]) -> list[R]:
    """将每个元素通过 fn 转换为新类型，返回新列表。"""
    return [fn(item) for item in items]


def filter_(items: Iterable[T], fn: Callable[[T], bool]) -> list[T]:
    """过滤元素，保留 fn 返回 True 的元素。"""
    return [item for item in items if fn(item)]


def unique(items: Iterable[T]) -> list[T]:
    """对可哈希类型序列去重，保持原始顺序。"""
    seen: set[T] = set()
    result: list[T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def unique_by(items: Iterable[T], key_fn: Callable[[T], K]) -> list[T]:
    """按键值去重，保持原始顺序。"""
    seen: set[K] = set()
    result: list[T] = []
    for item in items:
        k = key_fn(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def group_by(items: Iterable[T], key_fn: Callable[[T], K]) -> dict[K, list[T]]:
    """按键值分组。"""
    result: dict[K, list[T]] = {}
    for item in items:
        k = key_fn(item)
        result.setdefault(k, []).append(item)
    return result


def chunk(items: list[T], size: int) -> list[list[T]]:
    """将列表分割为指定大小的子列表。"""
    if size <= 0:
        return []
    return [items[i:i + size] for i in range(0, len(items), size)]


def contains(items: Iterable[T], target: T) -> bool:
    """判断序列是否包含指定元素。"""
    return target in list(items)


def find(items: Iterable[T], fn: Callable[[T], bool]) -> tuple[T | None, bool]:
    """查找第一个匹配元素，返回元素和是否找到。"""
    for item in items:
        if fn(item):
            return item, True
    return None, False


def flatten(lists: Iterable[list[T]]) -> list[T]:
    """展平二维列表为一维。"""
    result: list[T] = []
    for lst in lists:
        result.extend(lst)
    return result


def reverse(items: list[T]) -> list[T]:
    """返回反转后的列表（不修改原列表）。"""
    return list(reversed(items))


def reduce(items: Iterable[T], initial: R, fn: Callable[[R, T], R]) -> R:
    """将序列归约为单个值。"""
    from functools import reduce as _reduce
    return _reduce(fn, items, initial)
```

**使用示例**:
```python
# 转换
names = map_(users, lambda u: u.name)

# 过滤
active = filter_(users, lambda u: u.active)

# 去重
unique_ids = unique(user_ids)

# 分组
by_dept = group_by(employees, lambda e: e.department)

# 分块
pages = chunk(items, 20)
```

---

### 5. 字典工具封装

**问题**: 从 dict 中取值、转换 key/value、合并 dict 等操作重复编写。

**封装方案**:

```python
"""字典操作工具。"""

from typing import Callable, TypeVar, Hashable, Mapping

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
V2 = TypeVar("V2")
K2 = TypeVar("K2", bound=Hashable)


def keys(m: Mapping[K, V]) -> list[K]:
    """返回字典的所有 key。"""
    return list(m.keys())


def values(m: Mapping[K, V]) -> list[V]:
    """返回字典的所有 value。"""
    return list(m.values())


def merge(*dicts: dict[K, V]) -> dict[K, V]:
    """合并多个字典，后面的覆盖前面的同名 key。"""
    result: dict[K, V] = {}
    for d in dicts:
        result.update(d)
    return result


def invert(m: Mapping[K, V]) -> dict[V, K]:
    """交换 key 和 value（值必须唯一，否则会丢失）。"""
    return {v: k for k, v in m.items()}


def map_keys(m: Mapping[K, V], fn: Callable[[K], K2]) -> dict[K2, V]:
    """对字典的 key 进行转换。"""
    return {fn(k): v for k, v in m.items()}


def map_values(m: Mapping[K, V], fn: Callable[[V], V2]) -> dict[K, V2]:
    """对字典的 value 进行转换。"""
    return {k: fn(v) for k, v in m.items()}


def filter_dict(m: Mapping[K, V], fn: Callable[[K, V], bool]) -> dict[K, V]:
    """过滤字典中满足条件的键值对。"""
    return {k: v for k, v in m.items() if fn(k, v)}
```

**使用示例**:
```python
# 合并
merged = merge(config1, config2)

# 翻转键值
role_by_id = invert(id_by_role)

# 过滤
active_users = filter_dict(users, lambda k, v: v.is_active)
```

---

### 6. 分页工具封装

**问题**: 分页参数计算和响应构造在各 API 中重复出现。

**封装方案**:

```python
"""分页工具封装。"""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class PageParams:
    """分页请求参数。"""
    page: int = 1       # 当前页码，从 1 开始
    page_size: int = 20 # 每页条数

    def offset(self) -> int:
        """计算数据库偏移量。"""
        if self.page <= 0:
            return 0
        return (self.page - 1) * self.limit()

    def limit(self) -> int:
        """返回安全的每页条数（默认 20，最大 100）。"""
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
    pages: int  # 总页数


def page_result(items: list[T], total: int, params: PageParams) -> PageResult[T]:
    """构造分页结果。"""
    limit = params.limit()
    pages = total // limit + (1 if total % limit > 0 else 0)
    return PageResult(
        items=items,
        total=total,
        page=params.page,
        page_size=limit,
        pages=pages,
    )
```

**使用示例**:
```python
params = PageParams(page=2, page_size=20)
users = db.find_users(offset=params.offset(), limit=params.limit())
result = page_result(users, total_count, params)
```

---

### 7. Retry 重试工具封装

**问题**: 外部调用失败后的重试逻辑散落各处，退避策略不统一。

**封装方案**:

```python
"""带指数退避的重试工具。"""

import time
import logging
from typing import Callable, TypeVar
from dataclasses import dataclass

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class RetryConfig:
    """重试配置。"""
    max_attempts: int = 3       # 最大尝试次数（含首次）
    initial_wait: float = 1.0   # 首次重试等待时间（秒）
    max_wait: float = 30.0      # 最大等待时间（秒）
    multiplier: float = 2.0     # 退避倍数


def retry(
    fn: Callable[..., T],
    *args: Any,
    config: RetryConfig | None = None,
    **kwargs: Any,
) -> T:
    """执行带指数退避的重试。

    fn 返回值表示成功，抛出异常表示需要重试。
    """
    cfg = config or RetryConfig()
    wait = cfg.initial_wait

    for attempt in range(1, cfg.max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if attempt == cfg.max_attempts:
                raise RuntimeError(
                    f"重试 {cfg.max_attempts} 次后仍失败: {e}"
                ) from e

            logger.warning(f"第 {attempt} 次尝试失败: {e}, {wait}s 后重试")
            time.sleep(wait)

            # 指数退避
            wait = min(wait * cfg.multiplier, cfg.max_wait)

    raise RuntimeError("不应到达此处")
```

**使用示例**:
```python
result = retry(
    call_external_api,
    config=RetryConfig(max_attempts=5, initial_wait=0.5),
)
```

---

### 8. 类型转换工具封装

**问题**: `Any` / `object` 到具体类型的转换代码冗长且容易出错。

**封装方案**:

```python
"""安全类型转换工具。"""

from typing import Any


def to_int(value: Any, default: int = 0) -> int:
    """安全地将 Any 转换为 int。"""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default


def to_float(value: Any, default: float = 0.0) -> float:
    """安全地将 Any 转换为 float。"""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    return default


def to_str(value: Any, default: str = "") -> str:
    """安全地将 Any 转换为 str。"""
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if value is None:
        return default
    return str(value)


def to_bool(value: Any, default: bool = False) -> bool:
    """安全地将 Any 转换为 bool。"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    if isinstance(value, int):
        return value != 0
    return default
```

**使用示例**:
```python
page = to_int(request.args.get("page"), default=1)
active = to_bool(config.get("active"), default=False)
```

---

### 9. 业务错误码封装

**问题**: 各 API 错误响应格式不统一，错误码散落各处。

**封装方案**:

```python
"""业务错误码封装。"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorCode:
    """业务错误码类型。"""
    code: int
    message: str
    http_code: int


# 预定义错误码
ERR_INVALID_PARAM = ErrorCode(10001, "参数无效", 400)
ERR_UNAUTHORIZED = ErrorCode(10002, "未授权", 401)
ERR_NOT_FOUND = ErrorCode(10003, "资源不存在", 404)
ERR_CONFLICT = ErrorCode(10004, "资源冲突", 409)
ERR_INTERNAL = ErrorCode(10005, "内部错误", 500)


class AppError(Exception):
    """标准化业务错误，包含错误码、HTTP 状态码和原因。"""

    def __init__(
        self,
        error_code: ErrorCode,
        cause: Exception | None = None,
    ) -> None:
        self.code = error_code.code
        self.message = error_code.message
        self.http_code = error_code.http_code
        self.cause = cause
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if self.cause:
            return f"[{self.code}] {self.message}: {self.cause}"
        return f"[{self.code}] {self.message}"

    def to_dict(self) -> dict[str, Any]:
        """生成标准化的错误响应字典。"""
        return {"code": self.code, "message": self.message}
```

**使用示例**:
```python
# 基本使用
raise AppError(ERR_NOT_FOUND, cause=ValueError(f"user {id} not found"))

# 在 FastAPI handler 中
try:
    ...
except AppError as e:
    return JSONResponse(status_code=e.http_code, content=e.to_dict())
```

---

### 10. 参数验证器封装

**问题**: 参数校验散落在各 handler 中，if-else 堆叠难以维护。

**封装方案**:

```python
"""参数验证器，收集所有错误。"""

import re
import unicodedata
from typing import Callable


class Validator:
    """参数验证器，链式调用收集所有错误。"""

    def __init__(self) -> None:
        self._errors: list[str] = []

    def not_blank(self, field: str, value: str) -> "Validator":
        """校验字符串非空。"""
        if not value or not value.strip():
            self._errors.append(f"{field} 不能为空")
        return self

    def min_len(self, field: str, value: str, min_length: int) -> "Validator":
        """校验最小长度。"""
        if len(value) < min_length:
            self._errors.append(f"{field} 长度不能小于 {min_length}")
        return self

    def max_len(self, field: str, value: str, max_length: int) -> "Validator":
        """校验最大长度。"""
        if len(value) > max_length:
            self._errors.append(f"{field} 长度不能超过 {max_length}")
        return self

    def in_range(self, field: str, value: int, min_val: int, max_val: int) -> "Validator":
        """校验整数范围。"""
        if value < min_val or value > max_val:
            self._errors.append(f"{field} 必须在 {min_val}~{max_val} 之间")
        return self

    def email(self, field: str, value: str) -> "Validator":
        """校验邮箱格式。"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            self._errors.append(f"{field} 邮箱格式无效")
        return self

    def mobile(self, field: str, value: str) -> "Validator":
        """校验手机号（中国大陆）。"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            self._errors.append(f"{field} 手机号格式无效")
        return self

    def alphanumeric(self, field: str, value: str) -> "Validator":
        """校验仅含字母和数字。"""
        for ch in value:
            cat = unicodedata.category(ch)
            if cat not in ("Lu", "Ll", "Nd"):
                self._errors.append(f"{field} 只能包含字母和数字")
                break
        return self

    def custom(self, field: str, ok: bool, msg: str) -> "Validator":
        """自定义校验规则。"""
        if not ok:
            self._errors.append(f"{field} {msg}")
        return self

    def valid(self) -> list[str] | None:
        """返回验证结果，None 表示全部通过。"""
        if not self._errors:
            return None
        return self._errors
```

**使用示例**:
```python
errors = Validator() \
    .not_blank("用户名", req.username) \
    .min_len("密码", req.password, 8) \
    .email("邮箱", req.email) \
    .mobile("手机号", req.mobile) \
    .custom("年龄", req.age >= 18, "必须年满18岁") \
    .valid()

if errors:
    raise AppError(ERR_INVALID_PARAM)
```

---

### 11. ID 生成器封装

**问题**: UUID 生成、短 ID 等分散实现，ID 格式不统一。

**封装方案**:

```python
"""ID 生成器工具。"""

import secrets
import time
import uuid


def uuid4() -> str:
    """生成 v4 随机 UUID。"""
    return str(uuid.uuid4())


def uuid4_no_dash() -> str:
    """生成无连字符的 UUID。"""
    return uuid.uuid4().hex


def short_id(length: int = 16) -> str:
    """生成短 ID，基于时间戳+随机数。"""
    ts = int(time.time() * 1000) & 0xFFFFFFFF
    rand = secrets.token_hex(length // 2)
    return f"{ts:08x}{rand}"


def random_hex(length: int = 32) -> str:
    """生成随机十六进制字符串。"""
    return secrets.token_hex(length // 2)


def random_token(length: int = 32) -> str:
    """生成 URL 安全的随机 token。"""
    return secrets.token_urlsafe(length)
```

**使用示例**:
```python
id = uuid4()          # "550e8400-e29b-41d4-a716-446655440000"
short = short_id()    # "18f3a2bc7d9e1f0a"
token = random_token() # "aBcDeFgH..."
```

---

### 12. 时间格式化工具封装

**问题**: 时间格式化字符串散落各处，格式不统一。

**封装方案**:

```python
"""时间格式化工具。"""

from datetime import datetime, date, time, timedelta
from typing import Final

# 常用时间格式常量
DATETIME_SEC: Final = "%Y-%m-%d %H:%M:%S"
DATETIME_MILLI: Final = "%Y-%m-%d %H:%M:%S.%f"
DATE_ONLY: Final = "%Y-%m-%d"
TIME_ONLY: Final = "%H:%M:%S"
ISO8601: Final = "%Y-%m-%dT%H:%M:%S"


def format_datetime(dt: datetime) -> str:
    """格式化为 "YYYY-MM-DD HH:MM:SS"。"""
    return dt.strftime(DATETIME_SEC)


def format_date(dt: datetime | date) -> str:
    """格式化为 "YYYY-MM-DD"。"""
    if isinstance(dt, datetime):
        return dt.strftime(DATE_ONLY)
    return dt.isoformat()


def parse_datetime(s: str) -> datetime:
    """解析 "YYYY-MM-DD HH:MM:SS" 格式。"""
    return datetime.strptime(s, DATETIME_SEC)


def parse_date(s: str) -> date:
    """解析 "YYYY-MM-DD" 格式。"""
    return datetime.strptime(s, DATE_ONLY).date()


def start_of_day(dt: datetime) -> datetime:
    """返回当天的 00:00:00。"""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """返回当天的 23:59:59.999999。"""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_week(dt: datetime) -> datetime:
    """返回当周周一的 00:00:00。"""
    dt = start_of_day(dt)
    weekday = dt.weekday()  # Monday=0, Sunday=6
    return dt - timedelta(days=weekday)


def start_of_month(dt: datetime) -> datetime:
    """返回当月第一天的 00:00:00。"""
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def end_of_month(dt: datetime) -> datetime:
    """返回当月最后一天的 23:59:59.999999。"""
    next_month = dt.replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)
    return end_of_day(next_month - timedelta(days=1))


def timestamp_milli(dt: datetime) -> int:
    """返回毫秒级时间戳。"""
    return int(dt.timestamp() * 1000)


def from_timestamp_milli(ms: int) -> datetime:
    """从毫秒级时间戳创建 datetime。"""
    return datetime.fromtimestamp(ms / 1000)
```

**使用示例**:
```python
# 格式化
formatted = format_datetime(now)

# 解析
parsed = parse_datetime("2024-01-15 10:30:00")

# 日期范围
start = start_of_month(now)
end = end_of_month(now)
```

---

### 13. 文件操作工具封装

**问题**: 读写 JSON/YAML 文件、安全创建目录等操作重复编写。

**封装方案**:

```python
"""文件操作工具封装。"""

import json
import os
from pathlib import Path
from typing import Any


def read_json(path: str) -> dict[str, Any]:
    """从 JSON 文件读取并解码。"""
    data = Path(path).read_text(encoding="utf-8")
    return json.loads(data)


def write_json(path: str, data: Any, indent: int = 2) -> None:
    """将数据编码为 JSON 并写入文件，自动创建目录。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False),
        encoding="utf-8",
    )


def read_file(path: str) -> str:
    """读取文件全部内容。"""
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, data: str) -> None:
    """写入文件，自动创建目录。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding="utf-8")


def exists(path: str) -> bool:
    """判断文件或目录是否存在。"""
    return Path(path).exists()


def touch(path: str) -> None:
    """创建空文件，如已存在则更新修改时间。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()
```

**使用示例**:
```python
# 读取配置
cfg = read_json("config.json")

# 写入数据
write_json("output/result.json", data)

# 检查文件存在
if not exists("data/cache.json"):
    # 首次初始化
```

---

## 封装流程

1. **识别重复逻辑**
   - 搜索项目中相同模式的代码片段
   - 统计重复出现次数 >= 2 的模式
   - 评估封装收益（减少代码量、提升一致性、降低出错率）

2. **选择封装方案**
   - 优先使用标准库（`collections`、`dataclasses`、`typing`）
   - 参数接受标准协议（`Iterable`、`Mapping`、`Callable`）
   - 抛出异常而非静默失败
   - 使用 dataclass 简化定义

3. **实现封装**
   - 仅使用标准库，零外部依赖
   - 完整的类型注解和 docstring
   - 为每个公开函数编写单元测试

4. **验证封装**
   - 运行 `ruff check`
   - 运行 `pytest`
   - 确认原有代码可正确替换为新封装

---

## 快速参考：封装决策树

```
发现重复代码
  ├── 出现 >= 2 次？
  │   ├── 否 → 不封装，保持内联
  │   └── 是 → 逻辑是否稳定？
  │       ├── 否 → 考虑配置化而非封装
  │       └── 是 → 是否可用标准库替代？
  │           ├── 是 → 用标准库
  │           └── 否 → 封装为独立函数
  └── 涉及外部资源（HTTP、DB）？
      └── 是 → 封装为类，便于 Mock 测试
```

---

## 命名约定

| 模块名 | 职责 | 示例 |
|--------|------|------|
| `http_utils` | HTTP 客户端封装 | `Client.get()`, `Client.post()` |
| `sign_utils` | 签名工具 | `Signer.hmac_sha256()`, `signer.sign()` |
| `crypto_utils` | 加密/哈希 | `sha256()`, `aes_encrypt()` |
| `seq_utils` | 序列操作 | `map_()`, `filter_()`, `unique()` |
| `dict_utils` | 字典操作 | `keys()`, `merge()`, `group_by()` |
| `time_utils` | 时间工具 | `format_datetime()`, `start_of_day()` |
| `page_utils` | 分页工具 | `PageParams`, `page_result()` |
| `retry_utils` | 重试工具 | `retry()` |
| `conv_utils` | 类型转换 | `to_int()`, `to_str()`, `to_bool()` |
| `error_utils` | 业务错误码 | `AppError`, `ErrorCode` |
| `validator` | 参数验证器 | `Validator.not_blank()`, `Validator.email()` |
| `id_utils` | ID 生成器 | `uuid4()`, `short_id()`, `random_token()` |
| `file_utils` | 文件操作 | `read_json()`, `write_json()`, `exists()` |

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 代码重构 | 封装重复逻辑为工具函数 | `python-refactor-reviewer` 关注结构优化和设计模式 |
| 最小化代码 | 封装前先问 YAGNI | `python-minimal-code` 关注删除过度设计 |
| 性能问题 | 工具函数的性能优化（列表推导式等） | `python-performance-reviewer` 关注运行时瓶颈 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：工具函数封装                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：识别项目中的重复逻辑并封装为可复用工具函数
# 输入：项目代码文件
# 输出：封装方案（代码 + 使用示例）
#
# 封装步骤：
#   1. 搜索项目中重复出现的代码模式
#   2. 统计重复次数（>= 3 才值得封装）
#   3. 选择封装方案（标准库优先、类型注解优先）
#   4. 实现封装函数（零外部依赖）
#   5. 编写单元测试
#
# 常见封装场景：
#   - HTTP 客户端: → http_utils.Client
#   - 签名计算: → sign_utils.Signer
#   - 加密哈希: → crypto_utils
#   - 列表操作: → seq_utils (map_/filter_/unique/group_by)
#   - 字典操作: → dict_utils (merge/invert/filter_dict)
#   - 分页: → page_utils (PageParams/PageResult)
#   - 重试: → retry_utils.retry
#   - 类型转换: → conv_utils (to_int/to_str/to_bool)
#   - 错误码: → error_utils (AppError/ErrorCode)
#   - 参数验证: → validator.Validator
#   - ID 生成: → id_utils (uuid4/short_id)
#   - 时间格式化: → time_utils
#   - 文件操作: → file_utils
#
# AI-Usage-End
```

## 触发词

- "封装工具函数"
- "通用函数"
- "工具库"
- "HTTP封装"
- "签名工具"
- "加密工具"
- "Python工具函数"
- "utility functions"
- "最小可行封装"
