from __future__ import annotations

from socket import socket
from typing import Callable

from kit import Manager
from kit.network import (
    Method, 
    ServerSender, 
    ServerDispatcher
)

from .models import (
    MessageModel
)
from .updates import (
    MessageUpdate
)


class ServerManager(Manager, init=False):
    sender: ServerSender
    dispatcher: ServerDispatcher
    
    def __init__(self) -> None:
        self.sender = ServerSender()
        self.dispatcher = ServerDispatcher(self.sender)

    def message_update(self, connection: socket,
        message: MessageModel
    ) -> None:
        self.sender.send(connection,
            MessageUpdate(
                message=message
            )
        )

    def on(self, method: Method) -> Callable:
        def _(handler: Callable) -> None:
            self.dispatcher.register(method, handler)

        return _

    def on_connection(self, handler: Callable) -> None:
        return self.dispatcher.on_connection(handler)

    def on_disconnection(self, handler: Callable) -> None:
        return self.dispatcher.on_disconnection(handler)

    def on_method(self, handler: Callable) -> None:
        return self.dispatcher.on_method(handler)

    def start(self, host: str = "localhost", port: int = 7777) -> None:
        self.sender.start(host, port)

    def run(self) -> None:
        self.sender.run()
        self.dispatcher.run()