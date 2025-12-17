# 后端脚手架（Python 3.13 + FastAPI + ARQ）

本目录提供一个可执行的后端开发脚手架，遵循 `docs/development_architecture.md` 的“**演进式分层架构 (Pragmatic Layered Architecture)**”落地方式。我们保留了南向硬件对接的六边形适配模式，但简化了内部业务开发流程：

- `src/app/`：北向适配器（FastAPI Web/API）
- `src/core/`：核心域（统一模型 + 业务服务 + 接口定义）
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

本项目采用 **演进式分层架构**，在保留核心硬件解耦（南向网关）的前提下，大幅简化了业务实体的转换成本。

### 1. 核心域 (Core): 定义业务与数据
核心层包含实体定义和业务逻辑服务。

1.  **定义领域模型 (`src/core/models.py`)**
    *   直接使用 SQLAlchemy `DeclarativeBase` 定义核心实体。
    *   **原则**: 这里的模型既是业务实体，也是数据库表结构（Unified Model）。
    *   *Example*: `class InboundOrder(Base): ...`

2.  **定义端口/接口 (`src/core/ports.py`)**
    *   使用 `Protocol` 定义 Service 依赖的外部能力（尤其是 Repository 和 硬件接口）。
    *   **红线**: 凡是涉及 AGV/RCS/PLC 的交互，**必须**定义接口，**严禁**在 Service 直接写 HTTP 请求或 Socket 代码。

3.  **编写服务 (`src/core/services/`)**
    *   按领域划分 Service 类（如 `OrderService`）。
    *   通过构造函数注入 Ports (Dependency Injection)。
    *   直接操作 `src/core/models.py` 中的实体，无需编写 Mapper。

### 2. 基础设施层 (Infra): 实现技术细节
实现 Core 层定义的接口。

1.  **实现 Repository (`src/infra/repositories/`)**
    *   实现 `core/ports.py` 中的 Repository 接口。
    *   **简化**: 直接存取 Core 中的实体，无需编写 `_to_domain` 转换函数。

2.  **实现硬件适配器 (`src/southbound/`)**
    *   实现 `core/ports.py` 定义的硬件控制接口。
    *   处理具体的 HTTP/TCP/Modbus 协议细节。

### 3. 应用层 (App): 暴露 API
通过 API 暴露 Service 能力。

1.  **定义 API Schema (`src/app/schemas/`)**
    *   使用 Pydantic 定义请求（In）和响应（Out）的数据结构。
    *   **注意**: 这里的 Schema 仅用于 API 序列化，与 Core Model 区分开。

2.  **依赖注入装配 (`src/app/dependencies.py`)**
    *   编写 `get_xxx_service` 函数。
    *   装配 Repo、Outbox 和 Service。

3.  **编写路由 (`src/app/api/v1/`)**
    *   创建 API 路由函数。
    *   注入 Service: `service: OrderService = Depends(get_order_service)`.
    *   调用 Service 方法。

### 4. 异步任务 (Workers)
如果涉及后台处理（如 ARQ 任务）：

1.  **编写任务逻辑**: 在 `src/infra/workers/tasks.py` 中编写异步函数。
2.  **注册任务**: 在 `src/infra/workers/arq_worker.py` 的 `WorkerSettings.functions` 列表中添加该函数。
3.  **触发任务**: 在 Service 中通过 `JobQueue` 端口调用 `enqueue`。

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
