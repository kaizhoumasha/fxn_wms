# P9 WES 技术栈决策包(Technology Stack Decision Pack)

> **文档版本**: 1.0
> **日期**: 2025-12-16
> **牵头**: CTO Office / Architecture
> **状态**: 🟡 待讨论(Pending Decision)

本文件用于将两份文档的分析观点合并成一套一致口径，并把“结论”改为**可选决策项**供领导拍板。原文件保留作为历史记录与溯源依据。

---

## 1. 权威口径与范围 (Authority & Scope)

1. **需求与验收权威**：`@docs/SRS.md`
2. **供应商设备对接权威**：`@docs/third_party_integration_whitepaper.md`（对外唯一权威）
3. **内部架构与实现参考**：`@docs/system_architecture.md`、`@docs/hardware_interface_standard.md`、`@docs/development_architecture.md`

> 重要口径：对外 ECS 供应商接入优先采用 **HTTP/HTTPS + JSON** 的 “Command → Ack → Callback” 异步模式；TCP/Modbus 等多协议应尽量通过供应商网关/内部网关做协议收敛，避免把异构复杂度侵入核心域。

---

## 2. 系统定位与硬约束 (Positioning & Non-Negotiables)

P9 WES 的系统定位是：**独立部署的集成化控制中台**（Independent Integration & Control Middleware），本质是“边缘侧高性能代理 + 任务编排大脑”。

硬约束（不随语言变化）：

* **边缘部署 (Edge-Ready)**：优先单机/小集群，低运维复杂度（Docker/Compose 起步）
* **低延迟 (Low Latency)**：设备指令链路与 PDA 作业链路稳定在 <500ms 级别（以 P95 为管理目标）
* **异步编排 (Async Orchestration)**：Command→Ack→Callback，避免长连接阻塞与同步等待
* **幂等性 (Idempotency)**：网络抖动与重试不导致物理动作重复执行
* **插件化适配 (Plugin Adapters)**：核心域与厂商/协议解耦，支持多供应商并存
* **策略可配置 (Configurable Logic)**：可快速迭代，但必须可控、可审计、可回滚
* **存储基线 (Data Baseline)**：`PostgreSQL` + `Redis`（可选 TimescaleDB）

---

## 3. 决策驱动因素(Decision Drivers)

以下因素共同决定“技术栈选择的权重”：

1. **工作负载特征 (Workload)**：I/O 密集（高并发 API、设备/系统通信、状态更新）为主，CPU 密集为辅
2. **硬件异构 (Heterogeneous Hardware)**：现场协议多样（HTTP/TCP/Modbus/MQTT），但对外希望协议标准化
3. **策略灵活性 (Configurable Strategy)**：波次、装箱、路由等策略需要频繁迭代
4. **风险属性 (Risk)**：系统直接控制实体硬件，错误可能造成停线/物料损失/安全事件
5. **团队现状 (Team)**：现有核心语言资产偏 `.NET`（历史为 .NET Framework/Web Forms），新平台需要避免“框架升级但架构不升级”
6. **交付与长期维护 (Delivery & Maintenance)**：边缘现场运维能力、招聘成本、工具链成熟度

---

## 4. 平台能力基线（语言无关）(Language-Agnostic Platform Baseline)

无论选择 `.NET 8` 还是 `Python/FastAPI`，下列能力必须作为平台基线交付（否则无法满足稳定性/验收）：

1. **无状态 (Stateless)**：禁止依赖 `Session`/进程内状态承载业务；瞬态状态进 Redis，关键状态进 PostgreSQL
2. **异步设备编排 (Command → Ack → Callback)**：对外 ECS 按白皮书，避免同步阻塞
3. **幂等 (Idempotency)**：统一 `command_id/idempotency_key`；回调去重键建议 `(device_id, command_id)`
4. **超时/重试 (Timeout & Retry)**：统一超时、指数退避、最大重试次数；失败进入挂起/人工介入
5. **断点续传 (Checkpoint & Resume)**：状态机关键状态持久化；服务重启可从 checkpoint 恢复
6. **一致性出站 (Outbox Pattern)**：对外调用（下发命令、回传上游实绩等）可靠投递/可重放
7. **可配置策略治理 (Governance)**：规则表/决策表优先；脚本扩展需隔离（资源限制）、版本化、审批审计、灰度/回滚
8. **可观测性 (Observability)**：`trace_id/task_id/command_id` 全链路贯穿 API/Worker/外部调用/设备回调；指标+日志+告警能定位到“单任务链路”
9. **安全基线 (Security Baseline)**：Token/API Key + RBAC + 审计日志；按现场条件可选 mTLS/内网隔离
10. **部署与联调基建 (Deployment & Integration Readiness)**：Docker/Compose 一键部署；提供设备模拟器/Mock（超时、重试、重复回调、乱序回调）

