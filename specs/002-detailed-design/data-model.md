# Data Model（数据模型）

**Feature**: 002-detailed-design  
**Scope**: 设计产物的实体与关键字段，支持 Traceability、幂等/对账、观测与异常处理。

## Entities

### FlowDesignPackage（流程设计包）
- `FlowId`: 流程标识/名称（对应 docs/origin 行）。  
- `Steps`: 步骤列表（含 StepSeq、主/异常/补偿分支标记）。  
- `Preconditions` / `Postconditions`: 入口/出口条件。  
- `StateDiagramRef`: 状态/时序图引用。  
- `MetricsBinding`: 绑定的指标/日志/追踪点列表。

### IntegrationContract（接口契约）
- `InterfaceId`: 接口唯一标识；类型：SAP/MES/RCS/WCS/Device。  
- `RequestSchema`: 字段表（键名、类型、单位、必填/默认、幂等键）。  
- `ResponseSchema`: 字段表（键名、类型、成功/错误码、重试/超时）。  
- `SamplePayloads`: 请求/响应样例（含来源/供应商确认状态）。  
- `ErrorHandling`: 重试/补偿/告警策略。  
- `TraceRef`: 原始需求行引用。

### CommandMessage（指令消息）
- `TaskId`（WMS 任务号）、`AGVJobId`（RCS 任务号）、`ContainerId`（托盘/箱 ID）、`OrderNo`（业务单号）。  
- `StepSeq`: 步骤序号/分支标记。  
- `Payload`: 与设备/系统交互的字段集合。  
- `Timestamps`: `IssuedAt`、`AckAt`、`CompletedAt`（用于 p95 计算）。  
- `IdempotencyKey`: 幂等键（TaskId + StepSeq + ContainerId）。

### TelemetryEvent（状态/告警事件）
- `EventId`、`Source`（RCS/WCS/Device）  
- `TaskId` / `AGVJobId` / `ContainerId`  
- `EventType`: 状态变更、告警、拒单、超时等  
- `Payload`: 事件字段（含位置、设备、原因码）  
- `OccurredAt` / `IngestedAt`  
- `Severity` 与 `AckPolicy`

### ObservabilityProbe（可观测性探针）
- `MetricName` / `LogFields` / `TraceSpan`  
- `Location`: WMS、RCS、设备侧  
- `SLOTarget`: p95 ≤10s（命令链路），其他按流程定义  
- `CollectionMethod`: 拉取/推送、采样率、窗口

### RiskAssumption（风险与假设）
- `RiskId`、`Description`、`Likelihood`、`Impact`  
- `Owner`、`Mitigation`、`ETA`  
- `Evidence`: 实测或供应商提供材料  
- `TraceRef`: 对应需求行
