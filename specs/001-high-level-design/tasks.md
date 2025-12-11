# Tasks: 概要设计阶段启动 - 休斯顿 P9 WMS

**Input**: Design documents from `/specs/001-high-level-design/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md  
**Validations**: Traceability to docs/origin; integration boundary (调度中台，不做 PLC/IO；协议经工控机 Modbus/MQTT/SSE/WebSocket/HTTP；供应商提供点表/模拟器)；容量/性能基线基于现网测算。

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create/verify design folders: specs/001-high-level-design/diagrams, specs/001-high-level-design/validations, specs/001-high-level-design/contracts (ensure present)
- [ ] T002 Collect source references (docs/origin/*.xlsx/.docx/.pdf, docs/SRS.md) and note Sheet/Row/段落 mapping in plan.md
- [ ] T003 Maintain bilingual glossary section in plan.md and quickstart.md for new terms

## Phase 2: Traceability & Inputs (Blocking)

- [ ] T004 Map spec user stories and FRs to docs/origin citations in plan.md (file + Sheet/Row/段落)
- [ ] T005 Gather vendor inputs: point tables/field lists, protocol (Modbus/MQTT/SSE/WebSocket/HTTP) details, simulators or recorded payloads; summarize in contracts/integration-contracts.md
- [ ] T006 Capture initial capacity/performance assumptions and validation approach in validations/ (e.g., AGV 95%≤10s, ≥60 栈板/小时) with data sources from research.md

## Phase 3: User Story 1 - 构建端到端方案蓝图 (Priority: P1) 🎯 MVP

**Goal**: 高层蓝图覆盖入库、存储、SMT 发料、设备协同，模块职责与边界清晰。  
**Independent Review**: 蓝图能单独评审，所有主流程有模块/责任映射且无冲突。

### Deliverables

- [ ] T010 [P] [US1] Draft E2E流程与责任分界时序/流程图 (diagrams/) for inbound/storage/SMT supply
- [ ] T011 [P] [US1] Update data-model.md with modules and their inputs/outputs/dependencies
- [ ] T012 [US1] Add traceability annotations (docs/origin Sheet/Row/段落) to diagrams and plan.md summary
- [ ] T013 [US1] Compile risk list for职责冲突/流程缺口与缓解措施 in plan.md

### Validations for User Story 1 (OPTIONAL)

- [ ] T014 [P] [US1] Traceability check: spec ↔ plan ↔ diagrams mapped to docs/origin

**Checkpoint**: US1 reviewed;模块/责任分界无冲突且可追溯。

## Phase 4: User Story 2 - 明确跨系统接口契约 (Priority: P2)

**Goal**: SAP/MES/RCS/WCS/设备接口矩阵与时序完整，协议/字段/幂等/错误/供应商责任清晰。  
**Independent Review**: 每个交互有触发、负载、频率、错误与兜底定义，可模拟/验收。

### Deliverables

- [ ] T020 [P] [US2] Expand contracts/integration-contracts.md with per-system payloads, keys, error codes, retries, QoS
- [ ] T021 [P] [US2] Add sequence diagrams for key interactions (e.g., 收货→IQC→上架, 发料→补料→退料) to diagrams/
- [ ] T022 [US2] Document vendor handover requirements (point tables, simulators, manual fallback) in contracts/ and quickstart.md
- [ ] T023 [US2] Update data-model.md with contract-to-entity field mappings (IDs, reconciliation fields)

### Validations for User Story 2 (OPTIONAL)

- [ ] T024 [P] [US2] Traceability check: contracts/diagrams to spec FR-003 and docs/origin
- [ ] T025 [P] [US2] Scenario validation using sample payloads/simulators (if available) recorded in validations/

**Checkpoint**: US2 reviewed;接口矩阵可演示/走查且可追溯。

## Phase 5: User Story 3 - 风险与可验证性基线 (Priority: P3)

**Goal**: 容量/性能基线、可观察性与异常兜底策略明确，可用于联调与演练。  
**Independent Review**: 验证方法、告警/兜底路径覆盖主要作业；可执行演练。

### Deliverables

- [ ] T030 [P] [US3] Document capacity/performance assumptions and validation scripts/steps in validations/ (cite data sources)
- [ ] T031 [P] [US3] Define observability signals and alert thresholds for key paths in validations/ (AGV tasks, interface latency)
- [ ] T032 [P] [US3] Add fallback/rollback playbooks to integration/playbooks/ for top exceptions (设备离线、接口超时、库容超限)
- [ ] T033 [US3] Update data-model.md with exception handling states/locks and link to contracts/ error codes

### Validations for User Story 3 (OPTIONAL)

- [ ] T034 [P] [US3] Traceability check: validations/playbooks to FR-005/FR-006/FR-009 and docs/origin

**Checkpoint**: US3 reviewed;容量/可观察性/兜底方案可用于演练。

## Phase N: Cross-Cutting & Polish

- [ ] T100 [P] Consolidate glossary and bilingual annotations across plan.md, quickstart.md, contracts/
- [ ] T101 [P] Ensure all artifacts include docs/origin traceability (Sheet/Row/段落) before sign-off
- [ ] T102 [P] Align validations/ with SC metrics (SC-001..SC-004) and record evidence sources
- [ ] T103 [P] Prepare review packet (plan/research/data-model/contracts/diagrams/validations) for stakeholder sign-off

## Dependencies & Execution Order

- Setup (Phase 1) → Traceability & Inputs (Phase 2) → US1 (P1) → US2 (P2) → US3 (P3) → Cross-Cutting.
- Stories are independent after Phase 2; prioritize US1 as MVP.

## Parallel Opportunities

- Tasks with [P] can run in parallel when touching different files (e.g., diagrams vs data-model vs contracts).
- Different stories can proceed in parallel after Phase 2 if staffing allows.

## Implementation Strategy

- MVP: Complete US1 (蓝图+责任分界) then review.
- Incremental: Add US2 接口矩阵与供应商交互 → US3 容量/可观察性与兜底演练。
