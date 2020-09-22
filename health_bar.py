import pygame


class HealthBar:
    def __init__(self, hp, width, colour=(255, 0, 0), show_border=False, border_colour=(0, 0, 0)):
        self.hp = hp
        self.max_hp = hp
        self.width = width
        self.colour = colour
        self.show_border = show_border
        self.border_colour = border_colour

    def draw_bar(self, background, zoom_factor, pos_x_on_screen, pos_y_on_screen, radius):
        if self.show_border:
            pygame.draw.rect(background,
                             self.border_colour,
                             (pos_x_on_screen - self.width * zoom_factor / 2 - 1,
                              pos_y_on_screen - radius * zoom_factor * 2 - 1,
                              self.width * zoom_factor + 2,
                              2 * zoom_factor + 2),
                             1)
        if self.hp > 0:
            pygame.draw.rect(background,
                             self.colour,
                             (pos_x_on_screen - self.width * zoom_factor / 2,
                              pos_y_on_screen - radius * zoom_factor * 2,
                              (self.hp / self.max_hp) * self.width * zoom_factor,
                              2 * zoom_factor))

    def reduce_hp(self, difference):
        self.hp -= difference
        if self.hp < 0:
            self.hp = 0

    def __add__(self, other):
        self.hp += other.hp
        self.max_hp += other.max_hp
        # self.width += other.width
        return self
