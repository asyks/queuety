import asyncio
import logging
import queue
import random

from typing import Any, Coroutine, Generator


logger = logging.getLogger(__name__)

q = queue.Queue(100)


def enqueue(n: int) -> None:
    for _i in range(n):
        msg = f"message {_i}"
        q.put(msg)
        logger.info("enqueued %s", msg)


def dequeue() -> Generator[Any, None, None]:
    while True:
        try:
            msg = q.get(block=False)
        except queue.Empty:
            break
        else:
            logger.info("dequeued %s", msg)

        yield msg


async def handle_dequeued(msg: Any) -> Coroutine[None, None, None]:
    logger.info(f"handling dequeued %s", msg)
    lag = random.randint(0, 3)
    await asyncio.sleep(lag)
    logger.info("finished handling %s", msg)


async def main(n: int = 10) -> None:
    logger.info("Start ...")

    enqueue(n)
    await asyncio.gather(*[handle_dequeued(dequeued) for dequeued in dequeue()])

    logger.info("... End.")
