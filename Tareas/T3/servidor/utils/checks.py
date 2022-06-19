
def check_username(username: str):
    return 1 <= len(username) and username.isalnum()


def check_birthday(birthday: str):
    bd = birthday.split("/")
    if len(bd) > 3:
        return "Demaciados '/' en el cumpleaños (dd/mm/yyyy)"
    if len(bd) < 3:
        return "Muy pocos '/' en el cumpleaños (dd/mm/yyyy)"
    if not bd[0].isdigit() or not bd[1].isdigit() or not bd[2].isdigit():
        return "El cumpleaños solo debe contener numeros y '/'"
    if int(bd[0]) == 0:
        return "El cumpleaños no puede ser un dia 0"
    if int(bd[1]) == 0:
        return "El cumpleaños no puede ser un mes 0"
    if int(bd[0]) > 31:
        return "El cumpleaños no puede ser en un dia mayor a 31"
    if int(bd[1]) > 12:
        return "El cumpleaños no puede ser en un mes mayor a 12"
    if len(bd[0]) != 2:
        return "El dia debe ser de 2 digitos (puede partir con 0)"
    if len(bd[1]) != 2:
        return "El mes debe ser de 2 digitos (puede partir con 0)"
    if len(bd[2]) != 4:
        return "El año debe ser de 4 digitos (puede partir con 0)"
    return "ALLOW"
