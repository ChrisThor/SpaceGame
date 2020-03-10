import vector
import pygame


class NewPlanet:
    def __init__(self, position):
        self.position = position
        self.radius = 10
        self.speed = vector.Vector()
        self.particle_colour = (50, 50, 255)
        self.particle_lifetime = 8
        self.mass = 1e14
        self.visible = True
        self.static = False

    def change_radius(self, value):
        if self.radius + value > 3:
            self.radius += value

    def change_mass(self, value):
        self.mass += value * 5e12

    def change_size(self, value):
        self.change_radius(value)

    def draw_speed_vector(self, background, zoom_factor, pos_x_on_screen, pos_y_on_screen):
        pygame.draw.line(background,
                         (120, 120, 255),
                         (pos_x_on_screen, pos_y_on_screen),
                         (pos_x_on_screen + self.speed.x_value * zoom_factor,
                          pos_y_on_screen + self.speed.y_value * zoom_factor))
