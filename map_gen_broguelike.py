from random import randint

from utils_map_gen import get_direction_values, get_random_direction
from map_gen_base import MapGenBase


class MapGeneratorBrogueLike(MapGenBase):
    def run(self):
        # FIRST ROOM : try to place first room.
        first_room = None
        while not first_room:
            first_room = self.place_room(randint(0, self.map_width), randint(0, self.map_height))
        self.add_room(first_room)

        # STATS -----------------
        nb_iterations = 0
        nb_success = 0
        nb_failure = 0

        # NEW ROOMS ----------------
        while len(self.rooms) < self.max_rooms and nb_iterations < self.max_iterations:
            nb_iterations += 1

            if randint(0, 100) < self.any_room_may_be_previous:
                self.previous_room = self.rooms[randint(0, len(self.rooms) - 1)]

            # Nous cherchons à placer une nouvelle room. room.
            direction = get_random_direction()
            room = self.place_room(0, 0, from_room=self.previous_room, direction=direction)

            # Pas de room possible? Fail et on recommence.
            if not room:
                nb_failure += 1
                continue

            # Pas de corridor à placer? Nous avons une room valide, on peut partir.
            if not randint(0, 100) < self.corridor_chances:
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
              f'- Iterations {nb_iterations} - RoomRequested {len(self.rooms)} / {self.max_rooms}')

    def place_corridor(self, direction, room):
        # On va tenter de creer un Corridor et une salle au bout
        width, height = 1, 1
        if direction in ['north', 'south']:
            height = room.height
        if direction in ['east', 'west']:
            width = room.width

        corridor = self.place_room(0, 0, from_room=self.previous_room, direction=direction)
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
        if randint(0, 100) < self.room_if_no_corridor:
            room.position_relative_to_other_room_side(self.previous_room, direction)
            self.add_room(room)
            corridor = None
            return True
        corridor = None
        return False


def main():
    dict_params = {
        'map_width': 80,
        'map_height': 60,
        'room_min_s_w': 7,
        'room_max_s_w': 11,
        'room_min_s_h': 3,
        'room_max_s_h': 5,
        'max_rooms': 40,
        'max_placement_iterations': 20,
        'max_iterations': 600,
        'corridor_chances': 90,
        'room_if_no_corridor': 10,
        'any_room_may_be_previous': 20
    }

    map_gen = MapGeneratorBrogueLike(**dict_params)
    map_gen.run()


if __name__ == '__main__':
    main()


# TODO : Priorité sur la direction selon repartition, passage room to room, corridor like
