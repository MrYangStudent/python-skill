# Python Engineering Skills (python-skill)

<div align="center">

**A comprehensive Python engineering skill library covering the full development lifecycle: code development, testing, quality review, and documentation generation.**

[English](./README.md) | [中文](./README_zh.md)

</div>

---

## ✨ Features

- 🚀 **Full Lifecycle Coverage**: From requirements analysis → code implementation → testing → quality review → documentation → deployment
- 🤖 **AI-Friendly**: All documents include AI-Usage comment blocks for Cline/Cursor learning
- 📦 **15+ Specialized Skills**: Covering all aspects of development
- 🛡️ **Strict Standards**: PEP 8, Google/NumPy docstring conventions
- 🔒 **Type Safety**: Full TypeHint + Mypy static checking
- 🧩 **Modular Design**: Skills can be used independently or combined

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
│   └── feature-development-workflow/        # Feature development workflow
│
├── 📂 Testing/
│   └── python-test-generator/               # pytest test generation
│
├── 📂 Code Review/
│   ├── error-handling-reviewer/          # Error handling review
│   ├── python-concurrency-reviewer/        # Concurrency safety review
│   ├── security-reviewer/                 # Security audit
│   ├── database-reviewer/                 # Database review
│   ├── dependency-reviewer/              # Dependency management review
│   ├── performance-reviewer/              # Performance review
│   ├── logging-reviewer/                 # Logging standards review
│   ├── python-typing-reviewer/           # Type annotation review
│   └── api-design-reviewer/             # API design review
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
| [feature-development-workflow](./feature-development-workflow/) | Feature dev with TDD/BDD, requirements breakdown |

### Testing

| Skill | Description |
|-------|-------------|
| [python-test-generator](./python-test-generator/) | pytest unit tests, Mock, coverage optimization |

### Code Review

| Skill | Description |
|-------|-------------|
| [error-handling-reviewer](./error-handling-reviewer/) | Exception wrapping, parameter validation |
| [python-concurrency-reviewer](./python-concurrency-reviewer/) | Thread safety, GIL understanding, async review |
| [security-reviewer](./security-reviewer/) | Sensitive data, injection attacks, dependency vulnerabilities |
| [database-reviewer](./database-reviewer/) | Connection pool, transactions, N+1 detection |
| [dependency-reviewer](./dependency-reviewer/) | Third-party dependency necessity, security |
| [performance-reviewer](./performance-reviewer/) | Resource cleanup, memory leaks, async optimization |
| [logging-reviewer](./logging-reviewer/) | Log levels, data masking, structured logging |
| [python-typing-reviewer](./python-typing-reviewer/) | TypeHint completeness, Protocol usage |
| [api-design-reviewer](./api-design-reviewer/) | RESTful standards, HTTP semantics |

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

# Test generation
"Generate tests"
"Write unit tests"

# Documentation
"Generate API documentation"
"Generate docstring"
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
│  feature-development-workflow → Requirements clarification │
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
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 5: Documentation               │
│  python-api-doc-generator                               │
│  - OpenAPI 3.0 + Postman + curl examples               │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Phase 6: Validation & Deploy         │
│  pytest + mypy + uvicorn + API endpoint tests          │
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
