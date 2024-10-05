import json

from ..base import Model, Sender, Dispatcher
from ..answer import AnswerUpdate, ExceptionUpdate

from .client_sender import ClientSender


class ClientDispatcher(Dispatcher):
    sender: ClientSender

    def __init__(self, sender: Sender) -> None:
        super().__init__(sender)

        self.register(AnswerUpdate, self._answer_handler)
        self.register(ExceptionUpdate, self._exception_handler)

    def _answer_handler(self, answer: AnswerUpdate) -> None:
        result = answer.result
        answer_id = answer.answer_id

        with self.sender.lock:
            self.sender.answers[answer_id].set_result(result)
            del self.sender.answers[answer_id]

    def _exception_handler(self, exception: ExceptionUpdate) -> None:
        code = exception.code
        answer_id = exception.answer_id

        with self.sender.lock:
            self.sender.answers[answer_id].set_exception(code)
            del self.sender.answers[answer_id]

    def _run(self) -> None:
        all_data = b""

        while True:
            try:
                all_data += self.sender.sock.recv(1024)
            except ConnectionError:
                ...

            while True:
                if all_data.count(b"\n") == 0:
                    break

                data, _, all_data = all_data.partition(b"\n")
                loaded_data = json.loads(data)
                update = Model.parse(loaded_data)
                handler = self.get_handler(type(update))

                if handler:
                    handler(update)
