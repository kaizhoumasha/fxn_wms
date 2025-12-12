# Integration Contract Requirements Quality Checklist

**Purpose**: Validate integration/接口契约要求的完整性、清晰度与可验证性（发布前正式 gate）  
**Created**: 2025-12-11  
**Feature**: specs/001-high-level-design/spec.md (FR-003/US2 为主)

## Requirement Completeness

- [ ] CHK001 Are all primary flows (收货→上架、发料/补料、退料) covered with interface requirements for SAP/MES/RCS/WCS/设备？[Completeness, Spec §FR-003]
- [ ] CHK002 Are error/异常场景 requirements present for each system (超时、设备不可用、幂等冲突、版本不匹配)？[Completeness, Spec §FR-003, contracts/]
- [ ] CHK003 Are vendor deliverables (点表/字段、协议、模拟器、错误码表、QoS) explicitly required per system？[Completeness, contracts/integration-contracts.md]
- [ ] CHK004 Are retry/改派/人工兜底 requirements included for all external calls and任务派发？[Completeness, Spec §FR-003, playbooks/us3-fallback]

## Requirement Clarity

- [ ] CHK005 Are keys/幂等字段 (TaskID/CommandID/PO+Line/GRN/TraceID/MapVersion) explicitly defined and unambiguous？[Clarity, contracts/, data-model.md]
- [ ] CHK006 Are payload字段（必填/可选、枚举、数值范围） specified for SAP/MES/RCS/WCS/设备消息？[Clarity, contracts/]
- [ ] CHK007 Are protocol, auth, timeout, retry/backoff, QoS expectations stated per system？[Clarity, contracts/]
- [ ] CHK008 Is TraceID/CorrelationID propagation required end-to-end (SAP/MES/RCS/WCS/设备)？[Clarity, contracts/, Spec §FR-003]

## Requirement Consistency

- [ ] CHK009 Are interface requirements consistent with module responsibilities in plan/diagrams (no overlap/空白)? [Consistency, plan.md Traceability Mapping, diagrams/us1-flows.md, us2-sequence.md]
- [ ] CHK010 Are error code categories aligned across systems (通信/业务/设备/数据) with mapping rules？[Consistency, contracts/]
- [ ] CHK011 Are retry/幂等 rules compatible with data-model IDs and inventory/任务状态机？[Consistency, data-model.md, contracts/]

## Acceptance Criteria Quality / Measurability

- [ ] CHK012 Are measurable thresholds defined for interface success率/时延/QoS where required (e.g., success ≥99%，下发→确认 p95 ≤10s)？[Acceptance Criteria, validations/assumptions.md]
- [ ] CHK013 Are acceptance criteria for message completeness (必填字段、校验规则) stated so they can be objectively checked？[Acceptance Criteria, contracts/]

## Scenario & Edge Coverage

- [ ] CHK014 Are exception/recovery flows required for device offline、拥塞、接口超时、版本不匹配、部分成功？[Coverage, playbooks/us3-fallback.md]
- [ ] CHK015 Are fallback paths for人工接管/改派 documented as requirements (not just playbook steps)？[Coverage, Spec §FR-005, playbooks/us3-fallback.md]
- [ ] CHK016 Are versioning/兼容性 requirements specified (协议版本、地图版本、点表版本)？[Edge Case, contracts/]
- [ ] CHK017 Are sequencing/ordering requirements for关键流程（收货→IQC→上架；发料→补料→退料） documented with pre/post conditions？[Coverage, diagrams/us2-sequence.md]

## Dependencies & Assumptions

- [ ] CHK018 Are external dependencies (SAP/MES auth/节流、RCS 地码/设备清单、WCS 事件流、设备点表) enumerated with readiness gates before go-live？[Dependencies, contracts/, plan.md]
- [ ] CHK019 Are assumptions about data availability/质量（GRN/BOM/地码/六合一码/点表） explicitly recorded with validation steps？[Assumption, plan.md, contracts/]

## Ambiguities & Conflicts

- [ ] CHK020 Are any vague terms (e.g., “及时/快速/可靠”) replaced with quantified criteria, or flagged for clarification？[Ambiguity, validations/assumptions.md]
- [ ] CHK021 Are potential conflicts between SAP/MES quantities vs. WMS inventory states addressed (source of truth, reconciliation rules)？[Conflict, data-model.md, contracts/]
