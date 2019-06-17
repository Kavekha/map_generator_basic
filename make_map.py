from tile import Tile

from map_gen_jotaf import MapGeneratorJotaf
from map_gen_consts import *


def make_map(map_config):
    map_width = map_config.get('map_width', MAP_WIDTH)
    map_height = map_config.get('map_height', MAP_HEIGHT)

    tiles = initialize_tiles(map_width, map_height)
    make_indestructible_barriers(tiles, map_width, map_height)

    map_blueprint = get_map_blueprint(map_config)
    rooms, corridors = create_map(tiles, map_blueprint)

    d_created_elements = {'tiles': tiles, 'rooms': rooms, 'corridors': corridors}

    return d_created_elements


def create_map(tiles, map_blueprint):
    rooms = []
    corridors = []

    rooms_to_create = map_blueprint.get('rooms')
    corridors_to_create = map_blueprint.get('corridors')

    for room in rooms_to_create:
        rooms.append(room)
        create_room(tiles, room)

    for corridor in corridors_to_create:
        corridors.append(corridor)
        create_room(tiles, corridor)

    return rooms, corridors


def create_room(tiles, room):
    # go through the tiles in the rectangle and make them passable
    for y in range(room.y1, room.y2):
        for x in range(room.x1, room.x2):
            if is_destructible(tiles, x, y):
                tiles[x][y].blocked = False
                tiles[x][y].block_sight = False


def is_destructible(tiles, x, y):
    if tiles[x][y].destructible:
        return True
    return False


def get_map_blueprint(map_config):
    map_gen = map_config.get('map_algorithm', MapGeneratorJotaf)
    map_gen = map_gen(**map_config)
    map_gen.run()
    results = map_gen.get_results()
    return results


def make_indestructible_barriers(tiles, map_width, map_height):
        for y in range(0, map_height):
            tiles[0][y].destructible = False
            tiles[map_width - 1][y].destructible = False

        for x in range(0, map_width):
            tiles[x][0].destructible = False
            tiles[x][map_height - 1].destructible = False


def initialize_tiles(map_width, map_height):
        tiles = [[Tile(True) for y in range(map_height)] for x in range(map_width)]
        return tiles
