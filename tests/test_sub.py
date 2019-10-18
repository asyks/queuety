from unittest import TestCase
import asyncio

import queuety


class TestSubscriber(TestCase):
    def setUp(self):
        pass

    def test_handled_dequeued_msg(self):
        TEST_ROUTE = "task1"

        msg = queuety.model.Message(routes=[TEST_ROUTE])
        asyncio.run(
            queuety.sub.handle_dequeued_msg(queuety.sub.simulate_handle_route, msg)
        )

        self.assertTrue(msg.routes[TEST_ROUTE])

    def test_handle_route(self):
        TEST_ROUTE = "task1"

        msg = queuety.model.Message(routes=[TEST_ROUTE])
        asyncio.run(queuety.sub.simulate_handle_route(TEST_ROUTE, msg))

        self.assertTrue(msg.routes[TEST_ROUTE])
