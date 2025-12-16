# 文档中心 (Documentation Hub)

**fxn-wms** 项目文档导航 | Project Documentation Navigation

---

## 📋 快速导航 (Quick Navigation)

### 核心规格文档 (Core Specifications)

| 文档 | 说明 | 适用人群 |
|------|------|----------|
| [SRS.md](./SRS.md) | **软件需求规格说明书** (Software Requirements Specification)<br/>项目权威需求文档，定义系统功能、性能、接口规范 | 全体开发人员、测试人员、项目经理 |
| [user_requirement.md](./user_requirement.md) | **用户需求文档**<br/>从客户原始文档提取的完整需求 | 需求分析人员、产品经理 |
| [feature_list.md](./feature_list.md) | **功能清单**<br/>系统功能模块详细列表 | 开发人员、测试人员 |

### 架构设计文档 (Architecture Design)

| 文档 | 说明 | 适用人群 |
|------|------|----------|
| [system_architecture.md](./system_architecture.md) | **系统架构设计**<br/>三层架构设计、解耦原则、状态管理策略 | 架构师、高级开发人员 |
| [development_architecture.md](./development_architecture.md) | **开发架构**<br/>代码组织、模块划分、开发规范 | 全体开发人员 |
| [hardware_interface_standard.md](./hardware_interface_standard.md) | **硬件接口标准**<br/>UHI (Universal Hardware Interface) 规范、协议适配器设计 | 硬件集成开发人员 |

### 技术选型与集成 (Technology & Integration)

| 文档 | 说明 | 适用人群 |
|------|------|----------|
| [technology_stack_decision_pack.md](./technology_stack_decision_pack.md) | **技术栈决策包（合并版）**<br/>合并分析观点 + 领导可选结论（统一口径） | 管理层、技术负责人、架构师 |
| [third_party_integration_whitepaper.md](./third_party_integration_whitepaper.md) | **第三方集成白皮书**<br/>外部系统集成方案 (WMS/SAP/RCS/ECS/PDA) | 集成开发人员、接口对接人员 |
| [project_function_list_and_acceptance_criteria.md](./project_function_list_and_acceptance_criteria.md) | **功能清单与验收标准**<br/>功能模块与验收条件 | 测试人员、项目经理 |

### 原始资料 (Source Materials)

| 目录 | 说明 |
|------|------|
| [origin/](./origin/) | **客户原始文档**<br/>Excel、Word、PDF 格式的需求源文件 |
| [design/](./design/) | **设计文件**<br/>图表、原型、设计稿 |

---

## 🎯 按角色查阅 (Read by Role)

### 项目经理 / 产品经理 (Project/Product Manager)
1. [user_requirement.md](./user_requirement.md) - 了解客户需求
2. [SRS.md](./SRS.md) - 掌握系统规格
3. [project_function_list_and_acceptance_criteria.md](./project_function_list_and_acceptance_criteria.md) - 验收标准

### 架构师 (Architect)
1. [system_architecture.md](./system_architecture.md) - 系统架构设计
2. [development_architecture.md](./development_architecture.md) - 开发架构
3. [technology_stack_decision_pack.md](./technology_stack_decision_pack.md) - 技术选型（统一口径）
4. [hardware_interface_standard.md](./hardware_interface_standard.md) - 硬件接口规范

### 开发人员 (Developer)
1. [SRS.md](./SRS.md) - 功能需求
2. [development_architecture.md](./development_architecture.md) - 代码组织
3. [feature_list.md](./feature_list.md) - 功能模块
4. [hardware_interface_standard.md](./hardware_interface_standard.md) - 硬件接口 (如需对接硬件)

### 测试人员 (QA/Tester)
1. [SRS.md](./SRS.md) - 测试依据
2. [project_function_list_and_acceptance_criteria.md](./project_function_list_and_acceptance_criteria.md) - 验收标准
3. [feature_list.md](./feature_list.md) - 功能清单

