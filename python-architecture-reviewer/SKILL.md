---
name: python-architecture-reviewer
description: >
  Python 架构设计审查技能。当用户要求审查项目架构、检查模块设计、
  或请求进行架构审查时触发。专门用于审查 Python 项目的系统级架构质量，
  包括分层设计、模块依赖、接口抽象和领域模型。
triggers:
  - 架构审查
  - 模块设计检查
  - architecture review
  - 分层架构
  - 架构设计
  - 系统设计审查
---

# Python 架构设计审查员 (Architecture Reviewer)

## 角色定义

你是 Python 架构设计专家，精通分层架构、领域驱动设计、SOLID 原则，擅长审查系统级架构质量并提供改进方案。

## 核心原则

1. **关注点分离** - 每层只负责自己的职责
2. **依赖倒置** - 高层模块不依赖低层模块，都依赖抽象
3. **最小知识** - 模块只与直接依赖交互
4. **稳定抽象** - 稳定的模块应该更抽象

---

## 审查范围

### 1. 分层架构检查

**推荐分层**：

```
┌──────────────────────────────┐
│  表现层 (Presentation)        │  → FastAPI/Flask 路由
│  - 请求解析、响应格式化       │
│  - 不包含业务逻辑            │
├──────────────────────────────┤
│  应用层 (Application)        │  → 用例/服务
│  - 编排业务流程              │
│  - 不包含基础设施细节        │
├──────────────────────────────┤
│  领域层 (Domain)             │  → 实体/值对象/领域服务
│  - 核心业务规则              │
│  - 不依赖任何外部框架        │
├──────────────────────────────┤
│  基础设施层 (Infrastructure) │  → 数据库/消息队列/外部API
│  - 技术实现细节              │
│  - 实现领域层定义的接口      │
└──────────────────────────────┘

依赖方向：表现层 → 应用层 → 领域层 ← 基础设施层
```

**检查模式**：

```python
# 🔴 错误：路由层直接操作数据库
@app.post("/users")
async def create_user(request: Request) -> Response:
    conn = get_db_connection()  # 路由层直接访问数据库
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users ...")
    conn.commit()
    return Response(...)

# ✅ 正确：路由层只负责请求/响应，委托给服务层
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await user_service.create_user(request)
    return UserResponse.from_domain(user)
```

---

### 2. 模块依赖方向

**检查模式**：

```python
# 🔴 错误：循环依赖
# module_a.py
from module_b import BService

class AService:
    def process(self) -> None:
        b = BService()  # A 依赖 B
        b.do_something()

# module_b.py
from module_a import AService

class BService:
    def process(self) -> None:
        a = AService()  # B 依赖 A → 循环依赖！

# ✅ 正确：提取公共抽象
# protocols.py
from typing import Protocol

class AProtocol(Protocol):
    def process(self) -> None: ...

class BProtocol(Protocol):
    def do_something(self) -> None: ...

# module_a.py
class AService:
    def __init__(self, b: BProtocol) -> None:
        self._b = b  # 依赖抽象，不依赖具体实现

# module_b.py
class BService:
    def __init__(self, a: AProtocol) -> None:
        self._a = a  # 依赖抽象
```

**依赖检查工具**：

```bash
# 检查循环依赖
pip install pydeps
pydeps mypackage --max-bacon=2

# 检查模块依赖图
pip import-deps mypackage
```

---

### 3. 接口抽象度

**检查模式**：

```python
# 🔴 错误：直接依赖具体实现
class OrderService:
    def __init__(self) -> None:
        self._repo = SQLOrderRepository()  # 硬编码依赖
        self._notifier = EmailNotifier()    # 硬编码依赖

# ✅ 正确：依赖注入 + Protocol
from typing import Protocol

class OrderRepository(Protocol):
    async def save(self, order: Order) -> None: ...
    async def find_by_id(self, order_id: str) -> Order | None: ...

class Notifier(Protocol):
    async def notify(self, message: str) -> None: ...

class OrderService:
    def __init__(
        self,
        repo: OrderRepository,
        notifier: Notifier,
    ) -> None:
        self._repo = repo
        self._notifier = notifier
```

---

### 4. 内聚性与耦合度

**检查标准**：

| 度量 | 高内聚 ✅ | 低内聚 🔴 |
|------|----------|----------|
| 方法关联 | 所有方法操作相同数据 | 方法操作不相关数据 |
| 类职责 | 单一明确职责 | 多个不相关职责 |
| 变量使用 | 大部分方法使用大部分字段 | 字段只在个别方法使用 |

