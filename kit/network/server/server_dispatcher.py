import json
from socket import socket
from typing import Callable, Optional
from threading import Thread

from kit.network.base import Sender

from ..base import Model, Dispatcher
from ..answer import AnswerUpdate, ExceptionUpdate, NetworkException

from .server_sender import ServerSender


class ServerDispatcher(Dispatcher):
    sender: ServerSender

    on_connection_handler: Optional[Callable]
    on_disconnection_handler: Optional[Callable]
    on_method_handler: Optional[Callable]

    def __init__(self, sender: Sender) -> None:
        super().__init__(sender)

        self.on_connection_handler = None
        self.on_disconnection_handler = None
        self.on_method_handler = None

    def on_connection(self, handler: Callable) -> None:
        self.on_connection_handler = handler

    def on_disconnection(self, handler: Callable) -> None:
        self.on_disconnection_handler = handler

    def on_method(self, handler: Callable) -> None:
        self.on_method_handler = handler

    def process_connection(self, connection: socket) -> None:
        all_data = b""

        while True:
            try:
                all_data += connection.recv(1024)
            except ConnectionError:
                if self.on_disconnection_handler:
                    self.on_disconnection_handler(connection)

                self.sender.remove_connection(connection)

                return

            while True:
                if all_data.count(b"\n") == 0:
                    break

                data, _, all_data = all_data.partition(b"\n")
                loaded_data = json.loads(data)
                
                method = Model.parse(loaded_data)
                handler = self.get_handler(type(method))

                try:
                    if self.on_method_handler:
                        result = self.on_method_handler(connection, method, handler)
                    else:
                        result = handler(connection, method)
                except NetworkException as exc:
                    self.sender.send(connection, 
                        ExceptionUpdate(
                            code=exc.code,
                            result=None,
                            answer_id=loaded_data["id"]
                        )
                    )
                    
                    continue

                if result is None:
                    continue

                self.sender.send(connection, 
                    AnswerUpdate(
                        result=result,
                        answer_id=loaded_data["id"]
                    )
                )

    def _run(self) -> None:
        while True:
            connection = self.sender.sock.accept()[0]

            self.sender.add_connection(connection)

            if self.on_connection_handler:
                self.on_connection_handler(connection)
            
            Thread(target=self.process_connection, args=(connection, )).start()
