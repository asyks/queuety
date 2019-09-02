import asyncio
import logging

from . import pub, sub


logger = logging.getLogger(__name__)


def simulate(n: int = 10):
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()

    pub_coros = [pub.enqueue(q, pub_id) for pub_id in range(0, 4)]

    try:
        [loop.create_task(coro) for coro in pub_coros]
        loop.create_task(sub.dequeue(q))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("process interrupted")
    finally:
        loop.close()
        logger.info("process shutdown")
