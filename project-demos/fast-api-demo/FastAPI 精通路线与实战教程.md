# FastAPI 精通路线与实战教程：面向 Go 服务端工程师

## 1. 文档目标

本文面向已有 Go 服务端开发经验的工程师，目标不是简单写一个 `Hello World`，而是帮助你从后端工程视角系统掌握 FastAPI，最终具备以下能力：

- 独立搭建 FastAPI 后端服务。
- 理解 FastAPI、Pydantic、Starlette、Uvicorn 的关系。
- 设计清晰的项目结构。
- 完成参数校验、路由拆分、依赖注入、认证鉴权、数据库访问。
- 编写测试、容器化部署、排查性能和线上问题。
- 将 Go 服务端经验迁移到 Python / FastAPI 技术栈。

---

## 2. FastAPI 是什么

FastAPI 是一个基于 Python 类型注解构建的现代 Web 框架，主要特点是：

- 高性能，底层基于 Starlette 和 ASGI。
- 使用 Pydantic 做数据校验和序列化。
- 自动生成 OpenAPI 文档。
- 天然支持 `async` / `await`。
- 依赖注入系统强大。
- 适合构建 API 服务、后台管理系统、AI 服务接口、微服务网关等。

FastAPI 生态核心组件关系：

```text
FastAPI
  ├── Starlette：负责 ASGI、路由、请求响应、中间件、WebSocket
  ├── Pydantic：负责类型校验、数据转换、Schema 生成
  ├── Uvicorn：负责运行 ASGI 应用
  └── Python Typing：负责类型声明与开发体验
```

Go 服务端工程师可以这样类比：

| Go 技术栈 | FastAPI 技术栈 |
|---|---|
| Gin / Hertz / Echo | FastAPI |
| net/http handler | route function |
| struct tag binding | Pydantic Model |
| middleware | ASGI middleware / Depends |
| context.Context | Request / Depends / request.state |
| GORM | SQLAlchemy |
| goose / migrate | Alembic |
| go test | pytest |
| go run | uvicorn |

---

## 3. 学习阶段总览

建议分为 6 个阶段学习：

```text
阶段 1：Python 后端基础 + FastAPI 最小 API
阶段 2：Pydantic 参数校验与响应模型
阶段 3：APIRouter、分层结构与工程化
阶段 4：数据库、事务与 SQLAlchemy
阶段 5：Depends、JWT、中间件与认证鉴权
阶段 6：测试、部署、性能与可观测性
```

---

## 4. 第一阶段：FastAPI 最小入门

### 4.1 环境准备

推荐使用 Python 3.11+。

使用 `uv` 创建项目：

```bash
mkdir fast-api-demo
cd fast-api-demo
uv init
uv add fastapi uvicorn
```

如果不用 `uv`，也可以使用标准 `venv`：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
```

### 4.2 第一个 FastAPI 应用

创建 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI(title="FastAPI Demo", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
```

启动服务：

```bash
uvicorn main:app --reload
```

访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/healthz
http://127.0.0.1:8000/docs
```

其中 `/docs` 是 FastAPI 自动生成的 Swagger UI 文档。

### 4.3 路径参数与查询参数

```python
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., ge=1, description="用户 ID，必须大于等于 1"),
    verbose: bool = Query(False, description="是否返回详细信息"),
):
    user = {
        "id": user_id,
        "name": "Tom",
    }

    if verbose:
        user["profile"] = {
            "age": 18,
            "city": "Shanghai",
        }

    return user
```

请求示例：

```bash
curl "http://127.0.0.1:8000/users/1?verbose=true"
```

响应示例：

```json
{
  "id": 1,
  "name": "Tom",
  "profile": {
    "age": 18,
    "city": "Shanghai"
  }
}
```

---

## 5. 第二阶段：Pydantic 数据校验

FastAPI 的核心优势之一，是基于 Pydantic 自动完成请求参数校验和响应结构生成。

### 5.1 请求体模型

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    age: int = Field(..., ge=1, le=150, description="年龄")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(request: UserCreateRequest):
    return UserResponse(
        id=1,
        name=request.name,
        email=request.email,
        age=request.age,
    )
```