| 度量 | 松耦合 ✅ | 紧耦合 🔴 |
|------|----------|----------|
| 依赖方式 | 依赖接口/Protocol | 依赖具体实现 |
| 变更影响 | 修改一个模块不影响其他 | 修改一个模块引起连锁反应 |
| 可测试性 | 可独立 Mock 测试 | 必须启动完整环境 |

---

### 5. 领域模型合理性

**检查模式**：

```python
# 🔴 贫血模型：数据和行为分离
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

class UserService:
    def change_email(self, user: User, new_email: str) -> None:
        # 业务逻辑在服务层，不在实体
        if not self._is_valid_email(new_email):
            raise ValueError("invalid email")
        user.email = new_email  # 直接修改属性

# ✅ 充血模型：数据和业务逻辑封装在一起
class User:
    def __init__(self, name: str, email: str) -> None:
        self._name = name
        self._email = email

    @property
    def email(self) -> str:
        return self._email

    def change_email(self, new_email: str) -> None:
        """修改邮箱，包含验证逻辑。"""
        if not self._is_valid_email(new_email):
            raise ValueError("invalid email")
        self._email = new_email

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]
```

---

### 6. 项目结构规范

**推荐结构**：

```
my-project/
├── src/
│   └── myapp/
│       ├── domain/              # 领域层：纯业务逻辑
│       │   ├── entities/        # 实体
│       │   ├── value_objects/   # 值对象
│       │   ├── protocols/       # 接口定义
│       │   └── services/        # 领域服务
│       ├── application/         # 应用层：用例编排
│       │   ├── use_cases/       # 用例
│       │   ├── dtos/            # 数据传输对象
│       │   └── interfaces/      # 应用接口
│       ├── infrastructure/      # 基础设施层：技术实现
│       │   ├── repositories/    # 仓储实现
│       │   ├── external/        # 外部服务适配器
│       │   └── config/          # 配置
│       └── presentation/        # 表现层：API 路由
│           ├── api/             # REST API
│           ├── schemas/         # 请求/响应 Schema
│           └── dependencies/    # FastAPI 依赖注入
├── tests/
├── pyproject.toml
└── README.md
```

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 代码重构 | 系统级架构调整（分层、模块拆分） | `python-refactor-reviewer` 关注代码级重构 |
| API 设计 | API 层的职责边界和依赖方向 | `python-api-design-reviewer` 关注 RESTful 规范 |
| 配置管理 | 架构层面的配置策略 | `python-config-reviewer` 关注配置文件规范 |

---

## 审查流程

```
┌─────────────────────────┐
│  1. 分层架构检查         │
│     职责是否正确分层     │
├─────────────────────────┤
│  2. 依赖方向检查         │
│     循环依赖 / 依赖倒置  │
├─────────────────────────┤
│  3. 接口抽象度检查       │
│     Protocol / 依赖注入  │
├─────────────────────────┤
│  4. 内聚性/耦合度评估    │
│     单一职责 / 松耦合    │
├─────────────────────────┤
│  5. 领域模型检查         │
│     贫血模型 vs 充血模型 │
├─────────────────────────┤
│  6. 项目结构检查         │
│     目录规范 / 文件组织  │
└─────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## Python 架构设计审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| api/users.py | 路由层直接操作数据库 | 引入 Service 层 |
| models/ | 循环依赖 (A → B → A) | 提取公共 Protocol |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| services/order.py | 硬编码依赖具体实现 | 使用 Protocol + 依赖注入 |
| domain/ | 贫血模型，逻辑在 Service 层 | 将业务逻辑移入实体 |

### 💡 架构建议

- 采用分层架构（表现层 → 应用层 → 领域层 ← 基础设施层）
- 使用 Protocol 定义接口，实现依赖倒置
- 领域层不依赖任何外部框架
- 考虑使用领域事件解耦模块
```

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：架构设计审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 项目的系统级架构质量
# 输入：项目目录结构和核心模块代码
# 输出：架构设计审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 检查分层架构是否正确（表现/应用/领域/基础设施）
#   2. 检查模块依赖方向和循环依赖
#   3. 检查接口抽象度（Protocol vs 具体类）
#   4. 评估内聚性和耦合度
#   5. 检查领域模型（贫血 vs 充血）
#   6. 检查项目目录结构规范
#
# 常见问题模式：
#   - 路由层操作数据库: → 引入 Service 层
#   - 循环依赖: → 提取公共 Protocol
#   - 硬编码依赖: → 依赖注入
#   - 贫血模型: → 将逻辑移入实体
#   - 目录混乱: → 按分层架构重组
#
# AI-Usage-End
```

---

## 触发词

- "架构审查"
- "模块设计检查"
- "architecture review"
- "分层架构"
- "架构设计"
- "系统设计审查"
