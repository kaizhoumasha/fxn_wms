# Data Model — 概要设计阶段启动

> 追溯：参考 docs/SRS.md 与 docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx（按后续具体条目补充 Sheet/Row/段落）。

## 1. 业务模块 (Business Module)
- **属性**: 名称、职责域（入库/存储/SMT 发料/设备协同）、输入/输出、上游依赖、下游消费者。
- **标识**: `ModuleCode`（唯一）。
- **关系**: 关联接口契约；覆盖的关键业务路径列表。

## 2. 接口契约 (Interface Contract)
- **属性**: 交互方（SAP/MES/RCS/WCS/设备）、协议类型（HTTP/Modbus/MQTT/SSE/WebSocket）、触发条件、负载字段清单、QoS/重试/幂等策略、错误代码与兜底。
- **标识**: `ContractID`（唯一）、版本号。
- **关系**: 绑定业务模块；引用数据对象字段；关联异常场景。

## 3. 数据对象 (Data Object)
- **通用属性**: 唯一标识、来源系统、版本/时间戳、校验字段（签名/校验和）。
- **子类型**:
  - **Pallet (栈板)**: PalletID、PalletType、容器容量、绑定 GRN 列表。
  - **Bin/Box (料箱/托)**: BinID、BinType（Type A/Type B）、容积/层位、绑定料盘列表。
  - **Reel/MaterialLot (料盘/批次)**: ReelID/LotID、料号、批次、数量、包装规格、六合一码。
  - **InventorySnapshot**: SnapshotID、Location、Qty、质量状态、锁定标记。
  - **TransportTask (搬运任务)**: TaskID、Source/Target、状态机（创建→派发→执行→完成/异常）、关联设备/AGV。
  - **TraceEvent**: EventID、对象引用、事件类型、时间、操作者/设备来源。
- **关系**: 数据对象与接口契约字段映射；TransportTask 引用具体设备/AGV；InventorySnapshot 关联 Pallet/Bin/Reel。

## 4. 异常场景 (Exception Case)
- **属性**: 异常类型（设备离线/接口超时/数据不一致/库容超限等）、检测方式、告警级别、自动恢复策略、人工兜底步骤。
- **标识**: `ExceptionCode`。
- **关系**: 关联接口契约与业务模块；引用需要锁定/补偿的数据对象。

## 5. 验证工件 (Validation Asset)
- **属性**: 目标（容量/性能/追溯/双语）、验证方法（仿真、回放、演练）、输入数据集/模拟器、判定标准。
- **标识**: `ValidationID`。
- **关系**: 绑定业务模块与接口契约；消费数据对象样例；关联异常场景用于演练。
