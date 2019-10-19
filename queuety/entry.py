import asyncio
import logging
import signal
import typing as t

from . import pub, sub


logger = logging.getLogger(__name__)


async def shutdown(
    loop: asyncio.AbstractEventLoop, sig: t.Optional[signal.Signals] = None
) -> t.Coroutine:
    if isinstance(sig, signal.Signals):
        logging.info("Received exit signal %s...", sig.name)

    logging.info("Nacking outstanding messages")

    tasks_to_cancel: t.List[asyncio.Task] = []
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            tasks_to_cancel.append(task)

    for task in tasks_to_cancel:
        task.cancel()

    logging.info("Cancelling %i oustanding tasks" % len(tasks_to_cancel))

    await asyncio.gather(*tasks_to_cancel, return_exceptions=True)

    logging.info("Stopping event loop")

    loop.stop()


def handle_exception(
    loop: asyncio.AbstractEventLoop, context
) -> None:
    msg = context.get(
        "exception", context["message"]  # "exception" may not be set, "message" should
    )
    logging.error(f"Caught exception: {msg}")

    logging.info("Shutting down...")
    asyncio.create_task(shutdown(loop))


def main(publisher: pub.BasePublisher, subscriber: sub.BaseSubsriber) -> None:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    for shutdown_signal in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            shutdown_signal, lambda sig=shutdown_signal: asyncio.create_task(
                shutdown(loop, sig=sig)
            )
        )
    loop.set_exception_handler(handle_exception)

    q = asyncio.Queue()
    # Instantiate publish coroutines
    pub_coros = []
    for _ in range(0, 1):
        pub = publisher(queue=q)
        pub_coros.append(pub.enqueue())
    # Instantiate subscription coroutines
    sub_coros = []
    for _ in range(0, 1):
        sub = subscriber(queue=q)
        sub_coros.append(sub.dequeue())

    try:
        # Create a task for each publish coroutine
        [loop.create_task(coro) for coro in pub_coros]
        # Create a task for each subscription coroutine
        [loop.create_task(coro) for coro in sub_coros]

        loop.run_forever()
    finally:
        loop.close()
        logger.info("Process shutdown")


def run_simulation() -> None:
    main(pub.SimulatedPublisher, sub.SimulatedSubscriber)


def run() -> None:
    main(pub.SimulatedPublisher, sub.SimulatedSubscriber)  # TODO: add real pub/sub
