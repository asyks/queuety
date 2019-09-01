import asyncio
import logging
import queue
import random

from typing import Coroutine


logger = logging.getLogger(__name__)


async def dequeue(q: queue.Queue) -> Coroutine[None, None, None]:
    async def _dequeue(q: queue.Queue) -> Coroutine[None, None, None]:
        msg = q.get(block=True)
        logger.info("dequeued %s", msg)
        await asyncio.sleep(1)
        logger.info("finished %s", msg)

    await asyncio.sleep(random.randint(0, 2))
    asyncio.create_task(_dequeue(q))
