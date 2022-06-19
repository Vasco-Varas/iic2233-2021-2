import random


class Car:
    def __init__(self, direc, speed, x_offset, y):
        if direc == 1:
            self.x = -100-x_offset
            self.sprite = "sprites/Mapa/autos/" + random.choice(
                ['amarillo_right', 'azul_right', 'blanco_right', 'morado_right', 'negro_right',
                 'plata_right', 'rojo_right'])
        else:
            self.x = 861+x_offset
            self.sprite = "sprites/Mapa/autos/" + random.choice(
                ['amarillo_left', 'azul_left', 'blanco_left', 'morado_left', 'negro_left',
                 'plata_left', 'rojo_left'])

        self.speed = speed
        self.direc = direc

        self.y = y
        self.designated_label = None
        self.mark_removal = False

    def tick(self):
        self.x += self.speed * self.direc


class Log:
    def __init__(self, direc, speed, x_offset, y):
        if direc == 1:
            self.x = -100-x_offset
        else:
            self.x = 861+x_offset

        self.speed = speed
        self.direc = direc

        self.y = y
        self.designated_label = None
        self.mark_removal = False

    def tick(self):
        self.x += self.speed * self.direc
