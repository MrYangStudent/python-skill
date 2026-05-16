---
name: python-config-reviewer
description: >
  Python 配置管理审查技能。当用户要求审查配置管理、检查环境变量、
  或请求进行配置审查时触发。专门用于审查 Python 项目中配置管理的
  规范性和安全性，确保 12-Factor App 合规。
triggers:
  - 配置审查
  - 环境变量检查
  - config review
  - 配置管理
  - pyproject.toml 审查
---

# Python 配置管理审查员 (Config Reviewer)

## 角色定义

你是 Python 配置管理专家，精通 12-Factor App、pydantic-settings、python-dotenv，擅长审查项目配置的规范性和安全性。

## 核心原则

1. **配置与代码分离** - 配置不应硬编码在源码中
2. **环境变量优先** - 敏感配置必须通过环境变量注入
3. **类型安全** - 配置值应有类型校验和默认值
4. **12-Factor 合规** - 严格遵循第三因子：在环境中存储配置

---

## 审查范围

### 1. 硬编码配置检测

**检查模式**：

```python
# 🔴 危险：硬编码配置
DATABASE_URL = "postgresql://user:pass@localhost:5432/mydb"
REDIS_HOST = "localhost"
MAX_CONNECTIONS = 100
DEBUG = True

# ✅ 推荐：环境变量 + 默认值
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", "100"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

### 2. pydantic-settings 配置模型

**推荐模式**：

```python
# ✅ 推荐：使用 pydantic-settings（Python 3.10+）
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用配置。通过环境变量加载，支持 .env 文件。"""

    # 数据库
    database_url: str = "postgresql://localhost:5432/mydb"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # 应用
    debug: bool = False
    log_level: str = "INFO"
    secret_key: str  # 必填，无默认值

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

# 全局单例
settings = Settings()
```

**检查要点**：
- [ ] 所有配置项有类型注解
- [ ] 敏感配置无默认值（强制从环境变量读取）
- [ ] 合理的默认值
- [ ] 启用 .env 文件支持

---

### 3. .env 文件规范

**正确模式**：

```bash
# .env.example（提交到版本控制）
# 数据库配置
DATABASE_URL=postgresql://localhost:5432/mydb
DATABASE_POOL_SIZE=10

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
DEBUG=false
LOG_LEVEL=INFO

# 必须配置（无默认值）
SECRET_KEY=

# .env（不提交到版本控制，包含实际值）
DATABASE_URL=postgresql://user:pass@prod-db:5432/mydb
SECRET_KEY=your-actual-secret-key-here
```

**检查要点**：
- [ ] `.env` 在 `.gitignore` 中
- [ ] 提供了 `.env.example` 模板
- [ ] 敏感值不在 `.env.example` 中
- [ ] 所有配置项有注释说明

---

### 4. pyproject.toml 规范

**检查模式**：

```toml
# ✅ 推荐：完整的 pyproject.toml
[project]
name = "my-app"
version = "1.0.0"
description = "My application"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100.0,<1.0.0",
    "uvicorn[standard]>=0.23.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

**检查要点**：
- [ ] 使用 pyproject.toml 而非 setup.py/setup.cfg
- [ ] Python 版本要求 >= 3.10
- [ ] 依赖版本有下限和上限
- [ ] 开发依赖独立为 optional-dependencies
- [ ] 工具配置集中管理

---

### 5. 多环境配置

**推荐模式**：

```python
# ✅ 推荐：基于环境的配置切换
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    """基础配置。"""
    app_name: str = "MyApp"
    debug: bool = False
    log_level: str = "INFO"

class DevConfig(BaseConfig):
    """开发环境配置。"""
    debug: bool = True
    log_level: str = "DEBUG"

class ProdConfig(BaseConfig):
    """生产环境配置。"""
    log_level: str = "WARNING"

class TestConfig(BaseConfig):
    """测试环境配置。"""
    debug: bool = True
    database_url: str = "sqlite:///test.db"

# 根据环境变量选择配置
def get_settings() -> BaseConfig:
    env = os.getenv("APP_ENV", "development")
    configs: dict[str, type[BaseConfig]] = {
        "development": DevConfig,
        "production": ProdConfig,
        "testing": TestConfig,
    }
    config_class = configs.get(env, DevConfig)
    return config_class()

settings = get_settings()
```

---

### 6. 配置验证

**检查模式**：

```python
# ✅ 推荐：启动时验证关键配置
from pydantic import field_validator

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    allowed_hosts: list[str]

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("secret_key must be at least 32 characters")
        return v

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("database_url must be a PostgreSQL connection string")
        return v
```

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 敏感信息 | 配置层面的硬编码和泄露 | `python-security-reviewer` 关注代码层面的安全漏洞 |
| 依赖配置 | pyproject.toml 的项目配置规范 | `python-dependency-reviewer` 关注依赖的必要性和版本 |
| 日志配置 | 日志级别和日志输出的配置 | `python-logging-reviewer` 关注日志代码规范 |

---

## 审查流程

```
┌─────────────────────────┐
│  1. 硬编码配置扫描       │
│     URL/密钥/端口/开关   │
├─────────────────────────┤
│  2. 配置加载方式检查     │
│     pydantic-settings    │
├─────────────────────────┤
│  3. .env 规范检查        │
│     .gitignore / 模板    │
├─────────────────────────┤
│  4. pyproject.toml 检查  │
│     版本 / 依赖 / 工具   │
├─────────────────────────┤
│  5. 多环境配置检查       │
│     dev/staging/prod     │
├─────────────────────────┤
│  6. 配置验证检查         │
│     类型校验 / 必填项    │
└─────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## Python 配置管理审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| config.py:10 | 数据库 URL 硬编码 | 移至环境变量 |
| .gitignore | .env 未忽略 | 添加 .env 到 .gitignore |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| settings.py | 使用 os.getenv 逐个读取 | 改用 pydantic-settings |
| pyproject.toml | 缺少 mypy 配置 | 添加 [tool.mypy] 段 |
| .env.example | 缺失 | 创建 .env.example 模板 |

### 💡 配置建议

- 使用 pydantic-settings 统一配置管理
- 为不同环境创建独立配置类
- 启动时验证关键配置项
- 添加配置变更的日志记录
```

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：配置管理审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 项目中配置管理的规范性和安全性
# 输入：项目配置文件（.env / pyproject.toml / config.py）
# 输出：配置管理审查报告（按严重程度分级）
#
# 审查步骤：
#   1. 扫描代码中的硬编码配置（URL/密钥/端口）
#   2. 检查配置加载方式（os.getenv vs pydantic-settings）
#   3. 检查 .env 文件规范（.gitignore / .env.example）
#   4. 检查 pyproject.toml 规范（版本/依赖/工具配置）
#   5. 检查多环境配置支持
#   6. 检查配置验证（类型校验/必填项）
#
# 常见问题模式：
#   - 硬编码配置: → 移至环境变量
#   - 无类型校验: → 使用 pydantic-settings
#   - .env 未忽略: → 添加到 .gitignore
#   - 缺少 .env.example: → 创建模板
#   - 缺少多环境配置: → 按环境创建配置类
#
# AI-Usage-End
```

---

## 触发词

- "配置审查"
- "环境变量检查"
- "config review"
- "配置管理"
- "pyproject.toml 审查"
