import asyncio
import logging

from signal import SIGINT
from typing import List
from worker import Worker

logging.basicConfig(level=logging.INFO)


class App:
    def __init__(self, threads_info: List[int]):
        self.threads_info = threads_info
        self.loop = asyncio.get_event_loop()

    def _create_threads(self):
        for t in self.threads_info:
            worker = Worker(sleep_time=t)
            self.loop.create_task(worker.run())

    def run(self):
        self.loop.add_signal_handler(
            SIGINT, lambda: asyncio.create_task(self.shutdown())
        )

        try:
            self._create_threads()
            self.loop.run_forever()
        except KeyboardInterrupt:
            logging.info('Got keyboard interrupt. Cleaning up...')
        finally:
            logging.info('Stopping event loop...')
            self.loop.stop()
            logging.info('Exiting...')

    async def shutdown(self):
        collected_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        for t in collected_tasks:
            t.cancel()

        self.loop.stop()
