# Quickstart（阅读与联调准备）

**Feature**: 002-detailed-design  
**Audience**: 设计/研发/测试/运维、供应商联调人员

## 阅读路径
1) 先读 `spec.md`（用户故事、FR/SC、Clarifications）。  
2) 看 `plan.md`（Technical Context、Phase 计划）。  
3) 查 `research.md`（决策与备选）。  
4) 查 `data-model.md`（实体/字段/幂等/对账键）。  
5) 对应接口查看 `contracts/` 下具体文档与样例。  
6) 若有观测或性能需求，查 `validations/observability.md`；异常/兜底见 `validations/exception-handling.md`；安全与审计见 `validations/security.md`；假设/风险见 `validations/assumptions.md`。

## Traceability（可追溯性）
- 所有字段/流程/接口需标注 `TraceRef` 指向 `docs/origin` 的表/行。  
- 更新或新增契约时，同步补充 TraceRef。

## 契约校验（Pre-integration Checks）
- 样例 payload 过一遍字段约束（必填/单位/枚举/幂等键）。  
- 错误码表需覆盖重复、锁冲突、下游不可用、超时等场景。  
- 重试策略：指数退避 ≤3 次，超出转人工兜底并告警。  
- 性能目标：设备指令链路 p95 ≤10s，确保采集点（Issued→Ack/Completed）一致。

## 观测与验收
- 指标：命令下发/ACK/完成时延；事件处理成功率；错误码分布。  
- 日志：任务号/容器 ID/AGVJobId/IdempotencyKey 必须可检索。  
- 演练脚本（示例）：  
  - 主路径：收货→上架；补料→投料；退料→回库；发货→出库确认。  
  - 异常路径：RCS 拒单/超时；WCS/设备告警（堵塞/机械臂失败）；SAP/MES 不可用重试；校验失败（条码/称重/视觉）。  
  - 验收判定：CommandLatency p95≤10s，错误率<0.5%，日志含关键键可检索，告警命中。
