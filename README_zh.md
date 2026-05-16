# Python 工程化技能集 (python-skill)

<div align="center">

**覆盖完整开发生命周期的 Python 工程化技能库：代码开发、测试、质量审查、文档生成与部署。**

[English](./README.md) | [中文](./README_zh.md)

</div>

---

## ✨ 特性

- 🚀 **全生命周期覆盖**：需求分析 → 代码实现 → 测试 → 质量审查 → 文档 → 部署
- 🤖 **AI 友好**：所有文档包含 AI-Usage 注释块，支持 Cline/Cursor 学习
- 📦 **19+ 专项技能**：覆盖开发各方面
- 🛡️ **严格标准**：PEP 8、Google/NumPy docstring 规范
- 🔒 **类型安全**：全量 TypeHint + Mypy 静态检查（Python 3.10+）
- 🧩 **模块化设计**：技能可独立使用，也可组合联动
- 🏗️ **架构级别**：架构审查、重构审查、配置审查
- 🔄 **CI/CD 就绪**：GitHub Actions、Docker、pre-commit、质量门禁

---

## 📁 项目结构

```
python-skill/
├── README.md                               # 英文文档
├── README_zh.md                           # 中文文档
│
├── 📂 开发工作流/
│   ├── python-project-rules/              # 项目治理规则
│   ├── python-full-dev-workflow/           # 完整开发工作流
│   ├── python-feature-development-workflow/ # 新功能开发工作流
│   └── python-ci-cd-workflow/              # CI/CD 流水线工作流
│
├── 📂 测试/
│   └── python-test-generator/               # pytest 测试生成
│
├── 📂 代码审查/
│   ├── python-error-handling-reviewer/    # 错误处理审查
│   ├── python-concurrency-reviewer/        # 并发安全审查
│   ├── python-security-reviewer/           # 安全审查
│   ├── python-database-reviewer/           # 数据库审查
│   ├── python-dependency-reviewer/         # 依赖管理审查
│   ├── python-performance-reviewer/        # 性能审查
│   ├── python-logging-reviewer/            # 日志规范审查
│   ├── python-typing-reviewer/             # 类型注解审查
│   ├── python-api-design-reviewer/         # API 设计审查
│   ├── python-refactor-reviewer/           # 代码重构审查
│   ├── python-config-reviewer/             # 配置管理审查
│   └── python-architecture-reviewer/       # 架构设计审查
│
└── 📂 文档生成/
    ├── python-doc-generator/               # 代码文档生成
    └── python-api-doc-generator/          # API 文档生成
```

---

## 🎯 技能概览

### 开发工作流

| 技能 | 说明 |
|------|------|
| [python-project-rules](./python-project-rules/) | 项目治理、进度同步、README 联动 |
| [python-full-dev-workflow](./python-full-dev-workflow/) | 完整开发工作流整合 |
| [python-feature-development-workflow](./python-feature-development-workflow/) | 需求拆解、TDD/BDD 开发 |
| [python-ci-cd-workflow](./python-ci-cd-workflow/) | GitHub Actions、Docker、质量门禁、发布自动化 |

### 测试

| 技能 | 说明 |
|------|------|
| [python-test-generator](./python-test-generator/) | pytest 单元测试、Mock、覆盖率优化 |

### 代码审查

| 技能 | 说明 |
|------|------|
| [python-error-handling-reviewer](./python-error-handling-reviewer/) | 异常包装、参数校验 |
| [python-concurrency-reviewer](./python-concurrency-reviewer/) | 线程安全、GIL 理解、异步审查 |
| [python-security-reviewer](./python-security-reviewer/) | 敏感数据、注入攻击、依赖漏洞 |
| [python-database-reviewer](./python-database-reviewer/) | 连接池、事务处理、N+1 检测 |
| [python-dependency-reviewer](./python-dependency-reviewer/) | 第三方依赖必要性、安全性 |
| [python-performance-reviewer](./python-performance-reviewer/) | 资源清理、内存泄漏、异步优化 |
| [python-logging-reviewer](./python-logging-reviewer/) | 日志级别、数据脱敏、结构化日志 |
| [python-typing-reviewer](./python-typing-reviewer/) | TypeHint 完整性、Protocol 使用、Python 3.10+ 语法 |
| [python-api-design-reviewer](./python-api-design-reviewer/) | RESTful 规范、HTTP 语义 |
| [python-refactor-reviewer](./python-refactor-reviewer/) | DRY 原则、复杂度、Pythonic 惯用法、设计模式 |
| [python-config-reviewer](./python-config-reviewer/) | pydantic-settings、.env、pyproject.toml、12-Factor App |
| [python-architecture-reviewer](./python-architecture-reviewer/) | 分层架构、依赖方向、SOLID 原则 |

### 文档生成

| 技能 | 说明 |
|------|------|
| [python-doc-generator](./python-doc-generator/) | Docstring、README、AI 友好示例 |
| [python-api-doc-generator](./python-api-doc-generator/) | OpenAPI 3.0、Postman 集合、curl 命令 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 推荐 Python 3.10+
python --version

# 安装开发依赖
pip install pytest mypy black isort safety
```

### 2. 运行完整工作流

```bash
# 执行完整开发流程
"运行开发工作流"
"Python 开发流程"
```

### 3. 使用单个技能

```bash
# 代码审查
"安全审查"
"代码审查"
"类型注解审查"
"架构审查"
"重构审查"
"配置审查"

# 测试生成
"生成测试"
"写单元测试"

# 文档生成
"生成 API 文档"
"生成 Docstring"

# CI/CD
"配置 CI/CD"
"配置 GitHub Actions"
```

---

## 📊 开发工作流

```
┌─────────────────────────────────────────────────────────┐
│                      阶段零：项目治理                     │
│  python-project-rules                                    │
│  - 读取 README.md、project.md                           │
│  - 进度同步、架构联动、提交检查                           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段一：准备与文档                   │
│  python-feature-development-workflow → 需求澄清          │
│  python-doc-generator         → 项目结构文档             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段二：代码实现                     │
│  - Docstring + TypeHint 类型注解                         │
│  - 异常处理 + 日志记录                                   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段三：测试生成                     │
│  python-test-generator                                   │
│  - 正常路径 + 边界情况 + 错误路径 + 异步测试             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段四：质量审查                     │
│  error / concurrency / security / performance           │
│  database / logging / typing / api-design               │
│  refactor / config / architecture                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段五：文档生成                     │
│  python-api-doc-generator                               │
│  - OpenAPI 3.0 + Postman + curl 示例                    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段六：CI/CD 与部署                │
│  python-ci-cd-workflow                                   │
│  - 代码检查 + 类型检查 + 测试 + 构建 + 部署             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码标准

```bash
# 格式化（PEP 8）
black --check .

# 导入排序
isort --check .

# 静态类型检查
mypy .

# 测试执行
pytest -v --cov=. --cov-report=term-missing

# 安全扫描
safety check
```

---

## 📖 使用场景

- 🏗️ 新项目初始化和架构设计
- ⚙️ 复杂业务逻辑开发
- 🔍 代码质量审计和重构
- 📚 API 文档自动化
- 👥 团队编码规范对齐
- 🌐 Python Web 开发（FastAPI/Django/Flask）
- 📊 数据处理和科学计算项目
- 🔄 CI/CD 流水线配置和自动化

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/xxx`）
3. 提交变更（`git commit -m 'feat: add xxx'`）
4. 推送到分支（`git push origin feature/xxx`）
5. 创建 Pull Request

---

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star！**

</div>
