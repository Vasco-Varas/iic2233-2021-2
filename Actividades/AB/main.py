from pokemon import (obtener_info_habilidad, obtener_pokemones,
                     obtener_pokemon_mas_alto, obtener_pokemon_mas_rapido,
                     obtener_mejores_atacantes, obtener_pokemones_por_tipo)
from api_curso import info_api_curso, enviar_test


token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2VtYWlsIjoidmFzY28udmFyYXNAdWMuY2wifQ.0f1SzrRBUL3Mt8Dj-oxtdFyAivi5aUznHe0cZODIi44"  # Ingresar tu API Token personal aquí

info_curso = info_api_curso(token)

if not info_curso:
    print("No se pudo obtener la información de la API del curso")
    exit()

url = info_curso["ability"]["url"]

info_habilidad = obtener_info_habilidad(url)
print(f"Result 1: {enviar_test(token, 1, info_habilidad)}")
pokemones = obtener_pokemones(info_habilidad["pokemon"])
print(f"Result 2: {enviar_test(token, 2, pokemones)}")

mas_alto = obtener_pokemon_mas_alto(pokemones)
print(f"Result 3: {enviar_test(token, 3, mas_alto)}")
mas_rapido = obtener_pokemon_mas_rapido(pokemones)
print(f"Result 4: {enviar_test(token, 4, mas_rapido)}")
mejores_atacantes = obtener_mejores_atacantes(pokemones)

print(f"Result 5: {enviar_test(token, 5, mejores_atacantes)}")
pokemones_por_tipo = obtener_pokemones_por_tipo(pokemones)
print(f"Result 6: {enviar_test(token, 6, pokemones_por_tipo)}")

print("Mas alto", mas_alto)
print("Mas rapido", mas_rapido)
print("Mejores atacantes", mejores_atacantes)
print("Pokemones por tipo", pokemones_por_tipo)
