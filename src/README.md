# 后端脚手架（Python 3.13 + FastAPI + ARQ）

本目录提供一个可执行的后端开发脚手架，遵循 `docs/development_architecture.md` 的“模块化单体 + 六边形架构 (Hexagonal Architecture)”落地方式：

- `src/app/`：北向适配器（FastAPI Web/API）
- `src/core/`：核心域（策略/编排/状态机的框架无关实现）
- `src/infra/`：基础设施适配器（PostgreSQL/Redis/Outbox/Worker）
- `src/southbound/`：南向适配器（UHI/插件化硬件驱动）

## 本地启动（开发）

1) 启动依赖（PostgreSQL + Redis）：

`docker compose -f src/deploy/docker-compose.yml up -d`

2) 安装依赖：

`python -m pip install -r src/requirements.txt`

3) 启动 API：

`uvicorn src.main:app --reload --port 8000`

4) 启动 Worker（ARQ）：

`arq src.infra.workers.arq_worker.WorkerSettings`

> 若你暂时没启动 Postgres/Redis，API 也可以启动但会进入 `degraded`（见 `/api/v1/health`），相关业务接口会返回 `503`。

## 环境变量（可选）

- 参考 `src/.env.example`
- `WES_DATABASE_URL`：默认 `postgresql+asyncpg://postgres:postgres@localhost:5432/wes`
- `WES_REDIS_URL`：默认 `redis://localhost:6379/0`
- `WES_WMS_BASE_URL`：默认 `http://localhost:8080`
- `WES_AUTO_CREATE_DB`：默认 `true`（开发环境自动建表）
- `WES_STRICT_STARTUP`：默认 `false`（为 `true` 时依赖不可用将直接启动失败）

## 开发指南 (Step-by-Step)

本项目严格遵循**六边形架构**，新功能开发请按以下顺序进行，保持核心逻辑纯净。

### 1. 核心域 (Core): 定义“是什么”
开发应从业务逻辑开始，而非数据库。

1.  **定义领域模型 (`src/core/models.py`)**
    *   使用纯 Python `dataclass` 定义业务实体。
    *   **禁止**: 引入 SQLAlcehmy、Pydantic 或其他框架代码。
    *   *Example*: `class InboundOrder(...)`

2.  **定义端口/接口 (`src/core/ports.py`)**
    *   使用 `Protocol` 定义 Use Case 依赖的外部能力（如 Repository, Client）。
    *   **原则**: 接口签名应使用 Domain Model，而非 ORM Model。
    *   *Example*: `class InboundOrderRepository(Protocol): ...`

3.  **编写用例 (`src/core/use_cases/`)**
    *   实现具体的业务流程。
    *   通过构造函数注入 Ports (Dependency Injection)。
    *   *Example*: `class IngestInboundOrder: ...`

### 2. 基础设施层 (Infra): 实现“怎么做”
实现 Core 层定义的接口。

1.  **定义数据库表 (`src/infra/database/models.py`)**
    *   使用 SQLAlchemy `DeclarativeBase` 定义表结构。
    *   *Example*: `class InboundOrderRow(Base): ...`

2.  **实现 Repository (`src/infra/repositories/`)**
    *   实现 `core/ports.py` 中的 Repository 接口。
    *   **关键**: 负责 `Domain Model` <-> `ORM Model` 的相互转换。
    *   *Example*: `class SqlAlchemyInboundOrderRepository(...)`

### 3. 应用层 (App): 定义“入口”
通过 API 暴露 Use Case。

1.  **定义 API Schema (`src/app/schemas/`)**
    *   使用 Pydantic 定义请求（In）和响应（Out）的数据结构。
    *   *Example*: `class InboundOrderIn(BaseModel): ...`

2.  **依赖注入装配 (`src/app/dependencies.py`)**
    *   编写 `get_xxx_use_case` 函数。
    *   在此处实例化 Use Case，并注入具体的 Infra 实现（如 SqlAlchemy Repo）。

3.  **编写路由 (`src/app/api/v1/`)**
    *   创建 API 路由函数。
    *   使用 `Depends(get_xxx_use_case)` 获取业务对象。
    *   调用 `use_case.handle()` 并返回 Pydantic Schema。

4.  **注册路由 (`src/app/api/router.py`)**
    *   将新模块的 router include 进总 router。

### 4. 异步任务 (Workers)
如果涉及后台处理（如 ARQ 任务）：

1.  **编写任务逻辑**: 在 `src/infra/workers/tasks.py` 中编写异步函数。
2.  **注册任务**: 在 `src/infra/workers/arq_worker.py` 的 `WorkerSettings.functions` 列表中添加该函数。
3.  **触发任务**: 在 Use Case 中通过 `JobQueue` 端口调用 `enqueue`。

### 5. 代码质量检查

提交代码前，请运行以下命令确保符合规范：

```bash
# 格式化代码
ruff format src

# 静态检查 (Lint)
ruff check src --fix

# 运行测试 (如果有)
pytest
```