# Security & Audit（安全与审计）

**Feature**: 002-detailed-design  
**Scope**: 鉴权/权限、敏感字段处理、审计留痕。

## Authentication & Authorization
- 接口统一 Token/Bearer；支持设备/系统级凭证。  
- 关键操作（任务下发/取消、异常兜底）需鉴权并记录操作者/系统标识。  

## Data Protection
- 敏感字段（人员、位置、设备标识、物料批次）传输需 TLS；日志可脱敏显示。  
- 审计日志保留期：待确认（见 assumptions），需在实现期配置。  

## Audit Logging
- 必含：操作人/系统、时间、动作、对象（TaskId/OrderNo/ContainerId/PositionCode）、结果、reasonCode、TraceRef。  
- 异常/补偿/人工兜底需写审计日志。  

## TraceRef
- TraceRef: docs/origin/... （待补行号）
