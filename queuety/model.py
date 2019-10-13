import typing as t
import uuid


class Message:
    def __init__(self, routes: t.Iterable[str]):
        super().__init__()
        self.id: uuid.UUID = uuid.uuid4()
        self.body: str = f"message {self.id}"
        self.acked: bool = False
        self.extend_count: int = 0
        self.routes: t.Dict[str, bool] = {route: False for route in routes}
