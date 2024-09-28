from __future__ import annotations

from network import ServerManager
from network.models import (
    MessageModel
)
from network.methods import (
    SendMessageMethod
)

server = ServerManager()


@server.on(SendMessageMethod)
def on_send_message(method: SendMessageMethod) -> MessageModel:
    message = MessageModel(
        text=method.text,
        sender_name=method.sender_name
    )

    for connection in server.sender.connections:
        server.message_update(connection, message)

    return message


server.run()
