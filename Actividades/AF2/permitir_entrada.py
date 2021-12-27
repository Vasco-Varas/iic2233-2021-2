from excepciones_covid import RiesgoCovid


# NO DEBES MODIFICAR ESTA FUNCIÓN
def verificar_sintomas(invitade):
    if invitade.temperatura > 37.5:
        raise RiesgoCovid("fiebre", invitade.nombre)
    elif invitade.tos:
        raise RiesgoCovid("tos", invitade.nombre)
    elif invitade.dolor_cabeza:
        raise RiesgoCovid("dolor_cabeza", invitade.nombre)


def entregar_invitados(diccionario_invitades):
    lista_oficial = []
    for nombre, inst in diccionario_invitades.items():
        try:
            verificar_sintomas(inst)
        except RiesgoCovid as err:
            RiesgoCovid(err.sintoma, err.nombre_invitade).alerta_de_covid()
        else:
            # Debería hacer append() una instancia según el PDF,
            # pero .center() (llamado desde el main.py) es un atributo de strings
            lista_oficial.append(nombre)
    return lista_oficial
