import pygame


class MiningDevice:
    def __init__(self, size, speed):
        self.position = None
        self.mining_size = size
        self.building_size = size
        self.original_mining_size = size
        self.original_building_size = size
        self.mining_speed = speed
        self.zoom = None
        self.surface = None
        self.mode = 0
        self.tool = 0
        self.texture_set = False

    def draw_affected_area(self, background, zoom, player, center_x, center_y, textures):
        if player.block is not None and not self.texture_set:
            self.texture_set = True
            self.set_surface(zoom, player, textures)
        if self.zoom is not None:
            if self.zoom != zoom:
                self.set_surface(zoom, player, textures)
        else:
            self.set_surface(zoom, player, textures)

        relative_distance_to_player = (self.position - player.position) * zoom
        screen_position = (center_x + relative_distance_to_player.x_value,
                           center_y + relative_distance_to_player.y_value + player.height * zoom / 2)
        background.blit(self.surface, screen_position)

    def set_surface(self, zoom, player, textures):
        if self.tool == 1:
            if player.block is not None:
                self.surface = pygame.Surface((int(zoom * self.building_size), int(zoom * self.building_size)), pygame.SRCALPHA, 32)
                for i in range(self.building_size):
                    for j in range(self.building_size):
                        self.surface.blit(pygame.transform.scale(textures[player.block["texture"]], (zoom, zoom)),
                                          (i * zoom, j * zoom))
            else:
                self.surface = pygame.Surface((int(zoom * self.building_size), int(zoom * self.building_size)))
                self.surface.set_alpha(0)
        else:
            self.surface = pygame.Surface((int(zoom * self.mining_size), int(zoom * self.mining_size)))
            self.surface.fill((255, 50, 50))
            self.surface.set_alpha(175)
        self.zoom = zoom

    def update_position(self, position):
        self.position = position
