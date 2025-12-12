# Contracts Overview（接口契约概览）

**Scope**: SAP/MES/RCS/WCS/设备接口的字段级契约、样例 payload、错误码与重试/告警策略。所有字段需关联 TraceRef（docs/origin 行号）。

## 通用约定 (Conventions)
- **幂等键 IdempotencyKey**: `TaskId + StepSeq + ContainerId`（如有则加 `AGVJobId`）。  
- **时间戳 Timestamps**: ISO8601 UTC，字段含义：`IssuedAt`（下发），`AckAt`（接收/接单），`CompletedAt`（执行完成）。  
- **单位 Units**: 质量 kg，数量 pcs，长度 mm，时间 ms/s，角度 deg。  
- **错误码 Error Codes**: `code`（字符串），`message`（可双语），`retryable`（bool），`hint`（定位）。  
- **重试/补偿 Retry/Compensation**: 默认指数退避（≤3 次），超出后转人工兜底并告警。  
- **安全 Security**: 传输采用 TLS；敏感字段（人员、位置信息）支持脱敏/审计日志。

## 契约清单 (Artifacts)
- `sap-inbound.md`: SAP ↔ WMS 入库/出库单同步与回执。  
- `rcs-command.md`: WMS → RCS/AGV 行走/搬运指令，下发与确认。  
- `device-telemetry.md`: WCS/设备状态/告警回传（MQTT/SSE）。  
- `mes-orders.md`: MES 工单拉取与投料反馈。  
- `wcs-control.md`: WMS → WCS 启停/模式切换与线体任务下发。

## 样例缺口与来源 (Samples)
- 若供应商未提供样例 payload，需在各文件注明缺口与 ETA，并在此汇总：  
  - MES 样例：待 MES 提供（ETA：待定）  
  - WCS 样例：待供应商提供线体启停/任务样例（ETA：待定）

## TraceRef
- 所有接口需补 `TraceRef: docs/origin/...` 行级引用占位，并在实现时填充。
