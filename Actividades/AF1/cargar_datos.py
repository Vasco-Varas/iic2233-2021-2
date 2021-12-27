from mascota import Perro, Gato, Conejo


def cargar_mascotas(archivo_mascotas):

    pet_list = []
    with open(archivo_mascotas, 'r') as f:
        for pet in [ x.split(',') for x in f.read().split('\n')[1:] ]:
            if pet[1] == 'gato':
                pet_list.append(Gato(pet[0], pet[2], pet[3], int(pet[4]), int(pet[5])))
            elif pet[1] == 'perro':
                pet_list.append(Perro(pet[0], pet[2], pet[3], int(pet[4]), int(pet[5])))
            elif pet[1] == 'conejo':
                pet_list.append(Conejo(pet[0], pet[2], pet[3], int(pet[4]), int(pet[5])))
    return pet_list