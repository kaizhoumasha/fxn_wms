# 硬件接入标准 (Hardware Interface Standard)

> **⚠️ 重要提示**:
> - **权威文档层级**: SRS.md > third_party_integration_whitepaper.md > 本文档
> - 第三方 ECS 设备接入必须遵循 `@docs/third_party_integration_whitepaper.md`
> - 本文档的 ECS 章节（第 3.2 节）是白皮书的内部实现指南
> - 所有规范必须符合 `@docs/SRS.md` 第 3.7.3 节（异常处理）和第 4.2 节（南向接口）

## 1. 概述 (Overview)

本标准定义了 WES 南向接口的统一硬件接入规范，基于 SRS 第 3 章应用场景提炼而成。

### 1.1 文档范围

**本文档分为两部分**:

#### Part A: 第三方设备接入（遵循白皮书规范）
- **ECS (Equipment Control System)** - 机械臂、输送线、堆垛机、贴标机、分拣机
- **适用对象**: 外部供应商、集成商
- **权威文档**: `@docs/third_party_integration_whitepaper.md`
- **状态**: ✅ 生产环境

#### Part B: 内部系统接口（WES 内部规范）
- **RCS** - AGV 调度系统（暂由现有 WMS 管理，未来迁移至 WES）
- **PDA** - 手持终端
- **QMS** - 质量管理系统
- **SFC** - 车间控制系统
- **适用对象**: WES 开发团队
- **状态**: 🚧 规划中/内部使用

**重要**: ECS 相关章节必须与白皮书保持 100% 一致。

### 1.2 设计原则

- **供应商无关 (Vendor-Agnostic)**: 核心逻辑不依赖特定硬件协议
- **插件化架构 (Plugin Architecture)**: 通过协议适配器隔离硬件差异
- **幂等性保证 (Idempotency)**: 支持重试而不产生副作用
- **状态一致性 (State Consistency)**: 物理状态与数字状态同步验证

---

## 2. 通用硬件接口 (Universal Hardware Interface, UHI)

### 2.1 接口定义

所有硬件系统必须实现以下抽象接口:

```python
class IHardwareAdapter(ABC):
    """硬件适配器基类"""

    @abstractmethod
    async def send_command(self, command: Command) -> Response:
        """发送命令到硬件"""
        pass

    @abstractmethod
    async def query_status(self, resource_id: str) -> Status:
        """查询硬件资源状态"""
        pass

    @abstractmethod
    async def subscribe_events(self, callback: Callable) -> None:
        """订阅硬件事件 (异步通信)

        注意: ECS 不使用此方法，而是通过 HTTP 回调通知 WES
        详见白皮书第 3.2 节和本文档第 3.2 节
        """
        pass
```

### 2.2 命令封装格式

**注意**: 以下为 WES 内部通用格式。ECS 设备使用白皮书定义的格式（`task_type` 和 `params` 字段），详见第 3.2 节。

```json
{
  "command_id": "uuid",
  "device_type": "RCS|ECS|PDA|QMS|SFC",
  "command_type": "Transport|Exchange|Verify_Empty|...",
  "parameters": { /* 设备特定参数 */ },
  "idempotency_key": "unique_key",
  "timeout_ms": 10000,
  "retry_policy": {
    "max_attempts": 3,
    "backoff_ms": 1000
  }
}
```

### 2.3 响应封装格式

