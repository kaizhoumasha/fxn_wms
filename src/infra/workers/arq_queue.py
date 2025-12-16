from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from arq.connections import ArqRedis, RedisSettings, create_pool

from src.core.ports import JobQueue


async def create_arq_pool(redis_url: str) -> ArqRedis:
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
    redis: ArqRedis

    async def enqueue(self, fn: str, *, kwargs: dict, job_id: str | None = None) -> str:
        job = await self.redis.enqueue_job(fn, **kwargs, _job_id=job_id)
        if job is None:
            return job_id or ""
        return job.job_id if hasattr(job, "job_id") else job.id
