# Exception & Compensation（异常与补偿）

**Feature**: 002-detailed-design  
**Scope**: 锁冲突、拒单、超时、设备故障、网络异常的检测与兜底。

## 场景清单
- **锁冲突/库存锁**：下发任务/回执更新失败 → 重试≤3，仍失败转人工兜底并记录告警。  
- **拒单/NO_CAPACITY**：RCS 返回不可用/拒单 → 退避重试，必要时改派/人工调度。  
- **超时**：单步超时/回调超时 → 触发取消或 continueTask，告警并人工介入。  
- **设备故障/告警**：流水线卡滞、机械臂失败、拆包失败、检测超差 → reasonCode + 位置，人工放行/复核。  
- **网络/解析异常**：MQTT/SSE/HTTP 解析失败 → 4xx/5xx 告警，供应商可补发。

## 处理策略
- 重试：指数退避，≤3 次；失败后升级为人工兜底。  
- 补偿：撤销/取消任务（cancelTask），或重新下发新任务号；保持幂等键一致。  
- 告警：推送到监控（告警级别 info/warn/error），记录 TaskId/ContainerId/PositionCode/TraceRef。  
- 审计：异常处理需写入审计日志（操作人/时间/动作/原因）。

## TraceRef
- TraceRef: docs/origin/... （待补行号）
