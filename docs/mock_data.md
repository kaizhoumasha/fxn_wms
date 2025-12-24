# 模拟数据 (Mock Data) - fxn-wms

> **用途**: 用于验证 WES 系统在收货入库、IQC、装箱及特殊物料流程中的调度逻辑。
> **覆盖场景**: 标准入库、混托/分托、高值/MSD/PCB 特殊路由、机构件 AB 托协同、IQC 异常分拣。

## 1. 基础主数据 (Master Data)

| 物料代码 | 描述 | 属性 | 尺寸/包装 | 供应商 |
| :--- | :--- | :--- | :--- | :--- |
| **Capacitor-001** | 电容#0001 | 标准电子料 | 7寸盘, 5000PCS/盘 | V0001 |
| **Capacitor-002** | 电容#0002 | 标准电子料 | 7寸盘, 5000PCS/盘 | V0001 |
| **Resistor-001** | 电阻#0001 | 标准电子料 | 7寸盘, 5000PCS/盘 | V0002 |
| **Resistor-002** | 电阻#0002 | 标准电子料 | 7寸盘, 5000PCS/盘 | V0002 |
| **Chip-003** | 芯片#0003 | 标准电子料 | 13寸盘, 2000PCS/盘 | V0002 |
| **CPU-9999** | 高性能CPU | **High-Value (高值)** | 托盘装 (Tray) | V0003 |
| **IC-8888** | 驱动IC | **MSD (Level 3)** | 7寸盘 | V0003 |
| **PCB-7777** | 主板PCB | **PCB** | 真空包 | V0003 |
| **Top-Cover-6666** | 机箱上盖 | **Mechanical (机构件)** | 大箱 | V0004 |
| **Btm-Cover-5555** | 机箱下盖 | **Mechanical (机构件)** | 大箱 | V0004 |

---

## 2. 采购订单 (Purchase Orders)

### PO.0001 (供应商: V0001)
*   **L1**: Capacitor-001, 100,000 PCS
*   **L2**: Capacitor-002, 50,000 PCS

### PO.0002 (供应商: V0002)
*   **L1**: Resistor-001, 200,000 PCS
*   **L2**: Resistor-002, 100,000 PCS
*   **L3**: Chip-003, 50,000 PCS

### PO.0003 (供应商: V0003) - 特殊物料
*   **L1**: CPU-9999, 2,000 PCS (高值)
*   **L2**: IC-8888, 5,000 PCS (MSD)
*   **L3**: PCB-7777, 1,000 PCS (PCB)

### PO.0004 (供应商: V0004) - 机构件
*   **L1**: Top-Cover-6666, 500 PCS (上盖)
*   **L2**: Btm-Cover-5555, 500 PCS (下盖)

---

## 3. 收货通知单 (GRNs)

*假设 SAP 已返回以下 GRN 数据*

| GRN 号 | 来源 PO | 物料 | 数量 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| **GRN.0001** | PO.0001-L1 | Capacitor-001 | 100,000 | |
| **GRN.0002** | PO.0001-L2 | Capacitor-002 | 50,000 | |
| **GRN.0003** | PO.0002-L1 | Resistor-001 | 200,000 | |
| **GRN.0004** | PO.0002-L2 | Resistor-002 | 100,000 | |
| **GRN.0005** | PO.0002-L3 | Chip-003 | 50,000 | |
| **GRN.0006** | PO.0003-L1 | CPU-9999 | 2,000 | 高值 |
| **GRN.0007** | PO.0003-L2 | IC-8888 | 5,000 | MSD |
| **GRN.0008** | PO.0003-L3 | PCB-7777 | 1,000 | PCB |
| **GRN.0009** | PO.0004-L1 | Top-Cover-6666 | 500 | 机构件-上盖 |
| **GRN.0010** | PO.0004-L2 | Btm-Cover-5555 | 500 | 机构件-下盖 |

---

## 4. 码头绑定数据 (Dock Binding Data)

**日期**: 2025年12月20日 - 12月21日

### 场景 A: 标准电子料 (混合/分托测试)

