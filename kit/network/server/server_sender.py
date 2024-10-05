from __future__ import annotations

import time, json, socket
from typing import Optional, TYPE_CHECKING
from threading import Lock

from ..base import Sender, Method, Update

if TYPE_CHECKING:
    from .server_dispatcher import ServerDispatcher


class ServerSender(Sender):
    sock: Optional[socket.socket]
    dispatcher: Optional[ServerDispatcher]

    locks: dict[int, Lock]
    connections: dict[int, socket.socket]
    sending_lists: dict[int, list[Update]]

    def __init__(self) -> None:
        self.sock = None
        self.dispatcher = None

        self.locks = {}
        self.connections = {}
        self.sending_lists = {}

    def start(self, host: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

    def send(self, connection: socket.socket, method: Method) -> None:
        sock_id = id(connection)
        lock = self.locks[sock_id]
        
        with lock:
            self.sending_lists[sock_id].append(method)

    def add_connection(self, connection: socket) -> None:
        sock_id = id(connection)

        self.locks[sock_id] = Lock()
        self.connections[sock_id] = connection
        self.sending_lists[sock_id] = []

    def remove_connection(self, connection: socket) -> None:
        sock_id = id(connection)

        del self.locks[sock_id]
        del self.connections[sock_id]
        del self.sending_lists[sock_id]

    def _run(self) -> None:
        while True:
            time.sleep(0.01)
            
            for sock_id, connection in self.connections.items():
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
                    sending_list.clear()

                    try:
                        connection.sendall(data)
                    except ConnectionError:
                        if self.dispatcher and self.dispatcher.on_disconnection_handler:
                            self.dispatcher.on_disconnection_handler(connection)

                        self.sender.remove_connection(connection)

                        return
