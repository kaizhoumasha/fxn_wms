# Research Notes（设计调研）

**Feature**: 002-detailed-design  
**Date**: 2025-12-12  
**Context**: 支持 P1 作业流的详细设计包，确保接口契约、性能基线、幂等/对账与观测方案可落地。

## Decisions

### D-01 设备指令链路性能目标（Device Command SLO）
- **Decision**: 设备指令下发到执行完成的链路延迟目标定为 p95 ≤10s（测量区间：WMS 发出指令 → 设备 ACK 完成）。  
- **Rationale**: 符合前期设计假设，可在现有 AGV/RCS/设备链路内实现；成本与风险平衡。  
- **Alternatives**:  
  - 更紧 p95 ≤5s：对老设备/长链路风险高，需新增缓存/边缘协同。  
  - 更宽 p95 ≤15s：降低体验，设备拥塞时延迟可放大。

### D-02 接口协议与回传模式（Command/Telemetry Patterns）
- **Decision**: 命令下发采用 HTTP/REST，同步返回接收状态；状态/事件回传采用 MQTT 或 SSE（由供应商通道支持），要求携带任务 ID 与容器/托盘 ID。  
- **Rationale**: REST 便于幂等键、错误码与重试控制；MQTT/SSE 适合连续状态/告警推送，降低轮询延迟。  
- **Alternatives**:  
  - 全部 REST 轮询：延迟高且易漏报。  
  - gRPC 流式：部分供应商不支持。  
  - 专用 MQ 队列：需额外基础设施与运维成本。

### D-03 幂等与对账关键字段（Idempotency & Reconciliation Keys）
- **Decision**: 标准化字段：`TaskId`（WMS 任务号）、`OrderNo`（业务单号/ASN/SO）、`ContainerId`（托盘/周转箱 ID）、`AGVJobId`（RCS 下发任务号）、`StepSeq`（步骤序号）、`TraceRef`（docs/origin 行级引用）。  
- **Rationale**: 支撑跨系统去重、对账与追溯；覆盖业务单据与设备执行链路。  
- **Alternatives**:  
  - 仅用 TaskId：跨系统映射不足，难以对账。  
  - 仅用订单号：无法区分并发步骤或设备任务实例。
