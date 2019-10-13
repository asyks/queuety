import asyncio
import logging
import random
import typing as t

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


async def handle_route(route: str, msg: Message) -> t.Coroutine:
    await asyncio.sleep(random.randint(0, 2))
    msg.routes[route] = True
    logger.info("Handled route %s for %s", route, msg.id)


async def handle_dequeued_msg(msg: Message) -> t.Coroutine:
    event = asyncio.Event()
    asyncio.create_task(extend_until_complete(msg, event))
    asyncio.create_task(ack_dequeued_msg(msg, event))

    results = await asyncio.gather(
        *(handle_route(route, msg) for route in msg.routes), return_exceptions=True
    )

    for result in results:
        if isinstance(result, Exception):
            logging.error(f"Handling general error: {result}")

    event.set()


async def dequeue(q: asyncio.Queue, sub_id: int) -> t.Coroutine:
    while True:
        msg: Message = await q.get()
        logger.info("sub %s dequeued %s", sub_id, msg.id)
        asyncio.create_task(handle_dequeued_msg(msg))
