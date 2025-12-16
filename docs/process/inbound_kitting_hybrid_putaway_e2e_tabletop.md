# 收货入库 + 装箱协调 + 混合入库（Exchange）端到端演练过程记录 (Inbound + Kitting + Hybrid Putaway E2E Tabletop Record)

> **文档类型**: 过程文档（桌面演练 / Tabletop Exercise）
> **场景选择**: `1 + SAP→WMS→WES + 电子料 7 寸 (7-inch)`
> **演练模式**: 默认全成功路径（除非明确插入异常）
> **日期**: 2025-12-16

## 1. 目的与范围 (Purpose & Scope)

本文档记录一次基于 `docs/SRS.md` 的端到端（E2E）桌面演练过程，用于验证“收货入库→IQC→装箱→混合入库（交换）→WMS 入库确认”的关键链路是否闭环。

**不在本次演练范围**：
- 发料（Production Issue）、退料闭环（Return Loop）、异常/熔断/恢复的实际演练（仅保留引用点）。

## 2. 参与者与职责 (Actors & Responsibilities)

- **SAP（上游 / Upstream）**：业务单据源（本演练不直接对接 WES）。
- **现有 WMS（Existing WMS）**：单据中转、库存真实源（Single Source of Truth），提供库存接口与入库确认落账。
- **WES（本系统 / Middleware）**：流程编排（Orchestration）、策略决策（Strategy）、设备协调（Coordination）、状态中继（State Relay）。
- **PDA（现场终端 / PDA）**：打印触发、物理扫描、绑定与人工确认。
- **打印机（Printer）**：打印栈板标签（ZPL）。
- **RCS/AGV（搬运系统 / RCS）**：搬运任务执行（Move）。
- **ECS（设备控制 / ECS）**：视觉识别、装箱执行、结果回传（Check/Put/Result）。
- **CTU（料箱机器人 / CTU）**：五层货架侧交换动作执行（Exchange）。
- **QMS/IQC（质量系统 / QMS）**：抽检策略与检验结果回传。

## 3. 前置条件 (Preconditions)

- WES 已存在对应 `material_id+vendor_id` 的主数据（Master Data），用于尺寸/厚度校验（Error Proofing）。
- 现场有可用空单层货架（Single-Layer Rack），且可扫描到空箱号列表。
- 允许不同 GRN 混托（Mixed Pallet），即 `allow_mixed_pallet=true`。

## 4. 关键数据对象 (Key Objects)

- **幂等键 (Idempotency Key)**：`request_id`（北向接单）。
- **收货单据 (GRN)**：`GRN-20251216-0001`、`GRN-20251216-0002`
- **栈板 (PalletID)**：`PAL-20251216-0001`
- **任务 (Task)**：`TSK-TRANS-*`、`TSK-IQC-*`、`TSK-KIT-OUT-*`、`TSK-EXCH-*`
- **装箱作业 (Kitting Job)**：`KIT-20251216-0001`
- **单层货架/料箱 (Single-Layer Rack / Bin)**：`RACK-SL-01`、`BIN-01..BIN-04`
- **槽位 (Slot)**：`SLOT-01..SLOT-06`（以 A 型料箱 6 槽位为例）
- **PKG（六合一码 / PKG Code）**：示例 `PKG-R001-0001`、`PKG-R002-0001`（演练用）
- **库位码 (Location Code)**：示例 `SMT-A-01-03`（演练用）

## 5. 端到端过程 (End-to-End Procedure)

### 5.1 单据接入（Order Ingest）

**现有 WMS → WES**：`POST /api/v1/orders/inbound`

入参样例（第 1 单）：
```json
{
  "request_id": "req-20251216-0001",
  "grn_id": "GRN-20251216-0001",
  "dock_id": "Dock-01",
  "lines": [
    {
      "line_id": "1",
      "material_id": "R001",
      "vendor_id": "VENDOR-01",
      "qty": 1000,
      "uom": "EA",
      "dc": "2025-12-10",
      "lc": "LC-LOT-001",
      "tray_size_inch": 7,
      "tray_thickness_mm": 8.0
    }
  ],
  "allow_mixed_pallet": true
}
```

**WES 响应**（生成栈板与打印任务）：
- `pallet_id=PAL-20251216-0001`
- 下发打印（ZPL）任务：`PRINT-20251216-0001`
- 幂等约束：同 `request_id` 重复提交应返回同一结果

### 5.2 打印与 PDA 绑定（Dock Receiving & Binding）

- 打印成功（PDA 扫描确认 `PAL-20251216-0001`）
- PDA 绑定数量（第 1 单）：`GRN-20251216-0001 bind_qty=500`

**WES 校验**：
- `Sum(Current_Qty)=500 <= GRN.Remaining_Qty(1000)` ✅
- `GRN-20251216-0001 Remaining_Qty=500`

