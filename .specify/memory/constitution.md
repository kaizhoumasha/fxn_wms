<!--
SYNC IMPACT REPORT
==================
Version: 1.0.0 → 1.1.0
Type: Minor (Language Standardization)

Principles Established:
1. I. Spec-Driven Lifecycle (规格驱动生命周期) - Translated
2. II. Requirement Traceability (需求可追溯性) - Translated
3. III. Structured SA Design (结构化系统分析设计) - Translated
4. IV. Feature Branch Isolation (功能分支隔离) - Translated
5. V. Technical Feasibility (技术可行性) - Translated
6. VI. Language & Terminology (语言与术语) - New

Added Sections:
- Translated Scope & Artifacts (范围与产物)
- Translated Review & Verification (评审与验证)

Templates Status:
- .specify/templates/*.md: ✅ Compatible (Agents guided by Constitution to generate Chinese content)

Follow-up:
- Ensure future agent interactions respect the "Chinese with bilingual annotations" rule.
-->

# fxn-wms Constitution (项目章程)

## Core Principles (核心原则)

### I. Spec-Driven Lifecycle (规格驱动生命周期)

所有开发工作必须严格遵循 **规格驱动开发 (SDD)** 生命周期：**Specify (定义)** → **Clarify (澄清)** → **Plan (计划)** → **Tasks (任务)** → **Implement (实现)**。在上一阶段的产物被批准之前，不得进行详细设计或代码编写。这确保了在投入资源前的目标一致性。

### II. Requirement Traceability (需求可追溯性)

每一个设计决策和系统产物都必须能够追溯到位于 `docs/origin/` 中的原始客户需求。**系统分析 (SA)** 交付物必须明确地将功能需求映射到这些源文档，以确保保留“客户之声 (Voice of the Customer)”。

### III. Structured SA Design (结构化系统分析设计)

交付物必须遵循标准的**软件工程系统分析 (System Analysis, SA)** 方法。这包括必须提供的产物：**业务/流程流程图 (Flowcharts)**、**数据模型 (Data Models, ER/Schema)** 和 **API 契约 (API Contracts, Sequence/Interface)**。输出内容必须足够详细，能够作为架构师、软件工程师和数据工程师的实施蓝图。

### IV. Feature Branch Isolation (功能分支隔离)

所有工作必须在名为 `NNN-short-name` (例如 `005-agv-routing`) 的隔离**功能分支 (Feature Branches)** 中进行。主分支 (Main/Master) 仅保留已批准并集成的规格说明和设计。产物按分支进行版本控制，仅在完成“Implement (实现)”阶段后合并。

### V. Technical Feasibility (技术可行性 - Python/.Net Core优先)

虽然主要关注点是 **设计/系统分析 (Design/SA)**，但所有提议的解决方案必须在项目的核心技术栈 (**Python/.Net Core**) 内具备技术可行性。设计必须尊重目标环境的约束，并验证与现有 **AGV/RCS** 接口的兼容性。

### VI. Language & Terminology (语言与术语)

所有文档、规格说明和交互主要使用 **中文 (Chinese)** 进行。为了确保技术准确性，关键术语、专有名词及特殊含义词汇必须采用 **双语标注 (Bilingual Annotations)** 格式，例如：“系统分析 (System Analysis)”、“自动导引车 (AGV)”。

## Scope & Artifacts (范围与产物)

### Design Deliverables (设计交付物)

1. **Spec File (`specs/NNN/spec.md`)**: 高层功能需求与用户故事 (User Stories)。
2. **Plan File (`specs/NNN/plan.md`)**: 技术架构、技术栈决策及复杂度分析。
3. **Tasks File (`specs/NNN/tasks.md`)**: 细粒度的、可并行执行的实施步骤。
4. **Design Documents (设计文档)**: 补充图表 (Mermaid/PlantUML)、API 定义 (OpenAPI/Protobuf) 和数据字典。

## Review & Verification (评审与验证)

### Quality Gates (质量门禁)

1. **Prerequisites Check (前置检查)**: 自动验证在 Plan 之前是否存在 `spec.md`，在 Tasks 之前是否存在 `plan.md`。
2. **Constitution Check (章程检查)**: 每个 `plan.md` 必须明确确认符合这些核心原则。
3. **Peer Review (同行评审)**: 设计产物在移交实施前，必须经过清晰度和完整性评审。

## Governance (治理)

本章程取代所有临时性实践。

- **Amendments (修订)**: 必须通过 PR 修改 `.specify/memory/constitution.md` 并进行语义化版本升级。
- **Compliance (合规)**: 所有 `plan.md` 文件必须包含强制性的 "Constitution Check" 章节。
- **Guidance (指导)**: 参见 `GEMINI.md` 了解 Agent 操作协议。

**Version**: 1.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
