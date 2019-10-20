from unittest import TestCase, mock
import asyncio
import typing as t

import pytest

import queuety


TEST_ROUTE = "task1"


@pytest.fixture
def create_mock_coro(mocker, monkeypatch):
    def _create_mock_patch_coro(
        to_patch: t.Optional[str] = None
    ) -> t.Tuple[mocker.Mock, asyncio.coroutine]:
        mock = mocker.Mock()

        async def _coro(*args, **kwargs):
            return mock(*args, **kwargs)

        if to_patch:
            monkeypatch.setattr(to_patch, _coro)

        return mock, _coro

    return _create_mock_patch_coro


@pytest.fixture
def mock_sleep(create_mock_coro):
    mock, _ = create_mock_coro(to_patch="queuety.sub.asyncio.sleep")
    return mock


@pytest.fixture
def message():
    return queuety.model.Message(routes=[TEST_ROUTE])


@pytest.fixture
def mock_queue(mocker, monkeypatch):
    queue = mocker.Mock()
    monkeypatch.setattr(queuety.sub.asyncio, "Queue", queue)
    return queue.return_value


@pytest.fixture
def mock_get(mock_queue, create_mock_coro):
    mock_get, coro_get = create_mock_coro()
    mock_queue.get = coro_get
    return mock_get


@pytest.mark.asyncio
async def test_dequeue(mock_get, mock_queue, message, create_mock_coro):
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


@pytest.mark.asyncio
async def test_handle_route(mock_queue, message, mock_sleep):
    assert message.routes[TEST_ROUTE] is False  # Sanity check

    subscriber = queuety.sub.SimulatedSubscriber(queue=mock_queue)
    await subscriber.handle_route(TEST_ROUTE, message)

    assert message.routes[TEST_ROUTE] is True
    assert mock_sleep.call_count == 1
