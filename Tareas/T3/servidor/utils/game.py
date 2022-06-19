from utils.server_utils import Timer


class Game:
    def mark_as_overtime(self, player):
        if player.game:
            game = player.game
            other_player = game.player_1 if player is game.player_2 else game.player_2

            player.send_text(f"GAME\nEND\n{other_player.name}\n{player.name}")
            other_player.send_text(f"GAME\nEND\n{other_player.name}\n{player.name}")

            self.player_1.game = None
            self.player_1.name = None
            self.player_2.game = None
            self.player_2.name = None

    def __init__(self, p1, p2):
        self.player_1 = p1
        self.player_2 = p2

        self.turn_time = 0
        self.turn_timer = Timer(target=self.mark_as_overtime)

        self.player_1_ready = False
        self.player_2_ready = False

        self.player_1_bet = 0
        self.player_2_bet = 0

        self.player_1_bet_even = False
        self.player_2_bet_even = False

        self.turn = p1
        self.turn_id = 1

        self.p1_marbles = 10
        self.p2_marbles = 10

    def update_turns(self):
        print(f"Comienza el turno #{self.turn_id}: Jugador (ID:{self.turn.uuid})")
        if self.turn is self.player_1:
            self.player_1.send_text(f"GAME\nSETINFO\nTu turno!\n\n0")
            self.player_2.send_text(f"GAME\nSETINFO\nEsperando a {self.turn.name}\n\n0")
            self.player_1.send_text(f"GAME\nSETSELFTURN\nTRUE\n{self.turn_time}")
            self.player_2.send_text(f"GAME\nSETSELFTURN\nFALSE\n{self.turn_time}")
            if self.turn_time > 0:
                self.turn_timer.start_timer(self.turn_time, params=(self.player_1,))
        if self.turn is self.player_2:
            self.player_1.send_text(f"GAME\nSETINFO\nEsperando a {self.turn.name}\n\n0")
            self.player_2.send_text(f"GAME\nSETINFO\nTu turno!\n\n0")
            self.player_1.send_text(f"GAME\nSETSELFTURN\nFALSE\n{self.turn_time}")
            self.player_2.send_text(f"GAME\nSETSELFTURN\nTRUE\n{self.turn_time}")
            if self.turn_time > 0:
                self.turn_timer.start_timer(self.turn_time, params=(self.player_2,))

    def check_win_condition(self):
        if self.p1_marbles <= 0 or self.p2_marbles <= 0:
            winner = self.player_1 if self.p1_marbles > 0 else self.player_2
            print(f"Juego finalizado. Ganador: Usuario (ID: {winner.uuid})")
            if winner is self.player_1:
                self.player_1.send_text(f"GAME\nEND\n{self.player_1.name}\n{self.player_2.name}")
                self.player_2.send_text(f"GAME\nEND\n{self.player_1.name}\n{self.player_2.name}")
            else:
                self.player_1.send_text(f"GAME\nEND\n{self.player_2.name}\n{self.player_1.name}")
                self.player_2.send_text(f"GAME\nEND\n{self.player_2.name}\n{self.player_1.name}")
            self.player_1.game = None
            self.player_1.name = None
            self.player_2.game = None
            self.player_2.name = None

    def parse(self, cl, cmd):
        if len(cmd) == 1 and cmd[0] == "SET_READY":
            self.player_1_ready = cl is self.player_1 or self.player_1_ready
            self.player_2_ready = cl is self.player_2 or self.player_2_ready

            if self.player_1_ready and self.player_2_ready:
                self.update_turns()

        elif len(cmd) == 2 and cmd[0] == "CHEATCODE":
            if cmd[1] == "FA":
                # This cheatcode can only be used by the player 2
                if cl is self.player_2:
                    if self.turn is self.player_2:
                        print(
                            f"Player (ID:{self.turn.uuid}) used the FA cheatcode on " +
                            f"(ID:{self.player_1.uuid})")
                        self.player_2.send_text(f"GAME\nCHEATCODE\nFA\n{self.player_1_bet}")
                    else:
                        self.player_2.send_text(
                            f"GAME\nSHOWERROR\nThis cheatcode can only be used when its your turn")
                else:
                    self.player_1.send_text("SHOWERROR\nThis cheatcode cannot be used by player 2")
            elif cmd[1] == "ZX":
                if cl is self.turn:
                    if cl is self.player_1:
                        print(
                            f"Player (ID:{cl.uuid}) used the ZX cheatcode on " +
                            f"(ID:{self.player_2.uuid})")
                        self.p1_marbles += 3
                        self.p2_marbles -= 3
                    else:
                        print(
                            f"Player (ID:{cl.uuid}) used the ZX cheatcode on " +
                            f"(ID:{self.player_1.uuid})")
                        self.p2_marbles += 3
                        self.p1_marbles -= 3
                    self.player_1.send_text(
                        f"GAME\nSETMARBLES\n{self.p1_marbles}\n{self.p2_marbles}")
                    self.player_2.send_text(
                        f"GAME\nSETMARBLES\n{self.p1_marbles}\n{self.p2_marbles}")
                    self.check_win_condition()
                else:
                    cl.send_text(
                        f"GAME\nSHOWERROR\nThis cheatcode can only be used when its your turn")

        elif len(cmd) == 3 and cmd[0] == "SETBET":
            if self.turn is cl:
                self.turn_timer.stop()
                odd_even = "par" if cmd[1] == "TRUE" else "impar"

                if int(cmd[2]) <= 0:
                    print(f"El jugador (ID:{self.turn.uuid}) intentó apostar {cmd[2]} canicas.")
                    self.turn.send_text("GAME\nSHOWERROR\nNo puede apostar menos de 1 canica")
                    return
                if int(cmd[2]) > (
                        self.p1_marbles if self.turn is self.player_1 else self.p2_marbles):
                    print(
                        f"El jugador (ID:{self.turn.uuid}) intentó apostar {cmd[2]} " +
                        f"canicas (No tiene suficientes).")
                    self.turn.send_text("GAME\nSHOWERROR\nNo tienes suficientes canicas")
                    return

                print(
                    f"El jugador (ID:{self.turn.uuid}) apostó {cmd[2]} " +
                    f"canicas a que su oponente apostó {odd_even}")
                if self.turn is self.player_1:
                    self.player_1_bet = int(cmd[2])
                    self.player_1_bet_even = cmd[1] == "TRUE"
                    self.turn = self.player_2
                else:
                    self.player_2_bet = int(cmd[2])
                    self.player_2_bet_even = cmd[1] == "TRUE"
                    self.turn = self.player_1

                    oe1 = "par" if self.player_1_bet_even else "impar"
                    oe2 = "par" if self.player_2_bet_even else "impar"

                    p1_won = self.player_1_bet_even == (self.player_2_bet % 2 == 0)
                    p2_won = self.player_2_bet_even == (self.player_1_bet % 2 == 0)

                    self.player_1.send_text(f"GAME\nOPONENTBET\n{self.player_2_bet}\n" +
                                            f"{'TRUE' if self.player_2_bet_even else 'FALSE'}")
                    self.player_2.send_text(f"GAME\nOPONENTBET\n{self.player_1_bet}\n" +
                                            f"{'TRUE' if self.player_1_bet_even else 'FALSE'}")
                    win_type = ""
                    if p1_won == p2_won:
                        win_type = "Empate"
                        self.player_1.send_text(f"GAME\nSETINFO\n¡Empate!\n\n1")
                        self.player_2.send_text(f"GAME\nSETINFO\n¡Empate!\n\n1")
                    elif p1_won:
                        win_type = f"(ID: {self.player_1.uuid})"
                        self.p1_marbles += self.player_2_bet
                        self.p2_marbles -= self.player_2_bet
                        self.player_1.send_text(
                            f"GAME\nSETINFOPROTECT\n¡{self.player_2.name} ha perdido!" +
                            f"\nGanas {self.player_2_bet} canicas\n1\n1000")
                        self.player_2.send_text(
                            f"GAME\nSETINFOPROTECT\n¡{self.player_2.name} ha perdido!" +
                            f"\nPierdes {self.player_2_bet} canicas\n1\n1000")
                    elif p2_won:
                        win_type = f"(ID: {self.player_2.uuid})"
                        self.p1_marbles -= self.player_1_bet
                        self.p2_marbles += self.player_1_bet
                        self.player_1.send_text(
                            f"GAME\nSETINFOPROTECT\n¡{self.player_1.name} " +
                            f"ha perdido!\nPierdes {self.player_1_bet} canicas\n1\n1000")
                        self.player_2.send_text(
                            f"GAME\nSETINFOPROTECT\n¡{self.player_1.name} " +
                            f"ha perdido!\nGanas {self.player_1_bet} canicas\n1\n1000")

                    self.player_1.send_text(
                        f"GAME\nSETMARBLES\n{self.p1_marbles}\n{self.p2_marbles}")
                    self.player_2.send_text(
                        f"GAME\nSETMARBLES\n{self.p1_marbles}\n{self.p2_marbles}")

                    print(f'''Ronda {self.turn_id} finalizada:
El jugador (ID:{self.player_1.uuid} apostó {self.player_1_bet} canicas a que ''' +
                          f'''(ID:{self.player_2.uuid}) apostó {oe1}
El jugador (ID:{self.player_2.uuid} apostó {self.player_2_bet} canicas a que ''' +
                          f'''(ID:{self.player_1.uuid}) apostó {oe2}
Ganador de la ronda: {win_type}''')

                self.check_win_condition()

                self.turn_id += 1
                self.update_turns()
            else:
                print(f"Player (ID:{cl.uuid}) tried to play when its not their turn!")
