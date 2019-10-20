from typing import Optional, Tuple
import asyncio

import pytest

from . import constants
import queuety


@pytest.fixture
def create_mock_coro(mocker, monkeypatch):
    def _create_mock_patch_coro(
        to_patch: Optional[str] = None
    ) -> Tuple[mocker.Mock, asyncio.coroutine]:
        mock = mocker.Mock()

        async def _coro(*args, **kwargs):
            return mock(*args, **kwargs)

        if to_patch:
            monkeypatch.setattr(to_patch, _coro)

        return mock, _coro

    return _create_mock_patch_coro


@pytest.fixture
def mock_sleep(create_mock_coro):
    mock, _ = create_mock_coro(to_patch="asyncio.sleep")
    return mock


@pytest.fixture
def message():
    return queuety.model.Message(routes=[constants.TEST_ROUTE])


@pytest.fixture
def mock_queue(mocker, monkeypatch):
    queue = mocker.Mock()
    monkeypatch.setattr(asyncio, "Queue", queue)
    return queue.return_value


@pytest.fixture
def mock_get(mock_queue, create_mock_coro):
    mock_get, coro_get = create_mock_coro()
    mock_queue.get = coro_get
    return mock_get


@pytest.fixture
def mock_put(mock_queue, create_mock_coro):
    mock_put, coro_put = create_mock_coro()
    mock_queue.put = coro_put
    return mock_put
