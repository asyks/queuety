from unittest import mock
import asyncio

import pytest

from . import constants
import queuety


@pytest.mark.asyncio
class TestSimulatedSubscriber:
    async def test_dequeue(self, mock_get, mock_queue, message, create_mock_coro):
        mock_get.side_effect = [message, Exception("break while loop")]
        mock_handle_message, _ = create_mock_coro(
            "queuety.sub.SimulatedSubscriber.handle_message"
        )

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)

        with pytest.raises(Exception, match="break while loop"):
            await subscriber.dequeue()

        ret_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        mock_handle_message.assert_not_called()  # <-- sanity check

        await asyncio.gather(*ret_tasks)

        assert 1 == len(ret_tasks)
        mock_handle_message.assert_called_once_with(mock.ANY, message)

    async def test_handle_route(self, mock_queue, message, mock_sleep):
        assert message.routes[constants.TEST_ROUTE] is False  # Sanity check

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)
        await subscriber.handle_route(constants.TEST_ROUTE, message)

        assert message.routes[constants.TEST_ROUTE] is True
        assert mock_sleep.call_count == 1
