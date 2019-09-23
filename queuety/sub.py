import asyncio
import logging
import random
import typing as t

from .pub import Message


logger = logging.getLogger(__name__)


async def dequeue(q: asyncio.Queue, sub_id: int) -> t.Coroutine:
    while True:
        msg: Message = await q.get()
        logger.info("sub %s dequeued %s", sub_id, msg.id)
        asyncio.create_task(handle_dequeued_msg(msg))


async def handle_dequeued_msg(msg: Message) -> t.Coroutine:
    event = asyncio.Event()
    asyncio.create_task(extend_until_complete(msg, event))
    await asyncio.gather(
        *(handle_task(task, msg) for task in msg.routes)
    )
    event.set()


async def extend_until_complete(msg: Message, event: asyncio.Event) -> t.Coroutine:
    while not event.is_set():
        msg.extend_count += 1
        logging.info("Extended deadline for %s", msg.id)
        await asyncio.sleep(random.randint(0, 1))
    else:
        await ack_dequeued_msg(msg)


async def handle_task(task, msg) -> t.Coroutine:
    await asyncio.sleep(random.randint(0, 2))
    msg.routes[task] = True
    logger.info("Handled task %s for %s", task, msg.id)


async def ack_dequeued_msg(msg: Message) -> t.Coroutine:
    await asyncio.sleep(random.randint(0, 1))
    msg.acked = True
    logger.info("Acknowledged %s", msg.id)
