# US2 Sequence Diagrams — 接口契约与时序

> Traceability: Spec FR-003 / US2；docs/SRS.md §3.2/§3.3 流程接口描述，§3.7.5 接口可靠性保障；Origin: docs/origin/休斯顿P9自动化仓库功能分解清单_202511021.xlsx Sheet: 接口/系统分解（行号待补充）。

## 收货→上架 (SAP/MES/RCS/WCS)

```mermaid
sequenceDiagram
    participant SAP
    participant WMS
    participant RCS as RCS/AGV
    participant WCS as WCS/Conveyor
    SAP->>WMS: Request_GRN(PO/Line/Batch) [HTTP]
    WMS-->>SAP: GRN_List (GRN, Material, Qty, Batch)
    WMS->>RCS: CreateTask(TaskID, Src=Dock, Dst=IQC/Buffer, PalletID)
    RCS-->>WMS: TaskStatus(Dispatched/Exception)
    WMS->>WCS: Notify conveyor/slot allocation (CommandID, PalletID)
    WCS-->>WMS: Slot status / ErrorCode
    RCS-->>WMS: TaskStatus(Done)
    WMS-->>SAP: Inventory update (PalletID/GRN/Qty/Location)
```

## SMT 发料 (MES/RCS/WCS/设备)

```mermaid
sequenceDiagram
    participant MES
    participant WMS
    participant RCS as RCS/AGV
    participant WCS as WCS/Line/机械臂
    MES->>WMS: Demand(ProductionOrder, Material, Qty, Priority)
    WMS->>WMS: Plan pick/replenish/urgent
    WMS->>RCS: CreateTask(TaskID, Src=Storage, Dst=Line, BinID/ReelID)
    RCS-->>WMS: TaskStatus(Exec/Exception)
    WMS->>WCS: Feed command (CommandID, BinID, Slot, Params)
    WCS-->>WMS: Status/Alarm/Completion
    WMS-->>MES: Issue/Trace feedback (Qty, Batch, TraceID)
```

## 异常/兜底 (接口超时/设备不可用)

```mermaid
sequenceDiagram
    participant WMS
    participant RCS
    participant WCS
    WMS->>RCS: CreateTask/CancelTask
    RCS-->>WMS: Exception(ErrorCode=DeviceUnavailable/Congestion)
    WMS->>WMS: Reassign/Retry or escalate manual takeover
    WMS->>WCS: Pause/Redirect command
    WCS-->>WMS: Ack/Alarm
```

## Payload & Keys (摘要)

| System | Keys | Payload Highlights | Error/Retry |
| ------ | ---- | ------------------ | ----------- |
| SAP | PO, LineItem, GRN, Batch | Material, Qty, Vendor, Timestamps | 4xx manual fix; 5xx retry+alert |
| MES | ProductionOrder, LineItem | Material, Qty, Priority, BatchConstraints | 4xx manual; 5xx retry+alert |
| RCS | TaskID, MapVersion | Source/Target, DeviceType, Priority, Status, ErrorCode | Retry/redirect, manual takeover |
| WCS/设备 | CommandID, DeviceID | Action, PalletID/BinID, Sensors, AlarmCode | Recoverable flag, manual fallback |
