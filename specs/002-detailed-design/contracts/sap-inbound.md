# SAP ↔ WMS 入库/出库同步（Inbound/Outbound）契约

**Protocol**: HTTP/REST  
**Auth**: Token/Bearer，TLS  
**Idempotency**: `IdempotencyKey = TaskId + OrderNo`  
**TraceRef**: docs/origin 行号需在实现时补充

## 收货数据同步（Request_GRN / Return_GRN_List）

- **Method/Path**: `POST /api/v1/sap/grn/query`
- **Purpose**: 获取 GRN 列表（PO/行/批次/数量/供应商）作为收货任务生成依据（对应 SRS Step 1）
- **Request Fields**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| poNumber | string | Y | PO/采购单号 |
| trackingId | string | N | 物流跟踪号 |
| vendorCode | string | N | 供应商代码 |
| requestId | string | Y | 请求幂等键 |
| issuedAt | datetime | Y | UTC |

- **Response 200**
```json
{
  "code": "OK",
  "message": "success",
  "grnList": [
    { "po": "PO123", "lineItem": "10", "material": "MAT-9001", "batch": "B001", "qty": 120, "vendor": "V001" }
  ]
}
```

- **Error Codes**
| code | retryable | description |
|------|-----------|-------------|
| SAP_DOWNSTREAM | true | SAP 不可用，稍后重试 |
| INVALID_PO | false | PO/Tracking_ID 无效 |
| NO_DATA | false | 无匹配 GRN |

### 调用示例（GRN Query Example）

```bash
curl -X POST https://wms.example.com/api/v1/sap/grn/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "poNumber": "PO123",
    "trackingId": "TRK-001",
    "vendorCode": "V001",
    "requestId": "REQ-PO123-TRK001",
    "issuedAt": "2025-12-12T01:00:00Z"
  }'
```

## 请求：创建/更新单据（Create/Update Order）

- **Method/Path**: `POST /api/v1/orders`（创建）；`PUT /api/v1/orders/{orderNo}`（更新）
- **Request Fields**

| Field | Type | Req | Unit | Notes |
|-------|------|-----|------|-------|
| orderNo | string | Y | - | 业务单号（ASN/SO） |
| taskId | string | Y | - | WMS 任务号 |
| orderType | enum | Y | - | inbound / outbound |
| containerId | string | Y | - | 托盘/周转箱 ID |
| skuCode | string | Y | - | 物料编码 |
| qty | number | Y | pcs | 数量 |
| uom | string | Y | - | 计量单位 |
| warehouse | string | Y | - | 仓库代码 |
| fromLocation | string | N | - | 来源位 |
| toLocation | string | N | - | 目的位 |
| idempotencyKey | string | Y | - | 去重键 |
| issuedAt | datetime | Y | UTC | 下发时间 |

- **Response 200**
```json
{ "code": "OK", "message": "accepted", "taskId": "T123", "orderNo": "SO001" }
```

- **Error Codes**
| code | retryable | description |
|------|-----------|-------------|
| DUPLICATE | false | 已存在且内容一致 |
| INVALID_FIELD | false | 字段缺失或不合法 |
| LOCKED | true | 资源锁冲突，可重试 |
| SAP_DOWNSTREAM | true | SAP 不可用，稍后重试 |

### 调用示例（Example）

**创建单据 Create**
```bash
curl -X POST https://wms.example.com/api/v1/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "orderNo": "ASN-20251212-001",
    "taskId": "T-10001",
    "orderType": "inbound",
    "containerId": "PALT-001",
    "skuCode": "MAT-9001",
    "qty": 120,
    "uom": "pcs",
    "warehouse": "WH-A",
    "fromLocation": "DOCK-01",
    "toLocation": "STAGE-01",
    "idempotencyKey": "T-10001-ASN-20251212-001",
    "issuedAt": "2025-12-12T01:02:03Z"
  }'
```

## 回执：状态变更（Status Callback）

- **Method/Path**: `POST /api/v1/orders/{orderNo}/callbacks`
- **Request Fields**

| Field | Type | Req | Unit | Notes |
|-------|------|-----|------|-------|
| orderNo | string | Y | - | 业务单号 |
| taskId | string | Y | - | WMS 任务号 |
| status | enum | Y | - | accepted / in_progress / completed / failed |
| reasonCode | string | N | - | 失败/告警原因 |
| completedAt | datetime | N | UTC | 完成时间 |
| ackAt | datetime | Y | UTC | 接单/接收时间 |
| idempotencyKey | string | Y | - | 去重键 |

- **Response 200**
```json
{ "code": "OK", "message": "received" }
```

- **Error Codes**
| code | retryable | description |
|------|-----------|-------------|
| UNKNOWN_ORDER | false | 未找到 orderNo |
| DUPLICATE | false | 重复回执（相同幂等键） |
| INVALID_STATUS | false | 状态非法 |
| SAP_DOWNSTREAM | true | SAP 不可用，重试 |

### 回执示例（Callback Example）

```bash
curl -X POST https://wms.example.com/api/v1/orders/ASN-20251212-001/callbacks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "orderNo": "ASN-20251212-001",
    "taskId": "T-10001",
    "status": "completed",
    "reasonCode": null,
    "completedAt": "2025-12-12T03:04:05Z",
    "ackAt": "2025-12-12T01:02:05Z",
    "idempotencyKey": "T-10001-ASN-20251212-001"
  }'
```
