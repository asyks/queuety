import asyncio
import logging
import random

from typing import Coroutine

from .pub import Message


logger = logging.getLogger(__name__)


async def dequeue(q: asyncio.Queue) -> Coroutine[None, None, None]:
    while True:
        msg: Message = await q.get()
        if msg is None:
            break

        logger.info("dequeued %s", msg.id)
        await asyncio.sleep(random.randint(0, 2))
        logger.info("finished %s", msg.id)
