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

    def run(self) -> None:
        self.sender.run()
        self.dispatcher.run()