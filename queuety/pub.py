import asyncio
import logging
import random
import queue

from typing import Any, Coroutine


logger = logging.getLogger(__name__)


def enqueue(q: queue.Queue, msg: Any) -> None:
    q.put(msg)
    logger.info("enqueued %s", msg)


async def handle_enqueued(q: queue.Queue, msg: Any) -> Coroutine[None, None, None]:
    logger.info("handling %s", msg)
    await asyncio.sleep(random.randint(0, 3))
    enqueue(q, msg)
