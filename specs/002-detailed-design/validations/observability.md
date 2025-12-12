# Observability & Acceptance（可观测性与验收）

**Feature**: 002-detailed-design  
**Goal**: 定义指标/日志/追踪的采集点与验收口径，支撑 p95≤10s 链路目标与关键流程验收。

## Metrics（指标）
- **CommandLatency_p95**: WMS 指令下发 → 设备执行完成，p95 ≤10s；采集点：WMS issuedAt、设备 completedAt。  
- **CallbackLag_p95**: RCS 回调/设备事件到达 WMS 延迟，p95 ≤2s；采集点：事件 occurredAt vs ingestAt。  
- **ErrorRate**: 任务失败/告警事件占比（分设备/接口）；阈值：<0.5%/天。  
- **Throughput**: 每小时处理任务数（按场景：收货/上架/补料/退料/发货）。  
- **RetryCount**: 每接口重试次数，阈值：≤3；超出即告警。  

## Logs（日志）
- 必含键：TaskId、OrderNo、ContainerId、AGVJobId、PositionCode、IdempotencyKey、TraceRef。  
- 必含阶段：issued/ack/completed/failed；异常需记录 reasonCode、重试次数、告警 ID。  

## Traces（追踪）
- 关键 span：WMS→RCS 下发、RCS→WMS 回调、WMS→设备校验、设备事件回传。  
- 追踪字段：traceId、spanId、TaskId、stepSeq、PositionCode。  

## Acceptance / 演练
- 每个 P1 流程：至少 1 条主路径 + 1 条异常路径（拒单/超时/告警）演练脚本。  
- 验收判定：指标达标（CommandLatency_p95 ≤10s）、错误率 <0.5%，日志含关键键可检索，告警命中。  

## TraceRef
- TraceRef: docs/origin/... （待补行号）
