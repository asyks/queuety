from unittest import TestCase
import asyncio

import queuety


class TestSubscriber(TestCase):
    def setUp(self):
        pass

    def test_pub_sub(self):
        q = asyncio.Queue()
        num_messages = 5
        asyncio.run(queuety.pub.enqueue(q, num_messages))
        asyncio.run(queuety.sub.dequeue(q))
