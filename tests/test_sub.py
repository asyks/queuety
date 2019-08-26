from unittest import mock, TestCase
import asyncio

from tests.util import CoroutineMock
import queuety


@mock.patch("queuety.sub.handle_dequeued", new_callable=CoroutineMock)
class TestSubscriber(TestCase):
    def setUp(self):
        pass

    def test_sub_default_msg_num(self, mock_handle_dequeued):
        asyncio.run(queuety.main())

        self.assertEqual(mock_handle_dequeued.call_count, 10)

    def test_sub_custom_msg_num(self, mock_handle_dequeued):
        num_messages = 8
        asyncio.run(queuety.main(num_messages))

        self.assertEqual(mock_handle_dequeued.call_count, num_messages)
