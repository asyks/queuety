import asyncio
import logging
import random
import typing as t
import uuid

from .model import Message
from . import constants


logger = logging.getLogger(__name__)


class BaseSubsriber:

    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue
        self.subscriber_id = uuid.uuid4()

        super().__init__()

    async def extend(self, msg: Message, event: asyncio.Event) -> t.Coroutine:
        while not event.is_set():
            msg.extend_count += 1
            logging.info("Extended deadline for %s", msg.id)
            await asyncio.sleep(constants.MESSAGE_EXTEND_DELAY)

    async def acknowledge(self, msg: Message, event: asyncio.Event) -> t.Coroutine:
        raise NotImplementedError

    async def handle_route(self, route: str, msg: Message) -> t.Coroutine:
        raise NotImplementedError

    async def handle_message(self, msg: Message) -> t.Coroutine:
        event = asyncio.Event()
        asyncio.create_task(self.extend(msg, event))
        asyncio.create_task(self.acknowledge(msg, event))

        results = await asyncio.gather(
            *(
                self.handle_route(route, msg) for route in msg.routes
            ), return_exceptions=True
        )

        for result in results:
            if isinstance(result, Exception):
                logging.error("Handling error %s", result)

        event.set()

    async def dequeue(self) -> t.Coroutine:
        while True:
            msg: Message = await self.queue.get()
            logger.info("Subscriber %s dequeued %s", self.subscriber_id, msg.id)
            asyncio.create_task(self.handle_message(msg))


class SimulatedSubscriber(BaseSubsriber):
    """Extend BaseSubscriber: Implement coroutines which simulate IO intensive calls.

    Suspend each coroutine for a random, and realistic, but short amount of time.
    """
    async def handle_route(self, route: str, msg: Message) -> t.Coroutine:
        """Simulate route handling for a message."""
        await asyncio.sleep(random.random())
        msg.routes[route] = True
        logger.info("Handled route %s for %s", route, msg.id)

    async def acknowledge(self, msg: Message, event: asyncio.Event) -> t.Coroutine:
        """Simulate messsage acknowledgement."""
        await event.wait()
        await asyncio.sleep(random.random())
        msg.acked = True
        logger.info("Acknowledged %s", msg.id)