**WES 生成搬运任务**（Dock → Buffer）：
- `task_id=TSK-TRANS-20251216-0001`
- `from=Dock-01`、`to=Inbound-Buffer-01`、`payload=PAL-20251216-0001`

### 5.3 混托：追加绑定另一货物（Mixed Pallet / M:N Binding）

确认：允许混托（`allow_mixed_pallet=true`）且第二货物与第一货物 **不同**（`Material/Vendor/DC !=`）。

**现有 WMS → WES**：再次接单（第 2 单）
```json
{
  "request_id": "req-20251216-0002",
  "grn_id": "GRN-20251216-0002",
  "dock_id": "Dock-01",
  "lines": [
    {
      "line_id": "1",
      "material_id": "R002",
      "vendor_id": "VENDOR-02",
      "qty": 800,
      "uom": "EA",
      "dc": "2025-12-09",
      "lc": "LC-LOT-002",
      "tray_size_inch": 7,
      "tray_thickness_mm": 9.0
    }
  ],
  "allow_mixed_pallet": true
}
```

**PDA → WES**：绑定到同一栈板
- `PAL-20251216-0001` 追加绑定 `GRN-20251216-0002 bind_qty=800`（`<=800` ✅）

**混托约束（关键校验点）**：
- 后续装箱（Binning）必须保证同一槽位内 `Material+Vendor+DC` 一致（禁止混料 / No Mixing）。

### 5.4 搬运到 Buffer（RCS Move）

**RCS 回执**：
- `TSK-TRANS-20251216-0001 Accepted`
- `Arrived@Inbound-Buffer-01`（演练中未提供时间戳，记为待补）

### 5.5 IQC 动态路由（IQC Routing & Review）

**WES → QMS**：抽检策略查询 `POST /api/qms/sampling/query`

演练默认返回：
- `R001+VENDOR-01 Qty 500 → sampling_qty=20`；示例 `pkg_code=PKG-R001-0001`
- `R002+VENDOR-02 Qty 800 → sampling_qty=0`；示例 `pkg_code=PKG-R002-0001`

**WES 路由决策**：
- 混托场景下，以“整托”搬运到 IQC（无法只搬运部分载荷）
- `task_id=TSK-IQC-20251216-0001`：`Inbound-Buffer-01 → IQC-Area-01`

**RCS 回执（默认）**：
- `Accepted`
- `Arrived@IQC-Area-01 timestamp=2025-12-16T10:30:00+08:00`

**QMS/IQC 检验结果（默认）**：
- `Inspection_Result(GRN-20251216-0001)=OK`
- `Inspection_Result(GRN-20251216-0002)=OK`

**WES 路由**（All OK）：
- 生成回流任务：`TSK-IQC-RET-20251216-0001`：`IQC-Area-01 → Inbound-Buffer-01`

### 5.6 进入装箱区 + 空箱握手（Kitting Station Handshake）

演练确认（默认成功）：
- `PAL-20251216-0001 Arrived@Kitting-Station-01`
- `ECS → WES: Verify_Empty([BIN-01,BIN-02,BIN-03,BIN-04]) = PASS`

### 5.7 装箱协调完整过程（Smart Kitting Coordination）

**装箱批次参数（演练默认）**：
- `GRN-20251216-0001 (R001)`：`10 盘 * 50EA = 500EA`
- `GRN-20251216-0002 (R002)`：`16 盘 * 50EA = 800EA`
- 采用 A 型料箱（6 个 7 寸槽位）为示例；堆叠上限（示例）：
  - `R001 thickness=8.0mm → MaxStack=10`
  - `R002 thickness=9.0mm → MaxStack=8`

**作业创建**：
- `job_id=KIT-20251216-0001`

#### 5.7.1 R001（10 盘）— 同类合并（Same-SKU Merge）

- 第 1 盘：`ECS → WES: Check_Material(PKG_Code, Dims, Thickness)` 通过
- WES 分配：`BIN-01/SLOT-01`
- `WES → ECS: Put_Instruction(BIN-01,SLOT-01, expected_stack_height=1)`；`ECS → WES: Put_Result=OK`
- 第 2~10 盘：持续分配到同一槽位，`expected_stack_height=2..10`
- 结束：`BIN-01/SLOT-01 = FULL (10/10)`

#### 5.7.2 R002（16 盘）— 禁止混料 + 槽位满则换槽（No Mixing + Slot Rollover）

关键校验：`R002 != R001`，不可放入 `BIN-01/SLOT-01`（已被 R001 占用）。

- 第 1~8 盘：分配 `BIN-01/SLOT-02`，堆叠至 `8/8 FULL`
- 第 9~16 盘：`SLOT-02` 已满，切换到 `BIN-01/SLOT-03`，堆叠至 `8/8 FULL`

