import asyncio
import logging
import random
import typing as t
import uuid

from .model import Message
from . import constants


logger = logging.getLogger(__name__)


async def extend_until_complete(msg: Message, event: asyncio.Event) -> t.Coroutine:
    while not event.is_set():
        msg.extend_count += 1
        logging.info("Extended deadline for %s", msg.id)
        await asyncio.sleep(constants.MESSAGE_EXTEND_DELAY)


async def ack_dequeued_msg(msg: Message, event: asyncio.Event) -> t.Coroutine:
    await event.wait()
    await asyncio.sleep(random.randint(0, 1))
    msg.acked = True
    logger.info("Acknowledged %s", msg.id)


class BaseSubsriber:

    def __init__(self, queue: asyncio.Queue) -> None:
        self.queue = queue
        self.subscriber_id = uuid.uuid4()

        super().__init__()

    async def handle_route(self, route: str, msg: Message) -> t.Coroutine:
        raise NotImplementedError

    async def handle_message(self, msg: Message) -> t.Coroutine:
        event = asyncio.Event()
        asyncio.create_task(extend_until_complete(msg, event))
        asyncio.create_task(ack_dequeued_msg(msg, event))

        results = await asyncio.gather(
            *(
                self.handle_route(route, msg) for route in msg.routes
            ), return_exceptions=True
        )

        for result in results:
            if isinstance(result, Exception):
                logging.error("Handling error %s", result)

        event.set()

    async def dequeue(self):
        while True:
            msg: Message = await self.queue.get()
            logger.info("Subscriber %s dequeued %s", self.subscriber_id, msg.id)
            asyncio.create_task(self.handle_message(msg))


class SimulatedSubscriber(BaseSubsriber):

    async def handle_route(self, route: str, msg: Message) -> t.Coroutine:
        """Simulate route handling for a message.

        Suspend the route for a random, realistic, but short amount of time.
        """
        await asyncio.sleep(random.random())
        msg.routes[route] = True
        logger.info("Handled route %s for %s", route, msg.id)
