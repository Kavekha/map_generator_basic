from random import randint
from game_map import GameMap
from rectangle import Rect


# Sera dans la config de la map?
# Pas vraiment une room creation iteration :
# Ici on limite le nombre de formes de room possible avant d'abandonner le placement. Il faut un autre chapeau.
MAX_ROOM_CREATION_ITERATION = 100
MAX_ROOM_PLACEMENT_ITERATION = 20


class MapGen:
    def __init__(self):
        self.working_map = GameMap()
        self.creation_iteration = 0
        self.room_placement_iteration = 0
        self.rooms = []
        self.current_ref_room = None

    def run(self):
        # stats:
        nb_collisions = 0
        nb_out_of_map = 0
        nb_success = 0
        nb_placement_iterations = 0

        # On place la premiere map au hasard.

        while True:
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
            else:
                # on a notre première map, on la mets sur map de travail. Cela l'ajoute a notre liste aussi.
                self.put_room_on_working_map(room)
                break
        self.show_working_map()

        # Nous avons notre premiere map qui sert de reference. On construit par rapport à elle.

        while self.creation_iteration < MAX_ROOM_CREATION_ITERATION:
            # self.wait()
            print('\n************ {} ******************\n'.format(self.creation_iteration))

            # on créé, on montre.
            room = self.generate_room()
            self.show_room(room)

            # On tente de poser la room autour de l'existante.
            while self.room_placement_iteration < MAX_ROOM_PLACEMENT_ITERATION:
                print('\n!!!! {} / {} !!!!!!!!*\n'.format(self.room_placement_iteration, self.creation_iteration))

                # On prends une position x, y du prochain rectangle autour de la derniere salle de reference.
                x, y = self.get_random_position_around_room(self.current_ref_room)
                room.new_position(x, y)

                # on verifie si pas hors map.
                if self.working_map.out_of_map(room):
                    self.next_placement_iteration()
                    print('>>> OUT OF MAP')
                    nb_out_of_map += 1
                    nb_placement_iterations += 1
                else:
                    # si pas out of map, on mets sur layer.
                    self.put_room_on_layer_map(room)

                    # on regarde si collision
                    if self.working_map.get_collision(room):
                        self.show_working_map()
                        self.delete_layer()
                        self.next_placement_iteration()
                        print('>>>> COLLISION')
                        nb_collisions += 1
                        nb_placement_iterations += 1
                    else:
                        # on peut mettre sur la map de travail.
                        self.put_room_on_working_map(room)
                        self.delete_layer()
                        self.show_working_map()
                        self.next_creation_iteration()
                        nb_success += 1
                        break

            self.reset_placement_iteration()
            self.next_creation_iteration()

        print('\n >> END : Sucess : {} - Collisions : {} - Out of Map : {} - Placement iteration : {}'.format(
            nb_success, nb_collisions, nb_out_of_map, nb_placement_iterations))

    def create_layer(self):
        self.working_map.layer = GameMap()

    def delete_layer(self):
        self.working_map.layer = None

    def wait(self):
        next_iteration = input('Press any key')

    def next_creation_iteration(self):
        self.creation_iteration += 1

    def next_placement_iteration(self):
        self.room_placement_iteration += 1

    def reset_placement_iteration(self):
        self.room_placement_iteration = 0
        self.delete_layer()

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
        self.rooms.append(room)
        self.current_ref_room = room

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

    def get_random_position_around_room(self, room):
        x_or_y = randint(0, 1)
        if x_or_y == 0:
            x = randint(room.x1 - 1, room.x2 + 1)
            neg_or_pos = randint(0, 1)
            if neg_or_pos == 0:
                y = room.y1 - 1
            else:
                y = room.y2 + 1
        else:
            y = randint(room.y1 - 1, room.y2 + 1)
            neg_or_pos = randint(0, 1)
            if neg_or_pos == 0:
                x = room.x1 - 1
            else:
                x = room.x2 + 1

        print('random pos around room : ', x, y)
        print('room : ', room.x1, room.x2, room.y1, room.y2)
        return x, y

if __name__ == '__main__':
    # specs
    ROOM_MIN_S = 3
    ROOM_MAX_S = 8

    map_gen = MapGen()
    map_gen.run()
