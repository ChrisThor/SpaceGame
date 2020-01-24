class Particle:
    def __init__(self, colour, position, speed, lifetime, space_object, size, vanishable=True):
        """
        :param colour:      The colour of the particle
        :param position:    Its starting position
        :param speed:       The particle's speed is a vector
        :param lifetime:    must be given in seconds
        :param space_object: The object that produced this particle
        :param size:        in pixels
        """
        self.space_object = space_object
        self.ticks = 0
        self.size = size
        self.max_size = size
        self.colour = colour
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.position = position
        self.speed = speed
        self.show = False
        self.vanishable = vanishable
        self.vanished = False

    def tick(self, tickrate):
        self.lifetime -= tickrate
        self.ticks += tickrate
        try:
            if self.ticks > self.max_lifetime / 10:
                self.ticks = 0
                self.size -= self.max_size * .05
        except ZeroDivisionError:
            self.size -= self.max_size * .1

    def move(self, tickrate):
        self.position += self.speed * tickrate

    def is_on_screen(self, screen_width, screen_height, pos_x_on_screen, pos_y_on_screen):
        if self.size <= pos_x_on_screen <= screen_width + self.size:
            if -self.size <= pos_y_on_screen <= screen_height + self.size:
                return True
        return False
