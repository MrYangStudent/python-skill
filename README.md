# Python Engineering Skills (python-skill)

<div align="center">

**A comprehensive Python engineering skill library covering the full development lifecycle: code development, testing, quality review, and documentation generation.**

[English](./README.md) | [中文](./README_zh.md)

<a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/github/stars/MrYangStudent/python-skill?style=flat-square" alt="Stars"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/badge/language-Python-blue?style=flat-square" alt="Language"></a>
<a href="https://github.com/MrYangStudent/python-skill"><img src="https://img.shields.io/badge/skills-23+-green?style=flat-square" alt="Skills"></a>

</div>

---

## Table of Contents

- [Features](#-features)
- [Background](#-background)
- [Project Structure](#-project-structure)
- [Skills Overview](#-skills-overview)
  - [Development Workflow](#development-workflow)
  - [Testing](#testing)
  - [Code Review](#code-review)
  - [Code Simplification](#code-simplification)
  - [Documentation](#documentation)
  - [Knowledge Management](#knowledge-management)
- [Quick Start](#-quick-start)
- [Development Workflow](#-development-workflow)
- [Code Standards](#-code-standards)
- [Use Cases](#-use-cases)
- [Contributing](#-contributing)
- [Author](#author)
- [License](#-license)

---

## ✨ Features

- 🚀 **Full Lifecycle Coverage**: From requirements analysis → code implementation → testing → quality review → documentation → deployment
- 🤖 **AI-Friendly**: All documents include AI-Usage comment blocks for Cline/Cursor/CodeBuddy learning
- 📦 **23+ Specialized Skills**: Covering all aspects of development
- 🛡️ **Strict Standards**: PEP 8, Google/NumPy docstring conventions
- 🔒 **Type Safety**: Full TypeHint + Mypy static checking (Python 3.10+)
- 🧩 **Modular Design**: Skills can be used independently or combined
- 🏗️ **Architecture Level**: Architecture review, refactoring review, configuration review
- 🔄 **CI/CD Ready**: GitHub Actions, Docker, pre-commit, quality gates

---

## 📖 Background

When developing Python projects with AI coding assistants (CodeBuddy, Cline, Cursor), we found that:

- AI assistants often lack **domain-specific expertise** — they can write code but miss security vulnerabilities, concurrency bugs, and architecture flaws
- Code quality review requires **repeated manual prompting** — each review type needs different expertise
- Documentation generation is **tedious and inconsistent** — docstrings, API docs, README all need different templates
- **New feature development in existing projects** is risky — modifying old code while adding new features often breaks things

This skill library addresses these problems by packaging Python engineering best practices into **specialized, reusable AI skills**. Each skill follows strict standards (PEP 8, Google docstring, SOLID principles) and can be triggered by simple keywords in your AI assistant.

---

## 📁 Project Structure

```
python-skill/
├── README.md                               # English documentation
├── README_zh.md                           # Chinese documentation
├── LICENSE                                # MIT License
│
├── 📂 Development Workflow/
│   ├── python-project-rules/              # Project governance rules
│   ├── python-full-dev-workflow/           # Complete development workflow
│   ├── python-feature-development-workflow/ # Feature development workflow
│   ├── python-incremental-dev/            # Incremental dev for existing projects
│   └── python-ci-cd-workflow/              # CI/CD pipeline workflow
│
├── 📂 Testing/
│   └── python-test-generator/               # pytest test generation
│
├── 📂 Code Review/
│   ├── python-error-handling-reviewer/    # Error handling review
│   ├── python-concurrency-reviewer/        # Concurrency safety review
│   ├── python-async-lifecycle-reviewer/   # Async lifecycle review
│   ├── python-security-reviewer/           # Security audit
│   ├── python-database-reviewer/           # Database review
│   ├── python-dependency-reviewer/         # Dependency management review
│   ├── python-performance-reviewer/        # Performance review
│   ├── python-logging-reviewer/            # Logging standards review
│   ├── python-typing-reviewer/             # Type annotation review
│   ├── python-api-design-reviewer/         # API design review
│   ├── python-refactor-reviewer/           # Code refactoring review
│   ├── python-config-reviewer/             # Configuration management review
│   └── python-architecture-reviewer/       # Architecture design review
│
├── 📂 Code Simplification/
│   ├── python-minimal-code/               # YAGNI / minimal implementation
│   └── python-utility-functions/          # Type-safe utility function packaging
│
├── 📂 Documentation/
│   ├── python-doc-generator/               # Code documentation generator
│   └── python-api-doc-generator/          # API documentation generator
│
└── 📂 Knowledge Management/
    └── wiki-knowledge-base/               # Local LLM Wiki knowledge base
```

---

## 🎯 Skills Overview

### Development Workflow

| Skill | Description |
|-------|-------------|
| [python-project-rules](./python-project-rules/) | Project governance, progress sync, README sync |
| [python-full-dev-workflow](./python-full-dev-workflow/) | Full development workflow integration (17 skill chain) |
| [python-feature-development-workflow](./python-feature-development-workflow/) | Feature dev with TDD/BDD, requirements breakdown |
| [python-incremental-dev](./python-incremental-dev/) | Incremental dev in existing projects, minimal code change, knowledge-base CLI |
| [python-ci-cd-workflow](./python-ci-cd-workflow/) | GitHub Actions, Docker, quality gates, release automation |

### Testing

| Skill | Description |
|-------|-------------|
| [python-test-generator](./python-test-generator/) | pytest unit tests, Mock, coverage optimization |

### Code Review

| Skill | Description |
|-------|-------------|
| [python-error-handling-reviewer](./python-error-handling-reviewer/) | Exception wrapping, parameter validation |
| [python-concurrency-reviewer](./python-concurrency-reviewer/) | Thread safety, GIL understanding, async review |
| [python-async-lifecycle-reviewer](./python-async-lifecycle-reviewer/) | asyncio task lifecycle, cancellation propagation, timeout control |
| [python-security-reviewer](./python-security-reviewer/) | Sensitive data, injection attacks, dependency vulnerabilities |
| [python-database-reviewer](./python-database-reviewer/) | Connection pool, transactions, N+1 detection |
| [python-dependency-reviewer](./python-dependency-reviewer/) | Third-party dependency necessity, security |
| [python-performance-reviewer](./python-performance-reviewer/) | Resource cleanup, memory leaks, async optimization |
| [python-logging-reviewer](./python-logging-reviewer/) | Log levels, data masking, structured logging |
| [python-typing-reviewer](./python-typing-reviewer/) | TypeHint completeness, Protocol usage, Python 3.10+ syntax |
| [python-api-design-reviewer](./python-api-design-reviewer/) | RESTful standards, HTTP semantics |
| [python-refactor-reviewer](./python-refactor-reviewer/) | DRY, complexity, Pythonic idioms, design patterns |
| [python-config-reviewer](./python-config-reviewer/) | pydantic-settings, .env, pyproject.toml, 12-Factor App |
| [python-architecture-reviewer](./python-architecture-reviewer/) | Layered architecture, dependency direction, SOLID principles |

### Code Simplification

| Skill | Description |
|-------|-------------|
| [python-minimal-code](./python-minimal-code/) | YAGNI principle, 7-level simplification ladder, stdlib-first |
| [python-utility-functions](./python-utility-functions/) | Type-safe utility packaging, HTTP client, crypto, retry, pagination |

### Documentation

| Skill | Description |
|-------|-------------|
| [python-doc-generator](./python-doc-generator/) | Docstring, README, AI-friendly examples |
| [python-api-doc-generator](./python-api-doc-generator/) | OpenAPI 3.0, Postman collection, curl commands |

### Knowledge Management

| Skill | Description |
|-------|-------------|
| [wiki-knowledge-base](./wiki-knowledge-base/) | Local LLM Wiki: ingest sources → structured pages, query with citations |

---

## 🚀 Quick Start

### 1. Install as CodeBuddy Skills

```bash
# Clone the repository
git clone https://github.com/MrYangStudent/python-skill.git

# Copy desired skill directories to your CodeBuddy skills folder
# Linux/macOS:
cp -r python-skill/python-security-reviewer ~/.codebuddy/skills/
# Windows:
xcopy /E python-skill\python-security-reviewer %USERPROFILE%\.codebuddy\skills\

# Or copy all skills at once
cp -r python-skill/python-* ~/.codebuddy/skills/
```

### 2. Environment Requirements

```bash
# Python 3.10+ required
python --version

# Development dependencies (for projects using these skills)
pip install pytest mypy black isort safety
```

### 3. Trigger Skills in Your AI Assistant

These skills are designed for AI coding assistants (CodeBuddy, Cline, Cursor). Simply use the trigger keywords in your conversation:

**Development Workflow:**
- "Run development workflow" → triggers `python-full-dev-workflow`
- "Incremental development" / "开发新模块" → triggers `python-incremental-dev`

**Code Review:**
- "Security review" → triggers `python-security-reviewer`
- "Async review" / "异步生命周期审查" → triggers `python-async-lifecycle-reviewer`
- "Architecture review" → triggers `python-architecture-reviewer`
- "Refactoring review" → triggers `python-refactor-reviewer`

**Code Simplification:**
- "Simplify code" / "YAGNI" → triggers `python-minimal-code`
- "Package utility functions" → triggers `python-utility-functions`

**Testing:**
- "Generate tests" / "Write unit tests" → triggers `python-test-generator`

**Documentation:**
- "Generate API documentation" → triggers `python-api-doc-generator`
- "Generate docstring" → triggers `python-doc-generator`

**Knowledge Management:**
- "存入wiki知识库" → triggers `wiki-knowledge-base` ingest mode
- "检索wiki" → triggers `wiki-knowledge-base` query mode

---

## 📊 Development Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Phase 0: Project Governance           │
│  python-project-rules                                    │
│  - Read README.md, project.md                           │
│  - Progress sync, architecture link, commit check       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 1: Preparation & Docs           │
│  python-feature-development-workflow → Requirements clarification │
│  python-incremental-dev         → Knowledge-base reference │
│  python-doc-generator           → Project structure docs   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 2: Code Implementation          │
│  python-minimal-code → YAGNI / stdlib-first check       │
│  python-utility-functions → Reusable packaging           │
│  - Docstring + TypeHint annotations                     │
│  - Exception handling + Logging                         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 3: Test Generation             │
│  python-test-generator                                   │
│  - Happy path + Edge cases + Error paths + Async       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 4: Quality Review               │
│  error / concurrency / async-lifecycle / security       │
│  performance / database / logging / typing              │
│  api-design / refactor / config / architecture          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 5: Documentation               │
│  python-api-doc-generator                               │
│  - OpenAPI 3.0 + Postman + curl examples               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 6: CI/CD & Deploy              │
│  python-ci-cd-workflow                                   │
│  - Lint + Type check + Test + Build + Deploy           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Code Standards

```bash
# Formatting (PEP 8)
black --check .

# Import sorting
isort --check .

# Static type checking
mypy .

# Test execution
pytest -v --cov=. --cov-report=term-missing

# Security scan
safety check
```

---

## 📖 Use Cases

- 🏗️ New project initialization and architecture design
- ⚙️ Complex business logic development
- 🔍 Code quality audit and refactoring
- 📚 API documentation automation
- 👥 Team coding standards alignment
- 🌐 Python Web development (FastAPI/Django/Flask)
- 📊 Data processing and scientific computing projects
- 🔄 CI/CD pipeline setup and automation
- 🧩 Incremental feature development in existing large projects
- 🗂️ Project knowledge management and retrieval

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/xxx`)
3. Commit your changes (`git commit -m 'feat: add xxx'`)
4. Push to the branch (`git push origin feature/xxx`)
5. Open a Pull Request

---

## 👤 Author

- GitHub: [@MrYangStudent](https://github.com/MrYangStudent)
- Gitee: [@mryangsir](https://gitee.com/mryangsir)

---

## 📄 License

This project is open source under the [MIT License](LICENSE) — Copyright (c) 2026 MrYang.

---

<div align="center">

**If this project helps you, please give it a ⭐ Star!**

</div>
