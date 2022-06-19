import datetime
import sys

MAX_CARACTERES = 8
MIN_CARACTERES = 3


class DCCCache:
    def __init__(self):
        self.user = None  # The currently logged in user (None for anonymous)
        self.curMenu = MenuLoginMenu()  # The current menu
        self.curPub = None  # The last viewing publication


class MenuElement:
    def __init__(self):
        self.header = "--- ¡Bienvenid@s a DCCommerce! ---"
        self.text = ""
        self.footer = "Indique su opción: "

        self.options = []  # list of (displayText, ValidationFunction, ActionFunction)

    def action(self):
        print(self.header)
        print(self.text)

        idx = 0
        for element in self.options.copy():
            if element[1]():  # element[1] is the ValidationFunction
                print(f"[{idx + 1}] {element[0]}")
                idx += 1
            else:
                self.options.pop(idx)

        key = input(self.footer)
        while not key.isdigit() or int(key) > len(self.options) or int(key) < 1:
            print(f"Por favor seleccione un numero entre 1-{len(self.options)}")
            key = input(self.footer)

        numeric_key = int(key) - 1

        # Call the function corresponding to the key-based index
        self.options[numeric_key][2](numeric_key)


class MenuLoginMenu(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu Inicio ***

Selecciona una opción:
'''

    def refresh(self, cache: DCCCache):

        def _check_login(key_idx):
            username = input("Nombre de usuario: ")
            with open("usuarios.csv", 'r', encoding="utf-8") as f:
                users = f.read().split("\n")[1:]
                if username in users:
                    cache.curMenu = MenuMainMenu()
                    cache.user = username
                else:
                    print("Usuario no registrado")

        def _register(key_idx):
            username = input("Nombre de usuario: ")
            users = None
            with open("usuarios.csv", 'r', encoding="utf-8") as f:
                users = f.read().split("\n")[1:]

            if len(username) > MAX_CARACTERES or len(
                    username) < MIN_CARACTERES or ',' in username or username in users:
                if username in users:
                    print("Ya existe un usuario con ese nombre")
                else:
                    print(f"El nombre de usuario debe tener entre"
                          f"{MIN_CARACTERES}-{MAX_CARACTERES} caracteres y no debe contener commas")
                return

            users.append(username)

            with open("usuarios.csv", 'w', encoding="utf-8") as f:
                f.write("usuario\n" + '\n'.join(users))

        def _login_anonymous(key_idx):
            cache.user = None
            cache.curMenu = MenuMainMenu()

        self.options = [
            ("Ingresar sesión", lambda: True, _check_login),
            ("Registrar usuario", lambda: True, _register),
            ("Ingresar como usuario anónimo", lambda: True, _login_anonymous),
            ("Salir", lambda: True, lambda x: sys.exit(0))
        ]

        self.action()


class MenuMainMenu(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu Principal ***
'''

    def refresh(self, cache: DCCCache):
        def _back(key_idx):
            cache.curMenu = MenuLoginMenu()

        def _menu_pub(key_idx):
            cache.curMenu = MenuPubMenu()

        def _menu_pub_made(key_idx):
            cache.curMenu = MenuPubMadeMenu()

        self.options = [
            ("Menú de Publicaciones", lambda: True, _menu_pub),
            ("Menú de Publicaciones Realizadas", lambda: cache.user is not None, _menu_pub_made),
            ("Volver", lambda: True, _back)
        ]

        self.action()


class MenuPubMenu(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu de Publicaciones ***
'''

    def refresh(self, cache: DCCCache):
        def _enter_pub(key_idx):
            cache.curPub = key_idx + 1
            cache.curMenu = MenuPub()

        def _back(key_idx):
            cache.curMenu = MenuMainMenu()

        self.options = []
        pubs = None
        with open("publicaciones.csv", 'r', encoding="utf-8") as f:
            pubs = [x.split(",") for x in f.read().split("\n")][1:]  # Pub list on listArray

        # No es necesario ordenar las publicaciones por fecha y hora, ya que en el
        # archivo se agregan en ese orden

        for idx, element in enumerate(pubs):
            self.options.append((element[1], lambda: True, _enter_pub))

        self.options.append(("Volver", lambda: True, _back))

        self.action()


class MenuPub(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu de Publicaciones ***
'''

    def refresh(self, cache: DCCCache):
        with open("publicaciones.csv", 'r', encoding="utf-8") as f:
            pub = [x.split(",") for x in f.read().split("\n")][cache.curPub]

        comment = ','.join(pub[5:])

        self.text = f'''
*** {pub[1]} ***

Creado: {pub[3]}
Vendedor: {pub[2]}
Precio: {pub[4]}
Descripción: {comment}

Comentarios de la publicación:
'''

        pub_id = 0
        with open("comentarios.csv", 'r', encoding="utf-8") as f:
            with open("publicaciones.csv", 'r', encoding="utf-8") as pub_file:
                pub_id = [x.split(",") for x in pub_file.read().split("\n")][cache.curPub][0]

            comments = filter(lambda x: int(x[0]) == int(pub_id),
                              [x.split(",") for x in f.read().split("\n")][1:])

            # No es necesario ordenar los comentarios por fecha y hora
            # ya que en el archivo están en ese orden

            for comment in comments:
                self.text += f"{comment[2]} -- {comment[1]}: {','.join(comment[3:])}\n"

        def _back(key_idx):
            cache.curMenu = MenuPubMenu()

        def _add_comment(key_idx):
            date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            content = input("Ingrese comentario: ")
            with open("comentarios.csv", 'a', encoding="utf-8") as comment_file:
                comment_file.write(f"\n{pub_id},{cache.user},{date},{content}")

        self.options = [
            ("Agregar comentario", lambda: cache.user is not None, _add_comment),
            ("Volver", lambda: True, _back)
        ]

        self.action()


class MenuPubMadeMenu(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu Principal ***
'''

    def refresh(self, cache: DCCCache):
        self.text = f'''
*** Menú de Publicaciones Realizadas ***

Mis publicaciones:
'''

        with open("publicaciones.csv", 'r', encoding="utf-8") as f:
            # Pub list on listArray
            pubs = filter(lambda x: x[2] == cache.user,
                          [x.split(",") for x in f.read().split("\n")][1:])

            for pub in pubs:
                self.text += f"- {pub[1]}\n"

        def _new_pub(key_idx):
            pub_name = input("Nombre de la publicación: ")
            if ',' in pub_name:
                print("El nombre no puede contener comas")
                return
            pub_price = input("Precio de la publicación: ")
            if not pub_price.isdigit():
                print("El precio debe ser un numero")
                return
            pub_desc = input("Descripción de la publicación: ")
            pub_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            pub_id = 0
            with open("publicaciones.csv", 'r', encoding="utf-8") as pub_file:
                pub_id = max([int(x.split(",")[0]) for x in pub_file.read().split("\n")[1:]]) + 1

            with open("publicaciones.csv", 'a', encoding="utf-8") as pub_file:
                pub_file.write(
                    f"\n{pub_id},{pub_name},{cache.user},{pub_date},{pub_price},{pub_desc}")

        def _del_pub(key_idx):
            cache.curMenu = MenuDelPubMenu()

        def _back(key_idx):
            cache.curMenu = MenuMainMenu()

        self.options = [
            ("Crear nueva publicación", lambda: True, _new_pub),
            ("Eliminar publicación", lambda: True, _del_pub),
            ("Volver", lambda: True, _back)
        ]

        self.action()


class MenuDelPubMenu(MenuElement):
    def __init__(self):
        super().__init__()  # Call the MenuElement initialization function
        self.text = '''
*** Menu Principal ***
'''

    def refresh(self, cache: DCCCache):
        self.text = f'''
¿Cuál publicación deseas eliminar?:
'''
        self.options = []

        def _del_pub(key_idx):
            pub_id = -1
            write_buffer = ""
            with open("publicaciones.csv", 'r', encoding="utf-8") as f:
                table = [x.split(",") for x in f.read().split("\n")][1:]
                pub_id = list(filter(lambda x: x[2] == cache.user, table))[key_idx][0]

                new_table = filter(lambda x: x[0] != pub_id, table)
                write_buffer = '\n'.join([','.join(x) for x in new_table])

                comments = None
                with open("comentarios.csv", 'r', encoding="utf-8") as com_file:
                    comment_table = [x.split(",") for x in com_file.read().split("\n")][1:]
                    comments = list(filter(lambda x: x[0] != pub_id, comment_table))
                with open("comentarios.csv", 'w', encoding="utf-8") as com_file:
                    comment_list = [','.join(x) for x in comments]
                    comment_buffer = 'id_publicacion,usuario,fecha_emision,contenido\n'
                    comment_buffer += '\n'.join(comment_list)
                    com_file.write(comment_buffer)

            write_buffer = f"id_publicacion,nombre_publicacion," \
                           f"usuario,fecha_creacion,precio,descripcion\n" \
                           f"{write_buffer}"
            with open("publicaciones.csv", 'w', encoding="utf-8") as pub_file:
                pub_file.write(write_buffer)

        def _back(key_idx):
            cache.curMenu = MenuPubMadeMenu()

        with open("publicaciones.csv", 'r', encoding="utf-8") as f:
            pubs = filter(lambda x: x[2] == cache.user,
                          [x.split(",") for x in f.read().split("\n")][1:])

            for pub in pubs:
                self.options.append((f"{pub[1]} -- Creado el {pub[3]}", lambda: True, _del_pub))

        self.options.append(("Volver", lambda: True, _back))

        self.action()


def main():
    cache = DCCCache()

    while True:
        cache.curMenu.refresh(cache)


if __name__ == '__main__':
    main()
