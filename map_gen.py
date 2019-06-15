from random import randint
from rectangle import Rect

MAP_WIDTH = 80
MAP_HEIGHT = 60

ROOM_SIZE_MIN = 5
ROOM_SIZE_MAX = 9

ROOM_MIN_S_W = 7
ROOM_MAX_S_W = 11
ROOM_MIN_S_H = 3
ROOM_MAX_S_H = 5

MAX_ROOM = 30
MAX_ITERATION = 100

PREVIOUS_ROOM_MAY_BE_ANY_ROOM = True
CORRIDOR = True


class MapGenerator:
    def __init__(self):
        self.rooms = []
        self.previous_room = None

    def run(self):
        # On place la première room.
        while not self.rooms:
            room = self.generate_room(randint(0, MAP_WIDTH), randint(0, MAP_HEIGHT))
            if self.is_valid_position(room):
                self.add_room(room)

        # stats
        nb_iterations = 0
        nb_success = 0
        nb_failure = 0

        while len(self.rooms) < MAX_ROOM and nb_iterations < MAX_ITERATION:
            # Nous cherchons à placer la seconde room.
            room = self.generate_room(0, 0)

            direction = self.get_random_direction()
            room.position_relative_to_other_room_side(self.previous_room, direction)

            if self.is_valid_position(room):
                # Add the room as validated.
                self.add_room(room)
                nb_success += 1
            else:
                nb_failure += 1

            nb_iterations += 1
            if PREVIOUS_ROOM_MAY_BE_ANY_ROOM:
                self.previous_room = self.rooms[randint(0, len(self.rooms) - 1)]

        self.show_rooms_on_map()
        print(f'STATS : success {nb_success} - failures {nb_failure} '
              f'- Iterations {nb_iterations} - RoomRequested {MAX_ROOM}')

    def generate_room(self, x1=0, y1=0, width=None, height=None):
        if not width:
            width = randint(ROOM_MIN_S_W, ROOM_MAX_S_W)
        if not height:
            height = randint(ROOM_MIN_S_H, ROOM_MAX_S_H)
        x2 = width + x1
        y2 = height + y1

        room = Rect(x1, y1, x2, y2)

        return room

    def get_direction_values(self, direction):
        direction = direction.lower()
        if direction == 'north':
            return 0, -1
        elif direction == 'south':
            return 0, 1
        elif direction == 'west':
            return -1, 0
        elif direction == 'east':
            return 1, 0
        else:
            return 0, 0

    def add_room(self, room):
        self.rooms.append(room)
        self.previous_room = room

    def is_out_of_map(self, room):
        return (room.x1 < 0 or room.x2 > MAP_WIDTH or
                room.y1 < 0 or room.y2 > MAP_HEIGHT)

    def is_valid_position(self, room_to_validate):
        if self.is_out_of_map(room_to_validate):
            return False

        for room in self.rooms:
            if room_to_validate.intersect(room):
                return False
        return True

    def get_random_direction(self):
        rand = randint(0, 3)
        directions = ['north', 'east', 'south', 'west']

        return directions[rand]

    def show_room(self, room):
        print(room)

    def show_rooms_on_map(self):
        map_to_print = ""
        for y in range(0, MAP_HEIGHT):
            for x in range(0, MAP_WIDTH):
                char_to_add = '.'
                for room in self.rooms:
                    if y in range(room.y1, room.y2) and x in range(room.x1, room.x2):
                        char_to_add = '+'
                        break
                map_to_print += char_to_add
            map_to_print += "\n"

        print(map_to_print)




def main():
    map_gen = MapGenerator()
    map_gen.run()


if __name__ == '__main__':
    main()


# TODO : Priorité sur la direction selon repartition, passage room to room, corridor like




