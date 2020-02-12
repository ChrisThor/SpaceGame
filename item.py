import pygame


class Item:
    def __init__(self, textures, name="", description="", hardness=0, droppable=False):
        self.name = name
        self.description = description
        self.droppable = droppable
        self.textures = textures
        self.current_texture = textures[0]
        self.hardness = hardness

    def draw_as_block_content(self, background, pos_x_on_screen, pos_y_on_screen, zoom):
        background.blit(pygame.transform.scale(self.current_texture, (zoom, zoom)), (pos_x_on_screen, pos_y_on_screen))
