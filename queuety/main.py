#!/usr/bin/env python

from queue import Queue
import asyncio


q = Queue(100)


async def enqueue(n: int):
    for _i in range(n):
        msg = f"message {_i}"
        q.put(msg)
        await asyncio.sleep(1)
        print(f"enqueued {msg}")


def dequeue(n: int):
    for _i in range(n):
        msg = q.get()
        await asyncio.sleep(2)
        print(f"dequeued {msg}")


async def main():
    msg_num = 10
    print("Start ...")
    await asyncio.gather(enqueue(msg_num), dequeue(msg_num))
    print("... End.")


if __name__ == "__main__":
    asyncio.run(main())
