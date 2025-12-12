# Specification Quality Checklist: SRS Alignment（SRS 对齐检查）

**Purpose**: Validate that detailed design (spec/plan/contracts/tasks) is aligned with docs/SRS.md requirements  
**Created**: 2025-12-12  
**Feature**: specs/002-detailed-design/spec.md

## Requirement Completeness

- [x] CHK001 是否覆盖 SRS 中所有对外接口（SAP/MES/RCS/WCS/设备）并在设计中指明？【Completeness, Spec §FR-002】
- [x] CHK002 SRS 的收货 GRN 同步步骤（PO/行/批次/数量/供应商）是否在设计/契约中完整反映？【Completeness, contracts/sap-inbound.md】
- [x] CHK003 SRS 所述 RCS 任务生命周期（下发/继续/取消/状态回调/告警）是否全部体现在契约与样例中？【Completeness, contracts/rcs-command.md】
- [x] CHK004 SRS 涉及的多设备（流水线/机械臂/拆包机/检测设备）事件与校验需求是否在契约中覆盖？【Completeness, contracts/device-telemetry.md】

## Requirement Clarity

- [x] CHK005 接口字段是否具备单位/枚举/必填/默认说明（尤其位置码、货架/料箱、任务号、时间戳）？【Clarity, Spec §FR-002】
- [x] CHK006 性能目标（设备指令链路 p95 ≤10s）是否标注度量口径与采集点？【Clarity, Spec §FR-004】
- [x] CHK007 错误码、重试/超时/告警策略是否在各接口契约中明确（SAP/RCS/设备）？【Clarity, contracts/*】
- [x] CHK008 可观测性与验收标准（指标/日志/追踪 + 成功判定）是否与 SRS 中的流程节点一一对应？【Clarity, Spec §SC-004】

## Requirement Consistency

- [x] CHK009 跨文档的标识键/术语（TaskId/OrderNo/ContainerId/AGVJobId/PositionCode）是否一致且与 SRS 描述对应？【Consistency, data-model.md】
- [x] CHK010 状态枚举（accepted/in_progress/completed/failed/exception vs start/outbin/arrive/end/cancel）是否在 RCS 回调与设备事件中保持一致？【Consistency, contracts/rcs-command.md, device-telemetry.md】
- [x] CHK011 设备事件分类（completed/failed/alarm/heartbeat）是否与 RCS/WCS 回调语义一致且无冲突？【Consistency, device-telemetry.md】

## Coverage & Edge Cases

- [x] CHK012 异常/补偿/人工兜底路径（锁冲突、拒单、超时、设备故障）是否覆盖并可追溯到 SRS？【Coverage, Spec §FR-003】
- [x] CHK013 供应商样例缺失时的占位/ETA/最小可行样例是否要求明确？【Coverage, Spec Edge Cases】
- [x] CHK014 安全/审计要求（鉴权、敏感字段、审计留痕）是否在设计/契约中体现？【Coverage, Spec §FR-005】

## Traceability & Assumptions

- [x] CHK015 是否为新增/修改的接口与流程补充了 `docs/origin` 行级 TraceRef 占位？【Traceability】
- [x] CHK016 待补实测值或供应商确认项是否在风险/假设表中登记 Owner/ETA？【Assumptions, validations/assumptions.md】

## Notes

- 未通过项需在 spec/plan/contracts/data-model 中补足后再标记完成；保持 ≥80% 条目包含 TraceRef 或定位到文件/章节。
