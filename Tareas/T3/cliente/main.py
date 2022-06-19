import json
import socket

from utils.comms import ClientServerConnection
import sys
from PyQt5.QtWidgets import QApplication

from frontend.mainmenu_frontend import MainMenuFrontend
from backend.mainmenu_backend import MainMenuBackend

from frontend.error_frontend import ErrorFrontend

from frontend.lobby_frontend import LobbyFrontend
from backend.lobby_backend import LobbyBackend

from frontend.invitation_frontend import InvitationFrontend
from backend.invitation_backend import InvitationBackend

from frontend.game_frontend import GameFrontend
from backend.game_backend import GameBackend

from frontend.game_end_frontend import GameEndFrontend


def hook(type, _, traceback):
    print(type)
    print(traceback)


sys.__excepthook__ = hook

app = QApplication(sys.argv)


def connect_server():
    try:
        server_conn = ClientServerConnection(host, port)
    except socket.error as e:
        # This not handled here in order to be able to show the message in a GUI window
        print(f"Could not connect to server: Connection error ({e})")
    else:
        print(f"(Re)connected to {host}:{port}")

        if menu_backend:
            menu_backend.server_connection = server_conn
            lobby_backend.server_connection = server_conn
            game_backend.server_connection = server_conn
            game_end_frontend.server_connection = server_conn
        return server_conn


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

    paths = p["paths"] if "paths" in p else None
    if type(paths) != dict:
        print(
            "Invalid value for key: 'paths' in 'parametros.json'..." +
            " using defaults\nresources: 'resources/'")
        resources = "resources/"
    else:
        resources = paths["resources"] if "resources" in paths else None

    if not resources or type(resources) != str:
        if not resources:
            print(
                "paths.resources not found in 'parametros.json'..." +
                " using defaults\nresources: 'resources/'")
        resources = "resources/"

    if type(host) != str:
        host = socket.gethostname()
        print(f"Host has to be a string. Using '{host}'")

    if port.isdigit():
        port = int(port)
    else:
        print(f"Port has to be a number. switching fron {port} to 9000")
        port = 9000

    if not host or not port:
        if not host:
            host = socket.gethostname()
            print(f"Host not specified in parametros.py. Using '{host}'")
        if not port:
            port = 9000
            print(f"Port not specified in parametros.py. Using '{port}'")

    error_frontend = ErrorFrontend(resources)

    menu_backend = None
    server_conn = connect_server()
    if not server_conn:
        error_frontend.show_error(
            "No se pudo conectar al servidor.\nIntentelo de nuevo más tarde.")
        app.exec_()

    menu_frontend = MainMenuFrontend(resources)
    menu_backend = MainMenuBackend()

    lobby_frontend = LobbyFrontend(resources)
    lobby_backend = LobbyBackend()

    invitation_frontend = InvitationFrontend(resources)
    invitation_backend = InvitationBackend()

    game_frontend = GameFrontend(resources)
    game_backend = GameBackend()

    game_end_frontend = GameEndFrontend(resources)

    menu_frontend.sgn_login.connect(menu_backend.click_login)
    menu_frontend.sgn_check_server_status.connect(menu_backend.check_server_status)

    menu_backend.sgn_hide_mainmenu.connect(menu_frontend.hide)
    menu_backend.sgn_show_lobby.connect(lobby_backend.show_lobby)
    menu_backend.sgn_error.connect(error_frontend.show_error)
    menu_backend.sgn_hide_all.connect(game_end_frontend.hide)
    menu_backend.sgn_hide_all.connect(game_frontend.hide)
    menu_backend.sgn_hide_all.connect(invitation_frontend.hide)
    menu_backend.sgn_hide_all.connect(lobby_frontend.hide)
    menu_backend.sgn_hide_all.connect(menu_frontend.hide)
    menu_backend.sgn_reconnect.connect(connect_server)

    lobby_backend.sgn_show_lobby.connect(lobby_frontend.show)
    lobby_backend.sgn_update_users.connect(lobby_frontend.update_users)
    lobby_backend.sgn_show_invitation.connect(invitation_frontend.show_invitation)
    lobby_backend.sgn_hide_lobby.connect(lobby_frontend.hide)
    lobby_backend.sgn_start_game.connect(game_backend.start_game)

    lobby_frontend.sgn_invite.connect(lobby_backend.invite)

    invitation_frontend.sgn_answer.connect(lobby_backend.invitation_response)

    game_backend.sgn_show_game.connect(game_frontend.show_game)
    game_backend.sgn_update_info.connect(game_frontend.update_info)
    game_backend.sgn_update_marbles.connect(game_frontend.update_marbles)
    game_backend.sgn_show_error.connect(error_frontend.show_error)
    game_backend.sgn_update_turn.connect(game_frontend.update_turn)
    game_backend.sgn_show_oponent_bet.connect(game_frontend.update_oponent_bet)
    game_backend.sgn_delayer_start.connect(game_frontend.start_delayer)
    game_backend.sgn_show_win.connect(game_end_frontend.show_game_end)
    game_backend.sgn_hide_game.connect(game_frontend.hide)
    game_backend.sgn_timers_set_val.connect(game_frontend.sgn_timers_set_val)
    game_backend.sgn_timers_set_max.connect(game_frontend.sgn_timers_set_max)

    game_frontend.sgn_ready.connect(game_backend.click_ready)
    game_frontend.sgn_delayer_tick.connect(game_backend.delayer_stop)
    game_frontend.sgn_cheatcode_fa.connect(game_backend.cheatcode_fa)
    game_frontend.sgn_cheatcode_zx.connect(game_backend.cheatcode_zx)

    game_end_frontend.sgn_play_again.connect(menu_frontend.show)
    game_end_frontend.sgn_reconnect.connect(connect_server)

    menu_backend.server_connection = server_conn
    lobby_backend.server_connection = server_conn
    game_backend.server_connection = server_conn
    game_end_frontend.server_connection = server_conn

    if server_conn:
        menu_frontend.show()
        app.exec_()

        server_conn.send_text("DISCONNECTION")
