from unittest import TestCase
import subprocess


class TestApp(TestCase):
    def setUp(self):
        pass

    def test_main(self):
        proc = subprocess.run(
            ["python", "py_hello/main.py"], capture_output=True
        )

        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, b"Hello World!\n")

