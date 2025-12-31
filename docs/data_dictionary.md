# fxn-wms 全域数据字典 (Data Dictionary)

> **版本**: v1.0
> **日期**: 2025-12-31
> **说明**: 本文档汇总了 WMS (SQL Server) 和 WES (PostgreSQL) 的完整数据库模型，涵盖业务主数据、执行数据、审计日志及系统降级支持模型。

---

# 1. WMS 域 (SQL Server)

WMS 是系统的**业务决策、账务核心与人工兜底中心**。它管理全局主数据、库存账务，并在自动化设备失效时提供人工操作指引。

## 1.1 物理结构主数据 (Physical Master Data - Fallback Support)
*用于支持系统降级，使 WMS 在 WES 离线时仍能理解物理结构并指导人工操作。*

### `WMS_Rack_Profile` (货架规格表)
定义货架的物理模板。
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **profile_id** | VARCHAR(20) [PK] | 规格代码 (如 `FIVE_LAYER_STD`, `SINGLE_LAYER`) |
| **rack_type** | VARCHAR(20) | 类型：`SINGLE` (单层), `FIVE` (五层), `RETURN` (退料) |
| **total_layers** | INT | 总层数 |
| **has_sides** | BIT | 是否分AB面 (1=是, 0=否) |
| **bins_per_layer** | INT | 每层料箱位数 (通常为 4) |
| **is_slot_managed** | BIT | 是否直存料盘 (1=是, 0=存料箱) |

### `WMS_Bin_Profile` (料箱规格表)
定义料箱内部的格口布局。
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **profile_id** | VARCHAR(20) [PK] | 规格代码 (如 `BIN_TYPE_A`, `BIN_TYPE_B`) |
| **total_cells** | INT | 总格口数 |
| **cell_layout_json** | NVARCHAR(MAX) | JSON 描述格口布局，用于 PDA 渲染 (如 `{"1":"7inch", "7":"15inch"}`) |
| **max_depth** | DECIMAL(10,2) | 最大深度 (mm) |

### `WMS_Rack_Instance` (货架实例表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **rack_code** | VARCHAR(50) [PK] | 货架条码 (LPN) |
| **profile_id** | VARCHAR(20) [FK] | 关联货架规格 |
| **current_zone** | VARCHAR(50) | 当前所在逻辑区域 (SMT/IQC/DOCK) |
| **manual_lock** | BIT | 人工锁定状态 (1=人工操作中，禁止 AGV 调度) |

### `WMS_Location` (库位/地码表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **location_code** | VARCHAR(50) [PK] | 地码/库位编码 |
| **zone_code** | VARCHAR(50) | 所属区域 |
| **location_type** | VARCHAR(20) | 类型 (BUFFER, STORAGE, WORKSTATION) |
| **status** | VARCHAR(20) | 状态 (EMPTY, OCCUPIED, LOCKED) |
| **current_rack_code** | VARCHAR(50) [FK] | 当前停放的货架 (可空) |

---

## 1.2 业务主数据 (Business Master Data)

### `material` (物料主数据 - 扩展)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **material_id** | VARCHAR(50) [PK] | 物料编码 |
| **material_name** | NVARCHAR(200) | 物料名称 |
| **material_type** | VARCHAR(50) | 物料大类 |
| **is_high_value** | BIT | 是否高价值 (决定路由: 高价值区) |
| **is_msd** | BIT | 是否湿敏器件 (决定路由: MSD区) |
| **is_pcb** | BIT | 是否 PCB |
| **is_structural** | BIT | 是否机构件 |

### `routing_rule` (路由规则表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **rule_id** | VARCHAR(50) [PK] | 规则 ID |
| **material_type** | VARCHAR(50) | 匹配的物料类型 |
| **target_location** | VARCHAR(50) | 目标存储区域 |
| **requires_iqc** | BIT | 是否需要 IQC |
| **priority** | INT | 优先级 |

---

## 1.3 入库与绑定 (Inbound & Binding - 3.2.1)

### `arrival_record` (到货登记表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **arrival_id** | VARCHAR(50) [PK] | 到货记录 ID |
| **vehicle_number** | VARCHAR(50) | 车牌/快递号 |
| **box_count** | INT | 登记箱数 |
| **status** | VARCHAR(20) | `PENDING_MANIFEST`, `VALIDATED`, `MISMATCH` |

