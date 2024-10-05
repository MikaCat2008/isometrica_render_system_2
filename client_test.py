from __future__ import annotations

from network import ClientManager
from network.updates import (
    MessageUpdate
)

client = ClientManager()


@client.on(MessageUpdate)
def on_message(update: MessageUpdate) -> None:
    message = update.message

    print(f"{message.sender_name}: {message.text}")


client.connect()
client.run()

name = input("enter name: ")

client.authorize(name).wait()
message = client.send_message("hi").wait()
