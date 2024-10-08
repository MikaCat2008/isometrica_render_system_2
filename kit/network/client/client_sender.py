import time, json, socket
from typing import Optional
from threading import Lock

from ..base import Method, Runnable
from ..answer import Answer


class ClientSender(Runnable):
    lock: Lock
    sock: Optional[socket.socket]
    answers: dict[int, Answer]
    sending_list: list[tuple[Method, int]]
    next_answer_id: int
    
    def __init__(self) -> None:
        self.lock = Lock()
        self.sock = None
        self.answers = {}
        self.sending_list = []
        self.next_answer_id = 0

    def connect(self, host: str, port: int) -> None:
        self.answers = {}
        self.sending_list = []
        self.next_answer_id = 0
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, method: Method) -> Answer:
        with self.lock:
            answer_id = self.next_answer_id
            answer = Answer(answer_id, method.return_type)
                    
            self.next_answer_id += 1
            self.answers[answer_id] = answer
            self.sending_list.append((method, answer_id))

        return answer

    def _run(self) -> None:
        while True:
            time.sleep(0.01)

            with self.lock:
                if not self.sending_list:
                    continue

                data = b"".join(
                    json.dumps({
                        "id": answer_id,
                        "type": type(method).__name__,
                        "data": method.model_dump()
                    }).encode() + b"\n"
                    for method, answer_id in self.sending_list
                )
                self.sending_list.clear()

                try:
                    self.sock.sendall(data)
                except ConnectionError:
                    self.sock = None

                    return