### `arrival_manifest` (到货清单表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **manifest_id** | VARCHAR(50) [PK] | 清单 ID |
| **arrival_id** | VARCHAR(50) [FK] | 关联到货登记 |
| **grn_number** | VARCHAR(50) | SAP GRN 单号 |
| **manifest_status** | VARCHAR(20) | 清单状态 |

### `binding_detail` (绑定明细表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **binding_id** | VARCHAR(50) [PK] | 绑定 ID |
| **pallet_id** | VARCHAR(50) [FK] | 所属栈板 |
| **grn_number** | VARCHAR(50) | 关联 GRN |
| **material_id** | VARCHAR(50) | 物料编码 |
| **qty** | DECIMAL(18,4) | 绑定数量 |
| **pkg_code** | VARCHAR(100) | 原始箱条码内容 |

### `pallet` (栈板主表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **pallet_id** | VARCHAR(50) [PK] | 栈板号 (LPN) |
| **status** | VARCHAR(20) | `NEW`, `BOUND`, `MOVING`, `WAITING_IQC`, `STORED`, `EMPTY` |
| **current_location** | VARCHAR(50) | 当前位置 |
| **material_type** | VARCHAR(50) | 栈板物料属性 (用于混托校验) |

### `six_in_one_binding` (六合一绑定表 - 3.5)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **binding_id** | VARCHAR(50) [PK] | 绑定 ID |
| **pallet_id** | VARCHAR(50) [FK] | 栈板 ID |
| **six_in_one_barcode** | VARCHAR(100) | PKG 六合一码 (用于追溯) |
| **grn_number** | VARCHAR(50) | 关联 GRN |

---

## 1.4 库存管理 (Inventory)

### `WMS_Inventory_Detail` (精细化库存明细)
*记录库存的逻辑位置，支持到格口级别以供降级使用。*
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **inventory_id** | BIGINT [PK] | 自增 ID |
| **pkg_code** | VARCHAR(100) | PKG 六合一码 (业务主键) |
| **material_id** | VARCHAR(50) | 物料编码 |
| **rack_code** | VARCHAR(50) | 所在货架 |
| **bin_code** | VARCHAR(50) | 所在料箱 (可空) |
| **side** | CHAR(1) | 面向 (A/B) |
| **layer** | INT | 层号 |
| **cell_index** | INT | **格口号** (支持人工定位) |
| **stack_seq** | INT | **堆叠顺序** (1=最下/最里) |
| **qty** | DECIMAL(18,4) | 数量 |
| **status** | VARCHAR(20) | `INSTOCK`, `PICKED`, `LOCKED` |

---

## 1.5 质量与 IQC (Quality & IQC - 3.2.2)

### `iqc_pending_task` (IQC 待送检任务)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **task_id** | VARCHAR(50) [PK] | 任务 ID |
| **grn_number** | VARCHAR(50) | 关联 GRN |
| **sampling_qty** | DECIMAL(18,4) | 需抽检数量 |
| **priority** | INT | 优先级 (1-10) |
| **status** | VARCHAR(20) | `PENDING_CALL`, `CALLED`, `IN_TRANSIT` |

### `pallet_grn_inspection` (栈板-GRN 检验状态)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **record_id** | VARCHAR(50) [PK] | 记录 ID |
| **pallet_id** | VARCHAR(50) | 栈板号 |
| **grn_number** | VARCHAR(50) | GRN 号 |
| **inspection_status** | VARCHAR(20) | `SAMPLING`, `INSPECTING`, `PENDING_REVIEW` |
| **qms_result** | VARCHAR(20) | `OK`, `NG`, `SORTING` |

### `sampling_record` (取样记录)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **sampling_id** | VARCHAR(50) [PK] | 取样 ID |
| **pallet_id** | VARCHAR(50) | 来源栈板 |
| **pkg_code** | VARCHAR(100) | 取样的 PKG |
| **status** | VARCHAR(20) | `SAMPLED` (已取走), `RETURNED` (已归还) |

---

## 1.6 生产发料 (Production Issue - 3.3.3)