安装邮箱校验依赖：

```bash
uv add "pydantic[email]"
```

请求示例：

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom","email":"tom@example.com","age":18}'
```

如果传入非法参数，例如 `name` 太短、`email` 格式错误、`age` 小于 1，FastAPI 会自动返回 `422 Unprocessable Entity`。

### 5.2 请求模型与响应模型分离

真实项目中，不建议一个模型同时用于请求、响应和数据库。

```python
from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)
    email: EmailStr
    age: int = Field(..., ge=1)


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=32)
    age: int | None = Field(default=None, ge=1)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
```

推荐模型分工：

| 模型 | 用途 |
|---|---|
| `UserCreateRequest` | 创建用户请求 |
| `UserUpdateRequest` | 更新用户请求 |
| `UserResponse` | 返回给客户端的数据 |
| `UserDBModel` | 数据库模型 |
| `UserDomainModel` | 业务领域对象 |

---

## 6. 第三阶段：项目工程化结构

### 6.1 推荐目录结构

对于 Go 工程师，推荐使用接近业务模块化的结构：

```text
fast-api-demo/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── modules/
│   │   └── user/
│   │       ├── router.py
│   │       ├── schema.py
│   │       ├── service.py
│   │       └── repository.py
│   └── dependencies.py
├── tests/
│   └── test_users.py
├── pyproject.toml
└── README.md
```

Go 对照：

| Go 项目 | FastAPI 项目 |
|---|---|
| `cmd/server/main.go` | `app/main.py` |
| `internal/user/handler.go` | `modules/user/router.py` |
| `internal/user/service.go` | `modules/user/service.py` |
| `internal/user/repository.go` | `modules/user/repository.py` |
| `internal/config` | `core/config.py` |

### 6.2 `app/main.py`

```python
from fastapi import FastAPI

from app.modules.user.router import router as user_router

app = FastAPI(title="FastAPI Demo", version="0.1.0")

app.include_router(user_router, prefix="/api/v1")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
```

### 6.3 `app/modules/user/schema.py`

```python
from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)
    email: EmailStr
    age: int = Field(..., ge=1, le=150)


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=32)
    age: int | None = Field(default=None, ge=1, le=150)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
```

### 6.4 `app/modules/user/repository.py`

先用内存字典模拟数据库：

```python
from app.modules.user.schema import UserCreateRequest, UserResponse, UserUpdateRequest


class UserRepository:
    def __init__(self):
        self._users: dict[int, UserResponse] = {}
        self._next_id = 1

    def create(self, request: UserCreateRequest) -> UserResponse:
        user = UserResponse(
            id=self._next_id,
            name=request.name,
            email=request.email,
            age=request.age,
        )
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get_by_id(self, user_id: int) -> UserResponse | None:
        return self._users.get(user_id)

    def list(self) -> list[UserResponse]:
        return list(self._users.values())

    def update(self, user_id: int, request: UserUpdateRequest) -> UserResponse | None:
        user = self._users.get(user_id)
        if user is None:
            return None

        updated_user = user.model_copy(
            update=request.model_dump(exclude_unset=True)
        )
        self._users[user_id] = updated_user
        return updated_user

    def delete(self, user_id: int) -> bool:
        if user_id not in self._users:
            return False

        del self._users[user_id]
        return True
```

### 6.5 `app/modules/user/service.py`

```python
from fastapi import HTTPException, status

from app.modules.user.repository import UserRepository
from app.modules.user.schema import UserCreateRequest, UserResponse, UserUpdateRequest


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, request: UserCreateRequest) -> UserResponse:
        return self.repository.create(request)

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return user

    def list_users(self) -> list[UserResponse]:
        return self.repository.list()

    def update_user(self, user_id: int, request: UserUpdateRequest) -> UserResponse:
        user = self.repository.update(user_id, request)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
        return user

    def delete_user(self, user_id: int) -> None:
        deleted = self.repository.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在",
            )
