---
name: python-minimal-code
description: >
  Python 语言最小化代码技能。当用户要求简化代码、减少过度工程、检查 YAGNI 原则、
  或请求最简实现时触发。专门用于识别和消除过度设计，遵循"最好的代码是不会写的代码"哲学。
  集成 7 级阶梯原则：标准库优先、一行代码优先、最小可行实现。
triggers:
  - 简化代码
  - 减少过度工程
  - YAGNI
  - 最简实现
  - 懒惰开发
  - 代码精简
  - 最小化
  - 删除冗余
  - 标准库优先
  - 过度设计
  - 代码审查
  - minimal code
---

# Python 最小化代码技能 (Python Minimal Code)

## 技能定位

Python 代码精简专家，遵循"最好的代码是不会写的代码"哲学。你有资深开发者见过每一个过度设计的代码库，也被凌晨三点的电话叫醒过。

## 核心原则

### 7 级阶梯原则

在写任何代码之前，停在第一个能解决问题的阶梯上：

```
1. 需要存在吗？     → 否 → 跳过 (YAGNI)
2. 已存在吗？       → 是 → 复用
3. 标准库能做吗？   → 是 → 用标准库
4. 原生特性覆盖吗？ → 是 → 用原生
5. 已装依赖解决？   → 是 → 用依赖
6. 一行代码？       → 是 → 一行
7. 然后 → 最小可行实现
```

### 强度级别

| 级别 | 行为 | 使用场景 |
|------|------|----------|
| **lite** | 提示更简方案，用户选择 | 学习阶段、首次审查 |
| **full** | 严格执行阶梯原则 | 日常开发（推荐） |
| **ultra** | 激进删除，最大化简化 | 重构清理、技术债偿还 |

## 审查检查项

### 1. YAGNI 功能检查

```python
# 🔴 过度设计：推测性功能
class UserPermission:
    def __init__(self):
        self.can_read = False
        self.can_write = False
        self.can_delete = False
        self.can_admin = False

    def initialize(self):
        # 初始化各种权限 - 但现在只需要 Read
        ...

# ✅ Python Minimal Code：只实现需要的
class UserReader:
    def can_read(self) -> bool:
        return True
```

**检查清单**：
- [ ] 是否有"可能以后会用"的功能？
- [ ] 是否有未使用的配置字段？
- [ ] 是否有推测性抽象？

### 2. 标准库优先检查

```python
# 🔴 引入第三方库
import uuid
id = uuid.uuid4().hex

# ✅ 标准库（如只需随机 ID）
import secrets
id = secrets.token_hex(16)

# 🔴 手写 JSON 解析
def parse_json(data: str) -> dict:
    # 100 行手写解析
    ...

# ✅ 标准库
import json
result = json.loads(data)

# 🔴 引入第三方日期库做简单格式化
from dateutil import parser
parsed = parser.parse(date_str)

# ✅ 标准库
from datetime import datetime
parsed = datetime.fromisoformat(date_str)
```

**标准库替代优先级**：
1. `json` - JSON 处理
2. `csv` - CSV 解析
3. `urllib.request` / `httpx` - HTTP 客户端（项目已装的依赖优先）
4. `hashlib` / `hmac` - 加密和签名
5. `secrets` - 安全随机数
6. `collections` - 高级数据结构
7. `logging` - 日志
8. `pathlib` - 路径操作
9. `dataclasses` - 数据类
10. `re` - 正则表达式

### 3. 过度抽象检查

```python
# 🔴 抽象基类只有一个实现
from abc import ABC, abstractmethod

class CSVParser(ABC):
    @abstractmethod
    def parse(self, data: str) -> list[dict]:
        ...

class StandardCSVParser(CSVParser):
    def parse(self, data: str) -> list[dict]:
        ...

# ✅ 直接具体类
class CSVParser:
    def parse(self, data: str) -> list[dict]:
        ...

# 🔴 空壳函数
def process_user(user_id: str) -> dict:
    return process_user_internal(user_id)

# ✅ 直接调用
return process_user_internal(user_id)

# 🔴 过度使用装饰器做简单事情
class UserService:
    @inject
    @cache
    @validate
    @log
    @retry
    def get_user(self, user_id: str) -> dict:
        ...

# ✅ 直接实现核心逻辑
class UserService:
    def get_user(self, user_id: str) -> dict:
        ...
```