```json
{
  "command_id": "uuid",
  "status": "SUCCESS|FAILED|TIMEOUT|REJECTED",
  "result": { /* 设备特定结果 */ },
  "error_code": "E001",
  "error_message": "描述性错误信息",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

---

## 3. 设备类型与命令分类

### 3.1 RCS (Robot Control System)

**职责**: AGV 调度、货架搬运、路径规划

#### 命令类型

| 命令 | 参数 | 响应 | 场景 |
|------|------|------|------|
| `Transport` | `from_location`, `to_location`, `rack_id` | `task_id`, `status` | 货架搬运 |
| `Exchange` | `location_a`, `location_b`, `rack_id_a`, `rack_id_b` | `task_id`, `status` | 货架交换 |
| `Rotate` | `location`, `rack_id`, `target_side` (A/B) | `task_id`, `status` | 五层货架旋转 |

#### 状态查询

```json
{
  "task_id": "RCS-20251215-001",
  "status": "Pending|In_Progress|Completed|Failed|Suspended",
  "current_location": "A-01",
  "progress_percent": 75,
  "estimated_completion": "2025-12-15T10:35:00Z"
}
```

#### 事件订阅

- `TaskStarted`: AGV 开始执行任务
- `TaskCompleted`: 任务完成，货架到达目标位置
- `TaskFailed`: 任务失败 (障碍物、AGV 故障)
- `LocationOccupied`: 目标位置被占用

---

### 3.2 ECS (Equipment Control System)

> **⚠️ 本章节遵循白皮书规范**:
> - 命令格式必须与 `@docs/third_party_integration_whitepaper.md` 第 3.1.1 节完全一致
> - 使用 `task_type` 和 `params` 字段（不是 `command_type` 和 `parameters`）
> - 通信协议仅支持 HTTP/HTTPS + JSON

**职责**: 料盘检测、上下料、X-Ray 检测、标签打印

#### 命令格式（白皮书标准）

```json
{
  "command_id": "CMD-20251215-1001",
  "task_type": "PUT_INSTRUCTION",
  "priority": 1,
  "timeout": 30000,
  "params": {
    "source_loc": "BIN-01-A",
    "target_loc": "CONVEYOR-02",
    "material_code": "M123456",
    "quantity": 10
  },
  "timestamp": 1702627200000
}
```

#### 响应格式（白皮书标准）

```json
{
  "code": 200,
  "message": "Accepted",
  "trace_id": "DEV-LOG-998877"
}
```

#### 命令类型（task_type 枚举值）

| task_type | params 字段 | 响应 | 场景 |
|-----------|------------|------|------|
| `PUT_INSTRUCTION` | `bin_id`, `slot_id`, `pkg_code` | `code: 200/400/503` | 指导上料 |
| `PICK` | `bin_id`, `slot_id` | `code: 200`, `data.actual_qty` | 指导下料 |
| `SCAN` | `bin_id`, `slot_id` | `code: 200`, `data.scan_result` | 扫码/视觉识别 |
| `PROCESS` | `operation_type`, `target` | `code: 200` | 加工/检测（X-Ray、贴标等） |

**注意**:
- 上表为白皮书定义的标准 task_type 值
- 具体 params 字段根据实际业务场景扩展
- 详细定义见白皮书第 5.1 节（数据字典）

#### 回调机制（白皮书规范）

**ECS 不使用 `subscribe_events()` 方法**，而是通过 HTTP 回调通知 WES：

**供应商必须调用的 WES 接口**:

1. **任务结果回传**:
   ```
   POST http://<WES_IP>:<PORT>/api/v1/callback/result
   Body: {
     "command_id": "CMD-20251215-1001",
     "device_id": "ARM_01",
     "result": "SUCCESS|FAILED",
     "finish_time": 1702627250000,
     "data": { "actual_qty": 10, "scan_result": "PKG-X-99" },
     "error_detail": { "code": "E-MOTOR-01", "msg": "..." }
   }
   ```

2. **设备事件上报**:
   ```
   POST http://<WES_IP>:<PORT>/api/v1/callback/event
   Body: {
     "device_id": "ARM_01",
     "event_type": "ESTOP_PRESSED",
     "timestamp": 1702627300000
   }
   ```

详见白皮书第 3.2 节。

#### 失败处理

- `result: FAILED` + `error_detail.code: "PUT_FAIL"` → WES 标记 Slot 异常，重新分配
- `result: FAILED` + `error_detail.code: "PICK_FAIL"` → WES 扣减库存，标记 `Shortage`，尝试备选库存

---

### 3.3 PDA (Portable Data Acquisition)

**职责**: 人工扫码、绑定操作、手动指导

#### 命令类型

| 命令 | 参数 | 响应 | 场景 |
|------|------|------|------|
| `Scan_PKG` | `pallet_id` | `pkg_code`, `material`, `qty` | 扫描六合一码 |
| `Bind_Pallet` | `pallet_id`, `pkg_list` | `result: SUCCESS|FAIL` | 绑定栈板 |
| `Manual_Guide` | `instruction_text`, `target_location` | `confirmation: bool` | 人工指导界面 |
| `Verify_Label` | `new_pkg_code` | `result: SUCCESS|FAIL` | 换标后验证 |

#### 校验规则

- `Sum(Current_Qty) <= GRN.Remaining_Qty`: 防止超收
- `PKG.Format == "6-in-1"`: 强制六合一码格式
- `PKG.Material IN Master_Data`: 物料主数据校验

---

### 3.4 QMS (Quality Management System)

**职责**: 抽检策略、检验结果回传

#### 命令类型

| 命令 | 参数 | 响应 | 场景 |
|------|------|------|------|
| `Sampling_Request` | `material`, `vendor`, `qty` | `sampling_qty` | 请求抽检数量 |
| `Inspection_Result` | `grn_id`, `result: OK|NG` | `ack` | 检验结果回传 |

#### 业务规则

- `SamplingQty > 0` → WES 生成 `Route_Task(To IQC_Area)`
- `Result = NG` → WES 指导 PDA 拆板作业，隔离 NG 物料

---

### 3.5 SFC (Shop Floor Control)

**职责**: 产线需求、追溯数据

#### 命令类型

| 命令 | 参数 | 响应 | 场景 |
|------|------|------|------|
| `Magazine_Request` | `line_id`, `material`, `qty` | `task_id` | 产线呼叫料盘 |
| `Traceability_Push` | `pkg_code`, `production_data` | `ack` | 推送追溯数据 |

---

## 4. 通信模式 (Communication Patterns)

### 4.1 同步模式 (Synchronous)

**适用场景**: 状态查询、快速验证

```
WES → Hardware: Request
WES ← Hardware: Response (立即返回)
```

**示例**: `Verify_Empty`, `Check_Material`

---

### 4.2 异步模式 (Asynchronous)

**适用场景**: 长时间任务 (AGV 搬运)

```
WES → RCS: Transport_Command
WES ← RCS: Task_ID (立即返回)
...
WES ← RCS: TaskCompleted_Event (异步回调)
```

**实现要求**:
- 硬件必须提供 `task_id` 用于后续查询
- WES 通过 `subscribe_events` 接收异步事件
- 超时后 WES 主动查询 `query_status`

---

### 4.3 双向握手模式 (Bidirectional Handshake)

**适用场景**: 关键操作需要确认 (入库确认)

```
WES → WMS: Inbound_Confirm
WES ← WMS: ACK
WES → Hardware: Execute_Physical_Action
WES ← Hardware: Result
WES → WMS: Final_Confirm
```

---

## 5. 错误处理与重试机制

### 5.1 自动重试策略

```python
retry_policy = {
    "max_attempts": 3,
    "initial_backoff_ms": 1000,
    "backoff_multiplier": 2.0,
    "max_backoff_ms": 10000,
    "timeout_per_attempt_ms": 10000
}
```

**重试条件**:
- 网络超时 (`TIMEOUT`)
- 临时故障 (`TEMPORARY_ERROR`)
- 硬件繁忙 (`BUSY`)

**不重试条件**:
- 参数错误 (`INVALID_PARAMETER`)
- 资源不存在 (`NOT_FOUND`)
- 业务规则拒绝 (`REJECTED`)

---

### 5.2 失败处理流程

```
1. 标记任务失败: Task_Status = Failed
2. 通知上游系统: WMS/SAP
3. 记录异常日志: Exception_Log(TaskID, Reason, Timestamp)
4. 触发人工介入: 若 3 次重试失败
```

---

### 5.3 幂等性保证

**实现方式**:
- 每个命令携带 `idempotency_key` (基于业务 ID 生成)
- 硬件适配器缓存已执行命令的 `idempotency_key`
- 重复请求返回缓存结果，不重复执行物理动作

**示例**:
```python
idempotency_key = f"{grn_id}:{pallet_id}:{operation_type}"
```

---

## 6. 状态机定义

### 6.1 任务生命周期

```
Pending (待执行)
  ↓
