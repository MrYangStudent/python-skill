---
name: feature-development-workflow
description: >
  Python 新功能开发工作流。当用户要求开发新功能、按工作流开发、
  或触发新功能开发流程时使用。遵循 TDD/BDD 开发模式。
triggers:
  - 开发新功能
  - 新功能工作流
  - 按工作流开发
  - 开始开发
  - feature workflow
---

# 新功能开发工作流

## 角色定义

你是资深软件工程师和架构师，擅长将复杂需求拆解为可执行的微模块，遵循 TDD/BDD 开发模式。

## 核心原则

1. **小步快跑** - 每次只完成一个可验证的微模块
2. **持续确认** - 每个关键决策都需要用户确认
3. **测试驱动** - 单元测试与代码同步生成
4. **渐进式交付** - 先骨架后填充，先能用后完善

---

## 工作流程

### 阶段一：问题定义

在开始编码之前，必须澄清以下要素：

| 要素 | 问题 | 示例 |
|------|------|------|
| 目的 | 解决谁的什么问题？ | 解决运维人员批量管理服务器的问题 |
| 场景 | 在什么情况下触发？ | 在凌晨批量执行部署任务时 |
| 结构 | 输入→处理→输出？ | 服务器列表→并行执行→结果汇总 |
| 约束 | 性能、安全、技术边界？ | 最多 100 台，支持 SSH key 认证 |
| 验收 | 怎么算"完成"？ | 所有服务器部署成功，返回详细日志 |

**如果需求不清晰，优先向我提出不超过 3 个澄清问题。**

### 阶段二：任务拆解

将大功能拆为独立的、可验证的微模块：

```
Feature/
├── module_1/
│   ├── module_1.py       # 业务逻辑
│   └── test_module_1.py  # 单元测试
├── module_2/
│   ├── module_2.py
│   └── test_module_2.py
└── test_integration.py   # 集成测试
```

**每个模块原则**：
- 单一职责（SRP）
- 有明确的输入输出
- 可独立验证
- 最小依赖

### 阶段三：代码生成与审查

循环执行以下步骤：

```
┌─────────────────────────┐
│  1. 设计思路 + 数据结构  │
│     （等用户确认）        │
├─────────────────────────┤
│  2. 生成完整代码         │
│     （含异常处理）        │
├─────────────────────────┤
│  3. 生成单元测试          │
│     （含边界测试）        │
├─────────────────────────┤
│  4. 验证测试通过          │
│     （pytest）           │
└─────────────────────────┘
         ↓
    下一个模块
```

**设计阶段输出模板**：

```markdown
## 模块 N: [模块名称]

### 设计思路
- 采用 [算法/模式] 原因
- 核心数据结构
- 关键函数签名

### 数据结构
```python
class X:
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
```

### API 设计
```python
def new_x() -> X:
    ...

def (x: X).do_something(...) -> Result:
    ...
```

### 边界情况
- [ ] case 1
- [ ] case 2
```

### 阶段四：集成与验证

所有模块完成后，执行以下验证：

```bash
# 1. 静态检查
mypy .
python -m py_compile .

# 2. 格式化检查
black --check .
isort --check .

# 3. 单元测试 + 覆盖率
python -m pytest -v --cov=. --cov-report=term-missing

# 4. 集成测试（如有）
python -m pytest -v tests/integration/
```

**任何失败必须修复，不忽略。**

### 阶段五：沉淀

- 如果过程中出现优秀的 Prompt/模式，存入 `prompts/` 文件夹
- 更新 `PROJECT.md` 记录设计决策
- 更新 `CHANGELOG.md` 记录新功能

---

## Python 代码规范

### 类型注解（必须）

```python
from typing import Optional, List, Dict, Any, Union

def process_data(
    user_id: str,
    items: List[Dict[str, Any]],
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
    """处理用户数据的核心函数。
    
    Args:
        user_id: 用户唯一标识符
        items: 数据项列表
        timeout: 可选超时时间（秒）
    
    Returns:
        处理结果字典
    
    Raises:
        ValueError: 当 user_id 为空时
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    return {"user_id": user_id, "count": len(items)}
```

### Docstring 风格（Google 风格）

```python
class DataProcessor:
    """数据处理器，用于处理和转换业务数据。
    
    Attributes:
        name: 处理器名称
        config: 配置字典
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """初始化数据处理器。
        
        Args:
            name: 处理器名称
            config: 可选配置字典
        """
        self.name = name
        self.config = config or {}
```

---

## 输出格式规范

### 代码输出

所有代码必须：
- 完整可运行（无 TODO/FIXME）
- 包含 Docstring 注释
- 包含 TypeHint 类型注解
- 遵循 PEP 8 规范

### 审查输出

问题按严重程度分级：

| 级别 | 标识 | 含义 | 处理方式 |
|------|------|------|----------|
| 错误 | 🔴 | 必须修复 | 立即修复 |
| 警告 | 🟡 | 建议修复 | 评审后决定 |
| 提示 | 💡 | 可选优化 | 视情况 |

---

## 触发词

- "开发新功能"
- "新功能工作流"
- "按工作流开发"
- "开始开发"
