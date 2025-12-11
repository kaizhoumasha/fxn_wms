# Design Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. Align all content with the Constitution: design-first, traceable to `docs/origin/`, WMS as调度中台 (no PLC/IO coding), bilingual key terms.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Lifecycle: Spec/Clarify completed; plan scopes only design artifacts (no code by default).
- Traceability: Link each design element to `docs/origin/` (cite file + section/row).
- Integration Boundaries: WMS acts as 调度中台; no PLC programming. Interfaces via agreed protocols (e.g., Modbus/MQTT/SSE/WebSocket/HTTP). Vendor responsibilities (point lists, simulators) recorded.
- Feasibility: Compatible with AGV/RCS/设备能力 and Python/.Net Core constraints; aligns with provided interface specs.
- Language & Terminology: Chinese primary with bilingual key terms; glossary updated if new terms appear.

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

**Structure Decision**: [Document the selected structure and reference the real
directories captured above. If code is needed, document the actual paths used rather
than generic templates.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
