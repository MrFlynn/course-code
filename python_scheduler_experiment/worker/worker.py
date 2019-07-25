import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO)


class Worker:
    def __init__(self, sleep_time: int, worker_num: int, lock: asyncio.Lock):
        self.sleep_time = sleep_time
        self.worker_num = worker_num
        self.lock = lock

    async def run(self) -> str:
        async with self.lock:
            logging.info(f'Worker {self.worker_num} running.')
            time.sleep(self.sleep_time)
            logging.info(f'Worker {self.worker_num} exiting.')

        return self.digest

    @property
    def digest(self) -> str:
        h = hashlib.sha256()
        h.update(str(self.sleep_time).encode('utf-8'))
        h.update(str(self.worker_num).encode('utf-8'))

        return h.hexdigest()