**栈板 PAL.0001 (混托: 7寸 + 13寸)**
*   **箱01**: Capacitor-001, 50,000 PCS -> **GRN.0001**
*   **箱02**: Capacitor-001, 50,000 PCS -> **GRN.0001**
*   **箱03**: Capacitor-002, 25,000 PCS -> **GRN.0002**
*   **箱04**: Capacitor-002, 25,000 PCS -> **GRN.0002**
*   **箱11**: Chip-003, 10,000 PCS -> **GRN.0005** (分托部分)

**栈板 PAL.0002 (单料满托 - 将用于 IQC NG 测试)**
*   **箱05**: Resistor-001, 50,000 PCS -> **GRN.0003**
*   **箱06**: Resistor-001, 50,000 PCS -> **GRN.0003**

**栈板 PAL.0003 (单料满托)**
*   **箱07**: Resistor-001, 50,000 PCS -> **GRN.0003**
*   **箱08**: Resistor-001, 50,000 PCS -> **GRN.0003**

**栈板 PAL.0004 (单料满托)**
*   **箱09**: Resistor-002, 50,000 PCS -> **GRN.0004**
*   **箱10**: Resistor-002, 50,000 PCS -> **GRN.0004**

**栈板 PAL.0005 (GRN.0005 剩余部分)**
*   **箱12**: Chip-003, 10,000 PCS -> **GRN.0005**
*   **箱13**: Chip-003, 10,000 PCS -> **GRN.0005**
*   **箱14**: Chip-003, 10,000 PCS -> **GRN.0005**
*   **箱15**: Chip-003, 10,000 PCS -> **GRN.0005**

### 场景 B: 特殊物料路由测试

**栈板 PAL.0006 (高值物料)**
*   **箱20**: CPU-9999, 2,000 PCS -> **GRN.0006**
    *   *预期行为*: 触发 **SRS 3.5.1** 高值路由，直接送往高值区，跳过普通暂存区。

**栈板 PAL.0007 (MSD + PCB 混托)**
*   **箱21**: IC-8888, 5,000 PCS -> **GRN.0007** (MSD)
*   **箱22**: PCB-7777, 1,000 PCS -> **GRN.0008** (PCB)
    *   *预期行为*:
        1.  **MSD**: 触发 **SRS 3.5.2**，记录开封时间，送往 MSD 专区或干燥柜。
        2.  **PCB**: 触发 **SRS 3.5.3**，送往 PCB 专属存储区或人工线。
        3.  *注*: 由于是混托，WES 需在拆箱环节生成两个不同的搬运/存储指令。

### 场景 C: 机构件协同测试

**栈板 PAL.0008 (上盖 - Side A)**
*   **箱30**: Top-Cover-6666, 500 PCS -> **GRN.0009**

**栈板 PAL.0009 (下盖 - Side B)**
*   **箱31**: Btm-Cover-5555, 500 PCS -> **GRN.0010**

*   *预期行为*: 触发 **SRS 3.5.4** 成对协同。
    *   WES 识别 PAL.0008 和 PAL.0009 为配对组。
    *   调度 RCS 时，确保两车同时到达拆包线（时间差 < 5分钟）。

---

## 5. IQC 流程模拟 (IQC Simulation)

针对 **PAL.0002 (Resistor-001)** 进行异常流程模拟：

1.  **触发**: IQC 呼叫 PAL.0002 送检。
2.  **结果**: QMS 返回 **GRN.0003** 检验结果为 **NG** (Sample Failed)。
3.  **WES 动作**:
    *   将 PAL.0002 路由至 **复判区 (Review Area)**。
    *   下发 **拆板指令 (Split Task)**。
4.  **拆板执行**:
    *   将 100,000 PCS 全部移至新栈板 **PAL.0002-NG**。
    *   PAL.0002 (原) 变为空栈板，回收。
    *   PAL.0002-NG 贴上不良品标签，路由至不良品仓。

## 6. SMT 智能装箱模拟 (SMT Smart Kitting Simulation)

### 6.1 初始环境 (Initial Environment)

**配置**: 标准单层货架 (Single Layer Rack)

