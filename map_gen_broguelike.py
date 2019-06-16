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

MAX_ROOM = 40
MAX_ITERATION = 600
MAX_ROOM_PLACEMENT_ITERATION = 20

CORRIDOR = 90
ROOM_IF_NO_CORRIDOR_POSSIBLE = 10
PREVIOUS_ROOM_MAY_BE_ANY_ROOM = 30


class MapGeneratorBrogueLike:
    def __init__(self):
        self.rooms = []
        self.corridors = []
        self.previous_room = None

    def run(self):
        # FIRST ROOM : try to place first room.
        first_room = None
        while not first_room:
            first_room = self.place_room(randint(0, MAP_WIDTH), randint(0, MAP_HEIGHT))
        self.add_room(first_room)

        # STATS -----------------
        nb_iterations = 0
        nb_success = 0
        nb_failure = 0

        # NEW ROOMS ----------------
        while len(self.rooms) < MAX_ROOM and nb_iterations < MAX_ITERATION:
            nb_iterations += 1

            if randint(0, 100) < PREVIOUS_ROOM_MAY_BE_ANY_ROOM:
                self.previous_room = self.rooms[randint(0, len(self.rooms) - 1)]

            # Nous cherchons à placer une nouvelle room. room.
            direction = get_random_direction()
            room = self.place_room(0, 0, self.previous_room, direction)

            # Pas de room possible? Fail et on recommence.
            if not room:
                nb_failure += 1
                continue

            # Pas de corridor à placer? Nous avons une room valide, on peut partir.
            if randint(0, 100) > CORRIDOR:
                self.add_room(room)
                nb_success += 1
                continue

            # CORRIDOR ----------------------------------------------------------
            if not self.place_corridor(direction, room):
                nb_failure += 1
            else:
                nb_success += 1
                continue

        self.show_rooms_on_map()
        print(f'STATS : success {nb_success} - failures {nb_failure} '
              f'- Iterations {nb_iterations} - RoomRequested {len(self.rooms)} / {MAX_ROOM}')

    def place_corridor(self, direction, room):
        # On va tenter de creer un Corridor et une salle au bout
        width, height = 1, 1
        if direction in ['north', 'south']:
            height = room.height
        if direction in ['east', 'west']:
            width = room.width

        corridor = self.place_room(0, 0, self.previous_room, direction)
        if not corridor:    # Peu probable, car on doit pouvoir poser une room pour en arriver là.
            print('ERROR : Corridor should have been created.')
            return False

        # Preparation boucle pour poser le corridor.
        move = get_direction_values(direction)
        step = 1
        max_steps = randint(1, 10)
        corridor_success = False

        while step < max_steps:
            step += 1
            new_x, new_y = move
            corridor.new_position(corridor.x1 + new_x, corridor.y1 + new_y)
            if not self.is_valid_position(corridor):
                corridor.new_position(corridor.x1 - new_x, corridor.y1 - new_y)
                corridor_success = False
                break
            else:
                corridor_success = True

        if corridor_success:
            # We can try to place the room at the end
            room.position_relative_to_other_room_side(corridor, direction)

            if self.is_valid_position(room):
                width, height = 1, 1
                if direction in ['north', 'south']:
                    height = abs(room.y2 - self.previous_room.y2)
                if direction in ['east', 'west']:
                    width = abs(room.x2 - self.previous_room.x2)

                corridor = self.generate_room(0, 0, width, height)
                corridor.char = '+'
                corridor.position_relative_to_other_room_side(self.previous_room, direction)
                self.corridors.append(corridor)
                self.add_room(room)
                return True

        # Si corridor impossible, on peut tjrs placer la salle.
        if randint(0, 100) < ROOM_IF_NO_CORRIDOR_POSSIBLE:
            room.position_relative_to_other_room_side(self.previous_room, direction)
            self.add_room(room)
            corridor = None
            return True
        corridor = None
        return False

    def place_room(self, x, y, width=None, height=None, from_room=None, direction=None):
        iteration = 0
        while iteration < MAX_ROOM_PLACEMENT_ITERATION:
            room = self.generate_room(x, y, width, height)

            if from_room and direction:
                room.position_relative_to_other_room_side(from_room, direction)

            if self.is_valid_position(room):
                return room
            iteration += 1
        return False

    def generate_room(self, x1=0, y1=0, width=None, height=None):
        if not width:
            width = randint(ROOM_MIN_S_W, ROOM_MAX_S_W)
        if not height:
            height = randint(ROOM_MIN_S_H, ROOM_MAX_S_H)
        x2 = width + x1
        y2 = height + y1
        room = Rect(x1, y1, x2, y2)

        return room

    def add_room(self, room):
        self.rooms.append(room)
        self.previous_room = room

    def is_out_of_map(self, room):
        return (room.x1 < 1 or room.x2 > MAP_WIDTH - 1 or
                room.y1 < 1 or room.y2 > MAP_HEIGHT - 1)

    def is_valid_position(self, room_to_validate):
        if self.is_out_of_map(room_to_validate):
            return False

        for room in self.rooms:
            if room_to_validate.intersect(room):
                return False
        return True

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


def get_direction_values(direction):
    direction = direction.lower()
    if direction == 'north':
        move = 0, -1
    elif direction == 'south':
        move = 0, 1
    elif direction == 'west':
        move = -1, 0
    elif direction == 'east':
        move = 1, 0
    else:
        move = 0, 0
    return move


def get_random_direction():
    rand = randint(0, 3)
    directions = ['north', 'east', 'south', 'west']

    return directions[rand]

def main():
    map_gen = MapGeneratorBrogueLike()
    map_gen.run()


if __name__ == '__main__':
    main()


# TODO : Priorité sur la direction selon repartition, passage room to room, corridor like
