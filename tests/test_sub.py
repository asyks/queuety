from unittest import TestCase, mock
import asyncio

import pytest

import queuety


TEST_ROUTE = "task1"


@pytest.fixture
def message():
    return queuety.model.Message(routes=[TEST_ROUTE])


@pytest.mark.asyncio
async def test_handle_dequeued_msg(message):
    subscriber = queuety.sub.SimulatedSubscriber(mock.Mock())
    await subscriber.handle_message(message)

    assert message.routes[TEST_ROUTE] is True


@pytest.mark.asyncio
async def test_handle_route(message):
    subscriber = queuety.sub.SimulatedSubscriber(mock.Mock())
    await subscriber.handle_route(TEST_ROUTE, message)

    assert message.routes[TEST_ROUTE] is True
