# Design Plan: Detailed Design Phase（详细设计阶段）

**Branch**: `002-detailed-design` | **Date**: 2025-12-12 | **Spec**: specs/002-detailed-design/spec.md  
**Input**: Feature specification from `/specs/002-detailed-design/spec.md`

**Note**: 遵循 Constitution：设计优先、追溯到 `docs/origin/`、WMS 为调度中台（不做 PLC/IO）、关键术语中英双语。

## Summary

交付 P1 端到端作业（收货/上架/补料/退料/发货）的可执行详细设计包，含接口契约、异常/补偿、可观测性与安全合规设计。性能设计目标：设备指令下发到执行完成 p95 ≤10s。所有设计元素保持对 `docs/origin` 的行级追溯。

## Technical Context

**Language/Version**: Python 3.11 / .NET 8（目标实现栈；本阶段仅文档）  
**Primary Dependencies**: 文档/图表：Mermaid、PlantUML；接口协议：HTTP/REST + MQTT/SSE（设备/供应商回传）  
**Storage**: 本阶段无代码存储；数据字典/契约以文档形式，后续实现预计 PostgreSQL（假设，需在实现阶段确认）  
**Testing**: 设计自检 + 契约样例校验（联调前）  
**Target Platform**: Server-side WMS（Linux），设备控制由供应商工控机负责  
**Project Type**: Scheduling Middle Platform 设计文档  
**Performance Goals**: 设备指令下发到执行完成 p95 ≤10s（链路设计目标）  
**Constraints**: 不做 PLC/IO；遵循供应商协议能力；保持 Traceability 行级引用；关键术语双语  
**Scale/Scope**: 覆盖 P1 作业流（收货/上架/补料/退料/发货）及对应接口、观测与安全要求

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Lifecycle: PASS — Spec/Clarify 完成，计划仅产出设计文档与契约。  
- Traceability: PASS — 设计元素将保持 `docs/origin` 行级引用。  
- Integration Boundaries: PASS — WMS 为调度中台，不做 PLC/IO；接口依协议（HTTP/MQTT/SSE），供应商负责点表/模拟。  
- Feasibility: PASS — 方案可在 Python/.NET 栈与现有 AGV/RCS/设备协议能力内落地；需供应商样例确认。  
- Language & Terminology: PASS — 中文主导，关键术语双语，术语表同步更新。  

## Project Structure

### Documentation (this feature)

```text
specs/002-detailed-design/
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 design research
├── data-model.md        # Data dictionary, keys, reconciliation fields
├── quickstart.md        # How to read/run design simulations or mocks
├── contracts/           # Interface definitions (API/protocol payloads, point lists)
├── diagrams/            # Mermaid/PlantUML flows, sequence diagrams
├── validations/         # Capacity/performance assumptions, observability probes
└── tasks.md             # /speckit.tasks output (not created by /speckit.plan)
```

### Integration Assets

```text
integration/
├── vendor-handovers/    # Responsibilities, simulators, point tables
└── playbooks/           # Joint test/rollback/runbooks, manual fallback flows
```

**Structure Decision**: 采用上述目录，当前分支已存在 `spec.md`、`plan.md`、`checklists/`；本次将新增 `research.md`、`data-model.md`、`contracts/`、`quickstart.md`，并按需补充 `diagrams/` 与 `validations/`。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |

当前无章程偏离，表格留空。

## Phase Plan

### Phase 0 - Research
- R0.1 验证设备指令链路的 p95 ≤10s 目标的度量口径与采集点；明确采样位置（WMS→设备 ACK）。  
- R0.2 供应商接口协议组合：命令下发 HTTP/REST，状态/事件回传 MQTT/SSE；记录错误码与重试模式最佳实践。  
- R0.3 数据对账/幂等关键字段（任务号、订单号、容器/托盘 ID、AGV 任务 ID）及跨系统映射。

### Phase 1 - Design & Contracts
- D1.1 产出 `data-model.md`：实体/字段/关系、状态与幂等/对账键。  
- D1.2 产出 `contracts/`：SAP/MES/RCS/WCS/设备接口的请求/响应字段表、样例 payload、错误码与重试/补偿策略。  
- D1.3 产出 `quickstart.md`：阅读路径、如何复用契约样例与验收脚本思路。  
- D1.4 执行 `.specify/scripts/bash/update-agent-context.sh codex` 更新 Agent 语境。  
- D1.5 设计完成后复核 Constitution Check（Traceability、边界、可行性、双语）。

### Phase 2 - （后续任务分解与实现规划，当前指令到此为止）
本次工作在 Phase 1 完成后停止，留待 `/speckit.tasks` 与实现阶段继续。
