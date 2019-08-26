from unittest import mock, TestCase
import asyncio

from queuety import main
from tests.util import CoroutineMock


class TestSubscriber(TestCase):
    def setUp(self):
        pass

    @mock.patch("queuety.main.handle_dequeued", new_callable=CoroutineMock)
    def test_sub_default_msg_num(self, mock_handle_dequeued):
        asyncio.run(main.main())

        self.assertEqual(mock_handle_dequeued.call_count, 10)

    @mock.patch("queuety.main.handle_dequeued", new_callable=CoroutineMock)
    def test_sub_custom_msg_num(self, mock_handle_dequeued):
        num_messages = 8
        asyncio.run(main.main(num_messages))

        self.assertEqual(mock_handle_dequeued.call_count, num_messages)
