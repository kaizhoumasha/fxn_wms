from __future__ import annotations

from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from src.core.models import InboundOrder, OutboxEvent


@dataclass(frozen=True, slots=True)
class CreateInboundOrder:
    """
    创建入库单命令的数据类
    
    Attributes:
        request_id: 请求ID
        grn_id: 货物接收单ID
        dock_id: 码头ID
        payload: 负载数据字典
    """
    request_id: str
    grn_id: str
    dock_id: str
    payload: dict


class InboundOrderRepository(Protocol):
    """
    入库单仓储协议接口
    定义了处理入库单数据访问的方法
    """
    
    async def create_or_get(self, cmd: CreateInboundOrder) -> tuple[InboundOrder, bool]: 
        """
        创建或获取入库单
        
        Args:
            cmd: 创建入库单命令对象
            
        Returns:
            包含入库单对象和是否新建标志的元组
        """
        ...
    
    async def get(self, inbound_order_id: UUID) -> InboundOrder | None: 
        """
        根据ID获取入库单
        
        Args:
            inbound_order_id: 入库单UUID
            
        Returns:
            入库单对象，如果不存在则返回None
        """
        ...
    
    async def mark_processed(self, inbound_order_id: UUID) -> None: 
        """
        标记入库单为已处理
        
        Args:
            inbound_order_id: 入库单UUID
        """
        ...


class OutboxRepository(Protocol):
    """
    发件箱仓储协议接口
    定义了处理发件箱事件的方法
    """
    
    async def add(self, event: OutboxEvent) -> None: 
        """
        添加发件箱事件
        
        Args:
            event: 发件箱事件对象
        """
        ...
    
    async def claim_batch(self, *, limit: int) -> list[OutboxEvent]: 
        """
        声明一批发件箱事件进行处理
        
        Args:
            limit: 批量处理数量限制
            
        Returns:
            发件箱事件列表
        """
        ...
    
    async def mark_delivered(self, event_id: UUID) -> None: 
        """
        标记发件箱事件为已发送
        
        Args:
            event_id: 事件UUID
        """
        ...
    
    async def mark_failed(self, event_id: UUID, *, error: str) -> None: 
        """
        标记发件箱事件为发送失败
        
        Args:
            event_id: 事件UUID
            error: 错误信息
        """
        ...


class JobQueue(Protocol):
    """
    作业队列协议接口
    定义了任务队列操作方法
    """
    
    async def enqueue(self, fn: str, *, kwargs: dict, job_id: str | None = None) -> str: 
        """
        将任务加入队列
        
        Args:
            fn: 函数名称
            kwargs: 函数参数字典
            job_id: 任务ID，可选
            
        Returns:
            任务ID字符串
        """
        ...


class WmsClient(Protocol):
    """
    WMS客户端协议接口
    定义了与WMS系统交互的方法
    """
    
    async def post_inventory_putaway(self, payload: dict) -> None: 
        """
        发送库存上架请求
        
        Args:
            payload: 请求负载数据
        """
        ...
