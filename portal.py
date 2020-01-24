import turnable_space_object
import math
import space_object
import vector


class Portal(turnable_space_object.TurnableSpaceObject):
    def __init__(self, mass, x_speed, y_speed, x_position, y_position, particle_colour, particle_lifetime, diameter,
                 angle=0, show_health_bar=False):
        super().__init__("Portal", mass, 0, x_speed, y_speed, x_position, y_position, particle_colour,
                         particle_lifetime, static=True, show_health_bar=show_health_bar)
        self.teleportable = False
        self.angle = angle
        self.angle_speed = 1
        self.diameter = diameter
        self.linked_portal = None
        self.corner0 = vector.Vector()
        self.corner1 = vector.Vector()
        self.corner2 = vector.Vector()
        self.corner3 = vector.Vector()
        self.calculate_angle()

    def connect_portals(self, other_portal):
        self.linked_portal = other_portal
        other_portal.linked_portal = self

    def get_damage(self, bullet):
        self.teleport(bullet)

    def teleport(self, other: space_object.SpaceObject):
        if other.output_portal is None:
            other.output_portal = self.linked_portal
            speed_angle = get_vector_angle(other.speed)
            scalar = other.speed.norm() * self.angle_vector.norm()
            if scalar > 0:
                other.position = self.linked_portal.position + self.linked_portal.angle_vector * 1.1
            elif scalar < 0:
                speed_angle *= -1
                other.position = self.linked_portal.position + self.linked_portal.angle_vector * -1.1
            angle_difference = self.angle - self.linked_portal.angle
            try:
                other.angle -= angle_difference
            except AttributeError:
                pass
            temp_speed = other.speed.get_length()
            new_speed_y = -round(math.cos(angle_difference + speed_angle + math.pi / 2), 4)
            new_speed_x = -round(math.sin(angle_difference + speed_angle + math.pi / 2), 4)
            other.speed.x_value = temp_speed * new_speed_x
            other.speed.y_value = temp_speed * new_speed_y

    def __add__(self, other):
        self.teleport(other)
        return other

    def turn(self):
        self.corner0 = self.orthogonal_angle_vector * (self.diameter / 2) + self.angle_vector * 0.5
        self.corner1 = self.orthogonal_angle_vector * (self.diameter / 2) + self.angle_vector * -0.5
        self.corner2 = self.orthogonal_angle_vector * (-self.diameter / 2) + self.angle_vector * -0.5
        self.corner3 = self.orthogonal_angle_vector * (-self.diameter / 2) + self.angle_vector * 0.5


def get_vector_angle(v):
    return math.acos(vector.Vector(-1, 0) * v.norm())
