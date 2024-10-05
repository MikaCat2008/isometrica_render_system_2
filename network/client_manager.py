from __future__ import annotations

from typing import Callable

from kit import Manager
from kit.network import (
    Answer, 
    Update, 
    ClientSender, 
    ClientDispatcher
)

from .models import (
    MessageModel
)
from .methods import (
    AuthorizeMethod,
    SendMessageMethod
)


class ClientManager(Manager, init=False):
    token: int
    sender: ClientSender
    dispatcher: ClientDispatcher
    
    def __init__(self) -> None:
        self.token = -1
        self.sender = ClientSender()
        self.dispatcher = ClientDispatcher(self.sender)

    def _on_authorize_handler(self, token: int) -> None:
        self.token = token

    def authorize(self, name: str) -> Answer[int]:
        return self.sender.send(
            AuthorizeMethod(
                name=name
            )
        ).on_result(self._on_authorize_handler)

    def send_message(self, text: str) -> Answer[MessageModel]:
        return self.sender.send(
            SendMessageMethod(token=self.token,
                text=text
            )
        )

    def on(self, update: Update) -> Callable:
        def _(handler: Callable) -> None:
            self.dispatcher.register(update, handler)

        return _

    def connect(self, host: str = "localhost", port: int = 7777) -> None:
        self.sender.connect(host, port)

    def run(self) -> None:
        self.sender.run()
        self.dispatcher.run()
