# WCS 控制接口（WMS → WCS）

**Protocol**: HTTP/REST  
**Auth**: Token/Bearer，TLS  
**TraceRef**: docs/origin/... （待补行号）

## 启停与模式切换（Line Control）
- **Path**: `POST /api/v1/wcs/line/control`
- **Request**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| lineId | string | Y | 流水线/工位标识 |
| command | enum | Y | start / stop / pause / resume |
| reason | string | N | 停机原因 |
| requestId | string | Y | 幂等键 |

- **Response 200**
```json
{ "code": "OK", "message": "accepted" }
```

## 任务下发（Line Task）
- **Path**: `POST /api/v1/wcs/line/tasks`
- **Request**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| taskId | string | Y | WMS 任务号 |
| containerId | string | Y | 容器/托盘 |
| source | string | Y | 起点位 |
| target | string | Y | 终点位 |
| priority | integer | N | 越小越高 |
| requestId | string | Y | 幂等键 |

- **Response 200**
```json
{ "code": "OK", "message": "accepted" }
```

## 状态/告警回传（Line Events）
- 通道：MQTT/SSE（复用 device-telemetry 事件格式），eventType=completed/failed/alarm/heartbeat，附 reasonCode 与位置。

## 错误码/重试
- 标准错误码：DUPLICATE/INVALID_FIELD/LINE_BUSY/WCS_DOWN。  
- 重试：指数退避 ≤3 次，超过转人工兜底并告警。

## 样例与占位
- 缺失的供应商样例需在 contracts/README.md#samples 标记来源/ETA。
