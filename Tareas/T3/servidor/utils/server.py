import random
from threading import Thread
from utils.checks import check_username, check_birthday
from utils.game import Game


class Server(Thread):
    def __init__(self):
        super(Server, self).__init__()
        self.clients = {}
        self.keep_alive = True

        self.turn_time = 0

    def get_next_id(self):
        m = range(len(self.clients.keys()) + 1)
        return min(set(m) - set(self.clients.keys()))

    def clean_remove(self, removing):
        print("Removing user:", removing.name, removing.uuid)
        removing.alive = False
        if removing.game:
            gm = removing.game
            other_player = gm.player_1 if removing is not gm.player_1 else gm.player_2
            other_player.send_text(f"GAME\nEND\n{other_player.name}\n{removing.name}")
            other_player.send_text(
                "GAME\nSHOWERROR\nEl oponente se ha desconectado. Has ganado por defecto")
            other_player.game = None
            other_player.name = None

        if removing.name and removing.in_lobby:
            print("Continue:", removing.name, removing.uuid)
            for client in self.clients.values():
                if client.name is not None and client.in_lobby:
                    client.send_text(f"CLIENTS\nDISCONNECT\n{removing.uuid}")

    def fake_disconnect_user(self, user):
        print("Fake disconnecting:", user.name, user.uuid)
        if user.name is not None and user.in_lobby:
            print("Continue disconnecting:", user.name, user.uuid)
            for client in self.clients.values():
                if client.name is not None and client.in_lobby and client is not user:
                    client.send_text(f"CLIENTS\nDISCONNECT\n{user.uuid}")

    def amount_players_lobby(self):
        return len(
            list(filter(lambda x: x.name is not None and x.in_lobby, self.clients.values()))) + 1

    def run(self):
        while self.keep_alive:
            for cl in self.clients.copy().values():
                # if cl.last_ping == 0 and cl.name:
                #    print("PINGING", cl.uuid)
                #    cl.send_text("PING")
                # cl.last_ping = (cl.last_ping + 1) % 10000
                if not cl.alive:
                    print(f"User (ID:{cl.uuid}) was forcefully disconnected!")
                    self.clean_remove(self.clients.pop(cl.uuid))
                    continue
                msgs = cl.get_messages()
                for msg in msgs:
                    cmd = msg.split("\n")
                    if len(cmd) == 3 and cmd[0] == "RETO" and cmd[1] == "INICIO":
                        print(f"El usuario (ID: {cl.uuid}) reto al usuario (ID:{cmd[2]})")
                        n_cl = self.clients[int(cmd[2])]
                        for client in self.clients.values():
                            if client.uuid != n_cl.uuid:
                                client.send_text(f"USER\nNEW\n{n_cl.uuid}\n{n_cl.name}\nFALSE")
                        n_cl.send_text(f"RETO\nINVITACION\n{cl.name}\n{cl.uuid}")

                    elif len(cmd) == 3 and cmd[0] == "RETO" and cmd[1] == "ACCEPTED":
                        print(
                            f"El usuario (ID: {cl.uuid}) " +
                            f"aceptó el reto del usuario (ID:{cmd[2]})")
                        self.fake_disconnect_user(cl)
                        self.fake_disconnect_user(self.clients[int(cmd[2])])
                        cl.in_lobby = False
                        self.clients[int(cmd[2])].in_lobby = False
                        # Set random icons and id_value
                        players = [cl, self.clients[int(cmd[2])]]
                        p1 = random.choice(players)
                        players.remove(p1)
                        p2 = players[0]
                        new_game = Game(p1, p2)
                        new_game.turn_time = self.turn_time
                        p1.game = new_game
                        p2.game = new_game
                        p1.send_text(
                            f"GAME\nSTART\n1\n{p1.name}\n{p2.name}\n{new_game.p1_marbles}")
                        p2.send_text(
                            f"GAME\nSTART\n2\n{p1.name}\n{p2.name}\n{new_game.p1_marbles}")

                    elif cmd[0] == "GAME":
                        if cl.game:
                            cl.game.parse(cl, cmd[1:])
                        else:
                            print(f"Player (ID:{cl.uuid}) tried to play a non existing game")

                    elif len(cmd) == 1 and cmd[0] == "PING":
                        # print("Client is pinging")
                        pass

                    elif len(cmd) == 3 and cmd[0] == "RETO" and cmd[1] == "REFUSED":
                        print(
                            f"El usuario (ID: {cl.uuid}) rechazo " +
                            f"el reto del usuario (ID:{cmd[2]})")

                        n_cl = self.clients[cl.uuid]
                        for client in self.clients.values():
                            if client.uuid != n_cl.uuid:
                                client.send_text(f"USER\nNEW\n{n_cl.uuid}\n{n_cl.name}\nTRUE")

                    elif len(cmd) == 1 and cmd[0] == "DISCONNECTION":
                        print(f"Usuario (ID:{cl.uuid}) desconectado.")
                        self.clean_remove(self.clients.pop(cl.uuid))

                    elif len(cmd) == 3 and cmd[0] == "LOGIN":
                        print(f"El usuario (ID: {cl.uuid}) quiere el nombre {cmd[1]}", end="")
                        if not check_username(cmd[1]):
                            print(" pero no es valido")
                            cl.send_text("CLIENT\nUSERNAME\nNOTVALID")
                        elif cmd[1] in map(lambda x: x.name, self.clients.values()):
                            print(" pero ya hay un usuario llamado así")
                            cl.send_text("CLIENT\nUSERNAME\nINUSE")
                        else:
                            b_check = check_birthday(cmd[2])
                            if b_check != "ALLOW":
                                print(
                                    "... Disponible, pero el cumpleaños " +
                                    "no cumple los requisitos.")
                                cl.send_text(f"CLIENT\nBIRTHDAYERROR\n{b_check}")
                                continue
                            print(f"... Aceptado! y el cumpleaños ({cmd[2]}) también.", end="")
                            lobby_amount = self.amount_players_lobby()
                            if lobby_amount > 4:
                                print(f" Pero el lobby está lleno! ({lobby_amount}/4)")
                                cl.send_text(
                                    "CLIENT\nLOBBYFULL\nThe lobby is " +
                                    "full, please try again later")
                                continue
                            print(f" ({lobby_amount}/4 players are now in the lobby)")
                            cl.send_text("CLIENT\nUSERNAME\nACCEPTED")
                            logged_in_clients = ""
                            for client in self.clients.values():
                                if client.name is not None:
                                    client.send_text(f"USER\nNEW\n{cl.uuid}\n{cmd[1]}\nTRUE")
                                    str_in_lobby = 'TRUE' if client.in_lobby else 'FALSE'
                                    logged_in_clients += (f"\n{client.uuid}\n{client.name}\n" +
                                                          f"{str_in_lobby}")

                            cl.send_text(f"CLIENTS\nLIST{logged_in_clients}")
                            cl.name = cmd[1]
                            cl.in_lobby = True
                    else:
                        print(
                            f"Error en el commando '{cmd}' {len(cmd)} " +
                            f"enviado por User (ID:{cl.uuid})")

    def add_client(self, client):
        self.clients[client.uuid] = client
