import asyncio
import concurrent.futures
import functools
import logging

from signal import SIGINT
from typing import Dict, List
from worker import Worker

logging.basicConfig(level=logging.INFO)


class App:
    def __init__(self, threads_info: List[int]):
        self.threads_info = threads_info
        self.lock = asyncio.Lock()

        self.loop = asyncio.get_event_loop()
        self.loop.set_default_executor(
            concurrent.futures.ThreadPoolExecutor(max_workers=2)
        )

        self.workers: Dict[str, Worker] = {}

        self.loop.add_signal_handler(
            SIGINT, lambda: asyncio.create_task(self._shutdown())
        )

    def _create_workers(self):
        for idx, t in enumerate(self.threads_info):
            worker = Worker(t, idx, self.lock)
            self.workers[worker.digest] = worker

    def _sleep_worker(self, digest: str):
        sleep_time = self.workers[digest].sleep_time

        logging.info(
            f'Sleeping worker {self.workers[digest].worker_num} for '
            f'{sleep_time}.'
        )
        self.loop.call_later(
            sleep_time,
            self._run_worker,
            digest
        )

    def _schedule_worker_sleep(self, task: asyncio.Task):
        digest = None
        try:
            digest = task.result()
            if not digest in self.workers:
                raise KeyError

            self._sleep_worker(digest)
        except KeyError:
            logging.error(f'Could not find worker {digest}!')

    def _run_worker(self, digest: str):
        worker = self.workers[digest]

        task = self.loop.create_task(worker.run())
        task.add_done_callback(
            functools.partial(self._schedule_worker_sleep)
        )

    def run(self):
        self._create_workers()

        for d in self.workers.keys():
            self._sleep_worker(d)

        try:
            self.loop.run_forever()
        finally:
            self.loop.close()
            logging.info('Exiting...')

    async def _shutdown(self):
        collected_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for t in collected_tasks:
            t.cancel()

        self.loop.stop()
