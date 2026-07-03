# Python 工程化技能集 (python-skill)

<div align="center">

**覆盖完整开发生命周期的 Python 工程化技能库：代码开发、测试、质量审查、文档生成与部署。**

[English](./README.md) | [中文](./README_zh.md)

<a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/github/stars/MrYangStudent/python-skill?style=flat-square" alt="Stars"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/badge/language-Python-blue?style=flat-square" alt="Language"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/badge/skills-23+-green?style=flat-square" alt="Skills"></a>

</div>

---

## 目录

- [特性](#-特性)
- [背景](#-背景)
- [项目结构](#-项目结构)
- [技能概览](#-技能概览)
  - [开发工作流](#开发工作流)
  - [测试](#测试)
  - [代码审查](#代码审查)
  - [代码精简](#代码精简)
  - [文档生成](#文档生成)
  - [知识管理](#知识管理)
- [快速开始](#-快速开始)
- [开发工作流](#-开发工作流)
- [代码标准](#-代码标准)
- [使用场景](#-使用场景)
- [贡献](#-贡献)
- [作者](#作者)
- [许可证](#-许可证)

---

## ✨ 特性

- 🚀 **全生命周期覆盖**：需求分析 → 代码实现 → 测试 → 质量审查 → 文档 → 部署
- 🤖 **AI 友好**：所有文档包含 AI-Usage 注释块，支持 Cline/Cursor/CodeBuddy 学习
- 📦 **23+ 专项技能**：覆盖开发各方面
- 🛡️ **严格标准**：PEP 8、Google/NumPy docstring 规范
- 🔒 **类型安全**：全量 TypeHint + Mypy 静态检查（Python 3.10+）
- 🧩 **模块化设计**：技能可独立使用，也可组合联动
- 🏗️ **架构级别**：架构审查、重构审查、配置审查
- 🔄 **CI/CD 就绪**：GitHub Actions、Docker、pre-commit、质量门禁

---

## 📖 背景

在使用 AI 编程助手（CodeBuddy、Cline、Cursor）开发 Python 项目时，我们发现：

- AI 助手往往缺乏**领域专业知识** —— 能写代码但容易忽略安全漏洞、并发缺陷和架构问题
- 代码质量审查需要**反复手动提示** —— 每种审查类型都需要不同专业视角
- 文档生成**繁琐且不一致** —— Docstring、API 文档、README 需要不同模板
- **在已有项目中新增功能**风险高 —— 改旧代码加新功能经常破坏已有逻辑

本技能库将 Python 工程化最佳实践封装为**专项、可复用的 AI 技能**。每个技能遵循严格标准（PEP 8、Google Docstring、SOLID 原则），只需通过简单关键词即可在 AI 助手中触发。

---

## 📁 项目结构

```
python-skill/
├── README.md                               # 英文文档
├── README_zh.md                           # 中文文档
├── LICENSE                                # MIT 许可证
│
├── 📂 开发工作流/
│   ├── python-project-rules/              # 项目治理规则
│   ├── python-full-dev-workflow/           # 完整开发工作流
│   ├── python-feature-development-workflow/ # 新功能开发工作流
│   ├── python-incremental-dev/            # 增量开发（已有项目）
│   └── python-ci-cd-workflow/              # CI/CD 流水线工作流
│
├── 📂 测试/
│   └── python-test-generator/               # pytest 测试生成
│
├── 📂 代码审查/
│   ├── python-error-handling-reviewer/    # 错误处理审查
│   ├── python-concurrency-reviewer/        # 并发安全审查
│   ├── python-async-lifecycle-reviewer/   # 异步生命周期审查
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
├── 📂 代码精简/
│   ├── python-minimal-code/               # YAGNI / 最简实现
│   └── python-utility-functions/          # 类型安全工具函数封装
│
├── 📂 文档生成/
│   ├── python-doc-generator/               # 代码文档生成
│   └── python-api-doc-generator/          # API 文档生成
│
└── 📂 知识管理/
    └── wiki-knowledge-base/               # 本地 LLM Wiki 知识库
```

---

## 🎯 技能概览

### 开发工作流

| 技能 | 说明 |
|------|------|
| [python-project-rules](./python-project-rules/) | 项目治理、进度同步、README 联动 |
| [python-full-dev-workflow](./python-full-dev-workflow/) | 完整开发工作流整合（17 技能链） |
| [python-feature-development-workflow](./python-feature-development-workflow/) | 需求拆解、TDD/BDD 开发 |
| [python-incremental-dev](./python-incremental-dev/) | 增量开发（已有项目），最小改动，知识库 CLI |
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
| [python-async-lifecycle-reviewer](./python-async-lifecycle-reviewer/) | asyncio 任务生命周期、取消信号传播、超时控制 |
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

### 代码精简

| 技能 | 说明 |
|------|------|
| [python-minimal-code](./python-minimal-code/) | YAGNI 原则、7级精简阶梯、标准库优先 |
| [python-utility-functions](./python-utility-functions/) | 类型安全工具封装、HTTP 客户端、加密、重试、分页 |

### 文档生成

| 技能 | 说明 |
|------|------|
| [python-doc-generator](./python-doc-generator/) | Docstring、README、AI 友好示例 |
| [python-api-doc-generator](./python-api-doc-generator/) | OpenAPI 3.0、Postman 集合、curl 命令 |

### 知识管理

| 技能 | 说明 |
|------|------|
| [wiki-knowledge-base](./wiki-knowledge-base/) | 本地 LLM Wiki：存入来源 → 结构化页面，检索带引用 |

---

## 🚀 快速开始

### 1. 安装为 CodeBuddy 技能

```bash
# 克隆仓库
git clone https://github.com/MrYangStudent/python-skill.git

# 将需要的技能目录复制到 CodeBuddy 技能文件夹
# Linux/macOS:
cp -r python-skill/python-security-reviewer ~/.codebuddy/skills/
# Windows:
xcopy /E python-skill\python-security-reviewer %USERPROFILE%\.codebuddy\skills\

# 或一次性复制所有技能
cp -r python-skill/python-* ~/.codebuddy/skills/
```

### 2. 环境要求

```bash
# 需要 Python 3.10+
python --version

# 开发依赖（使用这些技能的项目所需）
pip install pytest mypy black isort safety
```

### 3. 在 AI 助手中触发技能

这些技能专为 AI 编程助手（CodeBuddy、Cline、Cursor）设计，在对话中使用触发关键词即可：

**开发工作流：**
- "运行开发工作流" → 触发 `python-full-dev-workflow`
- "增量开发" / "开发新模块" → 触发 `python-incremental-dev`

**代码审查：**
- "安全审查" → 触发 `python-security-reviewer`
- "异步生命周期审查" / "async review" → 触发 `python-async-lifecycle-reviewer`
- "架构审查" → 触发 `python-architecture-reviewer`
- "重构审查" → 触发 `python-refactor-reviewer`

**代码精简：**
- "简化代码" / "YAGNI" → 触发 `python-minimal-code`
- "封装工具函数" → 触发 `python-utility-functions`

**测试生成：**
- "生成测试" / "写单元测试" → 触发 `python-test-generator`

**文档生成：**
- "生成 API 文档" → 触发 `python-api-doc-generator`
- "生成 Docstring" → 触发 `python-doc-generator`

**知识管理：**
- "存入wiki知识库" → 触发 `wiki-knowledge-base` 存入模式
- "检索wiki" → 触发 `wiki-knowledge-base` 查询模式

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
│  python-incremental-dev         → 知识库参照             │
│  python-doc-generator           → 项目结构文档             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                      阶段二：代码实现                     │
│  python-minimal-code → YAGNI / 标准库优先检查            │
│  python-utility-functions → 可复用封装                    │
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
│  error / concurrency / async-lifecycle / security        │
│  performance / database / logging / typing               │
│  api-design / refactor / config / architecture           │
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
- 🧩 已有大型项目的增量功能开发
- 🗂️ 项目知识沉淀与检索

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/xxx`）
3. 提交变更（`git commit -m 'feat: add xxx'`）
4. 推送到分支（`git push origin feature/xxx`）
5. 创建 Pull Request

---

## 👤 作者

- GitHub: [@MrYangStudent](https://github.com/MrYangStudent)
- Gitee: [@mryangsir](https://gitee.com/mryangsir)

---

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源 — Copyright (c) 2026 MrYang.

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star！**

</div>
