import asyncio
import logging
import queue

from . import pub, sub


logger = logging.getLogger(__name__)


q = queue.Queue(100)


async def main(n: int = 10) -> None:
    await asyncio.gather(*[pub.handle_enqueued(q, f"message {_i}") for _i in range(n)])

    await asyncio.gather(
        *[sub.handle_dequeued(dequeued) for dequeued in sub.dequeue(q)]
    )
