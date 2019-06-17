from random import randint

from map_gen_base import MapGenBase


# Map generator, based on Jotaf Tutorial.
class MapGeneratorJotaf(MapGenBase):
    def run(self):
        nb_iterations = 0

        while len(self.rooms) < self.max_rooms and nb_iterations < self.max_iterations:

            # determine room attributes.
            width = randint(self.room_min_s_w, self.room_max_s_w)
            height = randint(self.room_min_s_h, self.room_max_s_h)
            x = randint(0, self.map_width - width)
            y = randint(0, self.map_height - height)

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




def main():
    dict_params = {
        'map_width': 80,
        'map_height': 60,
        'room_min_size': 3,
        'room_max_size': 5,
        'max_rooms': 30,
        'max_placement_iterations': 20,
        'max_iterations': 600,
        'corridor_chances': 0,
        'room_if_no_corridor': 0,
        'any_room_may_be_previous': 0
    }

    map_gen = MapGeneratorJotaf(**dict_params)
    map_gen.run()


if __name__ == '__main__':
    main()
