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
        if msg.acked is False:
            asyncio.create_task(handle_dequeued_msg(msg))


async def handle_dequeued_msg(msg: Message) -> Coroutine[None, None, None]:
    await asyncio.sleep(random.randint(0, 2))
    msg.acked = True
    logger.info("finished %s", msg.id)
