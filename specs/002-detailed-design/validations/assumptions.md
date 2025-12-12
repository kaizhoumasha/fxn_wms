# Assumptions & Risks（假设与风险）

**Feature**: 002-detailed-design  
**Purpose**: 记录待补实测值/供应商确认项，指派 Owner/ETA。

| Item | Status | Owner | ETA | Notes |
|------|--------|-------|-----|-------|
| 设备链路实测 p95（Issued→Completed） | 待采集 | 联调负责人 | 待定 | TraceRef: docs/origin/... |
| 供应商样例 payload（SAP/MES/RCS/WCS/设备） | 部分 | 集成负责人 | 待定 | 在 contracts/README.md 标注来源/缺口 |
| WCS/设备告警 reasonCode 清单 | 待补全 | 设备供应商 | 待定 | 需对齐 device-telemetry.md |
| 安全/审计留痕保留期 | 待确认 | 安全负责人 | 待定 | 在 contracts/README.md 和 validations/security.md 体现 |

> 更新时保持 TraceRef 行级引用，并同步到风险/任务。