---

## 5. 候选技术栈(Candidate Stacks)

### A. Python 3.13+ + FastAPI（敏捷与动态策略导向）

适配点：

* 异步 I/O 生态成熟，适合高并发代理与设备通信
* 动态策略天然易做（脚本/插件），利于快速迭代
* 工业侧协议库丰富（Modbus/串口/自定义解析），“非标适配”开发效率高

关键风险（必须治理）：

* 动态策略容易失控（脚本治理、审计、回滚与隔离缺失会带来生产风险）
* 运行时类型错误风险更高（需要更强的接口校验与测试纪律）
* 团队若缺少 Python 生产运维经验，初期交付风险会上升

典型组件（示例，不是强制）：

* Web/API：FastAPI + Uvicorn
* 任务编排：ARQ（Redis）或 Celery
* 数据：PostgreSQL（可选 TimescaleDB）+ Redis
* 集成：HTTPX、asyncio、pymodbus、aiomqtt
* 观测：OpenTelemetry + 结构化日志

### B. .NET 8 + ASP.NET Core Minimal APIs（风险控制与团队传承导向）

适配点：

* 性能与吞吐强，Linux/Docker 原生支持好，适合边缘高并发
* 强类型与工程化工具链完善，更利于“硬件控制场景”的风险控制
* 团队语言资产可复用（从 Framework 到 Core 的思维切换是重点）

关键风险（必须避免）：

* “用 Core 写出 Web Forms 风格”会直接失去边缘/高并发优势
* 动态策略若用“动态编译 C#”会显著增加复杂度与风险

典型组件（示例，不是强制）：

* Web/API：ASP.NET Core 8 Minimal APIs + OpenAPI/Swagger
* 后台编排：BackgroundService（可选 Hangfire/Quartz）
* 重试：Polly；内部队列：Channels；网络流：System.IO.Pipelines（如涉及 TCP）
* 数据：Npgsql +（Dapper 或 EF Core）
* 观测：OpenTelemetry + 结构化日志

动态策略建议路径（更稳健）：

* 规则表/决策表 + 版本化发布（优先）
* 如确需脚本：Lua/JS 引擎（NLua/Jint）或隔离服务（见方案 C）

### C. 混合方案：.NET 8 核心 + 策略/适配隔离（兼顾强类型与灵活性）

定位：当“策略热更新/复杂策略”是 P0 且频繁变化，但核心编排与硬件风险控制仍希望保持强类型时采用。

基本形态：

* WES 核心编排/状态机/接口层：`.NET 8`
* 策略执行：独立“策略沙箱服务”（可用 Python 或 Lua/JS 沙箱），通过 HTTP/gRPC 调用，强约束输入输出契约

收益与代价：

* 收益：核心稳定、策略可快速迭代且隔离风险
* 代价：系统复杂度与运维成本上升（服务间调用、版本管理、观测与容错更复杂）

---

## 6. 人力需求模型（基于 SRS）(Staffing Model Based on SRS)

> 本节基于 `@docs/SRS.md` 的范围、接口与非功能要求，推导“建设一套可交付的 WES 中台”所需角色与人力规模（FTE, Full-Time Equivalent）。用于预算/排期评估；实际人数需结合并行度、供应商配合度与上线窗口校准。

### 6.1 SRS 驱动的工作流拆分 (Workstreams Derived from SRS)

从 SRS 的章节结构可抽象出以下工作流（Workstreams）：

1. **平台底座 (Platform Baseline)**：断点续传/恢复（Checkpoint & Resume）、通信异常重试（Retry）、幂等（Idempotency）、降级（Manual Fallback）、启动独立性/故障恢复/可观测性（Observability）等（SRS 3.7、5）。
2. **核心编排与状态机 (Orchestration & State Machine)**：任务编排引擎、执行状态追踪、优先级与插队、并发控制（Concurrency Control）（SRS 3.4、3.7.4）。
3. **北向集成 (Northbound Integration)**：订单/工单/主数据接入、库存查询/预留/确认、与现有 WMS/SAP 的强一致性交互（SRS 4.1、5）。
4. **南向适配与设备联调 (Southbound Adapters & Commissioning)**：RCS/ECS 插件化适配、命令下发与回调、心跳/离线判定、现场异常处置联调（SRS 4.2、3.7.3；ECS 对外对接遵循白皮书）。
5. **策略与规则 (Strategy & Rules)**：装箱/波次/路由/分配等策略能力（SRS 3.4.2 等），并以“可配置策略治理”（版本、审批、审计、回滚、隔离）方式落地。
6. **作业端与管理端 (PDA/Console UI)**：PDA 指导与人工降级、监控与运维操作入口（SRS 3.7.2、4.1）。
7. **测试与验收保障 (QA & UAT Readiness)**：异常重试、断点恢复、熔断暂停/自动恢复、并发控制等端到端验证与回归基线（SRS 3.7、5）。
8. **交付与运维 (DevOps/SRE)**：边缘环境交付、监控告警、日志追踪、备份/恢复演练与现场值守机制（SRS 5）。

