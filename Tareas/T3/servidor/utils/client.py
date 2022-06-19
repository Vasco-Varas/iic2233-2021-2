from threading import Thread, Lock


class Client:
    def __init__(self, uuid, name=None, conn=None):
        self.name = name
        self.uuid = uuid
        self.conn = conn
        self.alive = True
        self.in_lobby = False
        self.game = None
        self.last_ping = 0

        self.message_list = []

        self._message_lock = Lock()

        listener_thr = Thread(target=self.listen_messages)
        listener_thr.start()

    def get_messages(self):
        with self._message_lock:
            messages = self.message_list
            self.message_list = []
        return messages

    def listen_messages(self):
        while self.alive:
            msg = self.conn.receive()
            self.alive = self.conn.alive
            if msg is None:
                return
            with self._message_lock:
                self.message_list.append(msg)

    def send_text(self, msg):
        if self.conn is not None:
            self.conn.send_text(msg)
        else:
            print("ERROR (send_text): client is not connected")
