
class SpecialObject:

    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.designated_label = None

    def in_collision(self, x1, y1):
        return self.x > x1 and self.x+40 < x1+80 and self.y > y1 and self.y+40 < x1+80