### 6.2 影响人力的主要变量 (Staffing Drivers)

SRS 明确该系统是集成中台，外部依赖会显著影响人力与排期：

* **上游系统 (Upstream)**：现有 WMS/SAP（接口稳定性、幂等规则、异常码、联调窗口）
* **下游系统 (Downstream)**：ECS/RCS（供应商实现质量、回调一致性、现场网络稳定性）
* **旁路系统 (Side Systems)**：QMS/SFC 等（是否纳入一期范围）
* **现场条件 (On-site Constraints)**：边缘服务器规格、网络拓扑、设备数量与上线窗口（停线/夜间窗口）

> 经验规则（用于估算）：每新增 1 个“外部系统/设备域”，通常需要额外 **0.5–1.5 FTE** 的集成与联调投入（Integration & Commissioning），并推高 QA/现场支持工作量。

### 6.3 建议角色配置（最小可交付 vs 标准交付）(Recommended Roles)

面向“先新建 WES 中台（不涉及旧系统替换）”，建议按下表配置（FTE）：

| 角色 (Role)                               | 核心职责 (Responsibility)                                | 最小可交付 (MVP) |        | 标准交付 (Recommended) |
| ----------------------------------------- | -------------------------------------------------------- | ---------------: | ------ | ---------------------: |
| 架构/技术负责人 (Architect/Tech Lead)     | 架构落地、关键机制（幂等/Outbox/状态机）、技术决策与评审 |                1 | 周凯   |                      1 |
| 后端核心 (Backend Core)                   | 编排/状态机、策略框架、数据模型、核心 API                |                2 | 开杰   |                   3–4 |
| 集成工程师 (Integration Engineer)         | WMS/SAP/QMS/SFC 接口对接、契约/Mock、联调闭环            |                1 |        |                      2 |
| 设备/适配器工程师 (Adapter/Commissioning) | ECS/RCS 适配器、回调幂等、心跳/离线、现场联调            |                1 | 供应商 |                   2–3 |
| 前端 (Frontend: PDA/Console)              | PDA 作业端 + 监控/配置台（PWA/SPA）                      |                1 | 周凯   |                      2 |
| QA/测试 (QA)                              | 自动化回归、端到端场景、UAT 支撑与验收脚本               |                1 | 实施   |                      2 |
| DevOps/SRE                                | Docker/Compose、监控告警、日志追踪、发布/回滚、演练      |              0.5 | 周凯   |                      1 |
| 产品/项目 (PM/PO)                         | 范围/里程碑、跨团队协同、验收组织与推进                  |              0.5 | 周凯   |                      1 |

汇总建议：

* **最小可交付团队**：约 **8 FTE**
* **标准交付团队**：约 **13–16 FTE**

### 6.4 里程碑与人力分配（建议）(Milestones & Allocation)

为降低集成项目不确定性，建议按“先底座、再业务流、再大联调”推进：

1. **第 0–4 周：平台底座闭环 (Platform Baseline Ready)**：幂等/重试/断点恢复/Outbox/观测/部署一键启动 + Mock 设备与最小链路。
2. **第 5–10 周：核心业务流 MVP (Core Flows MVP)**：跑通至少 1 条端到端主链路（单据接入 → 编排 → 下发 → 回调 → 确认/对账）。
3. **第 11–16 周：联调与验收 (Commissioning & UAT)**：多设备并发、异常恢复演练、现场 SOP 与告警闭环。

---

## 7. 可选项(Decision Options for Leadership)

> 说明：以下是“可选项”，不是自动结论。建议领导结合团队与交付风险做选择。

### 选项 1：单栈 `.NET 8 + Minimal APIs`（**默认推荐**）

**适用条件**：

* 团队主力是 C#，希望快速形成可维护的长期资产
* 更看重“稳定可控/风险可控”，策略以“配置/规则表”为主

**拍板后 2–4 周应验收的交付物**（建议）：

* `.NET 8` 工程脚手架（API/Core/Infra/Workers）+ Docker/Compose 一键启动
* 命令/回调幂等、重试、断点恢复、Outbox 的最小闭环
* Mock 设备模拟器 + 端到端链路测试样例

### 选项 2：单栈 `Python 3.11 + FastAPI`（敏捷与动态策略优先）

**适用条件**：

* 策略热更新与快速试错是 P0，且团队具备 Python 生产经验
* 能接受通过更严格的治理（沙箱/审批/审计/回滚/测试）来对冲动态风险

**关键前置**：

* 明确脚本治理红线（隔离执行、资源限制、审批审计、灰度回滚），否则不建议进入生产
