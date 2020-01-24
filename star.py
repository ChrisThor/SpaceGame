import random
import vector


class Star:
    def __init__(self, size, min_x, min_y, max_x, max_y, colour):
        self.size = size
        self.position = vector.Vector(random.randint(min_x, max_x), random.randint(min_y, max_y))
        self.colour = colour


def create_static_stars(screen_height, screen_width):
    static_stars = []
    amount = int(0.000125 * screen_height * screen_width)
    for i in range(amount):
        static_stars.append(Star(1, 0, 0, screen_width, screen_height, (255, 255, 255)))
    return static_stars


def create_small_stars(screen_height, screen_width):
    min_x = -int(screen_width / 2)
    min_y = -int(screen_height / 2)
    max_x = int(screen_width / 2)
    max_y = int(screen_height / 2)
    amount = int(0.000046875 * screen_height * screen_width)
    small_stars = []
    for i in range(amount):
        small_stars.append(Star(2, min_x, min_y, max_x, max_y, (255, 255, 255)))
    return small_stars


def create_big_stars(screen_height, screen_width):
    min_x = -int(screen_width / 2)
    min_y = -int(screen_height / 2)
    max_x = int(screen_width / 2)
    max_y = int(screen_height / 2)
    amount = int(0.0000234375 * screen_height * screen_width)
    big_stars = []
    for i in range(amount):
        big_stars.append(Star(3, min_x, min_y, max_x, max_y, (255, 255, 255)))
    return big_stars