```

### 6.6 `app/dependencies.py`

```python
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService

user_repository = UserRepository()


def get_user_service() -> UserService:
    return UserService(user_repository)
```

### 6.7 `app/modules/user/router.py`

```python
from fastapi import APIRouter, Depends, Path, status

from app.dependencies import get_user_service
from app.modules.user.schema import UserCreateRequest, UserResponse, UserUpdateRequest
from app.modules.user.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreateRequest,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(request)


@router.get("", response_model=list[UserResponse])
def list_users(
    service: UserService = Depends(get_user_service),
):
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(..., ge=1),
    service: UserService = Depends(get_user_service),
):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    request: UserUpdateRequest,
    user_id: int = Path(..., ge=1),
    service: UserService = Depends(get_user_service),
):
    return service.update_user(user_id, request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., ge=1),
    service: UserService = Depends(get_user_service),
):
    service.delete_user(user_id)
```

启动分层项目：

```bash
uvicorn app.main:app --reload
```

创建用户：

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom","email":"tom@example.com","age":18}'
```

---

## 7. 第四阶段：Depends 依赖注入

FastAPI 的 `Depends` 是一个强大的依赖注入机制，可以用于：

- 注入 service。
- 注入 repository。
- 注入数据库 session。
- 注入当前登录用户。
- 注入权限检查。
- 注入配置。
- 测试时替换依赖。

Go 工程师可以把它理解成：

```text
middleware + context value + constructor injection 的组合
```

### 7.1 Depends 基础示例

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def get_current_user():
    return {"id": 1, "name": "Tom"}


@app.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
```

### 7.2 yield 依赖：管理资源生命周期

常见场景是数据库 session：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

执行顺序：

```text
请求开始
  ↓
创建 db session
  ↓
执行业务 handler
  ↓
请求结束后关闭 db session
```

---

## 8. 第五阶段：数据库与 SQLAlchemy

### 8.1 安装依赖

```bash
uv add sqlalchemy alembic
```

如果使用 PostgreSQL：

```bash
uv add psycopg2-binary
```

### 8.2 数据库配置：`app/db/session.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fastapi_demo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
```

### 8.3 声明基类：`app/db/base.py`

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

### 8.4 SQLAlchemy Model：`app/modules/user/model.py`

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
```

### 8.5 创建表：`app/main.py`

```python
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.modules.user.model import UserModel
from app.modules.user.router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Demo", version="0.1.0")
app.include_router(user_router, prefix="/api/v1")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
```

> 生产环境中不建议用 `create_all` 管理表结构，应该使用 Alembic 迁移。这里为了入门演示保持简单。

### 8.6 数据库依赖：`app/dependencies.py`

```python
from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)
```

### 8.7 Repository 接入数据库

```python
from sqlalchemy.orm import Session

from app.modules.user.model import UserModel
from app.modules.user.schema import UserCreateRequest, UserUpdateRequest


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, request: UserCreateRequest) -> UserModel:
        user = UserModel(
            name=request.name,
            email=request.email,
            age=request.age,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def list(self, offset: int = 0, limit: int = 20) -> list[UserModel]:
        return (
            self.db.query(UserModel)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def update(self, user: UserModel, request: UserUpdateRequest) -> UserModel:
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
```

### 8.8 Pydantic 响应模型兼容 ORM

```python
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int
```

`from_attributes=True` 允许 Pydantic 从 SQLAlchemy ORM 对象读取字段。

---

## 9. 第六阶段：JWT 认证鉴权

### 9.1 安装依赖

```bash
uv add python-jose passlib bcrypt
```

### 9.2 密码哈希与 JWT 工具：`app/core/security.py`

```python
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

### 9.3 登录请求与响应模型

```python
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

### 9.4 当前用户依赖

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.security import ALGORITHM, SECRET_KEY
from app.dependencies import get_user_service
from app.modules.user.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="认证失败",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_service.get_user(int(subject))
    return user
```

### 9.5 受保护接口

```python
from fastapi import Depends

