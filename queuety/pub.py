import asyncio
import logging
import random

from typing import Coroutine


logger = logging.getLogger(__name__)


async def enqueue(q: asyncio.Queue, n: int) -> Coroutine[None, None, None]:
    for msg in (f"message {_i}" for _i in range(n)):
        logger.info("handling %s", msg)
        await asyncio.sleep(random.randint(0, 2))
        await q.put(msg)
        logger.info("enqueued %s", msg)

    await q.put(None)
