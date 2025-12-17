from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from arq.connections import ArqRedis, RedisSettings, create_pool

from src.core.ports import JobQueue


async def create_arq_pool(redis_url: str) -> ArqRedis:
    """
    根据Redis连接URL创建ARQ连接池
    
    Args:
        redis_url: Redis连接URL，支持redis://或rediss://协议
        
    Returns:
        ArqRedis: 配置好的ARQ Redis连接池实例
    """
    # 解析Redis连接URL并创建相应的配置
    parsed = urlparse(redis_url)
    settings = RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        database=int((parsed.path or "/0").lstrip("/") or "0"),
        password=parsed.password,
        ssl=parsed.scheme == "rediss",
    )
    return await create_pool(settings)


@dataclass(frozen=True, slots=True)
class ArqJobQueue(JobQueue):
    """
    基于ARQ的任务队列实现
    
    实现JobQueue协议，提供异步任务队列功能
    """
    redis: ArqRedis

    async def enqueue(self, fn: str, *, kwargs: dict, job_id: str | None = None) -> str:
        """
        将任务加入队列
        
        Args:
            fn: 要执行的函数名称
            kwargs: 函数的关键字参数字典
            job_id: 可选的任务唯一标识符
            
        Returns:
            任务ID字符串
        """
        job = await self.redis.enqueue_job(fn, **kwargs, _job_id=job_id)
        print('job:', job)
        if job is None:
            return job_id or ""
        return job.job_id if hasattr(job, "job_id") else job.id