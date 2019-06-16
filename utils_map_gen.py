from random import randint


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
