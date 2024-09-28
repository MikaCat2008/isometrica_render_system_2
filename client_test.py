from __future__ import annotations

from typing import Callable

from kit import Manager
from kit.network import Model, Answer, Method, Update, AnswerUpdate, ClientSender, ModelsFactory, ClientDispatcher


class ClientManager(Manager, init=False):
    sender: ClientSender
    dispatcher: ClientDispatcher
    
    def __init__(self) -> None:
        self.sender = ClientSender()
        self.dispatcher = ClientDispatcher(
            self.sender, models_factory
        )

    def send_message(self, text: str, sender_name: str) -> Answer[MessageModel]:
        return self.sender.send(
            SendMessageMethod(
                text=text,
                sender_name=sender_name
            )
        )

    def register(self, update: Update, handler: Callable) -> None:
        self.dispatcher.register(update, handler)

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
    SendMessageMethod,
])


def on_message(update: MessageUpdate) -> None:
    message = update.message

    print(f"{message.sender_name}: {message.text}")


client = ClientManager()
client.register(MessageUpdate, on_message)
client.run()

message = client.send_message("hi", "adolf").wait()

print(message)
