import asyncio
import logging


logging.basicConfig(level=logging.INFO)


class Worker:
    def __init__(self, sleep_time: int):
        self.sleep_time = sleep_time

    async def run(self):
        while True:
            logging.info(f'Thread running. Sleeping now for {self.sleep_time}')
            await asyncio.sleep(self.sleep_time)
