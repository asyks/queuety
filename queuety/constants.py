import os
import typing as t


MESSAGE_EXTEND_DELAY: int = os.environ.get("MESSAGE_EXTEND_DELAY", 2)
MESSAGE_ROUTES: t.List[str] = os.environ.get(
    "MESSAGE_ROUTES", ["task_1", "task_2", "task_3"]
)
