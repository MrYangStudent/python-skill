---
name: python-api-doc-generator
description: >
  Python API 文档生成技能。当用户要求生成 API 文档、创建 OpenAPI 规范、
  或请求生成 API 参考文档时使用。从 Python Web 框架（如 FastAPI、Flask）自动生成 API 文档。
triggers:
  - 生成 API 文档
  - 生成 OpenAPI
  - OpenAPI 规范
  - API 文档
  - FastAPI 文档
---

# Python API 文档生成器

为 Python Web 项目生成完整的 API 文档，包括 OpenAPI 3.0 规范、Postman 集合和 curl 命令示例。

## 工作流程

### 步骤 1：发现 API 端点

扫描 Python 项目以识别所有 HTTP 端点：

```bash
# 查找所有 FastAPI 路由装饰器
rg -t py "@app\.(get|post|put|delete|patch)\(" --no-heading

# 查找 Flask 路由装饰器
rg -t py "@app\.route\(" --no-heading

# 查找基于类的视图
rg -t py "class.*View" --type py --files-with-matches
```

### 步骤 2：分析处理函数签名

从处理函数中提取端点元数据：

1. **HTTP 方法**：查找 `@app.get()`、`@app.post()` 等
2. **路径模式**：解析路由装饰器
3. **参数**：
   - 路径参数：路由中的 `{item_id}`
   - 查询参数：`Query(...)`、`Request` 对象
   - 请求头参数：`Header(...)`
4. **请求体**：解析 Pydantic 模型或请求数据
5. **响应**：识别响应模型和状态码

### 步骤 3：生成 OpenAPI 3.0 规范

使用提供的模板或以编程方式生成：

```yaml
openapi: 3.0.3
info:
  title: {项目名称} API
  version: 1.0.0
  description: 自动生成的 API 文档
paths:
  /users/{user_id}:
    get:
      summary: 根据 ID 获取用户
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: 未找到
```

## 框架示例

### FastAPI

```python
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: str
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str = Path(..., description="用户 ID")
) -> User:
    """根据 ID 获取用户。"""
    ...

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate) -> User:
    """创建新用户。"""
    ...
```

### Flask

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """根据 ID 获取用户。"""
    return jsonify({"id": user_id, "name": "..."})

@app.route("/users", methods=["POST"])
def create_user():
    """创建新用户。"""
    data = request.get_json()
    return jsonify({"id": "...", **data}), 201
```

## 输出格式

### OpenAPI 3.0
- 格式：YAML 或 JSON
- 文件：`openapi.yaml` 或 `openapi.json`
- 标准：OpenAPI 3.0.3 规范

### Postman 集合 v2.1
- 格式：JSON
- 文件：`postman_collection.json`
- 导入：Postman 应用 → Import → 选择文件

### curl 命令
- 格式：Shell 脚本或 Markdown
- 文件：`curl_commands.sh` 或 `api_reference.md`
- 用法：复制粘贴或 Shell 执行

## 常见 Python Web 框架

| 框架 | 自动文档 | 适用场景 |
|------|---------|---------|
| FastAPI | Swagger UI, ReDoc | 现代 API，类型安全 |
| Flask | flask-swagger | 轻量级 API |
| Django REST | DRF Spectacular | Django 项目 |
| Starlette | 内置 | ASGI 应用 |

## 使用示例

```
# 为当前项目生成所有文档
分析 Python 项目 → 生成 OpenAPI → 生成 Postman → 生成 curl

# 仅生成特定格式
仅生成 OpenAPI 规范
仅生成 Postman 集合
仅生成 curl 命令
```

## 注意事项

- 处理同步和异步处理函数
- 支持中间件链文档
- 包含认证/授权上下文
- 文档化错误响应模型

---

## AI 使用示例

```python
# AI-Usage-Begin
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃  AI 使用示例：API 文档生成                              ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
# 场景：为 Python Web 项目生成 API 文档
# 输入：FastAPI/Flask/Django 项目代码
# 输出：OpenAPI 3.0 规范 + Postman 集合 + curl 命令
#
# 生成步骤：
#   1. 扫描项目发现所有 HTTP 端点
#   2. 分析处理函数签名（参数、请求体、响应模型）
#   3. 生成 OpenAPI 3.0 YAML/JSON 规范
#   4. 生成 Postman Collection v2.1
#   5. 生成 curl 命令示例
#
# 支持框架：
#   - FastAPI：自动从 Pydantic 模型提取 Schema
#   - Flask：从路由装饰器提取端点信息
#   - Django REST：从 Serializer 提取字段定义
#
# AI-Usage-End
```

---

## 触发词

- "生成 API 文档"
- "生成 OpenAPI"
- "OpenAPI 规范"
- "API 文档"
- "FastAPI 文档"
