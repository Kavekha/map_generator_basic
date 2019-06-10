from tile import Tile


class GameMap:
    def __init__(self):
        self.height = 50
        self.width = 80
        self.tiles = self.init_tiles()
        self.layer = None

    def init_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def add_layer(self, layer):
        self.layer = layer

    def get_collision(self, room):
        for y in range(room.y1, room.y2):
            for x in range(room.x1, room.x2):
                if self.tiles[x][y].assigned:
                    print('collision')
                    return True
        print('no collision')
        return False

    def __repr__(self):
        string = ''
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.layer and self.layer.tiles[x][y].assigned:
                    string += '-'
                elif self.tiles[x][y].assigned:
                    string += '+'
                else:
                    string += '.'
            string += '\n'
        return string

    def out_of_map(self, room):
        if room.x1 < 0 or room.x1 > self.width:
            return True
        if room.x2 < 0 or room.x2 > self.width:
            return True
        if room.y1 < 0 or room.y1 > self.height:
            return True
        if room.y2 < 0 or room.y2 > self.height:
            return True
        return False