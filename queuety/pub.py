import asyncio
import logging
import random
import uuid

from typing import Coroutine


logger = logging.getLogger(__name__)


class Message:
    def __init__(self):
        super().__init__()
        self.id: uuid.UUID = uuid.uuid4()
        self.body: str = f"message {self.id}"
        self.handled: bool = False


async def enqueue(q: asyncio.Queue, pub_id: int) -> Coroutine[None, None, None]:
    while True:
        msg: Message = Message()
        logger.info("%s handling %s", pub_id, msg.id)
        asyncio.create_task(q.put(msg))
        logger.info("%s enqueued %s", pub_id, msg.id)
        await asyncio.sleep(random.randint(0, 2))

    await q.put(None)
