import pygame


class MiningDevice:
    def __init__(self, size, speed):
        self.position = None
        self.size = size
        self.original_size = size
        self.mining_speed = speed
        self.mode = 0

    def draw_affected_area(self, background, zoom, player, center_x, center_y):
        surface = pygame.Surface((int(zoom * self.size), int(zoom * self.size)))
        surface.fill((255, 50, 50))
        surface.set_alpha(175)

        relative_distance_to_player = (self.position - player.position) * zoom
        screen_position = (center_x + relative_distance_to_player.x_value,
                           center_y + relative_distance_to_player.y_value + player.height * zoom / 2)
        background.blit(surface, screen_position)

    def update_position(self, position):
        self.position = position
