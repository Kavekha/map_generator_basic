from random import randint
from game_map import GameMap
from rectangle import Rect


# Sera dans la config de la map?
# Pas vraiment une room creation iteration :
# Ici on limite le nombre de formes de room possible avant d'abandonner le placement. Il faut un autre chapeau.
MAX_ROOM_CREATION_ITERATION = 50
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
            x = int(self.working_map.width / 2)
            y = int(self.working_map.height / 2)
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

            # On choisi un emplacement cardinal au hasard autour de la dernière room de reference.
            starting_direction = randint(0, 7)
            first_direction = starting_direction
            print('First direction is ', first_direction)

            # On tente de poser la room autour de l'existante.
            while self.room_placement_iteration < MAX_ROOM_PLACEMENT_ITERATION:
                print('\n!!!! {} / {} !!!!!!!!*\n'.format(self.room_placement_iteration, self.creation_iteration))

                # on créé, on montre.
                # corridor
                corridor = self.generate_room()
                corridor.corridor = True
                self.show_room(corridor)
                # On prends une position x, y du prochain rectangle autour de la derniere salle de reference.
                x, y = self.get_random_position_around_room(self.current_ref_room, corridor, starting_direction)
                corridor.new_position(x, y)

                room = self.generate_room()
                self.show_room(room)
                x, y = self.get_random_position_around_room(corridor, room, starting_direction)
                room.new_position(x, y)

                print('current starting direction = ', starting_direction)

                # on verifie si pas hors map.
                if self.working_map.out_of_map(room):

                    # on change la direction suivante
                    starting_direction += 1
                    if starting_direction > 7:
                        starting_direction = 0

                    self.next_placement_iteration()
                    print('>>> OUT OF MAP')
                    nb_out_of_map += 1
                    nb_placement_iterations += 1
                else:
                    # si pas out of map, on mets sur layer.
                    self.put_room_on_layer_map(corridor)
                    self.put_room_on_layer_map(room)

                    # on regarde si collision
                    if self.working_map.get_collision(room) or self.working_map.get_collision(corridor):
                        self.show_working_map()
                        self.delete_layer()

                        # on change la direction suivante
                        starting_direction += 1
                        if starting_direction > 7:
                            starting_direction = 0
                        # si on a fait le tour complet, on arrete
                        if starting_direction == first_direction:
                            break

                        self.next_placement_iteration()
                        print('>>>> COLLISION')
                        nb_collisions += 1
                        nb_placement_iterations += 1
                    else:
                        # on peut mettre sur la map de travail.
                        self.put_room_on_working_map(corridor)
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
        x2 = randint(ROOM_MIN_S_W, ROOM_MAX_S_W)
        y2 = randint(ROOM_MIN_S_H, ROOM_MAX_S_H)
        room = Rect(x1, y1, x2, y2)
        return room

    def generate_corridor(self, room, direction):
        x1, y1 = 0, 0
        x2 = randint(CORRIDOR_MIN_S_W, CORRIDOR_MAX_S_W)
        y2 = randint(CORRIDOR_MIN_S_H, CORRIDOR_MAX_S_H)
        corridor = Rect(x1, y1, x2, y2)
        corridor.corridor = True
        return corridor


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

    def carve_room(self, room, gmap):
        for y in range(max(0, room.y1), min(room.y2, gmap.height)):
            for x in range(max(0, room.x1), min(room.x2, gmap.width)):
                if room.corridor:
                    gmap.tiles[x][y].corridor = True
                gmap.tiles[x][y].assigned = True


    def get_random_position_around_room(self, ref_room, new_room, starting_direction):
        x, y = ref_room.center
        random = starting_direction
        if random == 0:
            # West
            x -= new_room.width
            x -= int(ref_room.width / 2)
        elif random == 1:
            # North
            y -= new_room.height
            y -= int(ref_room.height / 2)
        elif random == 2:
            # East
            x += int(ref_room.width / 2)
            if ref_room.width % 2 != 0:
                x += 1
        elif random == 3:
            # south
            y += int(ref_room.height / 2)
            if ref_room.height % 2 != 0:
                y += 1
        elif random == 4:
            # south West
            y += int(ref_room.height / 2)
            if ref_room.height % 2 != 0:
                y += 1
            x -= new_room.width
            x -= int(ref_room.width / 2)
        elif random == 5:
            # north West
            y -= new_room.height
            y -= int(ref_room.height / 2)
            x -= new_room.width
            x -= int(ref_room.width / 2)
        elif random == 6:
            # North East
            y -= new_room.height
            y -= int(ref_room.height / 2)
            x += int(ref_room.width / 2)
        elif random == 7:
            # South East
            y += int(ref_room.height / 2)
            x += int(ref_room.width / 2)

        return x, y

    def old_get_random_position_around_room(self, room):
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
    ROOM_MIN_S_W = 5
    ROOM_MAX_S_W = 9
    ROOM_MIN_S_H = 3
    ROOM_MAX_S_H = 7

    CORRIDOR_MIN_S_W = 3
    CORRIDOR_MAX_S_W = 5
    CORRIDOR_MIN_S_H = 3
    CORRIDOR_MAX_S_H = 5

    map_gen = MapGen()
    map_gen.run()