*   **Rack ID**: **SMART-RACK-001**
*   **Layout**: 4 Bins (2 Type-A + 2 Type-B)
    *   **Bin-01 (Type A)**: 6 x 7" Slots (Slots: **A1-1** ~ **A1-6**)
    *   **Bin-02 (Type A)**: 6 x 7" Slots (Slots: **A2-1** ~ **A2-6**)
    *   **Bin-03 (Type B)**: 2 x 7" Slots + 1 x 15" Slot (Slots: **B3-1** ~ **B3-2**, **B3-L1**)
    *   **Bin-04 (Type B)**: 2 x 7" Slots + 1 x 15" Slot (Slots: **B4-1** ~ **B4-2**, **B4-L1**)
*   **Slot Spec**: Max Depth 150mm

### 6.2 模拟物理输入流 (Physical Input Stream - Rod Based)

**物理场景**:
*   拆包区将外箱拆解，将料盘堆叠放入 **串杆 (Rod)**。
*   每根串杆承载一组料盘，由输送线步进送达 **工作位 (Position 4)**。
*   ECS 视觉系统此时只能看到 **最顶部 (Top)** 的第一个料盘。

**串杆上料配置 (Rod Loading Profile)**:

| 串杆号 | 堆叠顺序 (Top to Bottom) | 来源外箱 | 物料 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| **Rod-01** | **Reel #1** (Top) | Carton A | Capacitor-002 | Vision 可见 |
| | Reel #2 | Carton A | Capacitor-002 | 遮挡 |
| | Reel #3 | Carton A | Capacitor-002 | 遮挡 |
| | Reel #4 | Carton A | Capacitor-002 | 遮挡 |
| | Reel #5 (Bottom) | Carton A | Capacitor-002 | 遮挡 |
| **Rod-02** | **Reel #1** (Top) | Carton B | Capacitor-001 | Vision 可见 |
| | Reel #2 | Carton B | Capacitor-001 | 遮挡 |
| **Rod-03** | **Reel #1~10** | PAL.0003 | Resistor-001 | 10 Reels stacked |
| **Rod-04** | **Reel #1~10** | PAL.0003 | Resistor-001 | 10 Reels stacked |
| **Rod-05** | **Reel #1~10** | PAL.0004 | Resistor-002 | 10 Reels stacked |
| **Rod-06** | **Reel #1~10** | PAL.0004 | Resistor-002 | 10 Reels stacked |

### 6.3 物理交互追踪 (Physical Interaction Trace)

#### Phase 1: Rod-01 Processing Loop (Capacitor-002 x 5)

*   **Event 01**: `Rod-01` Arrives at Position 4.
*   **Loop Cycle 1**:
    *   **Vision Scans Top**. Found: `PKG-CA-01`.
    *   **WES Logic**: Assign to `Bin-01/A1-1`.
    *   **Arm Action**: PICK `PKG-CA-01` -> PUT `A1-1`.
*   **Loop Cycle 2**:
    *   *System Status*: Previous Top removed. New Top exposed.
    *   **Vision Scans Top**. Found: `PKG-CA-02`.
    *   **WES Logic**: Stack to `Bin-01/A1-1` (Same Mat).
    *   **Arm Action**: PICK `PKG-CA-02` -> PUT `A1-1`.