### `WMS_ProductionIssueTasks` (发料任务主表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **TaskID** | VARCHAR(50) [PK] | 任务 ID |
| **WorkOrder** | VARCHAR(50) | SAP 工单号 |
| **Priority** | INT | 优先级 |
| **Status** | VARCHAR(20) | `PENDING`, `WES_PROCESSING`, `COMPLETED` |

### `WMS_ProductionIssueMaterials` (发料物料明细)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **ID** | INT [PK] | 自增 ID |
| **TaskID** | VARCHAR(50) [FK] | 关联任务 |
| **MaterialID** | VARCHAR(50) | 物料编码 |
| **RequiredQty** | INT | 需求数量 |
| **CompletedQty** | INT | 已发数量 |

### `WMS_ProductionIssueTrays` (发料料盘明细)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **ID** | INT [PK] | 自增 ID |
| **TaskID** | VARCHAR(50) [FK] | 关联任务 |
| **PKGCode** | VARCHAR(100) | 指定拣选的 PKG |
| **SourceLocation** | VARCHAR(100) | 源位置 (WMS 规划) |
| **Status** | VARCHAR(20) | `PENDING`, `PICKED` |

---

## 1.7 审计、异常与日志 (Audit & Logs)

### `api_integration_log` (API 集成日志)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **log_id** | VARCHAR(50) [PK] | 日志 ID |
| **api_type** | VARCHAR(50) | `SAP`, `RCS`, `QMS`, `WES` |
| **request_url** | VARCHAR(500) | 请求地址 |
| **request_payload** | JSON | 请求体 |
| **response_status** | INT | HTTP 状态码 |
| **related_entity_id** | VARCHAR(50) | 关联业务 ID (如 PalletID) |

### `pallet_status_history` (栈板状态流水)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **history_id** | VARCHAR(50) [PK] | 历史 ID |
| **pallet_id** | VARCHAR(50) | 栈板号 |
| **old_status** | VARCHAR(50) | 原状态 |
| **new_status** | VARCHAR(50) | 新状态 |
| **changed_by** | VARCHAR(50) | 操作人/系统 |

### `WMS_Manual_Work_Task` (人工兜底任务)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **task_id** | VARCHAR(50) [PK] | 任务 ID |
| **work_type** | VARCHAR(20) | `MANUAL_PICK`, `MANUAL_PUT` |
| **target_rack** | VARCHAR(50) | 目标货架 |
| **target_cell** | INT | 目标格口 (PDA 指引核心) |
| **guide_message** | NVARCHAR(200) | 操作指引 (如"请注意A面") |
| **status** | VARCHAR(20) | `PENDING`, `COMPLETED` |

---

# 2. WES 域 (PostgreSQL)

WES 是**执行控制、算法策略与设备协调中心**。它管理微观的物理动作和设备状态。

## 2.1 核心设备与平台 (Core Platform - 3.3.0)

### `devices` (设备主数据)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **device_id** | VARCHAR(50) [PK] | 设备 ID |
| **type** | VARCHAR(20) | `ECS`, `CTU`, `AGV` |
| **base_url** | VARCHAR(200) | 设备 API 地址 |
| **status** | VARCHAR(20) | `IDLE`, `RUNNING`, `ERROR`, `OFFLINE` |
| **health_check_interval** | INT | 健康检查间隔 (秒) |

### `tasks` (WES 核心任务表)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **task_id** | VARCHAR(50) [PK] | 任务 ID |
| **command_id** | VARCHAR(50) | **幂等键** (CMD-时间戳-序号) |
| **device_id** | VARCHAR(50) | 目标设备 |
| **task_type** | VARCHAR(20) | `PICK`, `PUT`, `SCAN` |
| **priority** | INT | 优先级 (1-10) |
| **status** | VARCHAR(20) | `PENDING`, `RUNNING`, `COMPLETED`, `FAILED` |
| **params** | JSONB | 任务参数 |

### `wes_commands` (原子指令表 - 3.3.3)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **command_id** | VARCHAR(50) [PK] | 指令 ID |
| **task_id** | VARCHAR(50) [FK] | 关联 WES 任务 |
| **command_type** | VARCHAR(20) | `PICK`, `TRANSFER` |
| **working_height** | DECIMAL(10,2) | 机械臂工作高度 (mm) |
| **status** | VARCHAR(20) | `SENT`, `COMPLETED`, `FAILED` |

---

## 2.2 物理状态与算法 (Physical State & Algorithm)

