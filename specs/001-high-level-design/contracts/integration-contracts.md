# Integration Contracts — 概要设计阶段启动

> 协议/字段以供应商与系统方提供的规范为准；此处列出契约框架与交互要素。引用来源：docs/SRS.md，docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx（后续补充具体 Sheet/Row/段落）。

## 1. SAP
- **触发**: 收货/GRN 获取，库存变动回传。
- **协议**: HTTP/REST（假设），批量/同步调用；需确认鉴权方式。
- **载荷要素**: PO/GRN、LineItem、Material、Qty、Vendor、Batch。
- **幂等/错误**: 以业务键（PO+LineItem+Batch）去重；失败需重试+人工核对队列。
- **字段映射**:
  - Keys: PO, LineItem, GRN, Batch
  - Qty/Unit: OrderedQty, ReceivedQty, UoM
  - Timestamps: DeliveryDate, PostDate
  - Trace: TraceID/CorrelationID from WMS
- **错误码/恢复**: 4xx 参数/校验错误（人工复核）；5xx 重试+告警；幂等冲突记录人工队列。

## 2. MES
- **触发**: 生产工单与投料需求下发；投料回执/追溯上报。
- **协议**: HTTP/REST（假设）；需明确异步回调或轮询模式。
- **载荷要素**: ProductionOrder、BOM、需求明细（料号/数量/批次约束）、投料确认。
- **幂等/错误**: ProductionOrder+LineItem 作为幂等键；失败走告警+人工补录。
- **字段映射**:
  - Keys: ProductionOrder, LineItem
  - Demand: Material, Qty, BatchConstraints, Priority (急单标记)
  - Feedback: IssuedQty, ReturnedQty, TraceID, Timestamp
- **错误码/恢复**: 4xx 校验错误→人工修正；5xx 重试+告警；回执缺失→手工补录。

## 3. RCS (AGV/E-AGV/CTU)
- **触发**: 搬运任务创建/取消/状态回报。
- **协议**: HTTP/REST 或 WebSocket（事件推送）；RCS 定义地码与设备列表。
- **载荷要素**: TaskID、Source/Target 地码、载具/设备类型、优先级、状态、异常码。
- **幂等/错误**: TaskID 幂等；异常返回需支持重派/改派；拥塞/设备不可用需告警+人工接管。
- **字段映射**:
  - Keys: TaskID (WMS 生成), MapVersion, DeviceType, Priority
  - Locations: SourceCode, TargetCode, PalletID/BinID
  - Status: Created/Dispatched/Executing/Done/Exception, ErrorCode, RetryCount
  - Trace: TraceID/CorrelationID, Timestamp
- **错误码/恢复**: 错误码表需对齐阻塞/可重试类型；拥塞/设备不可用→改派/人工接管；超时重试+告警。

## 4. WCS / 固定设备 (输送线/分拣/叠盘/拆盘)
- **触发**: 启停、节拍/占位状态上报、错误事件。
- **协议**: 优先 SSE/WebSocket（事件流）或 MQTT（轻量消息）；HTTP 作为配置/下达指令。
- **载荷要素**: CommandID、设备位点、托盘/料箱标识、状态/错误码、传感器信号。
- **幂等/错误**: CommandID 幂等；错误需提供错误码表+人工兜底流程。
- **字段映射**:
  - Keys: CommandID, DeviceID, Station/Slot
  - Payload: PalletID/BinID, Action (Start/Stop/Divert), Sensors
  - Status/Error: State, ErrorCode, Recoverable flag
  - Trace: TraceID, Timestamp

## 5. 设备（流水线/机械臂/拆箱装 tray/自动拆叠栈）
- **触发**: 作业指令、点表读写、状态/故障上报。
- **协议**: 经工控机透传，基于 Modbus/MQTT/SSE/WebSocket/HTTP（按设备类型选择）。不进行 PLC/IO 直接控制。
- **载荷要素**: Point/Tag 列表、作业参数、状态/告警代码、作业结果（成功/失败+原因）。
- **供应商交付要求**: 点表/字段定义、协议/端口、QoS/重试/超时策略、模拟器或录播数据、版本兼容矩阵。
- **字段映射**:
  - Keys: DeviceID, PointID/Tag
  - Payload: Params (e.g., tray type, speed), PalletID/BinID
  - Status: ResultCode, AlarmCode, Timestamp
  - Trace: TraceID, Operator/Station (if applicable)

## 6. 通用错误与监控
- **错误码表**: 统一错误分类（通信/业务/设备/数据），映射到各系统/设备错误。
- **追溯字段**: CorrelationID/TraceID、时间戳、来源系统/设备、操作人/工位。
- **告警与兜底**: 超时/异常触发告警；提供人工接管/手工工单路径；关键路径支持重试/改派。

## Vendor Inputs Required (Per System)

- **SAP/MES**: 接口文档版本、鉴权方式、字段约束（必填/枚举）、批量/分页规则、节流限制；测试/沙箱环境与示例报文。
- **RCS**: 地码/地图版本、设备清单、任务指令字段/长度限制、状态/异常码表、推送方式（WebSocket/HTTP 回调）、重试/改派策略；模拟器或回放日志。
- **WCS/固定设备**: 设备列表与位点、指令/状态码表、事件推送格式（SSE/WebSocket/MQTT）、节拍/占位更新频率、错误恢复流程；模拟接口或录播。
- **现场自动化设备（机械臂/拆箱/装盘/叠栈等）**: 点表/寄存器定义、工控机协议与端口、作业参数范围、告警代码、作业完成/失败上报格式、版本兼容性；仿真/录播数据。
- **通用**: 安全要求（认证、加密）、IP 白名单、网络/QoS 约束、时钟同步方式、日志留存周期。

## Security & Auth Expectations
- **SAP/MES**: 明确 auth 方式（API key/Token/证书）、token 生命周期、TLS 要求；日志脱敏（不含敏感字段值）；节流/速率限制需声明。
- **RCS**: 认证（IP 白名单/证书）；超时/重试/幂等键（TaskID）与错误码表对齐；TraceID 必填；MapVersion 校验。
- **WCS/固定设备**: 认证（IP/证书/Topic 级 ACL）；超时/重试，CommandID 幂等；事件推送需带 TraceID。
- **现场设备**: 工控机侧鉴权/端口管理；Point/Tag 访问权限控制；传输 TLS（若协议支持），或隧道加密。
- **加密与保留**: 传输必须 TLS；日志/告警保留周期与审计要求对齐（参见 plan.md Security & Compliance）。
- **隐私/最小必要**: 消息仅含必要字段；敏感数据（如人员账号）不得进入设备接口。

## Traceability
- Spec: FR-003 (接口矩阵)；US2 (Priority P2)
- SRS: docs/SRS.md §3.7.5 接口可靠性保障；§3.2/§3.3 各流程接口描述
- Origin: docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx Sheet: 接口/系统分解（行号待补充）；AGV API SPEC；RCS/WCS/设备协议

## Glossary (Key Terms - Bilingual)
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
