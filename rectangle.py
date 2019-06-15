class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self):
        return abs(self.x2 - self.x1)

    @property
    def height(self):
        return abs(self.y2 - self.y1)

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def north(self):
        return (self.x1 + self.x2) // 2, self.y1

    @property
    def south(self):
        return (self.x1 + self.x2) // 2, self.y2

    @property
    def west(self):
        return self.x1, (self.y1 + self.y2) // 2

    @property
    def east(self):
        return self.x2, (self.y1 + self.y2) // 2

    def intersect(self, other):
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)

    def new_position(self, x, y):
        width = self.width
        height = self.height
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def position_relative_to_other_room_side(self, room, side='north'):
        side = side.lower()
        x, y = room.center
        if side == 'north':
            x, y = room.north
            # y -= 1
            y -= self.height
            x -= self.width // 2
        elif side == 'south':
            x, y = room.south
            # y += 1
            x -= self.width // 2
        elif side == 'west':
            x, y = room.west
            # x -= 1
            x -= self.width
            y -= self.height // 2
        elif side == 'east':
            x, y = room.east
            # x += 1
            y -= self.height // 2
        self.new_position(x, y)

    def __repr__(self):
        string = ""
        for y in range(self.y1, self.y2):
            for x in range(self.x1, self.x2):
                string += "#"
            string += "\n"
        return string




