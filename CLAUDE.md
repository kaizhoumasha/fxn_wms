# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## Project Overview

**fxn-wms** (富士康 WMS) is a Warehouse Execution System (WES) for the Houston P9 automated warehouse. It serves as an **independent control middleware** between enterprise WMS/SAP (upstream) and hardware systems like AGV/RCS/WCS (downstream).

**Current Stage**: Early development - primarily documentation and specifications. Source code structure exists (`src/app/`) but implementation is minimal.

**Key Characteristics**:
- **Spec-driven development** using OpenSpec workflow
- **Bilingual project**: Chinese primary with English technical annotations
- **Three-layer architecture**: Northbound (Business) → Core (Brain) → Southbound (Hardware)
- **Event-driven, decoupled design** with plugin-based hardware adapters

## Architecture

```
src/app/
├── api/              # Northbound REST API layer
│   └── endpoints/    # API route handlers
├── core/             # Strategy engine, orchestration, state management
├── domain/           # Business logic and domain services
│   └── services/
└── infra/            # Infrastructure layer
    ├── database/     # PostgreSQL + Redis
    └── external_adapters/  # Hardware protocol adapters (RCS, ECS, PDA)
```

**Design Principles** (from `docs/system_architecture.md`):
- **Decoupling**: WES issues intent-based commands, not device-specific instructions
- **Stateless Execution**: WES maintains transient execution state; WMS is inventory source of truth
- **Plugin Architecture**: Hardware drivers as adapters, vendor-agnostic

## Development Workflow

### OpenSpec Workflow (Primary)

This project uses **OpenSpec** for spec-driven development:

```bash
# Check existing work
openspec list                    # Active changes
openspec list --specs            # Existing capabilities

# Create new change proposal
openspec validate <change-id> --strict

# After deployment
openspec archive <change-id> --yes
```

**Key Files**:
- `openspec/project.md` - Project conventions (currently template, needs customization)
- `openspec/specs/` - Current truth (what IS built)
- `openspec/changes/` - Proposals (what SHOULD change)
- `openspec/AGENTS.md` - Complete workflow documentation

**Change Naming**: Use kebab-case, verb-led: `add-agv-routing`, `update-binning-strategy`

### Documentation Structure

**Primary Specs** (Chinese with English annotations):
- `docs/SRS.md` - Software Requirements Specification (软件需求规格说明书)
- `docs/user_requirement.md` - User requirements extracted from customer docs
- `docs/system_architecture.md` - System architecture design

**Original Materials**: `docs/origin/*.xlsx/.docx/.pdf` - Customer source documents

## Key Domain Concepts

**Hardware Systems**:
- **RCS** (Robot Control System) - AGV/CTU scheduling
- **ECS** (Equipment Control System) - Robotic arms, conveyors, vision
- **PDA** - Handheld terminals for manual operations
- **QMS** - Quality Management System integration
- **SFC** - Shop Floor Control for production tracking

**Warehouse Zones** (from SRS 3.1):
- 码头收货区 (Dock Receiving Area)
- IQC待检区/复判区 (IQC Inspection/Review Area)
- 料盘装箱区 (Tray Kitting Area)
- SMT作业区 (SMT Operation Area)
- 机构件作业区 (Mechanical Parts Area)
- 退料区 (Return Material Area)

**Rack Types** (SRS 3.1.2):
- **单层货架** (Single-Layer Rack) - 4 bins, transit buffer
- **五层货架** (Five-Layer Rack) - 20 bins (4×5), A/B sides, high-density storage
- **生产/退货货架** (Production/Return Rack) - Shelf structure, tray-level tracking

## Development Commands

### Python Environment

```bash
# Activate virtual environment
source .venv/bin/activate

# (No requirements.txt yet - add when dependencies are defined)
```

### OpenSpec Commands

```bash
# Validation
openspec validate --strict              # Validate all
openspec validate <change-id> --strict  # Validate specific change

# Inspection
openspec show <item>                    # View change or spec
openspec show <change> --json --deltas-only  # Debug deltas

# Management
openspec archive <change-id> --yes      # Archive after deployment
```

## Important Constraints

1. **Language**: User prefers Chinese communication with bilingual technical terms
2. **Spec-First**: No implementation without approved spec/plan/tasks
3. **Hardware Abstraction**: Never write vendor-specific code in core logic
4. **Idempotency**: All hardware commands must support retry (SRS 3.7.3)
5. **State Verification**: Physical state must match digital state before operations

## Integration Patterns

**Northbound (WMS/SAP)**:
- REST API for order ingest (GRN, work orders)
- Webhooks for inventory confirmation
- Query-driven: WES queries WMS for inventory, not vice versa

**Southbound (Hardware)**:
- Universal Hardware Interface (UHI) abstraction
- Protocol adapters: HTTP, TCP, Modbus, MQTT
- Three patterns: Synchronous (request-response), Asynchronous (events), Bidirectional (handshake)

**Error Handling** (SRS 3.7):
- 3 retry attempts with 10s timeout
- Automatic device health checks (heartbeat)
- Checkpoint/resume for task interruption
- Manual fallback mode when automation fails

## Notes for AI Assistants

- **Read SRS first**: `docs/SRS.md` contains authoritative requirements
- **Check OpenSpec**: Use `openspec list` before creating new changes
- **Bilingual output**: Provide Chinese explanations with English technical terms in parentheses
- **Architecture compliance**: Follow three-layer separation (L1 Business, L2 Core, L3 Hardware)
- **No premature implementation**: This is a spec-driven project - validate proposals before coding
