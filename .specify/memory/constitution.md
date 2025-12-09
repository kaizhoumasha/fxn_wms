<!--
SYNC IMPACT REPORT
==================
Version: 1.0.0 → 1.1.0
Type: Minor (Scope Refinement & Language Standardization)

Principles Established:
1. I. Spec-Driven Lifecycle (规格驱动生命周期) - Adapted for Design
2. II. Requirement Traceability (需求可追溯性) - Emphasized
3. III. Structured SA Design (结构化系统分析设计) - New
4. IV. Feature Branch Isolation (功能分支隔离) - Retained
5. V. Technical Feasibility (技术可行性) - Contextualized
6. VI. Language & Terminology (语言与术语) - New

Added Sections:
- Scope & Artifacts (范围与产物) - Defines SA deliverables
- Review & Verification (评审与验证) - Adapted for documents

Templates Status:
- .specify/templates/*.md: ⚠ Pending adaptation (Agents must interpret 'Implementation' as 'Design Creation' per Constitution)

Follow-up:
- Future plans should use the "Design Documents" structure instead of standard code layout.
-->

# fxn-wms Constitution (项目章程)

## Core Principles (核心原则)

### I. Spec-Driven Lifecycle (规格驱动生命周期)

本项目严格遵循 **规格驱动开发 (SDD)** 生命周期：**Specify (定义)** → **Clarify (澄清)** → **Plan (计划)** → **Tasks (任务)** → **Implement (实现)**。
**特别注意**：鉴于本项目为 **系统设计 (System Design)** 性质，“Implement (实现)”阶段的产出并非可执行软件，而是 **详细设计文档 (Detailed Design Documents)**、**系统分析方案 (SA Proposal)** 及 **接口定义 (Interface Definitions)**。

### II. Requirement Traceability (需求可追溯性)

每一个设计决策、数据字段及接口定义都必须能够追溯到位于 `docs/origin/` 中的原始客户需求。**系统分析 (SA)** 交付物必须建立从 **功能需求 (Functional Requirements)** 到原始文档的明确映射，确保“客户之声 (Voice of the Customer)”在设计中得到完整体现。

### III. Structured SA Design (结构化系统分析设计)

交付物必须遵循标准的 **软件工程系统分析 (System Analysis, SA)** 方法论。核心产物包括但不限于：
*   **业务流程图 (Business Process Flowcharts)**：描述作业流转。
*   **数据模型 (Data Models)**：ER 图、数据库 Schema 定义。
*   **API 契约 (API Contracts)**：时序图 (Sequence Diagrams)、接口定义 (OpenAPI/Protobuf)。
所有输出必须足够详细，能够作为后续 **架构师 (Architects)**、**软件工程师 (Software Engineers)** 和 **数据工程师 (Data Engineers)** 的直接实施蓝图。

### IV. Feature Branch Isolation (功能分支隔离)

所有设计工作必须在名为 `NNN-short-name` (例如 `005-agv-routing`) 的隔离 **功能分支 (Feature Branches)** 中进行。主分支 (Main/Master) 仅保留已评审通过并集成的设计方案。产物按分支进行版本控制。

### V. Technical Feasibility (技术可行性 - Python/.Net Core优先)

虽然主要产出为设计文档，但所有提议的解决方案必须在项目的核心技术栈 (**Python** / **.Net Core**) 内具备技术可行性。设计方案必须尊重目标环境的约束（如 **AGV/RCS** 硬件限制），并验证与现有接口文档（如 `AGV API SPEC`）的兼容性。

### VI. Language & Terminology (语言与术语)

所有文档、规格说明和交互主要使用 **中文 (Chinese)** 进行。
为了确保技术准确性及跨团队理解，**关键术语 (Key Terms)**、**专有名词 (Proper Nouns)** 及 **特殊含义词汇 (Specialized Vocabulary)** 必须采用 **双语标注 (Bilingual Annotations)** 格式，例如：“系统分析 (System Analysis)”、“自动导引车 (AGV)”、“物料清单 (BOM)”。

## Scope & Artifacts (范围与产物)

### Design Deliverables (设计交付物)

在 `specs/NNN-feature/` 目录下，应包含以下产物：

1.  **Spec File (`spec.md`)**: 高层功能需求、用户故事 (User Stories) 及验收标准。
2.  **Plan File (`plan.md`)**: 技术架构决策、涉及的系统模块及复杂度分析。
3.  **Tasks File (`tasks.md`)**: 细粒度的设计任务列表（例如：“绘制入库流程图”、“定义入库API字段”）。
4.  **Design Artifacts (设计产物)**:
    *   **Diagrams**: Mermaid 或 PlantUML 格式的流程图与时序图。
    *   **Schemas**: Excel 或 Markdown 格式的数据字典。
    *   **Interfaces**: JSON/YAML 格式的 API 定义。

## Review & Verification (评审与验证)

### Quality Gates (质量门禁)

1.  **Traceability Check (追溯性检查)**: 每个设计元素是否都有对应的需求来源？
2.  **Feasibility Check (可行性检查)**: 设计是否在现有 AGV/RCS 能力范围内？
3.  **Constitution Check (章程检查)**: `plan.md` 是否确认符合本章程原则？

## Governance (治理)

本章程为项目最高指导文件。

-   **Amendments (修订)**: 修改需通过 Pull Request 进行，并更新版本号。
-   **Compliance (合规)**: 所有 Agent 生成的 `plan.md` 必须包含 "Constitution Check" 章节。
-   **Guidance (指导)**: 参见 `GEMINI.md` 了解 Agent 操作协议。

**Version**: 1.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09