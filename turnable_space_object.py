import space_object
import vector
import math


class TurnableSpaceObject(space_object.SpaceObject):
    def __init__(self, name, mass, radius, x_speed, y_speed, x_position, y_position, particle_colour,
                 particle_lifetime, hp=1, static=False, show_health_bar=True):
        super().__init__(name, mass, radius, x_speed, y_speed, x_position, y_position, particle_colour,
                         particle_lifetime, hp=hp, static=static, show_health_bar=show_health_bar)
        self.angle = -math.pi / 2
        self.angle_speed = 0
        self.angle_vector = vector.Vector(0, -1)
        self.orthogonal_angle_vector = vector.Vector(1, 0)

    def calculate_angle_x(self):
        self.angle_vector.x_value = round(math.cos(self.angle), 4)
        self.orthogonal_angle_vector.x_value = round(math.cos(self.angle - math.pi / 2), 4)

    def calculate_angle_y(self):
        self.angle_vector.y_value = round(math.sin(self.angle), 4)
        self.orthogonal_angle_vector.y_value = round(math.sin(self.angle - math.pi / 2), 4)

    def calculate_angle(self):
        self.calculate_angle_x()
        self.calculate_angle_y()
        self.turn()

    def turn(self):
        """
        Must be defined in Child-Class
        :return:
        """
        pass