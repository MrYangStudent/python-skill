---
name: database-reviewer
description: >
  Python 数据库审查技能。当用户要求审查数据库代码、检查 SQL 性能、
  或请求进行数据库审查时触发。专门用于审查数据库相关代码的正确性和性能。
triggers:
  - 数据库审查
  - SQL 检查
  - database review
  - 连接池配置
  - N+1 查询
  - 事务检查
---

# Python 数据库审查员 (Database Reviewer)

## 角色定义

你是 Python 数据库专家，精通 SQL 优化、连接池管理、事务处理，擅长审查数据库相关代码的正确性和性能。

## 核心原则

1. **连接安全** - 正确管理连接生命周期
2. **事务正确** - 确保 ACID 特性
3. **查询高效** - 避免 N+1 和全表扫描
4. **资源清理** - 及时释放数据库资源

---

## 审查范围

### 1. 连接池配置

**检查要点**：

```python
# 🔴 危险：未配置连接池
import psycopg2
conn = psycopg2.connect(database="test")

# ✅ 安全：配置连接池
from psycopg2 import pool
conn_pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    database="test",
    user="user",
    password="pass"
)

# ✅ 使用 SQLAlchemy 连接池
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/test",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 连接前测试
    pool_recycle=3600,    # 一小时后回收
)
```

**配置检查清单**：
- [ ] 连接池大小设置合理
- [ ] 连接超时设置
- [ ] 连接回收策略
- [ ] pool_pre_ping 启用

---

### 2. 事务处理

**正确模式**：

```python
# 标准事务
def transfer_money(from_id: str, to_id: str, amount: float) -> None:
    with conn.cursor() as cur:
        try:
            cur.execute("BEGIN")
            
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE id = %s",
                (amount, from_id)
            )
            
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id)
            )
            
            cur.execute("COMMIT")
        except Exception:
            cur.execute("ROLLBACK")
            raise

# ✅ 使用 context manager
with conn.transaction() as tx:
    tx.execute("UPDATE ...")
    tx.execute("UPDATE ...")
# 自动提交或回滚
```

**危险模式**：

```python
# 🔴 危险：事务中无错误处理
cur.execute("BEGIN")
cur.execute("UPDATE ...")
cur.execute("COMMIT")  # 错误被忽略

# 🔴 危险：连接未关闭
def query():
    conn = get_connection()
    result = conn.execute("SELECT ...")
    # conn 未关闭
    return result

# ✅ 正确：使用 context manager
def query():
    with get_connection() as conn:
        return conn.execute("SELECT ...")
```

---

### 3. 查询效率

**N+1 查询检测**：

```python
# 🔴 危险：N+1 查询
def get_all_users_with_posts():
    users = db.execute("SELECT id, name FROM users").fetchall()
    result = []
    for user in users:
        # 每个用户触发一次额外查询
        posts = db.execute(
            "SELECT * FROM posts WHERE user_id = %s",
            (user["id"],)
        ).fetchall()
        result.append({**user, "posts": posts})
    return result

# ✅ 推荐：JOIN 查询
def get_all_users_with_posts():
    query = """
        SELECT u.id, u.name, p.id as post_id, p.title 
        FROM users u 
        LEFT JOIN posts p ON u.id = p.user_id 
        ORDER BY u.id
    """
    return db.execute(query).fetchall()

# ✅ 推荐：批量查询
def get_all_users_with_posts():
    users = db.execute("SELECT * FROM users").fetchall()
    user_ids = [u["id"] for u in users]
    
    # 一次查询获取所有相关 posts
    posts = db.execute(
        "SELECT * FROM posts WHERE user_id IN %s",
        (tuple(user_ids),)
    ).fetchall()
    
    # 在内存中关联
    posts_by_user = {}
    for post in posts:
        posts_by_user.setdefault(post["user_id"], []).append(post)
    
    return [
        {**user, "posts": posts_by_user.get(user["id"], [])}
        for user in users
    ]
```

---

### 4. 资源关闭

**必须关闭的类型**：

```python
# Cursor 必须关闭
with conn.cursor() as cur:
    cur.execute("SELECT ...")
    results = cur.fetchall()
# 自动关闭

# Rows 必须关闭
rows = cur.execute("SELECT ...")
try:
    for row in rows:
        process(row)
finally:
    rows.close()

# ✅ 推荐：使用 context manager
with conn.cursor() as cur:
    cur.execute("SELECT ...")
    for row in cur:
        process(row)
```

---

### 5. SQL 注入防护

```python
# 🔴 危险：字符串拼接
query = "SELECT * FROM users WHERE " + column + " = '" + value + "'"

# ✅ 安全：白名单 + 参数化
ALLOWED_COLUMNS = {"name", "email", "created_at"}

if column not in ALLOWED_COLUMNS:
    raise ValueError("invalid column")

query = "SELECT * FROM users WHERE " + column + " = %s"
cursor.execute(query, (value,))
```

---

### 6. 索引使用

**检查慢查询**：

```sql
-- 检查查询计划
EXPLAIN SELECT * FROM users WHERE email = 'xxx';

-- 必要索引场景
-- 1. WHERE 条件列
-- 2. JOIN 连接列
-- 3. ORDER BY 排序列
-- 4. 高区分度列
```

---

## ORM 最佳实践

### SQLAlchemy

```python
from sqlalchemy.orm import Session
from sqlalchemy import select

# ✅ 推荐：使用 Session 作为 context manager
with Session(engine) as session:
    result = session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

# ✅ 推荐：使用查询构建器
users = (
    session.query(User)
    .filter(User.active == True)
    .order_by(User.created_at.desc())
    .limit(100)
    .all()
)

# ✅ 推荐：使用 relationship 避免 N+1
from sqlalchemy.orm import joinedload

users = (
    session.query(User)
    .options(joinedload(User.posts))
    .all()
)
```

---

## 审查流程

```
┌─────────────────────────┐
│  1. 连接池配置检查       │
│     pool_size/maxconn    │
├─────────────────────────┤
│  2. 事务处理检查         │
│     Commit/Rollback      │
├─────────────────────────┤
│  3. 查询效率检查         │
│     N+1/全表扫描         │
├─────────────────────────┤
│  4. 资源关闭检查         │
│     cursor/connection     │
├─────────────────────────┤
│  5. SQL 注入检查         │
│     参数化查询           │
└─────────────────────────┘
```

---

## 输出格式

### 审查报告模板

```markdown
## 数据库审查报告

### 🔴 必须修复

| 位置 | 问题 | 建议 |
|------|------|------|
| dao/user.py:42 | 连接未关闭 | 使用 with 语句 |
| dao/order.py:55 | N+1 查询 | 改用 JOIN |

### 🟡 建议优化

| 位置 | 问题 | 建议 |
|------|------|------|
| db.py:20 | 连接池过小 | maxconn 设为 50 |
| dao/report.py:30 | 缺少索引 | 添加联合索引 |

### 💡 可选改进

| 建议 |
|------|
| 使用批量插入优化 |
| 添加查询超时 |
| 考虑读写分离 |
```

---

## 触发词

- "数据库审查"
- "SQL 检查"
- "database review"
- "连接池配置"
- "N+1 查询"
- "事务检查"
