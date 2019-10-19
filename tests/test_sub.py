from unittest import TestCase
import asyncio

import pytest

import queuety


class TestSubscriber(TestCase):
    @pytest.mark.asyncio
    def test_handle_dequeued_msg(self):
        TEST_ROUTE = "task1"

        queue: asyncio.Queue = asyncio.Queue()
        msg = queuety.model.Message(routes=[TEST_ROUTE])
        subscriber = queuety.sub.SimulatedSubscriber(queue)
        asyncio.run(subscriber.handle_message(msg))

        assert msg.routes[TEST_ROUTE] is True

    @pytest.mark.asyncio
    def test_handle_route(self):
        TEST_ROUTE = "task1"

        queue: asyncio.Queue = asyncio.Queue()
        msg = queuety.model.Message(routes=[TEST_ROUTE])
        subscriber = queuety.sub.SimulatedSubscriber(queue)
        asyncio.run(subscriber.handle_route(TEST_ROUTE, msg))

        assert msg.routes[TEST_ROUTE] is True
