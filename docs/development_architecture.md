# P9 WES 开发架构指南 (Development Architecture Guidelines)

## 1. 核心设计理念 (Design Philosophy)

本架构基于 `@docs/system_architecture.md` 和 `@docs/technology_stack_decision_pack.md`，旨在构建一个高可用、低延迟且易于扩展的控制中台。

1.  **模块化单体 (Modular Monolith)**:
    *   鉴于系统需“独立部署”且各模块交互紧密，采用单体仓库（Monorepo）开发。
    *   内部模块间保持严格边界，统一构建 Docker 镜像，适合边缘服务器部署。
2.  **六边形架构 (Hexagonal Architecture)**:
    *   **核心域 (Domain - L2)**: 纯净的业务逻辑（策略、编排），不依赖具体框架或驱动。
    *   **端口 (Ports)**: 定义核心域所需的接口（如 `IHardwareAdapter`, `IRepository`）。
    *   **适配器 (Adapters)**: L1 (FastAPI), L3 (HTTPX/Modbus), DB (SQLAlchemy) 作为适配器实现接口。
3.  **异步优先 (Async First)**:
    *   全链路异步（Async/Await），最大化利用 Python 3.11+ 和 FastAPI 的协程性能，处理大量设备 I/O。

## 2. 推荐的代码目录结构 (Directory Structure)

```text
p9-wes/
├── .github/                # CI/CD workflows
├── deploy/                 # Dockerfile, docker-compose.yml
├── docs/                   # 项目文档
├── frontend/               # React + Vite 前端项目 (PWA/SPA)
├── src/
│   ├── app/                # [L1 北向适配器] FastAPI Web 层
│   │   ├── api/            # Endpoints (Routes)
│   │   ├── main.py         # App factory
│   │   └── schemas/        # API DTOs (Pydantic models)
│   │
│   ├── core/               # [L2 核心域] 纯业务逻辑 (The Brain)
│   │   ├── engine/         # 策略引擎 (Strategy Pattern)
│   │   │   ├── interfaces.py # 策略接口定义
│   │   │   ├── binning.py  # 装箱算法实现
│   │   │   └── routing.py  # 路由算法实现
│   │   ├── orchestrator/   # 任务编排
│   │   │   ├── state_machine.py # 状态机逻辑
│   │   │   └── workflow.py # 任务流定义
│   │   ├── domain_models.py # 内部业务实体
│   │   └── ports.py        # 核心域接口定义 (IHardware, IRepo)
│   │
│   ├── infra/              # [基础设施适配器] 数据库与中间件
│   │   ├── database/       # SQLAlchemy models & Alembic
│   │   ├── repositories/   # IRepo 的具体实现 (PG/Timescale)
│   │   ├── redis/          # 缓存与分布式锁实现
│   │   └── workers/        # ARQ/Celery 异步任务配置
│   │
│   └── southbound/         # [L3 南向适配器] 硬件驱动
│       ├── adapters/       # IHardwareAdapter 的具体实现
│       │   ├── rcs_http.py # HTTPX client for AGV
│       │   ├── ecs_tcp.py  # Asyncio TCP client for PLC
│       │   └── pda_api.py
│       └── gateway.py      # 硬件网关逻辑 (UHI)
│
├── tests/                  # Pytest 测试集
├── poetry.lock             # 依赖锁定
├── pyproject.toml          # 项目配置
└── README.md
```

## 3. 关键模块实现模式 (Implementation Patterns)

### 3.1 核心层：策略模式与依赖注入 (Strategy & DI)
为了满足“业务逻辑可配置”，通过接口定义策略，并在运行时注入具体实现。

```python
# src/core/engine/interfaces.py
class IBinningStrategy(ABC):
    @abstractmethod
    async def calculate(self, material: Material, context: Context) -> BinLocation: ...

# src/app/dependencies.py (FastAPI Dependency Injection)
async def get_binning_strategy() -> IBinningStrategy:
    # 可从配置或数据库加载具体策略类
    return ConfigurableBinningStrategy()
```

### 3.2 南向层：插件化硬件适配器 (Plugin Adapters)
对应 `hardware_interface_standard.md`，实现通用硬件接口 (UHI)。

```python
# src/southbound/adapters/rcs_http.py
class RcsAdapter(IHardwareAdapter):
    async def send_command(self, cmd: Command) -> Response:
        # 将标准命令转换为 RCS 特定 JSON
        payload = self._to_rcs_payload(cmd)
        resp = await self.client.post("/task", json=payload)
        return self._from_rcs_response(resp)
```

### 3.3 数据层：CQRS 与 读写分离
*   **Command (Write)**: 业务操作（如下发任务）写入 PostgreSQL。
*   **Query (Read)**:
    *   **执行状态查询**: 实时大屏或高频查询优先读取 Redis 缓存（任务状态、设备状态等瞬态数据）。
    *   **库存查询**: 不维护本地库存镜像，实时透传至 WMS，可短时缓存查询结果 (TTL ≤ 30s)。
*   **TimescaleDB**: 硬件日志异步批量写入，避免阻塞主业务事务。

### 3.4 异步任务编排
使用 **ARQ** 处理耗时操作（如波次计算、跨系统同步）。
*   API 接收请求 -> 推送 Job 到 Redis -> Worker 异步执行 -> 更新 Task 状态。

## 4. 前端集成 (Frontend Integration)
*   **生成器**: 使用 `openapi-typescript-codegen` 基于 FastAPI 的 `openapi.json` 自动生成前端 TypeScript SDK，确保接口类型安全。
*   **部署**: 前端构建为静态资源，由 Nginx 反向代理，与后端 API 聚合在同一域名下，解决 CORS 问题。

## 5. 开发工作流 (Development Workflow)
1.  **环境管理**: 使用 **Poetry** 管理 Python 依赖。
2.  **代码规范**: 采用 **Ruff** (Linting) + **Black** (Formatting) + **Mypy** (Type Checking)。
3.  **测试**: 使用 **Pytest** + **Testcontainers** (在 Docker 中启动真实的 PG/Redis 进行集成测试)。
4.  **配置**: 使用 **Pydantic Settings** 管理环境变量 (`.env`)。