In_Progress (执行中)
  ↓
Completed (完成) / Failed (失败) / Suspended (挂起)
```

### 6.2 状态转换规则

| 当前状态 | 事件 | 目标状态 | 条件 |
|---------|------|---------|------|
| Pending | Start | In_Progress | 资源可用 |
| In_Progress | Success | Completed | 物理动作完成 |
| In_Progress | Error | Failed | 3 次重试失败 |
| In_Progress | Pause | Suspended | 人工干预 |
| Suspended | Resume | In_Progress | 问题解决 |
| Failed | Retry | Pending | 人工重置 |

---

## 7. 协议适配器实现指南

### 7.1 支持的协议

| 协议 | 适用设备 | 状态 | 实现类 | SRS 依据 |
|------|---------|------|--------|---------|
| **HTTP/HTTPS** | **ECS (白皮书规范)** | ✅ 生产 | `HttpAdapter` | SRS 4.2 |
| HTTP/REST | RCS, QMS, SFC | 🚧 内部 | `HttpAdapter` | SRS 4.2 |
| TCP Socket | 内部系统 | 🚧 规划 | `TcpAdapter` | SRS 4.2 |
| Modbus TCP | 传感器 | 🚧 规划 | `ModbusAdapter` | SRS 4.2 |
| MQTT | 事件订阅 | 🚧 规划 | `MqttAdapter` | SRS 4.2 |

**重要**:
- 第三方 ECS 设备**推荐使用 HTTP/HTTPS + JSON**（白皮书标准）
- SRS 第 4.2 节允许 TCP/Modbus/HTTP/MQTT，视硬件而定

### 7.2 适配器实现模板

```python
class RcsHttpAdapter(IHardwareAdapter):
    def __init__(self, base_url: str, timeout: int = 10000):
        self.base_url = base_url
        self.timeout = timeout

    async def send_command(self, command: Command) -> Response:
        # 1. 转换为 RCS 特定格式
        rcs_payload = self._to_rcs_format(command)

        # 2. 发送 HTTP 请求
        response = await http_client.post(
            f"{self.base_url}/api/transport",
            json=rcs_payload,
            timeout=self.timeout
        )

        # 3. 转换为统一响应格式
        return self._from_rcs_format(response)

    def _to_rcs_format(self, command: Command) -> dict:
        """转换为 RCS 特定格式"""
        return {
            "taskId": command.command_id,
            "fromLoc": command.parameters["from_location"],
            "toLoc": command.parameters["to_location"],
            "rackId": command.parameters["rack_id"]
        }

    def _from_rcs_format(self, response: dict) -> Response:
        """转换为统一响应格式"""
        return Response(
            command_id=response["taskId"],
            status="SUCCESS" if response["code"] == 0 else "FAILED",
            result={"task_id": response["taskId"]},
            error_code=response.get("errorCode"),
            error_message=response.get("message")
        )
