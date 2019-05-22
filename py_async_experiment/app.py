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

        self.loop = asyncio.get_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        self.workers: Dict[str, Worker] = {}

        self.loop.add_signal_handler(
            SIGINT, lambda: asyncio.create_task(self._shutdown())
        )

    def _create_workers(self):
        for idx, t in enumerate(self.threads_info):
            worker = Worker(t, idx)
            self.workers[worker.digest] = worker

    def _worker_sleep_callback(self, task: asyncio.Task):
        digest = None
        try:
            digest = task.result()
            if not digest in self.workers:
                raise KeyError

            self._add_worker_to_pool(digest)
        except KeyError:
            logging.error(f'Could not find worker {digest}!')

    def _sleep_worker(self, digest: str, duration: int):
        logging.info(f'Worker {digest} sleeping for {duration}s.')

        task = self.loop.create_task(asyncio.sleep(duration, result=digest))
        task.add_done_callback(
            functools.partial(self._worker_sleep_callback)
        )

    def _add_worker_to_pool(self, digest: str):
        worker = self.workers[digest]

        try:
            future = self.executor.submit(worker.run)
        except RuntimeError as e:
            if 'shutdown' in e.args[0]:
                return
            else:
                logging.fatal(e.with_traceback)
                raise RuntimeError

        done, _ = concurrent.futures.wait(
            [future], return_when=concurrent.futures.FIRST_COMPLETED
        )

        digest = None
        try:
            digest = done.pop().result()
            if not digest in self.workers:
                raise KeyError

            self._sleep_worker(digest, self.workers[digest].sleep_time)
        except KeyError:
            logging.error(f'Could not find worker {digest}!')

    def run(self):
        self._create_workers()

        for d in self.workers.keys():
            self._sleep_worker(d, 1)

        try:
            self.loop.run_forever()
        finally:
            self.loop.stop()
            logging.info('Exiting...')

    async def _shutdown(self):
        collected_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for t in collected_tasks:
            t.cancel()

        self.executor.shutdown(wait=True)

        self.loop.stop()
