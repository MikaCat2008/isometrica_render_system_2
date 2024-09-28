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
    SendMessageMethod
)


class ClientManager(Manager, init=False):
    sender: ClientSender
    dispatcher: ClientDispatcher
    
    def __init__(self) -> None:
        self.sender = ClientSender()
        self.dispatcher = ClientDispatcher(self.sender)

    def send_message(self, text: str, sender_name: str) -> Answer[MessageModel]:
        return self.sender.send(
            SendMessageMethod(
                text=text,
                sender_name=sender_name
            )
        )

    def on(self, update: Update) -> Callable:
        def _(handler: Callable) -> None:
            self.dispatcher.register(update, handler)

        return _

    def run(self) -> None:
        self.sender.run()
        self.dispatcher.run()