from app.dependencies import get_current_user
from app.modules.user.schema import UserResponse


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
```

请求示例：

```bash
curl "http://127.0.0.1:8000/api/v1/users/me" \
  -H "Authorization: Bearer <access_token>"
```

---

## 10. 第七阶段：中间件与统一异常处理

### 10.1 请求耗时中间件

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 10.2 Trace ID 中间件

```python
import uuid

from fastapi import Request


@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    request.state.trace_id = trace_id

    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id

    return response
```

### 10.3 自定义异常

`app/core/exceptions.py`：

```python
class BizError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
```

注册异常处理器：

```python
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BizError


@app.exception_handler(BizError)
async def biz_error_handler(request: Request, exc: BizError):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "trace_id": getattr(request.state, "trace_id", None),
        },
    )
```

---

## 11. 第八阶段：测试

### 11.1 安装测试依赖

```bash
uv add --dev pytest httpx
```

### 11.2 健康检查测试：`tests/test_health.py`

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

运行：

```bash
pytest
```

### 11.3 用户接口测试

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Tom",
            "email": "tom@example.com",
            "age": 18,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] >= 1
    assert data["name"] == "Tom"
    assert data["email"] == "tom@example.com"
    assert data["age"] == 18


def test_create_user_with_invalid_age():
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Tom",
            "email": "tom@example.com",
            "age": -1,
        },
    )

    assert response.status_code == 422
```

### 11.4 测试时覆盖依赖

FastAPI 支持依赖替换，非常适合测试。

```python
from app.dependencies import get_user_service


class FakeUserService:
    def list_users(self):
        return [
            {
                "id": 1,
                "name": "Fake User",
                "email": "fake@example.com",
                "age": 18,
            }
        ]


def override_get_user_service():
    return FakeUserService()


app.dependency_overrides[get_user_service] = override_get_user_service
```

测试结束后清理：

```python
app.dependency_overrides.clear()
```

---

## 12. 第九阶段：异步模型与性能

### 12.1 sync 与 async 的区别

FastAPI 支持两种 handler：

```python
@app.get("/sync")
def sync_handler():
    return {"type": "sync"}
```

```python
@app.get("/async")
async def async_handler():
    return {"type": "async"}
```

区别：

| 类型 | 适合场景 |
|---|---|
| `def` | 普通同步逻辑、同步数据库驱动 |
| `async def` | 异步 HTTP 调用、异步数据库、WebSocket |

### 12.2 错误示例：阻塞 event loop

```python
import time


@app.get("/bad")
async def bad_handler():
    time.sleep(3)
    return {"message": "done"}
```

`time.sleep(3)` 会阻塞事件循环。正确写法：

```python
import asyncio


@app.get("/good")
async def good_handler():
    await asyncio.sleep(3)
    return {"message": "done"}
```

### 12.3 Go 与 Python 并发模型对比

| Go | Python FastAPI |
|---|---|
| goroutine 很轻量 | coroutine 很轻量 |
| 阻塞 goroutine 通常影响较小 | 阻塞 event loop 影响很大 |
| runtime 调度 goroutine | event loop 调度 coroutine |
| channel 通信 | asyncio.Queue / await |
| CPU 密集可用 goroutine | CPU 密集任务不适合直接放 Web 进程 |

结论：

```text
FastAPI 非常适合 I/O 密集型 API 服务。
CPU 密集型任务建议交给独立 Worker、任务队列或其他服务处理。
```

---

## 13. 第十阶段：配置管理

### 13.1 安装依赖

```bash
uv add pydantic-settings
```

### 13.2 配置类：`app/core/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Demo"
    environment: str = "dev"
    database_url: str = "sqlite:///./fastapi_demo.db"
    jwt_secret_key: str = "change-me"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
```

使用配置：

```python
from app.core.config import settings

