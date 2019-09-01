import asyncio
import logging
import queue

from typing import Coroutine

from . import pub, sub


logger = logging.getLogger(__name__)


q = queue.Queue(100)


async def simulate_ingress(n: int = 10) -> Coroutine[None, None, None]:
    for msg in (f"message {_i}" for _i in range(n)):
        await pub.enqueue(q, msg)


async def simulate_egress() -> Coroutine[None, None, None]:
    while True:
        try:
            await sub.dequeue(q)
        except (queue.Empty, StopAsyncIteration):
            break


async def simulate_simultaneous(n: int = 10) -> Coroutine[None, None, None]:
    await asyncio.gather(simulate_ingress(n), simulate_egress())
