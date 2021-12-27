import requests


def info_api_curso(token):
    response = requests.get(f"https://www.avanzada.ml/api/v2/bonus/ability?api_token={token}")
    if response:
        return response.json()
    return {}


tests = [
    "obtener_info_habilidad",
    "obtener_info_pokemon",
    "obtener_pokemon_mas_alto",
    "obtener_pokemon_mas_rapido",
    "obtener_mejores_atacantes",
    "obtener_pokemones_por_tipo"
]


def enviar_test(token, test_id, respuesta):

    data = {
        "test": {
            "function_name": tests[test_id-1],
            "function_response": respuesta
        }
    }

    ans = requests.post(f"https://www.avanzada.ml/api/v2/bonus/tests/{test_id}?api_token={token}", json=data).json()
    return ans["result"] == "success"
