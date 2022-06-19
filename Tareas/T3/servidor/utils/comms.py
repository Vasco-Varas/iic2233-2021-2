import socket
import time


class ClientConnection:
    def __init__(self, socket_cliente, address):
        self.socket_cliente = socket_cliente
        self.address = address
        self.alive = True

    def close_connection(self):
        self.socket_cliente.close()
        self.alive = False

    def send_all(self, b):
        try:
            self.socket_cliente.sendall(b)
        except socket.error as e:
            if e.errno == 10053:  # aborted by software in host
                self.alive = False

    def encrypt(self, msg_bytes):
        b_1 = bytearray()
        b_2 = bytearray()
        b_3 = bytearray()

        for b_id, x in enumerate(msg_bytes):
            if b_id % 3 == 0:
                b_1.append(x)
            elif b_id % 3 == 1:
                b_2.append(x)
            elif b_id % 3 == 2:
                b_3.append(x)
        if b_2[0] > b_3[0]:
            b_1 = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_1])
            b_2 = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_2])
            b_3 = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_3])

            return b_1 + b_2 + b_3 + b'\x00'
        return b_2 + b_1 + b_3 + b'\x01'

    def decrypt(self, msg_bytes):
        b_1 = 0
        b_2 = 0
        b_3 = 0

        order = msg_bytes[-1] == 1
        if order:
            msg_bytes = msg_bytes[:-1]

        for b_id, x in enumerate(msg_bytes):
            if b_id % 3 == 0:
                b_1 += 1
            elif b_id % 3 == 1:
                b_2 += 1
            elif b_id % 3 == 2:
                b_3 += 1
        if order:
            b_b = msg_bytes[:b_2]
            b_a = msg_bytes[b_2:b_1 + b_2]
            b_c = msg_bytes[b_1 + b_2:b_1 + b_2 + b_3]

            dec = bytearray()
            for x in range(len(b_a)):
                adding = [b_a[x]]
                if len(b_b) > x:
                    adding.append(b_b[x])
                if len(b_c) > x:
                    adding.append(b_c[x])
                dec.extend(adding)
            return dec
        else:
            b_a = msg_bytes[:b_1]
            b_b = msg_bytes[b_1:b_1 + b_2]
            b_c = msg_bytes[b_1 + b_2:b_1 + b_2 + b_3]
            b_a = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_a])
            b_b = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_b])
            b_c = bytearray(
                [b'\x05' if x == b'\x03' else b'\x03' if x == b'\x05' else x for x in b_c])

            dec = bytearray()
            for x in range(len(b_a)):
                adding = [b_a[x]]
                if len(b_b) > x:
                    adding.append(b_b[x])
                if len(b_c) > x:
                    adding.append(b_c[x])
                dec.extend(adding)
            return dec

    def send_bytes(self, msg_bytes):
        msg_bytes = self.encrypt(msg_bytes)

        msg_len = len(msg_bytes).to_bytes(4, byteorder='little')

        msg_arr = []
        while len(msg_bytes) > 0:
            ba = bytearray(msg_bytes[:80])
            while len(ba) < 80:
                ba.append(0)
            msg_arr.append(ba)
            msg_bytes = msg_bytes[80:]

        self.send_all(msg_len)
        time.sleep(0.1)
        for id, byte_arr in enumerate(msg_arr):
            self.send_all(id.to_bytes(4, byteorder='big'))
            time.sleep(0.1)
            self.send_all(byte_arr)
        time.sleep(0.1)

    def send_text(self, msg):
        msg_bytes = msg.encode("utf-8")
        self.send_bytes(msg_bytes)

    def receive(self):
        try:
            data = self.socket_cliente.recv(4096)
            if data == b'':
                self.alive = False
                return None
            data_len = int.from_bytes(data, "little")
            total_bytes = []
            while len(total_bytes * 80) < data_len:
                part_id = int.from_bytes(self.socket_cliente.recv(4096), "little")
                part_msg = self.socket_cliente.recv(4096)
                total_bytes.append((part_id, part_msg))
            msg = bytearray()
            for msg_part in sorted(total_bytes, key=lambda x: x[0]):
                msg.extend(msg_part[1])
            while msg[-1] == 0:
                msg.pop()
            dec = self.decrypt(msg)
            return dec.decode('utf-8')
        except socket.error as e:
            if e.errno == 10054:  # Connection reset
                self.alive = False
        except Exception as e:
            print("Error reading msg", e)