app = FastAPI(title=settings.app_name)
```

`.env` 示例：

```env
APP_NAME=FastAPI Demo
ENVIRONMENT=dev
DATABASE_URL=sqlite:///./fastapi_demo.db
JWT_SECRET_KEY=please-change-me
```

---

## 14. 第十一阶段：Docker 部署

### 14.1 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy pydantic-settings

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建镜像：

```bash
docker build -t fast-api-demo .
```

运行容器：

```bash
docker run --rm -p 8000:8000 fast-api-demo
```

### 14.2 docker-compose 示例

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      APP_NAME: "FastAPI Demo"
      ENVIRONMENT: "dev"
      DATABASE_URL: "sqlite:///./fastapi_demo.db"
```

启动：

```bash
docker compose up --build
```

---

## 15. 第十二阶段：生产化能力

### 15.1 日志

简单示例：

```python
import logging

logger = logging.getLogger(__name__)


@app.get("/healthz")
def health_check():
    logger.info("health check")
    return {"status": "ok"}
```

生产建议：

- 日志使用 JSON 格式。
- 每个请求带 trace id。
- 错误日志包含异常栈。
- 敏感字段脱敏，例如 password、token、secret。

### 15.2 健康检查

```python
@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/readyz")
def readiness_check():
    return {
        "status": "ready",
        "dependencies": {
            "database": "ok",
        },
    }
```

### 15.3 Prometheus 指标

安装：

```bash
uv add prometheus-client
```

示例：

```python
from fastapi import Response
from prometheus_client import Counter, generate_latest

request_counter = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path"],
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    request_counter.labels(
        method=request.method,
        path=request.url.path,
    ).inc()
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

---

## 16. 推荐练手项目：Todo 任务管理系统

推荐做一个完整的 Todo API 项目。

功能迭代路线：

```text
版本 1：单文件 API
  - 创建 Todo
  - 查询 Todo
  - 删除 Todo

版本 2：分层结构
  - router
  - schema
  - service
  - repository

版本 3：数据库
  - SQLAlchemy
  - SQLite / PostgreSQL
  - Alembic

版本 4：认证鉴权
  - 用户注册
  - 用户登录
  - JWT
  - 当前用户只能访问自己的 Todo

版本 5：工程化
  - pytest
  - Docker
  - 配置管理
  - 日志
  - 统一异常

版本 6：生产化
  - Redis 缓存
  - Prometheus
  - OpenTelemetry
  - CI/CD
```

---

## 17. 精通 FastAPI 必学清单

### 17.1 第一优先级

```text
1. Python 类型注解
2. FastAPI 路由
3. Pydantic v2
4. Depends
5. APIRouter
6. pytest + TestClient
```

### 17.2 第二优先级

```text
7. SQLAlchemy
8. Alembic
9. JWT 鉴权
10. 中间件
11. 配置管理
12. 异常处理
```

### 17.3 第三优先级

```text
13. async / await
14. ASGI / Starlette
15. Docker 部署
16. 日志和监控
17. Redis / 后台任务
18. 性能优化
```

### 17.4 第四优先级

```text
19. WebSocket
20. OpenTelemetry
21. Kubernetes
22. FastAPI / Starlette 源码
23. 高级架构设计
```

---

## 18. 6 周学习计划

### 第 1 周：基础入门

目标：掌握 Python 类型注解、FastAPI 单文件 API、Pydantic 校验。

任务：

```text
1. 写 GET / POST 接口
2. 使用 Path / Query / Body
3. 使用 BaseModel
4. 查看 /docs 文档
5. 完成一个单文件 Todo API
```

### 第 2 周：项目结构

目标：掌握 APIRouter、分层项目结构、Depends。

任务：

```text
1. 拆分 router
2. 拆分 schema
3. 拆分 service
4. 拆分 repository
5. 用 Depends 注入 service
```

### 第 3 周：数据库

目标：掌握 SQLAlchemy、接入 SQLite 或 PostgreSQL、理解 session 生命周期。

任务：

```text
1. 定义数据库模型
2. 完成 CRUD
3. 用 Depends 注入 db session
4. 理解 commit / refresh / rollback
5. 尝试 Alembic 迁移
```

### 第 4 周：认证与测试

目标：掌握 JWT、pytest、依赖覆盖。

任务：

```text
1. 用户注册
2. 用户登录
3. 生成 access token
4. 编写受保护接口
5. 编写接口测试
```

### 第 5 周：异步、缓存与后台任务

目标：理解 async / await、使用 Redis、使用后台任务。

任务：

```text
1. 编写 async endpoint
2. 避免阻塞 event loop
3. 接入 Redis
4. 使用 BackgroundTasks
5. 理解任务队列适用场景
```

### 第 6 周：生产化

目标：Docker 部署、日志与监控、性能优化、阅读源码。

任务：

```text
1. 编写 Dockerfile
2. 编写 docker-compose.yaml
3. 添加 healthz / readyz
4. 添加 metrics
5. 阅读 FastAPI / Starlette 核心源码
```

---

## 19. 最小可运行完整示例

如果只想快速复制运行，可以使用下面这个单文件版本。

### `main.py`

```python
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="FastAPI 入门 Demo", version="0.1.0")


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=32)
    email: EmailStr
    age: int = Field(..., ge=1, le=150)


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=32)
    age: int | None = Field(default=None, ge=1, le=150)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


