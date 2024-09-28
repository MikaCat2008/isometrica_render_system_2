from __future__ import annotations

import socket
from typing import Callable

from kit import Manager
from kit.network import Model, Method, Update, AnswerUpdate, ServerSender, ModelsFactory, ServerDispatcher


class ServerManager(Manager, init=False):
    sender: ServerSender
    dispatcher: ServerDispatcher
    
    def __init__(self) -> None:
        self.sender = ServerSender()
        self.dispatcher = ServerDispatcher(
            self.sender, models_factory
        )

    def message_update(self, connection: socket.socket,
        message: MessageModel
    ) -> None:
        self.sender.send(connection,
            MessageUpdate(
                message=message
            )
        )

    def register(self, method: Method, handler: Callable) -> None:
        self.dispatcher.register(method, handler)

    def run(self) -> None:
        self.sender.run()
        self.dispatcher.run()


class MessageModel(Model):
    text: str
    sender_name: str


class SendMessageMethod(Method):
    return_type = MessageModel

    text: str
    sender_name: str


class MessageUpdate(Update):
    message: MessageModel


models_factory = ModelsFactory([
    AnswerUpdate,
    MessageModel,
    MessageUpdate, 
    SendMessageMethod
])


def on_send_message(method: SendMessageMethod) -> MessageModel:
    message = MessageModel(
        text=method.text,
        sender_name=method.sender_name
    )

    for connection in server.sender.connections:
        server.message_update(connection, message)

    return message


server = ServerManager()
server.register(SendMessageMethod, on_send_message)
server.run()
