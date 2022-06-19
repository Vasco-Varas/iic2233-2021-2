import socket
import json

from utils.comms import ClientConnection
from utils.client import Client
from utils.server import Server

try:
    with open("parametros.json", "r") as f:
        p = json.load(f)
except IOError:
    print("Could not read parameters file")
except json.decoder.JSONDecodeError as e:
    print(f"Could not decode json file. Is it correctly formatted?\nLine {e.lineno}: \"{e.msg}\"")
else:
    host = p["host"] if "host" in p else None
    port = p["port"] if "port" in p else None
    turn_time = p["TIEMPO_TURNO"] if "TIEMPO_TURNO" in p else None

    if turn_time is None:
        print("No TIEMPO_TURNO in 'parametros.json' using 0 (Disabled)")
        turn_time = 0
    if type(turn_time) == str:
        turn_time = int(turn_time)
    elif type(turn_time) != int:
        print("Invalid TIEMPO_TURNO in 'parametros.json' using 0 (Disabled)")
        turn_time = 0

    if type(host) != str:
        host = socket.gethostname()
        print(f"Host has to be a string. Using '{host}'")

    if type(port) == str and port.isdigit():
        port = int(port)
    elif type(port) != int:
        print(f"Port has to be a number. switching from {port} to 9000")
        port = 9000

    if not host or not port:
        if not host:
            host = socket.gethostname()
            print(f"Host not specified in parametros.py. Using '{host}'")
        if not port:
            port = 9000
            print(f"Port not specified in parametros.py. Using '{port}'")

    try:
        print(f"Iniciando el servidor en {host}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
    except socket.error as e:
        if e.errno == 10048:
            print(f"Could not start server. Maybe its already running or {host}:{port} is taken.")
        else:
            raise e
    else:
        print(f"Succesfully started server on port {port}")

        server = Server()
        server.turn_time = turn_time
        server.start()

        while True:
            try:
                socket_cliente, address = sock.accept()
            except socket.error as e:
                print(
                    "Uncaught exception when accepting an incoming connection. " +
                    "Continuing to listen for connections")
            cc = ClientConnection(socket_cliente, address)
            new_client_id = server.get_next_id()
            client = Client(new_client_id, conn=cc)
            # print(f"Adding client: {new_client_id}, {client.uuid}")
            # print(f"New client connected! (ID: {new_client_id})")
            server.add_client(client)
            print(f"Nuevo usuario conectado (ID:{client.uuid})")
