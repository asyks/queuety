import asyncio
import logging
import signal
import typing as t

from . import pub, sub


logger = logging.getLogger(__name__)


shutdown_signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)


async def shutdown(signal, loop) -> t.Coroutine:
    logging.info("Received exit signal %s...", signal.name)
    logging.info("Nacking outstanding messages")

    tasks_to_cancel: t.List[asyncio.Task] = []
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()
            tasks_to_cancel.append(task)

    logging.info("Cancelling %i oustanding tasks" % len(tasks_to_cancel))
    await asyncio.gather(*tasks_to_cancel, return_exceptions=True)
    logging.info("Stopping event loop")
    loop.stop()


def handle_signal(sig: signal.signal, loop: asyncio.AbstractEventLoop) -> None:
    asyncio.create_task(shutdown(sig, loop))


def simulate(n: int = 10):
    loop = asyncio.get_event_loop()

    for sig in shutdown_signals:
        loop.add_signal_handler(
            sig, lambda sig=sig: asyncio.create_task(shutdown(sig, loop))
        )

    q = asyncio.Queue()

    pub_coros = [pub.enqueue(q, pub_id) for pub_id in range(0, 2)]

    try:
        [loop.create_task(coro) for coro in pub_coros]
        loop.create_task(sub.dequeue(q))
        loop.run_forever()
    finally:
        loop.close()
        logger.info("Process shutdown")
