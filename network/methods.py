from kit.network import Method

from .models import MessageModel


class SecuredMethod(Method):
    token: int


class AuthorizeMethod(Method):
    return_type = int

    name: str


class SendMessageMethod(SecuredMethod):
    return_type = MessageModel

    text: str
