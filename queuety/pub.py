import asyncio
import logging
import queue
import random

from typing import Any, Coroutine


logger = logging.getLogger(__name__)


async def enqueue(q: queue.Queue, msg: Any) -> Coroutine[None, None, None]:
    async def _enqueue(q: queue.Queue, msg: Any) -> Coroutine[None, None, None]:
        logger.info("handling %s", msg)
        await asyncio.sleep(1)
        q.put(msg)
        logger.info("enqueued %s", msg)

    asyncio.create_task(_enqueue(q, msg))
    await asyncio.sleep(random.randint(0, 2))
