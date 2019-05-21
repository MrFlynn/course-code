import asyncio
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO)


class Worker:
    def __init__(self, sleep_time: int, worker_num: int):
        self.sleep_time = sleep_time
        self.worker_num = worker_num

    def run(self):
        logging.info(f'Worker {self.worker_num} running.')
        time.sleep(self.sleep_time)
        logging.info(f'Worker {self.worker_num} exiting.')

    @property
    def digest(self) -> str:
        h = hashlib.sha256()
        h.update(str(self.sleep_time).encode('utf-8'))
        h.update(str(self.worker_num).encode('utf-8'))

        return h.hexdigest()
