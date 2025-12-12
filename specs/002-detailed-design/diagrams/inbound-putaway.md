# Inbound & Putaway Flows（收货与上架流程设计包）

**Scope**: 收货、上架、补料、退料、发货 P1 主干流与关键异常/补偿分支。  
**TraceRef**: docs/origin/...（待补行号）

## 主路径概述（Main Paths）
- 收货→上架：码头收货 → GRN 同步 → Pallet/Container 绑定 → 质检路由 → 上架下发（WMS→RCS）→ 上架回执。  
- 补料/退料：工单需求 → 任务下发 → RCS/设备执行 → 回执/库存更新。  
- 发货：出库单/波次 → 拣选/集货 → 出库确认。  

## 序列要点（Sequence Highlights）
- 入口条件（Entry Criteria）：GRN 数据同步成功；Pallet/Container 已绑定；任务号/幂等键已生成。  
- 关键交互：  
  - SAP 接口：GRN 查询/创建/回执。  
  - RCS 接口：genAgvSchedulingTask / continueTask / cancelTask / agvCallback / warnCallback。  
  - WCS/设备：line control/task 下发；MQTT/SSE 事件回传；校验接口。  
- 退出条件（Exit Criteria）：位置/库存已落盘，回执已写入，异常已闭环或升级。

## 状态与异常/补偿（State & Exception）
- 状态：accepted → in_progress → completed；failed/exception 需记录 reasonCode 并触发补偿/人工。  
- 异常/补偿：锁冲突、拒单、超时、设备告警 → 重试≤3 → 人工兜底；可用 cancelTask 或重新下发新 taskCode。

## 字段与标识键
- 必含：TaskId、OrderNo、ContainerId、AGVJobId、PositionCode、IdempotencyKey、StepSeq、TraceRef。  
- 单位/枚举：时间 ms/s、数量 pcs、质量 kg、长度 mm、角度 deg；状态枚举 accepted/in_progress/completed/failed/exception。

## 完成判定（Done Criteria）
- 每条主路径/异常路径均具备：序列/状态图、字段表、入口/出口条件、异常/补偿策略、TraceRef 占位。  
- 可直接支撑验收与联调（无 TBD/TODO）。
