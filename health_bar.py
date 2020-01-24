import pygame


class HealthBar:
    def __init__(self, hp, width):
        self.hp = hp
        self.max_hp = hp
        self.width = width

    def draw_bar(self, background, zoom_factor, pos_x_on_screen, pos_y_on_screen, radius):
        pygame.draw.rect(background,
                         (255, 0, 0),
                         (pos_x_on_screen - self.width * zoom_factor / 2,
                          pos_y_on_screen - radius * zoom_factor * 2,
                          (self.hp / self.max_hp) * self.width * zoom_factor,
                          2 * zoom_factor))

    def __add__(self, other):
        self.hp += other.hp
        self.max_hp += other.max_hp
        # self.width += other.width
        return self
