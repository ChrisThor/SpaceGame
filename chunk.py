import pygame
import block
import vector
import random


class Chunk:
    def __init__(self, position=vector.Vector(), size=16):
        self.position = position
        self.blocks = []
        self.size = size
        if random.randint(0, 4) == 4:
            solid = False
        else:
            solid = True
        for i in range(size):
            buffer = []
            for j in range(size):
                buffer.append(block.Block(vector.Vector(i, j), self,
                                          (random.randint(0, 123), random.randint(0, 255), random.randint(0, 255)),
                                          solid=solid))
            self.blocks.append(buffer)

    def draw_chunk(self, background, center_x, center_y, zoom_factor, player):
        for block_line in self.blocks:
            for b in block_line:
                if b.solid:
                    relative_distance_to_player = \
                        ((self.position * self.size * b.size + b.position * b.size) - player.position) * zoom_factor
                    pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
                    pos_y_on_screen = int(
                        center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2)

                    if b.alternate_colour is None:
                        pygame.draw.rect(background,
                                         b.colour,
                                         (pos_x_on_screen, pos_y_on_screen,
                                          b.size * zoom_factor, b.size * zoom_factor))
                    else:
                        pygame.draw.rect(background,
                                         b.alternate_colour,
                                         (pos_x_on_screen, pos_y_on_screen,
                                          b.size * zoom_factor, b.size * zoom_factor))
                        b.alternate_colour = None
