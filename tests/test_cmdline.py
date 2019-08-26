from unittest import TestCase
import subprocess


class TestCmdlineEntrypoint(TestCase):
    def test_cmd(self):
        proc = subprocess.run(["python", "-m", "queuety"], capture_output=True)

        self.assertEqual(proc.returncode, 0)
