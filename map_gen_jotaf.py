from random import randint
from rectangle import Rect


MAP_WIDTH = 80
MAP_HEIGHT = 60

ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 7

MAX_ROOMS = 30
MAX_ITERATIONS = 600

MAX_ROOM_PLACEMENT_ITERATION = 20


# Map generator, based on Jotaf Tutorial.
class MapGeneratorJotaf:
    def __init__(self):
        self.rooms = []
        self.corridors = []
        self.previous_room = None

    def run(self):
        nb_iterations = 0

        while len(self.rooms) < MAX_ROOMS and nb_iterations < MAX_ITERATIONS:

            # determine room attributes.
            width = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            height = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = randint(0, MAP_WIDTH - width)
            y = randint(0, MAP_HEIGHT - height)

            # create and try to place room. False if cant do, Room return if success.
            room = self.place_room(x, y, width, height)
            if not room:
                continue

            # link room to previous room.
            if self.previous_room and self.previous_room != room:
                prev_x, prev_y = self.previous_room.center
                new_x, new_y = room.center

                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    tunnel_h = self.create_h_tunnel(prev_x, new_x, prev_y)
                    tunnel_v = self.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    tunnel_v = self.create_v_tunnel(prev_y, new_y, new_x)
                    tunnel_h = self.create_h_tunnel(prev_x, new_x, prev_y)

                if tunnel_h and tunnel_v:
                    tunnel_h.char = '+'
                    tunnel_v.char = '+'
                    self.corridors.append(tunnel_v)
                    self.corridors.append(tunnel_h)
                else:
                    continue

            self.add_room(room)
        self.show_rooms_on_map()

    def create_h_tunnel(self, x1, x2, y):
        return self.place_room(x1, y, x2, 1, can_intersect=True)

    def create_v_tunnel(self, y1, y2, x):
        return self.place_room(x, y1, 1, y2, can_intersect=True)

    def show_rooms_on_map(self):
        map_to_print = ""
        for y in range(0, MAP_HEIGHT):
            for x in range(0, MAP_WIDTH):
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

    def add_room(self, room):
        self.rooms.append(room)
        self.previous_room = room

    def place_room(self, x, y, width=None, height=None, from_room=None, direction=None, can_intersect=False):
        iteration = 0
        while iteration < MAX_ROOM_PLACEMENT_ITERATION:
            room = self.generate_room(x, y, width, height)

            if from_room and direction:
                room.position_relative_to_other_room_side(from_room, direction)

            if self.is_valid_position(room, can_intersect):
                return room
            iteration += 1
        return False

    def is_out_of_map(self, room):
        return (room.x1 < 1 or room.x2 > MAP_WIDTH - 1 or
                room.y1 < 1 or room.y2 > MAP_HEIGHT - 1)

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
            width = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        if not height:
            height = randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x2 = width + x1
        y2 = height + y1
        room = Rect(x1, y1, x2, y2)

        return room


def main():
    map_gen = MapGeneratorJotaf()
    map_gen.run()


if __name__ == '__main__':
    main()
