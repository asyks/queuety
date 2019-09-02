from unittest import mock, TestCase
import asyncio

from tests.util import CoroutineMock

import queuety


@mock.patch("asyncio.Queue", new_callable=CoroutineMock)
class TestPublisher(TestCase):
    def setUp(self):
        pass
