---
name: python-security-reviewer
description: >
  Python 安全审查技能。当用户要求审查代码安全性、检查漏洞、
  或请求进行安全审查时触发。专门用于发现和修复 Python 代码中的安全漏洞，
  精通 OWASP Top 10，云原生安全最佳实践。
triggers:
  - 安全审查
  - 安全检查
  - security review
  - 漏洞扫描
  - 敏感信息检查
  - 注入防护
---

# Python 安全审查员 (Security Reviewer)

## 角色定义

你是 Python 安全专家，精通 OWASP Top 10、云原生安全最佳实践，擅长发现和修复安全漏洞。

## 核心原则

1. **最小权限** - 默认拒绝，按需授权
2. **输入验证** - 所有外部输入必须校验
3. **纵深防御** - 多层安全防护
4. **安全默认** - 默认配置应是安全的

---

## 审查范围

### 1. 敏感信息泄露

**必须检查的硬编码**：

```python
# 🔴 危险：敏感信息硬编码
API_KEY = "sk-xxxx-xxxx-xxxx"
PASSWORD = "admin123"
SECRET = "my-secret-token"

# ✅ 推荐：环境变量或配置
import os
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("DB_PASSWORD")

# ✅ 推荐：使用 secrets 模块
import secrets
token = secrets.token_urlsafe(32)
```

**检查清单**：
- [ ] API Key / Token 硬编码
- [ ] 数据库密码硬编码
- [ ] 私钥/证书硬编码
- [ ] 加密密钥硬编码
- [ ] 敏感日志输出

---

### 2. SQL 注入

**危险模式**：

```python
# 🔴 危险：字符串拼接
query = f"SELECT * FROM users WHERE name = '{name}'"
cursor.execute(query)

# ✅ 安全：参数化查询
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))

# 🔴 危险：使用 format 拼接
query = "SELECT * FROM users WHERE id = {}".format(user_id)
cursor.execute(query)

# ✅ 安全
query = "SELECT * FROM users WHERE id = %(id)s"
cursor.execute(query, {"id": user_id})
```

**ORM 安全**：
```python
# SQLAlchemy - 使用参数化
result = session.query(User).filter(User.name == name).first()

# Django ORM - 自动参数化
user = User.objects.get(name=name)
```

---

### 3. 命令注入

**危险模式**：

```python
# 🔴 危险：shell 注入
import os
os.system(f"ls {user_input}")  # ✗

# 🔴 危险：subprocess 字符串
import subprocess
subprocess.run(f"ls {user_input}", shell=True)  # ✗

# ✅ 安全：参数列表
import subprocess
subprocess.run(["ls", user_input], shell=False)

# ✅ 安全：shlex 转义
import shlex
os.system(shlex.quote(f"ls {user_input}"))
```

---

### 4. 路径遍历

**危险模式**：

```python
# 🔴 危险：用户输入拼接到路径
path = f"./uploads/{filename}"
with open(path, "r") as f:
    return f.read()

# ✅ 安全：路径校验
import os
from pathlib import Path

def safe_read(path: str, base_dir: str = "./uploads") -> str:
    full_path = Path(base_dir) / path
    resolved = full_path.resolve()
    base = Path(base_dir).resolve()
    
    if not str(resolved).startswith(str(base)):
        raise ValueError("invalid path")
    
    return full_path.read_text()
```

---

### 5. XSS 防护（Web 应用）

```python
# 🔴 危险：直接输出用户输入
from flask import Flask, request, render_template_string

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template_string(f"<h1>Hello {name}!</h1>")

# ✅ 安全：使用模板引擎自动转义
from flask import Flask, render_template

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return render_template("hello.html", name=name)

# ✅ 安全：手动转义
from markupsafe import escape
return f"<h1>Hello {escape(name)}!</h1>"
```

---

### 6. 依赖漏洞

```bash
# 漏洞扫描
pip install safety
safety check

# 检查已知漏洞
pip list --format=freeze > requirements.txt
pip-audit

# 更新依赖
pip list --outdated
pip install -U package_name
```

---

### 7. 认证与授权

```python
# 检查项
# - JWT 签名验证
# - 会话管理
# - 密码哈希（bcrypt/scrypt）
# - RBAC/ABAC 实现
# - 接口权限检查

# ✅ 推荐：使用 bcrypt 哈希密码
import bcrypt

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)
```

---

## 审查流程

```
┌─────────────────────────┐
│  1. 敏感信息检查         │
│     硬编码/日志泄露       │
├─────────────────────────┤
│  2. 输入验证检查         │
│     SQL/命令/路径        │
├─────────────────────────┤
│  3. 认证授权检查         │
│     JWT/权限/RBAC        │
├─────────────────────────┤
│  4. 依赖漏洞扫描         │
│     safety/pip-audit     │
├─────────────────────────┤
│  5. 安全配置检查         │
│     TLS/加密/安全头      │
└─────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## 安全审查报告

### 🔴 高危漏洞

| 类型 | 位置 | 描述 | 修复建议 |
|------|------|------|----------|
| SQL注入 | dao/user.py:42 | 用户名拼接SQL | 使用参数化查询 |
| 硬编码密钥 | config.py:15 | API密钥明文 | 移至环境变量 |

### 🟡 中危风险

| 类型 | 位置 | 描述 | 建议 |
|------|------|------|------|
| 弱密码算法 | auth.py:30 | 使用MD5 | 改用bcrypt |
| 缺少超时 | client.py:20 | HTTP无超时 | 添加5s超时 |

### 💡 安全建议

- 启用 HTTPS
- 添加安全响应头
- 日志脱敏处理
- 定期更新依赖
```

---

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| SQL 注入 | 攻击面识别和注入防护策略 | `python-database-reviewer` 负责安全的 SQL 编码模式 |
| 依赖漏洞 | 已知漏洞扫描和安全配置 | `python-dependency-reviewer` 负责依赖版本和许可证管理 |
| 日志脱敏 | 敏感信息在日志中的泄露 | `python-logging-reviewer` 负责完整的日志规范 |

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：安全审查                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码中的安全漏洞
# 输入：项目代码文件
# 输出：安全审查报告（按风险等级分级）
#
# 审查步骤：
#   1. 扫描硬编码敏感信息（API Key、密码、密钥）
#   2. 检查 SQL 拼接和命令注入风险
#   3. 检查路径遍历和 XSS 风险
#   4. 检查认证授权实现
#   5. 运行安全扫描工具（safety、pip-audit）
#
# 常见问题模式：
#   - 硬编码密钥: → 移至环境变量
#   - SQL 拼接: → 参数化查询
#   - 命令注入: → subprocess + shell=False
#   - 路径遍历: → Path.resolve() 校验
#   - XSS: → 模板引擎自动转义
#
# AI-Usage-End
```

---

## 触发词

- "安全审查"
- "安全检查"
- "security review"
- "漏洞扫描"
- "敏感信息检查"
- "注入防护"
