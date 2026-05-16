# Python 工程技能库 (python-skill)

<div align="center">

**一套完整的 Python 工程实践技能集，覆盖从代码开发、测试、质量审查到文档生成的完整开发生命周期。**

[English](./README.md) | [中文](./README_zh.md)

</div>

---

## ✨ 特性

- 🚀 **全链路覆盖**：从需求分析 → 代码实现 → 测试验证 → 质量审查 → 文档沉淀 → 生产部署
- 🤖 **AI 友好**：所有文档包含 AI-Usage 注释块，支持 Cline/Cursor 等 AI 工具学习
- 📦 **15+ 专项技能**：覆盖开发全流程各环节
- 🛡️ **严格规范**：遵循 PEP 8、Google/NumPy docstring 规范
- 🔒 **类型安全**：全面使用 TypeHint + Mypy 静态检查
- 🧩 **模块化设计**：各技能可独立使用，也可组合使用

---

## 📁 项目结构

```
python-skill/
├── README_zh.md                          # 项目说明
│
├── 📂 开发流程技能/
│   ├── python-project-rules/             # 项目治理规则
│   ├── python-full-dev-workflow/         # 完整开发工作流
│   └── python-feature-development-workflow/ # 新功能开发工作流
│
├── 📂 测试技能/
│   └── python-test-generator/             # pytest 测试生成
│
├── 📂 代码审查技能/
│   ├── python-error-handling-reviewer/  # 错误处理审查
│   ├── python-concurrency-reviewer/      # 并发安全审查
│   ├── python-security-reviewer/         # 安全审查
│   ├── python-database-reviewer/         # 数据库审查
│   ├── python-dependency-reviewer/       # 依赖管理审查
│   ├── python-performance-reviewer/      # 性能审查
│   ├── python-logging-reviewer/          # 日志规范审查
│   ├── python-typing-reviewer/          # 类型注解审查
│   └── python-api-design-reviewer/      # API 设计审查
│
└── 📂 文档生成技能/
    ├── python-doc-generator/              # 代码文档生成
    └── python-api-doc-generator/         # API 文档生成
```

---

## 🎯 技能总览

### 开发流程

| 技能 | 描述 |
|------|------|
| [python-project-rules](./python-project-rules/) | 项目治理规则，进度同步、README 联动 |
| [python-full-dev-workflow](./python-full-dev-workflow/) | 完整开发工作流，全链路整合 |
| [python-feature-development-workflow](./python-feature-development-workflow/) | 新功能开发，需求拆解、TDD/BDD |

### 测试生成

| 技能 | 描述 |
|------|------|
| [python-test-generator](./python-test-generator/) | pytest 单元测试、Mock 编写、覆盖率优化 |

### 代码审查

| 技能 | 描述 |
|------|------|
| [python-error-handling-reviewer](./python-error-handling-reviewer/) | 异常包装、参数校验审计 |
| [python-concurrency-reviewer](./python-concurrency-reviewer/) | 线程安全、GIL 理解、异步审查 |
| [python-security-reviewer](./python-security-reviewer/) | 敏感信息、注入攻击、依赖漏洞 |
| [python-database-reviewer](./python-database-reviewer/) | 连接池、事务、N+1 检测 |
| [python-dependency-reviewer](./python-dependency-reviewer/) | 第三方依赖必要性、安全性 |
| [python-performance-reviewer](./python-performance-reviewer/) | 资源关闭、内存泄漏、async 优化 |
| [python-logging-reviewer](./python-logging-reviewer/) | 日志级别、脱敏处理、结构化日志 |
| [python-typing-reviewer](./python-typing-reviewer/) | TypeHint 完整性、Protocol 使用 |
| [python-api-design-reviewer](./python-api-design-reviewer/) | RESTful 规范、HTTP 语义 |

### 文档生成

| 技能 | 描述 |
|------|------|
| [python-doc-generator](./python-doc-generator/) | Docstring 注释、README、AI 友好示例 |
| [python-api-doc-generator](./python-api-doc-generator/) | OpenAPI 3.0、Postman 集合、curl 命令 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 推荐使用 Python 3.10+
python --version

# 安装开发依赖
pip install pytest mypy black isort safety
```

### 2. 使用完整工作流

```bash
# 一键执行完整开发流程
"运行开发工作流"
"Python 开发流程"
```

### 3. 按需调用技能

```python
# 代码审查
"安全审查"
"代码审查"
"类型注解审查"

# 测试生成
"生成测试"
"写单元测试"

# 文档生成
"生成 API 文档"
"生成 docstring"
```

---

## 📊 开发工作流

```
┌─────────────────────────────────────────────────────────┐
│                    阶段零：项目治理                       │
│  python-project-rules                                    │
│  - 读取 README.md、project.md                            │
│  - 进度同步、架构联动、提交检查                            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段一：准备与文档                     │
│  python-feature-development-workflow → 需求澄清、任务拆解  │
│  python-doc-generator         → 项目结构、模块文档        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段二：代码实现                       │
│  - Docstring 注释 + TypeHint 类型注解                    │
│  - 异常处理 + 日志记录                                   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段三：测试生成                       │
│  python-test-generator                                   │
│  - 正常路径 + 边界情况 + 错误路径 + 异步测试              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段四：质量审查                       │
│  error-handling / concurrency / security / performance   │
│  database / logging / typing / api-design                │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段五：文档生成                       │
│  python-api-doc-generator                               │
│  - OpenAPI 3.0 + Postman + curl 示例                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    阶段六：验证与部署                     │
│  pytest + mypy + uvicorn + API 端点测试                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 代码规范

```python
# 1. 格式化 (PEP 8)
black --check .

# 2. 导入排序
isort --check .

# 3. 静态类型检查
mypy .

# 4. 测试运行
pytest -v --cov=. --cov-report=term-missing

# 5. 安全扫描
safety check
```

---

## 📖 适用场景

- 🏗️ 新项目初始化与架构设计
- ⚙️ 复杂业务逻辑开发
- 🔍 代码质量审计与重构
- 📚 API 文档自动化生成
- 👥 团队编码规范统一
- 🌐 Python Web 应用开发（FastAPI/Django/Flask）
- 📊 数据处理和科学计算项目

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'feat: add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 📄 License

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**如果对你有帮助，请给个 ⭐ Star！**

</div>
