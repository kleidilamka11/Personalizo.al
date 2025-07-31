from fastapi import Request, HTTPException, status
import redis
from app.core.config import settings


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60, redis_url: str | None = None):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        url = redis_url or settings.REDIS_URL
        self.redis = redis.Redis.from_url(url, decode_responses=True)

    def __call__(self, request: Request) -> None:
        ip = request.client.host if request.client else "anonymous"
        key = f"rl:{ip}:{request.url.path}"
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, self.window_seconds)
        if count > self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )

    def reset(self) -> None:
        for key in self.redis.scan_iter(match="rl:*"):
            self.redis.delete(key)
