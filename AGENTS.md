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

# fxn-wms Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-11

## Active Technologies
- Python 3.11 / .NET 8（目标实现栈；本阶段仅文档） + 文档/图表：Mermaid、PlantUML；接口协议：HTTP/REST + MQTT/SSE（设备/供应商回传） (002-detailed-design)
- 本阶段无代码存储；数据字典/契约以文档形式，后续实现预计 PostgreSQL（假设，需在实现阶段确认） (002-detailed-design)

- Documentation phase; downstream实现面向 Python 3.11+ / .NET 8 兼容 + 设计依赖 SAP/MES/RCS/WCS 接口规范，设备协议 Modbus/MQTT/SSE/WebSocket/HTTP，供应商提供点表/模拟器 (001-high-level-design)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Documentation phase; downstream实现面向 Python 3.11+ / .NET 8 兼容: Follow standard conventions

## Recent Changes
- 002-detailed-design: Added Python 3.11 / .NET 8（目标实现栈；本阶段仅文档） + 文档/图表：Mermaid、PlantUML；接口协议：HTTP/REST + MQTT/SSE（设备/供应商回传）

- 001-high-level-design: Added Documentation phase; downstream实现面向 Python 3.11+ / .NET 8 兼容 + 设计依赖 SAP/MES/RCS/WCS 接口规范，设备协议 Modbus/MQTT/SSE/WebSocket/HTTP，供应商提供点表/模拟器

<!-- MANUAL ADDITIONS START -->
## Spec-Driven 开发与 Agent 使用规则 (中英双语关键术语)
- **流程 (Workflow)**: `/speckit.specify` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.plan` → `/speckit.implement`，严格遵循规格驱动 (Spec-Driven Development)。
- **章程 (Constitution) 必遵守**:
  - Traceability 追溯：所有设计元素需映射到 docs/origin（文件/Sheet/Row/段落）。
  - 调度中台边界 (Integration Boundary)：WMS 不做 PLC/IO；设备交互经协议/工控机 (Modbus/MQTT/SSE/WebSocket/HTTP)。
  - Feasibility 可行性：方案需适配 Python/.NET 栈与现有 AGV/RCS/设备能力。
  - Bilingual 双语：文档默认中文，关键术语中英双语标注。
- **模板要点 (Templates)**:
  - plan-template: Technical Context（语言/依赖/性能目标/约束）、结构与 Constitution Check。
  - tasks-template: 按用户故事 (User Story) 分阶段，可独立验证，严格 checklist 格式。
  - analyze: 用于跨文档一致性与覆盖检查，处理重复/歧义/缺口。
- **Agent 说明 (Agent Notes)**: AGENTS.md 自动聚合各 plan；若更换 Agent，需保持命令/目录结构符合 SpecKit 约定。
- **Review/质量门禁 (Quality Gates)**: Traceability Check、Integration Boundary Check、Feasibility Check、Language & Terminology。
<!-- MANUAL ADDITIONS END -->
