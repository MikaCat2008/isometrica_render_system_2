import time, json, socket
from threading import Lock

from ..base import Sender, Method, Update


class ServerSender(Sender):
    sock: socket.socket
    locks: dict[int, Lock]
    connections: list[socket.socket]
    sending_lists: dict[int, list[Update]]

    def __init__(self, host: str = "localhost", port: int = 7777) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        self.locks = {}
        self.connections = []
        self.sending_lists = {}

    def send(self, connection: socket.socket, method: Method) -> None:
        sock_id = id(connection)
        lock = self.locks[sock_id]
        
        with lock:
            self.sending_lists[sock_id].append(method)

    def _run(self) -> None:
        while True:
            time.sleep(0.01)
            
            for connection in self.connections:
                sock_id = id(connection)

                lock = self.locks[sock_id]
                sending_list = self.sending_lists[sock_id]
                
                with lock:
                    if not sending_list:
                        continue

                    data = b"".join(
                        json.dumps({
                            "type": type(update).__name__,
                            "data": update.model_dump()
                        }).encode() + b"\n"
                        for update in sending_list
                    )

                    connection.sendall(data)
                    sending_list.clear()
