import asyncio
import logging
import random
import typing as t
import uuid


logger = logging.getLogger(__name__)


class Message:
    def __init__(self, routes: t.Iterable[str]):
        super().__init__()
        self.id: uuid.UUID = uuid.uuid4()
        self.body: str = f"message {self.id}"
        self.acked: bool = False
        self.extend_count: int = 0
        self.routes: t.Dict[str, bool] = {route: False for route in routes}


async def enqueue(q: asyncio.Queue, pub_id: int) -> t.Coroutine:
    routes = ["task_1", "task_2", "task_3"]

    while True:
        msg: Message = Message(routes)
        logger.info("pub %s handling %s", pub_id, msg.id)
        asyncio.create_task(q.put(msg))
        logger.info("pub %s enqueued %s", pub_id, msg.id)
        await asyncio.sleep(random.randint(0, 2))
