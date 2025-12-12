# WCS/设备状态回传（Device Telemetry）

**Protocol**: MQTT 或 SSE（供应商可择一提供）  
**Auth**: 按通道配置（TLS + Token/Client Cert）  
**Security**: 传输需 TLS，敏感字段可脱敏日志，所有告警需审计留痕。  
**Idempotency**: 由 `eventId` + `containerId` + `occurredAt` 防重  
**TraceRef**: docs/origin 行号需在实现时补充

## 设备类型与通道（Device Types & Channels）

| DeviceType | Channel | Purpose |
|------------|---------|---------|
| Conveyor/流水线 | MQTT/SSE | 运行/堵塞/缓存位状态、心跳与告警 |
| RobotArm/机械臂 | MQTT/SSE | PickDone/Fail、位置、原因码 |
| AutoUnpack/拆包机 | MQTT/SSE | 拆包结果、扫码/称重校验、异常 |
| Vision/LCR/X-Ray | MQTT/SSE | 检测结果、Fail 原因、样本 ID |
| Print/Labeler | MQTT/SSE | 打印成功/失败、标签校验 |

## MQTT 主题与负载

- **Topic Pattern**: `wcs/{deviceId}/events`  
- **Payload (JSON)**
```json
{
  "eventId": "evt-123",
  "deviceId": "DEV-01",
  "taskId": "T123",
  "containerId": "PALT-001",
  "eventType": "completed",
  "status": "ok",
  "reasonCode": null,
  "location": "A1-01",
  "occurredAt": "2025-12-12T01:02:03Z"
}
```

- **Fields**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| eventId | string | Y | 幂等标识 |
| deviceId | string | Y | 设备/站点 |
| taskId | string | Y | WMS 任务号 |
| containerId | string | Y | 托盘/箱 |
| eventType | enum | Y | completed / failed / alarm / heartbeat |
| status | string | Y | ok / warn / error |
| reasonCode | string | N | 告警/失败原因 |
| location | string | N | 物理位 |
| occurredAt | datetime | Y | UTC |

- **QoS & Retry**
  - MQTT: QoS 1，消费者去重（eventId）。  
  - SSE: 客户端断线使用 `Last-Event-ID` 续传。

### MQTT 订阅示例（Subscribe Example）

```bash
mosquitto_sub -h mqtt.example.com -p 8883 \
  -u "wms" -P "<token>" --cafile ca.pem \
  -t "wcs/DEV-01/events" -q 1
```

## SSE 事件流

- **Endpoint**: `GET /api/v1/wcs/events/stream`  
- **Headers**: `Accept: text/event-stream`  
- **Event Format**: 标准 SSE，`id`=eventId，`data` 为与 MQTT 相同的 JSON。

### SSE 调用示例（Call Example）

```bash
curl -N -H "Accept: text/event-stream" \
  -H "Authorization: Bearer <token>" \
  https://wms.example.com/api/v1/wcs/events/stream
```

## 错误与告警处理
- 供应商侧发送失败需本地重试≤3 次；超出触发本地告警并记录。  
- WMS 接收端若解析失败，返回 4xx 并记录告警，供应商可根据响应决定补发。  
- 所有告警/失败事件需要 reasonCode 与发生位置（location）便于排障。
- 事件分类建议：`eventType` 采用 completed/failed/alarm/heartbeat，与 RCS 回调的状态保持一致，保证追溯与对账。

## 设备请求校验（Validation Request，设备→WMS）

- **Channel**: HTTP `POST /api/v1/wcs/validate`（若供应商仅支持 MQTT，可用 `wcs/{deviceId}/validate` 同步 RPC 通道约定）  
- **Fields**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| deviceId | string | Y | 设备/站点 |
| taskId | string | N | 关联任务 |
| containerId | string | N | 容器/托盘 |
| slot | string | N | 货位/槽位 |
| barcode | string | Y | 扫描码/料盘码 |
| weight | number | N | 称重值（若有） |
| imageRef | string | N | 视觉结果引用 |
| requestId | string | Y | 幂等键 |

- **Response 200**
```json
{ "allow": true, "reason": null, "normalizedCode": "PKG-123", "taskId": "T-9001" }
```
- **Response 400**
```json
{ "allow": false, "reason": "BARCODE_MISMATCH", "hint": "expected SO123-line10" }
```

### 校验示例（拆包机/机械臂扫码校验）

```bash
curl -X POST https://wms.example.com/api/v1/wcs/validate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "AUTO-UNPACK-01",
    "taskId": "T-30001",
    "containerId": "BIN-001",
    "slot": "S1",
    "barcode": "PKG-ABC-001",
    "weight": 123.4,
    "requestId": "REQ-VAL-30001-1"
  }'
```

## 设备事件扩展示例（Device-specific Events）

### Conveyor/流水线
```json
{
  "eventId": "evt-conv-1",
  "deviceId": "CONV-01",
  "eventType": "alarm",
  "status": "jammed",
  "reasonCode": "JAM_SENSOR_TRIP",
  "location": "INTAKE-01",
  "occurredAt": "2025-12-12T02:10:00Z"
}
```

### RobotArm/机械臂
```json
{
  "eventId": "evt-robot-1",
  "deviceId": "ROBOT-01",
  "eventType": "completed",
  "taskId": "T-40001",
  "containerId": "BIN-009",
  "payload": { "action": "PickDone", "from": "RACK-A1", "to": "LINE-01" },
  "occurredAt": "2025-12-12T02:15:00Z"
}
```

### AutoUnpack/拆包机
```json
{
  "eventId": "evt-unpack-1",
  "deviceId": "UNPACK-01",
  "eventType": "completed",
  "taskId": "T-50001",
  "containerId": "BOX-123",
  "payload": { "barcode": "PKG-ABC-001", "result": "pass", "pieces": 50 },
  "occurredAt": "2025-12-12T02:20:00Z"
}
```

### Vision / LCR / X-Ray
```json
{
  "eventId": "evt-lcr-1",
  "deviceId": "LCR-01",
  "eventType": "failed",
  "taskId": "T-51001",
  "containerId": "BIN-777",
  "payload": { "measure": "resistance", "value": 120.5, "threshold": 100, "unit": "ohm" },
  "reasonCode": "OUT_OF_TOLERANCE",
  "occurredAt": "2025-12-12T02:25:00Z"
}
```
