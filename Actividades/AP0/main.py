# Debes completar esta función para que retorne la información de los ayudantes
def cargar_datos(path):
    with open(path, "r") as f:
        return [x.split(",") for x in f.read().split("\n")]


# Completa esta función para encontrar la información del ayudante entregado
def buscar_info_ayudante(nombre_ayudante, lista_ayudantes):
    return list(filter(lambda x: x[0].lower() == nombre_ayudante.lower(), lista_ayudantes))[0]


# Completa esta función para que los ayudnates puedan saludar
def saludar_ayudante(info_ayudante):

    return(f"{info_ayudante[0]} ({info_ayudante[1]}): Hola, soy {info_ayudante[0]}, me puedes contactar por discord @ {info_ayudante[3]} y puedes ver mi portafolio en github @ {info_ayudante[2]}")


if __name__ == '__main__':
    pass
    # print(saludar_ayudante(buscar_info_ayudante("Christian Klempau", cargar_datos("ayudantes.csv"))))

    # El código que aquí escribas se ejecutará solo al llamar a este módulo.
    # Aquí puedes probar tu código llamando a las funciones definidas.

    # Puede llamar a cargar_datos con el path del archivo 'ayudantes.csv'
    # para probar si obtiene bien los datos.

    # Puedes intentar buscar la lista de unos de los nombres
    # que se encuentran en el archivo con la función buscar_info_ayudante.
    # Además puedes utilizar la lista obtenida para generar su saludo.

    # Hint: la función print puede se útil para revisar
    #       lo que se está retornando.