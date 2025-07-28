from collections import defaultdict
import time
from fastapi import Request, HTTPException, status


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.storage = defaultdict(list)

    def __call__(self, request: Request) -> None:
        ip = request.client.host if request.client else "anonymous"
        now = time.time()
        timestamps = [t for t in self.storage[ip] if now - t < self.window_seconds]
        if len(timestamps) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
        timestamps.append(now)
        self.storage[ip] = timestamps

    def reset(self) -> None:
        self.storage.clear()
