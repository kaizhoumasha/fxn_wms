# Traceability Checklist（行级追溯占位）

**Feature**: 002-detailed-design  
**Goal**: 确保所有设计/契约文件补充 `docs/origin` 行级 TraceRef 占位，并在实现时填充。

## 覆盖范围
- `spec.md`（FR/SC/User Stories）  
- `plan.md`（Phase/Technical Context）  
- `tasks.md`（任务源自 Spec/Plan，需可追溯）  
- `contracts/*.md`（SAP/MES/RCS/WCS/设备）  
- `data-model.md`（实体/字段/标识键/单位/枚举）  
- `diagrams/*.md`（流程/序列/状态）  
- `validations/*`（observability/exception/security/assumptions）  
- `quickstart.md`（验收/演练脚本）

## 要求
- 每个新增/修改的接口、字段、流程步骤需注明 TraceRef: `docs/origin/<file>#row...`；暂无行号时标占位，联调后补齐。  
- 保持与原始 SRS/需求清单的双向映射。
