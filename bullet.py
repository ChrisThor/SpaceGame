import space_object


class Bullet(space_object.SpaceObject):
    def __init__(self, radius, mass, position, speed, damage, name, particle_colour, particle_lifetime, lifetime="INF"):
        super().__init__(name, mass, radius, speed.x_value, speed.y_value, position.x_value, position.y_value,
                         particle_colour, particle_lifetime, lifetime)
        self.damage = damage
