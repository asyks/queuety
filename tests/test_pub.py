import asyncio

import pytest

import queuety


@pytest.mark.asyncio
class TestSimulatedPublisher:
    async def test_enqueue(
        self, mocker, mock_put, mock_queue, mock_sleep, message
    ):
        mock_sleep.side_effect = Exception("break while loop")
        mock_get_message = mocker.patch.object(
            queuety.pub.SimulatedPublisher, "get_message_from_ingress"
        )
        mock_get_message.return_value = message

        publisher = queuety.pub.SimulatedPublisher(queue=mock_queue)

        with pytest.raises(Exception, match="break while loop"):
            await publisher.enqueue()

        ret_tasks = [
            t for t in asyncio.all_tasks() if t is not asyncio.current_task()
        ]

        await asyncio.gather(*ret_tasks)

        assert 1 == len(ret_tasks)
        mock_put.assert_called_once_with(message)
        assert mock_sleep.call_count == 1
