# Validation Scenarios — US2 接口矩阵

> Traceability: Spec FR-003/US2；docs/SRS.md §3.2/§3.3/§3.7.5；Origin: docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx — Sheet “码头到收货暂存区” rows 3-21（GRN/收货链路），Sheet “收货暂存区到料盘装箱区” rows 3-23（装箱链路），Sheet “料盘装箱区到SMT作业区” rows 3-38（发料链路），Sheet “生产退料到SMT清点x-ray&LCR” rows 3-22（退料链路）。

## 场景列表
- **Inbound GRN 同步与上架任务**：SAP→WMS 获取 GRN，WMS→RCS 任务创建，WCS 占位/错误上报，WMS 回写 SAP 库存。
- **SMT 发料/补料**：MES 下发需求，WMS 规划，RCS 任务创建，WCS/设备供料，MES 回执。
- **异常与兜底**：RCS 设备不可用/拥塞，WCS 报警，WMS 改派/重试/人工接管。

## 验证方法
- **模拟/回放**：使用供应商模拟器或录播数据；覆盖上述场景。
- **判定标准**：键/字段齐全；TraceID 贯穿；幂等键生效；错误码映射明确；可产生告警/人工兜底路径。

## 示例载荷（可回放样例）
- **SAP GRN 请求/回传**
```json
{ "PO": "4500123456", "LineItem": "00010", "Material": "MAT-1001", "Vendor": "V-2001", "Batch": "B20251211A", "Qty": 120, "UoM": "EA", "TraceID": "TRC-20251211-0001" }
```

- **MES 发料需求**
```json
{ "ProductionOrder": "MO-78901", "LineItem": "0010", "Material": "MAT-2002", "Qty": 50, "Priority": "High", "BatchConstraints": "FEFO", "TraceID": "TRC-20251211-0002" }
```

- **RCS 搬运任务**
```json
{ "TaskID": "T-AGV-000123", "MapVersion": "v2024.12", "Source": "DOCK-A01", "Target": "IQC-AREA-01", "DeviceType": "E-AGV", "PalletID": "PLT-000567", "Priority": 5, "Status": "Created", "ErrorCode": null, "TraceID": "TRC-20251211-0003" }
```

- **WCS/设备指令**
```json
{ "CommandID": "CMD-000321", "DeviceID": "CONV-01", "Station": "LINE-A-IN", "PalletID": "PLT-000567", "Action": "Feed", "Sensors": ["OK"], "AlarmCode": null, "TraceID": "TRC-20251211-0004" }
```

- **错误码示例**
```json
{ "System": "RCS", "ErrorCode": "DEVICE_UNAVAILABLE", "Retryable": true, "Desc": "AGV offline", "TraceID": "TRC-20251211-0003" }
```
