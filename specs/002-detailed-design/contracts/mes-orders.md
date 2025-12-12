# MES 生产任务/发料接口（MES ↔ WMS）

**Protocol**: HTTP/REST  
**Auth**: Token/Bearer，TLS  
**TraceRef**: docs/origin/... （待补行号）

## 拉取生产工单（Fetch Production Orders）
- **Path**: `POST /api/v1/mes/orders/query`
- **Request**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| orderNo | string | N | 指定工单 |
| status | enum | N | released / in_progress |
| requestId | string | Y | 幂等键 |
| issuedAt | datetime | Y | UTC |

- **Response 200**
```json
{ "code": "OK", "orders": [ { "orderNo": "WO123", "material": "MAT-9001", "qty": 1000, "line": "SMT-01", "due": "2025-12-20T00:00:00Z" } ] }
```

## 投料反馈（Material Issue Feedback）
- **Path**: `POST /api/v1/mes/issues`
- **Request**

| Field | Type | Req | Unit | Notes |
|-------|------|-----|------|-------|
| orderNo | string | Y | - | 工单号 |
| taskId | string | Y | - | WMS 任务号 |
| containerId | string | Y | - | 料箱/托盘 |
| material | string | Y | - | 物料编码 |
| qty | number | Y | pcs | 投料数量 |
| location | string | N | - | 投料位 |
| issuedAt | datetime | Y | UTC | 投料时间 |
| requestId | string | Y | - | 幂等键 |

- **Response 200**
```json
{ "code": "OK", "message": "accepted" }
```

- **Error Codes**
| code | retryable | description |
|------|-----------|-------------|
| DUPLICATE | false | 幂等重复 |
| INVALID_ORDER | false | 工单无效 |
| MES_DOWN | true | MES 不可用，需重试 |

## 样例与占位
- 若缺少 MES 样例，由 MES 提供；缺口与 ETA 记录于 contracts/README.md#samples。