users: dict[int, UserResponse] = {}
next_user_id = 1


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreateRequest):
    global next_user_id

    user = UserResponse(
        id=next_user_id,
        name=request.name,
        email=request.email,
        age=request.age,
    )
    users[user.id] = user
    next_user_id += 1

    return user


@app.get("/users", response_model=list[UserResponse])
def list_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return list(users.values())[offset : offset + limit]


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int = Path(..., ge=1)):
    user = users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    return user


@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    request: UserUpdateRequest,
    user_id: int = Path(..., ge=1),
):
    user = users.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    updated_user = user.model_copy(update=request.model_dump(exclude_unset=True))
    users[user_id] = updated_user

    return updated_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int = Path(..., ge=1)):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    del users[user_id]
```

安装依赖：

```bash
uv add fastapi uvicorn "pydantic[email]"
```

启动：

```bash
uvicorn main:app --reload
```

创建用户：

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom","email":"tom@example.com","age":18}'
```

查询用户：

```bash
curl "http://127.0.0.1:8000/users/1"
```

查看接口文档：

```text
http://127.0.0.1:8000/docs
```

---

## 20. Go 工程师迁移注意事项

### 20.1 不要把 async 等同于 goroutine

Go 中：

```go
go func() {
    doSomething()
}()
```

Python 中：

```python
await do_something()
```

两者模型不同。Python 的 coroutine 需要主动 `await`，并且阻塞 event loop 会影响并发能力。

### 20.2 不要在 async handler 中写阻塞代码

错误：

```python
@app.get("/bad")
async def bad():
    time.sleep(1)
    return {"ok": True}
```

正确：

```python
@app.get("/good")
async def good():
    await asyncio.sleep(1)
    return {"ok": True}
```

### 20.3 不要把 Pydantic Model 当数据库 Model

推荐分离：

```text
Request Schema
Response Schema
Database Model
Domain Model
```

这类似 Go 项目中的：

```text
DTO
Entity
PO
VO
```

### 20.4 不要忽视 Depends

`Depends` 是 FastAPI 的核心能力之一，可以承担：

```text
认证
鉴权
数据库 session 生命周期
配置注入
service 注入
测试替换
资源清理
```

---

## 21. 总结

如果你是 Go 服务端工程师，学习 FastAPI 的最佳方式不是从 Python 语法细节开始，而是用后端工程视角迁移经验。

推荐路线：

```text
FastAPI 路由
  ↓
Pydantic 数据校验
  ↓
APIRouter 分层结构
  ↓
Depends 依赖注入
  ↓
SQLAlchemy 数据库
  ↓
JWT 认证鉴权
  ↓
pytest 测试
  ↓
Docker 部署
  ↓
日志、监控、性能优化
  ↓
ASGI / Starlette / FastAPI 源码
```

完成这条路线后，你不仅会写 FastAPI 接口，还能把 FastAPI 用在真实生产服务中。
