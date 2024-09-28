from kit.network import Update

from .models import MessageModel


class MessageUpdate(Update):
    message: MessageModel
