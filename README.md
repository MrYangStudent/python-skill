# Python Engineering Skills (python-skill)

<div align="center">

**A comprehensive Python engineering skill library covering the full development lifecycle: code development, testing, quality review, and documentation generation.**

[English](./README.md) | [中文](./README_zh.md)

</div>

---

## ✨ Features

- 🚀 **Full Lifecycle Coverage**: From requirements analysis → code implementation → testing → quality review → documentation → deployment
- 🤖 **AI-Friendly**: All documents include AI-Usage comment blocks for Cline/Cursor learning
- 📦 **19+ Specialized Skills**: Covering all aspects of development
- 🛡️ **Strict Standards**: PEP 8, Google/NumPy docstring conventions
- 🔒 **Type Safety**: Full TypeHint + Mypy static checking (Python 3.10+)
- 🧩 **Modular Design**: Skills can be used independently or combined
- 🏗️ **Architecture Level**: Architecture review, refactoring review, configuration review
- 🔄 **CI/CD Ready**: GitHub Actions, Docker, pre-commit, quality gates

---

## 📁 Project Structure

```
python-skill/
├── README.md                               # English documentation
├── README_zh.md                           # 中文文档
│
├── 📂 Development Workflow/
│   ├── python-project-rules/              # Project governance rules
│   ├── python-full-dev-workflow/           # Complete development workflow
│   ├── python-feature-development-workflow/ # Feature development workflow
│   └── python-ci-cd-workflow/              # CI/CD pipeline workflow
│
├── 📂 Testing/
│   └── python-test-generator/               # pytest test generation
│
├── 📂 Code Review/
│   ├── python-error-handling-reviewer/    # Error handling review
│   ├── python-concurrency-reviewer/        # Concurrency safety review
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
└── 📂 Documentation/
    ├── python-doc-generator/               # Code documentation generator
    └── python-api-doc-generator/          # API documentation generator
```

---

## 🎯 Skills Overview

### Development Workflow

| Skill | Description |
|-------|-------------|
| [python-project-rules](./python-project-rules/) | Project governance, progress sync, README sync |
| [python-full-dev-workflow](./python-full-dev-workflow/) | Full development workflow integration |
| [python-feature-development-workflow](./python-feature-development-workflow/) | Feature dev with TDD/BDD, requirements breakdown |
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

### Documentation

| Skill | Description |
|-------|-------------|
| [python-doc-generator](./python-doc-generator/) | Docstring, README, AI-friendly examples |
| [python-api-doc-generator](./python-api-doc-generator/) | OpenAPI 3.0, Postman collection, curl commands |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Python 3.10+ recommended
python --version

# Install development dependencies
pip install pytest mypy black isort safety
```

### 2. Run Full Workflow

```bash
# Execute complete development workflow
"Run development workflow"
"Python development process"
```

### 3. Use Individual Skills

```bash
# Code review
"Security review"
"Code review"
"Type annotation review"
"Architecture review"
"Refactoring review"
"Config review"

# Test generation
"Generate tests"
"Write unit tests"

# Documentation
"Generate API documentation"
"Generate docstring"

# CI/CD
"Setup CI/CD"
"Configure GitHub Actions"
```

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
│  python-doc-generator         → Project structure docs   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 2: Code Implementation          │
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
│  error / concurrency / security / performance           │
│  database / logging / typing / api-design               │
│  refactor / config / architecture                       │
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

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/xxx`)
3. Commit your changes (`git commit -m 'feat: add xxx'`)
4. Push to the branch (`git push origin feature/xxx`)
5. Open a Pull Request

---

## 📄 License

This project is open source under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**If this project helps you, please give it a ⭐ Star!**

</div>
