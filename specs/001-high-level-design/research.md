# Research (Phase 0) — 概要设计阶段启动

## 1) 交互边界与供应商配合
- **Decision**: WMS 仅作为调度中台，通过工控机或协议（Modbus/MQTT/SSE/WebSocket/HTTP）与设备交互；不做 PLC/IO 编程。所有设备点表/字段、模拟器/录播样例由设备供应商提供；契约中记录责任分界、触发条件、负载字段、QoS、错误处理与人工兜底。
- **Rationale**: 用户明确“系统不直接操作设备；通过协议交互，需供应商协助”。
- **Alternatives considered**: 直接 PLC/IO 控制（违背用户约束、增加安全风险）；仅 HTTP 接口（无法覆盖实时/低延迟场景）。

## 2) 容量/性能基线获取
- **Decision**: 采用现网能力测算：收集历史峰值（入库栈板/小时、AGV 指令往返时延、急单插单比例、网络抖动），结合场景仿真/时序走查，形成基线与验证方法（目标示例：AGV 95%≤10s、入库≥60 栈板/小时、双语可用率≥99%）。
- **Rationale**: Spec/FR 要求基于现网能力确认；需可验证、可追溯。
- **Alternatives considered**: 套用行业默认值（风险高、缺乏现场依据）；推迟定义（阻塞设计评审）。

## 3) 技术栈定位（设计阶段）
- **Decision**: 当前仅输出设计文档；后续实现需兼容 Python 3.11+ / .NET 8。设计中所有接口/数据模型保持与两栈兼容，避免绑定单一框架。
- **Rationale**: 章程与历史约定；保持实现弹性。
- **Alternatives considered**: 立即选定单一后端框架（缺乏实现阶段输入）；暂不声明技术栈（无法评估可行性）。

## 4) 需求追溯方法
- **Decision**: 在 plan/data-model/contracts/diagrams 中引用 docs/origin 具体文件与章节/行（如《休斯顿P9自动化仓库功能分解清单_202511021.xlsx》Sheet/Row，SRS 段落号）；每个接口/字段/流程均附来源。
- **Rationale**: 章程与 Spec 要求全链路追溯，便于评审与验收。
- **Alternatives considered**: 仅在 spec 维护追溯（易脱节）；后置到实现阶段（评审不可用）。
