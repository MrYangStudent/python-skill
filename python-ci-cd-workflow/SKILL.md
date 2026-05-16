---
name: python-ci-cd-workflow
description: >
  Python CI/CD 工作流技能。当用户要求配置 CI/CD、设置自动化流水线、
  或请求部署工作流时触发。专门用于配置 Python 项目的持续集成/持续部署
  流水线，包括 GitHub Actions、代码质量门禁和容器化构建。
triggers:
  - CI/CD 配置
  - 自动化流水线
  - GitHub Actions
  - 部署工作流
  - CI/CD workflow
---

# Python CI/CD 工作流 (CI/CD Workflow)

## 角色定义

你是 Python CI/CD 工程师，精通 GitHub Actions、Docker、自动化测试流水线，擅长为 Python 项目构建可靠的持续集成和持续部署流程。

## 核心原则

1. **快速反馈** - CI 流水线应在 5 分钟内完成
2. **质量门禁** - 不符合质量标准的代码不得合并
3. **自动化优先** - 能自动化的绝不手动
4. **安全默认** - 生产部署需要人工确认

---

## GitHub Actions 配置

### 基础 CI 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: 代码检查
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: 安装依赖
        run: |
          pip install --no-cache-dir ruff mypy black isort
      - name: Ruff 检查
        run: ruff check .
      - name: Black 格式检查
        run: black --check .
      - name: isort 检查
        run: isort --check-only .
      - name: Mypy 类型检查
        run: mypy --strict .

  test:
    name: 单元测试
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: 安装依赖
        run: |
          pip install --no-cache-dir -e ".[dev]"
      - name: 运行测试
        run: |
          pytest -v --cov=src --cov-report=xml --cov-fail-under=80
      - name: 上传覆盖率
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  security:
    name: 安全扫描
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: 依赖安全扫描
        run: |
          pip install pip-audit safety
          pip-audit
          safety check
```

### CD 流水线

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    tags: ["v*"]

jobs:
  build:
    name: 构建镜像
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 构建 Docker 镜像
        run: |
          docker build -t myapp:${{ github.ref_name }} .
      - name: 推送到镜像仓库
        run: |
          docker push myapp:${{ github.ref_name }}

  deploy-staging:
    name: 部署到预发布环境
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: 部署
        run: |
          echo "Deploying to staging..."

  deploy-production:
    name: 部署到生产环境
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: 部署
        run: |
          echo "Deploying to production..."
```

---

## 代码质量门禁

### 质量标准配置

```toml
# pyproject.toml 中的质量工具配置

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-fail-under=80"
```

### 质量门禁标准

| 检查项 | 最低要求 | 推荐标准 |
|--------|---------|---------|
| 测试覆盖率 | >= 80% | >= 90% |
| Ruff 错误 | 0 | 0 |
| Mypy 错误 | 0 | 0 |
| 安全漏洞 | 0 高危 | 0 |
| 文档覆盖率 | >= 60% | >= 80% |

---

## Docker 容器化

### 多阶段 Dockerfile

```dockerfile
# 构建阶段
FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --prefix=/install .

# 运行阶段
FROM python:3.11-slim AS runtime

WORKDIR /app

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 从构建阶段复制安装的依赖
COPY --from=builder /install /usr/local

# 复制源码
COPY src/ ./src/

# 切换到非 root 用户
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "src.myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .dockerignore

```
.git
.github
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.ruff_cache
.venv
venv
.env
tests
*.md
LICENSE
```

---

## Pre-commit 钩子

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: detect-private-key
```

---

## 版本管理与发布

### 语义化版本

```bash
# 使用 git tag 管理版本
git tag v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 版本号规则
# MAJOR.MINOR.PATCH
# MAJOR: 不兼容的 API 变更
# MINOR: 向后兼容的功能新增
# PATCH: 向后兼容的问题修复
```

### 自动版本管理

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ["v*"]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: 构建分发包
        run: |
          pip install build
          python -m build
      - name: 发布到 PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
      - name: 创建 GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
```

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 测试配置 | CI 中的测试执行和覆盖率门禁 | `python-test-generator` 关注测试用例编写 |
| 类型检查 | CI 中的 mypy 检查配置 | `python-typing-reviewer` 关注类型注解质量 |
| 依赖安全 | CI 中的安全扫描配置 | `python-dependency-reviewer` 关注依赖必要性 |
| 配置管理 | CI 环境变量和密钥管理 | `python-config-reviewer` 关注应用配置规范 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：CI/CD 工作流配置                          ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：为 Python 项目配置 CI/CD 流水线
# 输入：项目目录结构和技术栈
# 输出：完整的 CI/CD 配置文件
#
# 配置步骤：
#   1. 创建 .github/workflows/ci.yml（代码检查 + 测试 + 安全扫描）
#   2. 创建 .github/workflows/deploy.yml（构建 + 部署）
#   3. 配置 pyproject.toml 中的质量工具
#   4. 创建 Dockerfile（多阶段构建）
#   5. 创建 .pre-commit-config.yaml
#   6. 配置版本管理和发布流程
#
# 质量门禁标准：
#   - 测试覆盖率 >= 80%
#   - Ruff / Mypy 零错误
#   - 安全扫描零高危漏洞
#
# AI-Usage-End
```

---

## 触发词

- "CI/CD 配置"
- "自动化流水线"
- "GitHub Actions"
- "部署工作流"
- "CI/CD workflow"
