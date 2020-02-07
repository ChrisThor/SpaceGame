import pygame
import block
import vector
import math
import random


class Chunk:
    def __init__(self, textures, world_information, chunk_index, position=vector.Vector(), size=16, block_size=8):
        self.position = position
        self.block_offset = None
        self.blocks = []
        self.state = 0
        self.size = size
        solid = True
        if position.y_value < 0:
            solid = False
        for i in range(size):
            buffer = []
            for j in range(size):
                foreground_block = block.Block(vector.Vector(self.position.x_value * self.size + i,
                                                             self.position.y_value * self.size + j),
                                               size=block_size,
                                               chunk=self,
                                               texture=textures["test1"],
                                               block_information=world_information[chunk_index * self.size - i],
                                               colour=(
                                               random.randint(0, 123), random.randint(0, 255), random.randint(0, 255)),
                                               solid=solid)
                background_block = block.Block(vector.Vector(self.position.x_value * self.size + i,
                                                             self.position.y_value * self.size + j),
                                               size=block_size,
                                               chunk=self,
                                               texture=textures["test1"],
                                               block_information=world_information[chunk_index * self.size - i],
                                               colour=(
                                               random.randint(0, 123), random.randint(0, 255), random.randint(0, 255)),
                                               solid=solid,
                                               max_brightness=0.6)
                buffer.append([foreground_block, background_block])
            self.blocks.append(buffer)

    def draw_chunk_foreground(self, background, center_x, center_y, zoom_factor, player):
        if self.state == 0:
            for block_line in self.blocks:
                for bloq in block_line:
                    if bloq[0].solid:
                        bloq[0].draw_block(background, center_x, center_y, player, zoom_factor, self.block_offset)

    def draw_chunk_background(self, background, center_x, center_y, zoom_factor, player, colour):
        if self.state != 2:
            if self.state == 0:
                for block_line in self.blocks:
                    for bloq in block_line:
                        if bloq[1].solid and not bloq[0].solid:
                            bloq[1].draw_block(background, center_x, center_y, player, zoom_factor, self.block_offset)
            else:
                self.draw_black_chunk(background, center_x, center_y, player, zoom_factor, colour)

    def get_block_relative_to_block(self, bloq, active_chunks, x_offset=0, y_offset=0):
        try:
            chunk_x = math.floor((bloq.position.x_value + x_offset) / self.size)
            chunk_y = math.floor((bloq.position.y_value + y_offset) / self.size)
            if self.position.x_value == chunk_x and self.position.y_value == chunk_y:
                return self.blocks[(bloq.position.x_value + x_offset) % self.size][
                    (bloq.position.y_value + y_offset) % self.size]
            else:
                for chunk in active_chunks:
                    if chunk.position.x_value == chunk_x and chunk.position.y_value == chunk_y:
                        return chunk.get_block_relative_to_block(bloq, active_chunks, x_offset, y_offset)
        except IndexError:
            return None

    def draw_black_chunk(self, background, center_x, center_y, player, zoom_factor, colour):
        block_size = self.blocks[0][0][0].size
        if self.block_offset is None:
            relative_distance_to_player = (self.position * self.size - player.position) * zoom_factor * block_size
            pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
            pos_y_on_screen = int(
                center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2 * block_size)
        else:
            position = self.position.copy()
            position.x_value += self.block_offset / self.size
            relative_distance_to_player = (position * self.size - player.position) * zoom_factor * block_size
            pos_x_on_screen = int(center_x + relative_distance_to_player.x_value)
            pos_y_on_screen = int(
                center_y + relative_distance_to_player.y_value + player.height * zoom_factor / 2 * block_size)
        pygame.draw.rect(background,
                         colour,
                         (pos_x_on_screen, pos_y_on_screen,
                          self.size * block_size * zoom_factor, self.size * block_size * zoom_factor))
