import asyncio
import logging
import signal
import typing as t

from . import pub, sub


logger = logging.getLogger(__name__)


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


def simulate(n: int = 10):
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    for shutdown_signal in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            shutdown_signal, lambda sig=shutdown_signal: asyncio.create_task(
                shutdown(sig, loop)
            )
        )

    q = asyncio.Queue()

    # Instantiate multiple publish coroutines
    pub_coros = [pub.enqueue(q, pub_id) for pub_id in range(0, 2)]
    # Instantiate multiple subscription coroutines
    sub_coros = [sub.dequeue(q, sub_id) for sub_id in range(0, 2)]

    try:
        # Create a task for each publish coroutine
        [loop.create_task(coro) for coro in pub_coros]
        # Create a task for each subscription coroutine
        [loop.create_task(coro) for coro in sub_coros]

        loop.run_forever()
    finally:
        loop.close()
        logger.info("Process shutdown")
