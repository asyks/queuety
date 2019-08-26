import asyncio
import logging
import queue
import random

from typing import Any, Coroutine, Generator


logger = logging.getLogger(__name__)


def dequeue(q: queue.Queue) -> Generator[Any, None, None]:
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
