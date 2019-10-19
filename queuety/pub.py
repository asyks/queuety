import asyncio
import logging
import random
import typing as t
import uuid

from .model import Message
from . import constants


logger = logging.getLogger(__name__)


class BasePublisher:

    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue
        self.publisher_id = uuid.uuid4()

        super().__init__()

    def get_message_from_ingress(self) -> Message:
        raise NotImplementedError

    async def enqueue(self) -> t.Coroutine:
        while True:
            msg = self.get_message_from_ingress()
            logger.info("Publisher %s handling %s", self.publisher_id, msg.id)

            asyncio.create_task(self.queue.put(msg))
            logger.info("Publisher %s enqueued %s", self.publisher_id, msg.id)

            await asyncio.sleep(random.randint(0, 2))


class SimulatedPublisher(BasePublisher):

    def get_message_from_ingress(self) -> Message:
        return Message(constants.MESSAGE_ROUTES)
