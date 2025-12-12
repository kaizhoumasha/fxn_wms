# Observability & Alerts — US3

> Traceability: FR-005/FR-006/FR-009；docs/SRS.md §3.7 系统控制与可靠性；Origin: docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx — Sheet “码头到收货暂存区” rows 22-36（异常/要求）；Sheet “收货暂存区到料盘装箱区” rows 17-23（异常/节拍）；Sheet “料盘装箱区到SMT作业区” rows 30-38（异常/性能/交换）；Sheet “生产退料到SMT清点x-ray&LCR” rows 3-22（退料与检测异常）。

## Signals
- **Task Latency (RCS)**: 下发→确认 p95，目标 ≤ 10s；字段 TaskID, TraceID。
- **Interface Success Rate**: SAP/MES/RCS/WCS 调用成功率，目标 ≥ 99%；统计 TraceID。
- **Device Availability**: RCS/设备在线率，目标 ≥ 95%；Source=DeviceID/MapVersion。
- **Queue Depth**: 关键队列积压（搬运任务、接口重试队列），阈值按业务峰值设定。
- **Alarm Rate**: 告警/任务比，异常升高触发 P1。

## Alerts (Thresholds)
- **P1**: RCS 时延 p95 > 10s；接口成功率 < 99%；设备在线率 < 95%；重试队列 > 阈值。
- **P2**: 队列接近阈值；设备短暂离线恢复。

## Tracing
- **Trace Fields**: TraceID/CorrelationID, TaskID/CommandID, DeviceID, PalletID/BinID/ReelID, MapVersion, Timestamp.
- **Propagation**: SAP/MES/RCS/WCS/设备报文均带 TraceID；日志中对齐。

## Validation Steps
- **Simulate/Replay**: 结合 us2-scenarios，测量时延/成功率；记录指标。
- **Alert Drill**: 触发 P1/P2 阈值，验证告警分级与通知。
- **Fallback Link**: 告警对应 playbooks/us3-fallback.md，确保可人工接管/改派。
