import tcod as libtcod


from make_map import make_map
from map_gen_consts import *


map_config = {
        'map_width': 80,
        'map_height': 60,
        'room_min_size': 3,
        'room_max_size': 5,
        'max_rooms': 30,
        'max_placement_iterations': 20,
        'max_iterations': 600,
        'corridor_chances': 0,
        'room_if_no_corridor': 0,
        'any_room_may_be_previous': 0,
        "min_mobs": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
        "max_mob_room": [[10, 1], [11, 2], [13, 4], [15, 6], [17, 8], [20, 10]],
        "colors": {
            "dark_wall": libtcod.Color(0, 0, 100),
            "dark_ground": libtcod.Color(50, 50, 150),
            "light_wall": libtcod.Color(130, 110, 50),
            "light_ground": libtcod.Color(200, 180, 50),
        }
    }


class GameMap:
    """
    gère la creation de la map et son contenu, ainsi que sa mise à jour.
    """

    def __init__(self, map_config):
        self.spawner = None

        self.tiles = None
        self.fov_map = None
        self.map_width = None
        self.map_height = None
        self.colors = None

        self._entities = []
        self._player = None
        self._items = []
        self._fighters = []
        self._rooms = []
        self._corridors = []

    def generate_map(self):
        # get config
        # map_config = get_map_config(self.map_type)

        self.map_width = map_config.get('map_width', MAP_WIDTH)
        self.map_height = map_config.get('map_height', MAP_HEIGHT)

        self.colors = map_config.get('colors')

        map_elements = make_map(map_config)
        self.tiles = map_elements.get('tiles', False)
        self._rooms = map_elements.get('rooms', False)
        self._corridors = map_elements.get('corridors')

        self._player.x, self._player.y = self._rooms[0].center
        # self.fov_map = initialize_fov(self)

        # place stairs
        # place monsters and items.

