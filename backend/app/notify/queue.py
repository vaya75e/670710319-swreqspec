from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Callable

import redis


RETRY_INTERVAL = timedelta(minutes=5)
MAX_RETRIES = 3
QUEUE_KEY = "booking:notifications:scheduled"
PENDING_KEY = "booking:notifications:pending"
NotificationSender = Callable[[dict[str, object]], bool]


def _now_utc() -> datetime:
    # รองรับ: NFR-REL-02, IF-NOT-01
    return datetime.now(timezone.utc)


def _build_notification(booking_id: int, hn: str, queue_no: str, scheduled_at: datetime) -> dict[str, object]:
    # รองรับ: FR-BKG-05, IF-NOT-01
    return {
        "booking_id": booking_id,
        "hn": hn,
        "queue_no": queue_no,
        "retry_count": 0,
        "scheduled_at": scheduled_at.isoformat(),
    }


def _mark_failed(notification: dict[str, object], now: datetime) -> str:
    # รองรับ: NFR-REL-02, ASM-03
    retry_count = int(notification["retry_count"]) + 1
    notification["retry_count"] = retry_count
    if retry_count <= MAX_RETRIES:
        notification["scheduled_at"] = (now + RETRY_INTERVAL).isoformat()
        return "retry"
    return "pending"


class InMemoryNotificationQueue:
    # รองรับ: IF-NOT-01, NFR-REL-02
    def __init__(self):
        self._jobs: list[dict[str, object]] = []
        self.pending: list[dict[str, object]] = []
        self._lock = Lock()

    def enqueue(self, booking_id: int, hn: str, queue_no: str) -> None:
        notification = _build_notification(booking_id, hn, queue_no, _now_utc())
        with self._lock:
            self._jobs.append(notification)

    def process_due(self, sender: NotificationSender, now: datetime | None = None) -> dict[str, int]:
        current_time = now or _now_utc()
        with self._lock:
            due_jobs = [
                job for job in self._jobs
                if datetime.fromisoformat(str(job["scheduled_at"])) <= current_time
            ]
            self._jobs = [job for job in self._jobs if job not in due_jobs]

        sent = 0
        rescheduled = 0
        pending = 0
        for job in due_jobs:
            try:
                delivered = sender(job)
            except Exception:
                delivered = False

            if delivered:
                sent += 1
                continue

            state = _mark_failed(job, current_time)
            with self._lock:
                if state == "retry":
                    self._jobs.append(job)
                    rescheduled += 1
                else:
                    self.pending.append(job)
                    pending += 1

        return {"sent": sent, "rescheduled": rescheduled, "pending": pending}

    @property
    def jobs(self) -> list[dict[str, object]]:
        with self._lock:
            return list(self._jobs)


class RedisNotificationQueue:
    # รองรับ: IF-NOT-01, NFR-REL-02
    def __init__(self, client: redis.Redis):
        self._client = client

    def enqueue(self, booking_id: int, hn: str, queue_no: str) -> None:
        notification = _build_notification(booking_id, hn, queue_no, _now_utc())
        member = json.dumps(notification, separators=(",", ":"), sort_keys=True)
        score = datetime.fromisoformat(str(notification["scheduled_at"])).timestamp()
        self._client.zadd(QUEUE_KEY, {member: score})

    def process_due(self, sender: NotificationSender, now: datetime | None = None) -> dict[str, int]:
        current_time = now or _now_utc()
        members = self._client.zrangebyscore(QUEUE_KEY, "-inf", current_time.timestamp())
        sent = 0
        rescheduled = 0
        pending = 0

        for member in members:
            if not self._client.zrem(QUEUE_KEY, member):
                continue

            notification = json.loads(member)
            try:
                delivered = sender(notification)
            except Exception:
                delivered = False

            if delivered:
                sent += 1
                continue

            state = _mark_failed(notification, current_time)
            encoded = json.dumps(notification, separators=(",", ":"), sort_keys=True)
            if state == "retry":
                score = datetime.fromisoformat(str(notification["scheduled_at"])).timestamp()
                self._client.zadd(QUEUE_KEY, {encoded: score})
                rescheduled += 1
            else:
                self._client.rpush(PENDING_KEY, encoded)
                pending += 1

        return {"sent": sent, "rescheduled": rescheduled, "pending": pending}


_memory_queue = InMemoryNotificationQueue()
_redis_queue: RedisNotificationQueue | None = None
_redis_url: str | None = None
_queue_lock = Lock()


def get_notification_queue() -> InMemoryNotificationQueue | RedisNotificationQueue:
    # รองรับ: IF-NOT-01; deployments use Redis and tests use the in-memory queue.
    global _redis_queue, _redis_url
    configured_url = os.getenv("REDIS_URL")
    if not configured_url:
        return _memory_queue

    with _queue_lock:
        if configured_url != _redis_url:
            client = redis.Redis.from_url(configured_url, decode_responses=True)
            _redis_queue = RedisNotificationQueue(client)
            _redis_url = configured_url
        return _redis_queue
