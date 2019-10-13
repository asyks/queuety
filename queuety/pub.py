import asyncio
import logging
import random
import typing as t

from .model import Message
from . import constants


logger = logging.getLogger(__name__)


async def enqueue(q: asyncio.Queue, pub_id: int) -> t.Coroutine:
    while True:
        msg: Message = Message(constants.MESSAGE_ROUTES)
        logger.info("pub %s handling %s", pub_id, msg.id)
        asyncio.create_task(q.put(msg))
        logger.info("pub %s enqueued %s", pub_id, msg.id)
        await asyncio.sleep(random.randint(0, 2))
