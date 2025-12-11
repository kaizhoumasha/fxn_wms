---
description: "Task list template for feature design delivery"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`  
**Prerequisites**: plan.md (required), spec.md (user stories), research.md, data-model.md, contracts/, diagrams/  
**Validations**: Add validation tasks only if requested (capacity/performance, traceability audit, observability probes, vendor simulations).

**Organization**: Tasks are grouped by user story to enable independent delivery and review of each slice.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Design docs**: `specs/[###-feature-name]/` (plan.md, research.md, data-model.md, quickstart.md, contracts/, diagrams/, validations/, tasks.md)
- **Integration assets**: `integration/vendor-handovers/`, `integration/playbooks/` (if used for shared assets)
- If code work is required, state the real paths instead of using generic placeholders.

<!-- ============================================================================
IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
The /speckit.tasks command MUST replace these with actual tasks based on:
- User stories from spec.md (with priorities)
- Feature requirements from plan.md
- Entities from data-model.md
- Endpoints/protocols from contracts/
Tasks MUST be organized by user story so each story can be delivered and reviewed independently.
============================================================================ -->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure design workspace and inputs are ready

- [ ] T001 Create/verify design folder structure (plan.md, research.md, data-model.md, contracts/, diagrams/, validations/)
- [ ] T002 Collect and cite source docs from docs/origin/ with references noted in plan.md
- [ ] T003 Maintain glossary and bilingual key terms section for this feature

---

## Phase 2: Traceability & Inputs (Blocking)

**Purpose**: Establish mapping to original requirements and integration constraints

- [ ] T004 Map spec user stories to docs/origin references (sheet + row/section) in plan.md
- [ ] T005 Gather protocol/point-table details from vendors (Modbus/MQTT/SSE/WebSocket/HTTP), note responsibilities in contracts/vendor-handovers
- [ ] T006 Capture constraints and initial capacity/performance assumptions in validations/

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Review**: [How to verify this story works on its own]

### Deliverables

- [ ] T010 [P] [US1] Flow and sequence diagrams in diagrams/ for the end-to-end path
- [ ] T011 [P] [US1] Data dictionary & identifiers in data-model.md (keys, reconciliation fields)
- [ ] T012 [P] [US1] Interface/Protocol contract in contracts/ (payloads, triggers, QoS, errors)
- [ ] T013 [US1] Vendor handover notes: responsibilities, simulators, manual fallback steps
- [ ] T014 [US1] Capacity/performance/observability assumptions in validations/ (if requested)

### Validations for User Story 1 (OPTIONAL - include only if requested)

- [ ] T015 [P] [US1] Traceability check: spec ↔ plan ↔ contracts/diagrams mapped to docs/origin
- [ ] T016 [P] [US1] Scenario validation: run/mock sequence against vendor simulator or sample payloads

**Checkpoint**: User Story 1 design reviewed and traceable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Review**: [How to verify this story works on its own]

### Deliverables

- [ ] T020 [P] [US2] Flow/sequence diagrams in diagrams/
- [ ] T021 [P] [US2] Data dictionary updates in data-model.md
- [ ] T022 [P] [US2] Interface/Protocol contract in contracts/ (payloads, triggers, errors)
- [ ] T023 [US2] Vendor handover notes and fallback handling
- [ ] T024 [US2] Capacity/performance/observability updates in validations/ (if requested)

### Validations for User Story 2 (OPTIONAL)

- [ ] T025 [P] [US2] Traceability check vs docs/origin
- [ ] T026 [P] [US2] Scenario validation with sample payloads/simulators

**Checkpoint**: User Story 2 design reviewed and traceable independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Review**: [How to verify this story works on its own]

### Deliverables

- [ ] T030 [P] [US3] Flow/sequence diagrams in diagrams/
- [ ] T031 [P] [US3] Data dictionary updates in data-model.md
- [ ] T032 [P] [US3] Interface/Protocol contract in contracts/
- [ ] T033 [US3] Vendor handover notes and fallback handling
- [ ] T034 [US3] Capacity/performance/observability updates in validations/ (if requested)

### Validations for User Story 3 (OPTIONAL)

- [ ] T035 [P] [US3] Traceability check vs docs/origin
- [ ] T036 [P] [US3] Scenario validation with sample payloads/simulators

**Checkpoint**: User Story 3 design reviewed and traceable independently

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Cross-Cutting & Polish

**Purpose**: Items spanning multiple stories

- [ ] T100 [P] Consolidate glossary and bilingual annotations across artifacts
- [ ] T101 [P] Risk register and fallback/rollback playbooks in integration/playbooks/
- [ ] T102 [P] Observability/alerts definitions and validation probes in validations/
- [ ] T103 [P] Documentation polish (quickstart.md, plan.md consistency)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Traceability (Phase 2)**: Blocks all user stories until mapped and inputs gathered
- **User Stories (Phase 3+)**: Depend on Traceability completion; each story should remain independently reviewable
- **Cross-Cutting (Final Phase)**: After desired user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2
- **User Story 2 (P2)**: Can start after Phase 2; should remain independently reviewable
- **User Story 3 (P3)**: Can start after Phase 2; should remain independently reviewable

### Within Each User Story

- Diagrams before contracts
- Contracts before validations
- Vendor handover documented before declaring story complete
- Story complete before moving to next priority (unless explicitly parallel)

### Parallel Opportunities

- All tasks marked [P] can run in parallel if they do not touch the same artifact
- Different user stories can be worked on in parallel by different team members after Phase 2

---
