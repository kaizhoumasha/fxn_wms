# P9 WES 系统架构设计 (System Architecture)

## 1. 架构概览 (Architectural Overview)

休斯顿 P9 **仓储执行系统 (WES)** 设计为一个 **解耦的、事件驱动的控制中台 (Decoupled, Event-Driven Control Middleware)**。它是连接上层业务逻辑 (SAP/WMS) 与底层物理执行 (Hardware) 的 "执行大脑"。

### 1.1 核心原则 (Core Principles)
- **解耦 (Decoupling)**: WES 不依赖于硬件的内部实现。它发布标准的 **意图指令 (Intent-based Commands)**（例如 "移动单元"），而不是设备特定的指令（例如 "电机 A 旋转"）。
- **无状态执行 (Stateless Execution)**: WES 维护 **瞬态执行状态 (Transient Execution State)**，但依赖企业级 WMS 作为库存的 **唯一事实来源 (Single Source of Truth)**。
- **插件化架构 (Plugin Architecture)**: 硬件驱动程序以 **适配器 (Adapters)** 形式实现，允许更换不同的硬件供应商而无需更改 WES 核心逻辑。

## 2. 系统分层 (System Layering)

系统划分为三个严格的逻辑层：

### L1 - 北向层 (Northbound Layer - Business Integration)
**职责**: 与 **上游系统 (Upstream Systems)** (SAP / Enterprise WMS) 交互。
- **入站 (Inbound)**: 提供 REST API 接收 `Order_Ingest` (收货通知单 GRNs, 工单 Work Orders) 和 `Master_Data`。
- **出站 (Outbound)**: 通过 Webhooks/API 调用 `Confirm_Inventory` (上架/发料) 和 `Sync_Status`。
- **关键组件**:
  - `OrderController`: 验证并接收业务单据。
  - `WmsAdapter`: 标准化客户端，用于 WMS 库存查询和预留。

### L2 - 核心层 (Core Layer - The Brain)
**职责**: 策略执行、任务编排和状态管理。
- **策略引擎 (Strategy Engine)**:
  - `BinningStrategy`: 基于物料尺寸和规则确定 **目标箱位 (Target Bin)**。
  - `RoutingStrategy`: 计算最优路径 (**冷热区 Hot/Cold Zones**)。
  - `SchedulingStrategy`: **先失效先出 (FEFO)** 和优先级管理。
- **编排引擎 (Orchestration Engine)**:
  - `TaskDecomposer`: 将单个 **订单 (Order)** 拆解为多个 **原子任务 (Atomic Tasks)**。
  - `TaskManager`: 管理任务的生命周期 (`Pending` 挂起 -> `Dispatched` 已下发 -> `Completed` 完成)。
  - `StateTracker`: 维护仓库现场的实时 **"数字孪生" (Digital Twin)**。

### L3 - 南向层 (Southbound Layer - Hardware Abstraction)
**职责**: 将标准 WES 指令转换为特定于硬件的协议。
- **硬件网关 (Hardware Gateway - The Standard)**:
  - 定义内部逻辑使用的 **通用硬件接口 (Universal Hardware Interface - UHI)**。
  - *详见 `hardware_interface_standard.md`。*
- **协议适配器 (Protocol Adapters)**:
  - `RcsAdapter`: 将 UHI 指令转换为 AGV 调度调用 (HTTP/TCP)。
  - `EcsAdapter`: 将 UHI 指令转换为 PLC/机器人指令 (Modbus/OPC UA/HTTP)。
  - `PdaAdapter`: 适配手持设备以处理人工任务。

## 3. 数据流与边界 (Data Flow & Boundaries)

### 3.1 WES 与 WMS 边界
- **WMS 拥有**: "我们有什么" (库存数量、成本、所有者)。
- **WES 拥有**: "它正在哪里移动" (实时坐标、AGV 状态、瞬态箱位)。
- **交互**:
  1. WES 在开始任务前向 WMS 请求 **库存预留 (Inventory Reservation)**。
  2. WES 在任务完成后向 WMS 确认 **物理移动 (Physical Movement)**。

### 3.2 WES 与 硬件边界
- **WES 指令**: "将栈板 P1 从 A 运输到 B"。
- **硬件执行**: "锁定路径，转向 AGV 01，举升 P1，导航到 B，放下 P1"。
- **抽象**: WES 不需要知道 AGV *如何* 移动，只需要知道任务是被接受、进行中还是已完成。

### 3.3 地图与位置同步 (Map & Location Synchronization)
- **RCS**: 维护物理导航地图 (Physical Map)，包含精确的坐标 (X, Y) 和路径点 (Waypoints)。
- **WES**: 维护逻辑位置地图 (Logical Topology)，仅关注 **关键节点 (Nodes)** (例如 "Dock_01", "Rack_A_01")。
- **同步机制**:
  - 系统初始化时，WES 导入 RCS 的 **地码表 (Location Codes)**，建立 `Logical_ID` 到 `Physical_Code` 的映射。
  - 任务下发时，WES 使用 `Logical_ID`，由 `RcsAdapter` 转换为 RCS 识别的 `Physical_Code`。

## 4. 部署模型 (Deployment Model)
- **容器化 (Containerized)**: 基于 Docker 部署核心、数据库和适配器。
- **边缘就绪 (Edge-Ready)**: 支持在本地服务器运行，确保硬件控制的 **低延迟 (Low Latency)**。
- **数据库**:
  - **业务数据库 (Operational DB - PostgreSQL)**: 存储活动任务、策略和配置。
  - **缓存 (Cache - Redis)**: 高速状态跟踪和分布式锁。