### 集成工程师 (Integration Engineer)
1. [hardware_interface_standard.md](./hardware_interface_standard.md) - UHI 通用硬件接口规范
2. [third_party_integration_whitepaper.md](./third_party_integration_whitepaper.md) - ECS 设备接入白皮书
3. [SRS.md](./SRS.md) 第 3.8 节 - WMS 集成架构
4. [SRS.md](./SRS.md) 第 3.6 节 - 北向/南向接口需求

---

## 🔍 按主题查阅 (Read by Topic)

### 仓库业务流程 (Warehouse Business Processes)
- [SRS.md](./SRS.md) 第 3.1 节 - 仓库布局与货架类型
- [SRS.md](./SRS.md) 第 3.2 节 - 业务流程 (收货、上架、拣货、出库等)
- [user_requirement.md](./user_requirement.md) - 详细业务场景

### 硬件系统对接 (Hardware Integration)
- [hardware_interface_standard.md](./hardware_interface_standard.md) - UHI 通用硬件接口规范
- [third_party_integration_whitepaper.md](./third_party_integration_whitepaper.md) - ECS 及自动化设备接入白皮书
- [SRS.md](./SRS.md) 第 3.6.2 节 - 南向接口详细需求

### 上游系统对接 (Upstream Integration)
- [SRS.md](./SRS.md) 第 3.8 节 - 与现有 WMS 的集成架构（库存查询/预留/确认接口）
- [SRS.md](./SRS.md) 第 3.6.1 节 - 北向接口需求（SAP/WMS 单据接入）

### 异常处理与容错 (Error Handling & Fault Tolerance)
- [SRS.md](./SRS.md) 第 3.7 节 - 异常处理机制
- [system_architecture.md](./system_architecture.md) - 容错设计原则

### 性能与可靠性 (Performance & Reliability)
- [SRS.md](./SRS.md) 第 4 节 - 非功能性需求
- [technology_stack_decision_pack.md](./technology_stack_decision_pack.md) - 技术选型依据（统一口径）

---

## 📖 文档阅读顺序建议 (Recommended Reading Order)

### 新成员入门 (Onboarding)
```
1. README.md (本文档)
   ↓
2. system_architecture.md (理解系统架构)
   ↓
3. SRS.md 第 1-2 节 (项目概述与总体描述)
   ↓
4. development_architecture.md (了解代码结构)
   ↓
5. 根据角色选择其他文档
```

### 需求分析阶段 (Requirements Analysis)
```
1. user_requirement.md (原始需求)
   ↓
2. SRS.md (规格化需求)
   ↓
3. feature_list.md (功能分解)
   ↓
4. project_function_list_and_acceptance_criteria.md (验收标准)
```

### 设计开发阶段 (Design & Development)
```
1. system_architecture.md (架构设计)
   ↓
2. development_architecture.md (开发架构)
   ↓
3. technology_stack_decision_pack.md (技术选型，统一口径)
   ↓
4. hardware_interface_standard.md (接口设计)
   ↓
5. SRS.md 相关章节 (详细需求)
```

---

## 🔄 文档更新规范 (Documentation Update Guidelines)

### 更新原则
1. **SRS.md 为权威文档** - 所有需求变更必须更新 SRS
2. **保持文档同步** - 架构变更需同步更新相关设计文档
3. **版本控制** - 重大变更需在文档中记录版本历史
4. **双语维护** - 中文为主，关键技术术语附英文注释

### 文档责任人
- **SRS.md**: 需求分析师 + 项目经理
- **system_architecture.md**: 系统架构师
- **development_architecture.md**: 技术负责人
- **hardware_interface_standard.md**: 硬件集成负责人
- **third_party_integration_whitepaper.md**: 集成工程师

---

## 📞 文档反馈 (Feedback)

如发现文档问题或需要补充内容，请：
1. 提交 Issue 说明问题
2. 联系对应文档责任人
3. 遵循 OpenSpec 工作流提交变更提案

---

**最后更新**: 2025-12-15
**文档版本**: v1.0
**维护者**: fxn-wms 项目组
