def verificar_edad(invitade):
    if invitade.edad < 0:
        raise ValueError(f"Error: la edad de {invitade.nombre} es negativa")


def corregir_edad(invitade):
    try:
        verificar_edad(invitade)
    except ValueError as err:
        print(err)
        invitade.edad = -invitade.edad
        print(f"El error en la edad de {invitade.nombre} ha sido corregido")


def verificar_pase_movilidad(invitade):
    if type(invitade.pase_movilidad) is not bool:
        raise TypeError(f"Error: el pase de movilidad de {invitade.nombre} no es un bool")


def corregir_pase_movilidad(invitade):
    try:
        verificar_edad(invitade)
    except TypeError as err:
        print(err)
        invitade.pase_movilidad = True
        print(print(f"El error en el pase de movilidad de {invitade.nombre} ha sido corregido"))


def verificar_mail(invitade):
    if invitade.mail != f"{invitade.nombre}@uc.cl":
        raise ValueError(f"Error: El mail de {invitade.nombre} no está en el formato correcto")


def corregir_mail(invitade):
    try:
        verificar_mail(invitade)
    except ValueError as err:
        print(err)
        invitade.mail = f"{invitade.nombre}@uc.cl"
        print(f"El error en el mail de {invitade.nombre} ha sido corregido")


def dar_alerta_colado(nombre_asistente, diccionario_invitades):
    try:
        asistente = diccionario_invitades[nombre_asistente]
    except KeyError as err:
        print(err)
        print(f"Error: {nombre_asistente} se está intentando colar al carrete")
    else:
        print(f"{asistente.nombre} esta en la lista y tiene edad {asistente.edad}")
