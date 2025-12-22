# 料盘装箱区模拟步骤 v1.0

## 前置条件
- 两条流水线：Line 1（仅7寸），Line 2（7寸+13/15寸）
- 资源管理：共享模式（空货架存放区公共）
- 料箱类型：A型（6×7寸位），B型（2×7寸位+1×大尺寸位）
- 单层货架：可放4个料箱，A/B型可混装

## 已明确的业务规则
1. **混装栈板路由**：Line 2优先呼叫混装栈板
2. **DC匹配**：精确匹配（DC 2024-01-01 ≠ DC 2024-01-02）
3. **厚度数据源**：以机械臂实测为准，WMS数据仅作参考
4. **空储位选择**：优先放入装载率高的料箱
5. **货架-料箱绑定校验**：不一致则报警停止作业
6. **资源管理**：共享模式

## 待明确的问题
- 机械臂HOLD时长和超时处理（问题2）
- 人工拆箱节奏匹配（问题3）
- 其他NG类型处理流程（问题9）
- 货架切换超时降级策略（问题10）

## 模拟场景设定
- 栈板P001：混装50个7寸料盘（料号R001）+ 20个13寸料盘（料号R002）
- 目标流水线：Line 2（因为混装了13寸）
- 初始货架R001：4个料箱[B001(A型), B002(A型), B003(B型), B004(B型)]，全部为空

## 详细模拟步骤

### 阶段1：数据初始化
**Step 1.1 - 系统配置**
- WMS配置料箱类型：
  - A型：6个7寸储位，每个储位深度100mm
  - B型：2个7寸储位（深度100mm）+ 1个大尺寸储位（深度150mm）
- WMS配置物料主数据：
  - R001：7寸料盘，参考厚度10mm，参考尺寸180mm×180mm
  - R002：13寸料盘，参考厚度15mm，参考尺寸330mm×330mm

**Step 1.2 - 货架初始化**
- 空货架R001到达Line 2出料位
- ECS扫描货架码：R001
- ECS扫描料箱码：B001, B002, B003, B004
- ECS → WES: `POST /api/v1/callback/event`
  ```json
  {
    "device_id": "ECS_LINE_2",
    "event_type": "RACK_ARRIVED",
    "timestamp": 1702627200000,
    "data": {
      "rack_id": "R001",
      "bins": [
        {"bin_id": "B001", "type": "A", "position": 1},
        {"bin_id": "B002", "type": "A", "position": 2},
        {"bin_id": "B003", "type": "B", "position": 3},
        {"bin_id": "B004", "type": "B", "position": 4}
      ]
    }
  }
  ```
- WES处理：
  1. 接收事件，解析数据
  2. WES → WMS: 调用内部接口建立货架与料箱绑定
  3. WMS初始化储位状态表（逻辑同前）
  4. WES更新本地缓存状态

### 阶段2：栈板到位与人工拆箱
**Step 2.1 - 栈板路由**
- 栈板P001到达收货暂存区
- WMS查询栈板P001的物料清单：
  - GRN-001: 料号R001（7寸），数量50
  - GRN-002: 料号R002（13寸），数量20
- WMS判断：混装了13寸料盘 → 路由到Line 2
- WMS生成搬运任务 → RCS调度AGV → 栈板P001到达Line 2入料位

**Step 2.2 - 人工拆箱**
- 人工PDA扫描栈板号P001
- WMS显示待拆箱清单：GRN-001（R001，50个），GRN-002（R002，20个）
- 人工拆第1箱（假设5个7寸料盘，属于GRN-001）
- 人工将5个料盘串到串杆1上
- 人工拆第2箱（假设3个13寸料盘，属于GRN-002）
- 人工将3个料盘串到串杆2上
- ...（继续拆箱，直到串杆满或栈板拆完）

**注意**：人工拆箱节奏与机械臂装箱节奏的匹配问题待明确（问题3）

### 阶段3：机械臂装箱（正常流程）
**Step 3.1 - 第1个料盘（7寸，R001）**
- 串杆1移动到工作位，机械臂抓取第1个料盘
- 机械臂扫描PKG码：R001-PKG001
- 机械臂测量：厚度10.2mm，尺寸182mm×181mm
- ECS → WES: `POST /api/v1/callback/event`
  ```json
  {
    "device_id": "ECS_LINE_2",
    "event_type": "MATERIAL_SCANNED",
    "timestamp": 1702627210000,
    "data": {
      "pkg_code": "R001-PKG001",
      "thickness": 10.2,
      "dimensions": "182x181"
    }
  }
  ```

**Step 3.2 - WES计算与指令下发**
- WES处理：
  1. 解析PKG码，从 WMS 获取物料主数据与 GRN 信息
  2. 校验：R001存在且属于GRN-001 ✓
  3. 应用装箱算法（同前）：
     - 查找同类储位 → 无
     - 查找空储位 → 选择 B001 (装载率优先)
     - 选择 B001-Slot1
     - 校验容量 ✓
