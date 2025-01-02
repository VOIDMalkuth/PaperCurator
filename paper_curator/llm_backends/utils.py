import time
from typing import Optional


class IntervalTimer:
    def __init__(self, interval_sec: float):
        self.last_time: Optional[float] = None
        self.interval_sec = interval_sec

    def record(self) -> None:
        """Record current time"""
        self.last_time = time.monotonic()

    def has_elapsed_interval(self: float) -> bool:
        """Check if given number of seconds has elapsed since last record"""
        if self.last_time is None:
            return True
        return (time.monotonic() - self.last_time) >= self.interval_sec

    def wait_until_elapsed_interval(self) -> None:
        """Block until given number of seconds has elapsed since last record"""
        if self.last_time is None:
            return

        elapsed = time.monotonic() - self.last_time
        remaining = self.interval_sec - elapsed

        if remaining > 0:
            time.sleep(remaining)
