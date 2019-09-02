import asyncio
import logging

from . import pub, sub


logger = logging.getLogger(__name__)


def simulate(n: int = 10):
    q = asyncio.Queue()

    asyncio.run(pub.enqueue(q, n))
    asyncio.run(sub.dequeue(q))
