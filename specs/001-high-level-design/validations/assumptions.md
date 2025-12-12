# Validations & Assumptions — 概要设计阶段启动

## Capacity / Performance Baseline
- **AGV 指令响应**: 95% ≤ 10s（SRS §3.7；Origin Sheet “收货暂存区到料盘装箱区” rows 3-90）。验证：模拟/回放 RCS 任务流，记录下发→确认时延。
- **入库高峰吞吐**: ≥ 60 栈板/小时（SRS §3.2；Origin Sheet “码头到收货暂存区” rows 3-36）。验证：场景仿真或历史峰值对账，结合地码/设备节拍。
- **双语可用率**: ≥ 99%（界面/标签切换，SRS §3.7.1）。验证：关键界面/标签抽样检查、异常提示覆盖率。
- **发料链路延迟**: MES→WMS→RCS/WCS 端到端 ≤ 30s（SRS §3.3.3；Origin Sheet “料盘装箱区到SMT作业区” rows 3-120）。验证：时序仿真与接口回放。

## Observability & Alerts
- **指标**: RCS 任务下发/确认时延、接口成功率、设备在线率、队列积压深度、异常告警率。
- **告警阈值**: 时延 > 10s（AGV 指令）或接口成功率 < 99% 触发 P1 告警；设备在线率 < 95% 触发 P1。
- **追溯字段**: TraceID/CorrelationID、地码、设备 ID、PalletID/BinID/ReelID、任务 ID。

## Validation Methods
- **仿真/回放**: 使用供应商提供的模拟器或录播数据，覆盖收货→IQC→上架、发料→补料→退料全路径。
- **演练脚本**: 设计手工兜底/改派/重试脚本，记录前置条件、步骤、预期结果、回退条件。
- **数据来源**: docs/SRS.md §3.2/§3.3/§3.7，docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx（性能/异常条目，行号待标注），现场历史峰值数据（待采集）。

## US3 Validation Tasks (linked to T030–T034)
- 载荷/模拟：参见 validations/us2-scenarios.md 示例；回放时使用实际 TraceID/TaskID/CommandID。
- 演练/兜底：integration/playbooks/us3-fallback.md。
- 证据：记录仿真/演练结果、时延/成功率指标，更新 validations/ 目录下的结果文件（待运行时补充）。

## Evidence (to be collected)
| Metric | Target | Source | Status | Owner | ETA |
| ------ | ------ | ------ | ------ | ----- | --- |
| AGV 指令响应 p95 | ≤10s | RCS 任务回放日志；Origin Sheet “收货暂存区到料盘装箱区” rows 17-23 | 待填实测值 | Ops | 2025-12-18 |
| 入库吞吐 | ≥60 栈板/小时 | 仓库峰值记录；Origin Sheet “码头到收货暂存区” rows 3-21 | 待填实测值 | Ops | 2025-12-18 |
| 发料端到端时延 | ≤30s | MES/WMS/RCS/WCS 回放日志；Origin Sheet “料盘装箱区到SMT作业区” rows 3-38 | 待填实测值 | Ops | 2025-12-20 |
| 双语可用率 | ≥99% | 界面抽检记录 | 待填实测值 | QA | 2025-12-20 |

> 数据填充指引：获取实际指标后，将 “Pending” 替换为实测值与日期；若有日志/报表，请在此处记录文件路径（示例：`logs/perf/2025-12-AGV-latency.csv`），并在 plan.md Review Packet 中列为佐证。TraceID/TaskID/CommandID(追踪/任务/指令 ID) 需保留以便回溯。

## Alignment to Success Criteria (SC-001..SC-004)
- **SC-001 (追溯到模块/接口责任)**: TraceID/任务/接口映射在 contracts/、diagrams/，验证时确保责任分界可追溯。
- **SC-002 (接口覆盖与缺口=0)**: us2-scenarios + contracts 字段/错误/幂等检查，缺口列入评审。
- **SC-003 (性能/容量基线)**: 本文件的基线指标与验证方法；执行仿真/回放并记录结果。
- **SC-004 (风险与缓解签字)**: playbooks/us3-fallback + risk list in plan.md；验证演练结果并纳入评审记录。

## Security & Compliance Acceptance
- 数据分级、审计留存周期明确且与 SAP/MES 基线对齐；日志/告警保留 ≥ 1 年或现场约定值有记录。
- 接口鉴权/加密要求 per 系统（SAP/MES/RCS/WCS/设备）已在 contracts/ 指定；TraceID/脱敏要求明确。
- 访问控制与最小权限：角色/域分权声明；敏感字段不出现在设备/日志载荷。
- 证据：记录 auth/crypto 配置与日志保留策略的验证结果（Owner/ETA 同上表）。
