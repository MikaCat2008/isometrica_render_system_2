import json
from socket import socket
from threading import Lock, Thread

from ..base import Model, Dispatcher
from ..answer import AnswerUpdate

from .server_sender import ServerSender


class ServerDispatcher(Dispatcher):
    sender: ServerSender
    
    def process_connection(self, connection: socket) -> None:
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
                method = Model.parse(loaded_data)
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
