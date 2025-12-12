# Design Plan: 概要设计阶段启动 - 休斯顿 P9 WMS

**Branch**: `001-high-level-design` | **Date**: 2025-12-11 | **Spec**: specs/001-high-level-design/spec.md
**Input**: Feature specification from `/specs/001-high-level-design/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. Align all content with the Constitution: design-first, traceable to `docs/origin/`, WMS as调度中台 (no PLC/IO coding), bilingual key terms.

## Summary

完成概要设计：输出覆盖入库、存储、SMT 发料与设备协同的高层蓝图、接口矩阵与异常兜底方案。重点是以 WMS 调度中台角色编排 SAP/MES/RCS/WCS/设备，明确模块责任、数据标识、协议/负载字段及供应商配合事项（点表、模拟、联调支持），并给出容量/性能基线及验证路径。

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Documentation phase; downstream实现面向 Python 3.11+ / .NET 8 兼容  
**Primary Dependencies**: 设计依赖 SAP/MES/RCS/WCS 接口规范，设备协议 Modbus/MQTT/SSE/WebSocket/HTTP，供应商提供点表/模拟器  
**Storage**: N/A（本阶段仅设计）；后续实施预期关系型/时序库组合，待详细设计确认  
**Testing**: 设计验证通过联调/模拟、时序走查、容量假设验证（无代码测试）  
**Target Platform**: 工厂私有云/本地服务器；终端为工业 PC/PDA，工业 Wi-Fi/5G 网络  
**Project Type**: 设计交付（WMS 后端与设备调度方案），非代码实现阶段  
**Performance Goals**: AGV 指令 95% ≤10s；入库高峰 ≥60 栈板/小时；双语可用率 ≥99%；容量基线基于现网测算  
**Constraints**: WMS 仅调度中台，不做 PLC/IO；需遵循既有协议与 RCS/设备能力；必须双语；需供应商提供接口/点表/模拟  
**Scale/Scope**: 范围覆盖入库、存储、SMT 发料、设备协同（AGV/E-AGV/CTU、流水线、机械臂、拆箱/装 tray/叠栈设备）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Lifecycle: Spec/Clarify completed; plan仅产出设计文档（通过）。
- Traceability: 需在各工件引用 docs/origin/ 具体文件与章节/行（待执行）。
- Integration Boundaries: 明确调度中台、不做 PLC；协议 Modbus/MQTT/SSE/WebSocket/HTTP；需供应商点表/模拟支持（通过，需在工件落实）。
- Feasibility: 方案需匹配 AGV/RCS/设备能力与 Python/.Net Core 约束，依据现有接口文档（通过，待在合同/序列图中验证）。
- Language & Terminology: 中文为主，关键术语双语（通过）。

Gate Status: 允许继续 Phase 0（无阻断项，需在后续工件中落实追溯与协议细节）。

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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

**Structure Decision**: 使用上述文档结构；integration/ 作为共享交付（若后续落地，按实际创建）。

## Source References & Traceability Plan

- docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx（后续在各工件标注具体 Sheet/Row）
- docs/SRS.md（按段落标注）
- 其他外部接口规范：AGV API SPEC、RCS/WCS/设备协议（按供应商提供的版本记录）
- Traceability 方法：在 diagrams/、contracts/、plan.md 摘要处标注 “文件 + Sheet/Row/段落”。

### Traceability Mapping (User Stories / FR → Source)

| Item | SRS Reference | Origin Reference |
| ---- | ------------- | ---------------- |
| US1 / FR-001 / FR-002 (蓝图、流程) | docs/SRS.md §3.2 收货入库；§3.3.1~3.3.3 SMT 收货/存储/发料；§3.4 特殊物料；§3.5 机构件物流 | docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx：Sheet “码头到收货暂存区” rows 3-21；Sheet “收货暂存区到料盘装箱区” rows 3-23；Sheet “料盘装箱区到SMT作业区” rows 3-38；Sheet “生产退料到SMT清点x-ray&LCR” rows 3-22 |
| US2 / FR-003 (接口矩阵) | docs/SRS.md §3.7.5 接口可靠性保障；§3.2/§3.3 各流程接口描述 | Origin 同上表，重点：Sheet “码头到收货暂存区” rows 3-21（GRN/收货链路）；Sheet “收货暂存区到料盘装箱区” rows 3-23（装箱链路）；Sheet “料盘装箱区到SMT作业区” rows 3-38（发料链路） |
| US3 / FR-005/FR-006/FR-009 (异常、容量/可观察性) | docs/SRS.md §3.7 系统控制与可靠性；§3.8 核心算法（容量/策略）；§3.2/§3.3 异常说明 | Origin：Sheet “码头到收货暂存区” rows 22-36（异常/要求），Sheet “收货暂存区到料盘装箱区” rows 17-23，Sheet “料盘装箱区到SMT作业区” rows 30-38，Sheet “生产退料到SMT清点x-ray&LCR” rows 3-22；现场历史峰值数据（待采集并填入 validations/assumptions.md） |

## Bilingual Glossary (Key Terms)

- 调度中台 (Dispatching Platform)
- WMS (Warehouse Management System)
- RCS (Robot Control System)
- WCS (Warehouse Control System)
- AGV / E-AGV / CTU (Automated Guided Vehicle / Enhanced AGV / Container Transfer Unit)
- PLC (Programmable Logic Controller)
- 工控机 (Industrial PC, IPC)
- Modbus / MQTT / SSE / WebSocket / HTTP
- SAP / MES
- IQC (Incoming Quality Control)

## Security & Compliance
- **Data classification & audit**: 参考 SAP/MES 基线，划分数据级别（公开/内部/敏感），审计留存周期：默认 ≥ 1 年（待现场确认）；访问控制原则：最小权限、按角色/域分权。
- **Auth/Z & crypto**: SAP/MES/RCS/WCS/设备的鉴权方式（Token/API Key/证书）需在 contracts/ 指定；传输必须 TLS；日志需脱敏（不含敏感字段值）。
- **Traceability & retention**: TraceID/CorrelationID 贯穿接口；日志/告警保留期与审计要求一致（默认 ≥ 1 年），记录在 validations/assumptions.md。
- **Alignment**: contracts/ 列出 per-system auth/超时/重试/错误码映射；validations/assumptions.md 列出验证证据及 Owner/ETA。

## Environment & Sandbox Topology
- **Envs**: Dev / 联调 / 预生产 / 生产；每个 env 定义网络/ACL 边界、可用外部系统（SAP/MES/RCS/WCS/设备）与模拟器。
- **Endpoints & access**: 外部接口列表按 env 记录（不含敏感信息）；证书/密钥管理须在安全存储中维护（不在文档中展示）。
- **Readiness criteria**: 联调前需具备：RCS 地图/设备清单、点表/接口模拟器、SAP/MES 沙箱凭据、告警/监控接入策略。

### Environment Matrix (示例占位，填充真实信息时补完)
| Env | Purpose | Network/ACL | External Systems | Data Sets/Simulators | Notes |
|-----|---------|-------------|------------------|----------------------|-------|
| Dev | 开发自测 | 内网，仅模拟器 | 模拟 SAP/MES/RCS/WCS/设备 | 必需：接口模拟器、点表样例 | 不含真实凭据 |
| 联调 | 与外部联调 | 受限 ACL（白名单） | SAP/MES 沙箱，RCS/WCS 测试 | 模拟器 + 部分真机/回放 | 日志脱敏 |
| 预生产 | 演练/性能 | 与生产近似 ACL | SAP/MES 准生产，RCS/WCS 准生产 | 接近真实数据或脱敏回放 | 验证告警/兜底 |
| 生产 | 上线 | 正式 ACL | 全部正式 | 正式数据 | 严格审计/留存 |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Risk List (US1 Scope)

| 风险 | 影响 | 缓解措施 |
| ---- | ---- | ---- |
| 模块职责重叠/空白 | 责任不清导致返工 | US1 蓝图评审；在 diagrams/us1-flows.md 标注责任分界 |
| TraceID/标识不一致 | 追溯失败、幂等冲突 | 在 data-model.md 定义 ID/TraceID；接口契约注明幂等键 |
| 供应商接口/点表缺口 | 无法编排设备 | contracts/integration-contracts.md 记录供应商交付要求；缺口列入评审 |
| 网络/协议差异 | 时序/可靠性不足 | 在 contracts 中声明协议/QoS/重试；validations/assumptions.md 设计验证 |
| 容量基线不符合现网 | 性能风险 | validations/assumptions.md 基于历史数据/仿真；演练脚本准备 |

## Review Packet (for sign-off)
- plan.md, research.md, data-model.md, contracts/, diagrams/ (us1-flows.md, us2-sequence.md), validations/ (assumptions.md, us2-scenarios.md, us3-observability.md), integration/playbooks/us3-fallback.md, tasks.md。
- Traceability: plan.md Traceability Mapping 表、contracts Traceability、diagrams 注释、validations/assumptions.md SC 对齐。
