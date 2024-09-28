from kit.network import Method

from .models import MessageModel


class SendMessageMethod(Method):
    return_type = MessageModel

    text: str
    sender_name: str
