from random import randint

from rectangle import Rect


MAP_WIDTH = 80
MAP_HEIGHT = 60

ROOM_MIN_S_W = 7
ROOM_MAX_S_W = 11
ROOM_MIN_S_H = 3
ROOM_MAX_S_H = 5

MAX_ROOMS = 30
MAX_PLACEMENT_ITERATIONS = 20
MAX_ITERATIONS = 600

CORRIDOR_CHANCES = 0
ROOM_IF_NO_CORRIDOR = 0
ANY_ROOM_MAY_BE_PREVIOUS = 0


class MapGenBase:
    def __init__(self, **map_params):
        self.map_width = map_params.get('map_width', MAP_WIDTH)
        self.map_height = map_params.get('map_height', MAP_HEIGHT)

        self.room_min_s_w = map_params.get('room_min_s_w', map_params.get('room_min_size', ROOM_MIN_S_W))
        self.room_max_s_w = map_params.get('room_max_s_w', map_params.get('room_max_size', ROOM_MAX_S_W))
        self.room_min_s_h = map_params.get('room_min_s_h', map_params.get('room_min_size', ROOM_MIN_S_H))
        self.room_max_s_h = map_params.get('room_max_s_h', map_params.get('room_max_size', ROOM_MAX_S_H))

        self.max_rooms = map_params.get('max_rooms', MAX_ROOMS)
        self.max_placement_iterations = map_params.get('max_placement_iterations', MAX_PLACEMENT_ITERATIONS)
        self.max_iterations = map_params.get('max_iterations', MAX_ITERATIONS)

        self.corridor_chances = map_params.get('corridor_chances', CORRIDOR_CHANCES)
        self.room_if_no_corridor = map_params.get('room_if_no_corridor', ROOM_IF_NO_CORRIDOR)
        self.any_room_may_be_previous = map_params.get('any_room_may_be_previous', ANY_ROOM_MAY_BE_PREVIOUS)

        self.rooms = []
        self.corridors = []
        self.previous_room = None

    def run(self):
        raise NotImplementedError

    def add_room(self, room):
        self.rooms.append(room)
        self.previous_room = room

    def place_room(self, x, y, width=None, height=None, from_room=None, direction=None, can_intersect=False):
        iteration = 0
        while iteration < self.max_placement_iterations:
            room = self.generate_room(x, y, width, height)

            if from_room and direction:
                room.position_relative_to_other_room_side(from_room, direction)

            if self.is_valid_position(room, can_intersect):
                return room
            iteration += 1
        return False

    def is_out_of_map(self, room):
        return (room.x1 < 1 or room.x2 > self.map_width - 1 or
                room.y1 < 1 or room.y2 > self.map_height - 1)

    def is_valid_position(self, room_to_validate, can_intersect=False):
        if self.is_out_of_map(room_to_validate):
            return False

        if can_intersect:
            return True

        for room in self.rooms:
            if room_to_validate.intersect(room):
                return False
        return True

    def generate_room(self, x1=0, y1=0, width=None, height=None):
        if not width:
            width = randint(self.room_min_s_w, self.room_max_s_w)
        if not height:
            height = randint(self.room_min_s_h, self.room_max_s_h)
        x2 = width + x1
        y2 = height + y1
        room = Rect(x1, y1, x2, y2)

        return room

    def show_rooms_on_map(self):
        map_to_print = ""
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):
                char_to_add = '.'
                for corridor in self.corridors:
                    if y in range(corridor.y1, corridor.y2) and x in range(corridor.x1, corridor.x2):
                        char_to_add = corridor.char
                        break
                for room in self.rooms:
                    if y in range(room.y1, room.y2) and x in range(room.x1, room.x2):
                        char_to_add = room.char
                        break
                map_to_print += char_to_add
            map_to_print += "\n"

        print(map_to_print)

    def get_results(self):
        results = {
            'map_width': self.map_width,
            'map_height': self.map_height,
            'rooms': self.rooms,
            'corridors': self.corridors
        }
        return results
