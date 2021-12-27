from collections import defaultdict
import requests


def obtener_info_habilidad(url):
    # https://pokeapi.co/api/v2/ability/{id or name}
    d = requests.get(url).json()
    name = d["name"]
    for entry in d["effect_entries"]:
        if entry["language"]["name"] == "en":
            effect_entries = entry["short_effect"]

    pokemon = list(map(lambda x: x["pokemon"], d["pokemon"]))
    return {"name":name, "effect_entries":effect_entries, "pokemon":pokemon}


def obtener_pokemones(pokemones):
    p_list = []
    for poke in pokemones:
        poke_info = requests.get(poke["url"]).json()
        p_id = poke_info["id"]
        p_name = poke_info["name"]
        p_height = poke_info["height"]
        p_weight = poke_info["weight"]
        p_stats = {st["stat"]["name"]: {"base_stat": st["base_stat"], "effort": st["effort"]} for st
                   in poke_info["stats"]}
        p_types = list(map(lambda x: x["type"]["name"], poke_info["types"]))
        p_dict = {
            "id": p_id,
            "name": p_name,
            "height": p_height,
            "weight": p_weight,
            "stats": p_stats,
            "types": p_types
        }
        p_list.append(p_dict)
    return p_list


def obtener_pokemon_mas_alto(pokemones):
    return sorted(pokemones, key=lambda x: x["height"], reverse=True)[0]["name"]


def obtener_pokemon_mas_rapido(pokemones):
    return sorted(pokemones, key=lambda x: x["stats"]["speed"]["base_stat"] if "speed" in x["stats"] else 0, reverse=True)[0]["name"]


def obtener_mejores_atacantes(pokemones):
    allow_poke = filter(lambda x: "attack" in x["stats"] and "defense" in x["stats"], pokemones)
    return sorted(allow_poke, key=lambda x: x["stats"]["attack"]["base_stat"]/x["stats"]["defense"]["base_stat"], reverse=True)[:5]
    #return list(map(lambda x: {"name": x["name"], "attack": x["stats"]["attack"]["base_stat"], "defense": x["stats"]["defense"]["base_stat"]}, srt))


def obtener_pokemones_por_tipo(pokemones):
    types = []
    for poke in pokemones:
        types.extend(poke["types"])
    types = list(set(types))

    type_dict = {}
    for p_type in types:
        type_dict[p_type] = list(map(lambda x: x["name"], filter(lambda x: p_type in x["types"], pokemones)))
    return type_dict