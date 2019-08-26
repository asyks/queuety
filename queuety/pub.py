import logging


logger = logging.getLogger(__name__)


def enqueue(q, n: int) -> None:
    for _i in range(n):
        msg = f"message {_i}"
        q.put(msg)
        logger.info("enqueued %s", msg)