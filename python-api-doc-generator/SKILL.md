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

Generate comprehensive API documentation for Python Web projects including OpenAPI 3.0 specs, Postman collections, and curl command examples.

## Workflow

### Step 1: Discover API Endpoints

Scan the Python project to identify all HTTP endpoints:

```bash
# Find all FastAPI route decorators
rg -t py "@app\.(get|post|put|delete|patch)\(" --no-heading

# Find Flask route decorators
rg -t py "@app\.route\(" --no-heading

# Find class-based views
rg -t py "class.*View" --type py --files-with-matches
```

### Step 2: Analyze Handler Signatures

Extract endpoint metadata from handler functions:

1. **HTTP Method**: Look for `@app.get()`, `@app.post()`, etc.
2. **Path Pattern**: Parse route decorators
3. **Parameters**: 
   - Path params: `{item_id}` in routes
   - Query params: `Query(...)`, `Request` objects
   - Header params: `Header(...)`
4. **Request Body**: Parse Pydantic models or request data
5. **Response**: Identify response models and status codes

### Step 3: Generate OpenAPI 3.0 Spec

Use the provided template or generate programmatically:

```yaml
openapi: 3.0.3
info:
  title: {ProjectName} API
  version: 1.0.0
  description: Auto-generated API documentation
paths:
  /users/{user_id}:
    get:
      summary: Get user by ID
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: Not found
```

## Framework Examples

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
    user_id: str = Path(..., description="User ID")
) -> User:
    """Get user by ID."""
    ...

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate) -> User:
    """Create a new user."""
    ...
```

### Flask

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID."""
    return jsonify({"id": user_id, "name": "..."})

@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    data = request.get_json()
    return jsonify({"id": "...", **data}), 201
```

## Output Formats

### OpenAPI 3.0
- Format: YAML or JSON
- File: `openapi.yaml` or `openapi.json`
- Standards: OpenAPI 3.0.3 specification

### Postman Collection v2.1
- Format: JSON
- File: `postman_collection.json`
- Import: Postman app → Import → Select file

### curl Commands
- Format: Shell script or Markdown
- File: `curl_commands.sh` or `api_reference.md`
- Usage: Copy-paste or shell execution

## Common Python Web Frameworks

| Framework | Auto-doc | Best for |
|-----------|----------|----------|
| FastAPI | Swagger UI, ReDoc | Modern APIs, type safety |
| Flask | flask-swagger | Lightweight APIs |
| Django REST | DRF Spectacular | Django projects |
| Starlette | Built-in | ASGI apps |

## Example Usage

```
# Generate all documentation for current project
Analyze Python project → Generate OpenAPI → Generate Postman → Generate curl

# Generate specific format only
Generate OpenAPI spec only
Generate Postman collection only
Generate curl commands only
```

## Notes

- Handle both synchronous and asynchronous handlers
- Support middleware chain documentation
- Include authentication/authorization context
- Document error response schemas