**检查清单**：
- [ ] 是否有单一实现的抽象基类？
- [ ] 是否有空壳函数？
- [ ] 是否有过度分层？
- [ ] 是否有装饰器堆叠超过 3 层？

### 4. Pythonic 简洁性检查

```python
# 🔴 手写循环做简单操作
result = []
for item in items:
    if item.active:
        result.append(item.name)

# ✅ 列表推导式（一行）
result = [item.name for item in items if item.active]

# 🔴 手写 dict 合并
merged = {}
for k, v in dict1.items():
    merged[k] = v
for k, v in dict2.items():
    merged[k] = v

# ✅ 字典合并运算符（Python 3.9+）
merged = dict1 | dict2

# 🔴 手写枚举索引
for i in range(len(items)):
    print(i, items[i])

# ✅ enumerate
for i, item in enumerate(items):
    print(i, item)

# 🔴 手写字典默认值
if key not in result:
    result[key] = []
result[key].append(value)

# ✅ defaultdict
from collections import defaultdict
result = defaultdict(list)
result[key].append(value)
```

### 5. 代码量标准

| 项目 | 限制 | 说明 |
|------|------|------|
| 单文件行数 | ≤ 300 | 超过则拆分模块 |
| 单函数行数 | ≤ 50 | 超过则提取子函数 |
| 函数参数数 | ≤ 5 | 超过则使用 **kwargs 或配置对象 |
| 类属性数 | ≤ 10 | 超过则考虑拆分或使用 dataclass |
| 继承层级 | ≤ 2 | 超过则扁平化 |

## 封装决策树

在封装任何工具函数之前，严格执行以下判断：

```
发现重复代码
├── 出现 >= 2 次？
│   ├── 否 → 不封装，保持内联（YAGNI）
│   └── 是 → 逻辑是否稳定？
│       ├── 否 → 等等看，下次重复时再封装
│       └── 是 → 是否可用标准库替代？
│           ├── 是 → 用标准库
│           └── 否 → 封装为独立函数
└── 涉及外部资源（HTTP、DB）？
    └── 是 → 封装为类，便于 Mock 测试
```

### 封装门槛

| 重复次数 | 建议 | 说明 |
|----------|------|------|
| 1 次 | ❌ 不封装 | 第一次做决定是好抽象 |
| 2 次 | ⚠️ 谨慎 | 可能是巧合，等等看第 3 次 |
| 3 次+ | ✅ 封装 | 模式已确立，值得抽象 |

## 审查流程

### 轻量审查（PR 审查）

```
1. 浏览改动文件
2. 标记红旗信号
3. 输出一行发现：位置 + 标签 + 建议
4. 估计净减少行数
```

### 完整审查（重构前）

```
1. 检查依赖列表（pip list / requirements.txt）
2. 统计代码量（LOC、函数数、类数）
3. 逐项检查 5 个维度
4. 生成详细报告
5. 制定重构计划（删除优先于修改）
```

## 审查报告模板

