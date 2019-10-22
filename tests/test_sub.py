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

        mock_handle_message.assert_not_called()  # Sanity check

        await asyncio.gather(*ret_tasks)

        assert 1 == len(ret_tasks)
        mock_handle_message.assert_called_once_with(subscriber, message)

    async def test_handle_message(self, mock_queue, message, mock_sleep, create_mock_coro):
        mock_handle_route, _ = create_mock_coro(
            "queuety.sub.SimulatedSubscriber.handle_route"
        )
        mock_handle_route.return_value = []

        mock_sub_extend, _ = create_mock_coro(
            "queuety.sub.SimulatedSubscriber.extend"
        )
        mock_sub_acknowledge, _ = create_mock_coro(
            "queuety.sub.SimulatedSubscriber.acknowledge"
        )

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)

        await subscriber.handle_message(message)

        mock_handle_route.assert_called_once_with(
            subscriber, constants.TEST_ROUTE, message
        )

    async def test_handle_route(self, mock_queue, message, mock_sleep):
        assert message.routes[constants.TEST_ROUTE] is False  # Sanity check

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)
        await subscriber.handle_route(constants.TEST_ROUTE, message)

        assert message.routes[constants.TEST_ROUTE] is True
        assert mock_sleep.call_count == 1

    async def test_extend(self, mocker, mock_queue, message, mock_sleep):
        event = asyncio.Event()
        mock_event_is_set = mocker.patch.object(asyncio.Event, "is_set")
        mock_event_is_set.side_effect = [False, True]

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)
        await subscriber.extend(message, event)

        assert message.extend_count == 1
        assert mock_sleep.call_count == 1

    async def test_acknowledge(self, mocker, mock_queue, message, mock_sleep):
        event = asyncio.Event()
        event.set()

        subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)
        await subscriber.acknowledge(message, event)

        assert message.acked is True
        assert mock_sleep.call_count == 1
