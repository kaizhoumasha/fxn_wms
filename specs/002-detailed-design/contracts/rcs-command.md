# WMS → RCS/AGV 指令（Command to RCS/AGV）

**Protocol**: HTTP/REST  
**Auth**: Token/Bearer，TLS  
**Base Path**: `https://<rcs-host>/rcms/services/rest/hikRpcService/`（遵循 `docs/origin/AGV API SPEC_20220902(V2).xlsx` + `docs/origin/灿态WMS与RCS已对接清单(20250717).docx`）  
**TraceRef**: 请在实现时补充对应行号

## 下发搬运任务 genAgvSchedulingTask（Dispatch）

- **Method/Path**: `POST /rcms/services/rest/hikRpcService/genAgvSchedulingTask`
- **Request Fields（按原始接口）**

| Field | Type | Req | Notes |
|-------|------|-----|-------|
| agvCode | string | N | AGV 编号 |
| taskCode | string | Y | 搬运任务号（WMS 生成并与 RCS 对齐） |
| taskTyp | string | Y | 任务类型（例：CK02） |
| ctnrTyp | string | N | 容器类型 |
| ctnrCode | string | N | 容器编码 |
| wbCode | string | N | 工位/工控位编码 |
| positionCodePath | array | Y | 位置列表，每项包含 `positionCode`、`type`（00/03 等） |
| podCode | string | Y | 货架/Pod 编号 |
| podDir | string | Y | 货架方向（0/180 等） |
| podTyp | string | N | 货架类型 |
| materialLot | string | N | 料批 |
| priority | string | N | 优先级，数字越小越高 |
| data | string | Y | 业务标识，例如 `WMS_SHELF_MOVE_TASK` |
| reqCode | string | Y | 请求唯一标识（幂等/对账键之一） |
| reqTime | datetime | Y | 请求时间 |
| clientCode | string | Y | 调用方标识（例：MES-1-1） |
| tokenCode | string | N | 令牌 |

- **Response 200**
```json
{ "code": "0", "message": "成功", "reqCode": "d045749bb47c4dc1acad3a0a856979ac", "data": "3E94305EB994406A9405EDA53A76C762" }
```

- **调用示例（Dispatch Example，源自对接清单）**
```bash
curl -X POST https://<rcs-host>/rcms/services/rest/hikRpcService/genAgvSchedulingTask \
  -H "Content-Type: application/json" \
  -d '{
    "agvCode": null,
    "taskCode": "3E94305EB994406A9405EDA53A76C762",
    "taskTyp": "CK02",
    "ctnrTyp": null,
    "ctnrCode": null,
    "wbCode": null,
    "positionCodePath": [
      { "positionCode": "410069", "type": "03" },
      { "positionCode": "RK1501", "type": "00" }
    ],
    "podCode": "410069",
    "podDir": "0",
    "podTyp": null,
    "materialLot": null,
    "priority": "9",
    "data": "WMS_SHELF_MOVE_TASK",
    "reqCode": "d045749bb47c4dc1acad3a0a856979ac",
    "reqTime": "2021-12-29 10:33:15",
    "clientCode": "MES-1-1",
    "tokenCode": null
  }'
```

## 继续任务 continueTask（Next Step）

- **Method/Path**: `POST /rcms/services/rest/hikRpcService/continueTask`
- **关键字段**：`taskCode`（必填），`taskSeq`（步骤序号），`nextPositionCode`（位置+type），`reqCode`，`reqTime`，`clientCode`，`tokenCode`。
- **示例**
```bash
curl -X POST https://<rcs-host>/rcms/services/rest/hikRpcService/continueTask \
  -H "Content-Type: application/json" \
  -d '{
    "agvCode": null,
    "taskCode": "630EFBC79D8346D49658A73633438914",
    "wbCode": null,
    "podCode": null,
    "taskSeq": "2",
    "nextPositionCode": { "positionCode": "RK1501", "type": "00" },
    "reqCode": "4d60cb2dfcb940ebb6484b6a5cf34964",
    "reqTime": "2021-12-29 10:33:14",
    "clientCode": "MES-1-1",
    "tokenCode": null
  }'
```

## 取消任务 cancelTask（Optional）
- **Path**: `POST /rcms/services/rest/hikRpcService/cancelTask`
- **示例（对接清单）**
```json
{"reqCode": "4d60cb2dfcb940ebb6484b6a5cf34910", "reqTime": "2021-12-29 10:33:15", "clientCode": "MES-1-1", "tokenCode": "", "forceCancel": "1", "matterArea": "abc", "agvCode": "", "taskCode": "630EFBC79D8346D49658A73633438914"}
```

## 任务状态回调 agvCallback（RCS → WMS）

- **Method/Path**: `POST /wms/agv/agvCallbackService/agvCallback`
- **Payload 字段（原样对齐）**

| Field | Notes |
|-------|-------|
| cooX / cooY | 坐标 |
| currentPositionCode | 当前点位 |
| data | 业务标识，例如 `"WMS_SHELF_MOVE_TASK"` |
| mapCode / mapDataCode | 地图/点位 |
| method | start / outbin / arrive / end / cancel （可映射 accepted/in_progress/completed/failed）|
| podCode / podDir | 货架与方向 |
| robotCode | 车号 |
| taskCode | 搬运任务号 |
| wbCode | 工位 |
| reqCode / reqTime / clientCode / tokenCode | 请求标识 |

- **示例**
```bash
curl -X POST https://<wms-host>/wms/agv/agvCallbackService/agvCallback \
  -H "Content-Type: application/json" \
  -d '{
    "cooX": "54200.0",
    "cooY": "54662.0",
    "currentPositionCode": "RK1501",
    "data": "\"WMS_SHELF_MOVE_TASK\"",
    "mapCode": "AA",
    "mapDataCode": "054200AA054662",
    "method": "start",
    "podCode": "410125",
    "podDir": "",
    "robotCode": "3521",
    "taskCode": "8317507889E2477FB36284FFF739E2BF",
    "wbCode": "RK1501",
    "reqCode": "17E041343A4Z7II",
    "reqTime": "2021-12-29 10:44:38",
    "clientCode": "",
    "tokenCode": ""
  }'
```

### 状态枚举与异常处理
- 状态映射：  
  - `start`/`outbin` → `accepted`/`in_progress`  
  - `arrive` → `in_progress`  
  - `end` → `completed`  
  - `cancel` → `failed`（需 reasonCode）  
- 异常与告警：若 `code != 0` 或缺失字段，WMS 记录告警并可退避重试；拒单/异常需携带 `reasonCode`，可触发人工兜底。

## 告警推送 warnCallback（RCS → WMS）

- **Path**: `POST /wms/agv/agvCallbackService/warnCallback`
- **示例**
```json
{
  "reqCode": "1541954B96B1112",
  "reqTime": "",
  "clientCode": "",
  "tokenCode": "",
  "data:": [
    { "robotCode": "1001", "beginDate": "2020-04-02 23:12:12", "warnContent": "平台失联", "taskCode": "C002WWQQRR" },
    { "robotCode": "1002", "beginDate": "2020-04-02 23:12:12", "warnContent": "导航告警", "taskCode": "C002WWQQRR33" }
  ]
}
```

> 说明：本文件的调用示例直接采用对接清单/AGV API SPEC 中的字段与结构，避免自定义字段导致偏离；实现时需将 TraceRef 补充到行级来源。
