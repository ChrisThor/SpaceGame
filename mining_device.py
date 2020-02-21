import pygame


class MiningDevice:
    def __init__(self, size, speed):
        self.position = None
        self.size = size
        self.original_size = size
        self.mining_speed = speed
        self.zoom = None
        self.surface = None
        self.mode = 0
        self.tool = 0

    def draw_affected_area(self, background, zoom, player, center_x, center_y):
        if self.zoom is not None:
            if self.zoom != zoom:
                self.set_surface(zoom)
        else:
            self.set_surface(zoom)

        relative_distance_to_player = (self.position - player.position) * zoom
        screen_position = (center_x + relative_distance_to_player.x_value,
                           center_y + relative_distance_to_player.y_value + player.height * zoom / 2)
        background.blit(self.surface, screen_position)

    def set_surface(self, zoom):
        self.surface = pygame.Surface((int(zoom * self.size), int(zoom * self.size)))
        self.surface.fill((255, 50, 50))
        self.surface.set_alpha(175)
        self.zoom = zoom

    def update_position(self, position):
        self.position = position
