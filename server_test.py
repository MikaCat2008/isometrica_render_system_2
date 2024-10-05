from __future__ import annotations

from socket import socket
from typing import Any, Callable
from dataclasses import dataclass

from network import ServerManager
from network.models import (
    MessageModel
)
from network.methods import (
    Method,
    SecuredMethod,
    AuthorizeMethod,
    SendMessageMethod
)
from network.exceptions import Exceptions

server = ServerManager()


def broadcast_message(text: str, sender_name: str = "Server") -> MessageModel:
    message = MessageModel(
        text=text, sender_name=sender_name
    )

    for connection in server.sender.connections.values():
        server.message_update(connection, message)
    
    print(f"{sender_name}: {text}")

    return message


@server.on_disconnection
def on_disconnection(sock: socket) -> None:
    sock_id = id(sock)
    user_data = users[sock_id]

    broadcast_message(f"{user_data.name} has left")

    del users[sock_id]


@server.on_method
def on_method(connection: socket, method: Method, handler: Callable) -> Any:
    sock_id = id(connection)
    
    if isinstance(method, SecuredMethod):
        user_data = users.get(sock_id)

        if not user_data or method.token != user_data.token:
            raise Exceptions.NotAuthorized

    return handler(connection, method)


@server.on(AuthorizeMethod)
def on_authorize(connection: socket, method: AuthorizeMethod) -> int:
    name = method.name
    sock_id = id(connection)

    if sock_id not in users:
        users[sock_id] = UserData(
            name=name,
            token=sock_id
        )

        broadcast_message(f"{name} has joined")
    
    return sock_id


@server.on(SendMessageMethod)
def on_send_message(connection: socket, method: SendMessageMethod) -> MessageModel:
    user_data = users[id(connection)]
    
    return broadcast_message(
        method.text, user_data.name
    )


@dataclass
class UserData:
    name: str
    token: int


users: dict[int, UserData] = {}
server.start()
server.run()