### `bin_inventory_cache` (料箱物理缓存)
*WES 分箱算法的核心数据源，记录料箱内的实时物理状态。*
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **bin_id** | VARCHAR(50) [PK] | 料箱 ID |
| **rack_id** | VARCHAR(50) | 所在货架 |
| **rack_type** | VARCHAR(20) | `SINGLE_LAYER`, `FIVE_LAYER` |
| **tray_count** | INT | 当前料盘数 |
| **usage_rate** | DECIMAL(5,2) | 容量使用率 (0.00 - 1.00) |
| **metadata** | JSONB | 详细 Slot 占用情况 (用于深度计算) |

### `rack_locations` (货架逻辑地图)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **location_id** | VARCHAR(50) [PK] | 逻辑位置 ID (如 `WORK_POS_1`) |
| **area_type** | VARCHAR(30) | `SMT_WORK`, `EXCHANGE_AREA` |
| **rack_id** | VARCHAR(50) | 当前停放的货架 (可空) |
| **is_occupied** | BOOLEAN | 是否占用 |

---

## 2.3 SMT 业务追踪 (SMT Business Tracking - 3.3.1 ~ 3.3.3)

### `kitting_task` (智能装箱任务)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **task_id** | VARCHAR(50) [PK] | 任务 ID |
| **pallet_id** | VARCHAR(50) | 待拆栈板 |
| **processed_qty** | DECIMAL(18,4) | 已装箱数量 |
| **assigned_line** | VARCHAR(20) | 分配线体 (`LINE_1`, `LINE_2`) |
| **status** | VARCHAR(20) | `DISPATCHED`, `PROCESSING`, `COMPLETED` |

### `hybrid_inbound_tasks` (混合入库任务)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **task_id** | UUID [PK] | 任务 ID |
| **task_type** | VARCHAR(20) | `FULL_EXCHANGE` (满箱交换), `PIPELINE_PICKING` (拣选) |
| **source_bin_id** | VARCHAR(50) | 源料箱 |
| **target_bin_id** | VARCHAR(50) | 目标料箱 (交换模式用) |
| **status** | VARCHAR(20) | `PENDING`, `COMPLETED` |

### `smt_bin_tracking` (流水线料盒追踪)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **id** | SERIAL [PK] | 自增 ID |
| **bin_code** | VARCHAR(50) | 料盒码 |
| **current_location** | VARCHAR(100) | 当前流水线位置 |
| **recognition_stage**| VARCHAR(30) | `ENTRY`, `PLATFORM`, `WORK_POS` (识别阶段) |
| **orientation** | VARCHAR(20) | `NORMAL`, `REVERSE` (料盒朝向) |
| **status** | VARCHAR(20) | `ON_CONVEYOR`, `COMPLETED` |

---

## 2.4 日志与审计 (Logs & Audit)

### `command_log` (原始命令日志)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **command_id** | VARCHAR(50) [PK] | 命令 ID |
| **source_system** | VARCHAR(50) | 来源 (WMS) |
| **command_payload** | JSONB | 原始指令内容 |
| **processed_at** | TIMESTAMP | 处理时间 |

### `task_retry_history` (任务重试历史)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **retry_id** | VARCHAR(50) [PK] | 重试 ID |
| **task_id** | VARCHAR(50) | 关联任务 |
| **retry_attempt** | INT | 重试次数 (1, 2, 3) |
| **error_message** | TEXT | 失败原因 |
| **retry_delay_ms** | INT | 延迟时间 |

### `device_status_history` (设备状态流水)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **history_id** | VARCHAR(50) [PK] | 历史 ID |
| **device_id** | VARCHAR(50) | 设备 ID |
| **old_status** | VARCHAR(20) | 原状态 |
| **new_status** | VARCHAR(20) | 新状态 |
| **error_code** | VARCHAR(50) | 故障码 |

### `smt_return_conveyor_log` (退料回流日志)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| **id** | SERIAL [PK] | 自增 ID |
| **bin_code** | VARCHAR(50) | 料盒码 |
| **error_type** | VARCHAR(30) | `SCAN_FAIL`, `PKG_MISMATCH`, `ORIENTATION_ERROR` |
| **processing_status** | VARCHAR(30) | `RETURNING`, `RETURNED` |