```markdown
## Python Minimal Code 审查报告

**项目**: [项目名称]
**日期**: [审查日期]
**强度**: [lite/full/ultra]

### 摘要

| 维度 | 发现问题 | 预计净减少 |
|------|----------|------------|
| YAGNI 功能 | X | -Y 行 |
| 标准库替代 | X | -Y 行 |
| 过度抽象 | X | -Y 行 |
| Pythonic 简洁性 | X | -Y 行 |
| 代码量 | X | -Y 行 |
| **合计** | **X** | **-Y 行** |

### 详细发现

#### 🔴 高优先级（立即删除）

| 位置 | 标签 | 问题 | 建议 | 净减少 |
|------|------|------|------|--------|
| `foo.py:42` | yagni | 推测性功能 | 删除 | -150 行 |
| `bar.py:10` | stdlib | 手写 JSON 解析 | 用 `json.loads` | -30 行 |

#### 🟡 中优先级（下次重构）

| 位置 | 标签 | 问题 | 建议 | 净减少 |
|------|------|------|------|--------|
| `baz.py:55` | pythonic | 手写循环+append | 列表推导式 | -10 行 |

#### 💡 低优先级（可选优化）

| 位置 | 标签 | 问题 | 建议 | 净减少 |
|------|------|------|------|--------|
| `qux.py:20` | yagni | 单一实现 ABC | 直接类 | -5 行 |

### 结论

**净减少**: -XX 行（预计 -X% 代码量）

**下一步**:
1. [ ] 删除高优先级项目
2. [ ] 评估中优先级项目
3. [ ] 验证测试通过
4. [ ] 重新运行审查确认
```

## 典型场景速查

### 场景 1: CSV 解析
```python
# 🔴 引入第三方库 + 封装类
import pandas as pd
class CSVParser:
    ...

# ✅ 标准库
import csv
with open("data.csv") as f:
    records = list(csv.DictReader(f))
```
**减少**: 150 行 → **3 行** (-98%)

### 场景 2: 配置管理
```python
# 🔴 引入 dynaconf + 多层配置源
from dynaconf import Dynaconf
settings = Dynaconf(...)

# ✅ 环境变量 + dataclass
import os
from dataclasses import dataclass

@dataclass
class Config:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
```
**减少**: 400 行 → **10 行** (-98%)

### 场景 3: 数据模型
```python
# 🔴 手写 __init__/__repr__/__eq__
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    def __eq__(self, other):
        ...

# ✅ dataclass
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```
**减少**: 30 行 → **5 行** (-83%)

### 场景 4: 日志系统
```python
# 🔴 引入 loguru + 自定义格式 + Handler
from loguru import logger
logger.add(...)

# ✅ 标准库 logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```
**减少**: 50 行 → **3 行** (-94%)

## 删除优先清单

1. ❌ 推测性功能（"可能以后会用"）
2. ❌ 未使用的配置字段
3. ❌ 单一实现的抽象基类
4. ❌ 空壳函数（只做转发）
5. ❌ 冗余的中间层（Request → Controller → Service → Repository）
6. ❌ 手写的标准库功能
7. ❌ 过早封装（重复 <3 次）
8. ❌ 过度装饰器堆叠（>3 层）

## 保留清单（不可删除）

1. ✅ 输入验证（信任边界）
2. ✅ 错误处理（防止数据丢失）
3. ✅ 安全机制（认证、授权、加密）
4. ✅ 用户明确要求的功能
5. ✅ 已有测试覆盖的核心逻辑
6. ✅ 性能优化的关键路径

## 输出规范

### 代码优先

```python
# 直接给出简化后的代码
import csv

def parse_csv(filepath: str) -> list[dict]:
    with open(filepath) as f:
        return list(csv.DictReader(f))
```

### 要说明（最多三行）

```
→ skipped: 自定义 CSV 解析器，csv.DictReader 一行搞定
→ add when: 需要自定义分隔符或编码时
→ net: -25 lines
```

## 最佳实践

### 1. 标准库优先

```python
# ✅ 优先使用标准库
import json           # JSON 处理
import csv            # CSV 解析
import hashlib        # 哈希
import secrets        # 安全随机
import logging        # 日志
import pathlib        # 路径操作
import dataclasses    # 数据类
import re             # 正则
import collections    # 高级容器
import contextlib     # 上下文管理
```

### 2. 延迟抽象

```python
# ❌ 过早抽象
from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, data: str) -> dict:
        ...

# ✅ 重复 3 次后再抽象
class CSVParser:
    def parse(self, data: str) -> dict:
        # 实现
```

### 3. 一行代码优先

