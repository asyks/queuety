import os
import signal
import time
import threading

import pytest

import queuety


@pytest.mark.parametrize("tested_signal", ("SIGINT", "SIGTERM", "SIGHUP"))
def test_entry_main(
    tested_signal, create_mock_coro, event_loop, mock_queue, mock_gather
):
    tested_signal = getattr(signal, tested_signal)
    mock_enqueue, _ = create_mock_coro("queuety.pub.SimulatedPublisher.enqueue")
    mock_dequeue, _ = create_mock_coro("queuety.sub.SimulatedSubscriber.dequeue")

    def _send_signal():
        time.sleep(0.1)  # Allow time for the loop to start
        os.kill(os.getpid(), tested_signal)

    thread = threading.Thread(target=_send_signal, daemon=True)
    thread.start()

    queuety.entry.main(queuety.pub.SimulatedPublisher, queuety.sub.SimulatedSubscriber)

    assert tested_signal in event_loop._signal_handlers
    assert queuety.entry.handle_exception == event_loop.get_exception_handler()

    mock_gather.assert_called_once_with(return_exceptions=True)
    mock_enqueue.assert_called_once()
    mock_dequeue.assert_called_once()

    assert not event_loop.is_running()
    assert not event_loop.is_closed()
    event_loop.close.assert_called_once_with()
