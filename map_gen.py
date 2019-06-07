from random import randint
from game_map import GameMap
from rectangle import Rect


class MapGen:
    def __init__(self):
        self.working_map = GameMap()
        self.current_iteration = 0
        self.max_room_iteration = 100

    def run(self):
        # stats:
        nb_collisions = 0
        nb_out_of_map = 0
        nb_success = 0

        while self.current_iteration < self.max_room_iteration:

            # self.wait()
            print('\n************ {} ******************\n'.format(self.current_iteration))
            # on créé, on montre.
            room = self.generate_room()
            self.show_room(room)

            # On choisi un point au hasard
            x = randint(0, self.working_map.width)
            y = randint(0, self.working_map.height)
            room.new_position(x, y)

            # on regarde si position dans la map.
            if self.working_map.out_of_map(room):
                print('>>> OUT OF MAP')
                nb_out_of_map += 1
                self.next_iteration()
            else:
                # si pas out of map, on mets sur layer.
                self.put_room_on_layer_map(room)

                # on regarde si collision
                if self.working_map.get_collision(room):
                    print('>>>> COLLISION')
                    nb_collisions += 1
                    self.show_working_map()
                    self.delete_layer()
                    self.next_iteration()
                else:
                    # on peut mettre sur la map de travail.
                    self.put_room_on_working_map(room)
                    self.delete_layer()
                    self.show_working_map()
                    nb_success += 1
                    self.current_iteration += 1
        print('\n >> END : Sucess : {} - Collisions : {} - Out of Map : {} - TOTAL : {}'.format(
            nb_success, nb_collisions, nb_out_of_map, nb_out_of_map + nb_collisions + nb_success))

    def create_layer(self):
        self.working_map.layer = GameMap()

    def delete_layer(self):
        self.working_map.layer = None

    def wait(self):
        next_iteration = input('Press any key')

    def next_iteration(self):
        self.current_iteration += 1

    def generate_room(self):
        x1, y1 = 0, 0
        x2 = self.get_random_min_max_room_size()
        y2 = self.get_random_min_max_room_size()
        room = Rect(x1, y1, x2, y2)
        return room

    def put_room_on_layer_map(self, room):
        if not self.working_map.layer:
            self.create_layer()
        self.carve_room(room, self.working_map.layer)

    def put_room_on_working_map(self, room):
        self.carve_room(room, self.working_map)

    def show_working_map(self):
        print(self.working_map)

    def show_room(self, room):
        print(room)

    def carve_room(self, room, map):
        for y in range(max(0, room.y1), min(room.y2, map.height)):
            for x in range(max(0, room.x1), min(room.x2, map.width)):
                map.tiles[x][y].assigned = True

    def get_random_min_max_room_size(self):
        x = randint(ROOM_MIN_S, ROOM_MAX_S)
        return x


if __name__ == '__main__':
    # specs
    ROOM_MIN_S = 3
    ROOM_MAX_S = 8

    map_gen = MapGen()
    map_gen.run()
