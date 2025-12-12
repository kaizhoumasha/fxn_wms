# Task List: Detailed Design Phase（详细设计阶段）

**Branch**: `002-detailed-design`  
**Spec**: `specs/002-detailed-design/spec.md`  
**Plan**: `specs/002-detailed-design/plan.md`

## Dependencies & Order
- Story priority：US1 (P1) → US2 (P1) → US3 (P2)。US1/US2 可并行局部推进，但 US3 依赖前两者的接口/流程命名与采集点。
- Foundation（Phase 1-2）需先完成，确保术语、风险、数据字典基线明确。

## Parallel Examples
- US1 与 US2 不同文件夹（diagrams/ vs contracts/）的任务可并行，例如 T010 与 T020。
- US3 可在 US1/US2 完成主要命名后启动数据采集点设计（T030 与 T021 可交叉确认字段）。

## Implementation Strategy (MVP-first)
- MVP：完成 US1（核心 P1 流程设计包）+ US2（关键接口契约及样例、错误/重试闭环），即可解锁后续联调。
- 扩展：US3 观测与验收脚本，提升可运维性与上线信心。

---

## Phase 1 - Setup
- [ ] T001 统一目录与模板检查（specs/002-detailed-design/），确保 plan.md / contracts / diagrams / validations 结构就绪

## Phase 2 - Foundational
- [ ] T002 补充数据字典与术语表 TraceRef（specs/002-detailed-design/data-model.md）
- [ ] T003 风险与假设登记（含待填实测值 Owner/ETA）（specs/002-detailed-design/validations/assumptions.md）

## Phase 3 - User Story 1 (P1) E2E Flow LLD
- [ ] T010 [US1] 收货/上架/补料/退料/发货主干流程序列图与状态表（含触发/完成条件、异常/补偿）（specs/002-detailed-design/diagrams/inbound-putaway.md）
- [ ] T011 [US1] 补料/退料/内部移库异常与人工兜底路径（锁冲突、任务超时、拒单）（specs/002-detailed-design/validations/exception-handling.md）
- [ ] T012 [US1] 字段/单位/标识键对齐数据字典（StepSeq/TaskId/ContainerId/OrderNo/AGVJobId）（specs/002-detailed-design/data-model.md）
- [ ] T013 [US1] 产出每流程的入口/出口条件与完成判定清单（specs/002-detailed-design/diagrams/inbound-putaway.md）

## Phase 4 - User Story 2 (P1) Integration Contracts
- [ ] T020 [US2] SAP GRN 查询 + 单据创建/更新 + 回执契约与样例补 TraceRef、错误码/重试（specs/002-detailed-design/contracts/sap-inbound.md）
- [ ] T021 [US2] RCS 指令/继续/取消 + 回调/告警对齐现网字段与状态映射，补重试/退避策略（specs/002-detailed-design/contracts/rcs-command.md）
- [ ] T022 [US2] 多设备事件 & 校验接口（流水线/机械臂/拆包/检测）补字段校验、原因码、重试/告警策略（specs/002-detailed-design/contracts/device-telemetry.md）
- [ ] T023 [US2] 跨接口错误码/超时/重试策略矩阵与幂等键规范（specs/002-detailed-design/contracts/README.md）
- [ ] T024 [P] [US2] 收集并登记供应商/现场样例 payload 确认状态（specs/002-detailed-design/contracts/README.md#samples）

## Phase 5 - User Story 3 (P2) Observability & Acceptance
- [ ] T030 [US3] 观测性设计：指标/日志/追踪采集点，含设备链路 p95≤10s 度量口径（specs/002-detailed-design/validations/observability.md）
- [ ] T031 [US3] 验收/演练脚本大纲：每流程 1 主路径 + 1 异常路径，告警阈值与成功判定（specs/002-detailed-design/quickstart.md）
- [ ] T032 [US3] 安全/审计留痕要求落地（鉴权、敏感字段、审计日志保留期）（specs/002-detailed-design/validations/security.md）

## Phase 6 - Polish & Cross-cutting
- [ ] T040 Traceability 复核：所有设计/契约文件补全 docs/origin 行级引用（specs/002-detailed-design/validations/traceability.md）
- [ ] T041 TBD/TODO 清零与术语一致性巡检（specs/002-detailed-design/）
