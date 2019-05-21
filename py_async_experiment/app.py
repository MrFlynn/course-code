import asyncio
import functools
import logging

from signal import SIGINT
from typing import Dict, List
from worker import Worker

logging.basicConfig(level=logging.INFO)


class App:
    def __init__(self, threads_info: List[int]):
        self.threads_info = threads_info
        self.loop = asyncio.get_event_loop()

        self.workers: Dict[str, Worker] = {}

        self.loop.add_signal_handler(
            SIGINT, lambda: asyncio.create_task(self.shutdown())
        )

    def _create_workers(self):
        for idx, t in enumerate(self.threads_info):
            worker = Worker(t, idx)
            self.workers[worker.digest] = worker

    def _worker_sleep_callback(self, task: asyncio.Task):
        try:
            self.workers[task.result()].run()
        except KeyError:
            logging.error(f'Could not find worker {task.result}!')

    def _add_worker_sleep(self, digest: str, duration: int):
        task = self.loop.create_task(asyncio.sleep(duration, result=digest))
        task.add_done_callback(
            functools.partial(self._worker_sleep_callback)
        )

    def run(self):
        self._create_workers()

        for d, w in self.workers.items():
            self._add_worker_sleep(d, w.sleep_time)

        try:
            self.loop.run_forever()
        finally:
            self.loop.stop()
            logging.info('Exiting...')

    async def shutdown(self):
        collected_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for t in collected_tasks:
            t.cancel()

        self.loop.stop()
