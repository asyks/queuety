from unittest.mock import Mock
import asyncio


def CoroutineMock():
    coroutine = Mock(name="CoroutineResult")
    coroutine_func = Mock(
        name="CoroutineFunction", side_effect=asyncio.coroutine(coroutine)
    )
    coroutine_func.coro = coroutine

    return coroutine_func
