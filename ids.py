import os
import threading
import time

from dotenv import load_dotenv

load_dotenv()

EPOCH_MS = 1704067200000
MACHINE_BITS = 10
SEQUENCE_BITS = 12
MAX_MACHINE_ID = (1 << MACHINE_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1


class SnowflakeGenerator:
    def __init__(self, machine_id: int):
        if not 0 <= machine_id <= MAX_MACHINE_ID:
            raise ValueError("machine_id out of range")
        self.machine_id = machine_id
        self.last_timestamp = -1
        self.sequence = 0
        self.lock = threading.Lock()

    def _now_ms(self) -> int:
        return int(time.time() * 1000)

    def next_id(self) -> int:
        with self.lock:
            timestamp = self._now_ms()
            if timestamp < self.last_timestamp:
                timestamp = self.last_timestamp

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & MAX_SEQUENCE
                if self.sequence == 0:
                    while timestamp <= self.last_timestamp:
                        timestamp = self._now_ms()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp
            return (
                ((timestamp - EPOCH_MS) << (MACHINE_BITS + SEQUENCE_BITS))
                | (self.machine_id << SEQUENCE_BITS)
                | self.sequence
            )


generator = SnowflakeGenerator(int(os.getenv("MACHINE_ID", "1")))