#### 5.7.3 批次完成即切出（Batch Complete → Cut-out）

演练选择策略：**批次完成即切出**（即使整架未满）。

- `KIT-20251216-0001 = COMPLETED`
- 生成出站任务：`TSK-KIT-OUT-20251216-0001`
  - `Kitting-Station-01 → SMT-Buffer-01`
  - `payload=RACK-SL-01`

**RCS 回执（默认）**：
- `Accepted`
- `Arrived@SMT-Buffer-01 timestamp=2025-12-16T10:45:00+08:00`

### 5.8 混合入库策略（Hybrid Inbound Strategy / Priority Exchange）

对 `BIN-01` 使用率（示例口径）：`Usage = 3/6 = 50%` → 命中 `Priority Exchange`（`50% <= Usage < 80%`）。

#### 5.8.1 五层货架空箱资源查询与锁定（Empty Bin Discovery & Locking）

> 本小节用于补齐 `SRS 3.3.2` 中“锁定五层货架 Empty_Bin（指定层号和 A/B 面）”在 Exchange 前的可执行细节；SRS 当前未规定具体接口，本演练以“WES 内部资源服务 + 设备状态回读”方式展开。

**数据来源（建议口径）**：
- **静态配置（Initialization）**：来自上线前初始化（货架/容器/地码映射），用于枚举五层货架 `RackID/Layer/Side/Bin` 的结构。
- **动态状态（Runtime）**：来自 CTU/RCS 的实时上报或心跳（例如：某层某面箱位是否为空、是否被占用、是否可操作）。

**查询目标**：为即将执行的交换任务选择一个可用的 `Empty_Bin`，并明确到：
- `RackID`（五层货架）
- `Layer`（层号）
- `Side`（A/B 面）
- `Empty_Bin_ID`（具体空箱位/容器位标识）

**候选过滤（示例规则）**：
- `State == Empty`（空箱位）
- `Lock == None`（未被其他任务锁定）
- `Side` 偏好：优先 `Side-A`（靠近产线侧），同时满足 A/B 负载平衡策略（若有）
- `Layer` 可达：CTU 当前可操作层/同侧无冲突（避免并发占用）
- `TimeWindow`：在期望完成时间内可用（用于减少“锁了但来不及执行”）

**空箱锁定（Lock）**：
- WES 创建资源锁（Resource Lock），将候选 `Empty_Bin` 与本次 Exchange 任务绑定，避免被并发任务抢占。
- 锁记录（示例字段）：
  - `lock_id`
  - `resource = (RackID, Layer, Side, Empty_Bin_ID)`
  - `held_by_task_id = TSK-EXCH-...`
  - `expire_at`（TTL，避免死锁；超时自动释放或人工释放）
  - `status = Locked|Released|Expired`
- 幂等建议：同一 `TSK-EXCH` 重试锁定应返回同一 `lock_id` 或同一资源（避免抖动导致锁资源漂移）。

**可选的“空箱确认”（Verify Empty）**：
- 为避免“信息过期”（WES 状态认为空，但现场已被占用），可在锁定后、下发 Exchange 前做一次确认：
  - `WES -> CTU/RCS: Verify_Empty_Bin(RackID, Layer, Side, Empty_Bin_ID)`
  - `CTU/RCS -> WES: Verify_Empty_Bin_Result(OK/NotEmpty/Unavailable)`
- 若返回 `NotEmpty/Unavailable`：WES 释放锁并重新选择候选（带告警/计数）。

**锁释放（Release）**：
- `Exchange Completed`：释放锁或将 `Empty_Bin` 状态更新为 `Occupied`（因为它承载了交换进来的容器内容）。
- `Exchange Failed/Cancelled/Expired`：释放锁并记录异常原因，必要时触发人工介入。

**锁定五层货架空箱位**（演练输入）：
- `RACK-5L-01 / Layer-3 / Side-A / Empty_Bin=EBIN-12`

**WES → CTU/RCS**：下发原子交换指令（Exchange）
- `task_id=TSK-EXCH-20251216-0001`
- `Exchange(Source=RACK-SL-01:BIN-01, Target=RACK-5L-01, Layer=3, Side=A, Empty_Bin=EBIN-12)`

**CTU/RCS 回执（默认）**：
- `Accepted`
- `Completed timestamp=2025-12-16T10:50:00+08:00`

**WES 数据更新（交换后容器属性对调）**：
- `EBIN-12` 承载 `BIN-01` 的槽位内容（R001/R002 在不同槽位，不混料）
- `RACK-SL-01:BIN-01` 变为空箱（后续回流空箱位）

### 5.9 WMS 入库确认（Putaway Confirmation）

