from random import randint


class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    def __repr__(self):
        string = ''
        for y in range(self.y1, self.y2):
            for x in range(self.x1, self.x2):
                string += '#'
            string += '\n'
        return string

    def new_position(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 += x
        self.y2 += y

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y


