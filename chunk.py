import pygame
import block
import vector
import random


class Chunk:
    def __init__(self, position=vector.Vector(), size=16, block_size=8):
        self.position = position
        self.blocks = []
        self.size = size
        solid = True
        if position.y_value < 0:
            solid = False
        for i in range(size):
            buffer = []
            for j in range(size):
                buffer.append(block.Block(vector.Vector(self.position.x_value * self.size + i,
                                                        self.position.y_value * self.size + j),
                                          size=block_size,
                                          chunk=self,
                                          colour=(random.randint(0, 123), random.randint(0, 255), random.randint(0, 255)),
                                          solid=solid))
            self.blocks.append(buffer)

    def draw_chunk(self, background, center_x, center_y, zoom_factor, player):
        for block_line in self.blocks:
            for b in block_line:
                if b.solid:
                    relative_distance_to_player = (b.position - player.position) * zoom_factor * b.size
                    pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
                    pos_y_on_screen = int(
                        center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2 * b.size)

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