```

---

## 8. 集成检查清单

### 8.1 新硬件接入前

- [ ] 确认硬件支持的通信协议 (HTTP/TCP/Modbus/MQTT)
- [ ] 获取硬件 API 文档和命令列表
- [ ] 确认硬件是否支持幂等性 (或需要 WES 侧实现)
- [ ] 确认硬件事件推送机制 (Webhook/MQTT/轮询)
- [ ] 确认硬件超时和重试策略

### 8.2 适配器开发

- [ ] 实现 `IHardwareAdapter` 接口
- [ ] 实现命令格式转换 (`_to_xxx_format`, `_from_xxx_format`)
- [ ] 实现幂等性缓存 (若硬件不支持)
- [ ] 实现重试逻辑 (指数退避)
- [ ] 实现事件订阅 (若硬件支持异步)

### 8.3 测试验证

- [ ] 单元测试: 命令格式转换正确性
- [ ] 集成测试: 与真实硬件通信
- [ ] 幂等性测试: 重复发送相同命令
- [ ] 超时测试: 模拟网络延迟
- [ ] 失败恢复测试: 模拟硬件故障

---

## 9. 最佳实践

### 9.1 性能优化

- **批量操作**: 若硬件支持，合并多个命令为批量请求
- **连接池**: 复用 TCP/HTTP 连接，避免频繁建立连接
- **异步并发**: 使用 `asyncio` 并发发送独立命令

### 9.2 安全性

- **认证**: 所有硬件通信必须使用 API Key 或 Token
- **加密**: 敏感数据 (如物料编码) 使用 TLS 加密传输
- **审计日志**: 记录所有硬件命令和响应，保留 90 天

### 9.3 可观测性

- **指标监控**:
  - 命令成功率 (按设备类型)
  - 平均响应时间 (P50/P95/P99)
  - 重试次数分布
  - 超时次数

- **日志记录**:
  - 每个命令记录: `command_id`, `device_type`, `command_type`, `duration_ms`, `status`
  - 失败命令记录完整 `error_message` 和 `stack_trace`

- **告警规则**:
  - 命令失败率 > 5% (5 分钟窗口)
  - 平均响应时间 > 5s (1 分钟窗口)
  - 连续 3 次重试失败

---

## 10. 附录: 错误码定义

| 错误码 | 描述 | 重试 | 处理建议 |
|-------|------|------|---------|
| E001 | 网络超时 | ✓ | 自动重试 3 次 |
| E002 | 硬件繁忙 | ✓ | 延迟重试 |
| E003 | 参数错误 | ✗ | 检查命令参数 |
| E004 | 资源不存在 | ✗ | 检查资源 ID |
| E005 | 物理动作失败 | ✗ | 人工介入 |
| E006 | 业务规则拒绝 | ✗ | 检查业务逻辑 |
| E007 | 认证失败 | ✗ | 检查 API Key |
| E008 | 硬件故障 | ✗ | 通知维护人员 |

---

## 11. 版本历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|---------|
| 1.0 | 2025-12-15 | Claude | 初始版本，基于 SRS 第 3 章提炼 |
