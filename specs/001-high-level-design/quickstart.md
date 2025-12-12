# Quickstart — 概要设计阶段启动

## 目录结构
- `plan.md`: 本设计计划与 Constitution 检查。
- `research.md`: Phase 0 结论，含协议边界与容量基线获取方法。
- `data-model.md`: 业务模块、接口契约、数据对象、异常场景、验证工件。
- `contracts/`: 各系统/设备的交互契约框架与字段要素。
- `diagrams/`: 存放流程/时序图（待补充）。
- `validations/`: 容量/性能/可观察性假设与验证脚本（如有）。
- `tasks.md`: 后续 /speckit.tasks 生成的任务清单。

## 如何阅读与扩展
1) 先读 `research.md` 理解交互边界、供应商交付物需求。  
2) 在 `data-model.md` 补充各字段来源与标识/对账字段，引用 docs/origin 具体 Sheet/Row/段落。  
3) 在 `contracts/` 为 SAP/MES/RCS/WCS/设备补全协议、字段、幂等/错误处理，标注供应商需提供的点表/模拟器。  
4) 在 `diagrams/` 绘制关键路径（入库、发料、异常兜底）的流程与时序图，附引用。  
5) 将容量/性能假设与验证方法放入 `validations/`，并与 SC/FR 对齐。  
6) 供应商协作：在 contracts/integration-contracts.md 填写点表/接口/模拟器交付要求；在 validations/ 记录演练/仿真用例。

## 术语与缩写 (Bilingual Glossary)
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

## 提交前检查
- Constitution Check：调度中台、不做 PLC/IO；协议与供应商责任已记录。
- Traceability：每个接口/字段/流程引用 docs/origin 与 SRS 段落。
- 双语：关键术语保持中英对照。
- 性能/容量：基线与验证方法明确（源于现网测算）。
- SC 对齐：验证与 SC-001..SC-004 映射在 validations/assumptions.md。
- 交付包：plan/research/data-model/contracts/diagrams/validations、playbooks 汇总用于评审。
