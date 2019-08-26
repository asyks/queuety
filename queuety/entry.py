import asyncio
import queue

from . import pub, sub


q = queue.Queue(100)


async def main(n: int = 10) -> None:
    pub.enqueue(q, n)
    await asyncio.gather(
        *[sub.handle_dequeued(dequeued) for dequeued in sub.dequeue(q)]
    )
