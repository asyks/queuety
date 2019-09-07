import asyncio
import logging
import random

from typing import Coroutine

from .pub import Message


logger = logging.getLogger(__name__)


async def dequeue(q: asyncio.Queue) -> Coroutine:
    while True:
        msg: Message = await q.get()
        if msg is None:
            break

        logger.info("dequeued %s", msg.id)
        asyncio.create_task(handle_dequeued_msg(msg))


async def handle_dequeued_msg(msg: Message) -> Coroutine:
    await asyncio.gather(
        *(handle_task(task, msg) for task in msg.tasks)
    )
    await ack_dequeued_msg(msg)


async def handle_task(task, msg) -> Coroutine:
    await asyncio.sleep(random.randint(0, 2))
    msg.tasks[task] = True
    logger.info("Handled task %s for %s", task, msg.id)


async def ack_dequeued_msg(msg: Message) -> Coroutine:
    await asyncio.sleep(random.randint(0, 1))
    msg.acked = True
    logger.info("Acknowledged %s", msg.id)
