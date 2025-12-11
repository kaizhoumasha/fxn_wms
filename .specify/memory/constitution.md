<!--
SYNC IMPACT REPORT
==================
Version: 1.1.0 → 1.2.0
Type: Minor (new integration boundary principle + template alignment)

Modified Principles:
- V. Technical Feasibility (aligned with device/protocol constraints)
- VI. Language & Terminology (reinforced bilingual for interfaces)
- VII. Integration Boundaries & Vendor Collaboration (new)

Added Sections:
- None

Removed Sections:
- None

Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/agent-file-template.md ⚠ pending (auto-generated; refresh when plans aggregate)
- .specify/templates/commands/* N/A (directory not present)

Follow-up TODOs:
- None
-->

# fxn-wms Constitution (项目章程)

## Core Principles (核心原则)

### I. Spec-Driven Lifecycle (规格驱动生命周期)

本项目严格遵循 **规格驱动开发 (SDD)** 生命周期：**Specify (定义)** → **Clarify (澄清)** → **Plan (计划)** → **Tasks (任务)** → **Implement (实现)**。本项目的 “实现” 以 **系统设计文档 (Detailed Design Documents)**、**系统分析方案 (SA Proposal)** 与 **接口定义 (Interface Definitions)** 为主要产物，而非直接可执行的软件。

### II. Requirement Traceability (需求可追溯性)

每一个设计决策、数据字段及接口定义都必须能够追溯到 `docs/origin/` 的原始客户需求。**系统分析 (SA)** 交付物必须建立从 **功能需求 (Functional Requirements)** 到原始文档的明确映射，确保“客户之声 (Voice of the Customer)”在设计中得到完整体现。

### III. Structured SA Design (结构化系统分析设计)

交付物必须遵循标准的 **软件工程系统分析 (System Analysis, SA)** 方法论。核心产物包括但不限于：
* **业务流程图 (Business Process Flowcharts)**：描述作业流转。
* **数据模型 (Data Models)**：ER 图、数据字典、标识与对账字段。
* **API 契约 (API Contracts)**：时序图 (Sequence Diagrams)、接口定义 (OpenAPI/Protobuf)。
输出须足够详细，可直接指导 **架构师 (Architects)**、**软件工程师 (Software Engineers)**、**数据工程师 (Data Engineers)** 落地实施。

### IV. Feature Branch Isolation (功能分支隔离)

所有设计工作必须在名为 `NNN-short-name` (例如 `005-agv-routing`) 的隔离 **功能分支 (Feature Branches)** 中进行。主分支仅保留已评审通过并集成的设计方案，产物按分支进行版本控制。

### V. Technical Feasibility (技术可行性 - Python/.Net Core 优先)

设计方案必须在项目核心技术栈 (**Python** / **.Net Core**) 及目标环境约束内具备可行性，包含 **AGV/RCS** 硬件能力、现有接口规范、协议限制。需验证与已提供文档（如 `AGV API SPEC`）的兼容性，避免提出无法在现网设备/协议上实现的方案。

### VI. Language & Terminology (语言与术语)

所有文档、规格说明和交互主要使用 **中文**。为确保跨团队理解，**关键术语 (Key Terms)**、**专有名词 (Proper Nouns)** 及 **特殊含义词汇 (Specialized Vocabulary)** 必须采用 **双语标注 (Bilingual Annotations)**，例如：“系统分析 (System Analysis)”、“自动导引车 (AGV)”、“物料清单 (BOM)”。

### VII. Integration Boundaries & Vendor Collaboration (调度中台与设备交互边界)

本系统作为调度中台统一协调 **RCS（AGV/E-AGV/CTU）** 与各类自动化设备（流水线、机械臂、拆箱/装盘设备等）。WMS 不直接进行 PLC 编程或底层 IO 控制，设备控制由其工控机/本地控制器负责。与设备的交互需通过约定协议（如 **Modbus/MQTT/SSE/WebSocket/HTTP** 等）明确触发条件、负载字段、QoS 与错误处理，并要求设备供应商提供点表、接口/协议能力与模拟/联调支持。设计文档必须记录责任分界、接口契约与人工兜底路径。

## Scope & Artifacts (范围与产物)

### Design Deliverables (设计交付物)

在 `specs/NNN-feature/` 目录下，应包含以下产物：

1. **Spec File (`spec.md`)**: 高层功能需求、用户故事与验收标准。
2. **Plan File (`plan.md`)**: 技术架构与模块职责、复杂度分析、集成路径。
3. **Tasks File (`tasks.md`)**: 细粒度的设计任务列表（如流程图/时序图/数据字典/接口字段定义/演练脚本）。
4. **Design Artifacts (设计产物)**:
   * **Diagrams**: Mermaid/PlantUML 流程图、时序图。
   * **Schemas**: 数据字典、标识与对账字段、容量/性能假设。
   * **Interfaces**: JSON/YAML API 定义、协议字段映射、幂等与错误恢复设计。
   * **Integration & Vendor Handover**: 设备协议/点表清单、供应商责任分界、模拟/联调方案、人工兜底流程。

## Review & Verification (评审与验证)

### Quality Gates (质量门禁)

1. **Traceability Check (追溯性检查)**: 每个设计元素是否都有对应需求来源？
2. **Integration Boundary Check (交互边界检查)**: 是否明确 WMS 为调度中台、不做 PLC，协议/字段/错误处理与供应商责任已定义？
3. **Feasibility Check (可行性检查)**: 设计是否在现有 AGV/RCS/设备协议与 Python/.Net Core 能力范围内可行？
4. **Constitution Check (章程检查)**: `plan.md` 是否确认符合本章程原则并记录问题/偏差？

## Governance (治理)

本章程为项目最高指导文件。

- **Amendments (修订)**: 通过 Pull Request 进行，并更新版本号。
- **Compliance (合规)**: 所有 Agent 生成的 `plan.md` 必须包含 "Constitution Check" 章节并声明合规/偏差。
- **Guidance (指导)**: 参见 `GEMINI.md` 了解 Agent 操作协议。

**Version**: 1.2.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-11