*   `...` (Repeat for Reel #3, #4)
*   **Loop Cycle 5**:
    *   **Vision Scans Top**. Found: `PKG-CA-05` (Last one).
    *   **Arm Action**: PICK `PKG-CA-05` -> PUT `A1-1`.
*   **Event 02**: Vision Scans -> **Empty Rod**.
*   **WES Action**: Release `Rod-01`. Move Conveyor.

#### Phase 2: Rod-02 Processing Loop (Capacitor-001 x 2)

*   **Event 03**: `Rod-02` Arrives at Position 4.
*   **Loop Cycle 1**:
    *   **Vision Scans Top**. Found: `PKG-CB-01`.
    *   **WES Logic**: `Bin-01/A1-1` is occupied by Cap-002. Select `Bin-01/Slot-A1-2` (New Slot).
    *   **Arm Action**: PICK `PKG-CB-01` -> PUT `A1-2`. (Depth 15/150)

#### Phase 3: High Volume Fill (Rod-03 ~ Rod-06)

*   **Rod-03 (Resistor-001 x 10)**:
    *   System fills **Slot A1-3**. (Depth: 15*10 = 150mm -> **FULL**)
*   **Rod-04 (Resistor-001 x 10)**:
    *   System fills **Slot A1-4**. (Depth: 15*10 = 150mm -> **FULL**)
*   **Rod-05 (Resistor-002 x 10)**:
    *   System fills **Slot A1-5**. (Depth: 15*10 = 150mm -> **FULL**)
*   **Rod-06 (Resistor-002 x 10)**:
    *   System fills **Slot A1-6**. (Depth: 15*10 = 150mm -> **FULL**)

### 6.4 标准协议交互日志 (Standard Protocol Interaction Log - Auto Scan)

遵循 "Event-Driven" 模式：视觉系统由硬件自动触发，WES 仅被动接收扫描结果。

#### Phase 1: Rod-01 Arrival & First Reel

**1. [ECS -> WES] Event: Scan Completed (Hardware Triggered)**
*Hardware auto-scans the top reel when Rod arrives at position.*

```http
POST /api/v1/callback/event
Content-Type: application/json

{
  "device_id": "VISION_01",
  "event_type": "SCAN_COMPLETED",  // 硬件自动触发事件
  "timestamp": 1703318400000,
  "data": {
    "location": "STATION_KITTING_01",
    "rod_id": "Rod-01",
    "pkg_code": "PKG-CA-01",       // 识别结果
    "dims": "7inch",
    "thickness": 15
  }
}
```

**2. [WES -> ECS] Response (Ack)**
```http
HTTP/1.1 200 OK
```

**3. [WES -> ECS] Command: Pick & Put**
*WES processes the scan event and decides allocation.*

```http
POST /api/v1/device/command
Content-Type: application/json

{
  "command_id": "CMD-001",
  "task_type": "PUT",
  "priority": 10,
  "timeout": 10000,
  "params": {
    "pkg_code": "PKG-CA-01",
    "target_loc": "Bin-01",
    "target_slot": "A1-1",
    "expected_height": 15
  }
}
```

**4. [ECS -> WES] Callback: Put Result**
```http
POST /api/v1/callback/result
Content-Type: application/json

{
  "command_id": "CMD-001",
  "device_id": "ARM_01",
  "result": "SUCCESS",
  "data": {
    "actual_height": 15.2
  }
}
```

#### Phase 1.1: Rod-01 Loop (Next Reel Revealed)

*ECS 机械臂移走 Top Reel 后，Vision 传感器检测到下方 Reel 露出，自动触发下一次扫描*

**5. [ECS -> WES] Event: Scan Completed (Hardware Triggered)**
```http
POST /api/v1/callback/event
Content-Type: application/json

{
  "device_id": "VISION_01",
  "event_type": "SCAN_COMPLETED",
  "timestamp": 1703318410000,
  "data": {
    "rod_id": "Rod-01",
    "pkg_code": "PKG-CA-02",  // 下一个被扫描到的 Reel
    "dims": "7inch",
    "thickness": 15
  }
}
```

**6. [WES -> ECS] Command: Pick & Put (Stacking)**
```http
POST /api/v1/device/command
Content-Type: application/json

{
  "command_id": "CMD-002",
  "task_type": "PUT",
  "priority": 10,
  "params": {
    "pkg_code": "PKG-CA-02",
    "target_loc": "Bin-01",
    "target_slot": "A1-1", // 堆叠在同一个 Slot
    "expected_height": 30
  }
}
```

*... Loop continues until Vision scans NOTHING (Empty Rod) ...*

**7. [ECS Internal] Rod Empty Detection & Auto Step**
*ECS 检测到空串杆后，自动步进到下一个串杆（无需通知 WES）。*
- ECS 视觉系统检测到空串杆
- ECS 控制器自动触发流水线步进
- 下一个串杆 (Rod-02) 移动到 Position 4
- 视觉系统自动扫描新串杆的顶部料盘

### 6.5 模拟结果数据 (Simulation Result Data - Next Phase Input)

本节汇总上述模拟流程结束后，WES 系统中形成的最终数据状态。这些数据将作为 **3.3.2 混合入库 (Hybrid Inbound)** 场景的输入。

#### 1. 最终货架状态 (Final Rack State)

**Rack ID**: `SMART-RACK-001`

| Bin ID | Type | Slot ID | 存放物料 | 数量(Reels) | 已用深度 (Used/Max) | 状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bin-01** | A | **A1-1** | Capacitor-002 | 5 | **75mm** / 150mm | Particle |
| | | **A1-2** | Capacitor-001 | 5 | **75mm** / 150mm | Particle |
| | | **A1-3** | Resistor-001 | 10 | **150mm** / 150mm | **FULL** |
| | | **A1-4** | Resistor-001 | 10 | **150mm** / 150mm | **FULL** |
| | | **A1-5** | Resistor-002 | 10 | **150mm** / 150mm | **FULL** |
| | | **A1-6** | Resistor-002 | 10 | **150mm** / 150mm | **FULL** |
| **Bin-02** | A | All | (Empty) | 0 | 0 / 150mm | Empty |
| **Bin-03** | B | **B3-L1** | Chip-003 | 2 | **40mm** / 150mm | Particle (Large) |
| | | B3-1 ~ 2 | (Empty) | 0 | 0 / 150mm | Empty |
| **Bin-04** | B | All | (Empty) | 0 | 0 / 150mm | Empty |

**Bin-01 Utilization**:
*   Total Capacity: 6 Slots * 150mm = 900mm
*   Used Depth: 75 + 75 + 150 + 150 + 150 + 150 = **750mm**
*   Utilization Rate: 750 / 900 = **83.3%**
*   **Result**: Meets `BIN_FULL_EXCHANGE_THRESHOLD` (> 80%).

#### 2. 生成的库存记录 (Generated Inventory Records)

WES 在数据库中创建的 `Inventory` 记录 (模拟) - **PKG 级独立记录**:

```json
[
  // Slot A1-1: Capacitor-002 x 5 (Rod-01)
  {
    "id": "INV-PKG-001", "pkg_code": "PKG-CA-01",
    "material_id": "Capacitor-002", "vendor_code": "V0001", "dc_code": "DC-2024-001",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-1",
      "depth_position": 1, "depth_mm": 15
    }
  },
  {
    "id": "INV-PKG-002", "pkg_code": "PKG-CA-02",
    "material_id": "Capacitor-002", "vendor_code": "V0001", "dc_code": "DC-2024-001",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-1",
      "depth_position": 2, "depth_mm": 30
    }
  },
  {
    "id": "INV-PKG-003", "pkg_code": "PKG-CA-03",
    "material_id": "Capacitor-002", "vendor_code": "V0001", "dc_code": "DC-2024-001",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-1",
      "depth_position": 3, "depth_mm": 45
    }
  },
  {
    "id": "INV-PKG-004", "pkg_code": "PKG-CA-04",
    "material_id": "Capacitor-002", "vendor_code": "V0001", "dc_code": "DC-2024-001",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-1",
      "depth_position": 4, "depth_mm": 60
    }
  },
  {
    "id": "INV-PKG-005", "pkg_code": "PKG-CA-05",
    "material_id": "Capacitor-002", "vendor_code": "V0001", "dc_code": "DC-2024-001",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-1",
      "depth_position": 5, "depth_mm": 75
    }
  },

  // Slot A1-2: Capacitor-001 x 5 (Rod-02 + additional)
  {
    "id": "INV-PKG-006", "pkg_code": "PKG-CB-01",
    "material_id": "Capacitor-001", "vendor_code": "V0001", "dc_code": "DC-2024-002",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-2",
      "depth_position": 1, "depth_mm": 15
    }
  },
  {
    "id": "INV-PKG-007", "pkg_code": "PKG-CB-02",
    "material_id": "Capacitor-001", "vendor_code": "V0001", "dc_code": "DC-2024-002",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-2",
      "depth_position": 2, "depth_mm": 30
    }
  },
  // ... (PKG-CB-03 to PKG-CB-05, depth 45-75mm)

  // Slot A1-3: Resistor-001 x 10 (Rod-03)
  {
    "id": "INV-PKG-011", "pkg_code": "PKG-R1-01",
    "material_id": "Resistor-001", "vendor_code": "V0002", "dc_code": "DC-2024-003",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-3",
      "depth_position": 1, "depth_mm": 15
    }
  },
  // ... (PKG-R1-02 to PKG-R1-10, depth 30-150mm, FULL)

  // Slot A1-4: Resistor-001 x 10 (Rod-04)
  {
    "id": "INV-PKG-021", "pkg_code": "PKG-R1-11",
    "material_id": "Resistor-001", "vendor_code": "V0002", "dc_code": "DC-2024-003",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-4",
      "depth_position": 1, "depth_mm": 15
    }
  },
  // ... (PKG-R1-12 to PKG-R1-20, depth 30-150mm, FULL)

  // Slot A1-5: Resistor-002 x 10 (Rod-05)
  {
    "id": "INV-PKG-031", "pkg_code": "PKG-R2-01",
    "material_id": "Resistor-002", "vendor_code": "V0002", "dc_code": "DC-2024-004",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-5",
      "depth_position": 1, "depth_mm": 15
    }
  },
  // ... (PKG-R2-02 to PKG-R2-10, depth 30-150mm, FULL)

  // Slot A1-6: Resistor-002 x 10 (Rod-06)
  {
    "id": "INV-PKG-041", "pkg_code": "PKG-R2-11",
    "material_id": "Resistor-002", "vendor_code": "V0002", "dc_code": "DC-2024-004",
    "qty": 5000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-01", "slot_id": "A1-6",
      "depth_position": 1, "depth_mm": 15
    }
  },
  // ... (PKG-R2-12 to PKG-R2-20, depth 30-150mm, FULL)

  // Slot B3-L1: Chip-003 x 2 (13" reels)
  {
    "id": "INV-PKG-051", "pkg_code": "PKG-CH-01",
    "material_id": "Chip-003", "vendor_code": "V0002", "dc_code": "DC-2024-005",
    "qty": 2000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-03", "slot_id": "B3-L1",
      "depth_position": 1, "depth_mm": 20
    }
  },
  {
    "id": "INV-PKG-052", "pkg_code": "PKG-CH-02",
    "material_id": "Chip-003", "vendor_code": "V0002", "dc_code": "DC-2024-005",
    "qty": 2000, "uom": "PCS",
    "location": {
      "rack_id": "SMART-RACK-001", "bin_id": "Bin-03", "slot_id": "B3-L1",
      "depth_position": 2, "depth_mm": 40
    }
  }
]
```

**说明**:
- **PKG 级独立记录**: 每个料盘 (PKG) 创建独立库存记录
- **pkg_code**: 保留完整的 PKG 六合一码，支持精确追溯
- **qty**: 单个料盘的数量 (7寸盘 5000 PCS, 13寸盘 2000 PCS)
- **depth_position**: 堆叠位置 (1=底部, 递增向上)
- **depth_mm**: 累计深度 (用于高度验证)
- **vendor_code & dc_code**: 供应商和批次信息 (用于同物料合并判断)
- **总记录数**: 约 49 条 (5+5+10+10+10+10+2, 省略号表示类似记录)

#### 3. 触发的事件 (Triggered Events)

**货架切出触发条件** (离散事件触发):

1. **无可用储位触发**:
   - 场景: 下一个料盘到达，WES 执行智能分箱算法
   - 条件: 分箱算法无法为当前料盘分配储位（所有储位已满或无法容纳）
   - 动作: 立即触发货架切出，请求补充空货架

2. **栈板任务完成触发**:
   - 场景: 当前栈板的所有料盘已完成装箱
   - 条件: 无后续栈板任务
   - 动作: 将已装载的货架切出，送往 SMT 作业区，请求补充空货架

**当前模拟场景状态**:
- Bin-01 使用率: 83.3% (750mm / 900mm)
- 4 个储位已满 (A1-3 到 A1-6)，2 个储位部分使用 (A1-1, A1-2)
- **仍有可用空间**: A1-1 和 A1-2 可继续堆叠
- **下一步动作**: 继续处理后续料盘，直到无可用储位或栈板任务完成

