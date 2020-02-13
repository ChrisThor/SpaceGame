import pygame


class BlueprintObject:
    def __init__(self, texture, object_id, path):
        self.object_id = object_id
        self.path = path
        self.position = None
        self.texture = texture
        self.flip_texture = False
        self.size = texture.get_size()

    def draw_blueprint(self, background, player, zoom_factor, center_x, center_y, position, block_size, flip):
        self.flip_texture = flip
        zoom = zoom_factor * block_size
        relative_distance_to_player = (position - player.position) * zoom
        self.position = position
        position_on_screen = (center_x + relative_distance_to_player.x_value,
                              center_y + relative_distance_to_player.y_value - self.size[1] / 2 * zoom_factor - zoom / 4)
        texture = pygame.transform.flip(self.texture, flip, False)

        background.blit(pygame.transform.scale(texture,
                                               (int(self.size[0] * zoom_factor), int(self.size[1] * zoom_factor))),
                        position_on_screen)
