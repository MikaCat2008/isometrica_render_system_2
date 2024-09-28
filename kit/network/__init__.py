from __future__ import annotations

import time, json, socket
from typing import Any, Type, TypeVar, Generic, ClassVar, Callable, Optional
from threading import Lock, Event, Thread

from pydantic import BaseModel, TypeAdapter

T = TypeVar("T")


class Model(BaseModel):
    ...


class Method(Model):
    return_type: ClassVar[Any] = None


class Update(Model):
    ...


class AnswerUpdate(Update):
    result: Any
    answer_id: int


class Answer(Generic[T]):
    event: Event
    result: Any
    adapter: TypeAdapter
    answer_id: int
    listeners: list[Callable]
    result_type: Type
    
    def __init__(self, answer_id: int, result_type: Type) -> None:
        super().__init__()
        
        self.event = Event()
        self.result = None
        self.adapter = TypeAdapter(result_type)
        self.answer_id = answer_id
        self.listeners = []
        self.result_type = result_type
    
    def set(self, result: Any) -> None:
        self.result = self.adapter.validate_python(result)
        self.event.set()

        for listener in self.listeners:
            listener(self.result)
    
    def wait(self) -> T:
        if self.result_type is None:
            return None

        self.event.wait()
        
        return self.result

    def on_result(self, listener: Callable) -> None:
        self.listeners.append(listener)


class ModelsFactory:
    factories: dict[str, Type[Model]]

    def __init__(self, models: list[Type[Model]]) -> None:
        self.factories = {
            model.__name__: model
            for model in models
        }

    def create(self, data: dict) -> Model:
        model_type: str = data["type"]
        model_data: dict = data["data"]

        model_factory = self.factories[model_type]
        
        return model_factory(**model_data)


class Runnable:
    def _run(self) -> None:
        ...

    def run(self) -> None:
        self._thread = Thread(target=self._run)
        self._thread.start()


class Sender(Runnable):
    ...


class Dispatcher(Runnable):
    sender: Sender
    handlers: dict[Type[Model], Callable]
    models_factory: ModelsFactory
    
    def __init__(self, sender: Sender, models_factory: ModelsFactory) -> None:
        self.sender = sender
        self.handlers = {}
        self.models_factory = models_factory

    def process(self, model: Model) -> Any:
        handler = self.handlers.get(type(model))

        if handler:
            return handler(model)

    def register(self, model: Type[Model], handler: Callable) -> None:
        self.handlers[model] = handler


class ClientSender(Runnable):
    lock: Lock
    sock: socket.socket
    answers: dict[int, Answer]
    sending_list: list[tuple[Method, int]]
    next_answer_id: int
    
    def __init__(self, host: str = "localhost", port: int = 7777) -> None:
        self.lock = Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.answers = {}
        self.sending_list = []
        self.next_answer_id = 0

    def send(self, method: Method) -> Answer:
        with self.lock:
            answer_id = self.next_answer_id
            answer = Answer(answer_id, method.return_type)
                    
            self.next_answer_id += 1
            self.answers[answer_id] = answer
            self.sending_list.append((method, answer_id))

        return answer

    def _run(self) -> None:
        while True:
            time.sleep(0.01)

            with self.lock:
                if not self.sending_list:
                    continue

                data = b"".join(
                    json.dumps({
                        "id": answer_id,
                        "type": type(method).__name__,
                        "data": method.model_dump()
                    }).encode() + b"\n"
                    for method, answer_id in self.sending_list
                )

                self.sock.sendall(data)
                self.sending_list.clear()


class ClientDispatcher(Dispatcher):
    sender: ClientSender

    def __init__(self, sender: Sender, models_factory: ModelsFactory) -> None:
        super().__init__(sender, models_factory)

        self.register(AnswerUpdate, self.resolve)

    def resolve(self, answer: AnswerUpdate) -> None:
        result = answer.result
        answer_id = answer.answer_id

        with self.sender.lock:
            self.sender.answers[answer_id].set(result)
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
                update = self.models_factory.create(loaded_data)
                
                self.process(update)


class ServerSender(Sender):
    sock: socket.socket
    locks: dict[int, Lock]
    connections: list[socket.socket]
    sending_lists: dict[int, list[Update]]

    def __init__(self, host: str = "localhost", port: int = 7777) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        self.locks = {}
        self.connections = []
        self.sending_lists = {}

    def send(self, connection: socket.socket, method: Method) -> None:
        sock_id = id(connection)
        lock = self.locks[sock_id]
        
        with lock:
            self.sending_lists[sock_id].append(method)

    def _run(self) -> None:
        while True:
            time.sleep(0.01)
            
            for connection in self.connections:
                sock_id = id(connection)

                lock = self.locks[sock_id]
                sending_list = self.sending_lists[sock_id]
                
                with lock:
                    if not sending_list:
                        continue

                    data = b"".join(
                        json.dumps({
                            "type": type(update).__name__,
                            "data": update.model_dump()
                        }).encode() + b"\n"
                        for update in sending_list
                    )

                    connection.sendall(data)
                    sending_list.clear()


class ServerDispatcher(Dispatcher):
    sender: ServerSender
    
    def process_connection(self, connection: socket.socket) -> None:
        sock_id = id(connection)
        all_data = b""

        while True:
            try:
                all_data += connection.recv(1024)
            except ConnectionError:
                del self.sender.locks[sock_id]
                self.sender.connections.remove(connection)
                del self.sender.sending_lists[sock_id]

                return

            while True:
                if all_data.count(b"\n") == 0:
                    break

                data, _, all_data = all_data.partition(b"\n")
                loaded_data = json.loads(data)
                method = self.models_factory.create(loaded_data)
                result = self.process(method)

                if result is None:
                    continue

                self.sender.send(connection, 
                    AnswerUpdate(
                        result=result,
                        answer_id=loaded_data["id"]
                    )
                )

    def _run(self) -> None:
        while True:
            connection = self.sender.sock.accept()[0]

            sock_id = id(connection)

            self.sender.locks[sock_id] = Lock()
            self.sender.connections.append(connection)
            self.sender.sending_lists[sock_id] = []
            
            Thread(target=self.process_connection, args=(connection, )).start()