- WES → ECS: `POST /api/v1/device/command`
  ```json
  {
    "command_id": "CMD-KIT-001",
    "task_type": "PUT_INSTRUCTION",
    "priority": 5,
    "params": {
      "bin_id": "B001",
      "slot_id": "Slot1",
      "pkg_code": "R001-PKG001",
      "expected_stack_height": 10.2
    }
  }
  ```
- ECS → WES: `200 OK` (Ack)

**Step 3.3 - 机械臂放入料盘与确认**
- 机械臂将料盘放入B001-Slot1
- 机械臂测量实际堆叠高度：10.2mm ✓
- ECS → WES: `POST /api/v1/callback/result`
  ```json
  {
    "command_id": "CMD-KIT-001",
    "device_id": "ECS_LINE_2",
    "result": "SUCCESS",
    "finish_time": 1702627220000,
    "data": {
      "actual_height": 10.2
    }
  }
  ```
- WES处理：
  1. 收到成功回执
  2. WES → WMS: 调用内部接口更新库存状态
     - B001-Slot1: 已用深度10.2mm，剩余深度89.8mm
     - 绑定PKG: R001-PKG001 → B001-Slot1
     - 更新GRN-001: 已装箱数量+1
  3. WES → ECS: `200 OK`

**Step 3.4 - 第2个料盘（7寸，R001，同DC）**
- 机械臂抓取第2个料盘：R001-PKG002（DC=2024-01-01，厚度10.1mm）
- ECS 上报 `MATERIAL_SCANNED` 事件
- WES计算箱号：
  1. 查找"同类"储位（Material=R001, Vendor=V001, DC=2024-01-01）→ 找到B001-Slot1 ✓
  2. 检查容量：剩余深度89.8mm ≥ 厚度10.1mm ✓
  3. 选择B001-Slot1（堆叠）
- WES 下发 `PUT_INSTRUCTION` (CMD-KIT-002)
- 机械臂放入B001-Slot1（堆叠在PKG001上），回传 Result
- WES 更新状态：B001-Slot1已用深度20.3mm，剩余深度79.7mm

**Step 3.5 - 重复处理7寸料盘**
- 继续处理剩余的7寸料盘（R001-PKG003 ~ PKG050）
- WES 应用同类合并策略：优先堆叠到已有R001+V001+DC=2024-01-01的储位
- 当B001-Slot1满了（剩余深度<10mm），WES 选择B001-Slot2
- 当B001全部满了，根据"优先放入装载率高的料箱"策略，WES 选择B002
- ...

### 阶段4：机械臂装箱（13寸料盘，触发货架切换）
**Step 4.1 - 第51个料盘（13寸，R002）**
- 机械臂抓取第51个料盘：R002-PKG051（13寸，厚度15.3mm）
- ECS 上报 `MATERIAL_SCANNED`
- WES计算箱号：
  1. 查找"同类"储位（Material=R002, Vendor=V002, DC=2024-01-02）→ 无
  2. 查找空储位（13寸料盘 → 需要B型大尺寸位）：
     - B003-Slot3（大尺寸位）：空闲 ✓
     - B004-Slot3（大尺寸位）：空闲 ✓
  3. 应用策略"优先放入装载率高的料箱"：
     - B003装载率：假设7寸位已满，装载率66.7%（2/3）
     - B004装载率：假设7寸位为空，装载率0%（0/3）
     - 选择B003（装载率更高）
  4. 选择B003-Slot3
- WES 下发 `PUT_INSTRUCTION` -> ECS 执行 -> 回传 Result
- WES更新状态：B003-Slot3已用深度15.3mm，剩余深度134.7mm

**Step 4.2 - 继续处理13寸料盘**
- 处理R002-PKG052 ~ PKG060（共10个13寸料盘）
- 堆叠到B003-Slot3，直到满了（剩余深度<15mm）
- 然后使用B004-Slot3

**Step 4.3 - 触发货架切换（第61个料盘）**
- 机械臂抓取第61个料盘：R002-PKG061（13寸，厚度15.2mm）
- ECS 上报 `MATERIAL_SCANNED` (Event)
- WES计算箱号：
  1. 查找"同类"储位 → B003-Slot3和B004-Slot3都有R002
  2. 检查容量：
     - B003-Slot3剩余深度8mm < 15.2mm ✗
     - B004-Slot3剩余深度9mm < 15.2mm ✗
  3. 查找空储位（B型大尺寸位）→ 无 ✗
  4. 判断：需要换货架
- WES 决策：暂停装箱，触发换架
- WES → ECS: 暂不下发 `PUT_INSTRUCTION` (或下发一个 `WAIT` 类型的 `PROCESS` 指令，视具体协议实现而定)
  *注：ECS 侧会处于等待指令状态*

**Step 4.4 - 货架切换流程**
- WES生成搬运任务：
  1. 搬走满货架R001 → SMT作业区待入库缓存区
  2. 搬来空货架R002 → Line 2出料位
- WES → WMS: 请求创建 RCS 任务
- WMS → RCS: 呼叫AGV执行搬运任务
- 机械臂进入HOLD状态，等待新货架到位