```python
# ❌ 5 行循环
result = []
for item in items:
    if item.active:
        result.append(item.name)

# ✅ 一行推导式
result = [item.name for item in items if item.active]

# ❌ 手写 defaultdict 逻辑
groups = {}
for item in items:
    key = item.category
    if key not in groups:
        groups[key] = []
    groups[key].append(item)

# ✅ 一行（collections.defaultdict）
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

### 4. 删除优于添加

```python
# ❌ 添加新功能封装
class Store:
    def get_or_create(self, key: str) -> Item:
        item = self.get(key)
        if item is None:
            item = self.create(key)
        return item

# ✅ 调用方处理
item = store.get(key)
if item is None:
    item = store.create(key)
```

## 与专项审查配合

### 错误处理审查 + Python Minimal Code

```markdown
## 错误处理审查（Python Minimal Code 增强版）

### 正确性问题
- [ ] 异常被吞掉（bare except）
- [ ] 异常类型过于宽泛

### 过度工程问题 (Python Minimal Code)
- [ ] 未请求的自定义异常层级
- [ ] 过多中间层 try/except
- [ ] 冗余的异常转换

### 建议
净减少: -X 行
```

### 依赖审查 + Python Minimal Code

```markdown
## 依赖审查（Python Minimal Code 增强版）

### 必要性
- [ ] 标准库能否替代？
- [ ] 已有依赖能否复用？

### YAGNI 检查
- [ ] 是否"需要"还是"想要"？
- [ ] 传递依赖是否合理？

### 建议
净减少: -X 行
```

## 与其他技能的边界

| 重叠领域 | 本技能关注 | 其他技能关注 |
|---------|----------|-----------|
| 代码重构 | 过度设计和冗余代码的删除 | `python-refactor-reviewer` 关注结构优化和 Pythonic 惯用法 |
| 依赖管理 | 是否真的需要引入第三方库 | `python-dependency-reviewer` 负责版本安全和许可证管理 |
| 性能问题 | 过度封装导致的性能开销 | `python-performance-reviewer` 关注运行时性能瓶颈 |

## 注意事项

### 不适用场景

1. ❌ 安全关键代码（安全机制必须完整）
2. ❌ 合规要求严格的场景（审计跟踪、日志保留）
3. ❌ 团队协作初期（需要先建立模式再简化）
4. ❌ 原型验证阶段（快速实现优先，简化后续再做）

### 必须保留

无论强度多高，以下元素**不得删除**：
- 输入验证（信任边界）
- 错误处理（防止数据丢失）
- 安全机制（认证、授权、加密）
- 用户明确要求的功能

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：最小化代码审查                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：审查 Python 代码中的过度设计和冗余
# 输入：项目代码文件
# 输出：Minimal Code 审查报告（按优先级分级）
#
# 审查步骤：
#   1. 检查 YAGNI 功能（推测性功能、未使用的配置）
#   2. 检查标准库替代（第三方库 vs 标准库）
#   3. 检查过度抽象（单一实现的 ABC、空壳函数）
#   4. 检查 Pythonic 简洁性（推导式、dataclass、标准运算符）
#   5. 检查代码量标准（文件、函数、参数数量）
#
# 常见问题模式：
#   - 推测性功能: → 删除
#   - 第三方库可替代: → 用标准库
#   - 单一实现 ABC: → 直接类
#   - 手写循环+append: → 列表推导式
#   - 手写 __init__/__repr__: → @dataclass
#
# AI-Usage-End
```

## 快速命令

```bash
# 检查大文件
find . -name "*.py" -type f -exec wc -l {} \; | sort -rn | head -10

# 检查依赖数
pip list | wc -l

# 检查类继承深度
grep -rn "class.*\(.*\):" . --include="*.py" | head -20

# 检查 ABC 数量
grep -r "from abc import" . --include="*.py" | wc -l

# 检查长函数
awk '/^def /{start=NR} /^$/{if(NR-start>50) print FILENAME":"start}' *.py
```

---

**核心理念**: 最好的代码是不会写的代码。