演练采用库位映射示例：
- `RACK-5L-01/A/L3/EBIN-12 → location_code=SMT-A-01-03`

**WES → 现有 WMS**：`POST /api/wms/inventory/putaway`（按物料拆两笔确认）

1) `R001 Qty 500`
```json
{
  "grn": "GRN-20251216-0001",
  "material_id": "R001",
  "qty": 500,
  "location": "SMT-A-01-03",
  "pkg_code": "PKG-R001-0001",
  "timestamp": "2025-12-16T10:51:00+08:00"
}
```
WMS 回执（默认）：`status=OK, transaction_id=TXN-PUT-20251216-0001`

2) `R002 Qty 800`
```json
{
  "grn": "GRN-20251216-0002",
  "material_id": "R002",
  "qty": 800,
  "location": "SMT-A-01-03",
  "pkg_code": "PKG-R002-0001",
  "timestamp": "2025-12-16T10:51:05+08:00"
}
```
WMS 回执（默认）：`status=OK, transaction_id=TXN-PUT-20251216-0002`

### 5.10 WES 收尾（Completion & Transient State）

- 标记完成：`TSK-TRANS-20251216-0001`、`TSK-IQC-20251216-0001`、`TSK-KIT-OUT-20251216-0001`、`TSK-EXCH-20251216-0001`
- 清理瞬态 `Execution_State`（任务完成后清除；日志/追溯记录留存）
- 备注：`GRN-20251216-0001` 尚有 `Remaining_Qty=500` 未绑定/未入库（需后续分托/再建栈板流程）

## 6. 关键规则与校验点清单 (Key Rules & Checks)

- **幂等性 (Idempotency)**：北向接单以 `request_id` 去重（重复提交返回同结果）。
- **绑定校验 (Binding Validation)**：PDA 绑定时校验 `Sum(Current_Qty) <= GRN.Remaining_Qty`。
- **混托约束 (Mixed Pallet Constraint)**：IQC 路由与搬运以整托为单位；装箱槽位禁止混料（`Material+Vendor+DC` 一致）。
- **防错校验 (Error Proofing)**：`Check_Material(PKG_Code, Dims, Thickness)` 与主数据容差校验；7 寸仅入 7 寸槽位。
- **交换/拣选策略 (Exchange/Picking Strategy)**：使用率阈值决定 Full Exchange / Priority Exchange / Pipeline Picking。
- **库存协同 (Inventory Coordination)**：WMS 为库存真实源；入库确认通过 `putaway` 由 WMS 落账；确认接口需支持按 `TaskID` 幂等（概念要求）。

## 7. 追溯与来源映射 (Traceability)

**来自 SRS 的章节映射（需求/流程依据）**：
- `docs/SRS.md`：3.2.1（码头接收与绑定）、3.2.2（IQC 路由）、3.3.1（装箱协调）、3.3.2（混合入库）、3.4.1（库存协同）、3.8.2（接口规范）、3.8.3（数据一致性保障）、3.7（异常机制，未演练）

**到原始资料（docs/origin）追溯**：
- 本演练记录基于 SRS 文本抽取；若需满足“Origin 级追溯（文件/Sheet/Row/段落）”，需补充 SRS → `docs/origin/` 的映射表后再回填。

## 8. 备注与待澄清项 (Notes & Open Questions)

- **接口路径口径**：SRS 不同章节对 WMS 接口路径存在多种写法（如 `/api/wms/...` vs `/api/v1/wms/...`，以及 `confirm` 聚合接口）；本过程记录以 SRS 3.4/3.8 的分拆接口（`putaway/issue/reserve/query`）为主。
- **锁定栈板（Lock Pallet）**：本次演练未定义独立接口/事件；以“开始搬运/接单”为隐式锁定点，建议在规格中明确。
- **库位码映射（Location Code Mapping）**：`RACK/Side/Layer/Bin` 到 `location_code` 的映射规则需明确由谁维护（WES 主数据 or WMS 主数据）。
- **批次完成切出策略（Batch Complete Cut-out Policy）**：SRS 3.3.1 明确的切出触发是“满架切出”；本演练使用“批次完成即切出（可配置）”，如需落地应在规格中明确为可配置策略及其触发条件。
- **Usage 指标定义（Usage Metric Definition）**：SRS 3.3.2 使用 `Usage` 阈值（80%/50%）决策 Exchange/Picking，但未定义 Usage 的计算口径（按槽位占用、按深度/容量、或按重量/体积）；本演练以“槽位占用率”示例。
- **Exchange 指令参数（Exchange Command Parameters）**：SRS 3.3.2 文本同时出现“锁定 Empty_Bin（层号+A/B 面）”与示例 `Exchange(..., Layer, Side)`；本演练在命令侧显式携带 `Empty_Bin`，建议统一接口定义。