**关键问题**：
- 机械臂能HOLD多久？（待回答问题2）
- 如果AGV超时怎么办？（待回答问题2和10）

**Step 4.5 - 新货架到位与恢复**
- AGV将货架R002搬运到Line 2出料位
- ECS扫描货架R002 (上报 `RACK_ARRIVED` 事件)
- WES接收事件，建立新绑定 (R002)
- WES重新处理之前挂起的 R002-PKG061 分箱请求（或等待 ECS 超时重试 `MATERIAL_SCANNED`）
- WES计算箱号：选择R002的B型料箱的大尺寸位
- WES → ECS: 下发 `PUT_INSTRUCTION` (CMD-KIT-061)
- 机械臂从HOLD状态恢复，放入料盘

### 阶段5：异常处理（NG流程）
**Step 5.1 - 料盘放反（无法扫码）**
- 机械臂抓取料盘，尝试扫描PKG码 → 失败（料盘放反）
- ECS重试3次 → 仍然失败
- ECS判断：料盘放反
- 机械臂将料盘放入NG口
- ECS → WES: `POST /api/v1/callback/event`
  ```json
  {
    "device_id": "ECS_LINE_2",
    "event_type": "SCAN_FAILED",
    "timestamp": 1702627400000,
    "data": {
      "reason": "料盘放反，无法扫描PKG码"
    }
  }
  ```
  *(注：如果是因为之前收到了 SCAN 指令，则应调用 callback/result 返回 FAILED)*
- WES 记录异常日志
- 人工处理：从NG口取出料盘，翻转，重新放回串杆

**Step 5.2 - 其他NG类型**
待明确（问题9）：
- 标签破损/无法识别
- 读码错误（PKG码与WMS主数据不匹配）
- 尺寸异常（实测尺寸与WMS主数据偏差过大）

### 阶段6：完成与清理
**Step 6.1 - 栈板拆箱完成**
- 人工拆完栈板P001的所有箱子
- 人工PDA扫描栈板号P001，点击"拆箱完成"
- WMS校验：GRN-001和GRN-002的数量是否匹配
- WMS生成空栈板搬运任务 → RCS调度AGV → 栈板P001送回空栈板存放区

**Step 6.2 - 货架装满**
- WES/WMS 检测到货架R002的所有储位都满了
- WES 触发满架流程
- WMS生成搬运任务：货架R002 → SMT作业区待入库缓存区
- WMS呼叫新的空货架R003 → Line 2出料位
- 继续作业...

## 关键数据结构

### 货架-料箱-储位状态表
```json
{
  "rack_id": "R001",
  "line_id": "Line2",
  "status": "in_use",
  "bins": [
    {
      "bin_id": "B001",
      "type": "A",
      "position": 1,
      "slots": [
        {
          "slot_id": "Slot1",
          "type": "7inch",
          "depth_total": 100,
          "depth_used": 20.3,
          "depth_remaining": 79.7,
          "trays": [
            {"pkg": "R001-PKG001", "thickness": 10.2},
            {"pkg": "R001-PKG002", "thickness": 10.1}
          ]
        },
        // ... Slot2-6
      ]
    },
    // ... B002, B003, B004
  ]
}
```

### 装箱算法伪代码
```python
def calculate_bin_slot(pkg_info):
    # 1. 提取料盘信息
    material = pkg_info.material
    vendor = pkg_info.vendor
    dc = pkg_info.dc
    size = pkg_info.size  # 7寸 or 13寸
    thickness = pkg_info.thickness
    
    # 2. 查找"同类"储位（精确匹配DC）
    same_slots = find_slots(material=material, vendor=vendor, dc=dc)
    for slot in same_slots:
        if slot.depth_remaining >= thickness:
            return slot  # 堆叠到同类储位
    
    # 3. 查找空储位
    if size == "7inch":
        # 7寸料盘：可以放入A型或B型的7寸位
        empty_slots = find_empty_slots(type=["A_7inch", "B_7inch"])
    else:
        # 13/15寸料盘：只能放入B型的大尺寸位
        empty_slots = find_empty_slots(type=["B_large"])
    
    if not empty_slots:
        return None  # 需要换货架
    
    # 4. 应用策略"优先放入装载率高的料箱"
    bins_by_load_rate = sort_bins_by_load_rate(empty_slots)
    for bin in bins_by_load_rate:
        for slot in bin.slots:
            if slot.is_empty and slot.depth_total >= thickness:
                return slot
    
    return None  # 理论上不应该到这里
```

## ECS 接口定义 (遵循白皮书)
供应商需实现：
1. **接收指令**: `POST /api/v1/device/command`
   - 支持 `task_type`: `PUT_INSTRUCTION`, `SCAN` (如需)
2. **设备状态查询**: `GET /api/v1/device/status`

WES 提供回调：
1. **结果回传**: `POST /api/v1/callback/result`
   - 用于反馈 `PUT_INSTRUCTION` 的执行结果
2. **事件上报**: `POST /api/v1/callback/event`
   - 用于上报 `RACK_ARRIVED`, `MATERIAL_SCANNED`, `SCAN_FAILED` 等事件
